import { cn } from '@/lib/utils';
import { CheckCircle, XCircle, Clock, AlertTriangle, Bug } from 'lucide-react';

interface StatusBadgeProps {
  status: 'accepted' | 'wrong_answer' | 'time_limit' | 'runtime_error' | 'compile_error';
}

const statusConfig = {
  accepted: { 
    label: 'Aceito', 
    icon: CheckCircle,
    className: 'bg-neon-green/20 text-neon-green border-neon-green/50' 
  },
  wrong_answer: { 
    label: 'Resposta Errada', 
    icon: XCircle,
    className: 'bg-destructive/20 text-destructive border-destructive/50' 
  },
  time_limit: { 
    label: 'Tempo Excedido', 
    icon: Clock,
    className: 'bg-neon-orange/20 text-neon-orange border-neon-orange/50' 
  },
  runtime_error: { 
    label: 'Erro de Execução', 
    icon: AlertTriangle,
    className: 'bg-neon-yellow/20 text-neon-yellow border-neon-yellow/50' 
  },
  compile_error: { 
    label: 'Erro de Compilação', 
    icon: Bug,
    className: 'bg-accent/20 text-accent border-accent/50' 
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium',
        config.className
      )}
    >
      <Icon className="h-3 w-3" />
      {config.label}
    </span>
  );
}
