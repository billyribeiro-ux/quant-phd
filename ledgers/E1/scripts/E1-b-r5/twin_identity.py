# Verifier-written: compare page code block to twin, expected block to stdout, run twin alone under -I -W error.
import html, re, subprocess, sys, pathlib, tempfile, shutil
REPO = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS5-E1-b")
PY = str(REPO / ".venv/bin/python")
pages = {"L04": "lab-E1-L04-1", "L05": "lab-E1-L05-1", "L06": "lab-E1-L06-1"}
ok = True
for pg, lab in pages.items():
    html_text = (REPO / f"course/modules/E/E1/{pg}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', html_text, re.S)
    code = html.unescape(m.group(1))
    twin_src = (REPO / f"tests/labs/E1/{lab}.py").read_text(encoding="utf-8")
    eq = code.rstrip(chr(10)) == twin_src.rstrip(chr(10))  # page drops only the final newline
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, re.S)
    expected = html.unescape(e.group(1))
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"twin_{pg}_", dir="/tmp/e1b5/twins"))
    shutil.copy(REPO / f"tests/labs/E1/{lab}.py", tmp / "twin.py")
    r = subprocess.run([PY, "-I", "-W", "error", "twin.py"], cwd=tmp, capture_output=True, text=True)
    exp_eq = expected.rstrip("\n") == r.stdout.rstrip("\n")
    print(f"{pg}: rc={r.returncode} stderr_bytes={len(r.stderr.encode())} page_code_equals_twin={eq} "
          f"expected_equals_stdout={exp_eq} stdout_lines={len(r.stdout.splitlines())} code_bytes={len(code)}")
    if r.returncode or r.stderr or not eq or not exp_eq:
        ok = False
    (tmp / "stdout.txt").write_text(r.stdout)
print("ALL OK" if ok else "PROBLEM")
