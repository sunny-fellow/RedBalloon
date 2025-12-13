import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Play, Loader2 } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CodeEditor } from '@/components/common/CodeEditor';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { mockProblems, mockRooms } from '@/data/mockData';
import { toast } from '@/hooks/use-toast';

export default function RoomSolve() {
  const { id } = useParams();
  const problem = mockProblems.find(p => p.id === id) || mockProblems[0];
  const room = mockRooms[0];
  const [code, setCode] = useState('# Solução\n');
  const [language, setLanguage] = useState('python');
  const [submitting, setSubmitting] = useState(false);
  const handleSubmit = () => { setSubmitting(true); setTimeout(() => { setSubmitting(false); toast({ title: '✅ Aceito!' }); }, 2000); };
  return (
    <RoomLayout isHost roomName={room.name}>
      <div className="grid lg:grid-cols-2 gap-4 h-[calc(100vh-200px)]">
        <Card className="border-border/50 bg-card/50 overflow-auto">
          <CardHeader><div className="flex items-center justify-between"><CardTitle>{problem.title}</CardTitle><DifficultyBadge difficulty={problem.difficulty} /></div></CardHeader>
          <CardContent><p>{problem.description}</p><p className="text-sm text-muted-foreground mt-4">Tempo: {problem.timeLimit}ms | Memória: {problem.memoryLimit}MB</p></CardContent>
        </Card>
        <div className="flex flex-col"><div className="flex-1"><CodeEditor value={code} onChange={setCode} language={language} onLanguageChange={setLanguage} /></div><Button className="mt-4 gap-2" onClick={handleSubmit} disabled={submitting}>{submitting ? <><Loader2 className="h-4 w-4 animate-spin" />Submetendo...</> : <><Play className="h-4 w-4" />Submeter</>}</Button></div>
      </div>
    </RoomLayout>
  );
}
