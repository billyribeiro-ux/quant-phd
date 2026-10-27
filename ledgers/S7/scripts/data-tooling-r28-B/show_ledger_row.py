import json, sys
ledger = sys.argv[1]; ids = sys.argv[2].split(','); n = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
d = json.load(open(ledger))
rows = {r['id']: r for r in d['rows']}
for i in ids:
    r = rows.get(i)
    if r is None:
        print('## MISSING', i); continue
    print('##', i, r['status'], '|', r['check'], '|', r['location'])
    print(r['evidence'][:n]); print()
