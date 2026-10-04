import { create } from 'zustand';

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
  setHingesOpen: (open: boolean) => void;
  toggleHinges: () => void;
};

const query = new URLSearchParams(typeof window === 'undefined' ? '' : window.location.search);

export const useGarage = create<GarageState>()((set) => ({
  modelUrl: query.get('model') === 'placeholder' ? PLACEHOLDER_URL : MODEL_URL,
  model: null,
  modelError: null,
  triangles: 0,
  drawCalls: 0,
  loaded: false,
  hingesOpen: query.get('hinges') === 'open',
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
    };
  };
  publish(useGarage.getState());
  useGarage.subscribe(publish);
}
