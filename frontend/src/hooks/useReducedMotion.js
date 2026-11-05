import { useEffect, useState } from 'react';

/**
 * useReducedMotion — tracks the `prefers-reduced-motion` media query so
 * animated components (the 3D hero, in particular) can tone themselves
 * down or stop entirely.
 */
export default function useReducedMotion() {
  const [reduced, setReduced] = useState(
    () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  );

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handler = (e) => setReduced(e.matches);
    mq.addEventListener?.('change', handler);
    return () => mq.removeEventListener?.('change', handler);
  }, []);

  return reduced;
}
