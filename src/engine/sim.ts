/**
 * 1FZ-FE engine model for the rev experience (M5). Not a physics engine: a few first order
 * responses tuned to feel like a heavy inline six in a 2.5 tonne SUV.
 *
 *  - pedal to throttle: quick smoothing, progressive throttle curve
 *  - rpm chases a target (idle plus throttle) with separate rise and fall rates, capped like a
 *    heavy flywheel; in gear on the lift the wheels add inertia
 *  - cold start: about 1150 rpm fast idle that settles to 650 as the engine warms
 *  - rev limiter just above the 5000 rpm redline: fuel cut for a moment, which makes it bounce
 *  - body: roll and pitch on springs driven by the change in rpm (engine torque reaction),
 *    plus idle rock, stronger right after a cold start
 *
 * Numbers that are not from Toyota data are marked approx. The singleton runs its own
 * requestAnimationFrame loop so the HUD, the audio and the 3D scene all read one state.
 */

export const IDLE_RPM = 650; // approx, 1FZ-FE warm idle
export const COLD_IDLE_RPM = 1150; // approx, fast idle
export const REDLINE_RPM = 5000;
export const LIMIT_RPM = 5080;

// H151F five speed: first gear 4.08 (approx), final drive 4.10 (approx); 275/70R16 tire
const FIRST_GEAR = 4.08;
const FINAL_DRIVE = 4.1;
const TIRE_CIRCUMFERENCE_M = Math.PI * (16 * 0.0254 + 2 * 0.7 * 0.275);

export type Phase = 'off' | 'cranking' | 'running' | 'stopping';

export type EngineState = {
  phase: Phase;
  rpm: number;
  /** 0..1, what the driver asks for */
  pedal: number;
  /** 0..1, smoothed and after the limiter */
  throttle: number;
  /** rpm per second, for torque reaction and sound */
  rpmRate: number;
  gear: 'N' | '1';
  wheelRpm: number;
  speedKmh: number;
  /** 0 cold, 1 warm */
  warm: number;
  /** coolant gauge 0..1 */
  coolant: number;
  fuel: number;
  odometerKm: number;
  /** body motion in radians, applied to the sprung part of the car */
  roll: number;
  pitch: number;
  /** seconds since the last start, for the cold start wobble */
  sinceStart: number;
  /** time inside the current phase */
  phaseTime: number;
  limiterCut: number;
};

export const engine: EngineState = {
  phase: 'off',
  rpm: 0,
  pedal: 0,
  throttle: 0,
  rpmRate: 0,
  gear: 'N',
  wheelRpm: 0,
  speedKmh: 0,
  warm: 0,
  coolant: 0.12,
  fuel: 0.62,
  odometerKm: 0,
  roll: 0,
  pitch: 0,
  sinceStart: 0,
  phaseTime: 0,
  limiterCut: 0,
};

type Listener = (phase: Phase) => void;
const listeners = new Set<Listener>();
export function onPhase(fn: Listener) {
  listeners.add(fn);
  return () => void listeners.delete(fn);
}

function setPhase(p: Phase) {
  engine.phase = p;
  engine.phaseTime = 0;
  listeners.forEach((fn) => fn(p));
}

export const CRANK_SECONDS = 1.15;

export function startEngine() {
  if (engine.phase === 'running' || engine.phase === 'cranking') return;
  setPhase('cranking');
}

export function stopEngine() {
  if (engine.phase === 'off' || engine.phase === 'stopping') return;
  setPhase('stopping');
}

export function setPedal(v: number) {
  engine.pedal = Math.min(1, Math.max(0, v));
}

export function setGear(g: 'N' | '1') {
  engine.gear = g;
}

// body springs: natural frequency and damping of the sprung mass on its suspension (approx)
const ROLL_W = 2 * Math.PI * 1.5;
const ROLL_Z = 0.28;
const PITCH_W = 2 * Math.PI * 1.8;
const PITCH_Z = 0.35;
const body = { roll: 0, rollV: 0, pitch: 0, pitchV: 0 };

let t = 0;

