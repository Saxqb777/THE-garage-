'use client';

import { useEffect } from 'react';
import { useEnvironment, useProgress } from '@react-three/drei';
import { CREDITS } from '@/data/credits';
import contract from '@/data/parts.m1.json';
import { dueAt } from '@/data/catalog';
import { goToPart } from '@/scene/goTo';
import { SCENES, SCENE_ORDER, hdriUrl } from '@/scene/scenes';
import { PLACEHOLDER_URL, useGarage, type PresetKey } from '@/scene/store';
import styles from './Hud.module.css';

const num = new Intl.NumberFormat('en-US');

const PRESETS: [PresetKey, string][] = [
  ['hero', 'Hero'],
  ['front', 'Front'],
  ['rear', 'Rear'],
  ['side', 'Side'],
  ['engine', 'Engine'],
  ['interior', 'Cabin'],
  ['underside', 'Under'],
];

const SCENE_TAGS: Record<string, string> = { garage: 'WORKSHOP', dunes: 'LIWA', corniche_night: 'NIGHT', highway: 'E11', desert_road: 'E66' };

const Key = ({ k }: { k: string }) => <kbd className="key">{k}</kbd>;

/** The job card: vehicle, doors, camera, scene, light, service. Left side of the screen. */
export default function Hud() {
  const { progress } = useProgress();
  const url = useGarage((s) => s.modelUrl);
  const model = useGarage((s) => s.model);
  const error = useGarage((s) => s.modelError);
  const triangles = useGarage((s) => s.triangles);
  const drawCalls = useGarage((s) => s.drawCalls);
  const hingesOpen = useGarage((s) => s.hingesOpen);
  const setHingesOpen = useGarage((s) => s.setHingesOpen);
  const toggleHinges = useGarage((s) => s.toggleHinges);
  const sceneKey = useGarage((s) => s.targetScene);
  const shownKey = useGarage((s) => s.scene);
  const setScene = useGarage((s) => s.setScene);
  const timeOfDay = useGarage((s) => s.timeOfDay);
  const setTimeOfDay = useGarage((s) => s.setTimeOfDay);
  const lightsOn = useGarage((s) => s.lightsOn);
  const setLightsOn = useGarage((s) => s.setLightsOn);
  const xray = useGarage((s) => s.xray);
  const setXray = useGarage((s) => s.setXray);
  const scene = SCENES[sceneKey];
  const view = useGarage((s) => s.view);
  const camBusy = useGarage((s) => s.camBusy);
  const requestCam = useGarage((s) => s.requestCam);
  const lift = useGarage((s) => s.lift);
  const setLift = useGarage((s) => s.setLift);
  const inGarage = shownKey === 'garage';
  const exploded = useGarage((s) => s.explode.level > 0);
  const service = useGarage((s) => s.service);
  const setService = useGarage((s) => s.setService);
  const catalog = useGarage((s) => s.catalog);
  const due = service && catalog ? dueAt([...catalog.values()], service).sort((a, b) => a.nameEn.localeCompare(b.nameEn)) : [];
  const explodeAll = useGarage((s) => s.explodeAll);
  const assemble = useGarage((s) => s.assemble);
  const debug = typeof window !== 'undefined' && new URLSearchParams(window.location.search).has('debug');
  const v = contract.vehicle as { name: string; key: string; engine?: string; transmission?: string; drive?: string };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
      // typing in the search box is not a shortcut (checkboxes and sliders still are)
      if ((e.target instanceof HTMLInputElement && ['text', 'search'].includes(e.target.type)) || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === 'Escape') {
        const st = useGarage.getState();
        if (st.selected) st.select(null);
        else if (st.explode.level > 0) st.explodeUp();
        return;
      }
      if (e.key === 'h' || e.key === 'H') toggleHinges();
      if (e.key === 'l' || e.key === 'L') setLightsOn(!useGarage.getState().lightsOn);
      if (e.key === 'x' || e.key === 'X') setXray(!useGarage.getState().xray);
      if (e.key === 'g' || e.key === 'G') {
        const st = useGarage.getState();
        if (!st.camBusy) st.requestCam(st.view === 'cabin' ? { action: 'getOut' } : { action: 'getIn', seat: 'driver' });
      }
      const n = Number(e.key);
      if (n >= 1 && n <= SCENE_ORDER.length) setScene(SCENE_ORDER[n - 1]);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [toggleHinges, setLightsOn, setXray, setScene]);

  return (
    <aside className={`${styles.hud} panel boot`} style={{ '--boot': '0.05s' } as React.CSSProperties}>
      <header className={styles.head}>
        <span className="stamp">The Garage</span>
        <h1 className={styles.vehicle}>{v.name}</h1>
        <p className={styles.spec}>
          <b>FZJ100</b> · {v.engine ?? '1FZ-FE'} · {v.transmission ?? '5MT'} · {v.drive ?? 'LHD'} · GXR
        </p>
        {!model && !error && (
          <div className={styles.progress} aria-label="Loading model">
            <div className={styles.track}>
              <div className={styles.bar} style={{ transform: `scaleX(${progress / 100})` }} />
            </div>
            <span>{progress.toFixed(0)}%</span>
          </div>
        )}
      </header>
      {error && (
        <div className={styles.error}>
          <p>{error}</p>
          <p>
            Add the GLB to public/models, or <a href="?model=placeholder">open the placeholder</a>.
          </p>
        </div>
      )}

      <section className={styles.section}>
        <div className={styles.sectionHead}>
          <span className="label">Doors</span>
          <span>
            <Key k="H" />
          </span>
        </div>
        <div className={styles.seg} role="group" aria-label="Doors">
          <button type="button" onClick={() => setHingesOpen(true)} disabled={!model || hingesOpen}>
            Open all
          </button>
          <button type="button" onClick={() => setHingesOpen(false)} disabled={!model || !hingesOpen}>
            Close all
          </button>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionHead}>
          <span className="label">Camera</span>
          <span>
            <Key k="G" />
          </span>
        </div>
        <div className={styles.row}>
          <button
            type="button"
            className={`btn ${view === 'cabin' ? 'btnOn' : ''}`}
            disabled={!model || camBusy || exploded}
            onClick={() => requestCam(view === 'cabin' ? { action: 'getOut' } : { action: 'getIn', seat: 'driver' })}
          >
            {view === 'cabin' ? 'Get out' : 'Get in'}
          </button>
          <button type="button" className={`btn ${lift ? 'btnOn' : ''}`} disabled={!model || camBusy || !inGarage || view === 'cabin' || exploded} onClick={() => setLift(!lift)} title="Two post lift, Garage only">
            {lift ? 'Lower' : 'Lift'}
          </button>
          <button type="button" className={`btn ${exploded ? 'btnOn' : ''}`} disabled={!model || camBusy} onClick={() => (exploded ? assemble() : explodeAll())}>
            {exploded ? 'Assemble' : 'Explode'}
          </button>
        </div>
        <div className={styles.presets} aria-label="Views" style={{ marginTop: 6 }}>
          {PRESETS.map(([k, label]) => (
            <button key={k} type="button" disabled={!model || camBusy} onClick={() => requestCam({ action: 'preset', preset: k })}>
              {label}
            </button>
          ))}
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionHead}>
          <span className="label">Location</span>
          <span>
            <Key k="1" />
            <Key k="5" />
          </span>
        </div>
        <div className={styles.scenes} role="radiogroup" aria-label="Scene">
          {SCENE_ORDER.map((k, i) => (
            <button
              key={k}
              type="button"
              role="radio"
              aria-checked={k === sceneKey}
              aria-busy={k === sceneKey && k !== shownKey}
              className={k === sceneKey ? styles.sceneOn : undefined}
              title={SCENES[k].hint}
              onPointerEnter={() => useEnvironment.preload({ files: hdriUrl(SCENES[k]) })}
              onFocus={() => useEnvironment.preload({ files: hdriUrl(SCENES[k]) })}
              onClick={() => setScene(k)}
            >
              <kbd className="key">{i + 1}</kbd>
              {SCENES[k].label}
              <small>{SCENE_TAGS[k] ?? ''}</small>
            </button>
          ))}
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionHead}>
          <span className="label">Light</span>
          <span>
            <Key k="L" />
            <Key k="X" />
          </span>
        </div>
        <div className={styles.controls}>
          <label className={styles.slider} aria-disabled={!scene.timeOfDay}>
            <span>Sun</span>
            <input type="range" min={0} max={1} step={0.01} value={timeOfDay} disabled={!scene.timeOfDay} onChange={(e) => setTimeOfDay(Number(e.target.value))} />
          </label>
          <label className={styles.switch}>
            <input type="checkbox" checked={lightsOn} onChange={(e) => setLightsOn(e.target.checked)} />
            <i />
            <span style={{ marginRight: 'auto' }}>Lamps</span>
          </label>
          <label className={styles.switch}>
            <input type="checkbox" checked={xray} onChange={(e) => setXray(e.target.checked)} />
            <i />
            <span style={{ marginRight: 'auto' }}>X Ray</span>
          </label>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionHead}>
          <span className="label">Service</span>
          <span className={styles.spec}>km</span>
        </div>
        <div className={styles.chips} role="radiogroup" aria-label="Service interval">
          {[5000, 10000, 40000, 80000].map((km) => (
            <button key={km} type="button" role="radio" aria-checked={service === km} className={service === km ? styles.sceneOn : undefined} disabled={!catalog} onClick={() => setService(service === km ? null : km)}>
              {km / 1000}k
            </button>
          ))}
        </div>
        {service && (
          <ul className={styles.dueList}>
            {due.length === 0 && <li className={styles.hint}>Nothing listed for this interval yet</li>}
            {due.map((p) => (
              <li key={p.key}>
                <button type="button" onClick={() => goToPart(p.key)}>
                  {p.nameEn}
                  <span>{p.serviceIntervalKm! / 1000}k</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className={styles.keys}>
        <span>
          <Key k="/" /> search
        </span>
        <span>
          <Key k="E" /> engine
        </span>
        <span>
          <Key k="Space" /> rev
        </span>
        <span>
          <Key k="Esc" /> back
        </span>
        <span>drag to orbit · click a part</span>
      </div>
      {url === PLACEHOLDER_URL && <p className={styles.badge}>placeholder blockout</p>}
      {debug && (
        <dl className={styles.debug}>
          <dt>parts</dt>
          <dd>{model ? num.format(model.partKeys.length) : '...'}</dd>
          <dt>triangles</dt>
          <dd>{num.format(triangles)}</dd>
          <dt>draw calls</dt>
          <dd>{num.format(drawCalls)}</dd>
        </dl>
      )}

      <details className={styles.credits}>
        <summary>Credits</summary>
        <ul>
          {CREDITS.map((c) => (
            <li key={c.what}>
              {c.what}: {c.who} ({c.license})
            </li>
          ))}
        </ul>
      </details>
    </aside>
  );
}
