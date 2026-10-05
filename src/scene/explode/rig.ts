import { Box3, Quaternion, Vector3, type Object3D } from 'three';
import { meshesOf, partKeyOf, partNodes } from '../car/parts';
import type { ExplodeState } from '../store';

/**
 * Explode geometry (M6). Every part gets one direction, fixed at load from where it sits on the
 * car, and moves along it by a distance that depends on the stage:
 *
 *   position = rest + dir * (d1 * p1 + d2 * p2 + d3 * p3)
 *
 *   p1  level 1, the systems separate: top level parts move out, and a child moves out of its
 *       parent only when it belongs to another system (glass out of a door, a lamp out of a
 *       fender), so a tire does not leave its rim yet
 *   p2  level 2, the focused system spreads: every member of that system moves further
 *   p3  level 3, the focused assembly spreads: its direct children move out
 *
 * Directions are world space vectors expressed in the node's parent frame, weighted per system
 * so the result reads as designed rather than radial: wheels go sideways, lamps and bumpers
 * along the car, doors sideways with a lift, glass and the interior up, the hood up and forward.
 * The body shell is the anchor and never moves.
 */

export const SYSTEM_ORDER = ['WHEEL', 'LIGHT', 'TRIM', 'ELEC', 'DOOR', 'GLASS', 'BODY', 'INT'];

type Weights = { x: number; y: number; z: number; lift: number };
const WEIGHTS: Record<string, Weights> = {
  WHEEL: { x: 1, y: 0, z: 0.15, lift: 0 },
  LIGHT: { x: 0.35, y: 0.1, z: 1, lift: 0.05 },
  TRIM: { x: 1, y: 0.2, z: 0.8, lift: 0.1 },
  ELEC: { x: 0.4, y: 0.6, z: 1, lift: 0.35 },
  DOOR: { x: 1, y: 0.15, z: 0.12, lift: 0.22 },
  GLASS: { x: 0.45, y: 1, z: 0.45, lift: 0.7 },
  BODY: { x: 1, y: 0.55, z: 1, lift: 0.12 },
  INT: { x: 0.6, y: 1, z: 0.45, lift: 0.75 },
};

/** Metres each top level part of a system moves at level 1. */
const D1: Record<string, number> = { WHEEL: 1.3, LIGHT: 0.9, TRIM: 0.55, ELEC: 0.55, DOOR: 1.25, GLASS: 0.9, BODY: 0.95, INT: 1.0 };
const D1_CHILD = 0.38; // a child of another system, out of its parent
const D2 = 0.85; // extra for members of the focused system
const D2_CHILD = 0.55;
const D3 = 0.5; // children of the focused assembly

export type Entry = {
  key: string;
  system: string;
  parentKey: string | null;
  node: Object3D;
  rest: Vector3;
  /** unit, in the parent's frame */
  dir: Vector3;
  /** unit, world */
  dirWorld: Vector3;
  d1: number;
  d2: number;
  d3: number;
  /** stagger rank at level 1 */
  rank: number;
  /** world box at rest, the part with its sub parts */
  box: Box3;
  /** world box at rest of the part's own meshes only */
  own: Box3;
  /** tween targets 0..1 */
  p: { a: number; b: number; c: number };
};

export type Rig = { entries: Entry[]; byKey: Map<string, Entry>; maxRank: number };

const CAR_CENTER = new Vector3(0, 0.9, 0);

