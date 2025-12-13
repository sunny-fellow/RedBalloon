import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Send } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { TagBadge } from '@/components/ui/TagBadge';
import { communityTags } from '@/data/mockData';

export default function CommunityWrite() {
  const [content, setContent] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const toggleTag = (tag: string) => setSelectedTags(prev => prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]);
  return (
    <PageContainer>
      <Link to="/community"><Button variant="ghost" className="mb-4 gap-2"><ArrowLeft className="h-4 w-4" />Voltar</Button></Link>
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">Nova Publicação</h1>
        <div className="space-y-4">
          <div><label className="text-sm text-muted-foreground mb-2 block">Tags</label><div className="flex flex-wrap gap-2">{communityTags.map(t => <TagBadge key={t.id} tag={t.name} color={t.color as any} onClick={() => toggleTag(t.name)} selected={selectedTags.includes(t.name)} />)}</div></div>
          <Textarea placeholder="Escreva sua mensagem... Use @nome para mencionar usuários e #id para referenciar problemas." value={content} onChange={e => setContent(e.target.value)} className="min-h-[200px] bg-card/50" />
          <Button className="w-full gap-2"><Send className="h-4 w-4" />Publicar</Button>
        </div>
      </div>
    </PageContainer>
  );
}
