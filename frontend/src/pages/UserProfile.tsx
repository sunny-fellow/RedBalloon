import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ThumbsUp, MapPin, Mail, CheckCircle } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockUsers, mockProblems } from '@/data/mockData';

export default function UserProfile() {
  const { id } = useParams();
  const user = mockUsers.find(u => u.id === id) || mockUsers[0];
  
  return (
    <PageContainer>
      <Link to="/users">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />Voltar
        </Button>
      </Link>
      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="border-border/50 bg-card/50">
          <CardContent className="pt-6 text-center">
            <Avatar className="h-24 w-24 mx-auto ring-4 ring-secondary/30">
              <AvatarImage src={user.avatar} />
              <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
            </Avatar>
            <h2 className="mt-4 text-xl font-bold">{user.name}</h2>
            <p className="text-muted-foreground">@{user.login}</p>
            <div className="flex justify-center gap-2 mt-2 text-sm text-muted-foreground">
              <MapPin className="h-4 w-4" />{user.country}
            </div>
            <div className="flex justify-center gap-2 mt-1 text-sm text-muted-foreground">
              <Mail className="h-4 w-4" />{user.email}
            </div>
            <div className="mt-4">
              <Button className="w-full gap-2">
                <ThumbsUp className="h-4 w-4" />Like ({user.likes})
              </Button>
            </div>
          </CardContent>
        </Card>
        <div className="lg:col-span-2 space-y-6">
          <div className="flex gap-4">
            <Card className="flex-1 border-border/50 bg-card/50">
              <CardContent className="pt-6 text-center">
                <CheckCircle className="h-8 w-8 mx-auto text-neon-green" />
                <p className="text-3xl font-bold mt-2">{user.problemsSolved}</p>
                <p className="text-muted-foreground">Resolvidos</p>
              </CardContent>
            </Card>
          </div>
          <Card className="border-border/50 bg-card/50">
            <CardHeader>
              <CardTitle>Problemas Criados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {mockProblems.filter(p => p.creatorId === user.id).map(p => (
                  <Link 
                    to={`/problem/${p.id}`} 
                    key={p.id} 
                    className="block p-3 rounded-lg bg-background/50 hover:bg-background/80"
                  >
                    #{p.id} {p.title}
                  </Link>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
}
