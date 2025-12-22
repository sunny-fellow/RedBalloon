import { useState } from 'react';
import { Crown, UserMinus } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { mockRooms, mockUsers, currentUser } from '@/data/mockData';
import { useToast } from '@/hooks/use-toast';

export default function RoomLobby() {
  const room = mockRooms[0];
  const { toast } = useToast();
  const [transferDialogOpen, setTransferDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<typeof mockUsers[0] | null>(null);

  const handleTransferHost = (user: typeof mockUsers[0]) => {
    setSelectedUser(user);
    setTransferDialogOpen(true);
  };

  const confirmTransfer = () => {
    if (selectedUser) {
      toast({
        title: 'Controle transferido!',
        description: `${selectedUser.name} agora é o host da sala.`,
      });
      setTransferDialogOpen(false);
      setSelectedUser(null);
    }
  };

  const handleKickUser = (user: typeof mockUsers[0]) => {
    toast({
      title: 'Usuário removido',
      description: `${user.name} foi removido da sala.`,
      variant: 'destructive',
    });
  };

  return (
    <RoomLayout isHost roomName={room.name}>
      <Card className="border-border/50 bg-card/50 mb-6">
        <CardHeader><CardTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>{room.name}</CardTitle></CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{room.description}</p>
          <p className="text-sm mt-2">
            Criador: <span className="text-primary">{room.creatorName}</span>
          </p>
        </CardContent>
      </Card>
      
      <Card className="border-border/50 bg-card/50">
        <CardHeader>
          <CardTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>
            Jogadores ({room.currentPlayers}/{room.capacity})
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {mockUsers.slice(0, 4).map((u, i) => (
            <div key={u.id} className="flex items-center justify-between p-3 rounded-lg bg-background/50">
              <div className="flex items-center gap-3">
                <Avatar className="h-10 w-10">
                  <AvatarImage src={u.avatar} />
                  <AvatarFallback>{u.name.charAt(0)}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium flex items-center gap-2">
                    {u.name}
                    {i === 0 && <Crown className="h-4 w-4 text-neon-yellow" />}
                  </p>
                  <p className="text-sm text-muted-foreground">{u.problemsSolved} resolvidos</p>
                </div>
              </div>
              
              {/* Host controls for other players */}
              {i !== 0 && (
                <div className="flex items-center gap-1">
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    onClick={() => handleTransferHost(u)}
                    className="text-neon-yellow hover:text-neon-yellow hover:bg-neon-yellow/10"
                    title="Transferir controle"
                  >
                    <Crown className="h-4 w-4" />
                  </Button>
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    onClick={() => handleKickUser(u)}
                    className="text-destructive hover:text-destructive hover:bg-destructive/10"
                    title="Remover usuário"
                  >
                    <UserMinus className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Transfer Host Dialog */}
      <Dialog open={transferDialogOpen} onOpenChange={setTransferDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>
              Transferir Controle
            </DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <p className="text-muted-foreground">
              Você tem certeza que deseja transferir o controle da sala para{' '}
              <span className="text-primary font-medium">{selectedUser?.name}</span>?
            </p>
            <p className="text-sm text-muted-foreground mt-2">
              Você perderá os privilégios de host.
            </p>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setTransferDialogOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={confirmTransfer} className="arcade-button gap-2">
              <Crown className="h-4 w-4" />
              Confirmar Transferência
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </RoomLayout>
  );
}