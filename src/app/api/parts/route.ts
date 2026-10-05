import seed from '@/data/parts.seed.json';
import type { CatalogPart, CatalogResponse } from '@/data/catalog';

/**
 * The parts catalogue (M7). Reads the Neon database over its HTTP SQL endpoint (no driver
 * needed), keeps the result for a minute, and falls back to the committed seed export when the
 * database is not configured or not reachable, so the app always has a catalogue.
 */

const SQL = `select key, system, group_code, group_status, category, name_en, name_ar, aliases,
  oem_number, alt_oem_numbers, oem_status, fits_gxr, hotspot_position, mesh_present, service_interval_km
  from parts order by key`;

type Row = {
  key: string;
  system: string;
  group_code: string;
  group_status: CatalogPart['groupStatus'];
  category: string;
  name_en: string;
  name_ar: string;
  aliases: string[];
  oem_number: string | null;
  alt_oem_numbers: string[];
  oem_status: CatalogPart['oemStatus'];
  fits_gxr: boolean;
  hotspot_position: number[] | null;
  mesh_present: boolean;
  service_interval_km: number | null;
};

const toPart = (r: Row): CatalogPart => ({
  key: r.key,
  system: r.system,
  groupCode: r.group_code,
  groupStatus: r.group_status,
  category: r.category,
  nameEn: r.name_en,
  nameAr: r.name_ar,
  aliases: r.aliases ?? [],
  oemNumber: r.oem_number,
  altOemNumbers: r.alt_oem_numbers ?? [],
  oemStatus: r.oem_status,
  fitsGxr: r.fits_gxr,
  hotspot: r.hotspot_position && r.hotspot_position.length === 3 ? [r.hotspot_position[0], r.hotspot_position[1], r.hotspot_position[2]] : null,
  meshPresent: r.mesh_present,
  serviceIntervalKm: r.service_interval_km,
});

let cached: { at: number; body: CatalogResponse } | null = null;

async function fromNeon(url: string): Promise<CatalogPart[]> {
  const host = new URL(url.replace(/^postgres(ql)?:/, 'https:')).hostname;
  const res = await fetch(`https://${host}/sql`, {
    method: 'POST',
    headers: { 'Neon-Connection-String': url, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: SQL, params: [] }),
    cache: 'no-store',
  });
  if (!res.ok) throw new Error(`Neon ${res.status}: ${(await res.text()).slice(0, 200)}`);
  const data = (await res.json()) as { rows: Row[] };
  return data.rows.map(toPart);
}

export async function GET() {
  if (cached && Date.now() - cached.at < 60_000) return respond(cached.body);
  let body: CatalogResponse = { source: 'seed', parts: seed as CatalogPart[] };
  const url = process.env.DATABASE_URL;
  if (url) {
    try {
      const parts = await fromNeon(url);
      if (parts.length) body = { source: 'neon', parts };
    } catch (e) {
      console.error('[garage] parts from Neon failed, serving the seed', e);
    }
  }
  cached = { at: Date.now(), body };
  return respond(body);
}

function respond(body: CatalogResponse) {
  return Response.json(body, { headers: { 'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=600' } });
}
