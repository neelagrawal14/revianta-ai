import { useEffect, useRef, useState } from 'react';

/**
 * useCountUp — animates a number from 0 (or its previous value) up to
 * `target` over `duration` ms. Used by HealthOrb, risk score cards, and
 * workspace metrics so numbers feel "calculated" rather than static.
 * Respects reduced motion by snapping instantly when `enabled` is false.
 */
export default function useCountUp(target, { duration = 900, enabled = true } = {}) {
  const [value, setValue] = useState(enabled ? 0 : target);
  const frameRef = useRef();

  useEffect(() => {
    if (!enabled) {
      setValue(target);
      return;
    }
    const start = performance.now();
    const from = 0;

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      setValue(from + (target - from) * eased);
      if (progress < 1) {
        frameRef.current = requestAnimationFrame(tick);
      }
    }

    frameRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, duration, enabled]);

  return value;
}
