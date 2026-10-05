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
  ['interior', 'Interior'],
  ['underside', 'Under'],
];

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
    <aside className={styles.hud}>
      <h1 className={styles.title}>The Garage</h1>
      <p className={styles.vehicle}>{contract.vehicle.name}</p>
      <p className={styles.file}>{url.split('/').pop()}</p>

      {!model && !error && (
        <div className={styles.progress} aria-label="Loading model">
          <div className={styles.track}>
            <div className={styles.bar} style={{ transform: `scaleX(${progress / 100})` }} />
          </div>
          <span>{progress.toFixed(0)}%</span>
        </div>
      )}
      {error && (
        <div className={styles.error}>
          <p>{error}</p>
          <p>
            Add the GLB to public/models, or <a href="?model=placeholder">open the placeholder</a>.
          </p>
        </div>
      )}

      <dl className={styles.stats}>
        <dt>Parts</dt>
        <dd>{model ? num.format(model.partKeys.length) : '...'}</dd>
        <dt>Triangles</dt>
        <dd>{num.format(triangles)}</dd>
        <dt>Draw calls</dt>
        <dd>{num.format(drawCalls)}</dd>
      </dl>

      <div className={styles.actions}>
        <button type="button" onClick={() => setHingesOpen(true)} disabled={!model || hingesOpen}>
          Open all
        </button>
        <button type="button" onClick={() => setHingesOpen(false)} disabled={!model || !hingesOpen}>
          Close all
        </button>
      </div>

      <div className={styles.camera}>
        <button
          type="button"
          className={styles.primary}
          disabled={!model || camBusy || exploded}
          onClick={() => requestCam(view === 'cabin' ? { action: 'getOut' } : { action: 'getIn', seat: 'driver' })}
        >
          {view === 'cabin' ? 'Get out' : 'Get in'}
        </button>
        <button type="button" disabled={!model || camBusy || !inGarage || view === 'cabin' || exploded} onClick={() => setLift(!lift)} title="Two post lift, Garage only">
          {lift ? 'Lower lift' : 'Lift'}
        </button>
        <button type="button" className={exploded ? styles.primary : undefined} disabled={!model || camBusy} onClick={() => (exploded ? assemble() : explodeAll())}>
          {exploded ? 'Assemble' : 'Explode'}
        </button>
      </div>
      <div className={styles.presets} aria-label="Camera">
        {PRESETS.map(([k, label]) => (
          <button key={k} type="button" disabled={!model || camBusy} onClick={() => requestCam({ action: 'preset', preset: k })}>
            {label}
          </button>
        ))}
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
            title={`${SCENES[k].hint} (${i + 1})`}
            onPointerEnter={() => useEnvironment.preload({ files: hdriUrl(SCENES[k]) })}
            onFocus={() => useEnvironment.preload({ files: hdriUrl(SCENES[k]) })}
            onClick={() => setScene(k)}
          >
            {SCENES[k].label}
          </button>
        ))}
      </div>

      <div className={styles.controls}>
        <label className={styles.slider} aria-disabled={!scene.timeOfDay}>
          <span>Time of day</span>
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={timeOfDay}
            disabled={!scene.timeOfDay}
            onChange={(e) => setTimeOfDay(Number(e.target.value))}
          />
        </label>
        <label className={styles.toggle}>
          <input type="checkbox" checked={lightsOn} onChange={(e) => setLightsOn(e.target.checked)} />
          <span>Lights</span>
        </label>
        <label className={styles.toggle}>
          <input type="checkbox" checked={xray} onChange={(e) => setXray(e.target.checked)} />
          <span>X Ray</span>
        </label>
      </div>

      <div className={styles.service}>
        <p className={styles.sectionTitle}>Service</p>
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
      </div>

      <p className={styles.hint}>Click a part for its card · click doors to open · drag to orbit · G get in · H all doors · L lights · X x ray · 1 to 5 scenes · Esc back</p>
      {url === PLACEHOLDER_URL && <p className={styles.badge}>placeholder blockout</p>}

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
