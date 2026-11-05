import { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

/**
 * ResearchNetwork — the "meaning" layer of the hero: a small cluster of
 * glowing nodes (paper / technology / dataset / GitHub / patent / project)
 * connected by thin lines, echoing Revianta's knowledge-graph concept.
 * Connections pulse slowly rather than carrying any on-scene text.
 */
const NODE_TYPES = [
  { id: 'project', color: '#5b5ff0', position: [2.3, 0.3, 1.4] },
  { id: 'paper-1', color: '#35e0d0', position: [0.6, 1.5, 0.4] },
  { id: 'paper-2', color: '#35e0d0', position: [1.1, -0.9, 1.9] },
  { id: 'tech', color: '#9153ea', position: [3.8, 1.4, 0.9] },
  { id: 'dataset', color: '#7c80f5', position: [3.4, -1.5, 1.6] },
  { id: 'patent', color: '#f2b25c', position: [1.7, 2.2, -0.3] },
];

const LINKS = [
  ['project', 'paper-1'],
  ['project', 'paper-2'],
  ['project', 'tech'],
  ['project', 'dataset'],
  ['tech', 'patent'],
  ['paper-1', 'patent'],
];

export default function ResearchNetwork({ tier = 'desktop', parallax, motionEnabled = true }) {
  const groupRef = useRef();
  const nodeRefs = useRef({});
  const lineRefs = useRef([]);

  const nodes = tier === 'mobile' ? NODE_TYPES.slice(0, 4) : NODE_TYPES;
  const activeIds = new Set(nodes.map((n) => n.id));
  const links = LINKS.filter(([a, b]) => activeIds.has(a) && activeIds.has(b));

  const linePairs = useMemo(
    () =>
      links.map(([a, b]) => {
        const from = nodes.find((n) => n.id === a).position;
        const to = nodes.find((n) => n.id === b).position;
        return { from, to };
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [tier]
  );

  useFrame((state, delta) => {
    if (groupRef.current && motionEnabled) {
      groupRef.current.position.x = THREE.MathUtils.damp(groupRef.current.position.x, parallax.x * 0.55, 4, delta);
      groupRef.current.position.y = THREE.MathUtils.damp(groupRef.current.position.y, parallax.y * 0.55, 4, delta);
    }

    const t = state.clock.elapsedTime;
    lineRefs.current.forEach((mat, i) => {
      if (!mat) return;
      mat.opacity = motionEnabled ? 0.18 + Math.sin(t * 0.6 + i) * 0.12 : 0.22;
    });

    Object.values(nodeRefs.current).forEach((mesh, i) => {
      if (!mesh || !motionEnabled) return;
      mesh.position.y += Math.sin(t * 0.5 + i * 1.3) * 0.0006;
      const s = 1 + Math.sin(t * 0.8 + i) * 0.06;
      mesh.scale.setScalar(s);
    });
  });

  return (
    <group ref={groupRef}>
      {linePairs.map((pair, i) => (
        <line key={i}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={2}
              array={new Float32Array([...pair.from, ...pair.to])}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial
            ref={(el) => (lineRefs.current[i] = el)}
            color="#8990d6"
            transparent
            opacity={0.2}
          />
        </line>
      ))}

      {nodes.map((node) => (
        <mesh key={node.id} position={node.position} ref={(el) => (nodeRefs.current[node.id] = el)}>
          <sphereGeometry args={[0.09, 16, 16]} />
          <meshStandardMaterial color={node.color} emissive={node.color} emissiveIntensity={1.4} toneMapped={false} />
        </mesh>
      ))}
    </group>
  );
}
