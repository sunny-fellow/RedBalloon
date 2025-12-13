import { useState } from 'react';
import { Send } from 'lucide-react';
import { RoomLayout } from '@/components/room/RoomLayout';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { mockUsers, mockRooms, currentUser } from '@/data/mockData';

const messages = [
  { id: '1', odId: '1', odName: 'João Silva', odAvatar: mockUsers[0].avatar, content: 'Boa sorte a todos!', createdAt: '14:30' },
  { id: '2', odId: '2', odName: 'Maria Santos', odAvatar: mockUsers[1].avatar, content: '@joaodev obrigada! Vamos lá!', createdAt: '14:31' },
  { id: '3', odId: '3', odName: 'Carlos Ruiz', odAvatar: mockUsers[2].avatar, content: 'Alguém já resolveu o problema 1? @mariacode conseguiu?', createdAt: '14:35' },
  { id: '4', odId: '2', odName: 'Maria Santos', odAvatar: mockUsers[1].avatar, content: 'Sim! @joaodev me ajudou com uma dica sobre binary search', createdAt: '14:36' },
];

// Parse content and highlight mentions
const renderMessageContent = (content: string, currentUserLogin: string) => {
  const parts = content.split(/(@\w+)/g);
  
  return parts.map((part, index) => {
    if (part.startsWith('@')) {
      const username = part.slice(1).toLowerCase();
      const isCurrentUser = username === currentUserLogin.toLowerCase();
      
      return (
        <span 
          key={index} 
          className={`font-semibold ${
            isCurrentUser 
              ? 'text-[hsl(var(--neon-pink))] bg-[hsl(var(--neon-pink)/0.15)] px-1 rounded' 
              : 'text-[hsl(var(--neon-cyan))]'
          }`}
        >
          {part}
        </span>
      );
    }
    return part;
  });
};

export default function RoomChat() {
  const room = mockRooms[0];
  const [message, setMessage] = useState('');

  return (
    <RoomLayout isHost roomName={room.name}>
      <div className="flex flex-col h-[calc(100vh-200px)] border border-border/50 rounded-lg bg-card/50">
        <div className="flex-1 p-4 overflow-auto space-y-4">
          {messages.map(m => (
            <div key={m.id} className="flex gap-3">
              <Avatar className="h-8 w-8">
                <AvatarImage src={m.odAvatar} />
                <AvatarFallback>{m.odName.charAt(0)}</AvatarFallback>
              </Avatar>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-sm">{m.odName}</span>
                  <span className="text-xs text-muted-foreground">{m.createdAt}</span>
                </div>
                <p className="text-sm text-foreground/90">
                  {renderMessageContent(m.content, currentUser.login)}
                </p>
              </div>
            </div>
          ))}
        </div>
        <div className="p-4 border-t border-border/50 flex gap-2">
          <Input 
            placeholder="Digite sua mensagem... (máx 250 caracteres)" 
            value={message} 
            onChange={e => setMessage(e.target.value.slice(0, 250))} 
            className="bg-background/50" 
          />
          <Button size="icon"><Send className="h-4 w-4" /></Button>
        </div>
      </div>
    </RoomLayout>
  );
}
