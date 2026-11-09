import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
PY = str(root / ".venv/bin/python")
pages = {"L01": "lab-LX1-L01-1", "L03": "lab-LX1-L03-1", "L04": "lab-LX1-L04-1"}
for lid, twin in pages.items():
    page = (root / f"course/modules/LX/LX1/{lid}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    tw = (root / f"tests/labs/LX1/{twin}.py").read_text(encoding="utf-8")
    print(lid, "page code == twin:", code.strip() == tw.strip(), len(code), len(tw))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
    if lid == "L04":
        cwd = root / "tests/labs/LX1"
        # data path is data/fx_monthly.csv relative to cwd
        data_src = root / "course/assets/data/market/fx_monthly.csv"
        import tempfile, shutil, os
        d = tempfile.mkdtemp(prefix="l04lab_")
        os.makedirs(os.path.join(d, "data"))
        shutil.copy(data_src, os.path.join(d, "data", "fx_monthly.csv"))
        out = subprocess.run([PY, "-I", "-W", "error", str(root / f"tests/labs/LX1/{twin}.py")], cwd=d, capture_output=True, text=True)
    else:
        out = subprocess.run([PY, "-I", "-W", "error", str(root / f"tests/labs/LX1/{twin}.py")], capture_output=True, text=True)
    print(lid, "exit", out.returncode, "stderr-empty", out.stderr == "")
    print(lid, "output == page expected:", out.stdout.strip() == exp.strip(), "lines", len(out.stdout.splitlines()))
    if out.stdout.strip() != exp.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.stdout.strip().splitlines(), lineterm="")))
