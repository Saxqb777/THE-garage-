'use client';

import { useEffect, useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import gsap from 'gsap';
import { Color, Group, MeshStandardMaterial } from 'three';
import { carLift, LIFT_HEIGHT } from './liftState';
import { useGarage } from './store';

/**
 * Two post lift (Garage only), built from simple shapes in the colours of the lifts in the
 * workshop HDRI. Sequence up: posts rise out of the floor, the four arms swing in under the
 * lifting points on the sills, the carriages and the car rise together. Down is the reverse.
 * The car height is the shared carLift value, so the car, its shadow and the camera follow
 * without React re-renders.
 */

const POST_X = 1.5; // posts stand beside the doors, clear of the 1.94 m body
const POST_Z = 0.1;
const POST_H = 3.4;
const PAD_POINTS: [number, number][] = [
  // lifting points under the sills (x, z), just behind the front wheels and ahead of the rear ones
  [0.62, 0.85],
  [0.62, -0.95],
];
const PAD_Y = 0.3; // pad top touching the sill pinch weld with the car down

export default function Lift() {
  const lift = useGarage((s) => s.lift);
  const posts = useRef<Group>(null);
  const carriages = useRef<Group>(null);
  const state = useRef({ deploy: 0, swing: 0 });
  const paint = useMemo(() => new MeshStandardMaterial({ color: new Color('#b0202b'), roughness: 0.45, metalness: 0.2 }), []);
  const steel = useMemo(() => new MeshStandardMaterial({ color: new Color('#2b2d31'), roughness: 0.55, metalness: 0.6 }), []);
  const rubber = useMemo(() => new MeshStandardMaterial({ color: new Color('#111111'), roughness: 0.9 }), []);

  useEffect(() => {
    const st = state.current;
    const tl = gsap.timeline();
    if (lift) {
      useGarage.getState().setHingesOpen(false);
      tl.to(st, { deploy: 1, duration: 0.6, ease: 'power2.out' })
        .to(st, { swing: 1, duration: 0.8, ease: 'power2.inOut' })
        .to(carLift, { y: LIFT_HEIGHT, duration: 3.0, ease: 'power1.inOut' }, '+=0.1');
    } else {
      tl.to(carLift, { y: 0, duration: carLift.y > 0.01 ? 2.6 : 0, ease: 'power1.inOut' })
        .to(st, { swing: 0, duration: 0.6, ease: 'power2.inOut' })
        .to(st, { deploy: 0, duration: 0.5, ease: 'power2.in' });
    }
    return () => {
      tl.kill();
    };
  }, [lift]);

  useEffect(() => () => [paint, steel, rubber].forEach((m) => m.dispose()), [paint, steel, rubber]);

  useFrame(() => {
    const { deploy, swing } = state.current;
    if (posts.current) {
      posts.current.visible = deploy > 0.001;
      posts.current.scale.y = Math.max(deploy, 0.001);
    }
    if (carriages.current) {
      carriages.current.visible = deploy > 0.001;
      carriages.current.position.y = carLift.y;
      // arms swing from along the posts (parked) to under the car
      carriages.current.children.forEach((arm) => {
        const { side, end } = arm.userData as { side: number; end: number };
        arm.rotation.y = side * end * (1 - swing) * 1.25;
      });
    }
  });

  const arms = [];
  for (const side of [1, -1]) {
    for (const [px, pz] of PAD_POINTS) {
      const end = Math.sign(pz);
      const dx = side * px - side * POST_X;
      const dz = pz - POST_Z;
      const len = Math.hypot(dx, dz);
      const yaw = Math.atan2(-dz, dx); // arm points from the post to the pad
      arms.push(
        <group key={`${side}${end}`} position={[side * POST_X, 0, POST_Z]} userData={{ side, end }}>
          <group rotation-y={yaw}>
            <mesh position={[len / 2, PAD_Y - 0.13, 0]} material={steel}>
              <boxGeometry args={[len, 0.08, 0.12]} />
            </mesh>
            <mesh position={[len, PAD_Y - 0.05, 0]} material={rubber}>
              <cylinderGeometry args={[0.07, 0.07, 0.08, 20]} />
            </mesh>
          </group>
        </group>,
      );
    }
  }

  return (
    <group>
      <group ref={posts} visible={false}>
        {[1, -1].map((side) => (
          <group key={side} position={[side * POST_X, 0, POST_Z]}>
            <mesh position={[side * 0.06, POST_H / 2, 0]} material={paint}>
              <boxGeometry args={[0.24, POST_H, 0.3]} />
            </mesh>
            <mesh position={[0, 0.01, 0]} material={steel}>
              <boxGeometry args={[0.5, 0.02, 0.55]} />
            </mesh>
          </group>
        ))}
      </group>
      <group ref={carriages} visible={false}>
        {arms}
      </group>
    </group>
  );
}
