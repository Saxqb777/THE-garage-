import { create } from 'zustand';
import type { CatalogPart } from '@/data/catalog';
import { SCENES, isSceneKey, type SceneKey } from './scenes';

export const MODEL_URL = '/models/lc100.glb';
export const PLACEHOLDER_URL = '/models/lc100_placeholder.glb';

export type ModelInfo = {
  partKeys: string[];
  meshCount: number;
  materials: string[];
  /** In the GLB but not in the contract. */
  unknownKeys: string[];
  /** In the contract but not in the GLB (yet). */
  missingKeys: string[];
};

type GarageState = {
  modelUrl: string;
  model: ModelInfo | null;
  modelError: string | null;
  triangles: number;
  drawCalls: number;
  /** Model indexed and rendered at least once. */
  loaded: boolean;
  /** Any hinged part open (drives the Open all / Close all buttons). */
  hingesOpen: boolean;
  /** Hinged parts in the model on screen, and which of them are open. */
  hingeKeys: string[];
  open: Record<string, boolean>;
  setHingeKeys: (keys: string[]) => void;
  togglePart: (key: string) => void;
  /** Part under the pointer, and the part whose card is open. */
  hovered: string | null;
  setHovered: (key: string | null) => void;
  selected: string | null;
  select: (key: string | null) => void;
  /** Set one hinged part open or closed (camera presets use it). */
  setPartOpen: (key: string, open: boolean) => void;
  /** Camera: outside orbiting the car, or seated in the cabin. Requests are queued for CameraRig. */
  view: 'exterior' | 'cabin';
  seat: Seat | null;
  camBusy: boolean;
  camRequest: CamRequest | null;
  requestCam: (r: CamRequestInput) => void;
  /** Two post lift (Garage only). */
  lift: boolean;
  setLift: (on: boolean) => void;
  /** X Ray: body, doors, glass and lamps turn to ghost glass. */
  xray: boolean;
  setXray: (on: boolean) => void;
  /**
   * Explode (M6). Level 1: the systems separate. Level 2: one system's assemblies spread.
   * Level 3: one assembly's parts spread. Serialised in the URL as ?x=all, ?x=SYSTEM or
   * ?x=ASSEMBLY_KEY, so a link can open the car already apart.
   */
  explode: ExplodeState;
  /** Bumps when the explode rig is (re)built, so UI that reads it re-renders. */
  rigVersion: number;
  explodeAll: () => void;
  focusSystem: (system: string) => void;
  focusAssembly: (key: string) => void;
  explodeUp: () => void;
  assemble: () => void;
  /** Parts catalogue from /api/parts (M7), keyed by part key. */
  catalog: Map<string, CatalogPart> | null;
  catalogSource: 'neon' | 'seed' | null;
  /** Service layer: highlight the parts due at this many km, or off. */
  service: number | null;
  setService: (km: number | null) => void;
  /** The scene on screen. */
  scene: SceneKey;
  /** The scene asked for; it replaces `scene` once its sky has loaded (SceneSwap). */
  targetScene: SceneKey;
  setScene: (scene: SceneKey) => void;
  commitScene: (scene: SceneKey) => void;
  /** 0 dawn, 0.5 as shot, 1 dusk. */
  timeOfDay: number;
  setTimeOfDay: (t: number) => void;
  /** Headlights, tail lights and dash on. Follows the scene unless the user overrides it. */
  lightsOn: boolean;
  setLightsOn: (on: boolean) => void;
  setHingesOpen: (open: boolean) => void;
  toggleHinges: () => void;
};

export type ExplodeState = { level: 0 | 1 | 2 | 3; system: string | null; assembly: string | null };

export type Seat = 'driver' | 'rear';
export type PresetKey = 'hero' | 'front' | 'rear' | 'side' | 'engine' | 'interior' | 'underside';
export type CamRequest =
  | { id: number; action: 'preset'; preset: PresetKey }
  | { id: number; action: 'getIn'; seat: Seat }
  | { id: number; action: 'getOut' }
  /** Fit a world space box (three.js metres) in view, keeping the current direction. */
  | { id: number; action: 'frame'; min: [number, number, number]; max: [number, number, number] };

