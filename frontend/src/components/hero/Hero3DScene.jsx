import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import FloatingObjects from './FloatingObjects';
import ResearchNetwork from './ResearchNetwork';
import ParticleField from './ParticleField';
import CameraRig from './CameraRig';

const PARTICLE_COUNT = { mobile: 0, tablet: 60, desktop: 140 };

/**
 * Hero3DScene — the actual <Canvas>. Kept separate from HeroVisual so the
 * WebGL-dependent tree only exists once we know WebGL is available and
 * the wrapper has set up pointer/scroll tracking.
 */
export default function Hero3DScene({ tier, motionEnabled, pointerRef, scrollRef }) {
  // A tiny live "parallax" value read by children each frame — a plain
  // ref (not React state) so updating it doesn't trigger re-renders;
  // three.js components read it inside their own useFrame instead.
  const parallax = useRef({ x: 0, y: 0 }).current;

  return (
    <Canvas
      dpr={tier === 'mobile' ? 1 : [1, 1.8]}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      camera={{ position: [2, 0, 9], fov: 42, near: 0.1, far: 40 }}
      style={{ background: 'transparent' }}
    >
      <ParallaxSync pointerRef={pointerRef} parallax={parallax} />

      <ambientLight intensity={0.45} />
      <directionalLight position={[4, 6, 5]} intensity={0.8} color="#eef0fb" />
      <pointLight position={[-3, -2, 3]} intensity={22} color="#5b5ff0" />
      <pointLight position={[5, 3, -2]} intensity={18} color="#9153ea" />
      <pointLight position={[1, -3, 4]} intensity={10} color="#35e0d0" />

      <CameraRig pointer={pointerRef} scrollRef={scrollRef} motionEnabled={motionEnabled} />
      <ParticleField count={PARTICLE_COUNT[tier]} motionEnabled={motionEnabled} />
      <ResearchNetwork tier={tier} parallax={parallax} motionEnabled={motionEnabled} />
      <FloatingObjects tier={tier} parallax={parallax} motionEnabled={motionEnabled} />
    </Canvas>
  );
}

/**
 * ParallaxSync — reads the DOM-level pointer ref every frame and damps a
 * shared `parallax` value that FloatingObjects / ResearchNetwork consume.
 * Living inside the Canvas lets it use useFrame.
 */
function ParallaxSync({ pointerRef, parallax }) {
  useFrame(() => {
    parallax.x += (pointerRef.current.x * 0.8 - parallax.x) * 0.06;
    parallax.y += (pointerRef.current.y * 0.5 - parallax.y) * 0.06;
  });
  return null;
}
