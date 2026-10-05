"""Merge the parts workflow output into the full dataset (M7).

    python3 scripts/parts/merge_workflow.py <workflow result json> [data/parts.full.json]

The workflow returns {rows, issues, critic: {add, drop, replace, notes}}. This script:
  * maps every row that has a mesh onto its contract key (src/data/parts.m1.json is the authority
    for key, system and group of mesh parts; data/rekey_m7.json maps keys from before the re-key),
  * applies the critic (drop, replace, add) without ever dropping a contract part,
  * merges duplicate keys (aliases unioned, notes joined),
  * normalises group status against the variant's EPC group list (src/data/epcGroups.json),
  * fills any contract part the workflow missed from the contract and lists it for review,
  * writes the dataset sorted by key and prints everything that needs a look.
build_seed.py then does the strict checks and loads Neon.
"""
import json, re, sys

OEM_LIKE = re.compile(r'\b\d{5}-[0-9A-Z]{5}\b')

def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else 'data/parts.full.json'
    res = json.load(open(src))
    contract = {p['key']: p for p in json.load(open('src/data/parts.m1.json'))['parts']}
    rekey = json.load(open('data/rekey_m7.json'))
    groups = json.load(open('src/data/epcGroups.json'))
    log = []

    def resolve(k):
        if k in contract: return k
        if k in rekey: return rekey[k]
        return None

    def prepare(r, origin):
        r = dict(r)
        mesh = resolve(r.get('mesh_key') or '') or resolve(r['key'])
        if mesh:
            c = contract[mesh]
            if r['key'] != mesh: log.append(f'{origin}: {r["key"]} is the mesh {mesh}, keyed to it')
            r.update(key=mesh, mesh_key=mesh, system=c['system'], group_code=c['groupCode'], group_status=c['groupStatus'], hotspot=None)
        elif r.get('mesh_key'):
            log.append(f'{origin}: {r["key"]} names mesh {r["mesh_key"]} which is not in the contract, kept as a hotspot row')
            r['mesh_key'] = None
        if not mesh:
            g = r['group_code']
            if g == '0000': r['group_status'] = 'unknown'
            elif g in groups: r['group_status'] = 'verified'
            else: log.append(f'{origin}: {r["key"]} group {g} is not in the variant EPC, needs a fix')
        en = [a.strip() for a in r.get('aliases_en', []) if a.strip()]
        r['aliases_en'] = list(dict.fromkeys(a.lower() for a in en if a.lower() != r['name_en'].lower()))
        r['aliases_ar'] = list(dict.fromkeys(a.strip() for a in r.get('aliases_ar', []) if a.strip() and a.strip() != r.get('name_ar', '').strip()))
        for f in ('aliases_en', 'aliases_ar'):
            if any(OEM_LIKE.search(a) for a in r[f]): log.append(f'{origin}: {r["key"]} {f} has something like an OEM number, removed'); r[f] = [a for a in r[f] if not OEM_LIKE.search(a)]
        return r

    rows = {}
    def put(r, origin):
        k = r['key']
        if k not in rows: rows[k] = r; return
        a = rows[k]
        log.append(f'{origin}: duplicate {k} merged')
        a['aliases_en'] = list(dict.fromkeys(a['aliases_en'] + r['aliases_en']))
        a['aliases_ar'] = list(dict.fromkeys(a['aliases_ar'] + r['aliases_ar']))
        if r.get('notes') and r['notes'] not in (a.get('notes') or ''): a['notes'] = '; '.join(x for x in (a.get('notes'), r['notes']) if x)
        if a.get('service_interval_km') is None: a['service_interval_km'] = r.get('service_interval_km')
        if not a.get('name_ar'): a['name_ar'] = r.get('name_ar', '')

    for r in res['rows']: put(prepare(r, 'workflow'), 'workflow')

    critic = res.get('critic') or {}
    for k in critic.get('drop', []):
        rk = resolve(k) or k
        if rk in contract: log.append(f'critic: wanted to drop contract part {rk}, kept'); continue
        if rows.pop(rk, None) is not None: log.append(f'critic: dropped {rk}')
        else: log.append(f'critic: drop {k} matched nothing')
    for r in critic.get('replace', []):
        r = prepare(r, 'critic replace')
        if r['key'] in rows: rows[r['key']] = r; log.append(f'critic: replaced {r["key"]}')
        else: put(r, 'critic replace'); log.append(f'critic: replace {r["key"]} matched nothing, added')
    for r in critic.get('add', []):
        r = prepare(r, 'critic add')
        put(r, 'critic add')

    for k, c in contract.items():
        if k not in rows:
            rows[k] = {'key': k, 'system': c['system'], 'group_code': c['groupCode'], 'group_status': c['groupStatus'], 'name_en': c['nameEn'],
                       'name_ar': '', 'aliases_en': [], 'aliases_ar': [], 'category': 'Model parts', 'mesh_key': k, 'hotspot': None,
                       'service_interval_km': None, 'fits_gxr': True, 'notes': ''}
            log.append(f'contract: {k} was missing, filled from the contract (no Arabic yet)')

    data = [rows[k] for k in sorted(rows)]
    json.dump(data, open(out, 'w'), ensure_ascii=False, indent=1)
    print('\n'.join(log))
    print(f'{len(data)} rows written to {out}; critic notes:')
    for n in critic.get('notes', []): print(' *', n)

if __name__ == '__main__':
    main()
