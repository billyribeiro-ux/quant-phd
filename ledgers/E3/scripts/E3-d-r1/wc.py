import re, html, sys
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
def block(lines_from, lines_to):
    return '\n'.join(src[lines_from-1:lines_to])
def memo_divs(text):
    # extract content of every <div class="memo-text"> ... </div> (non-nested divs inside)
    out = []
    for m in re.finditer(r'<div class="memo-text">(.*?)</div>', text, re.S):
        out.append(m.group(1))
    return out
def count_literal(s):
    t = re.sub(r'<[^>]+>', '', s)
    t = html.unescape(t)
    return len(t.split())
def count_block(s):
    t = re.sub(r'</?(h[1-6]|p|li|ul|div|br|tr|td|th|section|article|aside|table|dd|dt)\b[^>]*>', ' ', s)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    return len(t.split())
A = block(650, 702); B = block(703, 766)
for name, txt in [('A', A), ('B', B)]:
    ds = memo_divs(txt)
    print(name, 'memo-text divs:', len(ds))
    print(' literal words (tags removed, no separators):', sum(count_literal(d) for d in ds))
    print(' block-tags-as-breaks:', sum(count_block(d) for d in ds))
    # whole article text, tags removed, no separators (annotation included for comparison)
    print(' whole article literal (incl. verdict/annotations):', count_literal(txt))
