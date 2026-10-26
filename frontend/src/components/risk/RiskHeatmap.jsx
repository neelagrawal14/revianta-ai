import { cn } from '../../utils/cn';

function colorFor(score) {
  if (score >= 60) return 'bg-rose/70';
  if (score >= 35) return 'bg-amber/60';
  return 'bg-cyan/50';
}

/**
 * RiskHeatmap — a compact single-row heatmap across all seven
 * dimensions, for a quick "where's the heat" read before scanning the
 * full dimension cards.
 */
export default function RiskHeatmap({ dimensions, className }) {
  return (
    <div className={cn('grid grid-cols-7 gap-1.5', className)}>
      {dimensions.map((d) => (
        <div key={d.id} className="flex flex-col items-center gap-1.5">
          <div
            className={cn('h-10 w-full rounded-lg border border-white/10', colorFor(d.score))}
            title={`${d.label}: ${d.score}%`}
          />
          <span className="mono-tag text-center text-[10px] leading-tight text-text-faint">
            {d.label.replace(' Risk', '')}
          </span>
        </div>
      ))}
    </div>
  );
}
