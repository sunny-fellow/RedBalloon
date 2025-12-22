import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, UserPlus, MapPin, Mail, CheckCircle, Lightbulb, Gamepad2, Users } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { mockUsers, mockProblems } from '@/data/mockData';

export default function UserProfile() {
  const { id } = useParams();
  const user = mockUsers.find(u => u.id === id) || mockUsers[0];
  const [activeTab, setActiveTab] = useState('solved');

  // Problems solved by this user (mock: based on problemsSolved count)
  const solvedProblems = mockProblems.slice(0, Math.min(user.problemsSolved, mockProblems.length));
  
  // Problems created by this user
  const createdProblems = mockProblems.filter(p => p.creatorId === user.id);
  
  return (
    <PageContainer>
      <Link to="/users">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      
      <div className="grid lg:grid-cols-3 gap-6 items-start">
        {/* Profile Card - Fixed height */}
        <Card className="lg:col-span-1 border-border/50 bg-card/50 pixel-card h-fit">
          <CardContent className="pt-6 text-center space-y-4">
            <Avatar className="h-24 w-24 mx-auto ring-4 ring-secondary/30">
              <AvatarImage src={user.avatar} />
              <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
            </Avatar>
            
            <div className="space-y-1">
              <h2 className="text-xl font-arcade font-bold text-glow-purple text-flicker">{user.name}</h2>
              <p className="text-muted-foreground font-mono text-sm">@{user.login}</p>
            </div>
            
            <div className="space-y-2 text-sm text-muted-foreground">
              <div className="flex justify-center items-center gap-2">
                <MapPin className="h-4 w-4" />
                <span>{user.country}</span>
              </div>
              <div className="flex justify-center items-center gap-2">
                <Mail className="h-4 w-4" />
                <span>{user.email}</span>
              </div>
              <div className="flex justify-center items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                <span className="text-foreground font-semibold">{user.followers}</span>
                <span>seguidores</span>
              </div>
            </div>
            
            <Button className="w-full gap-2 pixel-btn">
              <UserPlus className="h-4 w-4" />Seguir
            </Button>
          </CardContent>
        </Card>

        {/* Stats & Problems */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Card */}
          <Card className="border-border/50 bg-card/50 pixel-card arcade-hover-card relative">
            <CardContent className="pt-6 text-center">
              <CheckCircle className="h-8 w-8 mx-auto text-neon-green" />
              <p className="text-3xl font-arcade font-bold mt-2 text-glow-cyan">{user.problemsSolved}</p>
              <p className="text-muted-foreground font-pixel text-[8px] mt-1">RESOLVIDOS</p>
            </CardContent>
          </Card>

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
                      <p className="text-sm text-muted-foreground">Este usuário ainda não resolveu nenhum problema.</p>
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
                      <p className="text-sm text-muted-foreground">Este usuário ainda não criou nenhum problema.</p>
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