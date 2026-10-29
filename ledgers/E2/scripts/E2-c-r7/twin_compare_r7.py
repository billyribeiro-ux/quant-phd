import re, sys, html, pathlib
root = pathlib.Path(sys.argv[1])
for p in ["L07", "L08", "L09"]:
    page = (root / f"course/modules/E/E2/{p}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/E2/lab-E2-{p}-1.py").read_text(encoding="utf-8")
    m = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = [html.unescape(x) for x in m]
    print(p, "data-run blocks:", len(m), "equal_to_twin:", [c == twin for c in code])
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    print(p, "expected blocks:", len(exp))
    for e in exp:
        print("  expected_block_len", len(html.unescape(e)))
