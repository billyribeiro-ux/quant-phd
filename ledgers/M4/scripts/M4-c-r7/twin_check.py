import re, html, sys
root = sys.argv[1]
for t in ["L08", "L09", "L10"]:
    s = open(f"{root}/course/modules/M/M4/{t}.html", encoding="utf-8").read()
    code = html.unescape(re.sub(r"<[^>]+>", "", re.findall(r"<pre>(.*?)</pre>", s, re.S)[0]))
    exp = html.unescape(re.sub(r"<[^>]+>", "", re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)[0]))
    twin = open(f"{root}/tests/labs/M4/lab-M4-{t}-1.py", encoding="utf-8").read()
    out = open(f"/tmp/m4c_{t}-r7.out", encoding="utf-8").read()
    print(t, "code==twin (modulo final newline):", code + "\n" == twin, "| expected==output (modulo final newline):", exp.rstrip("\n") == out.rstrip("\n"))
