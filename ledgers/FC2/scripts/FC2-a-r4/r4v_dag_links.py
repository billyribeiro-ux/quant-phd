"""DAG and link check for FC2 slice a (index, L01-L03): every concept link resolves to a concepts.html id or an
earlier in-unit definition; every in-unit dfn with data-concept is defined once; every href target exists."""
import re, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
MOD = ROOT / 'course/modules/FC/FC2'
concepts = (ROOT / 'course/concepts.html').read_text(encoding='utf-8')
concept_ids = set(re.findall(r'id="([^"]+)"', concepts))
order = ['L01.html', 'L02.html', 'L03.html']
defined_so_far = set()
fails = 0
for page in ['index.html'] + order:
    raw = (MOD / page).read_text(encoding='utf-8')
    for m in re.finditer(r'<a class="concept"[^>]*data-concept="([^"]+)"[^>]*href="([^"]+)"', raw):
        cid, href = m.group(1), m.group(2)
        if href.startswith('../../../concepts.html#'):
            tgt = href.split('#', 1)[1]
            if tgt not in concept_ids or tgt != cid:
                print('BAD concept href', page, cid, href); fails += 1
        elif href.startswith('L') and '#' in href:
            file, frag = href.split('#', 1)
            if file not in order or frag != f'def-{cid}':
                print('BAD in-unit href', page, cid, href); fails += 1
            elif order.index(file) >= order.index(page) if page in order else False:
                print('FORWARD in-unit link', page, cid, href); fails += 1
            elif cid not in defined_so_far:
                print('link to concept not yet defined in its lesson', page, cid); fails += 1
        else:
            print('OTHER href', page, cid, href)
    for m in re.finditer(r'<dfn id="(def-[^"]+)" data-concept="([^"]+)"', raw):
        if m.group(2) in defined_so_far:
            print('DUPLICATE dfn', page, m.group(2)); fails += 1
        defined_so_far.add(m.group(2))
    for href in re.findall(r'href="([^"#]+)(?:#[^"]*)?"', raw):
        if href.startswith('http') or href.startswith('//'):
            print('EXTERNAL', page, href); fails += 1
        elif href and not href.startswith('mailto'):
            if not (MOD / href).exists() and not (MOD / '..' / href).exists():
                p = (MOD / href).resolve()
                if not p.exists():
                    print('MISSING href target', page, href); fails += 1
print('dag/link failures:', fails)
print('defined in unit (L01-L03):', sorted(defined_so_far))
