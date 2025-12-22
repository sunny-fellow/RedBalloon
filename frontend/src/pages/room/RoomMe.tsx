import { RoomLayout } from '@/components/room/RoomLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { BalloonBadge } from '@/components/ui/BalloonBadge';
import { mockSubmissions, mockRooms } from '@/data/mockData';

export default function RoomMe() {
  const room = mockRooms[0];
  
  return (
    <RoomLayout isHost roomName={room.name}>
      <div className="grid grid-cols-3 gap-4 mb-6">
        <Card className="border-border/50 bg-card/50">
          <CardContent className="pt-6 text-center">
            <p className="text-3xl font-bold text-neon-green">30</p>
            <p className="text-muted-foreground">Pontos</p>
          </CardContent>
        </Card>
        <Card className="border-border/50 bg-card/50">
          <CardContent className="pt-6 text-center">
            <p className="text-3xl font-bold">3</p>
            <p className="text-muted-foreground">Submissões</p>
          </CardContent>
        </Card>
        <Card className="border-border/50 bg-card/50">
          <CardContent className="pt-6 text-center">
            <p className="text-3xl font-bold text-neon-green">2</p>
            <p className="text-muted-foreground">Aceitos</p>
          </CardContent>
        </Card>
      </div>
      
      <Card className="border-border/50 bg-card/50">
        <CardHeader>
          <CardTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Minhas Submissões</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {mockSubmissions.map(s => (
            <div key={s.id} className="flex items-center justify-between p-3 rounded-lg bg-background/50">
              <div className="flex items-center gap-3">
                {/* Show balloon for accepted submissions */}
                {s.status === 'accepted' && s.balloonColor && (
                  <BalloonBadge color={s.balloonColor} size="md" />
                )}
                <div>
                  <p className="font-medium">{s.problemTitle}</p>
                  <p className="text-sm text-muted-foreground">{s.language} • {s.time}ms</p>
                </div>
              </div>
              <StatusBadge status={s.status} />
            </div>
          ))}
        </CardContent>
      </Card>
    </RoomLayout>
  );
}