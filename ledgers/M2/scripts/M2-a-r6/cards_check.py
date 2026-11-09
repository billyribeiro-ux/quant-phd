import json, re, pathlib, sys
root = pathlib.Path(sys.argv[1]) / 'course/modules/M/M2'
cards = json.loads((root / 'cards.json').read_text(encoding='utf-8'))
slice_lessons = {'L01', 'L02', 'L03', 'L04', 'L05', 'L06'}
lesson_text = {}
for L in slice_lessons:
    t = (root / f'{L}.html').read_text(encoding='utf-8')
    t = re.sub(r'\s+', ' ', t.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&'))
    lesson_text[L] = t
kinds = r'(Definition|Proposition|Corollary|Example|Theorem|Lemma|Remark|Misconception|Assumption|Problem|Lab|Section|Problems)\s?(\d+(?:\.\d+)?|[A-Z]\d+(?:\.\d+)?)'
bad = 0
n = 0
for c in cards:
    if c['lesson'] not in slice_lessons:
        continue
    n += 1
    for k, v in set(re.findall(kinds, c['front'] + ' ' + c['back'])):
        tok = f'{k} {v}'
        if tok not in lesson_text[c['lesson']] and not (k == 'Problem' and f'Problem {c["lesson"]}' in tok):
            # Problem ids like L01-R2 not matched by simple pattern; report only
            print('MISSING-TOKEN', c['id'], c['lesson'], repr(tok))
            bad += 1
    for num in set(re.findall(r'(?<![\w.])\d+\.\d+|(?<![\w.])\d+e-\d+', c['back'])):
        if num not in lesson_text[c['lesson']]:
            print('MISSING-NUMBER', c['id'], c['lesson'], num)
            bad += 1
print('slice cards', n, 'flags', bad)
