import { cn } from '@/lib/utils';
import { BALLOON_COLORS } from '@/data/mockData';

interface BalloonBadgeProps {
  color: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  className?: string;
}

export function BalloonBadge({ color, size = 'md', showLabel = false, className }: BalloonBadgeProps) {
  const balloon = BALLOON_COLORS.find(b => b.label === color || b.value === color);
  const hex = balloon?.hex || color;
  const label = balloon?.label || color;
  const value = balloon?.value || color;

  const sizeClasses = {
    sm: 'w-3 h-6',
    md: 'w-4 h-8',
    lg: 'w-6 h-12',
  };

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className={sizeClasses[size]}>
        <img
          src={value}
          alt={label}
          className="w-full h-full object-contain"
          style={{
            filter: `drop-shadow(0 0 6px ${hex})`,
            background: 'transparent'
          }}
        />
      </div>

      {showLabel && (
        <span className="text-sm text-muted-foreground">{label}</span>
      )}
    </div>
  );
}