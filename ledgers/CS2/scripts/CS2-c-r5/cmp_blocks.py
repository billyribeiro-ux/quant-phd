import re, html
base = '/tmp/verifyB5-CS2-c/course/modules/CS/CS2/'
for page, out in [('L09', '/tmp/cs2c_l09.out'), ('L10', '/tmp/cs2c_l10.out'), ('L11', '/tmp/cs2c_l11.out')]:
    t = open(base + page + '.html', encoding='utf-8').read()
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S).group(1))
    run = open(out).read()
    print(page, 'expected==run:', exp.strip() == run.strip())
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S).group(1))
    tw = open(f'/tmp/verifyB5-CS2-c/tests/labs/CS2/lab-CS2-{page}-1.py', encoding='utf-8').read()
    print(page, 'code==twin:', code.strip() == tw.strip())
