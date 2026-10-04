import type { Material, Mesh, Object3D } from 'three';

/**
 * Meshes per GLB material name (paint_white, glass_clear, chrome, ...). The names are
 * stable keys from blender/lib/materials.py; M2 swaps in tuned materials through this.
 */
export type MaterialRegistry = Map<string, Mesh[]>;

export function collectMaterials(root: Object3D): MaterialRegistry {
  const registry: MaterialRegistry = new Map();
  root.traverse((o) => {
    const mesh = o as Mesh;
    if (!mesh.isMesh) return;
    for (const material of ([] as Material[]).concat(mesh.material)) {
      const meshes = registry.get(material.name) ?? [];
      if (!meshes.includes(mesh)) meshes.push(mesh);
      registry.set(material.name, meshes);
    }
  });
  return registry;
}
