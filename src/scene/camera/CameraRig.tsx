'use client';

import { useEffect, useRef } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import gsap from 'gsap';
import { Box3, MathUtils, PerspectiveCamera, Spherical, Vector3 } from 'three';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import { carLift } from '../liftState';
import { useGarage, type CamRequest, type Seat } from '../store';
import { SEATS, SHOTS, UNDER_GROUND, UNDER_LIFTED, type Shot } from './presets';

/**
 * Camera choreography (M4): presets, Get In and Get Out, the underside on the lift.
 *
 * Moves between exterior shots travel on a sphere around the car (radius, height angle and
 * bearing interpolated separately), so a Front to Rear move swings around the car instead of
 * cutting through it. Entering and leaving the cabin goes through the open door: fly to just
 * outside it, dolly in to the seat, close the door behind. While a move runs the orbit controls
 * are off and the rig drives the camera directly; afterwards the controls get the limits of the
 * new view (outside: orbit and zoom with a floor; inside: look around from a fixed head).
 */

const FLOOR = 0.15; // the camera never goes lower than this outside
const CENTER = new Vector3(0, 0.9, 0);
const CABIN_LOOK = 0.05; // in the cabin the controls orbit a point this far ahead of the eye

type Controls = OrbitControlsImpl & { enabled: boolean };

export default function CameraRig() {
  const camera = useThree((s) => s.camera) as PerspectiveCamera;
  const controls = useThree((s) => s.controls) as Controls | null;
  const request = useGarage((s) => s.camRequest);
  const queue = useRef<Promise<void>>(Promise.resolve());
  const handled = useRef(0);

  // limits for the view we start in
  useEffect(() => {
    if (controls) configure(controls, useGarage.getState().view);
  }, [controls]);

  useEffect(() => {
    if (!controls || !request || request.id === handled.current) return;
    handled.current = request.id;
    queue.current = queue.current.then(() => run(request, camera, controls)).catch((e) => console.error('[garage] camera move failed', e));
  }, [request, camera, controls]);

  // outside, the lowest polar angle allowed keeps the camera above the floor at any distance
  useFrame(() => {
    if (controls && useGarage.getState().view === 'exterior') keepAboveFloor(controls, camera);
  });

  return null;
}

function keepAboveFloor(c: Controls, camera: PerspectiveCamera) {
  const t = c.target;
  const d = camera.position.distanceTo(t);
  const limit = Math.acos(MathUtils.clamp((FLOOR - t.y) / Math.max(d, 1e-3), -1, 1));
  c.maxPolarAngle = Math.min(Math.PI - 0.05, limit);
}

function configure(c: Controls, view: 'exterior' | 'cabin') {
  if (view === 'exterior') {
    c.enableZoom = true;
    c.minDistance = 0.6;
    c.maxDistance = 32;
    c.rotateSpeed = 1;
    c.minPolarAngle = 0;
  } else {
    // look around from a fixed head: orbit a point just ahead, dragging grabs the world
    c.enableZoom = false;
    c.minDistance = c.maxDistance = CABIN_LOOK;
    c.rotateSpeed = -0.35;
    c.minPolarAngle = Math.PI * 0.17;
    c.maxPolarAngle = Math.PI * 0.62;
  }
}

async function run(r: CamRequest, camera: PerspectiveCamera, controls: Controls) {
  const s = useGarage.getState();
  useGarage.setState({ camBusy: true });
  try {
    if (r.action === 'getIn') {
      if (s.view === 'cabin') await leaveCabin(camera, controls, false);
      await enterCabin(r.seat, camera, controls);
    } else if (r.action === 'getOut') {
      if (s.view === 'cabin') await leaveCabin(camera, controls, true);
    } else if (r.action === 'frame') {
      if (s.view === 'cabin') await leaveCabin(camera, controls, false);
      await frameBox(new Box3(new Vector3(...r.min), new Vector3(...r.max)), camera, controls);
    } else if (r.preset === 'interior') {
      if (s.view === 'cabin' && s.seat === 'rear') return;
      if (s.view === 'cabin') await leaveCabin(camera, controls, false);
      await enterCabin('rear', camera, controls);
    } else {
      if (s.view === 'cabin') await leaveCabin(camera, controls, false);
      const g = useGarage.getState();
      if (r.preset === 'engine') g.setPartOpen('BODY_5353_hood', true);
      if (r.preset === 'underside') {
        if (g.scene === 'garage') {
          g.setLift(true);
          await orbitTo(UNDER_LIFTED, camera, controls, 3.4);
        } else {
          await orbitTo(UNDER_GROUND, camera, controls, 1.6);
        }
        return;
      }
      if (r.preset === 'hero' && g.lift) g.setLift(false);
      await orbitTo(lifted(SHOTS[r.preset], r.preset === 'hero' ? 0 : carLift.y), camera, controls, 1.6);
    }
  } finally {
    useGarage.setState({ camBusy: false });
  }
}

