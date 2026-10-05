'use client';

import { useEffect, useRef } from 'react';
import { CONTRACT_PARTS } from '@/scene/car/parts';
import { useGarage } from '@/scene/store';
import styles from './HoverLabel.module.css';

/**
 * Name of the part under the pointer, riding next to the cursor. The position is written
 * straight to the element on every pointer move, so React only re-renders when the part changes.
 */
export default function HoverLabel() {
  const hovered = useGarage((s) => s.hovered);
  const open = useGarage((s) => (hovered ? s.open[hovered] : false));
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const move = (e: PointerEvent) => {
      if (ref.current) ref.current.style.transform = `translate(${e.clientX + 16}px, ${e.clientY + 14}px)`;
    };
    window.addEventListener('pointermove', move);
    return () => window.removeEventListener('pointermove', move);
  }, []);

  const part = hovered ? CONTRACT_PARTS.get(hovered) : undefined;
  return (
    <div ref={ref} className={styles.label} hidden={!hovered} aria-hidden>
      <span className={styles.name}>{part?.nameEn ?? hovered}</span>
      {part?.hinge && <span className={styles.action}>click to {open ? 'close' : 'open'}</span>}
    </div>
  );
}
