"""Round 3 M2-a: internal links and anchors on the hub and L01-L06; embedded lab code and expected output
against the twins, and against a fresh run under python -I -W error."""
import html, os, re, subprocess, sys
ROOT = "/tmp/verifyB3-M2-a"
os.chdir(ROOT)
M2 = os.path.join(ROOT, "course/modules/M/M2")
bad = []
pages = ["index.html"] + [f"L0{i}.html" for i in range(1, 7)]
for p in pages:
    s = open(os.path.join(M2, p), encoding="utf8").read()
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith(("http", "#", "mailto")):
            continue
        f = href.split("#")[0]
        if not f:
            continue
        path = os.path.normpath(os.path.join(M2, f))
        if not os.path.exists(path):
            bad.append((p, href))
        elif "#" in href and path.endswith(".html"):
            if f'id="{href.split("#")[1]}"' not in open(path, encoding="utf8").read():
                bad.append((p, href, "anchor"))
print("broken links or anchors:", bad)
for i in range(1, 7):
    s = open(os.path.join(M2, f"L0{i}.html"), encoding="utf8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', s, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1)).strip()
    twin = open(f"tests/labs/M2/lab-M2-L0{i}-1.py", encoding="utf8").read()
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"tests/labs/M2/lab-M2-L0{i}-1.py"],
                         capture_output=True, text=True).stdout.strip()
    print(f"L0{i}: embedded code == twin {code.strip() == twin.strip()}; expected == run {exp == out}")
