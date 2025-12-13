import { cn } from '@/lib/utils';

interface TagBadgeProps {
  tag: string;
  color?: 'cyan' | 'purple' | 'pink' | 'green' | 'orange' | 'yellow';
  size?: 'sm' | 'md';
  onClick?: () => void;
  selected?: boolean;
}

const colorClasses = {
  cyan: 'bg-neon-cyan/20 text-neon-cyan border-neon-cyan/50 hover:bg-neon-cyan/30',
  purple: 'bg-primary/20 text-primary border-primary/50 hover:bg-primary/30',
  pink: 'bg-accent/20 text-accent border-accent/50 hover:bg-accent/30',
  green: 'bg-neon-green/20 text-neon-green border-neon-green/50 hover:bg-neon-green/30',
  orange: 'bg-neon-orange/20 text-neon-orange border-neon-orange/50 hover:bg-neon-orange/30',
  yellow: 'bg-neon-yellow/20 text-neon-yellow border-neon-yellow/50 hover:bg-neon-yellow/30',
};

export function TagBadge({ tag, color = 'purple', size = 'sm', onClick, selected }: TagBadgeProps) {
  const sizeClasses = size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-3 py-1';

  return (
    <span
      onClick={onClick}
      className={cn(
        'inline-flex items-center rounded-full border font-mono transition-all',
        colorClasses[color],
        sizeClasses,
        onClick && 'cursor-pointer',
        selected && 'ring-2 ring-offset-2 ring-offset-background ring-current'
      )}
    >
      #{tag}
    </span>
  );
}
