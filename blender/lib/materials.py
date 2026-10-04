"""Material library. Every mesh uses one of these keys as its material name.

The web app looks materials up by these exact names and may swap in tuned
three.js MeshPhysicalMaterial versions (M2), so keep names stable.
Values are a sensible first pass that also export cleanly to glTF
(clearcoat, transmission, IOR and emission all survive the exporter).
"""
import bpy

# key: (base colour linear RGB, metallic, roughness, extra settings)
LIBRARY = {
    "paint_white": ((0.86, 0.865, 0.86), 0.0, 0.32, {"coat": 1.0, "coat_roughness": 0.04}),
    "plastic_trim_grey": ((0.045, 0.05, 0.053), 0.0, 0.62, {}),
    "plastic_black_gloss": ((0.012, 0.012, 0.013), 0.0, 0.22, {}),
    "plastic_black_matte": ((0.018, 0.018, 0.019), 0.0, 0.55, {}),
    "rubber_seal": ((0.01, 0.01, 0.01), 0.0, 0.7, {}),
    "rubber_tire": ((0.018, 0.018, 0.018), 0.0, 0.85, {}),
    "alloy_wheel": ((0.62, 0.63, 0.64), 1.0, 0.28, {}),
    "chrome": ((0.92, 0.92, 0.93), 1.0, 0.05, {}),
    "glass_clear": ((0.9, 0.97, 0.93), 0.0, 0.02, {"transmission": 1.0, "ior": 1.52}),
    "glass_privacy": ((0.08, 0.1, 0.1), 0.0, 0.02, {"transmission": 1.0, "ior": 1.52}),
    "lamp_lens_clear": ((0.95, 0.95, 0.95), 0.0, 0.02, {"transmission": 1.0, "ior": 1.49}),
    "lamp_lens_red": ((0.55, 0.01, 0.01), 0.0, 0.05, {"transmission": 0.85, "ior": 1.49}),
    "lamp_lens_amber": ((0.9, 0.35, 0.01), 0.0, 0.05, {"transmission": 0.85, "ior": 1.49}),
    "lamp_reflector": ((0.85, 0.85, 0.86), 1.0, 0.12, {}),
    "lamp_housing": ((0.02, 0.02, 0.02), 0.0, 0.5, {}),
    "body_cavity": ((0.015, 0.015, 0.016), 0.0, 0.8, {}),
    "underbody_black": ((0.02, 0.02, 0.021), 0.2, 0.7, {}),
    "interior_plastic_grey": ((0.11, 0.115, 0.12), 0.0, 0.6, {}),
    "interior_cloth_grey": ((0.22, 0.225, 0.225), 0.0, 0.95, {}),
    "interior_carpet": ((0.05, 0.05, 0.055), 0.0, 1.0, {}),
    "emissive_dial": ((0.02, 0.02, 0.02), 0.0, 0.4, {}),
}


def get(key):
    """Return the material for `key`, creating it on first use."""
    if key not in LIBRARY:
        raise KeyError(f"unknown material key {key!r}; add it to blender/lib/materials.py")
    mat = bpy.data.materials.get(key)
    if mat is not None:
        return mat
    base, metallic, roughness, extra = LIBRARY[key]
    mat = bpy.data.materials.new(key)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if "coat" in extra:
        bsdf.inputs["Coat Weight"].default_value = extra["coat"]
        bsdf.inputs["Coat Roughness"].default_value = extra["coat_roughness"]
    if "transmission" in extra:
        bsdf.inputs["Transmission Weight"].default_value = extra["transmission"]
    if "ior" in extra:
        bsdf.inputs["IOR"].default_value = extra["ior"]
    mat.diffuse_color = (*base, 1.0)
    return mat


def assign(obj, key):
    """Give `obj` a single material slot holding material `key`."""
    obj.data.materials.clear()
    obj.data.materials.append(get(key))
