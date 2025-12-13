import { Link } from 'react-router-dom';
import { ThumbsUp, ThumbsDown, Users, CheckCircle, Clock, HardDrive } from 'lucide-react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { TagBadge } from '@/components/ui/TagBadge';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { Problem } from '@/types';
import { problemTags } from '@/data/mockData';

interface ProblemCardProps {
  problem: Problem;
}

export function ProblemCard({ problem }: ProblemCardProps) {
  const getTagColor = (tagName: string) => {
    const tag = problemTags.find(t => t.name === tagName);
    return (tag?.color as 'cyan' | 'purple' | 'pink' | 'green' | 'orange' | 'yellow') || 'purple';
  };

  return (
    <Link to={`/problem/${problem.id}`}>
      <Card className="group relative overflow-hidden border-border/50 bg-card/50 backdrop-blur transition-all hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
        
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between gap-2">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground font-mono">#{problem.id}</span>
                <DifficultyBadge difficulty={problem.difficulty} />
              </div>
              <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors line-clamp-1">
                {problem.title}
              </h3>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pb-2">
          <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
            {problem.description}
          </p>
          
          <div className="flex flex-wrap gap-1.5">
            {problem.tags.slice(0, 3).map((tag) => (
              <TagBadge key={tag} tag={tag} color={getTagColor(tag)} />
            ))}
            {problem.tags.length > 3 && (
              <span className="text-xs text-muted-foreground">+{problem.tags.length - 3}</span>
            )}
          </div>
        </CardContent>

        <CardFooter className="pt-2 border-t border-border/50">
          <div className="flex items-center justify-between w-full text-xs text-muted-foreground">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1">
                <Users className="h-3 w-3" />
                {problem.attempts}
              </span>
              <span className="flex items-center gap-1 text-neon-green">
                <CheckCircle className="h-3 w-3" />
                {problem.solved}
              </span>
            </div>
            
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1">
                <ThumbsUp className="h-3 w-3" />
                {problem.likes}
              </span>
              <span className="flex items-center gap-1">
                <ThumbsDown className="h-3 w-3" />
                {problem.dislikes}
              </span>
            </div>
          </div>
        </CardFooter>
      </Card>
    </Link>
  );
}
