'use client';

import { Html } from '@react-three/drei';
import data from '@/data/hotspots.interior.json';
import { useGarage } from './store';
import styles from './Hotspots.module.css';

export type Hotspot = (typeof data.hotspots)[number];

export const HOTSPOTS = new Map(data.hotspots.map((h) => [h.id, h]));

/** Manual reference as a short tag: "View A 3" is A3, "Cluster 2" is C2. */
export function shortRef(ref: string) {
  const m = /^(?:View )?([AB]|Cluster) (\d+)/.exec(ref);
  return m ? `${m[1] === 'Cluster' ? 'C' : m[1]}${m[2]}` : ref;
}

/**
 * In cabin hotspots for the controls the owner's manual numbers (pages 2 to 6), stripped to the
 * GCC GXR. Each dot carries the manual's number; hovering shows the Toyota name, clicking opens
 * its card. Shown only while seated.
 */
export default function Hotspots() {
  const view = useGarage((s) => s.view);
  const busy = useGarage((s) => s.camBusy);
  const selected = useGarage((s) => s.selected);
  const select = useGarage((s) => s.select);
  if (view !== 'cabin' || busy) return null;
  return (
    <>
      {data.hotspots.map((h) => {
        const p = h.position;
        const n = h.normal;
        const id = `hotspot:${h.id}`;
        return (
          <Html key={h.id} position={[p[0] + n[0] * 0.012, p[1] + n[1] * 0.012, p[2] + n[2] * 0.012]} center zIndexRange={[5, 0]}>
            <button
              type="button"
              className={`${styles.dot} ${selected === id ? styles.on : ''}`}
              onClick={(e) => {
                e.stopPropagation();
                select(id);
              }}
              aria-label={h.label}
            >
              {shortRef(h.ref)}
              <span className={styles.tip}>{h.label}</span>
            </button>
          </Html>
        );
      })}
    </>
  );
}
