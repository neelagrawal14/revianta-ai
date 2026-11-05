import FloatingShape from './FloatingShape';

/**
 * FloatingObjects — the organic (non-symmetrical) collection of shapes
 * that make up the hero composition. Each entry has its own depth
 * (parallax strength), size, material, and motion so nothing feels
 * uniform or grid-like.
 *
 * `tier` trims the set for tablet/mobile so lower-power devices render
 * fewer objects rather than the same scene at a smaller size.
 */
const ALL_SHAPES = [
  { key: 'core-sphere', geometry: 'sphere', position: [1.6, 0.4, -0.5], scale: 1.35, color: '#5b5ff0', emissive: '#5b5ff0', emissiveIntensity: 0.4, roughness: 0.15, metalness: 0.6, depth: 0.7, floatSpeed: 0.7, floatIntensity: 0.9, rotationIntensity: 0.5, tier: 'all' },
  { key: 'glass-sphere', geometry: 'sphere', position: [3.4, -1.1, 0.6], scale: 0.85, color: '#9153ea', emissive: '#9153ea', emissiveIntensity: 0.25, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.55, depth: 1, floatSpeed: 1.1, floatIntensity: 1.2, rotationIntensity: 0.8, tier: 'all' },
  { key: 'rounded-cube', geometry: 'roundedBox', position: [0.4, -1.6, -1.2], scale: 0.9, color: '#141a33', emissive: '#5b5ff0', emissiveIntensity: 0.18, roughness: 0.35, metalness: 0.7, depth: 0.4, floatSpeed: 0.6, floatIntensity: 0.7, rotationIntensity: 0.6, tier: 'all' },
  { key: 'lowpoly', geometry: 'icosahedron', position: [4.4, 1.3, -1.6], scale: 0.7, color: '#1a2140', emissive: '#35e0d0', emissiveIntensity: 0.3, roughness: 0.4, metalness: 0.5, wireframe: false, depth: 0.3, floatSpeed: 0.9, floatIntensity: 0.8, rotationIntensity: 1.4, tier: 'desktop' },
  { key: 'ring-large', geometry: 'ring', position: [2.6, 1.9, -2.2], scale: 1.5, color: '#35e0d0', emissive: '#35e0d0', emissiveIntensity: 0.35, roughness: 0.3, metalness: 0.6, depth: 0.25, floatSpeed: 0.5, floatIntensity: 0.5, rotationIntensity: 0.4, tier: 'all' },
  { key: 'ring-small', geometry: 'ring', position: [0.2, 1.1, 0.8], scale: 0.55, color: '#7c80f5', emissive: '#7c80f5', emissiveIntensity: 0.3, roughness: 0.25, metalness: 0.5, depth: 0.9, floatSpeed: 1.2, floatIntensity: 1.1, rotationIntensity: 1.1, tier: 'tablet' },
  { key: 'torus', geometry: 'torus', position: [3.9, -0.2, -0.8], scale: 0.6, color: '#9153ea', emissive: '#9153ea', emissiveIntensity: 0.28, roughness: 0.3, metalness: 0.55, depth: 0.6, floatSpeed: 0.8, floatIntensity: 0.9, rotationIntensity: 0.9, tier: 'desktop' },
  { key: 'accent-sphere-1', geometry: 'sphere', position: [1.1, -2.3, 0.9], scale: 0.28, color: '#35e0d0', emissive: '#35e0d0', emissiveIntensity: 0.9, roughness: 0.1, metalness: 0.2, depth: 1.1, floatSpeed: 1.6, floatIntensity: 1.4, rotationIntensity: 0.5, tier: 'all' },
  { key: 'accent-sphere-2', geometry: 'sphere', position: [4.9, 0.2, 1.1], scale: 0.22, color: '#f2b25c', emissive: '#f2b25c', emissiveIntensity: 0.8, roughness: 0.1, metalness: 0.2, depth: 1.2, floatSpeed: 1.4, floatIntensity: 1.3, rotationIntensity: 0.5, tier: 'desktop' },
  { key: 'matte-box', geometry: 'roundedBox', position: [3.1, 2.4, 0.3], scale: 0.5, color: '#10142a', emissive: '#5b5ff0', emissiveIntensity: 0.15, roughness: 0.6, metalness: 0.2, depth: 0.35, floatSpeed: 0.65, floatIntensity: 0.6, rotationIntensity: 0.7, tier: 'tablet' },
];

const TIER_ORDER = { mobile: 0, tablet: 1, desktop: 2, all: -1 };

export default function FloatingObjects({ tier = 'desktop', parallax, motionEnabled = true }) {
  const shapes = ALL_SHAPES.filter((s) => TIER_ORDER[s.tier] <= TIER_ORDER[tier] || s.tier === 'all');

  return (
    <group>
      {shapes.map((s) => (
        <FloatingShape key={s.key} {...s} parallax={parallax} motionEnabled={motionEnabled} />
      ))}
    </group>
  );
}
