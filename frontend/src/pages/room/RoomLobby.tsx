import { Crown, UserMinus } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockRooms, mockUsers } from '@/data/mockData';

export default function RoomLobby() {
  const room = mockRooms[0];
  return (
    <RoomLayout isHost roomName={room.name}>
      <Card className="border-border/50 bg-card/50 mb-6">
        <CardHeader><CardTitle>{room.name}</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">{room.description}</p><p className="text-sm mt-2">Criador: <span className="text-primary">{room.creatorName}</span></p></CardContent>
      </Card>
      <Card className="border-border/50 bg-card/50">
        <CardHeader><CardTitle>Jogadores ({room.currentPlayers}/{room.capacity})</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          {mockUsers.slice(0, 4).map((u, i) => (
            <div key={u.id} className="flex items-center justify-between p-3 rounded-lg bg-background/50">
              <div className="flex items-center gap-3"><Avatar className="h-10 w-10"><AvatarImage src={u.avatar} /><AvatarFallback>{u.name.charAt(0)}</AvatarFallback></Avatar><div><p className="font-medium flex items-center gap-2">{u.name}{i === 0 && <Crown className="h-4 w-4 text-neon-yellow" />}</p><p className="text-sm text-muted-foreground">{u.problemsSolved} resolvidos</p></div></div>
              {i !== 0 && <Button variant="ghost" size="icon" className="text-destructive"><UserMinus className="h-4 w-4" /></Button>}
            </div>
          ))}
        </CardContent>
      </Card>
    </RoomLayout>
  );
}
