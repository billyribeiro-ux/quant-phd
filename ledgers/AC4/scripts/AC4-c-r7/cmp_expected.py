import html, re, subprocess, sys
root = "/tmp/verify7-AC4-c"
py = f"{root}/.venv/bin/python"
pairs = {"L05": ("tests/labs/AC4/lab-AC4-L05-1.py", "course/modules/AC/AC4/L05.html"),
         "L06": ("tests/labs/AC4/lab-AC4-L06-1.py", "course/modules/AC/AC4/L06.html")}
for name, (twin, page) in pairs.items():
    text = open(f"{root}/{page}", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(m.group(1)).strip()
    if len(sys.argv) > 1:
        target = sys.argv[1]
        out = subprocess.run([py, "-I", "-W", "error", target], capture_output=True, text=True).stdout.strip()
        print(name, "mutant", target.split("/")[-1], "MATCH" if out == expected else "DIFFERS")
        continue
    out = subprocess.run([py, "-I", "-W", "error", f"{root}/{twin}"], capture_output=True, text=True).stdout.strip()
    print(name, "twin vs page expected:", "MATCH" if out == expected else "DIFFERS", "lines", len(expected.splitlines()))
