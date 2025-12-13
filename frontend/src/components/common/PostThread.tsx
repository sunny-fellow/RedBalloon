import { useState } from 'react';
import { Link } from 'react-router-dom';
import { MessageSquare, Clock } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { TagBadge } from '@/components/ui/TagBadge';
import { Post } from '@/types';
import { communityTags } from '@/data/mockData';
import { cn } from '@/lib/utils';

interface PostThreadProps {
  post: Post;
  depth?: number;
}

function formatContent(content: string) {
  // Replace @mentions with links
  let formatted = content.replace(
    /@(\w+)/g,
    '<a href="/user/$1" class="text-secondary hover:underline">@$1</a>'
  );
  
  // Replace #problemId with links
  formatted = formatted.replace(
    /#(\d+)/g,
    '<a href="/problem/$1" class="text-primary hover:underline">#$1</a>'
  );

  return formatted;
}

function formatDate(dateString: string) {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);

  if (hours < 1) return 'agora mesmo';
  if (hours < 24) return `${hours}h atrás`;
  if (days < 7) return `${days}d atrás`;
  return date.toLocaleDateString('pt-BR');
}

export function PostThread({ post, depth = 0 }: PostThreadProps) {
  const [showReplyForm, setShowReplyForm] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [showReplies, setShowReplies] = useState(depth < 2);

  const getTagColor = (tagName: string) => {
    const tag = communityTags.find(t => t.name === tagName);
    return (tag?.color as 'cyan' | 'purple' | 'pink' | 'green' | 'orange' | 'yellow') || 'purple';
  };

  return (
    <div className={cn('relative', depth > 0 && 'ml-8 mt-4')}>
      {depth > 0 && (
        <div className="absolute left-[-20px] top-0 bottom-0 w-px bg-border/50" />
      )}
      
      <div className="group p-4 rounded-lg border border-border/50 bg-card/30 hover:bg-card/50 transition-colors">
        <div className="flex gap-3">
          <Link to={`/user/${post.userId}`}>
            <Avatar className="h-10 w-10 ring-2 ring-border group-hover:ring-primary/50 transition-colors">
              <AvatarImage src={post.userAvatar} alt={post.userName} />
              <AvatarFallback>{post.userName.charAt(0)}</AvatarFallback>
            </Avatar>
          </Link>

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <Link 
                to={`/user/${post.userId}`}
                className="font-medium hover:text-primary transition-colors"
              >
                {post.userName}
              </Link>
              <span className="text-xs text-muted-foreground flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {formatDate(post.createdAt)}
              </span>
            </div>

            {post.tags.length > 0 && (
              <div className="flex gap-1 mt-1 flex-wrap">
                {post.tags.map((tag) => (
                  <TagBadge key={tag} tag={tag} color={getTagColor(tag)} size="sm" />
                ))}
              </div>
            )}

            <div 
              className="mt-2 text-sm text-foreground/90"
              dangerouslySetInnerHTML={{ __html: formatContent(post.content) }}
            />

            <div className="flex items-center gap-4 mt-3">
              <Button
                variant="ghost"
                size="sm"
                className="h-7 text-xs gap-1 text-muted-foreground hover:text-primary"
                onClick={() => setShowReplyForm(!showReplyForm)}
              >
                <MessageSquare className="h-3 w-3" />
                Responder
              </Button>

              {post.replies.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-7 text-xs text-muted-foreground"
                  onClick={() => setShowReplies(!showReplies)}
                >
                  {showReplies ? 'Ocultar' : 'Ver'} {post.replies.length} resposta{post.replies.length !== 1 ? 's' : ''}
                </Button>
              )}
            </div>

            {showReplyForm && (
              <div className="mt-3 space-y-2">
                <Textarea
                  placeholder="Escreva sua resposta..."
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  className="min-h-[80px] bg-background/50"
                />
                <div className="flex justify-end gap-2">
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => {
                      setShowReplyForm(false);
                      setReplyContent('');
                    }}
                  >
                    Cancelar
                  </Button>
                  <Button size="sm">Responder</Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {showReplies && post.replies.map((reply) => (
        <PostThread key={reply.id} post={reply} depth={depth + 1} />
      ))}
    </div>
  );
}
