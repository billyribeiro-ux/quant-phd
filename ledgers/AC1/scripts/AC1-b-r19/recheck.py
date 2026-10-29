import json, collections, re, html
print(3319293/27832482, 14820224/91239905, 4974286, 3664530+2443020*0)
print(sorted(collections.Counter(c['id'] for c in json.load(open('course/modules/AC/AC1/cards.json'))).items(), key=lambda x:-x[1])[:2])
cards = json.load(open('course/modules/AC/AC1/cards.json'))
print('cards', len(cards), 'L04', sum(c['lesson']=='L04' for c in cards), 'L05', sum(c['lesson']=='L05' for c in cards), 'L06', sum(c['lesson']=='L06' for c in cards))
for c in cards:
    if c['id'] in ('AC1-c069','AC1-c066','AC1-c053','AC1-c140'): print(c['id'], c['back'])
# which Remark/Definition contains the 'convention-1 revenue ... over-time' sentence in L05
t = open('course/modules/AC/AC1/L05.html').read()
for m in re.finditer(r'<(p|div)[^>]*>(.*?)</\1>', t, re.S):
    if 'over-time obligations through month' in m.group(2) or 'from the over-time obligations' in m.group(2):
        print('FOUND in block starting:', html.unescape(re.sub('<[^>]+>','',m.group(2)))[:90], '| line', t[:m.start()].count('\n')+1)
