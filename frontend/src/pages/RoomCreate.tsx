import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, Save, Trash2, Search, X } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { mockProblems, problemTags, BALLOON_COLORS } from '@/data/mockData';
import { Problem } from '@/types';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { TagBadge } from '@/components/ui/TagBadge';
import { BalloonBadge } from '@/components/ui/BalloonBadge';
import { CodeEditor } from '@/components/common/CodeEditor';
import { useToast } from '@/hooks/use-toast';

interface RoomProblemItem {
  problem: Problem;
  points: number;
  balloonColor: string;
}

interface TestCase {
  id: string;
  input: string;
  expectedOutput: string;
}

export default function RoomCreate() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isPrivate, setIsPrivate] = useState(false);
  const [selectedProblems, setSelectedProblems] = useState<RoomProblemItem[]>([]);
  const [problemDialogOpen, setProblemDialogOpen] = useState(false);
  const [searchProblem, setSearchProblem] = useState('');

  // New problem form state
  const [newProblem, setNewProblem] = useState({
    title: '',
    description: '',
    timeLimit: 1000,
    memoryLimit: 256,
    difficulty: 'medium' as Problem['difficulty']
  });
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [validationMode, setValidationMode] = useState('expected');
  const [testCases, setTestCases] = useState<TestCase[]>([{ id: '1', input: '', expectedOutput: '' }]);
  const [checkerCode, setCheckerCode] = useState('');
  const [inputs, setInputs] = useState<{ id: string; value: string }[]>([{ id: '1', value: '' }]);

  const availableProblems = mockProblems.filter(
    p => !selectedProblems.some(sp => sp.problem.id === p.id)
  ).filter(
    p => p.title.toLowerCase().includes(searchProblem.toLowerCase()) ||
         p.id.includes(searchProblem)
  );

  const addProblem = (problem: Problem) => {
    const colorIndex = selectedProblems.length % BALLOON_COLORS.length;
    setSelectedProblems([...selectedProblems, { 
      problem, 
      points: 10, 
      balloonColor: BALLOON_COLORS[colorIndex].value 
    }]);
    setProblemDialogOpen(false);
  };

  const removeProblem = (problemId: string) => {
    setSelectedProblems(selectedProblems.filter(p => p.problem.id !== problemId));
  };

  const updateProblemPoints = (problemId: string, points: number) => {
    setSelectedProblems(selectedProblems.map(p => 
      p.problem.id === problemId ? { ...p, points } : p
    ));
  };

  const updateProblemBalloonColor = (problemId: string, balloonColor: string) => {
    setSelectedProblems(selectedProblems.map(p => 
      p.problem.id === problemId ? { ...p, balloonColor } : p
    ));
  };

  const toggleTag = (tag: string) => setSelectedTags(prev => 
    prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
  );

  const addTestCase = () => {
    setTestCases([...testCases, { id: Date.now().toString(), input: '', expectedOutput: '' }]);
  };

  const removeTestCase = (id: string) => {
    if (testCases.length > 1) {
      setTestCases(testCases.filter(tc => tc.id !== id));
    }
  };

  const updateTestCase = (id: string, field: 'input' | 'expectedOutput', value: string) => {
    setTestCases(testCases.map(tc => tc.id === id ? { ...tc, [field]: value } : tc));
  };

  const addInput = () => {
    setInputs([...inputs, { id: Date.now().toString(), value: '' }]);
  };

  const removeInput = (id: string) => {
    if (inputs.length > 1) {
      setInputs(inputs.filter(i => i.id !== id));
    }
  };

  const updateInput = (id: string, value: string) => {
    setInputs(inputs.map(i => i.id === id ? { ...i, value } : i));
  };

  const resetProblemForm = () => {
    setNewProblem({ title: '', description: '', timeLimit: 1000, memoryLimit: 256, difficulty: 'medium' });
    setSelectedTags([]);
    setValidationMode('expected');
    setTestCases([{ id: '1', input: '', expectedOutput: '' }]);
    setCheckerCode('');
    setInputs([{ id: '1', value: '' }]);
  };

  const createCustomProblem = () => {
    if (!newProblem.title.trim()) {
      toast({ title: 'Erro', description: 'Título é obrigatório', variant: 'destructive' });
      return;
    }

    const customProblem: Problem = {
      id: `custom-${Date.now()}`,
      title: newProblem.title,
      description: newProblem.description,
      difficulty: newProblem.difficulty,
      timeLimit: newProblem.timeLimit,
      memoryLimit: newProblem.memoryLimit,
      creatorId: '1',
      creatorName: 'Você',
      tags: selectedTags,
      attempts: 0,
      solved: 0,
      likes: 0,
      dislikes: 0,
      createdAt: new Date().toISOString()
    };

    const colorIndex = selectedProblems.length % BALLOON_COLORS.length;
    setSelectedProblems([...selectedProblems, { 
      problem: customProblem, 
      points: 10, 
      balloonColor: BALLOON_COLORS[colorIndex].value 
    }]);
    
    resetProblemForm();
    setProblemDialogOpen(false);
    toast({ title: 'Problema criado!', description: 'Problema adicionado à sala.' });
  };

  const handleCreateRoom = () => {
    toast({ title: 'Sala criada!', description: 'Redirecionando para o lobby...' });
    navigate('/room/lobby');
  };

  return (
    <PageContainer>
      <Link to="/rooms">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      
      <h1 className="text-2xl font-bold mb-6 gradient-text" style={{ fontFamily: 'Orbitron, sans-serif' }}>
        Criar Sala
      </h1>
      
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Left Column - Room Info */}
        <div className="space-y-4">
          <div className="space-y-2">
            <Label>Nome da Sala</Label>
            <Input placeholder="Nome da sala" className="bg-input" />
          </div>
          
          <div className="space-y-2">
            <Label>Descrição</Label>
            <Textarea placeholder="Descrição da sala..." className="bg-input" />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Capacidade</Label>
              <Input type="number" defaultValue={20} className="bg-input" />
            </div>
            <div className="space-y-2">
              <Label>Duração (min)</Label>
              <Input type="number" defaultValue={120} className="bg-input" />
            </div>
          </div>
          
          <div className="flex items-center justify-between p-4 rounded-lg arcade-card">
            <div>
              <Label>Sala Privada</Label>
              <p className="text-sm text-muted-foreground">Exigir senha para entrar</p>
            </div>
            <Switch checked={isPrivate} onCheckedChange={setIsPrivate} />
          </div>
          
          {isPrivate && (
            <div className="space-y-2">
              <Label>Senha</Label>
              <Input type="password" placeholder="Senha da sala" className="bg-input" />
            </div>
          )}
        </div>

        {/* Right Column - Problems */}
        <Card className="arcade-card">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Problemas</CardTitle>
            <span className="text-sm text-muted-foreground">
              {selectedProblems.length} selecionado(s)
            </span>
          </CardHeader>
          <CardContent className="space-y-3">
            {selectedProblems.length === 0 ? (
              <p className="text-center text-muted-foreground py-8">
                Nenhum problema adicionado ainda
              </p>
            ) : (
              <ScrollArea className="h-[300px] pr-4">
                <div className="space-y-3">
                  {selectedProblems.map((item, index) => (
                    <div 
                      key={item.problem.id} 
                      className="flex items-center justify-between p-3 rounded-lg bg-background/50 border border-border/50"
                    >
                      <div className="flex items-center gap-3 flex-1 min-w-0">
                        <BalloonBadge color={item.balloonColor} size="md" />
                        <div className="min-w-0">
                          <p className="font-medium truncate">{item.problem.title}</p>
                          <p className="text-xs text-muted-foreground">
                            {item.problem.id.startsWith('custom-') ? 'Personalizado' : `#${item.problem.id}`}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Input 
                          type="number" 
                          value={item.points}
                          onChange={(e) => updateProblemPoints(item.problem.id, parseInt(e.target.value) || 0)}
                          className="w-16 h-8 bg-input text-center"
                        />
                        <Select 
                          value={item.balloonColor}
                          onValueChange={(v) => updateProblemBalloonColor(item.problem.id, v)}
                        >
                          <SelectTrigger className="w-24 h-8 bg-input">
                            <BalloonBadge color={item.balloonColor} size="sm" showLabel />
                          </SelectTrigger>
                          <SelectContent>
                            {BALLOON_COLORS.map(b => (
                              <SelectItem key={b.value} value={b.value}>
                                <div className="flex items-center gap-2">
                                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: b.hex }} />
                                  {b.label}
                                </div>
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <Button 
                          variant="ghost" 
                          size="icon"
                          onClick={() => removeProblem(item.problem.id)}
                          className="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            )}
            
            <Button 
              variant="outline" 
              onClick={() => setProblemDialogOpen(true)}
              className="w-full gap-2 border-dashed border-[hsl(var(--neon-purple)/0.5)]"
            >
              <Plus className="h-4 w-4" />
              Adicionar Problema
            </Button>
          </CardContent>
        </Card>
      </div>
      
      <Button onClick={handleCreateRoom} className="mt-6 gap-2 arcade-button">
        <Save className="h-4 w-4" />
        Criar Sala
      </Button>

      {/* Dialog: Add Problem */}
      <Dialog open={problemDialogOpen} onOpenChange={(open) => { setProblemDialogOpen(open); if (!open) resetProblemForm(); }}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Adicionar Problema</DialogTitle>
          </DialogHeader>
          
          <Tabs defaultValue="existing">
            <TabsList className="grid grid-cols-2">
              <TabsTrigger value="existing">Problemas Existentes</TabsTrigger>
              <TabsTrigger value="create">Criar Novo</TabsTrigger>
            </TabsList>
            
            <TabsContent value="existing" className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input 
                  placeholder="Buscar por título ou ID..."
                  value={searchProblem}
                  onChange={(e) => setSearchProblem(e.target.value)}
                  className="pl-10 bg-input"
                />
              </div>
              
              <ScrollArea className="h-[300px]">
                <div className="space-y-2">
                  {availableProblems.length === 0 ? (
                    <p className="text-center text-muted-foreground py-8">
                      Nenhum problema encontrado
                    </p>
                  ) : (
                    availableProblems.map(problem => (
                      <div 
                        key={problem.id}
                        onClick={() => addProblem(problem)}
                        className="flex items-center justify-between p-3 rounded-lg border border-border/50 hover:border-[hsl(var(--neon-purple)/0.5)] hover:bg-card/50 cursor-pointer transition-all"
                      >
                        <div>
                          <p className="font-medium">{problem.title}</p>
                          <p className="text-sm text-muted-foreground">
                            #{problem.id} • {problem.creatorName}
                          </p>
                        </div>
                        <DifficultyBadge difficulty={problem.difficulty} />
                      </div>
                    ))
                  )}
                </div>
              </ScrollArea>
            </TabsContent>
            
            <TabsContent value="create" className="space-y-4">
              <div className="grid lg:grid-cols-2 gap-6">
                {/* Left - Basic info */}
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Título</Label>
                    <Input 
                      placeholder="Título do problema"
                      value={newProblem.title}
                      onChange={(e) => setNewProblem({ ...newProblem, title: e.target.value })}
                      className="bg-input"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Descrição (Markdown)</Label>
                    <Textarea 
                      placeholder="Descrição do problema..."
                      value={newProblem.description}
                      onChange={(e) => setNewProblem({ ...newProblem, description: e.target.value })}
                      className="bg-input min-h-[120px] font-mono"
                    />
                  </div>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label>Tempo (ms)</Label>
                      <Input 
                        type="number"
                        value={newProblem.timeLimit}
                        onChange={(e) => setNewProblem({ ...newProblem, timeLimit: parseInt(e.target.value) || 1000 })}
                        className="bg-input"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Memória (MB)</Label>
                      <Input 
                        type="number"
                        value={newProblem.memoryLimit}
                        onChange={(e) => setNewProblem({ ...newProblem, memoryLimit: parseInt(e.target.value) || 256 })}
                        className="bg-input"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Dificuldade</Label>
                      <Select 
                        value={newProblem.difficulty}
                        onValueChange={(v) => setNewProblem({ ...newProblem, difficulty: v as Problem['difficulty'] })}
                      >
                        <SelectTrigger className="bg-input">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="easy">Fácil</SelectItem>
                          <SelectItem value="medium">Médio</SelectItem>
                          <SelectItem value="hard">Difícil</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Tags</Label>
                    <div className="flex flex-wrap gap-2">
                      {problemTags.map(t => (
                        <TagBadge 
                          key={t.id} 
                          tag={t.name} 
                          color={t.color as any} 
                          onClick={() => toggleTag(t.name)} 
                          selected={selectedTags.includes(t.name)} 
                          size="sm"
                        />
                      ))}
                    </div>
                  </div>
                </div>

                {/* Right - Validation */}
                <Card className="arcade-card">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                      Modo de Validação
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Tabs value={validationMode} onValueChange={setValidationMode}>
                      <TabsList className="grid grid-cols-3 mb-4">
                        <TabsTrigger value="expected">Saída</TabsTrigger>
                        <TabsTrigger value="checker">Checker</TabsTrigger>
                        <TabsTrigger value="none">Nenhum</TabsTrigger>
                      </TabsList>

                      {/* Mode 1: Expected Output */}
                      <TabsContent value="expected" className="space-y-3">
                        <p className="text-xs text-muted-foreground">
                          Adicione casos de teste com entrada e saída esperada.
                        </p>
                        
                        <ScrollArea className="h-[250px] pr-2">
                          <div className="space-y-3">
                            {testCases.map((tc, index) => (
                              <Card key={tc.id} className="bg-background/50 border-border/50">
                                <CardContent className="p-3 space-y-2">
                                  <div className="flex items-center justify-between">
                                    <span className="text-xs font-medium text-[hsl(var(--neon-cyan))]">
                                      Caso {index + 1}
                                    </span>
                                    <Button 
                                      variant="ghost" 
                                      size="icon" 
                                      onClick={() => removeTestCase(tc.id)}
                                      disabled={testCases.length === 1}
                                      className="h-5 w-5 text-destructive hover:text-destructive"
                                    >
                                      <Trash2 className="h-3 w-3" />
                                    </Button>
                                  </div>
                                  <div className="space-y-1">
                                    <Label className="text-xs">Entrada</Label>
                                    <Textarea 
                                      value={tc.input}
                                      onChange={(e) => updateTestCase(tc.id, 'input', e.target.value)}
                                      placeholder="Entrada..."
                                      className="bg-input font-mono text-xs min-h-[50px]"
                                    />
                                  </div>
                                  <div className="space-y-1">
                                    <Label className="text-xs">Saída Esperada</Label>
                                    <Textarea 
                                      value={tc.expectedOutput}
                                      onChange={(e) => updateTestCase(tc.id, 'expectedOutput', e.target.value)}
                                      placeholder="Saída esperada..."
                                      className="bg-input font-mono text-xs min-h-[50px]"
                                    />
                                  </div>
                                </CardContent>
                              </Card>
                            ))}
                          </div>
                        </ScrollArea>
                        
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={addTestCase}
                          className="w-full gap-2 border-dashed border-[hsl(var(--neon-purple)/0.5)]"
                        >
                          <Plus className="h-3 w-3" />
                          Adicionar Caso
                        </Button>
                      </TabsContent>

                      {/* Mode 2: Checker Algorithm */}
                      <TabsContent value="checker" className="space-y-3">
                        <p className="text-xs text-muted-foreground">
                          Forneça um algoritmo que verifica se a resposta é válida.
                        </p>
                        
                        <div className="space-y-2">
                          <Label className="text-xs">Entradas de Teste</Label>
                          <ScrollArea className="h-[100px]">
                            <div className="space-y-2 pr-2">
                              {inputs.map((input, index) => (
                                <div key={input.id} className="flex gap-2">
                                  <Textarea
                                    value={input.value}
                                    onChange={(e) => updateInput(input.id, e.target.value)}
                                    placeholder={`Entrada ${index + 1}...`}
                                    className="bg-input font-mono text-xs min-h-[40px] flex-1"
                                  />
                                  <Button 
                                    variant="ghost" 
                                    size="icon"
                                    onClick={() => removeInput(input.id)}
                                    disabled={inputs.length === 1}
                                    className="text-destructive hover:text-destructive h-6 w-6"
                                  >
                                    <X className="h-3 w-3" />
                                  </Button>
                                </div>
                              ))}
                            </div>
                          </ScrollArea>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={addInput}
                            className="gap-1 border-dashed"
                          >
                            <Plus className="h-3 w-3" />
                            Adicionar
                          </Button>
                        </div>

                        <div className="space-y-2">
                          <Label className="text-xs">Algoritmo Checker</Label>
                          <div className="border border-border/50 rounded-lg overflow-hidden h-[120px]">
                            <CodeEditor 
                              value={checkerCode}
                              onChange={setCheckerCode}
                              language="cpp"
                              onLanguageChange={() => {}}
                            />
                          </div>
                        </div>
                      </TabsContent>

                      {/* Mode 3: No validation */}
                      <TabsContent value="none" className="space-y-3">
                        <p className="text-xs text-muted-foreground">
                          Sem validação automática. Adicione entradas de exemplo opcionais.
                        </p>
                        
                        <div className="space-y-2">
                          <Label className="text-xs">Entradas de Exemplo (Opcional)</Label>
                          <ScrollArea className="h-[150px]">
                            <div className="space-y-2 pr-2">
                              {inputs.map((input, index) => (
                                <div key={input.id} className="flex gap-2">
                                  <Textarea
                                    value={input.value}
                                    onChange={(e) => updateInput(input.id, e.target.value)}
                                    placeholder={`Exemplo ${index + 1}...`}
                                    className="bg-input font-mono text-xs min-h-[40px] flex-1"
                                  />
                                  <Button 
                                    variant="ghost" 
                                    size="icon"
                                    onClick={() => removeInput(input.id)}
                                    disabled={inputs.length === 1}
                                    className="text-destructive hover:text-destructive h-6 w-6"
                                  >
                                    <X className="h-3 w-3" />
                                  </Button>
                                </div>
                              ))}
                            </div>
                          </ScrollArea>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={addInput}
                            className="gap-1 border-dashed"
                          >
                            <Plus className="h-3 w-3" />
                            Adicionar
                          </Button>
                        </div>
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                </Card>
              </div>
              
              <DialogFooter>
                <Button onClick={createCustomProblem} className="arcade-button">
                  <Plus className="h-4 w-4 mr-2" />
                  Criar e Adicionar
                </Button>
              </DialogFooter>
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </PageContainer>
  );
}
