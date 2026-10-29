import json,re,collections,sys
new=json.load(open('course/modules/M/M4/cards.json'))
old={c['id']:c for c in json.load(open('/tmp/M4-d-r13-scratch/cards_old.json'))}
ids=[c['id'] for c in new]
print('count new',len(new),'old',len(old),'dup ids',[k for k,v in collections.Counter(ids).items() if v>1])
print('dup fronts',[k for k,v in collections.Counter(c['front'] for c in new).items() if v>1])
print('dup backs',[k for k,v in collections.Counter(c['back'] for c in new).items() if v>1])
print('keys',collections.Counter(tuple(sorted(c)) for c in new))
print('grades',collections.Counter(c['grade'] for c in new))
changed=[c['id'] for c in new if c['id'] in old and c!=old[c['id']]]
added=[c['id'] for c in new if c['id'] not in old]
removed=[k for k in old if k not in set(ids)]
print('changed',len(changed),changed)
print('added',len(added),added[0],added[-1])
print('removed',removed)
print('lessons',collections.Counter(c['lesson'] for c in new))
