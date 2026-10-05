'use client';

import { useEffect, useState } from 'react';
import { CONTRACT_PARTS, contract } from '@/scene/car/parts';
import { useGarage } from '@/scene/store';
import styles from './PartCard.module.css';

const SYSTEM_NAMES: Record<string, string> = {
  BODY: 'Body',
  DOOR: 'Doors',
  GLASS: 'Glass',
  WHEEL: 'Wheels and tires',
  SUSP: 'Suspension',
  BRAKE: 'Brakes',
  ENG: 'Engine',
  COOL: 'Cooling',
  EXH: 'Exhaust',
  TRANS: 'Gearbox',
  DRIVE: 'Driveline',
  ELEC: 'Electrical',
  INT: 'Interior',
  AC: 'Air conditioning',
  LIGHT: 'Lights',
  TRIM: 'Trim',
};

const SIDES: Record<string, string> = { L: 'Left', R: 'Right', F: 'Front', RR: 'Rear' };

/**
 * The part card (M4 version). It shows what the model and the contract know today: name,
 * key, system, Toyota group, fitment, open and close for hinged parts, and a deep link.
 * OEM number, price, stock and WhatsApp ordering come from the parts database in M7; the card
 * says so instead of showing made up numbers.
 */
export default function PartCard() {
  const key = useGarage((s) => s.selected);
  const select = useGarage((s) => s.select);
  const isOpen = useGarage((s) => (key ? !!s.open[key] : false));
  const togglePart = useGarage((s) => s.togglePart);
  // remembers which part's link was copied, so the label resets when another part opens
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') select(null);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [select]);

  if (!key) return null;
  const copied = copiedKey === key;
  const part = CONTRACT_PARTS.get(key);
  const side = key.match(/_(L|R|F|RR)$/)?.[1];
  const parent = part?.parent ? CONTRACT_PARTS.get(part.parent) : undefined;
  const v = contract.vehicle as { name: string; engine?: string; transmission?: string };

  const link = () => {
    const url = new URL(window.location.href);
    url.search = '';
    url.searchParams.set('part', key);
    return url.toString();
  };

  return (
    <aside className={styles.card} aria-label="Part card">
      <header className={styles.head}>
        <div>
          <p className={styles.system}>
            {SYSTEM_NAMES[part?.system ?? key.split('_')[0]] ?? 'Part'}
            {side && <span> · {SIDES[side]}</span>}
          </p>
          <h2 className={styles.name}>{part?.nameEn ?? 'Unknown part'}</h2>
        </div>
        <button type="button" className={styles.close} onClick={() => select(null)} aria-label="Close part card">
          ×
        </button>
      </header>

      <dl className={styles.facts}>
        <dt>Part key</dt>
        <dd className={styles.mono}>{key}</dd>
        <dt>Toyota group</dt>
        <dd>
          {part && part.groupCode !== '0000' ? (
            <>
              <span className={styles.mono}>{part.groupCode}</span>
              {part.groupStatus !== 'confirmed' && <span className={styles.muted}> (to confirm)</span>}
            </>
          ) : (
            <span className={styles.muted}>not known yet</span>
          )}
        </dd>
        {parent && (
          <>
            <dt>Part of</dt>
            <dd>
              <button type="button" className={styles.link} onClick={() => select(parent.key)}>
                {parent.nameEn}
              </button>
            </dd>
          </>
        )}
        <dt>Fits</dt>
        <dd>
          {v.name}, GXR{v.engine ? `, ${v.engine}` : ''}
          {v.transmission ? `, ${v.transmission}` : ''}
        </dd>
      </dl>

      <div className={styles.actions}>
        {part?.hinge && (
          <button type="button" onClick={() => togglePart(key)}>
            {isOpen ? 'Close' : 'Open'}
          </button>
        )}
        <button
          type="button"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(link());
              setCopiedKey(key);
            } catch {
              window.prompt('Copy this link', link());
            }
          }}
        >
          {copied ? 'Link copied' : 'Copy link'}
        </button>
      </div>

      <p className={styles.pending}>OEM number, price, stock and WhatsApp ordering arrive with the parts database (M7).</p>
    </aside>
  );
}
