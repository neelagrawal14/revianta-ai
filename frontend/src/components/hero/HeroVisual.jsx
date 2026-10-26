import { Suspense, useEffect, useRef, useState } from 'react';
import Hero3DScene from './Hero3DScene';
import NodeGraph from '../common/NodeGraph';
import useReducedMotion from '../../hooks/useReducedMotion';
import useResponsiveTier from '../../hooks/useResponsiveTier';
import { isWebGLAvailable } from '../../utils/webgl';
import { cn } from '../../utils/cn';

/**
 * HeroVisual — "Revianta AI's intelligence system running behind the
 * interface." Live 3D research-intelligence environment: floating
 * abstract objects + a small knowledge-graph of glowing nodes, with
 * mouse parallax and gentle scroll drift.
 *
 * Falls back to the static NodeGraph SVG (same one used elsewhere) when
 * WebGL isn't available, so there's no blank space or console error on
 * unsupported browsers.
 *
 * DOM-level pointer/scroll tracking lives here (outside the Canvas) so it
 * keeps working even where the canvas itself sits behind other content.
 */
export default function HeroVisual({ className }) {
  const containerRef = useRef(null);
  const pointerRef = useRef({ x: 0, y: 0 });
  const scrollRef = useRef(0);
  const [webgl, setWebgl] = useState(() => isWebGLAvailable());
  const [mounted, setMounted] = useState(false);

  const reducedMotion = useReducedMotion();
  const tier = useResponsiveTier();

  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 60);
    return () => clearTimeout(t);
  }, []);

  useEffect(() => {
    function handlePointerMove(e) {
      const rect = containerRef.current?.getBoundingClientRect();
      if (!rect) return;
      pointerRef.current = {
        x: ((e.clientX - rect.left) / rect.width) * 2 - 1,
        y: -(((e.clientY - rect.top) / rect.height) * 2 - 1),
      };
    }
    function handleScroll() {
      scrollRef.current = Math.min(window.scrollY / 900, 1);
    }
    window.addEventListener('pointermove', handlePointerMove, { passive: true });
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  if (!webgl) {
    return (
      <div className={cn('flex items-center justify-center', className)}>
        <div className="glass-strong w-full max-w-xl rounded-[28px] p-6">
          <NodeGraph className="h-auto w-full" />
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={cn(
        'transition-opacity duration-[1200ms] ease-out',
        mounted ? 'opacity-100' : 'opacity-0',
        className
      )}
      aria-hidden="true"
    >
      <Suspense fallback={null}>
        <Hero3DScene
          tier={tier}
          motionEnabled={!reducedMotion}
          pointerRef={pointerRef}
          scrollRef={scrollRef}
        />
      </Suspense>
    </div>
  );
}
