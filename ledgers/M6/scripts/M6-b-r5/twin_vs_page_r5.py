import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
for n in ["05", "06", "07", "08"]:
    page = (root / f"course/modules/M/M6/L{n}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M6/lab-M6-L{n}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-M6-L%s-1".*?<code class="language-python" data-run>(.*?)</code>' % n, page, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    exp = re.search(r'<section class="lab" id="lab-M6-L%s-1".*?<pre class="expected"[^>]*>(.*?)</pre>' % n, page, re.S)
    expected = html.unescape(exp.group(1))
    out = (root / f"{sys.argv[2]}/lab-L{n}.out").read_text(encoding="utf-8").replace("exit 0\n", "")
    print(n, "code==twin", code.strip() == twin.strip(), "expected==output", expected.strip() == out.strip(), len(code), len(twin))
