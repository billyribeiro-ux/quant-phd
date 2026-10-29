import html, re, subprocess, sys, pathlib, difflib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC6-E5-b")
py = str(root / ".venv/bin/python")
ok_all = True
for pg in ["L04", "L05", "L06"]:
    page = (root / f"course/modules/E/E5/{pg}.html").read_text()
    twin_path = root / f"tests/labs/E5/lab-E5-{pg}-1.py"
    twin = twin_path.read_text()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    eq_code = code.strip() == twin.strip()
    scratch = pathlib.Path(f"/tmp/e5b_r6_scratch/{pg}")
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / "lab.py").write_text(twin)
    r = subprocess.run([py, "-I", "-W", "error", str(scratch / "lab.py")], capture_output=True, text=True, cwd=str(scratch))
    out = r.stdout
    eq_exp = out.strip() == expected.strip()
    if not eq_exp:
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), "expected", "output", lineterm="")))
    if not eq_code:
        print("\n".join(list(difflib.unified_diff(code.strip().splitlines(), twin.strip().splitlines(), "page", "twin", lineterm=""))[:40]))
    print(pg, "exit=", r.returncode, "stderr=", repr(r.stderr[:200]), "page_code_equals_twin=", eq_code, "expected_equals_output=", eq_exp)
    ok_all = ok_all and r.returncode == 0 and eq_code and eq_exp and r.stderr == ""
print("ALL_OK" if ok_all else "NOT_OK")
