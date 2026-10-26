import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Float, RoundedBox } from '@react-three/drei';
import * as THREE from 'three';

/**
 * FloatingShape — a single object in the hero composition. Wrapped in
 * drei's <Float> for the slow bob/rotate/drift, with a small extra
 * hover response (scale + emissive bump) layered on top.
 *
 * `depth` (0 = far, 1 = near) drives how strongly the shape reacts to
 * the shared parallax offset passed down from Hero3DScene.
 */
export default function FloatingShape({
  geometry = 'sphere',
  position = [0, 0, 0],
  scale = 1,
  color = '#5b5ff0',
  emissive = '#5b5ff0',
  emissiveIntensity = 0.35,
  metalness = 0.4,
  roughness = 0.25,
  transparent = false,
  opacity = 1,
  wireframe = false,
  depth = 0.5,
  floatSpeed = 1,
  floatIntensity = 1,
  rotationIntensity = 1,
  parallax = { x: 0, y: 0 },
  motionEnabled = true,
}) {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  useFrame((_, delta) => {
    const mesh = meshRef.current;
    if (!mesh) return;

    // Parallax: nearer shapes (higher depth) shift more with the pointer.
    const targetX = position[0] + parallax.x * depth;
    const targetY = position[1] + parallax.y * depth;
    mesh.position.x = THREE.MathUtils.damp(mesh.position.x, targetX, 4, delta);
    mesh.position.y = THREE.MathUtils.damp(mesh.position.y, targetY, 4, delta);

    // Hover: subtle scale + glow bump.
    const targetScale = hovered ? scale * 1.12 : scale;
    mesh.scale.x = THREE.MathUtils.damp(mesh.scale.x, targetScale, 6, delta);
    mesh.scale.y = THREE.MathUtils.damp(mesh.scale.y, targetScale, 6, delta);
    mesh.scale.z = THREE.MathUtils.damp(mesh.scale.z, targetScale, 6, delta);

    if (mesh.material) {
      const targetEmissive = hovered ? emissiveIntensity * 1.8 : emissiveIntensity;
      mesh.material.emissiveIntensity = THREE.MathUtils.damp(
        mesh.material.emissiveIntensity,
        targetEmissive,
        6,
        delta
      );
    }
  });

  const material = (
    <meshPhysicalMaterial
      color={color}
      emissive={emissive}
      emissiveIntensity={emissiveIntensity}
      metalness={metalness}
      roughness={roughness}
      transparent={transparent}
      opacity={opacity}
      wireframe={wireframe}
      clearcoat={0.4}
      clearcoatRoughness={0.3}
    />
  );

  const body = (
    <mesh
      ref={meshRef}
      position={position}
      scale={scale}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
      }}
      onPointerOut={() => setHovered(false)}
    >
      {geometry === 'sphere' && <sphereGeometry args={[1, 32, 32]} />}
      {geometry === 'icosahedron' && <icosahedronGeometry args={[1, 0]} />}
      {geometry === 'box' && <boxGeometry args={[1.3, 1.3, 1.3]} />}
      {geometry === 'torus' && <torusGeometry args={[1, 0.32, 16, 48]} />}
      {geometry === 'ring' && <torusGeometry args={[1, 0.06, 12, 64]} />}
      {material}
    </mesh>
  );

  // RoundedBox needs drei's own geometry component rather than <boxGeometry>.
  const roundedBody = (
    <RoundedBox
      ref={meshRef}
      args={[1.2, 1.2, 1.2]}
      radius={0.18}
      smoothness={4}
      position={position}
      scale={scale}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
      }}
      onPointerOut={() => setHovered(false)}
    >
      {material}
    </RoundedBox>
  );

  const content = geometry === 'roundedBox' ? roundedBody : body;

  if (!motionEnabled) return content;

  return (
    <Float speed={floatSpeed} floatIntensity={floatIntensity} rotationIntensity={rotationIntensity}>
      {content}
    </Float>
  );
}
