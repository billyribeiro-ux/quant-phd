"""Compare each E5 L04-L06 page's lab code and expected block against its twin and the twin's stdout."""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
for lesson in ("L04", "L05", "L06"):
    page = (ROOT / f"course/modules/E/E5/{lesson}.html").read_text(encoding="utf-8")
    twin_name = f"lab-E5-{lesson}-1"
    twin = (ROOT / f"tests/labs/E5/{twin_name}.py").read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab" id="%s".*?</section>' % twin_name, page, re.S)
    if not sec:
        print(lesson, "NO LAB SECTION")
        continue
    body = sec.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    print(lesson, "page code equals twin (rstrip):", code.rstrip() == twin.rstrip())
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E5/{twin_name}.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(lesson, "twin exit", out.returncode, "stderr bytes", len(out.stderr.encode()))
    print(lesson, "expected block equals twin stdout (rstrip):", exp.rstrip() == out.stdout.rstrip())
    if exp.rstrip() != out.stdout.rstrip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.rstrip().splitlines(), out.stdout.rstrip().splitlines(), lineterm="")))
    print(lesson, "expected lines:", len(exp.splitlines()), "stdout lines:", len(out.stdout.splitlines()))
