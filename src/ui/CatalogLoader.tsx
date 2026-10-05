'use client';

import { useEffect, useRef } from 'react';
import type { CatalogPart, CatalogResponse } from '@/data/catalog';
import { goToPart } from '@/scene/goTo';
import { useGarage } from '@/scene/store';

/** Loads the parts catalogue once, then opens a deep linked part (?part=KEY) on the car. */
export default function CatalogLoader() {
  const loaded = useGarage((s) => s.model !== null);
  const catalog = useGarage((s) => s.catalog);
  const done = useRef(false);

  useEffect(() => {
    let alive = true;
    (async () => {
      let body: CatalogResponse;
      try {
        const res = await fetch('/api/parts');
        if (!res.ok) throw new Error(String(res.status));
        body = await res.json();
      } catch (e) {
        console.warn('[garage] /api/parts failed, using the bundled seed', e);
        const seed = (await import('@/data/parts.seed.json')).default as CatalogPart[];
        body = { source: 'seed', parts: seed };
      }
      if (!alive) return;
      useGarage.setState({ catalog: new Map(body.parts.map((p) => [p.key, p])), catalogSource: body.source });
    })();
    return () => {
      alive = false;
    };
  }, []);

  // a part in the link, with the car assembled: fly to it once everything is in
  useEffect(() => {
    if (done.current || !loaded || !catalog) return;
    done.current = true;
    const s = useGarage.getState();
    if (s.selected && s.explode.level === 0 && !s.selected.startsWith('hotspot:')) setTimeout(() => goToPart(s.selected!), 300);
  }, [loaded, catalog]);

  return null;
}
