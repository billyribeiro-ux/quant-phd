import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for t in ("L07", "L08"):
    page = (root / f"course/modules/AC/AC4/{t}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(m.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{t}-1.py")], capture_output=True, text=True).stdout
    print(t, "expected block equals twin stdout:", exp.strip() == out.strip(), "lines", len(out.splitlines()))
