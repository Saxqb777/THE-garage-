'use client';

import { ContactShadows } from '@react-three/drei';

/**
 * The floor itself comes from the ground projected HDRI (see Lighting). This adds the soft
 * contact shadow under the car so it sits on that floor instead of floating over it.
 */
export default function Ground() {
  return <ContactShadows position={[0, 0.002, -0.1]} scale={[6, 8.5]} resolution={1024} blur={3.2} far={1.2} opacity={0.55} />;
}
