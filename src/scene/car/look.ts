import {
  Color,
  DoubleSide,
  FrontSide,
  MeshPhysicalMaterial,
  MeshStandardMaterial,
  type Material,
  type Mesh,
  type Object3D,
  type Texture,
  type WebGLProgramParametersWithUniforms,
} from 'three';

/**
 * The look pass (M2): swaps every GLB material for a tuned MeshPhysicalMaterial, by material
 * name. Names are the stable keys from blender/lib/materials.py plus the tex_ keepers from the
 * source model. Paint gets clearcoat and orange peel, glass gets transmission, and every exterior
 * surface gets a little world space dust low down and in the arches, because perfect is fake.
 */

type Tune = Partial<{
  color: string | number;
  roughness: number;
  metalness: number;
  clearcoat: number;
  clearcoatRoughness: number;
  transmission: number;
  ior: number;
  thickness: number;
  sheen: number;
  sheenRoughness: number;
  sheenColor: string;
  envMapIntensity: number;
  emissive: string;
  emissiveIntensity: number;
  transparent: boolean;
  opacity: number;
  dust: number; // 0..1 how much the dust shader may darken and desaturate this surface
  peel: number; // orange peel strength on clearcoat normals
  keepMap: boolean; // keep the GLB's colour texture (tex_ materials)
  side: typeof FrontSide | typeof DoubleSide;
}>;

const PAINT: Tune = { color: '#dcdedc', roughness: 0.3, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.045, envMapIntensity: 1.15, dust: 0.75, peel: 1 };
const TUNES: Record<string, Tune> = {
  paint_white: PAINT,
  tex_paint_white: { ...PAINT, color: '#d9dbd9', keepMap: true },
  tex_side_step: { color: '#d9dbd9', roughness: 0.45, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.12, keepMap: true, dust: 1 },
  plastic_trim_grey: { color: '#3a3d40', roughness: 0.58, metalness: 0, clearcoat: 0.15, clearcoatRoughness: 0.5, dust: 1, sheen: 0.25, sheenRoughness: 0.9, sheenColor: '#777' },
  plastic_black_gloss: { color: '#111214', roughness: 0.22, metalness: 0, clearcoat: 0.8, clearcoatRoughness: 0.1, dust: 0.4 },
  plastic_black_matte: { color: '#17181a', roughness: 0.62, metalness: 0, dust: 0.6, sheen: 0.2, sheenRoughness: 0.9, sheenColor: '#666' },
  rubber_seal: { color: '#0c0c0d', roughness: 0.75, metalness: 0, dust: 0.3 },
  rubber_tire: { color: '#141415', roughness: 0.82, metalness: 0, sheen: 0.45, sheenRoughness: 0.75, sheenColor: '#3a3a3a', dust: 1 },
  alloy_wheel: { color: '#aeb1b4', roughness: 0.42, metalness: 0.95, clearcoat: 0.4, clearcoatRoughness: 0.3, envMapIntensity: 1.1, dust: 0.9 },
  chrome: { color: '#f2f3f5', roughness: 0.07, metalness: 1, envMapIntensity: 1.3 },
  glass_clear: { color: '#eef7f1', roughness: 0.03, metalness: 0, transmission: 1, ior: 1.52, thickness: 0.006, envMapIntensity: 1.2, transparent: true },
  glass_privacy: { color: '#1b2224', roughness: 0.04, metalness: 0, transmission: 0.55, ior: 1.52, thickness: 0.006, envMapIntensity: 1.2, transparent: true },
  lamp_lens_clear: { color: '#f4f6f6', roughness: 0.04, metalness: 0, transmission: 1, ior: 1.49, thickness: 0.004, transparent: true },
  lamp_lens_red: { color: '#b3100c', roughness: 0.08, metalness: 0, transmission: 0.45, ior: 1.49, thickness: 0.004, transparent: true, emissive: '#3a0000', emissiveIntensity: 0.4 },
  lamp_lens_amber: { color: '#e5801a', roughness: 0.08, metalness: 0, transmission: 0.4, ior: 1.49, thickness: 0.004, transparent: true, emissive: '#3a1c00', emissiveIntensity: 0.3 },
  lamp_reflector: { color: '#d8d9da', roughness: 0.14, metalness: 1, envMapIntensity: 1.2 },
  lamp_housing: { color: '#0a0a0a', roughness: 0.5, metalness: 0 },
  tex_lamp_front: { roughness: 0.25, metalness: 0.6, keepMap: true, envMapIntensity: 1.1 },
  tex_lamp_rear: { roughness: 0.25, metalness: 0.4, keepMap: true, envMapIntensity: 1.1 },
  underbody_black: { color: '#121212', roughness: 0.85, metalness: 0.1, dust: 1 },
  body_cavity: { color: '#0a0a0a', roughness: 0.9, metalness: 0 },
  interior_plastic_grey: { color: '#4a4c4f', roughness: 0.62, metalness: 0, sheen: 0.2, sheenRoughness: 0.9, sheenColor: '#888' },
  interior_cloth_grey: { color: '#5c5e5f', roughness: 0.95, metalness: 0, sheen: 0.6, sheenRoughness: 0.8, sheenColor: '#9a9a9a' },
  interior_carpet: { color: '#2a2a2c', roughness: 1, metalness: 0 },
  tex_seat_cloth: { roughness: 0.95, metalness: 0, keepMap: true, sheen: 0.6, sheenRoughness: 0.8, sheenColor: '#9a9a9a' },
  tex_dash: { roughness: 0.65, metalness: 0, keepMap: true },
  tex_interior_detail: { roughness: 0.6, metalness: 0, keepMap: true },
  tex_cluster: { roughness: 0.4, metalness: 0, keepMap: true },
};

