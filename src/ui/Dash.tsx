'use client';

import { useEffect, useRef, useState } from 'react';
import { engineAudio } from '@/engine/audio';
import { engine, LIMIT_RPM, onPhase, REDLINE_RPM, setPedal, startEngine, stopEngine, type Phase } from '@/engine/sim';
import { SCENES } from '@/scene/scenes';
import { useGarage } from '@/scene/store';
import styles from './Dash.module.css';

/**
 * Game style instrument cluster (M5): tachometer and speedometer with spring needles that
 * overshoot and settle, gear, digital speed, fuel and coolant, odometer, scene name, Start
 * Engine and a hold to rev button. Space revs, E starts and stops. Values are written straight
 * to the DOM every frame; React only re-renders when the engine phase changes.
 */

const SWEEP = 240; // degrees from zero to full scale
const START = -120;
const TACH_MAX = 6000;
const SPEED_MAX = 200;

// spring needle: underdamped, so it overshoots a little and settles
const K = 210;
const C = 2 * 0.42 * Math.sqrt(K);

function arc(r: number, a0: number, a1: number) {
  const p = (a: number) => {
    const rad = ((a - 90) * Math.PI) / 180;
    return `${50 + r * Math.cos(rad)} ${50 + r * Math.sin(rad)}`;
  };
  return `M ${p(a0)} A ${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${p(a1)}`;
}

function Gauge({ max, step, label, unit, redFrom, needle }: { max: number; step: number; label: (v: number) => string; unit: string; redFrom?: number; needle: React.RefObject<SVGGElement | null> }) {
  const ticks = [];
  for (let v = 0; v <= max; v += step / 2) {
    const a = START + (v / max) * SWEEP;
    const major = v % step === 0;
    const rad = ((a - 90) * Math.PI) / 180;
    const r0 = major ? 37 : 40;
    ticks.push(
      <line key={v} x1={50 + r0 * Math.cos(rad)} y1={50 + r0 * Math.sin(rad)} x2={50 + 44 * Math.cos(rad)} y2={50 + 44 * Math.sin(rad)} className={redFrom !== undefined && v >= redFrom ? styles.tickRed : styles.tick} strokeWidth={major ? 1.6 : 0.8} />,
    );
    if (major)
      ticks.push(
        <text key={`t${v}`} x={50 + 29 * Math.cos(rad)} y={50 + 29 * Math.sin(rad) + 2.6} className={styles.num} textAnchor="middle">
          {label(v)}
        </text>,
      );
  }
  return (
    <svg viewBox="0 0 100 100" className={styles.gauge} aria-hidden>
      <circle cx="50" cy="50" r="48" className={styles.face} />
      {redFrom !== undefined && <path d={arc(42, START + (redFrom / max) * SWEEP, START + SWEEP)} className={styles.redArc} />}
      {ticks}
      <text x="50" y="72" className={styles.unit} textAnchor="middle">
        {unit}
      </text>
      <g ref={needle} style={{ transformOrigin: '50px 50px' }}>
        <line x1="50" y1="56" x2="50" y2="12" className={styles.needle} />
      </g>
      <circle cx="50" cy="50" r="4" className={styles.hub} />
    </svg>
  );
}