/**
 * Fit a box in view from the current direction: the target moves to the box centre and the
 * camera backs off until the box's corners fit the view with a margin, projected on the real
 * screen axes (a bounding sphere would leave a long car small in frame). The subject sits a
 * little above centre, clear of the instrument cluster. Used by the explode stages and the zoom
 * to a part.
 */
function frameBox(box: Box3, camera: PerspectiveCamera, controls: Controls) {
  const center = box.getCenter(new Vector3());
  const dir = camera.position.clone().sub(controls.target);
  if (dir.lengthSq() < 1e-6) dir.set(1, 0.4, 1);
  dir.normalize();
  // never frame from below the floor line, and keep a little height so the floor reads
  dir.y = Math.max(dir.y, 0.18);
  dir.normalize();
  const forward = dir.clone().negate();
  const right = new Vector3().crossVectors(forward, new Vector3(0, 1, 0)).normalize();
  const up = new Vector3().crossVectors(right, forward);
  let halfW = 0;
  let halfH = 0;
  let halfD = 0;
  const corner = new Vector3();
  for (let i = 0; i < 8; i++) {
    corner.set(i & 1 ? box.max.x : box.min.x, i & 2 ? box.max.y : box.min.y, i & 4 ? box.max.z : box.min.z).sub(center);
    halfW = Math.max(halfW, Math.abs(corner.dot(right)));
    halfH = Math.max(halfH, Math.abs(corner.dot(up)));
    halfD = Math.max(halfD, Math.abs(corner.dot(forward)));
  }
  const vHalf = MathUtils.degToRad(camera.fov) / 2;
  const hHalf = Math.atan(Math.tan(vHalf) * camera.aspect);
  const margin = 1.12;
  const dist = MathUtils.clamp(Math.max((halfW * margin) / Math.tan(hHalf), (halfH * margin) / Math.tan(vHalf)) + halfD, 0.8, 40);
  // lift the subject by 9 percent of the frame, so the dash at the bottom does not cover it
  const lift = up.clone().multiplyScalar(-0.09 * 2 * dist * Math.tan(vHalf));
  const target = center.clone().add(lift);
  const position = target.clone().addScaledVector(dir, dist);
  position.y = Math.max(position.y, FLOOR + 0.2);
  return dolly({ position: position.toArray() as [number, number, number], target: target.toArray() as [number, number, number], fov: camera.fov }, camera, controls, 1.15).then(() =>
    finish(controls, 'exterior', null),
  );
}

/** A shot raised with the car on the lift. */
function lifted(shot: Shot, y: number): Shot {
  return { ...shot, position: [shot.position[0], shot.position[1] + y, shot.position[2]], target: [shot.target[0], shot.target[1] + y, shot.target[2]] };
}

