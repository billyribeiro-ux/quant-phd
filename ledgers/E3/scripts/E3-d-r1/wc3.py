import re, sys, html
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
def region(a,b): return '\n'.join(src[a-1:b])
for name,a,b in [('A',650,702),('B',703,766)]:
    r = region(a,b)
    memos = re.findall(r'<div class="memo-text">(.*?)\n\s*</div>', r, re.S)
    # proper tag pattern: only '<' followed by letter or '/' letter starts a tag
    tot_plain = 0; tot_sep = 0
    for m in memos:
        t = re.sub(r'</?[a-zA-Z][^>]*>', '', m)
        tot_plain += len(html.unescape(t).split())
        t2 = re.sub(r'</?[a-zA-Z][^>]*>', ' ', m)
        tot_sep += len(html.unescape(t2).split())
    print(name, 'memo divs', len(memos), 'plain', tot_plain, 'tags-as-space', tot_sep)
# adjacency check: block close/open with no whitespace between
txt = region(703,766)
