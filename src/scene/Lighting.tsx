'use client';

import { Environment, Lightformer } from '@react-three/drei';

// Poly Haven "autoshop_01" (CC0): the garage scene. See public/hdri/README.md for the other scenes.
const lowRes = typeof window !== 'undefined' && (window.devicePixelRatio < 1.5 && window.innerWidth < 900);
export const GARAGE_HDRI = lowRes ? '/hdri/autoshop_01_1k.hdr' : '/hdri/autoshop_01_2k.hdr';

/**
 * Garage lighting, HDRI driven.
 * The first Environment only draws the backdrop: the HDRI projected onto a dome with a flat
 * floor, so the car stands inside the workshop. The second one lights and reflects: the same
 * HDRI plus softbox Lightformers rendered into one cube map, so the white paint picks up crisp
 * studio highlights on top of the room.
 */
export default function Lighting() {
  return (
    <>
      <Environment files={GARAGE_HDRI} background="only" ground={{ height: 1.7, radius: 42, scale: 100 }} />
      <Environment files={GARAGE_HDRI} resolution={512} environmentIntensity={1}>
        {/* softbox strips along the car, overhead */}
        {[-2.4, 0, 2.4].map((x) => (
          <Lightformer key={x} form="rect" intensity={1.6} position={[x, 5.5, 0]} rotation={[Math.PI / 2, 0, 0]} scale={[1.1, 11, 1]} />
        ))}
        {/* warm key softbox from the front left (behind the hero camera), cool rim high at the rear right */}
        <Lightformer form="rect" intensity={2.4} color="#fff4e8" position={[6.5, 2.2, 6.5]} scale={[6, 3, 1]} target={[0, 0.9, 0]} />
        <Lightformer form="rect" intensity={1.4} color="#dfe8ff" position={[-6, 7, -6]} scale={[5, 2.5, 1]} target={[0, 0.8, 0]} />
      </Environment>
    </>
  );
}
