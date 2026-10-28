import sys, re, html
page, twin = sys.argv[1], sys.argv[2]
s = open(page, encoding='utf-8').read()
m = re.search(r'<code class="language-python" data-run>(.*?)</code>', s, re.S)
code = html.unescape(m.group(1))
t = open(twin, encoding='utf-8').read()
print(page.split('/')[-1], 'embedded==twin:', code.strip() == t.strip(), len(code), len(t))
