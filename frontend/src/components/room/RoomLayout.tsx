import { ReactNode } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { RoomMenu } from './RoomMenu';
import { mockRooms } from '@/data/mockData';

interface RoomLayoutProps {
  children: ReactNode;
  isHost?: boolean;
  roomName?: string;
}

export function RoomLayout({ children, isHost = false, roomName }: RoomLayoutProps) {
  const room = mockRooms[0];
  
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          <RoomMenu isHost={isHost} roomName={roomName || room.name} endTime={room.endTime} />
          <main className="flex-1 min-w-0">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
