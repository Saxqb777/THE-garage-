'use client';

import { useMemo } from 'react';
import { ContactShadows } from '@react-three/drei';
import { CanvasTexture, NoColorSpace, RepeatWrapping, SRGBColorSpace, type ColorSpace } from 'three';

const SIZE = 512;
const SLAB_METRES = 4; // one texture tile; its edges are the expansion joints
const RADIUS = 40;

/**
 * Seeded blotch and speckle noise with joints along two edges, so the tiling seams hide in
 * the joints. Same noise every call; the joint shade differs between colour and roughness.
 */
function drawConcrete(joint: string) {
  let seed = 1337;
  const rand = () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = SIZE;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = 'rgb(140,140,140)';
  ctx.fillRect(0, 0, SIZE, SIZE);
  for (let i = 0; i < 500; i++) {
    const v = Math.round(110 + rand() * 60);
    ctx.fillStyle = `rgba(${v},${v},${v},0.07)`;
    ctx.beginPath();
    ctx.arc(rand() * SIZE, rand() * SIZE, 6 + rand() * 70, 0, Math.PI * 2);
    ctx.fill();
  }
  const img = ctx.getImageData(0, 0, SIZE, SIZE);
  for (let i = 0; i < img.data.length; i += 4) {
    const n = (rand() - 0.5) * 26;
    img.data[i] += n;
    img.data[i + 1] += n;
    img.data[i + 2] += n;
  }
  ctx.putImageData(img, 0, 0);
  ctx.fillStyle = joint;
  ctx.fillRect(0, 0, SIZE, 3);
  ctx.fillRect(0, 0, 3, SIZE);
  return canvas;
}

function texture(canvas: HTMLCanvasElement, colorSpace: ColorSpace) {
  const tex = new CanvasTexture(canvas);
  tex.wrapS = tex.wrapT = RepeatWrapping;
  tex.repeat.setScalar((RADIUS * 2) / SLAB_METRES);
  tex.anisotropy = 8;
  tex.colorSpace = colorSpace;
  return tex;
}

/** Dark concrete floor with soft contact shadows under the car. */
export default function Ground() {
  const [map, roughnessMap] = useMemo(
    // dark joints in the colour, rough (light) joints in the roughness so they never turn glossy
    () => [texture(drawConcrete('rgba(20,20,20,0.85)'), SRGBColorSpace), texture(drawConcrete('rgb(235,235,235)'), NoColorSpace)],
    [],
  );
  return (
    <>
      <mesh rotation-x={-Math.PI / 2} receiveShadow>
        <circleGeometry args={[RADIUS, 96]} />
        <meshStandardMaterial
          color="#7d7f83"
          map={map}
          roughness={1.1} // times the map's ~0.55 grey: about 0.6, varying slab to slab
          roughnessMap={roughnessMap}
          metalness={0}
          envMapIntensity={0.9}
        />
      </mesh>
      <ContactShadows position={[0, 0.002, -0.1]} scale={[6, 8.5]} resolution={1024} blur={2.4} far={1.6} opacity={0.85} />
    </>
  );
}
