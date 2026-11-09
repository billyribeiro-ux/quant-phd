import json,sys
b=json.load(open(sys.argv[1])); h=json.load(open(sys.argv[2]))
print('keys sample', list(b[0].keys()))
bi={c['id']:c for c in b}; hi={c['id']:c for c in h}
print('base ids', len(bi), 'head ids', len(hi))
print('removed', sorted(set(bi)-set(hi)))
print('added', sorted(set(hi)-set(bi)))
ch=[k for k in sorted(set(bi)&set(hi)) if bi[k]!=hi[k]]
print('changed', ch)
for k in ch:
    print('==', k)
    for f in sorted(set(bi[k])|set(hi[k])):
        if bi[k].get(f)!=hi[k].get(f):
            print('  field', f)
            print('   BASE:', json.dumps(bi[k].get(f),ensure_ascii=False))
            print('   HEAD:', json.dumps(hi[k].get(f),ensure_ascii=False))
