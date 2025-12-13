import { useState } from 'react';
import { Github, ExternalLink, Filter, X } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { ProblemCard } from '@/components/cards/ProblemCard';
import { Pagination } from '@/components/common/Pagination';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { TagBadge } from '@/components/ui/TagBadge';
import { mockProblems, problemTags } from '@/data/mockData';
import { Search } from 'lucide-react';

export default function Home() {
  const [search, setSearch] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [tempSelectedTags, setTempSelectedTags] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [filterDialogOpen, setFilterDialogOpen] = useState(false);

  const handleOpenFilterDialog = () => {
    setTempSelectedTags(selectedTags);
    setFilterDialogOpen(true);
  };

  const handleApplyFilters = () => {
    setSelectedTags(tempSelectedTags);
    setFilterDialogOpen(false);
  };

  const handleToggleTempTag = (tag: string) => {
    setTempSelectedTags(prev => 
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const handleRemoveTag = (tag: string) => {
    setSelectedTags(prev => prev.filter(t => t !== tag));
  };

  const handleClearAll = () => {
    setSearch('');
    setSelectedTags([]);
  };

  const filteredProblems = mockProblems.filter(p => {
    const matchesSearch = p.title.toLowerCase().includes(search.toLowerCase()) ||
      p.id.includes(search) ||
      p.creatorName.toLowerCase().includes(search.toLowerCase());
    const matchesTags = selectedTags.length === 0 || selectedTags.some(t => p.tags.includes(t));
    return matchesSearch && matchesTags;
  });

  return (
    <PageContainer>
      <section className="relative py-12 mb-8 rounded-2xl overflow-hidden border border-border/50 bg-card/30">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,hsl(270_95%_65%/0.15),transparent_50%)]" />
        <div className="relative container text-center space-y-4">
          <div className="mx-auto w-20 h-20 rounded-full bg-destructive/20 flex items-center justify-center animate-pulse-slow"><span className="text-5xl">🎈</span></div>
          <h1 className="text-4xl md:text-5xl font-bold gradient-text">RedBalloon</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">Plataforma de programação competitiva. Resolva problemas, participe de competições e evolua suas habilidades.</p>
          <div className="flex justify-center gap-4">
            <Button variant="outline" className="gap-2"><Github className="h-4 w-4" />GitHub</Button>
            <Button variant="outline" className="gap-2"><ExternalLink className="h-4 w-4" />Sobre Nós</Button>
          </div>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-6">Problemas</h2>
        
        {/* Search and Filter Bar */}
        <div className="flex flex-col sm:flex-row gap-3 mb-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar por nome, id ou criador..."
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
            Filtrar Tags
          </Button>
          {(search || selectedTags.length > 0) && (
            <Button variant="ghost" size="icon" onClick={handleClearAll}>
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>

        {/* Selected Tags Display */}
        {selectedTags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {selectedTags.map(tag => {
              const tagInfo = problemTags.find(t => t.name === tag);
              return (
                <TagBadge
                  key={tag}
                  tag={tag}
                  color={(tagInfo?.color as any) || 'purple'}
                  selected
                  onClick={() => handleRemoveTag(tag)}
                />
              );
            })}
          </div>
        )}

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {filteredProblems.map(p => <ProblemCard key={p.id} problem={p} />)}
        </div>
        <div className="mt-8"><Pagination currentPage={page} totalPages={5} onPageChange={setPage} /></div>
      </section>

      {/* Filter Dialog */}
      <Dialog open={filterDialogOpen} onOpenChange={setFilterDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Filtrar por Tags</DialogTitle>
          </DialogHeader>
          
          <div className="grid grid-cols-2 gap-3 py-4">
            {problemTags.map(tag => (
              <div 
                key={tag.id} 
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-card/50 cursor-pointer"
                onClick={() => handleToggleTempTag(tag.name)}
              >
                <Checkbox 
                  id={tag.id}
                  checked={tempSelectedTags.includes(tag.name)}
                  onCheckedChange={() => handleToggleTempTag(tag.name)}
                />
                <Label 
                  htmlFor={tag.id} 
                  className="cursor-pointer flex-1"
                >
                  <TagBadge 
                    tag={tag.name} 
                    color={tag.color as any} 
                    size="sm"
                  />
                </Label>
              </div>
            ))}
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setTempSelectedTags([])}>
              Limpar
            </Button>
            <Button onClick={handleApplyFilters} className="arcade-button">
              Filtrar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </PageContainer>
  );
}
