'use client';

import { useMemo } from 'react';
import { useEnvironment } from '@react-three/drei';
import { BackSide, Matrix3, type Texture } from 'three';

/**
 * Ground projected HDRI backdrop, after three-stdlib's GroundProjectedEnv, plus a yaw so each
 * scene can turn its sky (skyline behind the car, road along the car) and an intensity for
 * the time of day slider. The flat floor sits at world y = 0; `height` is the camera height the
 * HDRI was shot from, `radius` how far the flat floor reaches. The dome mesh only has to enclose
 * the camera and stay inside the far plane: the projection is computed per view ray.
 *
 * The yaw matches three's scene.environmentRotation convention: HDRI content seen from
 * direction h appears in the world at Ry(yaw) h, so reflections and backdrop agree.
 */

// inside the camera's far plane (100) and well outside the orbit limit (14)
const DOME_SIZE = 80;

export default function SkyDome({
  file,
  height,
  radius,
  offset = [0, 0],
  yaw,
  intensity,
}: {
  file: string;
  height: number;
  radius: number;
  /** Where the HDRI was shot from on the floor (world x, z), when the car should not stand on that spot. */
  offset?: [number, number];
  yaw: number;
  intensity: number;
}) {
  const map = useEnvironment({ files: file }) as Texture;

  // constructor parameters, stable for the life of the dome
  const params = useMemo(
    () => ({
      uniforms: {
        map: { value: null },
        height: { value: 1.6 },
        radius: { value: 60 },
        intensity: { value: 1 },
        rotation: { value: new Matrix3() },
        offset: { value: [0, 0] },
      },
      vertexShader: VERTEX,
      fragmentShader: FRAGMENT,
    }),
    [],
  );

  // transpose of Ry(yaw) = Ry(-yaw): world direction to HDRI direction
  const rotation = useMemo(() => {
    const c = Math.cos(yaw);
    const s = Math.sin(yaw);
    return new Matrix3().set(c, 0, -s, 0, 1, 0, s, 0, c);
  }, [yaw]);

  return (
    <mesh scale={DOME_SIZE} renderOrder={-1000} frustumCulled={false}>
      <icosahedronGeometry args={[1, 16]} />
      <shaderMaterial
        args={[params]}
        side={BackSide}
        depthWrite={false}
        uniforms-map-value={map}
        uniforms-height-value={height}
        uniforms-radius-value={radius}
        uniforms-intensity-value={intensity}
        uniforms-rotation-value={rotation}
        uniforms-offset-value={offset}
      />
    </mesh>
  );
}

const VERTEX = /* glsl */ `
  varying vec3 vWorldPosition;
  void main() {
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    vWorldPosition = worldPosition.xyz;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }`;

const FRAGMENT = /* glsl */ `
  varying vec3 vWorldPosition;
  uniform sampler2D map;
  uniform float radius;
  uniform float height;
  uniform float intensity;
  uniform mat3 rotation;
  uniform vec2 offset;

  float diskIntersectWithBackFaceCulling(vec3 ro, vec3 rd, vec3 c, vec3 n, float r) {
    float d = dot(rd, n);
    if (d > 0.0) return 1e6;
    vec3 o = ro - c;
    float t = -dot(n, o) / d;
    vec3 q = o + rd * t;
    return (dot(q, q) < r * r) ? t : 1e6;
  }

  float sphereIntersect(vec3 ro, vec3 rd, vec3 ce, float ra) {
    vec3 oc = ro - ce;
    float b = dot(oc, rd);
    float c = dot(oc, oc) - ra * ra;
    float h = b * b - c;
    if (h < 0.0) return -1.0;
    return -b + sqrt(h);
  }

  vec3 project() {
    // the true view ray (three-stdlib uses the direction from the origin, which only works
    // with a dome far larger than the camera's far plane allows)
    vec3 p = normalize(vWorldPosition - cameraPosition);
    vec3 camPos = cameraPosition - vec3(offset.x, height, offset.y);
    float intersection = sphereIntersect(camPos, p, vec3(0.0), radius);
    if (intersection > 0.0) {
      vec3 h = vec3(0.0, -height, 0.0);
      float intersection2 = diskIntersectWithBackFaceCulling(camPos, p, h, vec3(0.0, 1.0, 0.0), radius);
      p = (camPos + min(intersection, intersection2) * p) / radius;
    } else {
      p = vec3(0.0, 1.0, 0.0);
    }
    return p;
  }

  #include <common>

  void main() {
    vec3 direction = normalize(rotation * project());
    vec3 outcolor = texture2D(map, equirectUv(direction)).rgb * intensity;
    gl_FragColor = vec4(outcolor, 1.0);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
  }`;
