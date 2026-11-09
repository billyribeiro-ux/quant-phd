import re, html, sys, difflib
page = open('course/modules/FC/FC2/project.html', encoding='utf-8').read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
print('python data-run blocks on page:', len(blocks))
for i, b in enumerate(blocks, 1):
    code = html.unescape(b)
    open(f'{sys.argv[1]}/page-block-{i}.py', 'w', encoding='utf-8').write(code if code.endswith('\n') else code + '\n')
    print(i, 'lines', code.count('\n'), 'first line:', code.splitlines()[0][:90])
for i, t in enumerate(['lab-FC2-project-1.py', 'lab-FC2-project-2.py', 'lab-FC2-project-3.py'], 1):
    tw = open('tests/labs/FC2/' + t, encoding='utf-8').read()
    pg = open(f'{sys.argv[1]}/page-block-{i}.py', encoding='utf-8').read()
    d = list(difflib.unified_diff(tw.splitlines(), pg.splitlines(), 'twin:' + t, 'page-block-%d' % i, lineterm='', n=0))
    print(t, 'identical' if tw == pg else f'DIFF lines={len(d)}')
    for line in d[:40]: print('   ', line[:160])
