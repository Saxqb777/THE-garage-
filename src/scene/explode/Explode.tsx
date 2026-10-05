'use client';

import { useEffect, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import gsap from 'gsap';
import { engineAudio } from '@/engine/audio';
import { kickBody } from '@/engine/sim';
import { useGarage, type ExplodeState } from '../store';
import { apply, buildRig, focusKeys, predictedBox, targets, type Rig } from './rig';

/**
 * Drives the explode rig from the store (M6). Level 1 bursts outward system by system with a
 * stagger and an expo ease; assembling runs the same order backwards, accelerating home, and
 * lands with a snap: a click and a knock the suspension absorbs. Focus changes (levels 2 and 3)
 * are shorter moves. Each change also asks the camera to frame what the stage is about, using
 * the positions the parts will have, so the camera and the parts move together.
 *
 * A link that opens the car already apart (?x=...) applies the state without animation and
 * frames the selected part, or the stage, once the model is in.
 */

export const explodeRig: { current: Rig | null } = { current: null };

const STEP = 0.045; // seconds per stagger rank

export default function Explode() {
  const ready = useGarage((s) => s.model !== null);
  const x = useGarage((s) => s.explode);
  const first = useRef(true);
  const applied = useRef<ExplodeState | null>(null);

  useEffect(() => {
    if (!ready) {
      explodeRig.current = null;
      return;
    }
    explodeRig.current = buildRig();
    first.current = true;
    useGarage.setState((s) => ({ rigVersion: s.rigVersion + 1 }));
    return () => {
      const rig = explodeRig.current;
      if (rig) {
        gsap.killTweensOf(rig.entries.map((e) => e.p));
        for (const e of rig.entries) e.node.position.copy(e.rest);
      }
      explodeRig.current = null;
    };
  }, [ready]);

  useEffect(() => {
    const rig = explodeRig.current;
    if (!rig) return;
    const instant = first.current;
    first.current = false;
    const prev = applied.current;
    applied.current = x;
    if (instant && x.level === 0) return;
    animate(rig, x, prev, instant);
    frame(rig, x, instant);
  }, [x, ready]);

  useFrame(() => {
    if (explodeRig.current) apply(explodeRig.current);
  });

  return null;
}

function animate(rig: Rig, x: ExplodeState, prev: ExplodeState | null, instant: boolean) {
  const t = targets(rig, x);
  const ps = rig.entries.map((e) => e.p);
  gsap.killTweensOf(ps);
  if (instant) {
    for (const e of rig.entries) Object.assign(e.p, t.get(e));
    return;
  }
  const bursting = x.level >= 1 && (!prev || prev.level === 0);
  const assembling = x.level === 0 && prev && prev.level >= 1;
  let end = 0;
  for (const e of rig.entries) {
    const target = t.get(e)!;
    const changed = target.a !== e.p.a || target.b !== e.p.b || target.c !== e.p.c;
    if (!changed) continue;
    let delay = 0;
    let duration = 0.8;
    let ease = 'power2.inOut';
    if (bursting) {
      delay = e.rank * STEP;
      duration = 1.4;
      ease = 'expo.out';
    } else if (assembling) {
      delay = (rig.maxRank - e.rank) * STEP * 0.6;
      duration = 0.9;
      ease = 'power3.in';
    } else {
      delay = (e.parentKey ? 0.08 : 0) + (e.rank % 7) * 0.025;
    }
    end = Math.max(end, delay + duration);
    gsap.to(e.p, { a: target.a, b: target.b, c: target.c, delay, duration, ease, overwrite: true });
  }
  if (assembling) {
    gsap.delayedCall(end, () => {
      kickBody(0.11, 0.04);
      try {
        engineAudio.click(0.8);
      } catch {
        // no audio without a gesture; the knock still shows
      }
    });
  }
}

function frame(rig: Rig, x: ExplodeState, instant: boolean) {
  const s = useGarage.getState();
  const keys = instant && s.selected && rig.byKey.has(s.selected) ? [s.selected] : focusKeys(rig, x);
  const box = predictedBox(rig, x, keys);
  if (box.isEmpty()) return;
  s.requestCam({ action: 'frame', min: box.min.toArray() as [number, number, number], max: box.max.toArray() as [number, number, number] });
}

/** Zoom to one part where it is now (or will be): used when a leaf part is clicked while exploded. */
export function frameParts(keys: string[]) {
  const rig = explodeRig.current;
  if (!rig) return;
  const s = useGarage.getState();
  const box = predictedBox(rig, s.explode, keys);
  if (box.isEmpty()) return;
  s.requestCam({ action: 'frame', min: box.min.toArray() as [number, number, number], max: box.max.toArray() as [number, number, number] });
}
