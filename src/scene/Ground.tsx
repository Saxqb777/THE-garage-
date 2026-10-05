'use client';

import { useTexture, MeshReflectorMaterial } from '@react-three/drei';
import { NoColorSpace } from 'three';
import shadow from '@/data/groundShadow.json';
import { SCENES } from './scenes';
import { useGarage } from './store';

/**
 * What the car stands on. The floor itself is the HDRI's ground (SkyDome) except on the
 * corniche, where a wet road mirrors the city. Two shadows sit on it:
 *  - the parked shadow, baked once in Blender (blender/bake_ground_shadow.py): soft occlusion
 *    from the whole sky plus an overhead softbox, the thing that plants the tires on the floor;
 *  - the sun's hard shadow, live from the directional light, so it follows the time of day.
 *
 * drei's AccumulativeShadows was the first plan for the parked shadow, but with three 0.186
 * its light map pass receives no occlusion at all (see docs/decisions.md), and it would cost
 * dozens of frames on every scene switch anyway; the bake is free at runtime.
 */
export default function Ground() {
  const key = useGarage((s) => s.scene);
  const scene = SCENES[key];
  return (
    <>
      {scene.floor === 'wet' && <WetRoad />}
      <ParkedShadow color={scene.shadowColor} opacity={scene.aoOpacity} />
      {scene.sun && (
        <mesh rotation-x={-Math.PI / 2} position-y={0.003} receiveShadow renderOrder={2}>
          <planeGeometry args={[30, 30]} />
          <shadowMaterial color={scene.shadowColor} opacity={scene.sunShadowOpacity} transparent depthWrite={false} />
        </mesh>
      )}
    </>
  );
}

function ParkedShadow({ color, opacity }: { color: string; opacity: number }) {
  const map = useTexture(shadow.texture, (t) => {
    t.colorSpace = NoColorSpace;
  });
  return (
    <mesh rotation-x={-Math.PI / 2} position={[shadow.center[0], 0.002, shadow.center[2]]} renderOrder={1}>
      <planeGeometry args={[shadow.size[0], shadow.size[1]]} />
      <meshBasicMaterial color={color} alphaMap={map} opacity={opacity} transparent depthWrite={false} toneMapped={false} />
    </mesh>
  );
}

/** Mirrors the skyline into a dark, slightly blurred wet asphalt. */
function WetRoad() {
  return (
    <mesh rotation-x={-Math.PI / 2} position-y={0.001}>
      <circleGeometry args={[45, 96]} />
      <MeshReflectorMaterial
        resolution={1024}
        blur={[500, 120]}
        mixBlur={1}
        mixStrength={3.5}
        mixContrast={1}
        depthScale={1}
        minDepthThreshold={0.4}
        maxDepthThreshold={1.4}
        roughness={0.8}
        metalness={0.2}
        color="#0d0f13"
        mirror={0.4}
      />
    </mesh>
  );
}
