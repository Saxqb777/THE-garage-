"""Build the parts seed and load it into Neon (M7).

    python3 scripts/parts/build_seed.py data/parts.full.json [--no-db]

Input: the full dataset (every row with names, aliases, group, hotspot, interval, fitment and
owner notes). Checks every row against the naming spec, the contract (src/data/parts.m1.json),
the Toyota EPC groups verified for this variant (src/data/epcGroups.json) and the car's bounds,
then writes:
  src/data/parts.seed.json   what the app serves when the database is not reachable
  data/parts_oem_sheet.csv   a sheet for the owner to fill in OEM numbers (import_oem.py)
and upserts the rows into the parts table. Owner entered fields (oem_number, alt_oem_numbers,
oem_status, supplier_note) are never overwritten by a re-seed.
"""
import csv, json, re, sys
sys.path.insert(0, 'scripts/parts')

KEY = re.compile(r'^(BODY|DOOR|GLASS|WHEEL|SUSP|BRAKE|ENG|COOL|EXH|TRANS|DRIVE|ELEC|INT|AC|LIGHT|TRIM)_(\d{4})_([a-z0-9]+(?:_[a-z0-9]+)*?)(?:_(L|R|F|RR))?$')
OEM_LIKE = re.compile(r'\b\d{5}-[0-9A-Z]{5}\b')
INTERVALS = {None, 5000, 10000, 40000, 80000}

def check(rows, contract_keys, groups):
    problems, seen = [], set()
    for r in rows:
        k = r['key']
        m = KEY.match(k)
        if not m: problems.append(f'{k}: key does not match the naming pattern'); continue
        if m.group(1) != r['system']: problems.append(f'{k}: system {r["system"]} differs from the key')
        if m.group(2) != r['group_code']: problems.append(f'{k}: group {r["group_code"]} differs from the key')
        if r['group_code'] != '0000' and r['group_code'] not in groups: problems.append(f'{k}: group {r["group_code"]} is not in this variant\'s EPC')
        if k in seen: problems.append(f'{k}: duplicate key')
        seen.add(k)
        mesh = k in contract_keys
        if not mesh:
            h = r.get('hotspot')
            if not h or len(h) != 3: problems.append(f'{k}: no mesh and no hotspot')
            else:
                x, y, z = h
                if not (-1.1 <= x <= 1.1 and 0.0 <= y <= 2.0 and -2.55 <= z <= 2.55): problems.append(f'{k}: hotspot {h} is outside the car')
        if r.get('service_interval_km') not in INTERVALS: problems.append(f'{k}: service interval {r.get("service_interval_km")}')
        for f in ('name_en', 'name_ar', 'notes'):
            if OEM_LIKE.search(r.get(f) or ''): problems.append(f'{k}: {f} contains something that looks like an OEM number')
        if not r.get('name_en'): problems.append(f'{k}: no English name')
    missing = sorted(contract_keys - seen)
    for k in missing: problems.append(f'{k}: contract part missing from the dataset')
    return problems

def to_app(r, contract_keys):
    mesh = r['key'] in contract_keys
    return {
        'key': r['key'], 'system': r['system'], 'groupCode': r['group_code'], 'groupStatus': r['group_status'],
        'category': r['category'], 'nameEn': r['name_en'], 'nameAr': r.get('name_ar', ''),
        'aliases': list(dict.fromkeys([*r.get('aliases_en', []), *r.get('aliases_ar', [])])),
        'oemNumber': None, 'altOemNumbers': [], 'oemStatus': 'pending', 'fitsGxr': r.get('fits_gxr', True),
        'hotspot': None if mesh else [round(v, 3) for v in r['hotspot']], 'meshPresent': mesh,
        'serviceIntervalKm': r.get('service_interval_km'),
    }

COLS = ['key', 'system', 'group_code', 'group_status', 'category', 'name_en', 'name_ar', 'aliases', 'fits_gxr', 'hotspot_position', 'mesh_present', 'service_interval_km', 'notes', 'diagram_group']

def upsert(app_rows, notes, groups):
    from neon import sql
    values, params = [], []
    for i, a in enumerate(app_rows):
        row = [a['key'], a['system'], a['groupCode'], a['groupStatus'], a['category'], a['nameEn'], a['nameAr'], a['aliases'], a['fitsGxr'],
               a['hotspot'], a['meshPresent'], a['serviceIntervalKm'], notes.get(a['key'], ''),
               f"{a['groupCode']} {groups[a['groupCode']]}" if a['groupCode'] in groups else None]
        base = len(params)
        casts = ['', '', '', '', '', '', '', '::text[]', '::boolean', '::real[]', '::boolean', '::integer', '', '']
        values.append('(' + ', '.join(f'${base + j + 1}{casts[j]}' for j in range(len(row))) + ')')
        params.extend(row)
    update = ', '.join(f'{c} = excluded.{c}' for c in COLS if c != 'key')
    q = f'insert into parts ({", ".join(COLS)}) values {", ".join(values)} on conflict (key) do update set {update}'
    sql(q, params)
    keys = [a['key'] for a in app_rows]
    stale = sql('select key from parts where not (key = any($1::text[]))', [keys])['rows']
    return len(app_rows), [r['key'] for r in stale]

def main():
    src = sys.argv[1]
    rows = json.load(open(src))
    contract = json.load(open('src/data/parts.m1.json'))
    contract_keys = {p['key'] for p in contract['parts']}
    groups = json.load(open('src/data/epcGroups.json'))
    problems = check(rows, contract_keys, groups)
    if problems:
        print('\n'.join(problems)); raise SystemExit(f'{len(problems)} problems, nothing written')
    app_rows = sorted((to_app(r, contract_keys) for r in rows), key=lambda a: a['key'])
    json.dump(app_rows, open('src/data/parts.seed.json', 'w'), ensure_ascii=False, indent=1)
    with open('data/parts_oem_sheet.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['key', 'name_en', 'name_ar', 'toyota_group', 'fits_gxr', 'oem_number', 'alt_oem_numbers', 'supplier_note'])
        for a in app_rows:
            w.writerow([a['key'], a['nameEn'], a['nameAr'], f"{a['groupCode']} {groups.get(a['groupCode'], '')}".strip(), 'yes' if a['fitsGxr'] else 'no', '', '', ''])
    print(f'{len(app_rows)} rows: {sum(a["meshPresent"] for a in app_rows)} on the model, {sum(not a["meshPresent"] for a in app_rows)} hotspots, '
          f'{sum(1 for a in app_rows if a["serviceIntervalKm"])} with a service interval, {sum(not a["fitsGxr"] for a in app_rows)} not on the GXR')
    if '--no-db' not in sys.argv:
        notes = {r['key']: r.get('notes', '') for r in rows}
        n, stale = upsert(app_rows, notes, groups)
        print(f'upserted {n} rows into Neon' + (f'; rows in the database that are not in this seed (left alone): {stale}' if stale else ''))

if __name__ == '__main__':
    main()
