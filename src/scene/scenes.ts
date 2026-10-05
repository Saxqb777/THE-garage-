/**
 * The four environments (plus the spare desert road) as data. Everything scene specific lives
 * here: which HDRI, how it is projected onto the ground, where its sun is, what the floor is
 * made of and whether the car's lights are on. Lighting, Ground and the HUD only read this.
 *
 * Sun directions are unit vectors in the HDRI's own frame, measured from its brightest pixels;
 * the scene yaw turns them with the sky, so the cast shadow lands where the photo says it should.
 * Yaws: corniche puts the skyline behind the car in the hero view, desert road and highway lay
 * the road along the car, dunes moves the sun off the camera axis so the body gets modelling.
 */
export type SceneKey = 'garage' | 'dunes' | 'desert_road' | 'corniche_night' | 'highway';

export type Floor = 'hdri' | 'wet';

export type SceneDef = {
  key: SceneKey;
  label: string;
  hint: string;
  /** Poly Haven name, files are public/hdri/{name}_{1k,2k}.hdr */
  hdri: string;
  /**
   * Ground projection: camera height when the HDRI was shot, flat floor radius, and optionally
   * where on the floor it was shot (world x, z) so the car can stand somewhere else, e.g. in a
   * lane instead of on the median the photographer stood on.
   */
  ground: { height: number; radius: number; offset?: [number, number] };
  /** Turns the sky around the car (radians, three.js environmentRotation convention). */
  yaw: number;
  /** Sun as a unit direction towards the light. Null for scenes without a sun. */
  sun: [number, number, number] | null;
  sunColor: string;
  sunIntensity: number;
  /** How soft the sun shadow is: 0 crisp, 1 overcast. */
  sunSoftness: number;
  envIntensity: number;
  backgroundIntensity: number;
  /** Bloom strength and the linear luminance it starts at. Night needs a high threshold. */
  bloom: { intensity: number; threshold: number };
  floor: Floor;
  shadowColor: string;
  /** Strength of the baked parked shadow and of the live sun shadow. */
  aoOpacity: number;
  sunShadowOpacity: number;
  night: boolean;
  /** Time of day slider meaningful for this HDRI. */
  timeOfDay: boolean;
  /** Studio softboxes rendered into the reflection map (garage only). */
  lightformers: boolean;
};

export const SCENES: Record<SceneKey, SceneDef> = {
  garage: {
    key: 'garage',
    label: 'Garage',
    hint: 'Workshop, studio light',
    hdri: 'autoshop_01',
    ground: { height: 1.55, radius: 12 },
    yaw: 0,
    sun: null,
    sunColor: '#ffffff',
    sunIntensity: 0,
    sunSoftness: 1,
    envIntensity: 1,
    backgroundIntensity: 1,
    bloom: { intensity: 0.35, threshold: 1.0 },
    floor: 'hdri',
    shadowColor: '#1a1c22',
    aoOpacity: 0.95,
    sunShadowOpacity: 0,
    night: false,
    timeOfDay: false,
    lightformers: true,
  },
  dunes: {
    key: 'dunes',
    label: 'Liwa Dunes',
    hint: 'Sand, hard sun',
    hdri: 'goegap',
    ground: { height: 1.6, radius: 80 },
    yaw: -1.08,
    sun: [0.535, 0.726, 0.433],
    sunColor: '#fff1dc',
    sunIntensity: 3.2,
    sunSoftness: 0.08,
    envIntensity: 1,
    backgroundIntensity: 1,
    bloom: { intensity: 0.3, threshold: 1.2 },
    floor: 'hdri',
    shadowColor: '#4a3a2a',
    aoOpacity: 0.7,
    sunShadowOpacity: 0.55,
    night: false,
    timeOfDay: true,
    lightformers: false,
  },
  desert_road: {
    key: 'desert_road',
    label: 'Desert Road',
    hint: 'The drive to Liwa',
    hdri: 'nowhere_road',
    ground: { height: 1.6, radius: 80 },
    yaw: Math.PI / 2,
    sun: [0.179, 0.975, 0.131],
    sunColor: '#fff6e8',
    sunIntensity: 3.4,
    sunSoftness: 0.06,
    envIntensity: 1,
    backgroundIntensity: 1,
    bloom: { intensity: 0.3, threshold: 1.2 },
    floor: 'hdri',
    shadowColor: '#3a3430',
    aoOpacity: 0.7,
    sunShadowOpacity: 0.6,
    night: false,
    timeOfDay: true,
    lightformers: false,
  },
  corniche_night: {
    key: 'corniche_night',
    label: 'Corniche Night',
    hint: 'Wet road, city lights',
    hdri: 'shanghai_bund',
    ground: { height: 1.6, radius: 60 },
    yaw: Math.PI,
    sun: null,
    sunColor: '#ffffff',
    sunIntensity: 0,
    sunSoftness: 1,
    envIntensity: 0.55,
    backgroundIntensity: 0.55,
    bloom: { intensity: 0.25, threshold: 5 },
    floor: 'wet',
    shadowColor: '#06070c',
    aoOpacity: 0.9,
    sunShadowOpacity: 0,
    night: true,
    timeOfDay: false,
    lightformers: false,
  },
  highway: {
    key: 'highway',
    label: 'Sheikh Zayed Road',
    hint: 'Freeway, golden hour',
    hdri: 'highway_bridge_sunset',
    ground: { height: 1.7, radius: 60, offset: [3.6, 0] },
    yaw: 1.26,
    sun: [0.899, 0.141, 0.416],
    sunColor: '#ffb469',
    sunIntensity: 2.6,
    sunSoftness: 0.15,
    envIntensity: 1,
    backgroundIntensity: 1,
    bloom: { intensity: 0.35, threshold: 1.0 },
    floor: 'hdri',
    shadowColor: '#2a2230',
    aoOpacity: 0.75,
    sunShadowOpacity: 0.4,
    night: false,
    timeOfDay: true,
    lightformers: false,
  },
};

export const SCENE_ORDER: SceneKey[] = ['garage', 'dunes', 'corniche_night', 'highway', 'desert_road'];

export function isSceneKey(v: unknown): v is SceneKey {
  return typeof v === 'string' && v in SCENES;
}

const lowRes = typeof window !== 'undefined' && window.devicePixelRatio < 1.5 && window.innerWidth < 900;

export function hdriUrl(scene: SceneDef) {
  return `/hdri/${scene.hdri}_${lowRes ? '1k' : '2k'}.hdr`;
}

/**
 * Time of day, 0 dawn to 1 dusk with 0.5 the HDRI as shot. Only exposure, warmth and the
 * sun's height move: the sky itself is a photo. Returns multipliers for Lighting.
 */
export function timeOfDayLook(scene: SceneDef, t: number) {
  if (!scene.timeOfDay) return { exposure: 1, warmth: 0, sunElevationScale: 1, sunIntensityScale: 1 };
  const edge = Math.abs(t - 0.5) * 2; // 0 midday, 1 at either end
  return {
    exposure: 1 - 0.55 * edge * edge,
    warmth: 0.75 * edge * edge,
    sunElevationScale: 1 - 0.8 * edge,
    sunIntensityScale: 1 - 0.5 * edge,
  };
}

/** The sun after the scene yaw, as a world direction. */
export function worldSun(scene: SceneDef): [number, number, number] | null {
  if (!scene.sun) return null;
  const [x, y, z] = scene.sun;
  const c = Math.cos(scene.yaw);
  const s = Math.sin(scene.yaw);
  return [x * c + z * s, y, -x * s + z * c];
}
