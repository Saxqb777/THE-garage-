import { engine, IDLE_RPM, onPhase } from './sim';

/**
 * Engine sound (M5), Web Audio only.
 *
 * Six steady RPM loops of an even fire inline six (public/audio/engine_i6, 1100 to 6000 rpm)
 * all play at once. For the current rpm the two nearest loops are crossfaded with equal power
 * and each is pitched to the exact rpm (playbackRate = rpm / loop rpm), so a sweep never
 * steps. Throttle opens a low pass filter and adds level: on throttle sounds bright and hard,
 * off throttle dull. The starter crank is synthesized (a starter whine plus compression pulses
 * at the crank rhythm), because the supplied ignition clip is an already running engine of a
 * different character and would not match the loops.
 *
 * Audio needs a user gesture, so nothing loads until the first Start Engine click.
 */

const LOOPS = [1100, 2000, 3000, 4000, 5000, 6000];

class EngineAudio {
  private ctx: AudioContext | null = null;
  private loading: Promise<void> | null = null;
  private voices: { rpm: number; src: AudioBufferSourceNode; gain: GainNode }[] = [];
  private filter!: BiquadFilterNode;
  private engineGain!: GainNode;
  private master!: GainNode;
  private crank: { stop: () => void } | null = null;
  private raf = 0;
  muted = false;

  /** Loads and wires everything; call from a click or key handler. */
  init() {
    if (this.loading) return this.loading;
    this.loading = this.setup();
    return this.loading;
  }

  private async setup() {
    const ctx = new AudioContext();
    this.ctx = ctx;
    this.master = ctx.createGain();
    this.master.gain.value = this.muted ? 0 : 0.9;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -14;
    comp.ratio.value = 3;
    this.master.connect(comp).connect(ctx.destination);

    this.filter = ctx.createBiquadFilter();
    this.filter.type = 'lowpass';
    this.filter.frequency.value = 1500;
    this.filter.Q.value = 0.6;
    this.engineGain = ctx.createGain();
    this.engineGain.gain.value = 0;
    this.filter.connect(this.engineGain).connect(this.master);

    const buffers = await Promise.all(
      LOOPS.map(async (rpm) => {
        const res = await fetch(`/audio/engine_i6/${rpm}.wav`);
        return ctx.decodeAudioData(await res.arrayBuffer());
      }),
    );
    this.voices = buffers.map((buffer, i) => {
      const src = ctx.createBufferSource();
      src.buffer = buffer;
      src.loop = true;
      const gain = ctx.createGain();
      gain.gain.value = 0;
      src.connect(gain).connect(this.filter);
      // offset starts so the loops do not pulse together
      src.start(0, (i * 0.37) % buffer.duration);
      return { rpm: LOOPS[i], src, gain };
    });

    onPhase((p) => {
      if (p === 'cranking') this.startCrank();
      else this.stopCrank();
    });
    if (engine.phase === 'cranking') this.startCrank();

    const tick = () => {
      this.update();
      this.raf = requestAnimationFrame(tick);
    };
    this.raf = requestAnimationFrame(tick);
  }

  setMuted(m: boolean) {
    this.muted = m;
    if (this.ctx) this.master.gain.setTargetAtTime(m ? 0 : 0.9, this.ctx.currentTime, 0.05);
  }

  /** Follows the engine state every frame. */
  private update() {
    const ctx = this.ctx;
    if (!ctx || !this.voices.length) return;
    const now = ctx.currentTime;
    const tc = 0.025;
    const e = engine;
    const running = e.phase === 'running' || e.phase === 'stopping';
    const rpm = Math.max(e.rpm, 1);

    // which two loops, and how much of each (equal power in log rpm)
    const lr = Math.log(Math.max(rpm, LOOPS[0]));
    let lo = 0;
    while (lo < LOOPS.length - 2 && lr > Math.log(LOOPS[lo + 1])) lo++;
    const a = Math.log(LOOPS[lo]);
    const b = Math.log(LOOPS[lo + 1]);
    const k = Math.min(1, Math.max(0, (lr - a) / (b - a)));
    this.voices.forEach((v, i) => {
      const w = i === lo ? Math.cos((k * Math.PI) / 2) : i === lo + 1 ? Math.sin((k * Math.PI) / 2) : 0;
      v.gain.gain.setTargetAtTime(w, now, tc);
      v.src.playbackRate.setTargetAtTime(Math.min(2, Math.max(0.3, rpm / v.rpm)), now, tc);
    });

    // level and brightness: idle is soft, throttle opens it up; dying engine fades out
    const load = e.throttle;
    const rpmN = Math.min(1, rpm / 5000);
    const level = running ? (0.45 + 0.35 * load + 0.2 * rpmN) * Math.min(1, e.rpm / IDLE_RPM) : 0;
    this.engineGain.gain.setTargetAtTime(level, now, e.phase === 'stopping' ? 0.12 : 0.04);
    this.filter.frequency.setTargetAtTime(900 + 2600 * rpmN + 5200 * load, now, 0.04);
  }

  /** Starter motor: a whine with compression pulses at the crank rhythm. */
  private startCrank() {
    const ctx = this.ctx;
    if (!ctx || this.crank) return;
    const now = ctx.currentTime;
    const out = ctx.createGain();
    out.gain.setValueAtTime(0, now);
    out.gain.linearRampToValueAtTime(0.55, now + 0.08);
    out.connect(this.master);

    const whine = ctx.createOscillator();
    whine.type = 'sawtooth';
    whine.frequency.setValueAtTime(140, now);
    whine.frequency.linearRampToValueAtTime(205, now + 0.5);
    const whineF = ctx.createBiquadFilter();
    whineF.type = 'bandpass';
    whineF.frequency.value = 900;
    whineF.Q.value = 0.8;
    const whineG = ctx.createGain();
    whineG.gain.value = 0.12;
    whine.connect(whineF).connect(whineG).connect(out);

    // compression pulses: low noise chugs, about 9.5 per second
    const len = ctx.sampleRate * 2;
    const noise = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = noise.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    const src = ctx.createBufferSource();
    src.buffer = noise;
    src.loop = true;
    const body = ctx.createBiquadFilter();
    body.type = 'lowpass';
    body.frequency.value = 260;
    const pulse = ctx.createGain();
    pulse.gain.value = 0;
    const lfo = ctx.createOscillator();
    lfo.frequency.value = 9.5;
    const shaper = ctx.createWaveShaper();
    shaper.curve = new Float32Array(Array.from({ length: 64 }, (_, i) => Math.max(0, (i / 63) * 2 - 1) ** 2 * 2.2));
    lfo.connect(shaper).connect(pulse.gain);
    src.connect(body).connect(pulse).connect(out);

    whine.start(now);
    src.start(now);
    lfo.start(now);
    this.crank = {
      stop: () => {
        const t = ctx.currentTime;
        out.gain.cancelScheduledValues(t);
        out.gain.setTargetAtTime(0, t, 0.05);
        [whine, src, lfo].forEach((n) => n.stop(t + 0.4));
      },
    };
  }

  private stopCrank() {
    this.crank?.stop();
    this.crank = null;
  }
}

export const engineAudio = new EngineAudio();
