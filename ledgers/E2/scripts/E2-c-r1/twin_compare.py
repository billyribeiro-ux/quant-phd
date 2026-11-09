import html, re, subprocess, sys, pathlib, tempfile, shutil
root = pathlib.Path(sys.argv[1])
pages = {"L07": "course/modules/E/E2/L07.html", "L08": "course/modules/E/E2/L08.html", "L09": "course/modules/E/E2/L09.html"}
for p, rel in pages.items():
    src = (root / rel).read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    lab = re.search(r'data-lab="([^"]+)"|id="(lab-E2-[^"]+)"', src)
    twin_name = re.search(r"(lab-E2-L\d\d-\d)", src)
    twin_src = (root / "tests/labs/E2" / (twin_name.group(1) + ".py")).read_text(encoding="utf-8") if twin_name else None
    page_code = html.unescape(m.group(1))
    print(p, "twin file:", twin_name.group(1) if twin_name else None, "data-run len", len(page_code), "twin len", len(twin_src or ""))
    print(p, "page code == twin (exact):", page_code == twin_src, "| rstrip-equal:", page_code.rstrip() == (twin_src or "").rstrip())
    d = tempfile.mkdtemp(prefix="e2c_run_")
    try:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/E2" / (twin_name.group(1) + ".py"))],
                           cwd=d, capture_output=True, text=True, timeout=120)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print(p, "exit", r.returncode, "stderr bytes", len(r.stderr))
    expected = html.unescape(e.group(1))
    print(p, "expected == stdout (strip):", expected.strip() == r.stdout.strip(), "| expected len", len(expected.strip()), "stdout len", len(r.stdout.strip()))
    if expected.strip() != r.stdout.strip():
        print("DIFF expected:", repr(expected[:300])); print("DIFF stdout:", repr(r.stdout[:300]))
