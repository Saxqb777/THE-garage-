import type { Mesh, Object3D } from 'three';
import contractJson from '@/data/parts.m1.json';
import { collectMaterials } from './materials';

export type Hinge = { axis: [number, number, number]; openDeg: number };

export type ContractPart = {
  key: string;
  system: string;
  groupCode: string;
  groupStatus: string;
  nameEn: string;
  parent: string | null;
  kind: 'mesh' | 'assembly';
  hinge?: Hinge;
};

export const contract = contractJson as {
  version: number;
  vehicle: { key: string; name: string };
  parts: ContractPart[];
};

export const CONTRACT_PARTS = new Map(contract.parts.map((p) => [p.key, p]));

const SYSTEMS = 'BODY|DOOR|GLASS|WHEEL|SUSP|BRAKE|ENG|COOL|EXH|TRANS|DRIVE|ELEC|INT|AC|LIGHT|TRIM';
export const PART_KEY_RE = new RegExp(`^(${SYSTEMS})_(\\d{4})_([a-z0-9]+(?:_[a-z0-9]+)*?)(?:_(L|R|F|RR))?$`);
const LOOKS_LIKE_PART_RE = new RegExp(`^(${SYSTEMS})_`);

export type PartNode = {
  key: string;
  system: string;
  object: Object3D;
  parentKey: string | null;
  type: 'mesh' | 'group';
  hinge: Hinge | null;
};

export type ModelInspection = {
  parts: Map<string, PartNode>;
  meshCount: number;
  materials: string[];
  unknownKeys: string[];
  missingKeys: string[];
  malformed: string[];
  duplicates: string[];
};

function isMesh(o: Object3D): o is Mesh {
  return (o as Mesh).isMesh === true;
}

/** Hinge from the node extras, falling back to the contract. */
function hingeOf(o: Object3D, key: string): Hinge | null {
  const { hingeAxis, openDeg } = o.userData;
  if (Array.isArray(hingeAxis) && hingeAxis.length === 3 && typeof openDeg === 'number') {
    return { axis: hingeAxis as Hinge['axis'], openDeg };
  }
  return CONTRACT_PARTS.get(key)?.hinge ?? null;
}

/** Finds every part node in a loaded GLB by name, anywhere in the tree, and checks it against the contract. */
export function inspectModel(root: Object3D): ModelInspection {
  const parts = new Map<string, PartNode>();
  const keyOf = new Map<Object3D, string>();
  const malformed: string[] = [];
  const duplicates: string[] = [];
  let meshCount = 0;

  root.traverse((o) => {
    if (isMesh(o)) meshCount++;
    // GLTFLoader keeps the glTF node name in userData.name. The meshes it splits out of a
    // multi material node have no node name of their own (and may reuse it with a suffix).
    const key = o.userData.name;
    if (typeof key !== 'string') return;
    const match = PART_KEY_RE.exec(key);
    if (!match) {
      if (LOOKS_LIKE_PART_RE.test(key)) malformed.push(key);
      return;
    }
    if (parts.has(key)) {
      duplicates.push(key);
      return;
    }
    let parent = o.parent;
    while (parent && !keyOf.has(parent)) parent = parent.parent;
    parts.set(key, {
      key,
      system: match[1],
      object: o,
      parentKey: parent ? keyOf.get(parent)! : null,
      type: isMesh(o) ? 'mesh' : 'group',
      hinge: hingeOf(o, key),
    });
    keyOf.set(o, key);
  });

  return {
    parts,
    meshCount,
    materials: [...collectMaterials(root).keys()].sort(),
    unknownKeys: [...parts.keys()].filter((k) => !CONTRACT_PARTS.has(k)),
    missingKeys: [...CONTRACT_PARTS.keys()].filter((k) => !parts.has(k)),
    malformed,
    duplicates,
  };
}

const logged = new WeakSet<Object3D>();

/** Console report for a freshly loaded model (once per scene, StrictMode mounts twice). */
export function logModel(url: string, root: Object3D, info: ModelInspection) {
  if (logged.has(root)) return;
  logged.add(root);

  const rows = [...info.parts.values()].map((p) => ({
    key: p.key,
    system: p.system,
    parent: p.parentKey ?? '',
    type: p.type,
    hinge: p.hinge ? `${p.hinge.openDeg} deg` : '',
  }));
  const perSystem: Record<string, number> = {};
  for (const r of rows) perSystem[r.system] = (perSystem[r.system] ?? 0) + 1;
  const groups = rows.filter((r) => r.type === 'group').length;
  const covered = CONTRACT_PARTS.size - info.missingKeys.length;

  console.info(
    `[garage] ${url}: ${rows.length} parts (${rows.length - groups} meshes, ${groups} groups), ` +
      `${info.meshCount} three.js meshes, ${covered}/${CONTRACT_PARTS.size} contract keys`,
  );
  console.table(rows);
  console.info('[garage] parts per system', perSystem);
  console.info(`[garage] ${info.materials.length} materials`, info.materials);

  if (info.unknownKeys.length) {
    console.warn(`[garage] ${info.unknownKeys.length} part keys in the GLB are not in the contract`, info.unknownKeys);
  }
  if (info.malformed.length) {
    console.warn('[garage] node names that look like part keys but break the naming pattern', info.malformed);
  }
  if (info.duplicates.length) console.warn('[garage] duplicate part nodes', info.duplicates);
  const misparented = rows.filter((r) => {
    const expected = CONTRACT_PARTS.get(r.key)?.parent;
    return expected !== undefined && (expected ?? '') !== r.parent;
  });
  if (misparented.length) {
    console.warn(
      '[garage] parts parented differently from the contract',
      misparented.map((r) => `${r.key} under ${r.parent || 'root'}, expected ${CONTRACT_PARTS.get(r.key)?.parent ?? 'root'}`),
    );
  }
  if (info.missingKeys.length) {
    console.info(`[garage] ${info.missingKeys.length} contract parts are not in this model yet`, info.missingKeys);
  }
}

/** Shadows on for every mesh in the model. */
export function enableShadows(root: Object3D) {
  root.traverse((o) => {
    if (isMesh(o)) o.castShadow = o.receiveShadow = true;
  });
}
