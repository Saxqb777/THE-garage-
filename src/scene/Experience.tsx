'use client';

import { Component, Suspense, useEffect, type ReactNode } from 'react';
import { Canvas, addAfterEffect, addEffect, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Bloom, EffectComposer, SMAA, ToneMapping, Vignette } from '@react-three/postprocessing';
import { ToneMappingMode } from 'postprocessing';
import { NoToneMapping, SRGBColorSpace } from 'three';
import CarModel from './car/CarModel';
import Ground from './Ground';
import Lighting from './Lighting';
import { useGarage } from './store';

// Hero 3/4 front view from the front left (the car faces +Z, its left side is +X).
const CAMERA_POSITION: [number, number, number] = [5.5, 1.6, 6.0];
const CAMERA_TARGET: [number, number, number] = [0, 0.8, 0.2];

export default function Experience() {
  const url = useGarage((s) => s.modelUrl);
  return (
    <Canvas
      shadows
      dpr={[1, 2]}
      camera={{ fov: 35, near: 0.1, far: 100, position: CAMERA_POSITION }}
      gl={{ antialias: false, toneMapping: NoToneMapping, outputColorSpace: SRGBColorSpace }}
    >
      <Lighting />
      <Ground />
      <ModelBoundary url={url}>
        <Suspense fallback={null}>
          <CarModel url={url} />
        </Suspense>
      </ModelBoundary>
      <OrbitControls
        makeDefault
        target={CAMERA_TARGET}
        enablePan={false}
        enableDamping
        dampingFactor={0.08}
        minDistance={2.5}
        maxDistance={14}
        maxPolarAngle={Math.PI / 2 - 0.04}
      />
      <PostFX />
      <RenderStats />
    </Canvas>
  );
}

/** ACES in the composer (the canvas renders linear), a whisper of bloom on the highlights, SMAA, soft vignette. */
function PostFX() {
  return (
    <EffectComposer multisampling={0}>
      <Bloom mipmapBlur intensity={0.35} luminanceThreshold={1.0} luminanceSmoothing={0.2} />
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      <Vignette eskil={false} offset={0.25} darkness={0.55} />
      <SMAA />
    </EffectComposer>
  );
}

/** gl.info is reset once per frame here (not per render call), so the composer passes add up. */
function RenderStats() {
  const gl = useThree((s) => s.gl);
  useEffect(() => {
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
