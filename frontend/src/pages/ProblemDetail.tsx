import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ThumbsUp, ThumbsDown, Clock, HardDrive, Play, MessageSquare, Send } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { TagBadge } from '@/components/ui/TagBadge';
import { mockProblems, problemTags, mockComments } from '@/data/mockData';

export default function ProblemDetail() {
  const { id } = useParams();
  const problem = mockProblems.find(p => p.id === id) || mockProblems[0];
  const comments = mockComments.filter(c => c.problemId === problem.id);
  const getTagColor = (t: string) => (problemTags.find(pt => pt.name === t)?.color as any) || 'purple';
  
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR', { 
      day: '2-digit', 
      month: 'short', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  return (
    <PageContainer>
      <Link to="/home">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-border/50 bg-card/50 pixel-card">
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
          
          {/* Comments Section */}
          <Card className="border-border/50 bg-card/50 pixel-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 font-arcade text-sm">
                <MessageSquare className="h-5 w-5 text-primary" />
                Comentários ({comments.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Comment Input */}
              <div className="flex gap-3">
                <Textarea 
                  placeholder="Escreva um comentário..." 
                  className="bg-background/50 flex-1 min-h-[80px] resize-none" 
                />
                <Button className="self-end gap-2 pixel-btn">
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              
              {/* Comments List */}
              {comments.length > 0 ? (
                <div className="space-y-4 pt-4 border-t border-border/30">
                  {comments.map((comment) => (
                    <div 
                      key={comment.id} 
                      className="p-4 rounded-lg bg-background/50 arcade-list-item"
                    >
                      <div className="flex items-start gap-3">
                        <Avatar className="h-10 w-10 ring-2 ring-primary/30">
                          <AvatarImage src={comment.userAvatar} />
                          <AvatarFallback>{comment.userName.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <Link 
                              to={`/user/${comment.userId}`}
                              className="font-semibold text-sm hover:text-primary transition-colors"
                            >
                              {comment.userName}
                            </Link>
                            <span className="text-xs text-muted-foreground">
                              {formatDate(comment.createdAt)}
                            </span>
                          </div>
                          <p className="text-foreground/90 text-sm">{comment.content}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 border-t border-border/30">
                  <MessageSquare className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
                  <p className="font-pixel text-[8px] text-muted-foreground mb-1">SEM COMENTÁRIOS</p>
                  <p className="text-sm text-muted-foreground">Seja o primeiro a comentar!</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
        
        <div className="space-y-4">
          <Card className="border-border/50 bg-card/50 pixel-card">
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
          <div className="flex flex-col justify-center gap-5">
            <div className="flex gap-2">
              <Button variant="outline" className="flex-1 gap-2">
                <ThumbsUp className="h-4 w-4" />{problem.likes}
              </Button>
              <Button variant="outline" className="flex-1 gap-2">
                <ThumbsDown className="h-4 w-4" />{problem.dislikes}
              </Button>
            </div>

            <Link to={`/solve/${problem.id}`}>
              <Button className="w-full gap-2 pixel-btn">
                <Play className="h-4 w-4" />Resolver
              </Button>
            </Link>

            <Link to={`/problem/${id}/solves`}>
              <Button variant="outline" className="w-full">
                Ver Soluções
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}