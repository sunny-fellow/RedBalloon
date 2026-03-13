import { useState } from 'react';
import { Save, Ban, Play } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockRooms } from '@/data/mockData';
import { useToast } from '@/hooks/use-toast';

export default function RoomConfig() {
  const room = mockRooms[0];
  const { toast } = useToast();
  const [isPrivate, setIsPrivate] = useState(room.isPrivate);
  const [acceptingSubmissions, setAcceptingSubmissions] = useState(room.acceptingSubmissions ?? true);
  const [endTime, setEndTime] = useState(() => {
    if (room.endTime) {
      const date = new Date(room.endTime);
      return date.toISOString().slice(0, 16);
    }
    return '';
  });

  const handleSave = () => {
    toast({ title: 'Salvo!', description: 'Configurações atualizadas.' });
  };

  const toggleSubmissions = () => {
    setAcceptingSubmissions(!acceptingSubmissions);
    toast({
      title: !acceptingSubmissions ? 'Submissões abertas' : 'Submissões fechadas',
      description: !acceptingSubmissions 
        ? 'Os participantes podem enviar soluções novamente.' 
        : 'Os participantes não podem mais enviar soluções.',
    });
  };

  return (
    <RoomLayout isHost roomName={room.name}>
      <Card className="border-border/50 bg-card/50">
        <CardHeader><CardTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>Configurações da Sala</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Nome</Label>
            <Input defaultValue={room.name} className="bg-background/50" />
          </div>
          
          <div className="space-y-2">
            <Label>Descrição</Label>
            <Textarea defaultValue={room.description} className="bg-background/50" />
          </div>
          
          <div className="space-y-2">
            <Label>Capacidade</Label>
            <Input type="number" defaultValue={room.capacity} className="bg-background/50" />
          </div>

          <div className="space-y-2">
            <Label>Data/Hora de Término</Label>
            <Input 
              type="datetime-local" 
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              className="bg-background/50" 
            />
            <p className="text-xs text-muted-foreground">
              Defina quando a competição termina
            </p>
          </div>
          
          <div className="flex items-center justify-between p-4 rounded-lg border border-border/50">
            <div>
              <Label>Sala Privada</Label>
              <p className="text-sm text-muted-foreground">Exigir senha</p>
            </div>
            <Switch checked={isPrivate} onCheckedChange={setIsPrivate} />
          </div>
          
          {isPrivate && (
            <div className="space-y-2">
              <Label>Nova Senha</Label>
              <Input type="password" className="bg-background/50" />
            </div>
          )}

          {/* Submissions Control */}
          <div className={`flex items-center justify-between p-4 rounded-lg border ${acceptingSubmissions ? 'border-[hsl(var(--neon-green)/0.5)] bg-[hsl(var(--neon-green)/0.05)]' : 'border-destructive/50 bg-destructive/5'}`}>
            <div>
              <Label className={acceptingSubmissions ? 'text-[hsl(var(--neon-green))]' : 'text-destructive'}>
                {acceptingSubmissions ? 'Aceitando Submissões' : 'Submissões Pausadas'}
              </Label>
              <p className="text-sm text-muted-foreground">
                {acceptingSubmissions 
                  ? 'Participantes podem enviar soluções' 
                  : 'Participantes não podem enviar soluções'}
              </p>
            </div>
            <Button 
              variant={acceptingSubmissions ? 'outline' : 'default'}
              size="sm"
              onClick={toggleSubmissions}
              className={acceptingSubmissions ? 'border-destructive text-destructive hover:bg-destructive/10' : 'arcade-button'}
            >
              {acceptingSubmissions ? (
                <>
                  <Ban className="h-4 w-4 mr-2" />
                  Pausar
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 mr-2" />
                  Retomar
                </>
              )}
            </Button>
          </div>
          
          <Button onClick={handleSave} className="w-full gap-2 arcade-button">
            <Save className="h-4 w-4" />Salvar
          </Button>
        </CardContent>
      </Card>
    </RoomLayout>
  );
}