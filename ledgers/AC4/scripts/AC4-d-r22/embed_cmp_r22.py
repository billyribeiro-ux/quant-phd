import html, re, subprocess, sys
root = sys.argv[1]
for t in ("L07", "L08"):
    page = open(f"{root}/course/modules/AC/AC4/{t}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/AC4/lab-AC4-{t}-1.py"], capture_output=True, text=True).stdout.strip()
    print(t, "embedded==run:", exp == out, "lines", len(exp.splitlines()))
