import { useState } from 'react';
import { Save } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockRooms } from '@/data/mockData';

export default function RoomConfig() {
  const room = mockRooms[0];
  const [isPrivate, setIsPrivate] = useState(room.isPrivate);
  return (
    <RoomLayout isHost roomName={room.name}>
      <Card className="border-border/50 bg-card/50">
        <CardHeader><CardTitle>Configurações da Sala</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2"><Label>Nome</Label><Input defaultValue={room.name} className="bg-background/50" /></div>
          <div className="space-y-2"><Label>Descrição</Label><Textarea defaultValue={room.description} className="bg-background/50" /></div>
          <div className="space-y-2"><Label>Capacidade</Label><Input type="number" defaultValue={room.capacity} className="bg-background/50" /></div>
          <div className="flex items-center justify-between p-4 rounded-lg border border-border/50"><div><Label>Sala Privada</Label><p className="text-sm text-muted-foreground">Exigir senha</p></div><Switch checked={isPrivate} onCheckedChange={setIsPrivate} /></div>
          {isPrivate && <div className="space-y-2"><Label>Nova Senha</Label><Input type="password" className="bg-background/50" /></div>}
          <Button className="w-full gap-2"><Save className="h-4 w-4" />Salvar</Button>
        </CardContent>
      </Card>
    </RoomLayout>
  );
}
