import html, re, subprocess, sys
root = "/tmp/verifyB4-E1-a"
for lid, page in [("L01-1", "L01"), ("L02-1", "L02"), ("L03-1", "L03")]:
    src = open(f"{root}/course/modules/E/E1/{page}.html", encoding="utf-8").read()
    pres = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E1/lab-E1-{lid}.py"],
                         capture_output=True, text=True).stdout
    for i, p in enumerate(pres):
        exp = html.unescape(p).strip()
        print(page, "expected block", i, "lines", len(exp.splitlines()), "matches run:", exp == out.strip())
    print(page, "run lines", len(out.strip().splitlines()))
