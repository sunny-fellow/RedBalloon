import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ThumbsUp, ThumbsDown, Clock, HardDrive, Play, MessageSquare } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { TagBadge } from '@/components/ui/TagBadge';
import { mockProblems, problemTags } from '@/data/mockData';

export default function ProblemDetail() {
  const { id } = useParams();
  const problem = mockProblems.find(p => p.id === id) || mockProblems[0];
  const getTagColor = (t: string) => (problemTags.find(pt => pt.name === t)?.color as any) || 'purple';
  
  return (
    <PageContainer>
      <Link to="/home">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-border/50 bg-card/50">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-sm text-muted-foreground font-mono">#{problem.id}</span>
                  <h1 className="text-2xl font-bold mt-1">{problem.title}</h1>
                  <p className="text-muted-foreground">por {problem.creatorName}</p>
                </div>
                <DifficultyBadge difficulty={problem.difficulty} />
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-foreground/90 mb-4">{problem.description}</p>
              <div className="flex flex-wrap gap-2">
                {problem.tags.map(t => <TagBadge key={t} tag={t} color={getTagColor(t)} />)}
              </div>
            </CardContent>
          </Card>
          <Card className="border-border/50 bg-card/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />Comentários
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Textarea placeholder="Escreva um comentário..." className="bg-background/50 mb-3" />
              <Button>Comentar</Button>
            </CardContent>
          </Card>
        </div>
        <div className="space-y-4">
          <Card className="border-border/50 bg-card/50">
            <CardContent className="pt-6 space-y-3">
              <div className="flex justify-between">
                <span className="text-muted-foreground flex items-center gap-2">
                  <Clock className="h-4 w-4" />Tempo
                </span>
                <span>{problem.timeLimit}ms</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground flex items-center gap-2">
                  <HardDrive className="h-4 w-4" />Memória
                </span>
                <span>{problem.memoryLimit}MB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tentativas</span>
                <span>{problem.attempts}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Resolvidos</span>
                <span className="text-neon-green">{problem.solved}</span>
              </div>
            </CardContent>
          </Card>
          <div className="flex gap-2">
            <Button variant="outline" className="flex-1 gap-2">
              <ThumbsUp className="h-4 w-4" />{problem.likes}
            </Button>
            <Button variant="outline" className="flex-1 gap-2">
              <ThumbsDown className="h-4 w-4" />{problem.dislikes}
            </Button>
          </div>
          <Link to={`/solve/${problem.id}`}>
            <Button className="w-full gap-2">
              <Play className="h-4 w-4" />Resolver
            </Button>
          </Link>
          <Link to={`/problem/resolutions`}>
            <Button variant="outline" className="w-full">Ver Soluções</Button>
          </Link>
        </div>
      </div>
    </PageContainer>
  );
}
