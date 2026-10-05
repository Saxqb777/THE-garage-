'use client';

import { Suspense, useEffect, useMemo } from 'react';
import { Environment, Lightformer, useEnvironment } from '@react-three/drei';
import { Color, Euler, Vector3 } from 'three';
import { SCENES, hdriUrl, timeOfDayLook, worldSun, type SceneDef } from './scenes';
import SkyDome from './SkyDome';
import { useGarage } from './store';

/**
 * Scene lighting, HDRI driven and data driven (see scenes.ts).
 * SkyDome draws the backdrop: the HDRI projected onto a dome with a flat floor at y = 0, so the
 * car stands on the photo's ground. An Environment lights and reflects; in the garage it also
 * carries softbox Lightformers for crisp studio highlights on the paint. Outdoor scenes add a
 * directional sun placed where the HDRI's sun is, which gives real cast shadows on the car.
 */
export default function Lighting() {
  const key = useGarage((s) => s.scene);
  const tod = useGarage((s) => s.timeOfDay);
  const scene = SCENES[key];
  const look = timeOfDayLook(scene, tod);
  const rotation = useMemo(() => new Euler(0, scene.yaw, 0), [scene.yaw]);

  return (
    <>
      <Suspense fallback={null}>
        <SkyDome
          file={hdriUrl(scene)}
          height={scene.ground.height}
          radius={scene.ground.radius}
          offset={scene.ground.offset}
          yaw={scene.yaw}
          intensity={scene.backgroundIntensity * look.exposure}
        />
        {scene.lightformers ? (
          <Environment files={hdriUrl(scene)} resolution={512} environmentIntensity={scene.envIntensity * look.exposure} environmentRotation={rotation}>
            {/* softbox strips along the car, overhead */}
            {[-2.4, 0, 2.4].map((x) => (
              <Lightformer key={x} form="rect" intensity={1.6} position={[x, 5.5, 0]} rotation={[Math.PI / 2, 0, 0]} scale={[1.1, 11, 1]} />
            ))}
            {/* warm key softbox from the front left (behind the hero camera), cool rim high at the rear right */}
            <Lightformer form="rect" intensity={2.4} color="#fff4e8" position={[6.5, 2.2, 6.5]} scale={[6, 3, 1]} target={[0, 0.9, 0]} />
            <Lightformer form="rect" intensity={1.4} color="#dfe8ff" position={[-6, 7, -6]} scale={[5, 2.5, 1]} target={[0, 0.8, 0]} />
          </Environment>
        ) : (
          <Environment files={hdriUrl(scene)} environmentIntensity={scene.envIntensity * look.exposure} environmentRotation={rotation} />
        )}
      </Suspense>
      {scene.sun && <Sun scene={scene} elevationScale={look.sunElevationScale} intensityScale={look.sunIntensityScale} warmth={look.warmth} />}
      {scene.night && <hemisphereLight args={['#5a6a8a', '#101014', 0.25]} />}
    </>
  );
}

/** Where the sun sits after the time of day slider lowers it: same azimuth, scaled elevation. */
export function sunPosition(scene: SceneDef, elevationScale: number, distance = 14): [number, number, number] {
  const [x, y, z] = worldSun(scene) ?? [0, 1, 0];
  const az = Math.atan2(z, x);
  const el = Math.max(0.06, Math.asin(y) * elevationScale);
  return [Math.cos(el) * Math.cos(az) * distance, Math.sin(el) * distance, Math.cos(el) * Math.sin(az) * distance];
}

function Sun({ scene, elevationScale, intensityScale, warmth }: { scene: SceneDef; elevationScale: number; intensityScale: number; warmth: number }) {
  const position = useMemo(() => sunPosition(scene, elevationScale), [scene, elevationScale]);
  const color = useMemo(() => new Color(scene.sunColor).lerp(new Color('#ff8f3a'), warmth), [scene.sunColor, warmth]);
  const target = useMemo(() => new Vector3(0, 0.6, 0), []);
  return (
    <directionalLight
      position={position}
      color={color}
      intensity={scene.sunIntensity * intensityScale}
      castShadow
      shadow-mapSize={[2048, 2048]}
      shadow-bias={-0.0004}
      shadow-normalBias={0.02}
      shadow-camera-near={1}
      shadow-camera-far={40}
      shadow-camera-left={-5}
      shadow-camera-right={5}
      shadow-camera-top={5}
      shadow-camera-bottom={-5}
      shadow-radius={2 + scene.sunSoftness * 6}
      target-position={target}
    />
  );
}

/**
 * Scene switches wait for the new sky: the requested scene's HDRI loads in a hidden Suspense
 * boundary, and only then becomes the scene on screen, so a switch never flashes an unlit car.
 */
export function SceneSwap() {
  const target = useGarage((s) => s.targetScene);
  const current = useGarage((s) => s.scene);
  if (target === current) return null;
  return (
    <Suspense fallback={null}>
      <SkyReady key={target} file={hdriUrl(SCENES[target])} onReady={() => useGarage.getState().commitScene(target)} />
    </Suspense>
  );
}

function SkyReady({ file, onReady }: { file: string; onReady: () => void }) {
  useEnvironment({ files: file });
  useEffect(() => onReady(), [onReady]);
  return null;
}
