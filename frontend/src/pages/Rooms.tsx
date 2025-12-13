import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Plus } from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { RoomCard } from '@/components/cards/RoomCard';
import { SearchFilters } from '@/components/common/SearchFilters';
import { Pagination } from '@/components/common/Pagination';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { mockRooms } from '@/data/mockData';
import { Room } from '@/types';
import { useToast } from '@/hooks/use-toast';

export default function Rooms() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [page, setPage] = useState(1);
  const [passwordDialog, setPasswordDialog] = useState<Room | null>(null);
  const [password, setPassword] = useState('');

  const handleJoin = (room: Room) => {
    if (room.isPrivate) {
      setPasswordDialog(room);
    } else {
      toast({ title: 'Entrando na sala...', description: room.name });
      navigate('/room/lobby');
    }
  };

  const handlePasswordSubmit = () => {
    if (!password) {
      toast({ title: 'Erro', description: 'Digite a senha', variant: 'destructive' });
      return;
    }
    toast({ title: 'Entrando na sala...', description: passwordDialog?.name });
    setPasswordDialog(null);
    setPassword('');
    navigate('/room/lobby');
  };

  return (
    <PageContainer>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold gradient-text" style={{ fontFamily: 'Orbitron, sans-serif' }}>
          Salas
        </h1>
        <Link to="/room/create">
          <Button className="gap-2 arcade-button">
            <Plus className="h-4 w-4" />
            Criar Sala
          </Button>
        </Link>
      </div>
      
      <SearchFilters 
        searchPlaceholder="Buscar sala..." 
        searchValue={search} 
        onSearchChange={setSearch} 
        filters={[
          { 
            key: 'status', 
            label: 'Status', 
            options: [
              { value: 'waiting', label: 'Aguardando' }, 
              { value: 'in_progress', label: 'Em andamento' }
            ], 
            value: status, 
            onChange: setStatus 
          }
        ]} 
        onClearFilters={() => { setSearch(''); setStatus(''); }} 
      />
      
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
        {mockRooms.map(r => (
          <RoomCard key={r.id} room={r} onJoin={handleJoin} />
        ))}
      </div>
      
      <div className="mt-8">
        <Pagination currentPage={page} totalPages={2} onPageChange={setPage} />
      </div>
      
      {/* Password Dialog */}
      <Dialog open={!!passwordDialog} onOpenChange={() => { setPasswordDialog(null); setPassword(''); }}>
        <DialogContent className="arcade-card">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Orbitron, sans-serif' }}>
              Sala Privada
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <p className="text-muted-foreground">
              Esta sala é privada. Digite a senha para entrar.
            </p>
            <div className="space-y-2">
              <Label>Senha</Label>
              <Input 
                type="password" 
                placeholder="Digite a senha" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handlePasswordSubmit()}
                className="bg-input" 
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => { setPasswordDialog(null); setPassword(''); }}>
              Cancelar
            </Button>
            <Button onClick={handlePasswordSubmit} className="arcade-button">
              Entrar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </PageContainer>
  );
}
