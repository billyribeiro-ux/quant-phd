import json, re, html, sys
base = 'course/modules/M/M2/'
cards = json.load(open(base + 'cards.json'))
slice_lessons = {'L19','L20','L21','L22','L23','L24'}
text = {}
for L in sorted(slice_lessons):
    text[L] = html.unescape(open(base + L + '.html', encoding='utf-8').read())
ids = [c['id'] for c in cards]; fronts = [c['front'] for c in cards]
print('dup ids', len(ids)-len(set(ids)), 'dup fronts', len(fronts)-len(set(fronts)))
num = re.compile(r'\d+(?:\.\d+)?(?:e[+-]?\d+)?')
for c in cards:
    if c['lesson'] not in slice_lessons: continue
    nums = set(num.findall(c['front'] + ' ' + c['back']))
    missing = [n for n in nums if n not in text[c['lesson']]]
    if missing: print('MISSING', c['id'], c['lesson'], missing, '|', c['back'][:120])
print('slice cards', sum(1 for c in cards if c['lesson'] in slice_lessons))
