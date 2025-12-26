import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, Code } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Pagination } from '@/components/common/Pagination';
import { CodeEditor } from '@/components/common/CodeEditor';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { mockSubmissions } from '@/data/mockData';


export default function ProblemResolutions() {
  const { id } = useParams();
  const [page, setPage] = useState(1);
  const accepted = mockSubmissions.filter(s => s.status === 'accepted' && s.problemId === id);
  return (
    <PageContainer>
      <Link to="/home"><Button variant="ghost" className="mb-4 gap-2"><ArrowLeft className="h-4 w-4" />Voltar</Button></Link>
      <h1 className="text-2xl font-bold mb-6">Soluções Aceitas</h1>
      <div className="grid gap-4">
        {accepted.map(s => (
          <Card key={s.id} className="border-border/50 bg-card/50 cursor-pointer hover:border-primary/50" onClick={() => window.open(`/problem/${id}/solve/${s.id}`)}>
            <CardContent className="py-4 flex items-center justify-between">
              <div className="flex items-center gap-4"><Code className="h-5 w-5 text-primary" /><div><p className="font-medium">{s.problemTitle}</p><p className="text-sm text-muted-foreground">por {s.odName} • {s.language}</p></div></div>
              <div className="flex items-center gap-4"><StatusBadge status={s.status} /><span className="text-sm text-muted-foreground">{s.time}ms</span></div>
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="mt-8"><Pagination currentPage={page} totalPages={3} onPageChange={setPage} /></div>
    </PageContainer>
  );
}
