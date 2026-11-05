# For each PC3 lesson page in the slice: compare the embedded data-run code with the twin file,
# and the expected block with the twin's actual stdout (run under python -I -W error).
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
pages = {"L01": "lab-PC3-L01-1", "L02": "lab-PC3-L02-1", "L03": "lab-PC3-L03-1"}
ok = True
for page, lab in pages.items():
    text = (root / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/PC3/{lab}.py").read_text(encoding="utf-8")
    same_code = code.strip() == twin.strip()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1)).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/PC3/{lab}.py")],
                         capture_output=True, text=True).stdout.strip()
    same_out = expected == out
    print(page, "code==twin:", same_code, "expected==stdout:", same_out, "lines:", len(out.splitlines()))
    ok = ok and same_code and same_out
print("ALL OK" if ok else "MISMATCH")
