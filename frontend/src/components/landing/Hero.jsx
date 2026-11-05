import { lazy, Suspense } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Compass } from 'lucide-react';
import GlowButton from '../common/GlowButton';

// Three.js + @react-three/fiber/drei are the heaviest dependency in this
// app by far — code-split them into their own chunk so the landing
// page's critical text/CTAs render immediately and the 3D scene streams
// in afterward instead of blocking first paint.
const HeroVisual = lazy(() => import('../hero/HeroVisual'));

export default function Hero() {
  return (
    <section className="relative min-h-[92vh] overflow-hidden px-4 pb-20 pt-40 sm:px-6 lg:pb-28 lg:pt-48">
      {/* Live 3D research-intelligence environment — full-bleed, sits behind
          the text/CTA column rather than boxed into a small card. */}
      <Suspense fallback={null}>
        <HeroVisual className="pointer-events-auto absolute inset-y-0 right-[-10%] left-[8%] z-0 sm:left-[20%] lg:left-[28%]" />
      </Suspense>

      {/* Left-to-right scrim so hero copy stays legible over the 3D scene
          without hiding it — same "controlled glow" language as the rest
          of the design system, not a flat opaque panel. */}
      <div
        className="pointer-events-none absolute inset-0 z-[1]"
        style={{
          background:
            'linear-gradient(90deg, var(--color-base) 0%, rgba(6,8,17,0.85) 28%, rgba(6,8,17,0.35) 52%, transparent 72%)',
        }}
      />

      <div className="relative z-10 mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.19, 1, 0.22, 1] }}
          className="max-w-xl"
        >
          <h1 className="font-display text-[2.6rem] leading-[1.05] tracking-tight text-text sm:text-6xl lg:text-[3.6rem]">
            Research intelligence,
            <br />
            before you build.
          </h1>
          <p className="mt-6 max-w-md text-[15px] leading-relaxed text-text-dim sm:text-base">
            Revianta reads the papers, repos, datasets, and patents around your idea before
            you write a line of code — so you validate earlier and build with confidence.
          </p>

          <div className="mt-9 flex flex-wrap items-center gap-3">
            <GlowButton as={Link} to="/register" size="lg">
              Start a project
              <ArrowRight size={17} />
            </GlowButton>
            <GlowButton as={Link} to="/dashboard" variant="ghost" size="lg">
              <Compass size={17} />
              Explore intelligence
            </GlowButton>
          </div>

          <div className="mt-12 flex items-center gap-6 border-t border-line pt-6 text-sm text-text-faint">
            <span>428 papers analyzed</span>
            <span className="h-1 w-1 rounded-full bg-text-faint" />
            <span>112 repositories mapped</span>
            <span className="hidden h-1 w-1 rounded-full bg-text-faint sm:block" />
            <span className="hidden sm:block">61 patents cross-checked</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
