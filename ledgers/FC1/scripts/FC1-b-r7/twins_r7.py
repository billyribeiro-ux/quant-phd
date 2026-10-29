import re, subprocess, sys, html, pathlib, difflib
root = pathlib.Path(sys.argv[1])
for lab, page in [("L04", "course/modules/FC/FC1/L04.html"), ("L05", "course/modules/FC/FC1/L05.html")]:
    src = (root / page).read_text(encoding="utf-8")
    twin = (root / f"tests/labs/FC1/lab-FC1-{lab}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    print(lab, "page_code==twin:", code.strip() == twin.strip(), len(code), len(twin))
    if code.strip() != twin.strip():
        print("".join(list(difflib.unified_diff(twin.splitlines(1), code.splitlines(1)))[:40]))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC1/lab-FC1-{lab}-1.py")], capture_output=True, text=True)
    print(lab, "twin rc", r.returncode, "stderr bytes", len(r.stderr))
    ex = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    print(lab, "expected blocks:", len(ex))
    for e in ex:
        et = html.unescape(re.sub(r"<[^>]+>", "", e))
        print(lab, "expected==stdout:", et.strip() == r.stdout.strip())
        if et.strip() != r.stdout.strip():
            print("".join(list(difflib.unified_diff(r.stdout.splitlines(1), et.splitlines(1)))[:40]))
