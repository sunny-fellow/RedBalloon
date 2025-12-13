import { Link } from 'react-router-dom';
import { ThumbsUp, CheckCircle, MapPin } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { User } from '@/types';

interface UserCardProps {
  user: User;
}

export function UserCard({ user }: UserCardProps) {
  return (
    <Link to={`/user/${user.id}`}>
      <Card className="group relative overflow-hidden border-border/50 bg-card/50 backdrop-blur transition-all hover:border-secondary/50 hover:shadow-lg hover:shadow-secondary/10">
        <div className="absolute inset-0 bg-gradient-to-br from-secondary/5 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
        
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <Avatar className="h-16 w-16 ring-2 ring-border group-hover:ring-secondary/50 transition-all">
              <AvatarImage src={user.avatar} alt={user.name} />
              <AvatarFallback className="bg-secondary/20 text-secondary text-lg">
                {user.name.charAt(0)}
              </AvatarFallback>
            </Avatar>

            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-foreground group-hover:text-secondary transition-colors truncate">
                {user.name}
              </h3>
              <p className="text-sm text-muted-foreground truncate">@{user.login}</p>
              
              <div className="flex items-center gap-1 mt-1 text-xs text-muted-foreground">
                <MapPin className="h-3 w-3" />
                {user.country}
              </div>
            </div>
          </div>

          <div className="flex items-center justify-around mt-4 pt-3 border-t border-border/50">
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 text-neon-green">
                <CheckCircle className="h-4 w-4" />
                <span className="font-bold">{user.problemsSolved}</span>
              </div>
              <span className="text-xs text-muted-foreground">Resolvidos</span>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 text-accent">
                <ThumbsUp className="h-4 w-4" />
                <span className="font-bold">{user.likes}</span>
              </div>
              <span className="text-xs text-muted-foreground">Likes</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