export function buildRig(): Rig {
  const q = new Quaternion();
  const raw: { key: string; node: Object3D; parentKey: string | null; box: Box3; own: Box3; centroid: Vector3 }[] = [];
  for (const [key, node] of partNodes) {
    const box = new Box3().setFromObject(node, true);
    if (box.isEmpty()) continue;
    const own = new Box3();
    for (const m of meshesOf(key)) own.union(new Box3().setFromObject(m, true));
    raw.push({ key, node, parentKey: partKeyOf(node.parent), box, own: own.isEmpty() ? box.clone() : own, centroid: box.getCenter(new Vector3()) });
  }
  const byKeyRaw = new Map(raw.map((r) => [r.key, r]));
  // sub parts that sit on their parent (a rim in its tire, a blade on its arm) share one way
  // out: they fan along it at staggered distances instead of travelling as one lump
  const siblings = new Map<string, string[]>();
  for (const r of raw) if (r.parentKey) siblings.set(r.parentKey, [...(siblings.get(r.parentKey) ?? []), r.key].sort());

  const entries: Entry[] = raw.map((r) => {
    const system = r.key.split('_')[0];
    const w = WEIGHTS[system] ?? WEIGHTS.BODY;
    const parent = r.parentKey ? byKeyRaw.get(r.parentKey) : undefined;
    const ref = parent ? parent.centroid : CAR_CENTER;
    const v = r.centroid.clone().sub(ref);
    const weighted = (vec: Vector3, ww: Weights) => new Vector3(vec.x * ww.x, Math.max(0, vec.y) * ww.y, vec.z * ww.z);
    const isWheelChild = system === 'WHEEL' && !!parent;
    const degenerateOf = (k: string) => {
      const o = byKeyRaw.get(k)!;
      const op = o.parentKey ? byKeyRaw.get(o.parentKey) : undefined;
      if (!op) return false;
      return k.startsWith('WHEEL_') || weighted(o.centroid.clone().sub(op.centroid), WEIGHTS[k.split('_')[0]] ?? WEIGHTS.BODY).length() < 0.12;
    };
    const dirWorld = weighted(v, w);
    if (system === 'WHEEL') dirWorld.set(Math.sign(r.centroid.x) || 1, 0, 0.15 * Math.sign(r.centroid.z));
    // sub parts that share one way out fan along it at staggered distances (rim and tire)
    let fan = 1;
    if (parent && (isWheelChild || degenerateOf(r.key))) {
      const group = (siblings.get(parent.key) ?? [r.key]).filter(degenerateOf);
      const i = group.indexOf(r.key);
      if (group.length > 1 && i >= 0) fan = i / (group.length - 1);
    }
    if (dirWorld.length() < 0.12) {
      // sits on its reference (carpet, a blade on its arm): fall back to the system's natural way out
      if (system === 'WHEEL') dirWorld.set(Math.sign(r.centroid.x) || 1, 0, 0);
      else if (system === 'INT' || system === 'GLASS') dirWorld.set(0, 1, 0);
      else dirWorld.set(0, 0.4, Math.sign(r.centroid.z) || 1);
    }
    dirWorld.normalize();
    dirWorld.y += w.lift;
    dirWorld.normalize();
    // keep the mudguards and steps off the floor
    if (r.centroid.y < 0.45 && dirWorld.y < 0) dirWorld.y = 0;
    dirWorld.normalize();

    const dir = dirWorld.clone();
    if (r.node.parent) {
      r.node.parent.getWorldQuaternion(q);
      dir.applyQuaternion(q.invert());
    }
    const parentSystem = parent?.key.split('_')[0];
    const sameSystem = parentSystem === system;
    const isShell = r.key === 'BODY_0000_body_shell';
    const d1 = isShell ? 0 : parent ? (sameSystem ? 0 : D1_CHILD) : (D1[system] ?? 0.7) * (r.key === 'BODY_5301_hood' || /bumper/.test(r.key) ? 1.15 : 1);
    return {
      key: r.key,
      system,
      parentKey: r.parentKey,
      node: r.node,
      rest: r.node.position.clone(),
      dir,
      dirWorld,
      d1,
      // a sub part of the same system stays with its parent until that assembly is opened
      d2: isShell ? 0 : parent ? (sameSystem ? 0 : D2_CHILD) : D2,
      d3: parent ? D3 * (0.4 + 0.9 * fan) : 0,
      rank: 0,
      box: r.box,
      own: r.own,
      p: { a: 0, b: 0, c: 0 },
    };
  });

  // stagger: system by system, front to back inside a system, children after their parents
  const order = [...entries].sort((a, b) => {
    const sa = SYSTEM_ORDER.indexOf(a.system);
    const sb = SYSTEM_ORDER.indexOf(b.system);
    if (sa !== sb) return sa - sb;
    const da = a.parentKey ? 1 : 0;
    const db = b.parentKey ? 1 : 0;
    if (da !== db) return da - db;
    return b.box.max.z - a.box.max.z;
  });
  let rank = 0;
  let lastSystem = '';
  for (const e of order) {
    if (e.system !== lastSystem) {
      rank += 3; // a beat between systems
      lastSystem = e.system;
    }
    e.rank = rank++;
  }
  return { entries, byKey: new Map(entries.map((e) => [e.key, e])), maxRank: rank };
}

/** Target progress of every entry for a state. */
export function targets(rig: Rig, x: ExplodeState) {
  const out = new Map<Entry, { a: number; b: number; c: number }>();
  for (const e of rig.entries) {
    const a = x.level >= 1 ? 1 : 0;
    const b = x.level >= 2 && e.system === x.system ? 1 : 0;
    const c = x.level >= 3 && e.parentKey === x.assembly ? 1 : 0;
    out.set(e, { a, b, c });
  }
  return out;
}

/** Writes the positions for the current progress; call every frame. */
export function apply(rig: Rig) {
  for (const e of rig.entries) {
    const d = e.d1 * e.p.a + e.d2 * e.p.b + e.d3 * e.p.c;
    e.node.position.copy(e.rest).addScaledVector(e.dir, d);
  }
}

/** World offset an entry will have at the given progress, including its ancestors' moves. */
function worldOffset(rig: Rig, e: Entry, t: Map<Entry, { a: number; b: number; c: number }>, out: Vector3) {
  out.set(0, 0, 0);
  for (let cur: Entry | undefined = e; cur; cur = cur.parentKey ? rig.byKey.get(cur.parentKey) : undefined) {
    const p = t.get(cur)!;
    out.addScaledVector(cur.dirWorld, cur.d1 * p.a + cur.d2 * p.b + cur.d3 * p.c);
  }
  return out;
}

/** Where a set of parts, with their sub parts, will be once the state is reached: for the camera to frame. */
export function predictedBox(rig: Rig, x: ExplodeState, keys: Iterable<string>) {
  const t = targets(rig, x);
  const wanted = new Set(keys);
  const box = new Box3();
  const off = new Vector3();
  for (const e of rig.entries) {
    let hit = wanted.has(e.key);
    for (let p = e.parentKey; p && !hit; p = rig.byKey.get(p)?.parentKey ?? null) hit = wanted.has(p);
    if (!hit) continue;
    worldOffset(rig, e, t, off);
    box.union(e.own.clone().translate(off));
  }
  return box;
}

/** The parts a stage is about: everything, one system, or one assembly with its children. */
export function focusKeys(rig: Rig, x: ExplodeState): string[] {
  if (x.level === 2) return rig.entries.filter((e) => e.system === x.system).map((e) => e.key);
  if (x.level === 3) return rig.entries.filter((e) => e.key === x.assembly || e.parentKey === x.assembly).map((e) => e.key);
  return rig.entries.map((e) => e.key);
}

export function childrenOf(rig: Rig | null, key: string) {
  return rig ? rig.entries.filter((e) => e.parentKey === key) : [];
}
