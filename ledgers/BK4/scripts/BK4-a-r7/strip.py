import re, sys, html
# Strip only real tags: '<' followed by a letter, '/' or '!'. A bare '<' in math (e.g. \(\mu < 0\)) is kept.
TAG = re.compile(r'</?[A-Za-z!][^>]*>')
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
for n, line in enumerate(src, 1):
    t = TAG.sub('', line)
    t = html.unescape(t).strip()
    if t:
        print(f"{n}: {t}")
