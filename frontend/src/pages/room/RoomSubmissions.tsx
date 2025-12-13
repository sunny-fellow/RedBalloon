import { useState } from 'react';
import { Filter, X } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Pagination } from '@/components/common/Pagination';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Search } from 'lucide-react';
import { mockSubmissions, mockRooms, languages } from '@/data/mockData';
import { Submission } from '@/types';

const statusOptions = [
  { value: 'accepted', label: 'Aceito', color: 'text-neon-green' },
  { value: 'wrong_answer', label: 'Resposta Errada', color: 'text-destructive' },
  { value: 'time_limit', label: 'Tempo Limite', color: 'text-neon-orange' },
  { value: 'runtime_error', label: 'Erro de Execução', color: 'text-neon-pink' },
  { value: 'compile_error', label: 'Erro de Compilação', color: 'text-muted-foreground' },
];

const languageLabels: Record<string, string> = {
  java: 'Java',
  python: 'Python',
  c: 'C',
  cpp: 'C++',
};

export default function RoomSubmissions() {
  const room = mockRooms[0];
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [filterDialogOpen, setFilterDialogOpen] = useState(false);
  
  // Filter states
  const [selectedProblems, setSelectedProblems] = useState<string[]>([]);
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>([]);
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>([]);
  
  // Temp filter states (for dialog)
  const [tempProblems, setTempProblems] = useState<string[]>([]);
  const [tempStatuses, setTempStatuses] = useState<string[]>([]);
  const [tempLanguages, setTempLanguages] = useState<string[]>([]);

  const handleOpenFilterDialog = () => {
    setTempProblems(selectedProblems);
    setTempStatuses(selectedStatuses);
    setTempLanguages(selectedLanguages);
    setFilterDialogOpen(true);
  };

  const handleApplyFilters = () => {
    setSelectedProblems(tempProblems);
    setSelectedStatuses(tempStatuses);
    setSelectedLanguages(tempLanguages);
    setFilterDialogOpen(false);
  };

  const handleClearFilters = () => {
    setTempProblems([]);
    setTempStatuses([]);
    setTempLanguages([]);
  };

  const handleClearAll = () => {
    setSearch('');
    setSelectedProblems([]);
    setSelectedStatuses([]);
    setSelectedLanguages([]);
  };

  const toggleItem = (arr: string[], setArr: React.Dispatch<React.SetStateAction<string[]>>, item: string) => {
    setArr(prev => prev.includes(item) ? prev.filter(i => i !== item) : [...prev, item]);
  };

  const activeFiltersCount = selectedProblems.length + selectedStatuses.length + selectedLanguages.length;

  const filteredSubmissions = mockSubmissions.filter((s: Submission) => {
    const matchesSearch = search === '' || 
      s.odName.toLowerCase().includes(search.toLowerCase()) ||
      s.problemTitle.toLowerCase().includes(search.toLowerCase());
    const matchesProblem = selectedProblems.length === 0 || selectedProblems.includes(s.problemId);
    const matchesStatus = selectedStatuses.length === 0 || selectedStatuses.includes(s.status);
    const matchesLanguage = selectedLanguages.length === 0 || selectedLanguages.includes(s.language);
    return matchesSearch && matchesProblem && matchesStatus && matchesLanguage;
  });

  // Get unique problems from submissions
  const problemsInRoom = Array.from(new Set(mockSubmissions.map(s => ({ id: s.problemId, title: s.problemTitle }))))
    .filter((v, i, a) => a.findIndex(t => t.id === v.id) === i);

  return (
    <RoomLayout isHost roomName={room.name}>
      <h2 className="text-xl font-bold mb-4">Submissões Gerais</h2>
      
      {/* Search and Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar por usuário ou problema..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 bg-card/50 border-border/50 focus:border-primary"
          />
        </div>
        <Button 
          variant="outline" 
          onClick={handleOpenFilterDialog}
          className="gap-2"
        >
          <Filter className="h-4 w-4" />
          Filtrar
          {activeFiltersCount > 0 && (
            <span className="ml-1 px-1.5 py-0.5 text-xs rounded-full bg-primary text-primary-foreground">
              {activeFiltersCount}
            </span>
          )}
        </Button>
        {(search || activeFiltersCount > 0) && (
          <Button variant="ghost" size="icon" onClick={handleClearAll}>
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      <div className="space-y-3">
        {filteredSubmissions.length === 0 ? (
          <p className="text-center text-muted-foreground py-8">
            Nenhuma submissão encontrada
          </p>
        ) : (
          filteredSubmissions.map(s => (
            <Card key={s.id} className="border-border/50 bg-card/50">
              <CardContent className="py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={s.odAvatar} />
                    <AvatarFallback>{s.odName.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium">{s.problemTitle}</p>
                    <p className="text-sm text-muted-foreground">{s.odName} • {languageLabels[s.language] || s.language}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <StatusBadge status={s.status} />
                  <span className="text-sm text-muted-foreground">{s.time}ms</span>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      <div className="mt-6">
        <Pagination currentPage={page} totalPages={3} onPageChange={setPage} />
      </div>

      {/* Filter Dialog */}
      <Dialog open={filterDialogOpen} onOpenChange={setFilterDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Filtrar Submissões</DialogTitle>
          </DialogHeader>
          
          <div className="space-y-6 py-4">
            {/* Problems Filter */}
            <div className="space-y-3">
              <h4 className="font-medium text-sm text-[hsl(var(--neon-cyan))]">Problema</h4>
              <div className="grid gap-2">
                {problemsInRoom.map(problem => (
                  <div 
                    key={problem.id} 
                    className="flex items-center space-x-3 p-2 rounded-lg hover:bg-card/50 cursor-pointer"
                    onClick={() => toggleItem(tempProblems, setTempProblems, problem.id)}
                  >
                    <Checkbox 
                      id={`prob-${problem.id}`}
                      checked={tempProblems.includes(problem.id)}
                      onCheckedChange={() => toggleItem(tempProblems, setTempProblems, problem.id)}
                    />
                    <Label htmlFor={`prob-${problem.id}`} className="cursor-pointer flex-1">
                      {problem.title}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {/* Status Filter */}
            <div className="space-y-3">
              <h4 className="font-medium text-sm text-[hsl(var(--neon-purple))]">Status</h4>
              <div className="grid grid-cols-2 gap-2">
                {statusOptions.map(status => (
                  <div 
                    key={status.value} 
                    className="flex items-center space-x-3 p-2 rounded-lg hover:bg-card/50 cursor-pointer"
                    onClick={() => toggleItem(tempStatuses, setTempStatuses, status.value)}
                  >
                    <Checkbox 
                      id={`status-${status.value}`}
                      checked={tempStatuses.includes(status.value)}
                      onCheckedChange={() => toggleItem(tempStatuses, setTempStatuses, status.value)}
                    />
                    <Label htmlFor={`status-${status.value}`} className={`cursor-pointer flex-1 ${status.color}`}>
                      {status.label}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {/* Language Filter */}
            <div className="space-y-3">
              <h4 className="font-medium text-sm text-[hsl(var(--neon-pink))]">Linguagem</h4>
              <div className="grid grid-cols-2 gap-2">
                {languages.map(lang => (
                  <div 
                    key={lang} 
                    className="flex items-center space-x-3 p-2 rounded-lg hover:bg-card/50 cursor-pointer"
                    onClick={() => toggleItem(tempLanguages, setTempLanguages, lang)}
                  >
                    <Checkbox 
                      id={`lang-${lang}`}
                      checked={tempLanguages.includes(lang)}
                      onCheckedChange={() => toggleItem(tempLanguages, setTempLanguages, lang)}
                    />
                    <Label htmlFor={`lang-${lang}`} className="cursor-pointer flex-1">
                      {languageLabels[lang] || lang}
                    </Label>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={handleClearFilters}>
              Limpar
            </Button>
            <Button onClick={handleApplyFilters} className="arcade-button">
              Aplicar Filtros
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </RoomLayout>
  );
}
