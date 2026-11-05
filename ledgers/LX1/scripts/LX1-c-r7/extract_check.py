import html, re, sys, difflib, subprocess, os, shutil, tempfile, pathlib
ROOT = pathlib.Path(sys.argv[1])
page = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("lab blocks on page:", len(blocks))
for i, (code, expected) in enumerate(blocks, 1):
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (ROOT / f"tests/labs/LX1/lab-LX1-project-{i}.py").read_text(encoding="utf-8")
    same = code == twin
    print(f"lab {i}: page_code==twin {same}; code_lines={code.count(chr(10))} twin_lines={twin.count(chr(10))}")
    if not same:
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
            print("   ", line)
    tmp = tempfile.mkdtemp(prefix="lx1c-r7-")
    os.makedirs(os.path.join(tmp, "data"))
    shutil.copy(ROOT / "course/assets/data/market/fx_monthly.csv", os.path.join(tmp, "data/fx_monthly.csv"))
    script = os.path.join(tmp, f"lab{i}.py")
    open(script, "w", encoding="utf-8").write(twin)
    r = subprocess.run([sys.executable, "-I", "-W", "error", script], cwd=tmp, capture_output=True, text=True)
    print(f"lab {i}: twin rc={r.returncode} stderr_empty={r.stderr == ''} stdout==expected {r.stdout == expected.rstrip(chr(10)) + chr(10) or r.stdout.rstrip() == expected.rstrip()}")
    if r.stderr: print("   stderr:", r.stderr[:500])
    # page code run too (the reader's code, lab 2 blanks would fail; run only if no blanks)
    if "___" not in code:
        open(script, "w", encoding="utf-8").write(code)
        r2 = subprocess.run([sys.executable, "-I", "-W", "error", script], cwd=tmp, capture_output=True, text=True)
        print(f"lab {i}: page code rc={r2.returncode} stdout.rstrip==expected.rstrip {r2.stdout.rstrip() == expected.rstrip()}")
    shutil.rmtree(tmp)
