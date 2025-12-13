import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileCode, 
  Settings, 
  User, 
  MessageSquare, 
  List,
  LogOut
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface RoomMenuProps {
  isHost?: boolean;
  roomName?: string;
}

const menuItems = [
  { path: '/room/lobby', label: 'Lobby', icon: LayoutDashboard },
  { path: '/room/problems', label: 'Problemas', icon: FileCode },
  { path: '/room/me', label: 'Minhas Submissões', icon: User },
  { path: '/room/submissions', label: 'Submissões Gerais', icon: List },
  { path: '/room/chat', label: 'Chat', icon: MessageSquare },
];

export function RoomMenu({ isHost = false, roomName = 'Sala' }: RoomMenuProps) {
  const location = useLocation();

  return (
    <div className="w-full lg:w-64 flex-shrink-0">
      <div className="sticky top-20 space-y-4">
        <div className="p-4 rounded-lg border border-border/50 bg-card/50">
          <h2 className="font-semibold text-lg truncate">{roomName}</h2>
          <p className="text-sm text-muted-foreground">Menu da Sala</p>
        </div>

        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <Link key={item.path} to={item.path}>
                <Button
                  variant="ghost"
                  className={cn(
                    'w-full justify-start gap-3',
                    isActive && 'bg-primary/10 text-primary neon-text'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Button>
              </Link>
            );
          })}

          {isHost && (
            <Link to="/room/config">
              <Button
                variant="ghost"
                className={cn(
                  'w-full justify-start gap-3',
                  location.pathname === '/room/config' && 'bg-primary/10 text-primary neon-text'
                )}
              >
                <Settings className="h-4 w-4" />
                Configurações
              </Button>
            </Link>
          )}

          <Link to="/rooms">
            <Button
              variant="ghost"
              className="w-full justify-start gap-3 text-destructive hover:text-destructive hover:bg-destructive/10"
            >
              <LogOut className="h-4 w-4" />
              Sair da Sala
            </Button>
          </Link>
        </nav>
      </div>
    </div>
  );
}
