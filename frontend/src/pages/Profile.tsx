import { Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, Target, Edit2 } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { currentUser, mockProblems } from '@/data/mockData';

export default function Profile() {
  return (
    <PageContainer>
      <Link to="/home"><Button variant="ghost" className="mb-4 gap-2"><ArrowLeft className="h-4 w-4" />Voltar</Button></Link>
      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1 border-border/50 bg-card/50">
          <CardContent className="pt-6 text-center">
            <Avatar className="h-24 w-24 mx-auto ring-4 ring-primary/30"><AvatarImage src={currentUser.avatar} /><AvatarFallback>{currentUser.name.charAt(0)}</AvatarFallback></Avatar>
            <h2 className="mt-4 text-xl font-bold">{currentUser.name}</h2>
            <p className="text-muted-foreground">@{currentUser.login}</p>
            <div className="mt-4 space-y-2">
              <Input defaultValue={currentUser.name} className="bg-background/50" />
              <Input defaultValue={currentUser.email} className="bg-background/50" />
            </div>
            <Button className="mt-4 w-full gap-2"><Edit2 className="h-4 w-4" />Salvar Alterações</Button>
          </CardContent>
        </Card>
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <Card className="border-border/50 bg-card/50"><CardContent className="pt-6 text-center"><Target className="h-8 w-8 mx-auto text-neon-orange" /><p className="text-3xl font-bold mt-2">{currentUser.problemsAttempted}</p><p className="text-muted-foreground">Tentados</p></CardContent></Card>
            <Card className="border-border/50 bg-card/50"><CardContent className="pt-6 text-center"><CheckCircle className="h-8 w-8 mx-auto text-neon-green" /><p className="text-3xl font-bold mt-2">{currentUser.problemsSolved}</p><p className="text-muted-foreground">Resolvidos</p></CardContent></Card>
          </div>
          <Card className="border-border/50 bg-card/50">
            <CardHeader><CardTitle>Problemas Resolvidos</CardTitle></CardHeader>
            <CardContent><div className="space-y-2">{mockProblems.slice(0, 3).map(p => <div key={p.id} className="flex justify-between p-3 rounded-lg bg-background/50"><span>#{p.id} {p.title}</span><span className="text-neon-green">Aceito</span></div>)}</div></CardContent>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
}
