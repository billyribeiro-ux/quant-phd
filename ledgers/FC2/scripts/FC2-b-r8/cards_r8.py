import json, re, html, collections, sys
cards = json.load(open('course/modules/FC/FC2/cards.json'))
print('total cards', len(cards))
ids = [c['id'] for c in cards]
print('unique ids', len(set(ids)) == len(ids), 'dup ids', [i for i,n in collections.Counter(ids).items() if n>1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print('key sets', dict(keys))
bylesson = collections.defaultdict(list)
for c in cards: bylesson[c['lesson']].append(c)
print('per lesson', {k: len(v) for k, v in sorted(bylesson.items())})
def norm(s): return re.sub(r'\W+', ' ', s.lower()).strip()
fr = collections.defaultdict(list)
for c in cards: fr[norm(c['front'])].append(c['id'])
print('duplicate fronts', [v for v in fr.values() if len(v) > 1])
bk = collections.defaultdict(list)
for c in cards: bk[norm(c['back'])].append(c['id'])
print('duplicate backs', [v for v in bk.values() if len(v) > 1])
# slice lessons
for L in ['L04','L05','L06']:
    page = open(f'course/modules/FC/FC2/{L}.html', encoding='utf-8').read()
    text = html.unescape(re.sub(r'<[^>]+>', ' ', page))
    text = re.sub(r'\s+', ' ', text)
    print('==', L, 'cards', len(bylesson[L]))
    for c in bylesson[L]:
        refs = re.findall(r'\((?:[^()]*?)\)', c['back'])
        nums = re.findall(r'\d+(?:[./]\d+)?', c['back'])
        missing_nums = [n for n in nums if n not in text and n not in page]
        refs_missing = []
        for r in re.findall(r'(Definition|Theorem|Proposition|Remark|Lemma|Example|Section|Assumption|Corollary|Problem|A\d)\s*[\d.]*', c['back']):
            pass
        m = re.findall(r'\b(Definition|Theorem|Proposition|Remark|Lemma|Example|Section|Corollary|Problem|Misconception|Lab|misconception)\s+(\d+(?:\.\d+)?)', c['back'])
        for kind, num in m:
            pat = {'Section': r'Section', }.get(kind, kind)
            if not re.search(kind + r'\s*' + re.escape(num) + r'\b', page) and not re.search(kind + r'\s*' + re.escape(num) + r'\b', text):
                refs_missing.append(f'{kind} {num}')
        print(c['id'], c.get('grade', '-'), 'refs_missing=' + str(refs_missing), 'nums_missing=' + str(missing_nums))
