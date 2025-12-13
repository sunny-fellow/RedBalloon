import { useState } from 'react';
import { Link } from 'react-router-dom';
import { PenSquare, Search, Filter, X } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { PostThread } from '@/components/common/PostThread';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { TagBadge } from '@/components/ui/TagBadge';
import { mockPosts, communityTags } from '@/data/mockData';

export default function Community() {
  const [search, setSearch] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [tempSelectedTags, setTempSelectedTags] = useState<string[]>([]);
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

  const filteredPosts = mockPosts.filter(post => {
    const matchesSearch = search === '' || 
      post.userName.toLowerCase().includes(search.toLowerCase()) ||
      post.content.toLowerCase().includes(search.toLowerCase());
    const matchesTags = selectedTags.length === 0 || 
      selectedTags.some(t => post.tags.includes(t));
    return matchesSearch && matchesTags;
  });

  return (
    <PageContainer>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold gradient-text">Comunidade</h1>
        <Link to="/community/write">
          <Button className="gap-2">
            <PenSquare className="h-4 w-4" />Escrever
          </Button>
        </Link>
      </div>

      {/* Search and Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar por autor ou conteúdo..."
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
            const tagInfo = communityTags.find(t => t.name === tag);
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

      <div className="space-y-4">
        {filteredPosts.length === 0 ? (
          <p className="text-center text-muted-foreground py-8">
            Nenhuma postagem encontrada
          </p>
        ) : (
          filteredPosts.map(post => <PostThread key={post.id} post={post} />)
        )}
      </div>

      {/* Filter Dialog */}
      <Dialog open={filterDialogOpen} onOpenChange={setFilterDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Filtrar por Tags</DialogTitle>
          </DialogHeader>
          
          <div className="grid grid-cols-2 gap-3 py-4">
            {communityTags.map(tag => (
              <div 
                key={tag.id} 
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-card/50 cursor-pointer"
                onClick={() => handleToggleTempTag(tag.name)}
              >
                <Checkbox 
                  id={`comm-${tag.id}`}
                  checked={tempSelectedTags.includes(tag.name)}
                  onCheckedChange={() => handleToggleTempTag(tag.name)}
                />
                <Label 
                  htmlFor={`comm-${tag.id}`} 
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
