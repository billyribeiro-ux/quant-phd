import html, re, sys, subprocess
pages = {"L01": "course/modules/AC/AC1/L01.html", "L02": "course/modules/AC/AC1/L02.html", "L03": "course/modules/AC/AC1/L03.html"}
root = "/tmp/verify13-AC1-a/"
for lid, p in pages.items():
    src = open(root + p, encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1))
    out = subprocess.run([root + ".venv/bin/python", "-I", "-W", "error", root + f"tests/labs/AC1/lab-AC1-{lid}-1.py"], capture_output=True, text=True).stdout
    print(lid, "page expected == twin stdout:", expected.strip() == out.strip(), len(expected), len(out))
    if expected.strip() != out.strip():
        import difflib
        for line in difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm=""):
            print("  ", line)
