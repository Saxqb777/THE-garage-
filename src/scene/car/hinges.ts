import { MathUtils, Quaternion, Vector3, type Object3D } from 'three';
import type { PartNode } from './parts';

/** One hinged node; GSAP tweens t between 0 (closed) and 1 (open). */
export type HingeRig = { key: string; node: Object3D; axis: Vector3; rest: Quaternion; angle: number; t: number };

// Rest pose per node, captured once: useGLTF caches the scene, so it can be mounted again while open.
const restPose = new WeakMap<Object3D, Quaternion>();

export function rigHinges(root: Object3D, parts: Iterable<PartNode>): HingeRig[] {
  const rigs: HingeRig[] = [];
  for (const { key, object: node, hinge } of parts) {
    if (!hinge) continue;
    if (!restPose.has(node)) restPose.set(node, node.quaternion.clone());
    // Hinge axes are given in model (three) space; express them in the node's parent space.
    const parentToModel = new Quaternion();
    for (let p = node.parent; p && p !== root; p = p.parent) parentToModel.premultiply(restPose.get(p) ?? p.quaternion);
    rigs.push({
      key,
      node,
      axis: new Vector3(...hinge.axis).normalize().applyQuaternion(parentToModel.invert()),
      rest: restPose.get(node)!,
      angle: MathUtils.degToRad(hinge.openDeg),
      t: 0,
    });
  }
  return rigs;
}

const open = new Quaternion();

/** Opening rotation about the hinge axis, applied on top of the rest rotation. */
export function poseHinges(rigs: HingeRig[]) {
  for (const r of rigs) r.node.quaternion.multiplyQuaternions(open.setFromAxisAngle(r.axis, r.t * r.angle), r.rest);
}

export function closeHinges(rigs: HingeRig[]) {
  for (const r of rigs) r.t = 0;
  poseHinges(rigs);
}
