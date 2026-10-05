"""Load OEM numbers from the filled sheet into Neon.

    python3 scripts/parts/import_oem.py data/parts_oem_sheet.csv

Rows with an oem_number set become oem_status 'entered'. Blank rows are left as they are.
alt_oem_numbers takes several numbers separated by spaces or commas.
"""
import csv, re, sys
sys.path.insert(0, 'scripts/parts')
from neon import sql

OEM = re.compile(r'^[0-9A-Z]{5}-?[0-9A-Z]{5}$')

def main():
    n = 0
    bad = []
    for r in csv.DictReader(open(sys.argv[1], encoding='utf-8')):
        oem = (r.get('oem_number') or '').strip().upper()
        if not oem: continue
        alts = [a.strip().upper() for a in re.split(r'[ ,;]+', r.get('alt_oem_numbers') or '') if a.strip()]
        for o in [oem, *alts]:
            if not OEM.match(o): bad.append(f'{r["key"]}: {o}')
        sql("update parts set oem_number = $2, alt_oem_numbers = $3::text[], oem_status = 'entered', supplier_note = nullif($4, '') where key = $1",
            [r['key'], oem, alts, (r.get('supplier_note') or '').strip()])
        n += 1
    print(f'{n} parts updated')
    if bad: print('check these, they do not look like Toyota numbers (5 + 5 characters):\n' + '\n'.join(bad))

if __name__ == '__main__':
    main()
