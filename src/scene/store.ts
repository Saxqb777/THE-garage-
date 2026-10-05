import { create } from 'zustand';
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
  hingesOpen: boolean;
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

const query = new URLSearchParams(typeof window === 'undefined' ? '' : window.location.search);
const initialScene: SceneKey = isSceneKey(query.get('scene')) ? (query.get('scene') as SceneKey) : 'garage';

export const useGarage = create<GarageState>()((set) => ({
  modelUrl: query.get('model') === 'placeholder' ? PLACEHOLDER_URL : MODEL_URL,
  model: null,
  modelError: null,
  triangles: 0,
  drawCalls: 0,
  loaded: false,
  hingesOpen: query.get('hinges') === 'open',
  scene: initialScene,
  targetScene: initialScene,
  setScene: (targetScene) => set({ targetScene }),
  commitScene: (scene) => set({ scene, lightsOn: SCENES[scene].night }),
  timeOfDay: query.has('tod') ? Math.min(1, Math.max(0, Number(query.get('tod')) || 0)) : 0.5,
  setTimeOfDay: (timeOfDay) => set({ timeOfDay }),
  lightsOn: query.get('lights') ? query.get('lights') === 'on' : SCENES[initialScene].night,
  setLightsOn: (lightsOn) => set({ lightsOn }),
  setHingesOpen: (hingesOpen) => set({ hingesOpen }),
  toggleHinges: () => set((s) => ({ hingesOpen: !s.hingesOpen })),
}));

// window.__garage is the read only view that scripts/screenshot.mjs and tests poll.
export type GarageDebug = ModelInfo & {
  loaded: boolean;
  model: string;
  error: string | null;
  triangles: number;
  drawCalls: number;
  hingesOpen: boolean;
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
      scene: s.scene,
      targetScene: s.targetScene,
      timeOfDay: s.timeOfDay,
      lightsOn: s.lightsOn,
    };
  };
  publish(useGarage.getState());
  useGarage.subscribe(publish);
}
