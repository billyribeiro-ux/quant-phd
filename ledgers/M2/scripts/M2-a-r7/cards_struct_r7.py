import json, sys, collections
cards = json.load(open(sys.argv[1] + '/course/modules/M/M2/cards.json', encoding='utf-8'))
ids = collections.Counter(c['id'] for c in cards)
fronts = collections.Counter(c['front'] for c in cards)
print('cards', len(cards), 'dup ids', [k for k, v in ids.items() if v > 1], 'dup fronts', [k for k, v in fronts.items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
for k, v in keys.items():
    print('keyset', v, k)
bad_grade = [c['id'] for c in cards if 'grade' in c and c['grade'] not in ('T', 'C', 'X', 'R', 'U')]
print('odd grades', bad_grade, collections.Counter(c.get('grade') for c in cards))
slice_l = {'L01', 'L02', 'L03', 'L04', 'L05', 'L06'}
print('slice-lesson cards with no basis key but grade C', [c['id'] for c in cards if c['lesson'] in slice_l and c.get('grade') == 'C' and 'basis' not in c])
for c in cards:
    if c['id'] in ('M2-c013', 'M2-c044', 'M2-c064', 'M2-c394', 'M2-c414', 'M2-c006', 'M2-c424'):
        print(json.dumps(c, ensure_ascii=False))
