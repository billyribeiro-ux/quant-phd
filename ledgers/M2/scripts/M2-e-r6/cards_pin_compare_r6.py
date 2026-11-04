import json, collections
a = json.load(open('ledgers/M2/scripts/M2-e-r6/cards_440_pin.json'))
b = json.load(open('ledgers/M2/scripts/M2-e-r6/cards_142_pin.json'))
print(type(a), len(a), len(b))
A = {c['id']: c for c in a}; B = {c['id']: c for c in b}
print('dup ids A', len(a)-len(A), 'dup ids B', len(b)-len(B))
changed = [i for i in A if i in B and A[i] != B[i]]
removed = [i for i in A if i not in B]
added = [i for i in B if i not in A]
print('changed', changed)
print('removed', removed)
print('added', added)
lessons = collections.Counter(c['lesson'] for c in b)
print(sorted(lessons.items()))
print('keys', set(k for c in b for k in c))
