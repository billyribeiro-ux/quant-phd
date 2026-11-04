"""Compare each lab block on a BK4 page with its twin: code equals twin source (rstrip per line),
and the expected block equals the output of python3 -I -W error on the twin (tolerance-free text compare)."""
import html, re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])
scripts = Path(sys.argv[2])
for page, lab in (("L01", "lab-BK4-L01-1"), ("L02", "lab-BK4-L02-1"), ("L03", "lab-BK4-L03-1")):
    src = (root / f"course/modules/BK/BK4/{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", code_m.group(1)))
    expected = html.unescape(re.sub(r"<[^>]+>", "", exp_m.group(1)))
    twin = (root / f"tests/labs/BK4/{lab}.py").read_text(encoding="utf-8")
    rs = lambda t: [ln.rstrip() for ln in t.strip("\n").split("\n")]
    code_eq = rs(code) == rs(twin)
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/BK4/{lab}.py")],
                         capture_output=True, text=True, cwd="/tmp")
    out_eq = rs(expected) == rs(run.stdout)
    print(page, lab, "code==twin:", code_eq, "expected==output:", out_eq, "exit:", run.returncode,
          "stderr bytes:", len(run.stderr), "expected lines:", len(rs(expected)), "output lines:", len(rs(run.stdout)))
    if not out_eq:
        import difflib
        for d in difflib.unified_diff(rs(expected), rs(run.stdout), lineterm=""):
            print("   ", d)
    if not code_eq:
        import difflib
        for d in difflib.unified_diff(rs(code), rs(twin), lineterm=""):
            print("   ", d)
