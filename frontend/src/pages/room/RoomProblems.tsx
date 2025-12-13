import { Link } from 'react-router-dom';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Card, CardContent } from '@/components/ui/card';
import { mockRooms } from '@/data/mockData';

export default function RoomProblems() {
  const room = mockRooms[0];
  return (
    <RoomLayout isHost roomName={room.name}>
      <h2 className="text-xl font-bold mb-4">Problemas da Sala</h2>
      <div className="space-y-4">
        {room.problems.map(p => (
          <Link to={`/room/solve/${p.problemId}`} key={p.problemId}>
            <Card className="border-border/50 bg-card/50 hover:border-primary/50 transition-colors">
              <CardContent className="py-4 flex items-center justify-between">
                <div className="flex items-center gap-4"><div className="w-6 h-6 rounded-full" style={{ backgroundColor: p.balloonColor }} /><div><p className="font-medium">{p.title}</p><p className="text-sm text-muted-foreground">{p.points} pontos</p></div></div>
                <div className="text-sm text-muted-foreground"><span className="text-neon-green">{p.correct}</span>/{p.submissions} aceitos</div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </RoomLayout>
  );
}
