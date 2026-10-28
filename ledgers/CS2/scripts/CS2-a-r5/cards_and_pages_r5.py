import json, re, sys
root = sys.argv[1]
cards = {c['id']: c for c in json.load(open(root + '/course/modules/CS/CS2/cards.json'))}
checks = {
    'CS2-c015': ('independently', 'Assumption 2.1 wording in L02.html says "without regard"; card says "independently"'),
    'CS2-c018': ('expected', 'lesson uses "average" (no "expected" in L02.html)'),
    'CS2-c155': ('193', 'card claims totals 257 and 193; 3.0156 x 256 = 772, and 193/64 = 772/256'),
    'CS2-c047': ('records', 'Prop 2.1 hypothesis (6) absent from card'),
    'CS2-c055': ('records', 'Prop 2.1 hypothesis (6) absent from card'),
    'CS2-c037': ('not constant', 'page proves only an upper bound'),
    'CS2-c049': ('Definition 3.1', 'gap is an unnumbered paragraph after Definition 3.1'),
}
for cid, (needle, why) in checks.items():
    print(cid, 'contains', repr(needle), '->', needle in cards[cid]['back'] or needle in cards[cid]['front'], '|', why)
l04 = open(root + '/course/modules/CS/CS2/L04.html', encoding='utf-8').read()
print('L04.html has hypothesis (6):', '(6) On every input' in l04)
l02 = open(root + '/course/modules/CS/CS2/L02.html', encoding='utf-8').read()
print('L02.html contains "without regard":', 'without regard' in l02, '| "expected":', 'expected' in l02)
l03 = open(root + '/course/modules/CS/CS2/L03.html', encoding='utf-8').read()
print('L03.html "proves no constant bound":', 'proves no constant bound' in l03)
idx = open(root + '/course/modules/CS/CS2/index.html', encoding='utf-8').read()
print('index.html claims every lab hypothesis labels SIMULATED:', 'each lab' in idx and 'labels them SIMULATED' in idx)
l04h = re.search(r'<p class="hypothesis">(.*?)</p>', l04, re.S).group(1)
print('L04 hypothesis mentions SIMULATED:', l04h.count('SIMULATED'), 'times; Part A only:', 'Part A' in l04h)
