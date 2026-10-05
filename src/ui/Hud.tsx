'use client';

import { useEffect } from 'react';
import { useEnvironment, useProgress } from '@react-three/drei';
import { CREDITS } from '@/data/credits';
import contract from '@/data/parts.m1.json';
import { SCENES, SCENE_ORDER, hdriUrl } from '@/scene/scenes';
import { PLACEHOLDER_URL, useGarage } from '@/scene/store';
import styles from './Hud.module.css';

const num = new Intl.NumberFormat('en-US');

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
  const scene = SCENES[sceneKey];

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'h' || e.key === 'H') toggleHinges();
      if (e.key === 'l' || e.key === 'L') setLightsOn(!useGarage.getState().lightsOn);
      const n = Number(e.key);
      if (n >= 1 && n <= SCENE_ORDER.length) setScene(SCENE_ORDER[n - 1]);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [toggleHinges, setLightsOn, setScene]);

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
      </div>

      <p className={styles.hint}>Drag to orbit · scroll to zoom · H doors · L lights · 1 to 5 scenes</p>
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