/** Exterior move around the car on a sphere centred on it. */
function orbitTo(shot: Shot, camera: PerspectiveCamera, controls: Controls, duration: number) {
  controls.enabled = false;
  const center = CENTER.clone().setY(CENTER.y + carLift.y);
  const from = new Spherical().setFromVector3(camera.position.clone().sub(center));
  const to = new Spherical().setFromVector3(new Vector3(...shot.position).sub(center));
  // shortest way round
  let dTheta = to.theta - from.theta;
  dTheta = Math.atan2(Math.sin(dTheta), Math.cos(dTheta));
  const t0 = controls.target.clone();
  const t1 = new Vector3(...shot.target);
  const f0 = camera.fov;
  const sph = new Spherical();
  const p = { k: 0 };
  return tween(p, duration, 'power2.inOut', () => {
    const k = p.k;
    sph.set(MathUtils.lerp(from.radius, to.radius, k), MathUtils.lerp(from.phi, to.phi, k), from.theta + dTheta * k);
    camera.position.setFromSpherical(sph).add(center);
    controls.target.lerpVectors(t0, t1, k);
    setFov(camera, MathUtils.lerp(f0, shot.fov, k));
    camera.lookAt(controls.target);
  }).then(() => finish(controls, 'exterior', null));
}

/** Straight move with eased look, used for the door and seat legs. */
function dolly(to: Shot, camera: PerspectiveCamera, controls: Controls, duration: number, ease = 'power2.inOut') {
  controls.enabled = false;
  const p0 = camera.position.clone();
  const p1 = new Vector3(...to.position);
  const t0 = controls.target.clone();
  const t1 = new Vector3(...to.target);
  const f0 = camera.fov;
  const p = { k: 0 };
  return tween(p, duration, ease, () => {
    camera.position.lerpVectors(p0, p1, p.k);
    controls.target.lerpVectors(t0, t1, p.k);
    setFov(camera, MathUtils.lerp(f0, to.fov, p.k));
    camera.lookAt(controls.target);
  });
}

async function enterCabin(seat: Seat, camera: PerspectiveCamera, controls: Controls) {
  const g = useGarage.getState();
  if (g.lift) {
    g.setLift(false);
    await wait(2.9);
  }
  const s = SEATS[seat];
  useGarage.getState().setPartOpen(s.door, true);
  useGarage.getState().select(null);
  await orbitTo(s.approach, camera, controls, 1.3);
  await dolly({ position: s.eye, target: s.look, fov: s.fov }, camera, controls, 1.8, 'power3.inOut');
  // settle: a small head drop into the seat
  await dolly({ position: [s.eye[0], s.eye[1] - 0.025, s.eye[2]], target: s.look, fov: s.fov }, camera, controls, 0.45, 'sine.out');
  useGarage.getState().setPartOpen(s.door, false);
  const eye = camera.position.clone();
  const dir = new Vector3(...s.look).sub(eye).normalize();
  controls.target.copy(eye).addScaledVector(dir, CABIN_LOOK);
  useGarage.setState({ view: 'cabin', seat });
  finish(controls, 'cabin', seat);
}

async function leaveCabin(camera: PerspectiveCamera, controls: Controls, toHero: boolean) {
  const g = useGarage.getState();
  const seat = g.seat ?? 'driver';
  const s = SEATS[seat];
  g.setPartOpen(s.door, true);
  // look toward the door, then back out through it
  const far = new Vector3(...s.look);
  controls.target.copy(far);
  await dolly({ position: s.eye, target: [3, 1.35, (s.eye[2] + 0.25) as number], fov: 50 }, camera, controls, 0.7, 'sine.inOut');
  useGarage.setState({ view: 'exterior', seat: null });
  await dolly(s.approach, camera, controls, 1.3, 'power2.inOut');
  useGarage.getState().setPartOpen(s.door, false);
  if (toHero) await orbitTo(SHOTS.hero, camera, controls, 1.5);
  else finish(controls, 'exterior', null);
}

function finish(controls: Controls, view: 'exterior' | 'cabin', seat: Seat | null) {
  useGarage.setState({ view, seat });
  configure(controls, view);
  controls.enabled = true;
  controls.update();
}

function setFov(camera: PerspectiveCamera, fov: number) {
  camera.fov = fov;
  camera.updateProjectionMatrix();
}

function tween(obj: { k: number }, duration: number, ease: string, onUpdate: () => void) {
  return new Promise<void>((resolve) => {
    gsap.to(obj, { k: 1, duration, ease, onUpdate, onComplete: resolve });
  });
}

function wait(seconds: number) {
  return new Promise<void>((resolve) => gsap.delayedCall(seconds, resolve));
}
