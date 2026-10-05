'use client';

import { useEffect, useMemo, useRef } from 'react';
import type { Group, Object3D, SpotLight } from 'three';
import { useFrame, type ThreeEvent } from '@react-three/fiber';
import { Bvh, useGLTF } from '@react-three/drei';
import gsap from 'gsap';
import { carLift } from '../liftState';
import { useGarage } from '../store';
import { closeHinges, poseHinges, rigHinges, type HingeRig } from './hinges';
import { applyLook, applyModes } from './look';
import { CONTRACT_PARTS, enableShadows, inspectModel, logModel, partKeyOf, partNodes } from './parts';

// Self hosted decoder (copied from three/examples/jsm/libs/draco/gltf), no CDN.
const DRACO_PATH = '/draco/';

// Keep tweens on wall clock time even when frames are slow (software GL in screenshots),
// instead of GSAP's default of stretching long frames to 33 ms.
gsap.ticker.lagSmoothing(0);

export default function CarModel({ url }: { url: string }) {
  const { scene } = useGLTF(url, DRACO_PATH);
  const open = useGarage((s) => s.open);
  const lightsOn = useGarage((s) => s.lightsOn);
  const xray = useGarage((s) => s.xray);
  const info = useMemo(() => inspectModel(scene), [scene]);
  const rigs = useMemo(() => rigHinges(scene, info.parts.values()), [scene, info]);

  useEffect(() => {
    applyLook(scene);
    enableShadows(scene);
    logModel(url, scene, info);
    partNodes.clear();
    for (const [key, part] of info.parts) partNodes.set(key, part.object);
    useGarage.getState().setHingeKeys(rigs.map((r) => r.key));
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
    return () => {
      partNodes.clear();
      useGarage.setState({ model: null, loaded: false, hovered: null });
    };
  }, [scene, url, info, rigs]);

  useEffect(() => {
    applyModes(scene, { lightsOn, xray });
    return () => applyModes(scene, { lightsOn: false, xray: false });
  }, [scene, lightsOn, xray]);

  // Back to the rest pose when unmounted, since useGLTF hands the same scene to the next mount.
  useEffect(() => () => closeHinges(rigs), [rigs]);

  // Each hinged part tweens on its own; parts that change together (Open all) are staggered.
  const tweened = useRef(new Map<HingeRig, number>());
  useEffect(() => {
    const changed = rigs.filter((r) => (open[r.key] ? 1 : 0) !== tweened.current.get(r));
    const opening = changed.some((r) => open[r.key]);
    const order = opening ? changed : [...changed].reverse();
    order.forEach((r, i) => {
      const target = open[r.key] ? 1 : 0;
      tweened.current.set(r, target);
      gsap.to(r, {
        t: target,
        duration: 1.2,
        ease: 'power2.inOut',
        delay: i * 0.08,
        overwrite: true,
        onUpdate: () => poseHinges([r]),
      });
    });
  }, [open, rigs]);
  useEffect(() => () => gsap.killTweensOf(rigs), [rigs]);

  // the car rides the lift
  const body = useRef<Group>(null);
  useFrame(() => {
    if (body.current) body.current.position.y = carLift.y;
  });

  return (
    <group ref={body}>
      <Bvh firstHitOnly>
        <primitive object={scene} onPointerMove={onPointerMove} onPointerOut={onPointerOut} onClick={onClick} />
      </Bvh>
      {lightsOn && <Headlights />}
    </group>
  );
}

// Picking. Ghosted (X Ray) meshes let the event through to whatever is behind them, and a
// click that was really the end of an orbit drag is ignored.
function onPointerMove(e: ThreeEvent<PointerEvent>) {
  if (e.object.userData.ghost) return;
  e.stopPropagation();
  const key = partKeyOf(e.object);
  const s = useGarage.getState();
  if (key !== s.hovered) s.setHovered(key);
  document.body.style.cursor = key ? 'pointer' : '';
}

function onPointerOut(e: ThreeEvent<PointerEvent>) {
  const s = useGarage.getState();
  if (s.hovered && partKeyOf(e.object) === s.hovered) s.setHovered(null);
  document.body.style.cursor = '';
}

function onClick(e: ThreeEvent<MouseEvent>) {
  if (e.object.userData.ghost || e.delta > 6) return;
  e.stopPropagation();
  const key = partKeyOf(e.object);
  if (!key) return;
  const s = useGarage.getState();
  // the driver's seat is the way in
  if (key === 'INT_0000_front_seat_L' && s.view === 'exterior' && !s.camBusy) {
    s.requestCam({ action: 'getIn', seat: 'driver' });
    return;
  }
  s.select(key);
  if (CONTRACT_PARTS.get(key)?.hinge && !s.camBusy) s.togglePart(key);
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
