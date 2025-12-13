import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Play, Loader2, ThumbsUp, ThumbsDown, Clock, HardDrive } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CodeEditor } from '@/components/common/CodeEditor';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { Navbar } from '@/components/layout/Navbar';
import { mockProblems } from '@/data/mockData';
import { toast } from '@/hooks/use-toast';

export default function Solve() {
  const { id } = useParams();
  const problem = mockProblems.find(p => p.id === id) || mockProblems[0];
  const [code, setCode] = useState('# Escreva sua solução aqui\n\ndef solve():\n    pass\n');
  const [language, setLanguage] = useState('python');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = () => {
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      const results = ['accepted', 'wrong_answer', 'time_limit'];
      const result = results[Math.floor(Math.random() * results.length)];
      toast({ title: result === 'accepted' ? '✅ Aceito!' : result === 'wrong_answer' ? '❌ Resposta Errada' : '⏱️ Tempo Excedido', variant: result === 'accepted' ? 'default' : 'destructive' });
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex h-[calc(100vh-64px)]">
        <div className="w-1/2 p-4 overflow-auto border-r border-border/50">
          <Link to={`/problem/${problem.id}`}><Button variant="ghost" size="sm" className="mb-4 gap-2"><ArrowLeft className="h-4 w-4" />Voltar</Button></Link>
          <Card className="border-border/50 bg-card/50">
            <CardHeader><div className="flex items-center justify-between"><div><span className="text-sm text-muted-foreground font-mono">#{problem.id}</span><CardTitle className="mt-1">{problem.title}</CardTitle><p className="text-sm text-muted-foreground">por {problem.creatorName}</p></div><DifficultyBadge difficulty={problem.difficulty} /></div></CardHeader>
            <CardContent className="space-y-4">
              <p>{problem.description}</p>
              <div className="grid grid-cols-2 gap-4 text-sm"><div className="flex items-center gap-2 text-muted-foreground"><Clock className="h-4 w-4" />{problem.timeLimit}ms</div><div className="flex items-center gap-2 text-muted-foreground"><HardDrive className="h-4 w-4" />{problem.memoryLimit}MB</div></div>
              <div className="flex gap-4 text-sm"><span className="flex items-center gap-1"><ThumbsUp className="h-4 w-4" />{problem.likes}</span><span className="flex items-center gap-1"><ThumbsDown className="h-4 w-4" />{problem.dislikes}</span></div>
            </CardContent>
          </Card>
        </div>
        <div className="w-1/2 p-4 flex flex-col">
          <div className="flex-1 mb-4"><CodeEditor value={code} onChange={setCode} language={language} onLanguageChange={setLanguage} /></div>
          <Button className="w-full gap-2" onClick={handleSubmit} disabled={submitting}>{submitting ? <><Loader2 className="h-4 w-4 animate-spin" />Submetendo...</> : <><Play className="h-4 w-4" />Submeter</>}</Button>
        </div>
      </div>
    </div>
  );
}
