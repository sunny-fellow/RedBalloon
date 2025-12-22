import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, Target, Edit2, Lightbulb, Gamepad2 } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { currentUser, mockProblems } from '@/data/mockData';

export default function Profile() {
  const [activeTab, setActiveTab] = useState('solved');

  // Problems solved by the current user (mock: first 3 for demo)
  const solvedProblems = mockProblems.slice(0, 3);
  
  // Problems created by the current user
  const createdProblems = mockProblems.filter(p => p.creatorId === currentUser.id);

  return (
    <PageContainer>
      <Link to="/home">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      
      <div className="grid lg:grid-cols-3 gap-6 items-start">
        {/* Profile Card - Fixed height */}
        <Card className="lg:col-span-1 border-border/50 bg-card/50 pixel-card h-fit">
          <CardContent className="pt-6 text-center space-y-4">
            <Avatar className="h-24 w-24 mx-auto ring-4 ring-primary/30">
              <AvatarImage src={currentUser.avatar} />
              <AvatarFallback>{currentUser.name.charAt(0)}</AvatarFallback>
            </Avatar>
            
            <div className="space-y-1">
              <h2 className="text-xl font-arcade font-bold text-glow-purple text-flicker">{currentUser.name}</h2>
              <p className="text-muted-foreground font-mono text-sm">@{currentUser.login}</p>
            </div>
            
            <div className="space-y-3 pt-2">
              <Input defaultValue={currentUser.name} className="bg-background/50" />
              <Input defaultValue={currentUser.email} className="bg-background/50" />
            </div>
            
            <Button className="w-full gap-2 pixel-btn">
              <Edit2 className="h-4 w-4" />Salvar Alterações
            </Button>
          </CardContent>
        </Card>

        {/* Stats & Problems */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 gap-4">
            <Card className="border-border/50 bg-card/50 pixel-card arcade-hover-card relative">
              <CardContent className="pt-6 text-center">
                <Target className="h-8 w-8 mx-auto text-neon-orange" />
                <p className="text-3xl font-arcade font-bold mt-2 text-glow-pink">{currentUser.problemsAttempted}</p>
                <p className="text-muted-foreground font-pixel text-[8px] mt-1">TENTADOS</p>
              </CardContent>
            </Card>
            <Card className="border-border/50 bg-card/50 pixel-card arcade-hover-card relative">
              <CardContent className="pt-6 text-center">
                <CheckCircle className="h-8 w-8 mx-auto text-neon-green" />
                <p className="text-3xl font-arcade font-bold mt-2 text-glow-cyan">{currentUser.problemsSolved}</p>
                <p className="text-muted-foreground font-pixel text-[8px] mt-1">RESOLVIDOS</p>
              </CardContent>
            </Card>
          </div>

          {/* Problems Tabs */}
          <Card className="border-border/50 bg-card/50 pixel-card pixel-scanlines">
            <CardHeader className="pb-0">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-2 bg-background/50 p-1">
                  <TabsTrigger 
                    value="solved" 
                    className="gap-2 font-arcade text-xs arcade-tab data-[state=active]:text-primary-foreground"
                  >
                    <CheckCircle className="h-4 w-4" />
                    Resolvidos
                  </TabsTrigger>
                  <TabsTrigger 
                    value="created" 
                    className="gap-2 font-arcade text-xs arcade-tab data-[state=active]:text-primary-foreground"
                  >
                    <Lightbulb className="h-4 w-4" />
                    Criados
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </CardHeader>
            <CardContent className="pt-4">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsContent value="solved" className="mt-0 tab-content-enter">
                  {solvedProblems.length > 0 ? (
                    <div className="space-y-2">
                      {solvedProblems.map(p => (
                        <Link 
                          to={`/problem/${p.id}`} 
                          key={p.id} 
                          className="flex justify-between items-center p-3 rounded-lg bg-background/50 arcade-list-item"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-muted-foreground font-mono">#{p.id}</span>
                            <span>{p.title}</span>
                            <DifficultyBadge difficulty={p.difficulty} />
                          </div>
                          <span className="text-neon-green font-pixel text-[8px]">ACEITO</span>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <Gamepad2 className="h-16 w-16 mx-auto text-muted-foreground/50 mb-4" />
                      <p className="font-pixel text-[10px] text-muted-foreground mb-2">NENHUM PROBLEMA RESOLVIDO</p>
                      <p className="text-sm text-muted-foreground">Comece a resolver problemas para aparecer aqui!</p>
                      <Link to="/home">
                        <Button variant="outline" className="mt-4">
                          Ver Problemas
                        </Button>
                      </Link>
                    </div>
                  )}
                </TabsContent>
                
                <TabsContent value="created" className="mt-0 tab-content-enter">
                  {createdProblems.length > 0 ? (
                    <div className="space-y-2">
                      {createdProblems.map(p => (
                        <Link 
                          to={`/problem/${p.id}`} 
                          key={p.id} 
                          className="flex justify-between items-center p-3 rounded-lg bg-background/50 arcade-list-item"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-muted-foreground font-mono">#{p.id}</span>
                            <span>{p.title}</span>
                            <DifficultyBadge difficulty={p.difficulty} />
                          </div>
                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <span>{p.solved} soluções</span>
                          </div>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <Lightbulb className="h-16 w-16 mx-auto text-muted-foreground/50 mb-4" />
                      <p className="font-pixel text-[10px] text-muted-foreground mb-2">NENHUM PROBLEMA CRIADO</p>
                      <p className="text-sm text-muted-foreground">Crie seu primeiro problema para a comunidade!</p>
                      <Link to="/problem/create">
                        <Button variant="outline" className="mt-4">
                          Criar Problema
                        </Button>
                      </Link>
                    </div>
                  )}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
}