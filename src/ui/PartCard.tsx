'use client';

import { useState } from 'react';
import { groupLabel, whatsappLink } from '@/data/catalog';
import { CONTRACT_PARTS, SYSTEM_NAMES, contract } from '@/scene/car/parts';
import { goToPart } from '@/scene/goTo';
import { childrenOf } from '@/scene/explode/rig';
import { explodeRig } from '@/scene/explode/Explode';
import { HOTSPOTS, shortRef } from '@/scene/Hotspots';
import { useGarage } from '@/scene/store';
import styles from './PartCard.module.css';


const SIDES: Record<string, string> = { L: 'Left', R: 'Right', F: 'Front', RR: 'Rear' };

/**
 * The part card (M7). Name in English and Arabic, OEM number (or "to confirm" until the shop or
 * the owner fills it in), Toyota EPC group with its name, fitment, service interval, sub parts,
 * open and close for hinged parts, a share link, and Get price: there are no prices on the site,
 * the button opens WhatsApp with this exact part prefilled and the shop replies with the price.
 */
export default function PartCard() {
  const key = useGarage((s) => s.selected);
  const select = useGarage((s) => s.select);
  const isOpen = useGarage((s) => (key ? !!s.open[key] : false));
  const togglePart = useGarage((s) => s.togglePart);
  const catalog = useGarage((s) => s.catalog);
  useGarage((s) => s.rigVersion); // sub parts come from the explode rig
  // remembers which part's link was copied, so the label resets when another part opens
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  if (!key) return null;
  if (key.startsWith('hotspot:')) return <HotspotCard id={key.slice('hotspot:'.length)} onClose={() => select(null)} onPart={select} />;
  const copied = copiedKey === key;
  const row = catalog?.get(key);
  const part = CONTRACT_PARTS.get(key);
  const name = row?.nameEn ?? part?.nameEn ?? 'Unknown part';
  const system = row?.system ?? part?.system ?? key.split('_')[0];
  const groupCode = row?.groupCode ?? part?.groupCode ?? key.split('_')[1];
  const groupStatus = row?.groupStatus ?? part?.groupStatus ?? 'unknown';
  const group = groupLabel(groupCode);
  const side = key.match(/_(L|R|F|RR)$/)?.[1];
  const parent = part?.parent ? CONTRACT_PARTS.get(part.parent) : undefined;
  const v = contract.vehicle as { name: string; engine?: string; transmission?: string };
  const children = childrenOf(explodeRig.current, key);
  const x = useGarage.getState().explode;
  // the address bar already carries scene, explode stage and part (store syncUrl)
  const link = () => window.location.href;
  const wa = row && typeof window !== 'undefined' ? whatsappLink(row, window.location.href) : null;

  return (
    <aside className={`${styles.card} panel`} aria-label="Part card">
      <header className={styles.head}>
        <div>
          <p className={styles.system}>
            {SYSTEM_NAMES[system] ?? 'Part'}
            {side && <span> · {SIDES[side]}</span>}
          </p>
          <h2 className={styles.name}>{name}</h2>
          {row?.nameAr && (
            <p className={styles.ar} dir="rtl" lang="ar">
              {row.nameAr}
            </p>
          )}
          {row && !row.fitsGxr && <p className={styles.warn}>Not fitted to the GXR as standard</p>}
        </div>
        <button type="button" className={styles.close} onClick={() => select(null)} aria-label="Close part card">
          ×
        </button>
      </header>

      <dl className={styles.facts}>
        <dt>OEM number</dt>
        <dd>
          {row?.oemNumber ? (
            <span className={styles.mono}>{row.oemNumber}</span>
          ) : (
            <span className={styles.muted}>to confirm with the shop</span>
          )}
          {row?.altOemNumbers.length ? <span className={styles.muted}> (also {row.altOemNumbers.join(', ')})</span> : null}
        </dd>
        <dt>Toyota group</dt>
        <dd>
          {group ? (
            <>
              <span className={styles.mono}>{groupCode}</span> {group.slice(5)}
              {groupStatus !== 'verified' && <span className={styles.muted}> (to confirm)</span>}
            </>
          ) : (
            <span className={styles.muted}>no single group in the Toyota catalogue</span>
          )}
        </dd>
        <dt>Fits</dt>
        <dd>
          {v.name}, GXR{v.engine ? `, ${v.engine}` : ''}
          {v.transmission ? `, ${v.transmission}` : ''}
        </dd>
        {row?.serviceIntervalKm && (
          <>
            <dt>Service</dt>
            <dd>every {row.serviceIntervalKm.toLocaleString('en-US')} km</dd>
          </>
        )}
        {parent && (
          <>
            <dt>Part of</dt>
            <dd>
              <button type="button" className={styles.link} onClick={() => goToPart(parent.key)}>
                {parent.nameEn}
              </button>
            </dd>
          </>
        )}
        {row && !row.meshPresent ? (
          <>
            <dt>On the car</dt>
            <dd className={styles.muted}>not shown on the car yet</dd>
          </>
        ) : (
          <>
            <dt>Sub parts</dt>
            <dd>
              {children.length ? (
                <>
                  {children.length} in the model
                  {x.level > 0 && x.assembly !== key && <span className={styles.muted}>, click the part to explode it</span>}
                </>
              ) : (
                <span className={styles.muted}>none in the model</span>
              )}
            </dd>
          </>
        )}
      </dl>
      <Barcode code={key} />
      <p className={styles.code}>{key}</p>

      <div className={styles.actions}>
        {wa ? (
          <a className={styles.price} href={wa} target="_blank" rel="noopener noreferrer">
            Get price on WhatsApp
          </a>
        ) : (
          <button type="button" className={styles.price} disabled title="The shop's WhatsApp number is not set yet">
            Get price on WhatsApp
          </button>
        )}
      </div>
      <div className={styles.actions}>
        {part?.hinge && (
          <button type="button" className="btn" onClick={() => togglePart(key)}>
            {isOpen ? 'Close' : 'Open'}
          </button>
        )}
        <button
          type="button"
          className="btn"
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
      {!wa && <p className={styles.pending}>The shop&apos;s WhatsApp number is not set yet.</p>}
    </aside>
  );
}

/** Bars from the part key, like the label on a parts bin: the same key always draws the same bars. */
function Barcode({ code }: { code: string }) {
  const bars: number[] = [];
  let h = 2166136261;
  for (let i = 0; i < 46; i++) {
    h = Math.imul(h ^ code.charCodeAt(i % code.length), 16777619) >>> 0;
    bars.push(1 + (h % 3));
  }
  return (
    <div className={styles.barcode} aria-hidden>
      {bars.map((w, i) => (
        <i key={i} style={{ width: w, marginRight: i % 2 ? 1 : 0, height: i % 11 === 0 ? '100%' : '82%' }} />
      ))}
    </div>
  );
}

/** Card for a cabin control from the owner's manual (no mesh of its own yet). */
function HotspotCard({ id, onClose, onPart }: { id: string; onClose: () => void; onPart: (key: string) => void }) {
  const h = HOTSPOTS.get(id);
  if (!h) return null;
  const part = h.partKey ? CONTRACT_PARTS.get(h.partKey) : undefined;
  return (
    <aside className={`${styles.card} panel`} aria-label="Control card">
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
      <p className={styles.pending}>Part numbers for the cabin controls come with the switch parts in the catalogue.</p>
    </aside>
  );
}
