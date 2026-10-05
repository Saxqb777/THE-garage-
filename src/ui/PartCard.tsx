'use client';

import { useState } from 'react';
import { CONTRACT_PARTS, SYSTEM_NAMES, contract } from '@/scene/car/parts';
import { childrenOf } from '@/scene/explode/rig';
import { explodeRig } from '@/scene/explode/Explode';
import { HOTSPOTS, shortRef } from '@/scene/Hotspots';
import { useGarage } from '@/scene/store';
import styles from './PartCard.module.css';


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
  useGarage((s) => s.rigVersion); // sub parts come from the explode rig
  // remembers which part's link was copied, so the label resets when another part opens
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  if (!key) return null;
  if (key.startsWith('hotspot:')) return <HotspotCard id={key.slice('hotspot:'.length)} onClose={() => select(null)} onPart={select} />;
  const copied = copiedKey === key;
  const part = CONTRACT_PARTS.get(key);
  const side = key.match(/_(L|R|F|RR)$/)?.[1];
  const parent = part?.parent ? CONTRACT_PARTS.get(part.parent) : undefined;
  const v = contract.vehicle as { name: string; engine?: string; transmission?: string };

  // the address bar already carries scene, explode stage and part (store syncUrl)
  const link = () => window.location.href;
  const children = childrenOf(explodeRig.current, key);
  const x = useGarage.getState().explode;

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
        <dt>Sub parts</dt>
        <dd>
          {children.length ? (
            <>
              {children.length} in the model
              {x.level > 0 && x.assembly !== key && <span className={styles.muted}>, click the part to explode it</span>}
            </>
          ) : (
            <span className={styles.muted}>none in the model yet, the Toyota diagram comes with M7</span>
          )}
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

/** Card for a cabin control from the owner's manual (no mesh of its own yet). */
function HotspotCard({ id, onClose, onPart }: { id: string; onClose: () => void; onPart: (key: string) => void }) {
  const h = HOTSPOTS.get(id);
  if (!h) return null;
  const part = h.partKey ? CONTRACT_PARTS.get(h.partKey) : undefined;
  return (
    <aside className={styles.card} aria-label="Control card">
      <header className={styles.head}>
        <div>
          <p className={styles.system}>
            Cabin control · <span className={styles.mono}>{shortRef(h.ref)}</span>
          </p>
          <h2 className={styles.name}>{h.label}</h2>
        </div>
        <button type="button" className={styles.close} onClick={onClose} aria-label="Close card">
          ×
        </button>
      </header>
      <dl className={styles.facts}>
        <dt>Owner&apos;s manual</dt>
        <dd>
          {h.ref}, pages 2 to 6
        </dd>
        {part && (
          <>
            <dt>Sits on</dt>
            <dd>
              <button type="button" className={styles.link} onClick={() => onPart(part.key)}>
                {part.nameEn}
              </button>
            </dd>
          </>
        )}
        <dt>Position</dt>
        <dd>{h.placement === 'raycast' ? 'picked on the model' : 'approximate, the control is hidden or not modelled'}</dd>
      </dl>
      <p className={styles.pending}>Part number, price and WhatsApp ordering arrive with the parts database (M7).</p>
    </aside>
  );
}
