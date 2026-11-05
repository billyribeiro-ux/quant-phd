"""SC1-b round 7: page lab code equals twin; expected block equals twin stdout (python -I -W error)."""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
PAGES = {"L04": "lab-SC1-L04-1", "L05": "lab-SC1-L05-1", "L06": "lab-SC1-L06-1"}
pat = re.compile(
    r'<section class="lab" id="(?P<id>[^"]+)" data-runtime="python">.*?'
    r'<code class="language-python" data-run>(?P<code>.*?)</code></pre>\s*'
    r'<pre class="expected"[^>]*>(?P<expected>.*?)</pre>',
    re.S,
)
ok = True
for page, lab in PAGES.items():
    text = (ROOT / "course/modules/SC/SC1" / f"{page}.html").read_text(encoding="utf-8")
    m = pat.search(text)
    if not m or m.group("id") != lab:
        print(page, "NO MATCH"); ok = False; continue
    code = html.unescape(m.group("code"))
    expected = html.unescape(m.group("expected"))
    twin = (ROOT / "tests/labs/SC1" / f"{lab}.py").read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as d:
        out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/SC1" / f"{lab}.py")],
                             cwd=d, capture_output=True, text=True)
    stdout_eq = out.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{page} lab={lab} page_code_equals_twin={code_eq} expected_equals_stdout={stdout_eq} "
          f"rc={out.returncode} stderr_bytes={len(out.stderr)} expected_lines={len(expected.splitlines())}")
    ok = ok and code_eq and stdout_eq and out.returncode == 0 and not out.stderr
print("ALL PASS" if ok else "FAIL")
