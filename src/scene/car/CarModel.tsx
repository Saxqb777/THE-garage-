'use client';

import { useEffect, useMemo } from 'react';
import { useGLTF } from '@react-three/drei';
import gsap from 'gsap';
import { useGarage } from '../store';
import { closeHinges, poseHinges, rigHinges } from './hinges';
import { enableShadows, inspectModel, logModel } from './parts';

// Self hosted decoder (copied from three/examples/jsm/libs/draco/gltf), no CDN.
const DRACO_PATH = '/draco/';

// Keep tweens on wall clock time even when frames are slow (software GL in screenshots),
// instead of GSAP's default of stretching long frames to 33 ms.
gsap.ticker.lagSmoothing(0);

export default function CarModel({ url }: { url: string }) {
  const { scene } = useGLTF(url, DRACO_PATH);
  const hingesOpen = useGarage((s) => s.hingesOpen);
  const info = useMemo(() => inspectModel(scene), [scene]);
  const rigs = useMemo(() => rigHinges(scene, info.parts.values()), [scene, info]);

  useEffect(() => {
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

  return <primitive object={scene} />;
}
