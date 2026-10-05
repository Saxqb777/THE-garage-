'use client';

import { useEffect, useMemo, useRef } from 'react';
import type { Object3D, SpotLight } from 'three';
import { useGLTF } from '@react-three/drei';
import gsap from 'gsap';
import { useGarage } from '../store';
import { closeHinges, poseHinges, rigHinges } from './hinges';
import { applyLook, setLights } from './look';
import { enableShadows, inspectModel, logModel } from './parts';

// Self hosted decoder (copied from three/examples/jsm/libs/draco/gltf), no CDN.
const DRACO_PATH = '/draco/';

// Keep tweens on wall clock time even when frames are slow (software GL in screenshots),
// instead of GSAP's default of stretching long frames to 33 ms.
gsap.ticker.lagSmoothing(0);

export default function CarModel({ url }: { url: string }) {
  const { scene } = useGLTF(url, DRACO_PATH);
  const hingesOpen = useGarage((s) => s.hingesOpen);
  const lightsOn = useGarage((s) => s.lightsOn);
  const info = useMemo(() => inspectModel(scene), [scene]);
  const rigs = useMemo(() => rigHinges(scene, info.parts.values()), [scene, info]);

  useEffect(() => {
    applyLook(scene);
    enableShadows(scene);
    logModel(url, scene, info);
    useGarage.setState({
      modelError: null,
      model: {
        partKeys: [...info.parts.keys()],
        meshCount: info.meshCount,
        materials: info.materials,
        unknownKeys: info.unknownKeys,
        missingKeys: info.missingKeys,
      },
    });
    return () => useGarage.setState({ model: null, loaded: false });
  }, [scene, url, info]);

  useEffect(() => {
    setLights(scene, lightsOn);
    return () => setLights(scene, false);
  }, [scene, lightsOn]);

  // Back to the rest pose when unmounted, since useGLTF hands the same scene to the next mount.
  useEffect(() => () => closeHinges(rigs), [rigs]);

  useEffect(() => {
    if (!rigs.length) return;
    const tween = gsap.to(rigs, {
      t: hingesOpen ? 1 : 0,
      duration: 1.2,
      ease: 'power2.inOut',
      stagger: { each: 0.08, from: hingesOpen ? 'start' : 'end' },
      overwrite: true,
      onUpdate: () => poseHinges(rigs),
    });
    return () => {
      tween.kill();
    };
  }, [hingesOpen, rigs]);

  return (
    <>
      <primitive object={scene} />
      {lightsOn && <Headlights />}
    </>
  );
}

// Low beams: two spots from the lamp centres (three.js space, car faces +Z), aimed down the road.
const LAMPS: [number, number, number][] = [
  [0.72, 0.94, 2.28],
  [-0.72, 0.94, 2.28],
];

function Headlights() {
  return (
    <>
      {LAMPS.map((p) => (
        <Beam key={p[0]} position={p} />
      ))}
    </>
  );
}

function Beam({ position }: { position: [number, number, number] }) {
  const light = useRef<SpotLight>(null);
  const target = useRef<Object3D>(null);
  useEffect(() => {
    if (light.current && target.current) light.current.target = target.current;
  }, []);
  return (
    <>
      <spotLight ref={light} position={position} color="#fff2d2" intensity={160} angle={0.55} penumbra={0.6} distance={40} decay={2} />
      <object3D ref={target} position={[position[0] * 1.4, 0, 12]} />
    </>
  );
}
