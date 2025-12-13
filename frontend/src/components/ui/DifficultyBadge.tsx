import { cn } from '@/lib/utils';

interface DifficultyBadgeProps {
  difficulty: 'easy' | 'medium' | 'hard';
}

const difficultyConfig = {
  easy: { label: 'Fácil', className: 'bg-neon-green/20 text-neon-green border-neon-green/50' },
  medium: { label: 'Médio', className: 'bg-neon-orange/20 text-neon-orange border-neon-orange/50' },
  hard: { label: 'Difícil', className: 'bg-destructive/20 text-destructive border-destructive/50' },
};

export function DifficultyBadge({ difficulty }: DifficultyBadgeProps) {
  const config = difficultyConfig[difficulty];

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium',
        config.className
      )}
    >
      {config.label}
    </span>
  );
}
