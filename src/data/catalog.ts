import epcGroups from './epcGroups.json';

/** One row of the parts catalogue as the app sees it (the database row minus internal notes). */
export type CatalogPart = {
  key: string;
  system: string;
  groupCode: string;
  groupStatus: 'verified' | 'recalled' | 'unknown';
  category: string;
  nameEn: string;
  nameAr: string;
  aliases: string[];
  oemNumber: string | null;
  altOemNumbers: string[];
  oemStatus: 'pending' | 'entered' | 'verified';
  fitsGxr: boolean;
  /** three.js car space, for parts that are not meshes in the model */
  hotspot: [number, number, number] | null;
  meshPresent: boolean;
  serviceIntervalKm: number | null;
};

export type CatalogResponse = { source: 'neon' | 'seed'; parts: CatalogPart[] };

/** Toyota EPC illustration group names for FZJ100 1FZ-FE GX MTM LHD GCC. */
export const EPC_GROUPS = epcGroups as Record<string, string>;

export function groupLabel(code: string) {
  const name = EPC_GROUPS[code];
  return name ? `${code} ${name}` : null;
}

// ---------------------------------------------------------------------------------------------
// Search. The catalogue is a few hundred rows, so it is searched in the browser: instant, and it
// works offline. Arabic is normalised the way people type it (hamza forms, taa marbuta, alef
// maqsura, no diacritics), Latin is lower cased, OEM numbers match with or without dashes.

const TASHKEEL = /[ً-ْٰـ]/g;

export function normalise(text: string) {
  return text
    .toLowerCase()
    .replace(TASHKEEL, '')
    .replace(/[أإآٱ]/g, 'ا')
    .replace(/ة/g, 'ه')
    .replace(/ى/g, 'ي')
    .replace(/ؤ/g, 'و')
    .replace(/ئ/g, 'ي')
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim();
}

const digits = (s: string) => s.replace(/[^0-9a-z]/gi, '').toLowerCase();

type Indexed = { part: CatalogPart; name: string; words: string[]; text: string; oems: string[] };

export function buildIndex(parts: CatalogPart[]): Indexed[] {
  return parts.map((part) => {
    const fields = [part.nameEn, part.nameAr, ...part.aliases, part.key.replace(/_/g, ' '), part.category];
    const text = normalise(fields.join(' '));
    return {
      part,
      name: normalise(part.nameEn),
      words: text.split(' '),
      text,
      oems: [part.oemNumber, ...part.altOemNumbers].filter((x): x is string => !!x).map(digits),
    };
  });
}

/** Ranked matches; every query word has to match somewhere. */
export function search(index: Indexed[], query: string, limit = 8): CatalogPart[] {
  const q = normalise(query);
  if (!q) return [];
  const tokens = q.split(' ');
  const qDigits = digits(query);
  const scored: { part: CatalogPart; score: number }[] = [];
  for (const it of index) {
    let score = 0;
    if (qDigits.length >= 5 && it.oems.some((o) => o.startsWith(qDigits) || o.includes(qDigits))) score += 120;
    let all = true;
    for (const t of tokens) {
      let best = 0;
      for (const w of it.words) {
        if (w === t) best = Math.max(best, 30);
        else if (w.startsWith(t)) best = Math.max(best, 20);
        else if (t.length >= 3 && w.includes(t)) best = Math.max(best, 8);
      }
      if (!best && score < 120) {
        all = false;
        break;
      }
      score += best;
    }
    if (!all) continue;
    if (it.name.startsWith(q)) score += 25;
    if (it.part.meshPresent) score += 2;
    if (!it.part.fitsGxr) score -= 15;
    scored.push({ part: it.part, score });
  }
  scored.sort((a, b) => b.score - a.score || a.part.nameEn.localeCompare(b.part.nameEn));
  return scored.slice(0, limit).map((s) => s.part);
}

/** Parts due at a service at `km` (an interval divides it: the 10 000 km service includes the 5 000 km items). */
export function dueAt(parts: CatalogPart[], km: number) {
  return parts.filter((p) => p.serviceIntervalKm && km % p.serviceIntervalKm === 0);
}

const CAR = 'Toyota Land Cruiser 100, 2005, GCC GXR, 1FZ-FE, 5 speed manual';

/** WhatsApp link that asks the shop for a price for exactly this part. Null when no number is configured. */
export function whatsappLink(part: CatalogPart, link: string, number = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER) {
  const n = (number ?? '').replace(/[^0-9]/g, '');
  if (!n) return null;
  const group = groupLabel(part.groupCode);
  const lines = [
    'Hi, can I get the price for this part?',
    `Part: ${part.nameEn}${part.nameAr ? ` (${part.nameAr})` : ''}`,
    `OEM number: ${part.oemNumber ?? 'to confirm'}`,
    group ? `Toyota group: ${group}` : null,
    `Car: ${CAR}`,
    `Part code: ${part.key}`,
    link,
  ].filter(Boolean);
  return `https://wa.me/${n}?text=${encodeURIComponent(lines.join('\n'))}`;
}
