"""Exact check: each changed lesson's expected block equals the twin's stdout; page code equals twin."""
import html, re, subprocess, sys, tempfile, os, pathlib
root = pathlib.Path(sys.argv[1])
pages = {"L01": "lab-E3-L01-1.py", "L03": "lab-E3-L03-1.py", "L05": "lab-E3-L05-1.py", "L06": "lab-E3-L06-1.py", "L08": "lab-E3-L08-1.py", "L04": None, "L07": None, "L02": None}
for page, twin in pages.items():
    text = (root / "course/modules/E/E3" / f"{page}.html").read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    print(f"{page}: run-blocks={len(codes)} expected-blocks={len(exps)}")
    if not twin:
        continue
    src = (root / "tests/labs/E3" / twin).read_text(encoding="utf-8")
    code = html.unescape(codes[0])
    print(f"  page code == twin: {code.rstrip(chr(10)) == src.rstrip(chr(10))}")
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/E3" / twin)], cwd=d, capture_output=True, text=True, timeout=600)
    print(f"  exit {r.returncode} stderr_bytes {len(r.stderr)}")
    out = r.stdout
    for i, e in enumerate(exps):
        ev = html.unescape(e)
        print(f"  expected[{i}] == stdout: {ev.strip() == out.strip()}  (len {len(ev.strip())} vs {len(out.strip())})")
    print(f"  stdout lines {len(out.splitlines())}")
