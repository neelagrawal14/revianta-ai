import { cn } from '../../utils/cn';

/**
 * LoadingState — an "intelligent" loading indicator: three nodes pulsing
 * in sequence, echoing the research-graph motif rather than a generic
 * spinner or skeleton bar.
 */
export default function LoadingState({ label = 'Analyzing', className }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className={cn('flex flex-col items-center justify-center gap-4 py-16 text-center', className)}
    >
      <svg width="72" height="28" viewBox="0 0 72 28" aria-hidden="true">
        {[10, 36, 62].map((cx, i) => (
          <circle
            key={cx}
            cx={cx}
            cy="14"
            r="5"
            fill="var(--color-indigo-soft)"
            style={{
              animation: 'pulse-node 1.4s ease-in-out infinite',
              animationDelay: `${i * 0.2}s`,
            }}
          />
        ))}
        <line x1="15" y1="14" x2="31" y2="14" stroke="var(--color-line-strong)" strokeWidth="1.5" />
        <line x1="41" y1="14" x2="57" y2="14" stroke="var(--color-line-strong)" strokeWidth="1.5" />
      </svg>
      <p className="text-sm text-text-dim">{label}…</p>
    </div>
  );
}
