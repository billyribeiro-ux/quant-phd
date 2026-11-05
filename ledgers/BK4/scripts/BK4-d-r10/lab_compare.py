"""Compare each BK4 lesson lab on the page with its twin and with the twin's observed output.

Checks: (1) the code inside <code data-run> equals tests/labs/BK4/<lab>.py (HTML-unescaped);
(2) the <pre class="expected"> block equals the stdout of the twin run under python -I -W error.
Usage: python -I lab_compare.py <checkout_root> <twin_output_dir>
"""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
outdir = pathlib.Path(sys.argv[2])
labs = [("L01", "lab-BK4-L01-1"), ("L02", "lab-BK4-L02-1"), ("L03", "lab-BK4-L03-1"),
        ("L04", "lab-BK4-L04-1"), ("L05", "lab-BK4-L05-1")]
for page, lab in labs:
    src = (root / f"course/modules/BK/BK4/{page}.html").read_text(encoding="utf-8")
    sec = re.search(rf'<section class="lab[^"]*" id="{lab}".*?</section>', src, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/BK4/{lab}.py").read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/BK4/{lab}.py")],
                         capture_output=True, text=True, timeout=120)
    out_eq = run.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab}: page code equals twin: {code_eq}; twin exit {run.returncode}; stderr bytes {len(run.stderr)}; "
          f"expected block equals twin stdout: {out_eq}")
    if not code_eq:
        print("  code differs; first differing line index:",
              next((i for i, (a, b) in enumerate(zip(code.splitlines(), twin.splitlines())) if a != b), "len"))
    if not out_eq:
        print("  expected lines:", len(expected.splitlines()), "output lines:", len(run.stdout.splitlines()))
    (outdir / f"{lab}.stdout").write_text(run.stdout, encoding="utf-8")