export function step(dt: number) {
  dt = Math.min(dt, 0.05);
  t += dt;
  const e = engine;
  e.phaseTime += dt;
  const prevRpm = e.rpm;

  // warm up: fast idle fades over about 40 s of running, the gauge climbs over about 90 s
  if (e.phase === 'running') {
    e.warm = Math.min(1, e.warm + dt / 40);
    e.coolant = Math.min(0.5, e.coolant + dt / 180);
    e.sinceStart += dt;
  } else if (e.phase === 'off') {
    e.coolant = Math.max(0.12, e.coolant - dt / 900);
    e.warm = Math.max(0, e.warm - dt / 600);
  }

  if (e.phase === 'cranking') {
    // starter speed with compression pulses: six cylinders, three firings per turn
    e.rpm = 190 + 45 * Math.sin(t * 2 * Math.PI * 9.5) + 15 * Math.sin(t * 2 * Math.PI * 23);
    e.throttle = 0;
    if (e.phaseTime >= CRANK_SECONDS * (e.warm > 0.5 ? 0.6 : 1)) {
      e.sinceStart = 0;
      setPhase('running');
    }
  } else if (e.phase === 'running') {
    e.throttle += (e.pedal - e.throttle) * Math.min(1, dt * 14);
    if (e.rpm >= LIMIT_RPM) e.limiterCut = 0.07;
    e.limiterCut = Math.max(0, e.limiterCut - dt);
    const thr = e.limiterCut > 0 ? 0 : e.throttle;
    const idle = COLD_IDLE_RPM + (IDLE_RPM - COLD_IDLE_RPM) * e.warm;
    // catch flare after the start, and a little idle hunting
    const flare = 950 * Math.exp(-e.sinceStart / 0.55) * Math.min(1, e.sinceStart * 6);
    const hunt = 14 * Math.sin(t * 2.1) + 9 * Math.sin(t * 5.3);
    const curve = 1 - (1 - thr) * (1 - thr);
    const target = idle + flare + hunt + curve * (LIMIT_RPM + 250 - idle);
    const inertia = e.gear === '1' ? 0.6 : 1;
    const diff = target - e.rpm;
    if (diff > 0) e.rpm += Math.min(diff * 3.2 * inertia * dt, 3600 * inertia * dt);
    else e.rpm += Math.max(diff * 1.7 * dt, -2300 * dt);
  } else if (e.phase === 'stopping') {
    e.throttle = 0;
    e.rpm = Math.max(0, e.rpm - (e.rpm * 2.6 + 260) * dt);
    if (e.rpm < 20) {
      e.rpm = 0;
      setPhase('off');
    }
  } else {
    e.rpm = 0;
    e.throttle = 0;
  }

  e.rpmRate = (e.rpm - prevRpm) / Math.max(dt, 1e-4);

  // first gear on the lift: the wheels turn with the engine
  e.wheelRpm = e.gear === '1' && e.phase === 'running' ? Math.max(0, e.rpm - 900) / (FIRST_GEAR * FINAL_DRIVE) : e.wheelRpm * Math.exp(-dt * 0.8);
  e.speedKmh = (e.wheelRpm * TIRE_CIRCUMFERENCE_M * 60) / 1000;
  e.odometerKm += (e.speedKmh / 3600) * dt;

  // torque reaction: rolls the body when the rpm changes, pitches it a little
  const rollIn = -e.rpmRate * 2.6e-6;
  const pitchIn = e.rpmRate * 0.6e-6;
  body.rollV += (ROLL_W * ROLL_W * (rollIn - body.roll) - 2 * ROLL_Z * ROLL_W * body.rollV) * dt;
  body.roll += body.rollV * dt;
  body.pitchV += (PITCH_W * PITCH_W * (pitchIn - body.pitch) - 2 * PITCH_Z * PITCH_W * body.pitchV) * dt;
  body.pitch += body.pitchV * dt;

  // idle rock: a running engine shakes the body a little, much more just after a cold start
  let rock = 0;
  if (e.phase === 'running') {
    const cold = 1 + 3.2 * Math.exp(-e.sinceStart / 2.2) * (1 - e.warm * 0.7);
    const low = Math.max(0, 1 - (e.rpm - 600) / 1800);
    rock = 0.00045 * cold * (0.35 + low);
  } else if (e.phase === 'cranking') {
    rock = 0.0012;
  } else if (e.phase === 'stopping') {
    rock = 0.0016 * Math.min(1, e.rpm / 300);
  }
  const jitter = Math.sin(t * 2 * Math.PI * 8.7) * 0.6 + Math.sin(t * 2 * Math.PI * 13.3) * 0.4;
  e.roll = body.roll + rock * jitter;
  e.pitch = body.pitch + rock * 0.4 * Math.sin(t * 2 * Math.PI * 11.1);
}

// one loop for everyone
if (typeof window !== 'undefined') {
  // read only view for scripted checks, like window.__garage
  (window as unknown as { __engine: EngineState }).__engine = engine;
  let last = performance.now();
  const loop = (now: number) => {
    // run the real elapsed time in small steps, so slow frames do not slow the engine down;
    // after a long pause (hidden tab) only catch up one second
    let left = Math.min(1, (now - last) / 1000);
    while (left > 0) {
      const dt = Math.min(left, 1 / 60);
      step(dt);
      left -= dt;
    }
    last = now;
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
}
