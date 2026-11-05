import re, html, sys
page = open('course/modules/LX/LX1/project.html', encoding='utf-8').read()
for n in (1, 2, 3):
    m = re.search(r'<section class="lab[^"]*" id="lab-LX1-project-%d".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % n, page, re.S)
    code = html.unescape(m.group(1)); exp = html.unescape(m.group(2))
    twin = open('tests/labs/LX1/lab-LX1-project-%d.py' % n, encoding='utf-8').read()
    print('lab', n, 'code==twin (rstrip):', code.rstrip() == twin.rstrip(), 'exact:', code == twin, 'len page', len(code), 'len twin', len(twin))
    if code.rstrip() != twin.rstrip():
        import difflib
        print(''.join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), 'twin', 'page'))[:3000])
    out = open('/tmp/lx1c-r8-blind/twin%d.out' % n if n != 3 else '/tmp/lx1c-r8-blind/twin3.out', encoding='utf-8').read()
    print('lab', n, 'expected==output:', exp.strip() == out.strip())
    if exp.strip() != out.strip():
        import difflib
        print(''.join(difflib.unified_diff(out.splitlines(True), exp.splitlines(True), 'out', 'expected'))[:2000])
    print('lab', n, 'exp lines', len(exp.splitlines()))
