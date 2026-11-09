import re, sys, html, json
root = sys.argv[1]
spec = sys.argv[2:]  # pairs: LESSON:LOCATOR  e.g. L05:Definition 2.1 ; LOCATOR may be 'section 5' etc
def strip(t):
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()
for item in spec:
    lesson, loc = item.split(':', 1)
    src = open(f'{root}/course/modules/E/E3/{lesson}.html', encoding='utf-8').read()
    # block titles and problem titles
    pos = None
    for m in re.finditer(r'(<span class="block-title[^>]*>|<span class="problem-title">|<h[23][^>]*>)', src):
        seg = strip(src[m.start():m.start()+400])
        if seg.startswith(loc + ' ') or seg.startswith(loc + '<') or seg.startswith(loc + '(') or seg.startswith(loc+' ·') or seg.startswith(loc):
            pos = m.start(); break
    if pos is None:
        print(f'## {lesson}:{loc} NOT FOUND'); continue
    chunk = src[pos:pos+2600]
    end = chunk.find('</div>')
    txt = strip(chunk[:end if end > 0 else 1500])
    print(f'## {lesson}:{loc} :: {txt[:900]}')
