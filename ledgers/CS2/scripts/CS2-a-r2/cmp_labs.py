"""Compare each CS2 slice-a lab page's embedded code and expected block with its twin, and run the twin."""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
PAGES = ["L01", "L02", "L03", "L04"]
for lid in PAGES:
    page = (ROOT / "course/modules/CS/CS2" / f"{lid}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    embedded = html.unescape(code.group(1))
    exp = html.unescape(expected.group(1))
    twin_path = ROOT / "tests/labs" / "CS2" / f"lab-CS2-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = embedded.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run(
        [str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(twin_path)],
        capture_output=True, text=True, timeout=120,
    )
    out_ok = run.stdout.rstrip("\n") == exp.rstrip("\n")
    print(f"{lid}: embedded==twin {same}; run exit {run.returncode}; stderr_empty {run.stderr.strip()==''}; stdout==expected {out_ok}")
    if not out_ok:
        import difflib
        for line in difflib.unified_diff(exp.splitlines(), run.stdout.splitlines(), lineterm="", n=0):
            print("   ", line)
