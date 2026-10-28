import html, re, subprocess, sys
root = "/tmp/verify30-AC4-a"
for lab, page in (("L01", "course/modules/AC/AC4/L01.html"), ("L02", "course/modules/AC/AC4/L02.html")):
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py"],
                         capture_output=True, text=True).stdout
    txt = open(f"{root}/{page}", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', txt, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    print(lab, "equal" if exp.strip() == out.strip() else "DIFF", len(out.splitlines()), "lines")