// Dust and orange peel live in world space, so no UVs are needed and panels stay continuous.
const DUST_PARS = /* glsl */ `
uniform float uDust;
uniform float uPeel;
varying vec3 vWorldPosDust;
float hash31(vec3 p) { p = fract(p * 0.3183099 + vec3(0.1, 0.2, 0.3)); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
float vnoise(vec3 p) {
  vec3 i = floor(p); vec3 f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(hash31(i), hash31(i + vec3(1,0,0)), f.x), mix(hash31(i + vec3(0,1,0)), hash31(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hash31(i + vec3(0,0,1)), hash31(i + vec3(1,0,1)), f.x), mix(hash31(i + vec3(0,1,1)), hash31(i + vec3(1,1,1)), f.x), f.y), f.z);
}
float fbm(vec3 p) { return 0.5 * vnoise(p) + 0.25 * vnoise(p * 2.03) + 0.125 * vnoise(p * 4.11); }
`;

function withDust(material: MeshPhysicalMaterial, dust: number, peel: number) {
  material.onBeforeCompile = (shader: WebGLProgramParametersWithUniforms) => {
    shader.uniforms.uDust = { value: dust };
    shader.uniforms.uPeel = { value: peel };
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWorldPosDust;')
      .replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvWorldPosDust = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', '#include <common>\n' + DUST_PARS)
      .replace(
        '#include <color_fragment>',
        /* glsl */ `#include <color_fragment>
        {
          // more dust low on the car and in the wheel arches, broken up by two noise scales
          float h = clamp(1.0 - (vWorldPosDust.y - 0.25) / 0.75, 0.0, 1.0);
          float arch = 0.0;
          for (int k = 0; k < 2; k++) {
            float az = k == 0 ? 1.425 : -1.425;
            float d = length(vec2(vWorldPosDust.z - az, vWorldPosDust.y - 0.385));
            arch = max(arch, smoothstep(0.75, 0.45, d) * step(0.42, d));
          }
          // soft, low frequency film of dust: strongest on the sills and arches, barely there higher up
          float n = fbm(vWorldPosDust * 3.5) * 0.7 + fbm(vWorldPosDust * 11.0) * 0.3;
          float dustAmt = uDust * clamp(h * h * 0.18 + arch * 0.22, 0.0, 1.0) * smoothstep(0.3, 0.8, n);
          vec3 dustColor = vec3(0.66, 0.6, 0.5);
          diffuseColor.rgb = mix(diffuseColor.rgb, dustColor * (0.55 + 0.45 * diffuseColor.rgb), dustAmt);
        }`,
      )
      .replace(
        '#include <roughnessmap_fragment>',
        /* glsl */ `#include <roughnessmap_fragment>
        {
          float h = clamp(1.0 - (vWorldPosDust.y - 0.25) / 0.75, 0.0, 1.0);
          float n = fbm(vWorldPosDust * 3.5);
          roughnessFactor = clamp(roughnessFactor + uDust * h * h * 0.12 * smoothstep(0.3, 0.8, n) + uPeel * (fbm(vWorldPosDust * 6.0) - 0.5) * 0.03, 0.02, 1.0);
        }`,
      );
    if (peel > 0) {
      // orange peel: a faint high frequency wobble on the clearcoat normal
      shader.fragmentShader = shader.fragmentShader.replace(
        '#include <clearcoat_normal_fragment_maps>',
        /* glsl */ `#include <clearcoat_normal_fragment_maps>
        {
          vec3 p = vWorldPosDust * 180.0;
          vec3 g = vec3(vnoise(p + vec3(0.37, 0, 0)) - vnoise(p - vec3(0.37, 0, 0)), vnoise(p + vec3(0, 0.37, 0)) - vnoise(p - vec3(0, 0.37, 0)), vnoise(p + vec3(0, 0, 0.37)) - vnoise(p - vec3(0, 0, 0.37)));
          clearcoatNormal = normalize(clearcoatNormal + uPeel * 0.012 * g);
        }`,
      );
    }
  };
  material.customProgramCacheKey = () => `dust${dust.toFixed(2)}peel${peel.toFixed(2)}`;
}

