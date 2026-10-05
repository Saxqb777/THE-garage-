'use client';

import { Component, Suspense, useEffect, useMemo, type ReactNode } from 'react';
import { Canvas, addAfterEffect, addEffect, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Bloom, EffectComposer, Outline, SMAA, ToneMapping, Vignette } from '@react-three/postprocessing';
import { ToneMappingMode } from 'postprocessing';
import { NoToneMapping, SRGBColorSpace } from 'three';
import CarModel from './car/CarModel';
import { meshesOf } from './car/parts';
import { dueAt } from '@/data/catalog';
import CameraRig from './camera/CameraRig';
import Explode from './explode/Explode';
import Ground from './Ground';
import Hotspots from './Hotspots';
import Lift from './Lift';
import Lighting, { SceneSwap } from './Lighting';
import { SCENES, timeOfDayLook } from './scenes';
import { useGarage } from './store';
import { WarmthEffect } from './Warmth';

// Hero 3/4 front view from the front left (the car faces +Z, its left side is +X).
// ?cam=x,y,z&look=x,y,z&fov=35 override it, which the photo comparison shots use.
const query = new URLSearchParams(typeof window === 'undefined' ? '' : window.location.search);
const vec3 = (key: string, fallback: [number, number, number]): [number, number, number] => {
  const v = query.get(key)?.split(',').map(Number);
  return v && v.length === 3 && v.every(Number.isFinite) ? [v[0], v[1], v[2]] : fallback;
};
const CAMERA_POSITION = vec3('cam', [5.5, 1.6, 6.0]);
const CAMERA_TARGET = vec3('look', [0, 0.8, 0.2]);
const CAMERA_FOV = Number(query.get('fov')) || 35;

let downAt: [number, number] = [0, 0];

export default function Experience() {
  const url = useGarage((s) => s.modelUrl);
  return (
    <Canvas
      onPointerDown={(e) => {
        downAt = [e.clientX, e.clientY];
      }}
      onPointerMissed={(e) => {
        // a click on empty space closes the part card; the end of an orbit drag does not
        const moved = Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]);
        if (e.type === 'click' && moved < 6) useGarage.getState().select(null);
      }}
      shadows
      dpr={[1, 2]}
      camera={{ fov: CAMERA_FOV, near: 0.1, far: 100, position: CAMERA_POSITION }}
      gl={{ antialias: false, toneMapping: NoToneMapping, outputColorSpace: SRGBColorSpace }}
    >
      <Lighting />
      <SceneSwap />
      <Ground />
      <ModelBoundary url={url}>
        <Suspense fallback={null}>
          <CarModel url={url} />
        </Suspense>
      </ModelBoundary>
      <OrbitControls makeDefault target={CAMERA_TARGET} enablePan={false} enableDamping dampingFactor={0.08} />
      <CameraRig />
      <Explode />
      <Lift />
      <Hotspots />
      <PostFX />
      <RenderStats />
      {query.has('debug') && <DevHandle />}
    </Canvas>
  );
}

/** ACES in the composer (the canvas renders linear), a whisper of bloom on the highlights, SMAA, soft vignette. */
function PostFX() {
  const key = useGarage((s) => s.scene);
  const scene = SCENES[key];
  const warmth = useMemo(
    () =>
      new WarmthEffect(() => {
        const s = useGarage.getState();
        return timeOfDayLook(SCENES[s.scene], s.timeOfDay).warmth;
      }),
    [],
  );
  return (
    <EffectComposer multisampling={0} autoClear={false}>
      <Bloom mipmapBlur intensity={scene.bloom.intensity} luminanceThreshold={scene.bloom.threshold} luminanceSmoothing={0.2} />
      <primitive object={warmth} />
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      <Vignette eskil={false} offset={0.25} darkness={0.55} />
      <PartOutline />
      <SMAA />
    </EffectComposer>
  );
}

/** Gold outline on the part under the pointer and on the part whose card is open. */
function PartOutline() {
  const hovered = useGarage((s) => s.hovered);
  const selected = useGarage((s) => s.selected);
  const loaded = useGarage((s) => s.model !== null);
  const service = useGarage((s) => s.service);
  const catalog = useGarage((s) => s.catalog);
  const selection = useMemo(() => {
    if (!loaded) return [];
    const keys = new Set([hovered, selected].filter((k): k is string => !!k));
    if (service && catalog) for (const p of dueAt([...catalog.values()], service)) if (p.meshPresent) keys.add(p.key);
    return [...keys].flatMap(meshesOf);
  }, [hovered, selected, loaded, service, catalog]);
  return (
    <Outline
      selection={selection}
      visibleEdgeColor={0xf2c36b}
      hiddenEdgeColor={0x6b5530}
      edgeStrength={3.5}
      blur
      xRay
    />
  );
}

/** gl.info is reset once per frame here (not per render call), so the composer passes add up. */
function RenderStats() {
  const gl = useThree((s) => s.gl);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/immutability -- renderer stats flag, not React state
    gl.info.autoReset = false;
    const stop = addEffect(() => gl.info.reset());
    return () => {
      stop();
      gl.info.autoReset = true;
    };
  }, [gl]);
  useEffect(
    () =>
      addAfterEffect(() => {
        const { calls, triangles } = gl.info.render;
        const s = useGarage.getState();
        const loaded = s.model !== null;
        if (calls !== s.drawCalls || triangles !== s.triangles || loaded !== s.loaded) {
          useGarage.setState({ drawCalls: calls, triangles, loaded });
        }
      }),
    [gl],
  );
  return null;
}

/** ?debug exposes the R3F state as window.__r3f for scripted inspection. */
function DevHandle() {
  const state = useThree();
  useEffect(() => {
    (window as unknown as { __r3f?: unknown }).__r3f = state;
  }, [state]);
  return null;
}

/** A missing or broken GLB shows up in the HUD instead of taking the canvas down. */
class ModelBoundary extends Component<{ url: string; children: ReactNode }, { failed: boolean }> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error: Error) {
    useGarage.setState({ modelError: `Could not load ${this.props.url}: ${error.message}` });
  }

  render() {
    return this.state.failed ? null : this.props.children;
  }
}
