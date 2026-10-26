import GlassCard from './GlassCard';
import { cn } from '../../utils/cn';

/**
 * MetricCard — a single workspace metric (count + trend).
 * Numbers are set in mono to read as measured/instrumented data.
 */
export default function MetricCard({ label, value, delta, positive, className }) {
  const isPositive = positive ?? (typeof delta === 'string' ? delta.trim().startsWith('+') : undefined);

  return (
    <GlassCard className={cn('p-5', className)}>
      <p className="text-sm text-text-dim">{label}</p>
      <p className="mt-3 font-display text-3xl text-text">{value}</p>
      {delta && (
        <p
          className={cn(
            'mono-tag mt-2',
            isPositive === undefined ? 'text-text-faint' : isPositive ? 'text-cyan' : 'text-rose'
          )}
        >
          {delta}
        </p>
      )}
    </GlassCard>
  );
}