function tuned(src: Material, tune: Tune): MeshPhysicalMaterial {
  const old = src as MeshStandardMaterial & { map?: Texture | null };
  const m = new MeshPhysicalMaterial();
  m.name = src.name;
  if (tune.keepMap && old.map) m.map = old.map;
  m.color = new Color(tune.color ?? '#ffffff');
  m.roughness = tune.roughness ?? 0.5;
  m.metalness = tune.metalness ?? 0;
  m.clearcoat = tune.clearcoat ?? 0;
  m.clearcoatRoughness = tune.clearcoatRoughness ?? 0.1;
  m.transmission = tune.transmission ?? 0;
  m.ior = tune.ior ?? 1.5;
  m.thickness = tune.thickness ?? 0;
  m.sheen = tune.sheen ?? 0;
  m.sheenRoughness = tune.sheenRoughness ?? 1;
  if (tune.sheenColor) m.sheenColor = new Color(tune.sheenColor);
  m.envMapIntensity = tune.envMapIntensity ?? 1;
  if (tune.emissive) {
    m.emissive = new Color(tune.emissive);
    m.emissiveIntensity = tune.emissiveIntensity ?? 1;
  }
  m.transparent = tune.transparent ?? false;
  if (tune.opacity !== undefined) m.opacity = tune.opacity;
  m.side = tune.side ?? FrontSide;
  if (tune.transmission) m.depthWrite = false;
  if (tune.dust || tune.peel) withDust(m, tune.dust ?? 0, tune.peel ?? 0);
  return m;
}

const cache = new WeakMap<Object3D, Map<string, MeshPhysicalMaterial>>();

/** Replace materials in place, once per loaded scene. Unknown names keep the GLB material. */
export function applyLook(root: Object3D) {
  if (cache.has(root)) return;
  const made = new Map<string, MeshPhysicalMaterial>();
  cache.set(root, made);
  root.traverse((o) => {
    const mesh = o as Mesh;
    if (!mesh.isMesh) return;
    const mats = ([] as Material[]).concat(mesh.material);
    const next = mats.map((mat) => {
      const tune = TUNES[mat.name];
      if (!tune) return mat;
      let m = made.get(mat.name);
      if (!m) {
        m = tuned(mat, tune);
        made.set(mat.name, m);
      }
      return m;
    });
    mesh.material = Array.isArray(mesh.material) ? next : next[0];
  });
}

/**
 * Night mode: lamps and the dash glow, decided per part, because front and rear lamps share
 * material names (a reflector is a reflector). Headlamps glow warm white, the rear combination
 * lamps glow red as tail lights (no stop or reverse lamps: the car is parked), the cluster
 * lights up; everything else stays dark. Glowing meshes get a cloned material, so switching off
 * just puts the day material back. Textured lamps use their colour map as the emissive map,
 * which lights the lens pattern instead of a flat slab.
 */
