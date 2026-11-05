import { cn } from '../../utils/cn';

const TONES = {
  neutral: 'bg-white/[0.06] text-text-dim border-line',
  indigo: 'bg-indigo/10 text-indigo-soft border-indigo/30',
  cyan: 'bg-cyan/10 text-cyan border-cyan/30',
  amber: 'bg-amber/10 text-amber border-amber/30',
  rose: 'bg-rose/10 text-rose border-rose/30',
};

/** Small pill label used for tags, risk levels, and status. */
export default function Badge({ tone = 'neutral', className, children }) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium leading-none',
        TONES[tone],
        className
      )}
    >
      {children}
    </span>
  );
}

/** Maps a project risk level to a Badge tone + dot color. */
export function riskTone(risk) {
  switch (risk?.toLowerCase()) {
    case 'low':
      return 'cyan';
    case 'high':
      return 'rose';
    default:
      return 'amber';
  }
}
