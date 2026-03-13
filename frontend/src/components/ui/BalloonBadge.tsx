import { cn } from '@/lib/utils';
import { BALLOON_COLORS } from '@/data/mockData';

interface BalloonBadgeProps {
  color: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  className?: string;
}

export function BalloonBadge({ color, size = 'md', showLabel = false, className }: BalloonBadgeProps) {
  const balloon = BALLOON_COLORS.find(b => b.value === color);
  const hex = balloon?.hex || color;
  const label = balloon?.label || color;

  const sizeClasses = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-6 h-6',
  };

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div 
        className={cn(
          'rounded-full shadow-sm',
          sizeClasses[size]
        )}
        style={{ 
          backgroundColor: hex,
          boxShadow: `0 0 8px ${hex}40`,
        }}
      />
      {showLabel && (
        <span className="text-sm text-muted-foreground">{label}</span>
      )}
    </div>
  );
}