import json, sys, difflib
root = sys.argv[1]
cards = json.load(open(f'{root}/course/modules/E/E3/cards.json', encoding='utf-8'))
ids = {'E3-c005','E3-c007','E3-c008','E3-c011','E3-c012','E3-c017','E3-c025','E3-c037','E3-c188','E3-c049','E3-c083','E3-c101','E3-c106','E3-c117','E3-c154','E3-c173'}
out = []
for a in cards:
    if a['id'] not in ids: continue
    for b in cards:
        if a['id'] == b['id']: continue
        rf = difflib.SequenceMatcher(None, a['front'], b['front']).ratio()
        rb = difflib.SequenceMatcher(None, a['back'], b['back']).ratio()
        if rf > 0.7 or rb > 0.7:
            out.append((a['id'], b['id'], round(rf,2), round(rb,2)))
print('pairs over 0.7 for changed cards:', len(out))
for o in out: print(o)
ids_all = [c['id'] for c in cards]
print('total', len(ids_all), 'distinct', len(set(ids_all)))
print('ids in c001..c188 missing:', [f'E3-c{i:03d}' for i in range(1,189) if f'E3-c{i:03d}' not in set(ids_all)])
