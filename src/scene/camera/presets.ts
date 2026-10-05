import type { PresetKey, Seat } from '../store';

type V3 = [number, number, number];
export type Shot = { position: V3; target: V3; fov: number };

/** Exterior presets in three.js space (car faces +Z, its left side is +X). */
export const SHOTS: Record<Exclude<PresetKey, 'interior' | 'underside'>, Shot> = {
  hero: { position: [5.5, 1.6, 6.0], target: [0, 0.8, 0.2], fov: 35 },
  front: { position: [0.0, 1.25, 7.6], target: [0, 0.85, 0.4], fov: 32 },
  rear: { position: [0.0, 1.45, -7.6], target: [0, 0.9, -0.3], fov: 32 },
  side: { position: [8.6, 1.15, 0.1], target: [0, 0.85, 0.1], fov: 30 },
  // over the opened hood, looking down into the engine bay
  engine: { position: [0.0, 2.9, 4.1], target: [0, 0.95, 1.55], fov: 40 },
};

/**
 * Underside: on the lift (Garage), crouched beside the raised car looking up at the floor pan
 * (absolute positions, already for the car at full lift height); elsewhere a ground level look.
 */
export const UNDER_LIFTED: Shot = { position: [3.1, 0.45, 2.7], target: [0, 1.62, -0.15], fov: 50 };
export const UNDER_GROUND: Shot = { position: [2.6, 0.2, 0.7], target: [0, 0.42, 0.0], fov: 45 };

/**
 * Seats. `door` is the hinged part the camera passes through, `approach` the shot just outside
 * that door, `eye` where the head is and `look` a far point straight ahead.
 */
export const SEATS: Record<Seat, { door: string; approach: Shot; eye: V3; look: V3; fov: number }> = {
  driver: {
    door: 'DOOR_6751_front_door_L',
    approach: { position: [2.35, 1.55, 0.2], target: [0.45, 1.35, 0.25], fov: 40 },
    eye: [0.45, 1.5, -0.14],
    look: [0.2, 1.02, 2.8],
    fov: 62,
  },
  rear: {
    door: 'DOOR_6755_rear_door_L',
    approach: { position: [2.35, 1.55, -0.6], target: [0.4, 1.35, -0.6], fov: 40 },
    eye: [0.12, 1.5, -0.98],
    look: [0.0, 1.05, 3.0],
    fov: 66,
  },
};
