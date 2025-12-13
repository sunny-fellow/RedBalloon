import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Plus, Save, Trash2, X } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TagBadge } from '@/components/ui/TagBadge';
import { problemTags } from '@/data/mockData';
import { CodeEditor } from '@/components/common/CodeEditor';

interface TestCase {
  id: string;
  input: string;
  expectedOutput: string;
}

export default function ProblemCreate() {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [validationMode, setValidationMode] = useState('expected');
  const [testCases, setTestCases] = useState<TestCase[]>([{ id: '1', input: '', expectedOutput: '' }]);
  const [checkerCode, setCheckerCode] = useState('');
  const [inputs, setInputs] = useState<{ id: string; value: string }[]>([{ id: '1', value: '' }]);

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

  return (
    <PageContainer>
      <Link to="/home">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      <h1 className="text-2xl font-bold mb-6 gradient-text" style={{ fontFamily: 'Orbitron, sans-serif' }}>
        Criar Problema
      </h1>
      
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column - Basic Info */}
        <div className="lg:col-span-2 space-y-4">
          <div className="space-y-2">
            <Label>Título</Label>
            <Input placeholder="Título do problema" className="bg-input" />
          </div>
          
          <div className="space-y-2">
            <Label>Descrição (Markdown)</Label>
            <Textarea 
              placeholder="Descreva o problema em detalhes..." 
              className="min-h-[200px] bg-input font-mono" 
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Tempo Limite (ms)</Label>
              <Input type="number" defaultValue={1000} className="bg-input" />
            </div>
            <div className="space-y-2">
              <Label>Memória Limite (MB)</Label>
              <Input type="number" defaultValue={256} className="bg-input" />
            </div>
          </div>
          
          <div className="space-y-2">
            <Label>Dificuldade</Label>
            <Select>
              <SelectTrigger className="bg-input">
                <SelectValue placeholder="Selecione" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="easy">Fácil</SelectItem>
                <SelectItem value="medium">Médio</SelectItem>
                <SelectItem value="hard">Difícil</SelectItem>
              </SelectContent>
            </Select>
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
                />
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Validation */}
        <div className="space-y-4">
          <Card className="arcade-card">
            <CardHeader>
              <CardTitle className="text-lg" style={{ fontFamily: 'Orbitron, sans-serif' }}>
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
                <TabsContent value="expected" className="space-y-4">
                  <p className="text-sm text-muted-foreground">
                    Adicione casos de teste com entrada e saída esperada.
                  </p>
                  
                  <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                    {testCases.map((tc, index) => (
                      <Card key={tc.id} className="bg-background/50 border-border/50">
                        <CardContent className="p-4 space-y-3">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-[hsl(var(--neon-cyan))]">
                              Caso {index + 1}
                            </span>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              onClick={() => removeTestCase(tc.id)}
                              disabled={testCases.length === 1}
                              className="h-6 w-6 text-destructive hover:text-destructive"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                          <div className="space-y-2">
                            <Label className="text-xs">Entrada</Label>
                            <Textarea 
                              value={tc.input}
                              onChange={(e) => updateTestCase(tc.id, 'input', e.target.value)}
                              placeholder="Entrada do caso de teste..."
                              className="bg-input font-mono text-sm min-h-[80px]"
                            />
                          </div>
                          <div className="space-y-2">
                            <Label className="text-xs">Saída Esperada</Label>
                            <Textarea 
                              value={tc.expectedOutput}
                              onChange={(e) => updateTestCase(tc.id, 'expectedOutput', e.target.value)}
                              placeholder="Saída esperada..."
                              className="bg-input font-mono text-sm min-h-[80px]"
                            />
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                  
                  <Button 
                    variant="outline" 
                    onClick={addTestCase}
                    className="w-full gap-2 border-dashed border-[hsl(var(--neon-purple)/0.5)]"
                  >
                    <Plus className="h-4 w-4" />
                    Adicionar Caso de Teste
                  </Button>
                </TabsContent>

                {/* Mode 2: Checker Algorithm */}
                <TabsContent value="checker" className="space-y-4">
                  <p className="text-sm text-muted-foreground">
                    Forneça um algoritmo que verifica se a resposta é válida. 
                    Retorne 1 para aceito, 0 para rejeitado.
                  </p>
                  
                  {/* Inputs for checker mode */}
                  <div className="space-y-3">
                    <Label>Entradas de Teste</Label>
                    <div className="space-y-2 max-h-[150px] overflow-y-auto">
                      {inputs.map((input, index) => (
                        <div key={input.id} className="flex gap-2">
                          <div className="flex-1">
                            <Textarea
                              value={input.value}
                              onChange={(e) => updateInput(input.id, e.target.value)}
                              placeholder={`Entrada ${index + 1}...`}
                              className="bg-input font-mono text-sm min-h-[60px]"
                            />
                          </div>
                          <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => removeInput(input.id)}
                            disabled={inputs.length === 1}
                            className="text-destructive hover:text-destructive h-8 w-8"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={addInput}
                      className="gap-1 border-dashed"
                    >
                      <Plus className="h-3 w-3" />
                      Adicionar Entrada
                    </Button>
                  </div>

                  <div className="space-y-2">
                    <Label>Algoritmo Checker</Label>
                    <div className="border border-border/50 rounded-lg overflow-hidden h-[200px]">
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
                <TabsContent value="none" className="space-y-4">
                  <p className="text-sm text-muted-foreground">
                    Sem validação automática. Apenas o enunciado do problema será exibido.
                  </p>
                  
                  {/* Optional inputs */}
                  <div className="space-y-3">
                    <Label>Entradas de Exemplo (Opcional)</Label>
                    <div className="space-y-2 max-h-[200px] overflow-y-auto">
                      {inputs.map((input, index) => (
                        <div key={input.id} className="flex gap-2">
                          <div className="flex-1">
                            <Textarea
                              value={input.value}
                              onChange={(e) => updateInput(input.id, e.target.value)}
                              placeholder={`Exemplo ${index + 1}...`}
                              className="bg-input font-mono text-sm min-h-[60px]"
                            />
                          </div>
                          <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => removeInput(input.id)}
                            disabled={inputs.length === 1}
                            className="text-destructive hover:text-destructive h-8 w-8"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={addInput}
                      className="gap-1 border-dashed"
                    >
                      <Plus className="h-3 w-3" />
                      Adicionar Exemplo
                    </Button>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
          
          <Button className="w-full gap-2 arcade-button">
            <Save className="h-4 w-4" />
            Criar Problema
          </Button>
        </div>
      </div>
    </PageContainer>
  );
}
