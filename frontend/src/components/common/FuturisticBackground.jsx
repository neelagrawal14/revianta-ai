import { cn } from '../../utils/cn';

/**
 * FuturisticBackground — the ambient environment behind every screen.
 *
 * Composed of three cheap, static-friendly layers so it stays performant:
 *  1. a fixed void gradient (no animation)
 *  2. two slow-drifting radial glows (CSS animation, GPU-friendly)
 *  3. a faint fixed grid + noise-free vignette
 *
 * `variant="cinematic"` (landing hero) adds a touch more glow strength.
 * Respect `prefers-reduced-motion` — the drift animation is disabled
 * globally in index.css for reduced-motion users.
 */
export default function FuturisticBackground({ variant = 'default', className }) {
  const strong = variant === 'cinematic';

  return (
    <div className={cn('pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-base', className)} aria-hidden="true">
      {/* base grid */}
      <div
        className="absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(148,163,214,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,214,0.06) 1px, transparent 1px)',
          backgroundSize: '64px 64px',
          maskImage: 'radial-gradient(ellipse 80% 60% at 50% 0%, black 40%, transparent 100%)',
        }}
      />

      {/* drifting glows */}
      <div
        className="absolute -top-40 left-[8%] h-[36rem] w-[36rem] rounded-full blur-[120px]"
        style={{
          background: `radial-gradient(closest-side, rgba(91,95,240,${strong ? 0.32 : 0.22}), transparent)`,
          animation: 'drift 22s ease-in-out infinite',
        }}
      />
      <div
        className="absolute top-1/3 right-[4%] h-[30rem] w-[30rem] rounded-full blur-[130px]"
        style={{
          background: `radial-gradient(closest-side, rgba(145,83,234,${strong ? 0.28 : 0.18}), transparent)`,
          animation: 'drift 26s ease-in-out infinite reverse',
        }}
      />
      <div
        className="absolute bottom-[-10%] left-1/3 h-[26rem] w-[26rem] rounded-full blur-[130px]"
        style={{
          background: `radial-gradient(closest-side, rgba(53,224,208,${strong ? 0.16 : 0.1}), transparent)`,
          animation: 'drift 30s ease-in-out infinite',
        }}
      />

      {/* vignette to keep edges/content readable */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_35%,rgba(4,5,11,0.7)_100%)]" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-base to-transparent" />
    </div>
  );
}
