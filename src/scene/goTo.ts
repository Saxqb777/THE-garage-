import { Box3, Vector3 } from 'three';
import { partNodes } from './car/parts';
import { explodeRig } from './explode/Explode';
import { predictedBox } from './explode/rig';
import { useGarage } from './store';

/**
 * Show one part on the car (search results, deep links, the service list): select it and fly the
 * camera to it. Parts that are not on the model (engine, brakes, suspension: on hold) only open
 * their card; the camera stays where it is.
 */
export function goToPart(key: string) {
  const s = useGarage.getState();
  s.select(key);
  const node = partNodes.get(key);
  if (!node) return;
  const rig = explodeRig.current;
  const box = rig && s.explode.level > 0 ? predictedBox(rig, s.explode, [key]) : new Box3().setFromObject(node, true);
  if (box.isEmpty()) return;
  // small parts get some of the car around them for context
  const size = box.getSize(new Vector3());
  const min = 0.9;
  box.expandByVector(new Vector3(Math.max(0, min - size.x) / 2, Math.max(0, min - size.y) / 2, Math.max(0, min - size.z) / 2));
  s.requestCam({ action: 'frame', min: box.min.toArray() as [number, number, number], max: box.max.toArray() as [number, number, number] });
}
