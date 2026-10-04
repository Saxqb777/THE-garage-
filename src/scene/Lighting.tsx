'use client';

import { Environment, Lightformer } from '@react-three/drei';

export const BACKDROP = '#08090b';

// Light panels on the far garage walls, facing the car. They read as the room in the backdrop
// and give the paint something to reflect along its sides.
const WALL_PANELS: [number, number, number][] = [
  [-13, 1.8, 3],
  [-12, 1.8, -5],
  [-7, 1.8, -12],
  [1, 1.8, -14],
  [9, 1.8, -11],
  [13, 1.8, 2],
  [6, 1.8, 13],
  [-6, 1.8, 13],
];

/**
 * Garage studio built from Lightformers and rendered into a cube map once, so lighting,
 * reflections and the backdrop need no HDRI download.
 */
export default function Lighting() {
  return (
    <>
      <fog attach="fog" args={[BACKDROP, 9, 30]} />
      <Environment resolution={512} background backgroundBlurriness={0.12} backgroundIntensity={0.4}>
        <color attach="background" args={[BACKDROP]} />
        {/* softbox strips along the car, overhead */}
        {[-2.4, 0, 2.4].map((x) => (
          <Lightformer key={x} form="rect" intensity={2.6} position={[x, 5.5, 0]} rotation={[Math.PI / 2, 0, 0]} scale={[1.1, 11, 1]} />
        ))}
        {/* dim ceiling fill */}
        <Lightformer form="rect" intensity={0.5} position={[0, 8, 0]} rotation={[Math.PI / 2, 0, 0]} scale={[16, 16, 1]} />
        {WALL_PANELS.map((p) => (
          <Lightformer key={p.join()} form="rect" intensity={0.75} position={p} scale={[1.2, 3, 1]} target={[0, 1.8, 0]} />
        ))}
        {/* warm key softbox and a ring accent from the front left (behind the hero camera), cool rim high at the rear right */}
        <Lightformer form="rect" intensity={4} color="#fff4e8" position={[6.5, 2.2, 6.5]} scale={[6, 3, 1]} target={[0, 0.9, 0]} />
        <Lightformer form="ring" intensity={4} color="#fff1df" position={[7, 5.5, 5]} scale={3} target={[0, 0.8, 0]} />
        <Lightformer form="rect" intensity={2} color="#dfe8ff" position={[-6, 7, -6]} scale={[5, 2.5, 1]} target={[0, 0.8, 0]} />
      </Environment>
    </>
  );
}
