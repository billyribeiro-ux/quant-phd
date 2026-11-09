# Process-word, banned-string and non-ASCII scan of the cards changed or added in the closing delta, plus duplicate checks.
import collections, json, re
b = json.load(open('/Users/billyribeiro/.fanout/wt/verifyH1-M2-b/course/modules/M/M2/cards.json', encoding='utf-8'))
proc = r'\b(now|previous|previously|earlier|changed|revised|corrected|verifier|builder|round|draft|we|I|my|our|fixed|stale|ruling)\b'
ban = ['TODO','TBD','lorem','...','for brevity','omitted','beyond the scope','left as an exercise','you can add','important to note','studies show','experts agree','well known','obviously','clearly','historically','roughly']
for c in b:
    if c['id'] in ('M2-c107','M2-c161','M2-c431','M2-c432'):
        t = c['front'] + ' ' + c['back']
        print(c['id'], 'process-words:', re.findall(proc, t, flags=re.I), 'banned:', [x for x in ban if x.lower() in t.lower()], 'non-ascii:', [ch for ch in t if ord(ch) > 127])
print('cards:', len(b), 'unique ids:', len({c['id'] for c in b}))
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
fr = collections.defaultdict(list); bk = collections.defaultdict(list)
for c in b:
    fr[norm(c['front'])].append(c['id']); bk[norm(c['back'])].append(c['id'])
print('duplicate normalized fronts:', [v for v in fr.values() if len(v) > 1])
print('duplicate normalized backs:', [v for v in bk.values() if len(v) > 1])
