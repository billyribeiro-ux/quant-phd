"""Compare each page's <code data-run> block with its lab twin, and the expected block with a fresh run (FC2-a r3)."""
import html, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
for lid, page in [("lab-FC2-L01-1", "L01"), ("lab-FC2-L02-1", "L02"), ("lab-FC2-L03-1", "L03")]:
    text = (root / "course/modules/FC/FC2" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="%s".*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lid, text, re.S)
    code = html.unescape(m.group(1)); expected = html.unescape(m.group(2))
    twin = (root / "tests/labs/FC2" / f"{lid}.py").read_text(encoding="utf-8")
    print(lid, "page code == twin:", code == twin, "len", len(code), len(twin))
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:40]))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/FC2" / f"{lid}.py")], capture_output=True, text=True)
    print(lid, "twin exit", out.returncode, "stdout == expected:", out.stdout.rstrip("\n") == expected.rstrip("\n"))