type Glow = {
  emissive: string;
  intensity: number;
  /** Light the colour map's pattern instead of a flat colour. */
  useMap?: boolean;
  /** Only the red parts of the map glow (tail lamp red, not the clear reverse lamp). */
  redOnly?: boolean;
};

const NIGHT_BY_PART: { part: RegExp; glow: Record<string, Glow> }[] = [
  {
    part: /^LIGHT_8101_headlamp_/,
    glow: {
      lamp_reflector: { emissive: '#fff3dc', intensity: 6 },
      lamp_lens_clear: { emissive: '#fff6e4', intensity: 1.6 },
      tex_lamp_front: { emissive: '#fff4e0', intensity: 3.5, useMap: true },
    },
  },
  {
    // the red is painted in the lamp texture under a clear lens
    part: /^LIGHT_8105_rear_combination_lamp_/,
    glow: {
      tex_lamp_rear: { emissive: '#ff2a1c', intensity: 9, useMap: true, redOnly: true },
      lamp_lens_red: { emissive: '#ff1a10', intensity: 7 },
    },
  },
  { part: /.*/, glow: { tex_cluster: { emissive: '#ffd8a6', intensity: 1.4, useMap: true } } },
];

// SYSTEM_GROUPCODE_part_name_side, e.g. LIGHT_8105_rear_combination_lamp_L
const PART_NAME = /^[A-Z]+_\d{4}_[A-Za-z0-9_]+$/;

function partKeyOf(o: Object3D): string {
  for (let p: Object3D | null = o; p; p = p.parent) {
    const name = p.userData.name;
    if (typeof name === 'string' && PART_NAME.test(name)) return name;
  }
  return '';
}

function glowFor(part: string): Record<string, Glow> {
  const out: Record<string, Glow> = {};
  // first matching rule wins per material
  for (const rule of NIGHT_BY_PART) {
    if (!rule.part.test(part)) continue;
    for (const [name, g] of Object.entries(rule.glow)) out[name] ??= g;
  }
  return out;
}

/** Masks the emissive map to its red areas: redness = r minus the larger of g and b. */
function redOnly(m: MeshPhysicalMaterial) {
  m.onBeforeCompile = (shader) => {
    shader.fragmentShader = shader.fragmentShader.replace(
      '#include <emissivemap_fragment>',
      /* glsl */ `
      #ifdef USE_EMISSIVEMAP
        vec4 emissiveColor = texture2D(emissiveMap, vEmissiveMapUv);
        float redness = clamp((emissiveColor.r - max(emissiveColor.g, emissiveColor.b)) * 3.0, 0.0, 1.0);
        totalEmissiveRadiance *= redness * (0.4 + 0.6 * emissiveColor.r);
      #endif`,
    );
  };
  m.customProgramCacheKey = () => 'redOnlyEmissive';
}

const nightMade = new WeakMap<Object3D, Map<string, Material>>();

export function setLights(root: Object3D, on: boolean) {
  let made = nightMade.get(root);
  if (!made) {
    made = new Map();
    nightMade.set(root, made);
  }
  root.traverse((o) => {
    const mesh = o as Mesh;
    if (!mesh.isMesh) return;
    const day = (mesh.userData.dayMaterial ?? mesh.material) as Material | Material[];
    if (!on) {
      if (mesh.userData.dayMaterial) {
        mesh.material = day;
        delete mesh.userData.dayMaterial;
      }
      return;
    }
    const glow = glowFor(partKeyOf(mesh));
    let changed = false;
    const next = ([] as Material[]).concat(day).map((m) => {
      const g = glow[m.name];
      if (!g) return m;
      changed = true;
      const id = `${m.name}|${g.emissive}|${g.intensity}`;
      let n = made.get(id);
      if (!n) {
        const lit = (m as MeshPhysicalMaterial).clone();
        lit.emissive.set(g.emissive);
        lit.emissiveIntensity = g.intensity;
        if (g.useMap && lit.map) lit.emissiveMap = lit.map;
        if (g.redOnly && lit.emissiveMap) redOnly(lit);
        made.set(id, lit);
        n = lit;
      }
      return n;
    });
    if (changed) {
      mesh.userData.dayMaterial = day;
      mesh.material = Array.isArray(day) ? next : next[0];
    }
  });
}
