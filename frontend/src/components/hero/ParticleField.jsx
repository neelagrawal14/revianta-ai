import { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';

/**
 * ParticleField — a single Points object (one draw call) used for the
 * "very subtle particles" background layer. Count is tuned per tier so
 * mobile skips it (or renders very few) rather than tanking frame rate.
 */
export default function ParticleField({ count = 140, motionEnabled = true }) {
  const pointsRef = useRef();

  const positions = useMemo(() => {
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const radius = 4 + Math.random() * 5;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      arr[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      arr[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta) * 0.6;
      arr[i * 3 + 2] = radius * Math.cos(phi) - 2;
    }
    return arr;
  }, [count]);

  useFrame((_, delta) => {
    if (pointsRef.current && motionEnabled) {
      pointsRef.current.rotation.y += delta * 0.015;
    }
  });

  if (count <= 0) return null;

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial color="#7c80f5" size={0.035} sizeAttenuation transparent opacity={0.5} />
    </points>
  );
}
