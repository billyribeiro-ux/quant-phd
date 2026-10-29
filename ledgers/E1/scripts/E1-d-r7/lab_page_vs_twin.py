import html, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
page = (root / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-E1-project-{n}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/E1/lab-E1-project-{n}.py").read_text(encoding="utf-8")
    print(f"lab {n}: page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)")
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:40]))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E1/lab-E1-project-{n}.py")], capture_output=True, text=True).stdout
    print(f"lab {n}: twin output == expected block: {out.strip() == exp.strip()}")
    if out.strip() != exp.strip():
        print("OUT:\n" + out + "EXP:\n" + exp)
