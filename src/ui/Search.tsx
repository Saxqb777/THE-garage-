'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { buildIndex, search } from '@/data/catalog';
import { SYSTEM_NAMES } from '@/scene/car/parts';
import { goToPart } from '@/scene/goTo';
import { useGarage } from '@/scene/store';
import styles from './Search.module.css';

/**
 * Part search (M7): English, Arabic, UAE slang and OEM numbers, instant, in the browser.
 * "/" focuses it, arrows move, Enter shows the part on the car. Picking a result flies the camera
 * to the part, highlights it and opens its card.
 */
export default function Search() {
  const catalog = useGarage((s) => s.catalog);
  const index = useMemo(() => (catalog ? buildIndex([...catalog.values()]) : []), [catalog]);
  const [q, setQ] = useState('');
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  const results = useMemo(() => search(index, q, 8), [index, q]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const typing = e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement;
      if (e.key === '/' && !typing) {
        e.preventDefault();
        input.current?.focus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const pick = (key: string) => {
    goToPart(key);
    setOpen(false);
    input.current?.blur();
  };

  return (
    <div className={styles.wrap} role="search">
      <input
        ref={input}
        className={styles.input}
        type="search"
        role="combobox"
        aria-autocomplete="list"
        placeholder={catalog ? 'Search parts: alternator, دينمو, 90915…' : 'Loading parts…'}
        value={q}
        disabled={!catalog}
        aria-label="Search parts"
        aria-expanded={open && results.length > 0}
        aria-controls="part-results"
        onChange={(e) => {
          setQ(e.target.value);
          setActive(0);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
        onKeyDown={(e) => {
          // keep the scene's keys (Space revs, X ray, scenes 1 to 5) out of the search box
          e.stopPropagation();
          if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActive((a) => Math.min(results.length - 1, a + 1));
          } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActive((a) => Math.max(0, a - 1));
          } else if (e.key === 'Enter' && results[active]) {
            pick(results[active].key);
          } else if (e.key === 'Escape') {
            setOpen(false);
            input.current?.blur();
          }
        }}
      />
      {open && q && (
        <ul id="part-results" className={styles.results} role="listbox">
          {results.length === 0 && <li className={styles.empty}>No part matches “{q}”</li>}
          {results.map((p, i) => (
            <li key={p.key} role="option" aria-selected={i === active}>
              <button
                type="button"
                className={i === active ? styles.active : undefined}
                onMouseEnter={() => setActive(i)}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => pick(p.key)}
              >
                <span className={styles.name}>{p.nameEn}</span>
                {p.nameAr && (
                  <span className={styles.ar} dir="rtl" lang="ar">
                    {p.nameAr}
                  </span>
                )}
                <span className={styles.meta}>
                  {SYSTEM_NAMES[p.system] ?? p.system}
                  {' · '}
                  {p.meshPresent ? 'on the car' : 'not on the car yet'}
                  {p.oemNumber ? ` · ${p.oemNumber}` : ''}
                  {!p.fitsGxr && ' · not on the GXR'}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
