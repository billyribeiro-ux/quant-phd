import html, re, subprocess, sys, os, shutil, pathlib
root = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
for lid in ["L01", "L02", "L03", "L04"]:
    page = (root / f"course/modules/LX/LX1/{lid}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin_path = root / f"tests/labs/LX1/lab-LX1-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(lid, "page code == twin:", code == twin, "len", len(code), len(twin))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    # run twin in an empty scratch dir with its data copied
    scratch = pathlib.Path(f"/tmp/lx1d10/run_{lid}")
    shutil.rmtree(scratch, ignore_errors=True)
    (scratch / "data").mkdir(parents=True)
    if lid == "L04":
        shutil.copy(root / "course/assets/data/market/fx_monthly.csv", scratch / "data/fx_monthly.csv")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], cwd=scratch, capture_output=True, text=True)
    (out / f"twin_{lid}.txt").write_text(r.stdout + ("\nSTDERR:\n" + r.stderr if r.stderr else "") + f"\nexit={r.returncode}\n", encoding="utf-8")
    print(lid, "exit", r.returncode, "stderr", repr(r.stderr[:200]))
    print(lid, "expected block == output:", expected.strip() == r.stdout.strip(), "| expected lines", len(expected.strip().splitlines()), "output lines", len(r.stdout.strip().splitlines()))
    if expected.strip() != r.stdout.strip():
        import difflib
        for d in difflib.unified_diff(expected.strip().splitlines(), r.stdout.strip().splitlines(), lineterm="", n=0):
            print("   ", d)
