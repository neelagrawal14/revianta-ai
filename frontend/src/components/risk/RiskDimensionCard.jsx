import GlassCard from '../common/GlassCard';
import Badge from '../common/Badge';
import { cn } from '../../utils/cn';

const SEVERITY_TONE = { Low: 'cyan', Medium: 'amber', High: 'rose' };
const SEVERITY_COLOR = { Low: 'var(--color-cyan)', Medium: 'var(--color-amber)', High: 'var(--color-rose)' };

/**
 * RiskDimensionCard — one of the seven NRIE dimensions: score, severity,
 * the reason behind the score, and the contributing factors.
 */
export default function RiskDimensionCard({ dimension }) {
  const color = SEVERITY_COLOR[dimension.severity] || SEVERITY_COLOR.Medium;

  return (
    <GlassCard className="p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm text-text-dim">{dimension.label}</p>
          <p className="mt-1 font-display text-2xl text-text">{dimension.score}%</p>
        </div>
        <Badge tone={SEVERITY_TONE[dimension.severity] || 'amber'}>{dimension.severity}</Badge>
      </div>

      <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-white/[0.06]">
        <div
          className={cn('h-full rounded-full transition-all duration-700 ease-out')}
          style={{ width: `${dimension.score}%`, background: color }}
        />
      </div>

      <p className="mt-4 text-sm text-text-dim">{dimension.reason}</p>

      {dimension.factors?.length > 0 && (
        <ul className="mt-3 space-y-1.5 border-t border-line pt-3">
          {dimension.factors.map((f) => (
            <li key={f} className="flex gap-2 text-xs text-text-faint">
              <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-text-faint" />
              {f}
            </li>
          ))}
        </ul>
      )}
    </GlassCard>
  );
}