// without the id, per variant (a plain Omit would collapse the union)
export type CamRequestInput = CamRequest extends infer R ? (R extends CamRequest ? Omit<R, 'id'> : never) : never;

let camRequestId = 0;

const query = new URLSearchParams(typeof window === 'undefined' ? '' : window.location.search);
const initialScene: SceneKey = isSceneKey(query.get('scene')) ? (query.get('scene') as SceneKey) : 'garage';

const ASSEMBLED: ExplodeState = { level: 0, system: null, assembly: null };

/** ?x=all, ?x=DOOR or ?x=DOOR_6751_front_door_L */
function explodeFromParam(x: string | null): ExplodeState {
  if (!x) return ASSEMBLED;
  if (x === 'all') return { level: 1, system: null, assembly: null };
  if (/^[A-Z]+$/.test(x)) return { level: 2, system: x, assembly: null };
  if (/^[A-Z]+_\d{4}_/.test(x)) return { level: 3, system: x.split('_')[0], assembly: x };
  return ASSEMBLED;
}

export function explodeParam(x: ExplodeState) {
  return x.level === 0 ? null : x.level === 1 ? 'all' : x.level === 2 ? x.system : x.assembly;
}

export const useGarage = create<GarageState>()((set) => ({
  modelUrl: query.get('model') === 'placeholder' ? PLACEHOLDER_URL : MODEL_URL,
  model: null,
  modelError: null,
  triangles: 0,
  drawCalls: 0,
  loaded: false,
  hingesOpen: false,
  hingeKeys: [],
  open: {},
  // ?hinges=open opens everything as soon as the model reports its hinges
  setHingeKeys: (hingeKeys) => set(() => withOpen(hingeKeys, Object.fromEntries(hingeKeys.map((k) => [k, query.get('hinges') === 'open'])))),
  togglePart: (key) => set((s) => withOpen(s.hingeKeys, { ...s.open, [key]: !s.open[key] })),
  setPartOpen: (key, value) => set((s) => (s.open[key] === value ? {} : withOpen(s.hingeKeys, { ...s.open, [key]: value }))),
  view: 'exterior',
  seat: null,
  camBusy: false,
  camRequest: null,
  requestCam: (r) => set({ camRequest: { ...r, id: ++camRequestId } as CamRequest }),
  lift: false,
  setLift: (lift) => set({ lift }),
  hovered: null,
  setHovered: (hovered) => set({ hovered }),
  selected: query.get('part'),
  select: (selected) => set({ selected }),
  xray: query.get('xray') === '1',
  setXray: (xray) => set({ xray }),
  explode: explodeFromParam(query.get('x')),
  rigVersion: 0,
  // flying apart happens with the doors shut, the car on the ground and nobody inside
  explodeAll: () =>
    set((s) => {
      if (s.view === 'cabin') s.requestCam({ action: 'getOut' });
      return { explode: { level: 1, system: null, assembly: null }, lift: false, ...withOpen(s.hingeKeys, Object.fromEntries(s.hingeKeys.map((k) => [k, false]))) };
    }),
  focusSystem: (system) => set((s) => ({ explode: { level: 2, system, assembly: null }, lift: false, ...(s.explode.level === 0 ? withOpen(s.hingeKeys, {}) : {}) })),
  focusAssembly: (key) => set((s) => ({ explode: { level: 3, system: key.split('_')[0], assembly: key }, lift: false, ...(s.explode.level === 0 ? withOpen(s.hingeKeys, {}) : {}) })),
  explodeUp: () =>
    set((s) => {
      const x = s.explode;
      if (x.level === 3) return { explode: { level: 2, system: x.system, assembly: null } };
      if (x.level === 2) return { explode: { level: 1, system: null, assembly: null } };
      return { explode: ASSEMBLED };
    }),
  assemble: () => set({ explode: ASSEMBLED }),
  catalog: null,
  catalogSource: null,
  service: null,
  setService: (service) => set((s) => ({ service, xray: service ? true : s.xray })),
  scene: initialScene,
  targetScene: initialScene,
  setScene: (targetScene) => set({ targetScene }),
  // the lift lives in the garage: leaving it lowers the car
  commitScene: (scene) => set((s) => ({ scene, lightsOn: SCENES[scene].night, lift: scene === 'garage' ? s.lift : false })),
  timeOfDay: query.has('tod') ? Math.min(1, Math.max(0, Number(query.get('tod')) || 0)) : 0.5,
  setTimeOfDay: (timeOfDay) => set({ timeOfDay }),
  lightsOn: query.get('lights') ? query.get('lights') === 'on' : SCENES[initialScene].night,
  setLightsOn: (lightsOn) => set({ lightsOn }),
  setHingesOpen: (all) => set((s) => withOpen(s.hingeKeys, Object.fromEntries(s.hingeKeys.map((k) => [k, all])))),
  toggleHinges: () => set((s) => withOpen(s.hingeKeys, Object.fromEntries(s.hingeKeys.map((k) => [k, !s.hingesOpen])))),
}));

