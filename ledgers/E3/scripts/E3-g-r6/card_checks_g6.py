# Card checks for E3 slice g (L05-L08): numbers present in the lesson text, duplicate scan, process words, grades vs key results.
import json, re, difflib, sys
cards = json.load(open('course/modules/E/E3/cards.json', encoding='utf-8'))
texts = {L: open(f'ledgers/E3/scripts/E3-g-r6/text/{L}.txt', encoding='utf-8').read() for L in ('L05','L06','L07','L08')}
allt = '\n'.join(texts.values())
slice_cards = [c for c in cards if c['lesson'] in ('L05','L06','L07','L08')]
print('slice cards:', len(slice_cards), 'ids:', sorted(c['id'] for c in slice_cards)[0], '..', sorted(c['id'] for c in slice_cards)[-1])
print('all unit cards:', len(cards), 'unique ids:', len({c['id'] for c in cards}))
print('grade counts (slice):', {g: sum(1 for c in slice_cards if c.get('grade')==g) for g in ('T','C',None)})
# 1. numbers in card text must occur in the lesson text of the card's own lesson or any slice lesson
num_re = re.compile(r'\d+(?:\.\d+)?(?:e-?\d+)?|\d+/\d+')
print('== numbers not found verbatim in L05-L08 text (card id: token)')
for c in slice_cards:
    for field in ('front','back'):
        for tok in num_re.findall(c[field]):
            if tok not in allt:
                print(c['id'], field, repr(tok))
# 2. process words
bad = re.compile(r"\b(we|our|let's|TODO|verifier|builder|round|FIXME)\b", re.I)
print('== process-word hits:', [(c['id'], m.group(0)) for c in cards for f in ('front','back') for m in [bad.search(c[f])] if m])
# 3. duplicates: exact and near (difflib on front+back) across the whole unit
print('== exact duplicate fronts/backs:', [k for k,v in __import__('collections').Counter(c['front'] for c in cards).items() if v>1], [k for k,v in __import__('collections').Counter(c['back'] for c in cards).items() if v>1])
pairs=[]
for i,a in enumerate(cards):
    for b in cards[i+1:]:
        ra = difflib.SequenceMatcher(None, a['front']+' '+a['back'], b['front']+' '+b['back']).ratio()
        if ra >= 0.55 and (a['lesson'] in ('L05','L06','L07','L08') or b['lesson'] in ('L05','L06','L07','L08')):
            pairs.append((round(ra,3), a['id'], b['id']))
pairs.sort(reverse=True)
print('== near pairs (ratio>=0.55, at least one slice card):', len(pairs))
for p in pairs: print(p)
# 4. ids present and sequential gaps in slice
ids = sorted(int(c['id'].split('-c')[1]) for c in slice_cards)
print('== slice id numbers:', ids)
