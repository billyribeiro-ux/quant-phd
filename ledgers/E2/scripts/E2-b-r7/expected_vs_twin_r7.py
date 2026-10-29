import html, re, sys
# compare each page's expected block with the twin's actual output (run in r7 scripts dir)
pages = {"04": "course/modules/E/E2/L04.html", "05": "course/modules/E/E2/L05.html", "06": "course/modules/E/E2/L06.html"}
root = sys.argv[1]
for n, p in pages.items():
    src = open(f"{root}/{p}", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    exp = html.unescape(m.group(1))
    out = open(f"{root}/ledgers/E2/scripts/E2-b-r7/twin_L{n}.out", encoding="utf-8").read()
    print(n, "expected == twin output:", exp.strip() == out.strip(), "lines", len(out.splitlines()))
