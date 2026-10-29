import json,re,html
cards=json.load(open('cards.json'))
raw={}
for i in range(1,11):
    raw[f'L{i:02d}']=open(f'L{i:02d}.html',encoding='utf-8').read()
miss=[]
for c in cards:
    back=c['back']
    toks=re.findall(r'\d+(?:\.\d+)?(?:/\d+)?',back)
    txt=html.unescape(raw[c['lesson']]).replace('\\','')
    txt2=re.sub(r'\s','',txt)
    for t in toks:
        if t in ('0','1','2','3','4','5'): continue
        if t not in txt and t.replace(' ','') not in txt2:
            miss.append((c['id'],c['lesson'],t))
print('tokens not found in own lesson html:',len(miss))
for m in miss: print(m)
