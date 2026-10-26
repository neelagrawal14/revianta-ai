import { useEffect, useState } from 'react';
import { Check, Loader2 } from 'lucide-react';
import { cn } from '../../utils/cn';
import useReducedMotion from '../../hooks/useReducedMotion';

/**
 * AnalysisSequence — the "REVIANTA INTELLIGENCE ENGINE" loading
 * experience: steps through a list of pipeline stages one at a time,
 * then calls `onComplete`. Used by the New Project wizard's "Run
 * Research Intelligence" step; reusable anywhere the app needs to
 * dramatize a multi-stage analysis instead of a plain spinner.
 */
export default function AnalysisSequence({ steps, stepDuration = 850, onComplete, className }) {
  const reducedMotion = useReducedMotion();
  const [activeIndex, setActiveIndex] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (done) return;
    const duration = reducedMotion ? 120 : stepDuration;

    if (activeIndex >= steps.length) {
      setDone(true);
      onComplete?.();
      return;
    }

    const t = setTimeout(() => setActiveIndex((i) => i + 1), duration);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex, done]);

  return (
    <div className={cn('mx-auto max-w-md text-center', className)} role="status" aria-live="polite">
      <p className="mono-tag text-indigo-soft">Revianta Intelligence Engine</p>
      <h3 className="mt-2 font-display text-xl text-text">Analyzing project…</h3>

      <ul className="mt-8 space-y-3 text-left">
        {steps.map((step, i) => {
          const complete = i < activeIndex;
          const active = i === activeIndex;
          return (
            <li
              key={step}
              className={cn(
                'flex items-center gap-3 rounded-xl border px-4 py-3 text-sm transition-colors duration-300',
                complete && 'border-cyan/25 bg-cyan/[0.06] text-text',
                active && 'border-indigo/35 bg-indigo/[0.08] text-text',
                !complete && !active && 'border-line bg-white/[0.02] text-text-faint'
              )}
            >
              <span className="mono-tag w-7 shrink-0 text-text-faint">{String(i + 1).padStart(2, '0')}</span>
              <span className="flex-1">{step}</span>
              {complete && <Check size={15} className="shrink-0 text-cyan" />}
              {active && <Loader2 size={15} className="shrink-0 animate-spin text-indigo-soft" />}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
