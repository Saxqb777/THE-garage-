'use client';

import { useLayoutEffect, useMemo, useRef } from 'react';
import { useFrame, type ThreeEvent } from '@react-three/fiber';
import { Color, Group, InstancedMesh, Matrix4, MeshBasicMaterial, Vector3, type Mesh } from 'three';
import { dueAt, type CatalogPart } from '@/data/catalog';
import { goToPart } from './goTo';
import { carLift } from './liftState';
import { useGarage } from './store';

/**
 * Markers for catalogue parts that are not meshes in the model (engine, brakes, filters,
 * suspension...), at their hotspot positions. With a service interval active only the parts due
 * (and the selected one) show; otherwise all of them show in X Ray (the brief's "hotspots for
 * mechanical parts become visible in place"), else just the selected part. Drawn on top, so they
 * read through the ghosted body, and sized by camera distance so they stay about the same size on
 * screen instead of turning into blobs close up.
 */

const BASE = new Color('#7cc8ff');
const DIM = new Color('#4d7896');
const DUE = new Color('#ffb547');
const SELECTED = new Color('#f2c36b');
// dot radius per metre of camera distance (about 6 px at the default field of view), clamped in metres
const PER_METRE = 0.007;
const MIN_R = 0.006;
const MAX_R = 0.035;
const dotRadius = (distance: number) => Math.min(MAX_R, Math.max(MIN_R, distance * PER_METRE));
const m = new Matrix4();
const v = new Vector3();

export default function PartHotspots() {
  const catalog = useGarage((s) => s.catalog);
  const xray = useGarage((s) => s.xray);
  const selected = useGarage((s) => s.selected);
  const service = useGarage((s) => s.service);
  const view = useGarage((s) => s.view);
  const group = useRef<Group>(null);
  const dots = useRef<InstancedMesh>(null);
  const ring = useRef<Mesh>(null);
  const boundsFor = useRef<CatalogPart[] | null>(null);

  const all = useMemo(() => (catalog ? [...catalog.values()].filter((p) => !p.meshPresent && p.hotspot) : []), [catalog]);
  const due = useMemo(() => new Set(service && catalog ? dueAt([...catalog.values()], service).map((p) => p.key) : []), [catalog, service]);
  const shown: CatalogPart[] = useMemo(
    () => {
      if (view === 'cabin') return [];
      if (service) return all.filter((p) => due.has(p.key) || p.key === selected);
      return all.filter((p) => xray || p.key === selected);
    },
    [all, xray, selected, due, service, view],
  );

  useLayoutEffect(() => {
    const mesh = dots.current;
    if (!mesh) return;
    shown.forEach((p, i) => mesh.setColorAt(i, p.key === selected ? SELECTED : due.has(p.key) ? DUE : selected ? DIM : BASE));
    mesh.count = shown.length;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  }, [shown, selected, due]);

  const selectedPart = selected ? shown.find((p) => p.key === selected) : undefined;

  useFrame(({ clock, camera }) => {
    if (group.current) group.current.position.y = carLift.y;
    const mesh = dots.current;
    if (mesh) {
      // other markers shrink while a part is selected, so the selected one reads first
      shown.forEach((p, i) => {
        const r = dotRadius(camera.position.distanceTo(v.set(p.hotspot![0], p.hotspot![1] + carLift.y, p.hotspot![2])));
        const s = selected && p.key !== selected && !due.has(p.key) ? r * 0.7 : r;
        m.makeScale(s, s, s).setPosition(p.hotspot![0], p.hotspot![1], p.hotspot![2]);
        mesh.setMatrixAt(i, m);
      });
      mesh.instanceMatrix.needsUpdate = true;
      // pointer picking tests the cached bounding sphere first, so refresh it when the set changes
      if (boundsFor.current !== shown) {
        mesh.computeBoundingSphere();
        boundsFor.current = shown;
      }
    }
    if (ring.current && selectedPart) {
      const h = selectedPart.hotspot!;
      const r = dotRadius(camera.position.distanceTo(v.set(h[0], h[1] + carLift.y, h[2])));
      const k = 1 + 0.35 * Math.sin(clock.elapsedTime * 4);
      ring.current.scale.setScalar(r * 2.2 * k);
      (ring.current.material as MeshBasicMaterial).opacity = 0.9 - 0.4 * (k - 0.65);
    }
  });

  const pick = (e: ThreeEvent<PointerEvent | MouseEvent>) => (e.instanceId !== undefined ? shown[e.instanceId] : undefined);

  return (
    <group ref={group}>
      <instancedMesh
        ref={dots}
        args={[undefined, undefined, Math.max(1, all.length)]}
        renderOrder={1000}
        frustumCulled={false}
        onPointerMove={(e) => {
          const p = pick(e);
          if (!p) return;
          e.stopPropagation();
          if (useGarage.getState().hovered !== p.key) useGarage.getState().setHovered(p.key);
          document.body.style.cursor = 'pointer';
        }}
        onPointerOut={() => {
          useGarage.getState().setHovered(null);
          document.body.style.cursor = '';
        }}
        onClick={(e) => {
          const p = pick(e);
          if (!p || e.delta > 6) return;
          e.stopPropagation();
          goToPart(p.key);
        }}
      >
        <sphereGeometry args={[1, 16, 12]} />
        <meshBasicMaterial depthTest={false} depthWrite={false} transparent opacity={0.95} toneMapped={false} />
      </instancedMesh>
      {selectedPart && (
        <mesh ref={ring} position={selectedPart.hotspot!} renderOrder={1001}>
          <sphereGeometry args={[1, 20, 14]} />
          <meshBasicMaterial color={SELECTED} wireframe depthTest={false} depthWrite={false} transparent toneMapped={false} />
        </mesh>
      )}
    </group>
  );
}
