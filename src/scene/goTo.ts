import { Box3, Vector3 } from 'three';
import { partNodes } from './car/parts';
import { explodeRig } from './explode/Explode';
import { predictedBox } from './explode/rig';
import { carLift } from './liftState';
import { useGarage } from './store';

/**
 * Show one part on the car (search results, deep links, the service list): select it, fly the
 * camera to it and, for a part that is only a hotspot (engine, brakes, suspension parts that are
 * not modelled), turn on X Ray so its marker can be seen through the body.
 */
export function goToPart(key: string) {
  const s = useGarage.getState();
  const part = s.catalog?.get(key);
  s.select(key);
  const node = partNodes.get(key);
  let box: Box3 | null = null;
  if (node) {
    const rig = explodeRig.current;
    box = rig && s.explode.level > 0 ? predictedBox(rig, s.explode, [key]) : new Box3().setFromObject(node, true);
  } else if (part?.hotspot) {
    const [x, y, z] = part.hotspot;
    box = new Box3().setFromCenterAndSize(new Vector3(x, y + carLift.y, z), new Vector3(0.6, 0.6, 0.6));
    if (!s.xray) s.setXray(true);
  }
  if (!box || box.isEmpty()) return;
  // small parts get some of the car around them for context
  const size = box.getSize(new Vector3());
  const min = 0.9;
  box.expandByVector(new Vector3(Math.max(0, min - size.x) / 2, Math.max(0, min - size.y) / 2, Math.max(0, min - size.z) / 2));
  s.requestCam({ action: 'frame', min: box.min.toArray() as [number, number, number], max: box.max.toArray() as [number, number, number] });
}