function withOpen(hingeKeys: string[], open: Record<string, boolean>) {
  return { hingeKeys, open, hingesOpen: hingeKeys.some((k) => open[k]) };
}

// window.__garage is the read only view that scripts/screenshot.mjs and tests poll.
export type GarageDebug = ModelInfo & {
  loaded: boolean;
  model: string;
  error: string | null;
  triangles: number;
  drawCalls: number;
  hingesOpen: boolean;
  open: string[];
  selected: string | null;
  xray: boolean;
  explode: ExplodeState;
  service: number | null;
  catalogSource: 'neon' | 'seed' | null;
  catalogSize: number;
  view: 'exterior' | 'cabin';
  lift: boolean;
  camBusy: boolean;
  scene: SceneKey;
  targetScene: SceneKey;
  timeOfDay: number;
  lightsOn: boolean;
};

declare global {
  interface Window {
    __garage?: GarageDebug;
  }
}

if (typeof window !== 'undefined') {
  const publish = (s: GarageState) => {
    window.__garage = {
      loaded: s.loaded,
      model: s.modelUrl,
      error: s.modelError,
      partKeys: s.model?.partKeys ?? [],
      meshCount: s.model?.meshCount ?? 0,
      triangles: s.triangles,
      drawCalls: s.drawCalls,
      materials: s.model?.materials ?? [],
      unknownKeys: s.model?.unknownKeys ?? [],
      missingKeys: s.model?.missingKeys ?? [],
      hingesOpen: s.hingesOpen,
      open: Object.keys(s.open).filter((k) => s.open[k]),
      selected: s.selected,
      xray: s.xray,
      explode: s.explode,
      service: s.service,
      catalogSource: s.catalogSource,
      catalogSize: s.catalog?.size ?? 0,
      view: s.view,
      lift: s.lift,
      camBusy: s.camBusy,
      scene: s.scene,
      targetScene: s.targetScene,
      timeOfDay: s.timeOfDay,
      lightsOn: s.lightsOn,
    };
  };
  publish(useGarage.getState());
  useGarage.subscribe(publish);

  // The address bar follows the state that is worth sharing (scene, explode, part, x ray), so
  // the current URL is always a deep link. Other params (camera overrides, debug) are kept.
  const syncUrl = (s: GarageState) => {
    const url = new URL(window.location.href);
    const p = url.searchParams;
    const put = (k: string, v: string | null) => (v ? p.set(k, v) : p.delete(k));
    put('scene', s.targetScene === 'garage' ? null : s.targetScene);
    put('x', explodeParam(s.explode));
    put('part', s.selected);
    put('xray', s.xray ? '1' : null);
    const q = p.toString();
    const next = `${url.pathname}${q ? `?${q}` : ''}${url.hash}`;
    if (next !== `${window.location.pathname}${window.location.search}${window.location.hash}`) window.history.replaceState(null, '', next);
  };
  useGarage.subscribe(syncUrl);
}
