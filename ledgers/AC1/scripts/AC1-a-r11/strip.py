import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read().splitlines()
for i, line in enumerate(src, 1):
    if re.search(r'<pre class="expected"', line) or re.search(r'<pre><code', line):
        pass
    t = re.sub(r'<[^>]+>', '', line)
    t = html.unescape(t).strip()
    if t:
        print(f"{i}: {t}")
