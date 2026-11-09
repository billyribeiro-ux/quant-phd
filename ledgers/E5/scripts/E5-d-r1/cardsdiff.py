import json,subprocess,difflib,sys
c=json.load(open('course/modules/E/E5/cards.json'))
old=json.loads(subprocess.run(['git','show','04626e9:course/modules/E/E5/cards.json'],capture_output=True,text=True).stdout)
om={x['id']:x for x in old}
out=[]
for x in c:
    i=x['id']
    if i not in om:
        out.append(f"### NEW {i} [{x['lesson']}] grade={x.get('grade')} basis={x.get('basis')}\nFRONT: {x['front']}\nBACK: {x['back']}")
        continue
    o=om[i]
    if o==x: continue
    out.append(f"### CHG {i} [{x['lesson']}] grade={x.get('grade')} basis={x.get('basis')}")
    for f in ('front','back','grade','basis'):
        if o.get(f)!=x.get(f):
            a=(o.get(f) or '').split(' '); b=(x.get(f) or '').split(' ')
            sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
            s=[]
            for tag,i1,i2,j1,j2 in sm.get_opcodes():
                if tag=='equal': s.append(' '.join(a[i1:i2]))
                else:
                    if i2>i1: s.append('[-'+' '.join(a[i1:i2])+'-]')
                    if j2>j1: s.append('{+'+' '.join(b[j1:j2])+'+}')
            out.append(f"{f.upper()}: "+' '.join(s))
open('/tmp/e5r1/cards_delta.txt','w').write('\n'.join(out))
print(len(out))
