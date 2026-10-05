'use client';

import { useEffect, useMemo, useRef } from 'react';
import { Euler, Group, Quaternion, Vector3, type Object3D, type SpotLight } from 'three';
import { useFrame, type ThreeEvent } from '@react-three/fiber';
import { Bvh, useGLTF } from '@react-three/drei';
import gsap from 'gsap';
import { engineAudio } from '@/engine/audio';
import { engine, kickBody, setGear } from '@/engine/sim';
import { carLift } from '../liftState';
import { childrenOf } from '../explode/rig';
import { explodeRig, frameParts } from '../explode/Explode';
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
  // body parts go into a sprung group that can roll on its suspension; wheels stay planted
  const rig = useMemo(() => sprungRig(scene), [scene]);
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
      // opening swings out and settles against the check with a small bounce; closing
      // accelerates home and lands with a thud the body absorbs
      gsap.to(r, {
        t: target,
        duration: target ? 1.0 : 0.7,
        ease: target ? 'back.out(1.25)' : 'power2.in',
        delay: i * 0.1,
        overwrite: true,
        onUpdate: () => poseHinges([r]),
        onComplete: () => {
          if (target) return;
          engineAudio.click(0.45);
          kickBody(0.025, r.key.endsWith('_L') ? 0.02 : r.key.endsWith('_R') ? -0.02 : 0);
        },
      });
    });
  }, [open, rigs]);
  useEffect(() => () => gsap.killTweensOf(rigs), [rigs]);

  // the car rides the lift
  const body = useRef<Group>(null);
  useFrame((_, dt) => {
    if (body.current) body.current.position.y = carLift.y;
    // engine torque reaction and idle rock, about a roll centre above the axles
    q.setFromEuler(euler.set(engine.pitch, 0, engine.roll));
    rig.sprung.quaternion.copy(q);
    rig.sprung.position.copy(PIVOT).sub(tmp.copy(PIVOT).applyQuaternion(q));
    // first gear when the car is up on the lift, so revving turns the wheels
    const gear = carLift.y > 1 ? '1' : 'N';
    if (engine.gear !== gear) setGear(gear);
    const spin = (engine.wheelRpm / 60) * Math.PI * 2 * Math.min(dt, 0.05);
    if (spin) for (const w of rig.wheels) w.rotateX(spin);
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

const PIVOT = new Vector3(0, 0.55, 0);
const q = new Quaternion();
const euler = new Euler();
const tmp = new Vector3();

/** Moves every top level node except the wheels into one group, once per loaded scene. */
function sprungRig(scene: Object3D) {
  let sprung = scene.getObjectByName('__sprung') as Group | undefined;
  if (!sprung) {
    sprung = new Group();
    sprung.name = '__sprung';
    for (const child of [...scene.children]) {
      const key = child.userData.name;
      if (typeof key === 'string' && key.startsWith('WHEEL_')) continue;
      sprung.add(child);
    }
    scene.add(sprung);
  }
  const wheels = scene.children.filter((c) => typeof c.userData.name === 'string' && c.userData.name.startsWith('WHEEL_'));
  return { sprung, wheels };
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
  // exploded: a click drills in (system, then assembly) or zooms to the part
  if (s.explode.level > 0) {
    const x = s.explode;
    const system = key.split('_')[0];
    const hasChildren = childrenOf(explodeRig.current, key).length > 0;
    s.select(key);
    if (x.level === 1 || x.system !== system) s.focusSystem(system);
    else if (hasChildren && x.assembly !== key) s.focusAssembly(key);
    else if (!s.camBusy) frameParts([key]);
    return;
  }
  // the driver's seat is the way in
  if (key === 'INT_7151_front_seat_L' && s.view === 'exterior' && !s.camBusy) {
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
