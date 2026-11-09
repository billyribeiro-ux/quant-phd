import re, collections, sys
files = ['index.html', 'L01.html', 'L02.html', 'L03.html', 'L04.html', 'L05.html', 'L06.html']
cnt = collections.Counter()
for f in files:
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'\\([A-Za-z]+)', t):
        cnt[m.group(1)] += 1
print(' '.join(f'{k}:{v}' for k, v in sorted(cnt.items(), key=lambda x: -x[1])))
