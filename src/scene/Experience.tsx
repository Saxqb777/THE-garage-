'use client';

import { Component, Suspense, useEffect, type ReactNode } from 'react';
import { Canvas, addAfterEffect, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { ACESFilmicToneMapping, SRGBColorSpace } from 'three';
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
      gl={{ antialias: true, toneMapping: ACESFilmicToneMapping, outputColorSpace: SRGBColorSpace }}
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
      <RenderStats />
    </Canvas>
  );
}

/** gl.info resets on every render call, so after the frame it holds the main pass. */
function RenderStats() {
  const gl = useThree((s) => s.gl);
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
