'use client';

import { CONTRACT_PARTS, SYSTEM_NAMES } from '@/scene/car/parts';
import { useGarage } from '@/scene/store';
import styles from './ExplodeBar.module.css';

/** Breadcrumb for the explode stages: Exploded › Doors › Front door, left. Each crumb goes back to its stage. */
export default function ExplodeBar() {
  const x = useGarage((s) => s.explode);
  const busy = useGarage((s) => s.camBusy);
  const explodeAll = useGarage((s) => s.explodeAll);
  const focusSystem = useGarage((s) => s.focusSystem);
  const explodeUp = useGarage((s) => s.explodeUp);
  const assemble = useGarage((s) => s.assemble);
  if (x.level === 0) return null;
  const crumbs: { label: string; go: () => void; current: boolean }[] = [{ label: 'Exploded', go: explodeAll, current: x.level === 1 }];
  if (x.system) crumbs.push({ label: SYSTEM_NAMES[x.system] ?? x.system, go: () => focusSystem(x.system!), current: x.level === 2 });
  if (x.assembly) crumbs.push({ label: CONTRACT_PARTS.get(x.assembly)?.nameEn ?? x.assembly, go: () => {}, current: true });
  return (
    <nav className={`${styles.bar} panel`} aria-label="Explode stages">
      <ol className={styles.crumbs}>
        {crumbs.map((c, i) => (
          <li key={c.label}>
            {i > 0 && <span className={styles.sep}>›</span>}
            <button type="button" className={c.current ? styles.current : undefined} onClick={c.go} disabled={c.current}>
              {c.label}
            </button>
          </li>
        ))}
      </ol>
      <div className={styles.actions}>
        <button type="button" className="btn" onClick={explodeUp} disabled={busy} title="Esc">
          Back
        </button>
        <button type="button" className="btn btnOn" onClick={assemble} disabled={busy}>
          Assemble
        </button>
      </div>
    </nav>
  );
}
