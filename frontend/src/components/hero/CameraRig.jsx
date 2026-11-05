import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

/**
 * CameraRig — moves the camera a small amount toward the pointer target
 * and applies a gentle scroll-driven rotation, always damped so motion
 * reads as smooth drift rather than snapping.
 */
export default function CameraRig({ pointer, scrollRef, motionEnabled = true }) {
  const baseLookAt = useRef(new THREE.Vector3(2, 0, 0));

  useFrame((state, delta) => {
    if (!motionEnabled) return;
    const { camera } = state;
    const scroll = scrollRef.current || 0;

    const targetX = 2 + pointer.current.x * 0.6;
    const targetY = pointer.current.y * 0.35 - scroll * 0.6;

    camera.position.x = THREE.MathUtils.damp(camera.position.x, targetX, 2.5, delta);
    camera.position.y = THREE.MathUtils.damp(camera.position.y, targetY, 2.5, delta);
    camera.position.z = THREE.MathUtils.damp(camera.position.z, 9 - scroll * 1.2, 2.5, delta);
    camera.lookAt(baseLookAt.current);
  });

  return null;
}
