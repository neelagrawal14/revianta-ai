import { useEffect, useState } from 'react';

/**
 * useResponsiveTier — coarse device tier used to scale the hero's 3D scene
 * complexity (object count, particle count, pixel ratio) rather than
 * rendering the same scene everywhere and hoping it's fast enough.
 */
export default function useResponsiveTier() {
  const [tier, setTier] = useState(() => getTier());

  useEffect(() => {
    let frame;
    function onResize() {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => setTier(getTier()));
    }
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      cancelAnimationFrame(frame);
    };
  }, []);

  return tier;
}

function getTier() {
  if (typeof window === 'undefined') return 'desktop';
  const w = window.innerWidth;
  if (w < 640) return 'mobile';
  if (w < 1024) return 'tablet';
  return 'desktop';
}
