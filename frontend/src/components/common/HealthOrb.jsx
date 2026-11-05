import useCountUp from '../../hooks/useCountUp';
import useReducedMotion from '../../hooks/useReducedMotion';
import { cn } from '../../utils/cn';

function healthColor(score) {
  if (score >= 65) return { stroke: 'var(--color-cyan)', glow: 'rgba(53,224,208,0.45)' };
  if (score >= 40) return { stroke: 'var(--color-amber)', glow: 'rgba(242,178,92,0.4)' };
  return { stroke: 'var(--color-rose)', glow: 'rgba(239,106,124,0.4)' };
}

/**
 * HealthOrb — signature visual #2: a large animated ring gauge for
 * "Overall Project Health", used on the Risk Intelligence page and the
 * project workspace header. Reuses the same ring-gauge idea as the small
 * indicator on ProjectCard, scaled up with a count-up animation and glow.
 */
export default function HealthOrb({ score = 0, label = 'Project Health', size = 176, className }) {
  const reducedMotion = useReducedMotion();
  const animated = useCountUp(score, { enabled: !reducedMotion });
  const { stroke, glow } = healthColor(score);

  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const dash = (animated / 100) * circumference;

  return (
    <div className={cn('relative flex flex-col items-center justify-center', className)} style={{ width: size, height: size }}>
      <div
        className="absolute inset-0 rounded-full blur-2xl"
        style={{ background: `radial-gradient(closest-side, ${glow}, transparent)` }}
        aria-hidden="true"
      />
      <svg viewBox="0 0 100 100" className="relative -rotate-90" style={{ width: size, height: size }}>
        <circle cx="50" cy="50" r={radius} fill="none" stroke="rgba(148,163,214,0.14)" strokeWidth="7" />
        <circle
          cx="50" cy="50" r={radius} fill="none"
          stroke={stroke} strokeWidth="7" strokeLinecap="round"
          strokeDasharray={`${dash} ${circumference}`}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="font-display text-4xl text-text">{Math.round(animated)}%</span>
        <span className="mt-1 text-xs text-text-dim">{label}</span>
      </div>
    </div>
  );
}
