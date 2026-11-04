import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
for lab, page in (("L03", "course/modules/LX/LX1/L03.html"), ("L04", "course/modules/LX/LX1/L04.html")):
    text = (root / page).read_text(encoding="utf-8")
    twin = (root / f"tests/labs/LX1/lab-LX1-{lab}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = Path(sys.argv[2 + ["L03", "L04"].index(lab)]).read_text(encoding="utf-8")
    print(lab, "code==twin exact:", code == twin, "| code==twin rstrip:", code.rstrip() == twin.rstrip())
    print(lab, "expected==twin stdout exact:", expected == out, "| rstrip:", expected.rstrip() == out.rstrip())
    if expected.rstrip() != out.rstrip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.rstrip().splitlines(), out.rstrip().splitlines(), lineterm="")))
    print(lab, "expected lines:", len(expected.rstrip().splitlines()), "output lines:", len(out.splitlines()))
