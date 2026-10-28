import sys, re, html
page, out = sys.argv[1], sys.argv[2]
s = open(page, encoding='utf-8').read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
exp = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
got = open(out, encoding='utf-8').read()
print('expected lines', len(exp.splitlines()), 'got lines', len(got.splitlines()), 'identical:', exp.strip() == got.strip())
if exp.strip() != got.strip():
    import difflib
    print('\n'.join(list(difflib.unified_diff(exp.strip().splitlines(), got.strip().splitlines(), lineterm=''))[:40]))
