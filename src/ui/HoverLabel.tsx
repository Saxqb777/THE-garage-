'use client';

import { useEffect, useRef } from 'react';
import { CONTRACT_PARTS, SYSTEM_NAMES } from '@/scene/car/parts';
import { childrenOf } from '@/scene/explode/rig';
import { explodeRig } from '@/scene/explode/Explode';
import { useGarage } from '@/scene/store';
import styles from './HoverLabel.module.css';

/**
 * Name of the part under the pointer, riding next to the cursor. The position is written
 * straight to the element on every pointer move, so React only re-renders when the part changes.
 */
export default function HoverLabel() {
  const hovered = useGarage((s) => s.hovered);
  const open = useGarage((s) => (hovered ? s.open[hovered] : false));
  const x = useGarage((s) => s.explode);
  useGarage((s) => s.rigVersion);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const move = (e: PointerEvent) => {
      if (ref.current) ref.current.style.transform = `translate(${e.clientX + 16}px, ${e.clientY + 14}px)`;
    };
    window.addEventListener('pointermove', move);
    return () => window.removeEventListener('pointermove', move);
  }, []);

  const part = hovered ? CONTRACT_PARTS.get(hovered) : undefined;
  const row = useGarage((s) => (hovered ? s.catalog?.get(hovered) : undefined));
  let hint: string | null = null;
  if (hovered && x.level > 0) {
    const system = hovered.split('_')[0];
    if (x.level === 1 || x.system !== system) hint = `click to explode ${SYSTEM_NAMES[system] ?? system}`;
    else if (childrenOf(explodeRig.current, hovered).length && x.assembly !== hovered) hint = 'click to explode this assembly';
    else hint = 'click to zoom in';
  } else if (part?.hinge) hint = `click to ${open ? 'close' : 'open'}`;
  return (
    <div ref={ref} className={styles.label} hidden={!hovered} aria-hidden>
      <span className={styles.name}>{row?.nameEn ?? part?.nameEn ?? hovered}</span>
      {row?.nameAr && (
        <span className={styles.ar} dir="rtl" lang="ar">
          {row.nameAr}
        </span>
      )}
      {hint && <span className={styles.action}>{hint}</span>}
    </div>
  );
}