export default function Dash() {
  const tach = useRef<SVGGElement>(null);
  const speedo = useRef<SVGGElement>(null);
  const rpmText = useRef<HTMLSpanElement>(null);
  const speedText = useRef<HTMLSpanElement>(null);
  const gearText = useRef<HTMLSpanElement>(null);
  const odoText = useRef<HTMLSpanElement>(null);
  const fuelBar = useRef<HTMLDivElement>(null);
  const tempBar = useRef<HTMLDivElement>(null);
  const shift = useRef<HTMLDivElement>(null);
  const [phase, setPhaseState] = useState<Phase>(engine.phase);
  const [loading, setLoading] = useState(false);
  const sceneKey = useGarage((s) => s.scene);

  useEffect(() => onPhase(setPhaseState), []);

  // needles and readouts
  useEffect(() => {
    const n = { tach: { a: START, v: 0 }, speed: { a: START, v: 0 } };
    let last = performance.now();
    let raf = 0;
    const springTo = (s: { a: number; v: number }, target: number, dt: number) => {
      s.v += (K * (target - s.a) - C * s.v) * dt;
      s.a += s.v * dt;
    };
    const tick = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      springTo(n.tach, START + (Math.min(engine.rpm, TACH_MAX) / TACH_MAX) * SWEEP, dt);
      springTo(n.speed, START + (Math.min(engine.speedKmh, SPEED_MAX) / SPEED_MAX) * SWEEP, dt);
      if (tach.current) tach.current.style.transform = `rotate(${n.tach.a}deg)`;
      if (speedo.current) speedo.current.style.transform = `rotate(${n.speed.a}deg)`;
      if (rpmText.current) rpmText.current.textContent = String(Math.round(engine.rpm / 10) * 10).padStart(4, ' ');
      if (speedText.current) speedText.current.textContent = String(Math.round(engine.speedKmh)).padStart(3, ' ');
      if (gearText.current) gearText.current.textContent = engine.gear;
      if (odoText.current) odoText.current.textContent = String(Math.floor(engine.odometerKm)).padStart(6, '0');
      if (fuelBar.current) fuelBar.current.style.transform = `scaleX(${engine.fuel})`;
      if (tempBar.current) tempBar.current.style.transform = `scaleX(${engine.coolant})`;
      if (shift.current) shift.current.dataset.on = String(engine.rpm > REDLINE_RPM - 250 && engine.phase === 'running');
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  const toggleEngine = async () => {
    if (engine.phase === 'running' || engine.phase === 'cranking') {
      stopEngine();
      return;
    }
    setLoading(true);
    try {
      await engineAudio.init();
    } catch (e) {
      console.error('[garage] engine sound failed to load', e);
    } finally {
      setLoading(false);
    }
    startEngine();
  };

  // Space revs, E starts and stops
  useEffect(() => {
    const typing = (e: KeyboardEvent) => e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement;
    const down = (e: KeyboardEvent) => {
      if (typing(e)) return;
      if (e.code === 'Space') {
        e.preventDefault();
        if (!e.repeat) setPedal(1);
      }
      if ((e.key === 'e' || e.key === 'E') && !e.repeat) void toggleEngine();
    };
    const up = (e: KeyboardEvent) => {
      if (e.code === 'Space') setPedal(0);
    };
    const blur = () => setPedal(0);
    window.addEventListener('keydown', down);
    window.addEventListener('keyup', up);
    window.addEventListener('blur', blur);
    return () => {
      window.removeEventListener('keydown', down);
      window.removeEventListener('keyup', up);
      window.removeEventListener('blur', blur);
    };
  }, []);

  const on = phase === 'running' || phase === 'cranking';
  return (
    <section className={styles.dash} aria-label="Instrument cluster">
      <Gauge max={TACH_MAX} step={1000} label={(v) => String(v / 1000)} unit="x1000 r/min" redFrom={REDLINE_RPM} needle={tach} />
      <div className={styles.center}>
        <p className={styles.scene}>{SCENES[sceneKey].label}</p>
        <div className={styles.gearRow}>
          <span ref={gearText} className={styles.gear}>
            N
          </span>
          <div className={styles.digits}>
            <span>
              <span ref={speedText}>0</span>
              <small>km/h</small>
            </span>
            <span>
              <span ref={rpmText}>0</span>
              <small>rpm</small>
            </span>
          </div>
        </div>
        <div ref={shift} className={styles.shift} data-on="false" aria-hidden />
        <div className={styles.bars}>
          <label>
            <span>F</span>
            <div className={styles.bar}>
              <div ref={fuelBar} />
            </div>
          </label>
          <label>
            <span>T</span>
            <div className={`${styles.bar} ${styles.temp}`}>
              <div ref={tempBar} />
            </div>
          </label>
        </div>
        <p className={styles.odo}>
          ODO <span ref={odoText}>000000</span> km
        </p>
        <div className={styles.buttons}>
          <button type="button" className={on ? styles.stop : styles.start} onClick={() => void toggleEngine()} disabled={loading || phase === 'stopping'}>
            {loading ? 'Loading' : on ? 'Stop engine' : 'Start engine'}
          </button>
          <button
            type="button"
            className={styles.rev}
            disabled={phase !== 'running'}
            onPointerDown={(e) => {
              e.currentTarget.setPointerCapture(e.pointerId);
              setPedal(1);
            }}
            onPointerUp={() => setPedal(0)}
            onPointerCancel={() => setPedal(0)}
            onContextMenu={(e) => e.preventDefault()}
          >
            Hold to rev
          </button>
        </div>
      </div>
      <Gauge max={SPEED_MAX} step={40} label={(v) => String(v)} unit="km/h" needle={speedo} />
      <p className={styles.hint}>Space revs · E starts · limiter at {Math.round(LIMIT_RPM / 10) * 10}</p>
    </section>
  );
}
