import re, html, subprocess, sys, pathlib
ROOT = pathlib.Path(sys.argv[1]); PY = str(ROOT / ".venv/bin/python")
for f in sorted(pathlib.Path(sys.argv[2]).glob("mut*_L0*.py")):
    lab = f.stem.split("_")[-1]
    page = (ROOT / f"course/modules/CF/CF1/{lab}.html").read_text(encoding="utf-8")
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip().splitlines()
    r = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True)
    got = r.stdout.strip().splitlines()
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(exp, got)) if a != b]
    print(f.name, "rc", r.returncode, "lines", len(exp), len(got), "first diff:", diffs[0] if diffs else "none")
