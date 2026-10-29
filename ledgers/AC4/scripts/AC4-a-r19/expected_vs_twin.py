import html, re, subprocess, sys
root = "/tmp/verify19-AC4-a"
for lab, page in (("L01", "L01"), ("L02", "L02")):
    src = open(f"{root}/course/modules/AC/AC4/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip("\n")
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py"],
                         capture_output=True, text=True, cwd="/tmp").stdout.strip("\n")
    print(lab, "page line", src[:m.start()].count("\n") + 1, "expected lines", exp.count("\n") + 1,
          "stdout lines", out.count("\n") + 1, "IDENTICAL" if exp == out else "DIFFERENT")
