import { Link } from 'react-router-dom';
import { Users, Lock, Unlock, Clock, Play, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Room } from '@/types';
import { cn } from '@/lib/utils';

interface RoomCardProps {
  room: Room;
  onJoin: (room: Room) => void;
}

const statusConfig = {
  waiting: { label: 'Aguardando', icon: Clock, className: 'bg-neon-cyan/20 text-neon-cyan' },
  in_progress: { label: 'Em andamento', icon: Play, className: 'bg-neon-green/20 text-neon-green' },
  finished: { label: 'Finalizado', icon: CheckCircle, className: 'bg-muted text-muted-foreground' },
};

export function RoomCard({ room, onJoin }: RoomCardProps) {
  const status = statusConfig[room.status];
  const StatusIcon = status.icon;
  const isFull = room.currentPlayers >= room.capacity;

  return (
    <Card className="group relative overflow-hidden border-border/50 bg-card/50 backdrop-blur transition-all hover:border-accent/50 hover:shadow-lg hover:shadow-accent/10">
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
      
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <div className="space-y-1 flex-1 min-w-0">
            <div className="flex items-center gap-2">
              {room.isPrivate ? (
                <Lock className="h-4 w-4 text-neon-orange" />
              ) : (
                <Unlock className="h-4 w-4 text-neon-green" />
              )}
              <Badge className={cn('text-xs', status.className)}>
                <StatusIcon className="h-3 w-3 mr-1" />
                {status.label}
              </Badge>
            </div>
            <h3 className="font-semibold text-foreground group-hover:text-accent transition-colors truncate">
              {room.name}
            </h3>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pb-2">
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {room.description}
        </p>
        
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">
            Criador: <span className="text-foreground">{room.creatorName}</span>
          </span>
          <div className={cn(
            'flex items-center gap-1 font-medium',
            isFull ? 'text-destructive' : 'text-neon-green'
          )}>
            <Users className="h-4 w-4" />
            {room.currentPlayers}/{room.capacity}
          </div>
        </div>

        {room.duration && (
          <div className="flex items-center gap-1 mt-2 text-xs text-muted-foreground">
            <Clock className="h-3 w-3" />
            Duração: {room.duration} min
          </div>
        )}
      </CardContent>

      <CardFooter className="pt-2 border-t border-border/50">
        <div className="flex gap-2 w-full">
          <Button
            className="flex-1"
            variant={isFull ? 'outline' : 'default'}
            disabled={isFull || room.status === 'finished'}
            onClick={(e) => {
              e.preventDefault();
              onJoin(room);
            }}
          >
            {isFull ? 'Sala Cheia' : 'Entrar'}
          </Button>
          <Link to={`/room/lobby`} className="flex-1">
            <Button variant="outline" className="w-full">
              Ver Detalhes
            </Button>
          </Link>
        </div>
      </CardFooter>
    </Card>
  );
}
