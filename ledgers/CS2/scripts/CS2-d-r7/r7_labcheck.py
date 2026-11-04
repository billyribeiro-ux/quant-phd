import html, re, subprocess, sys, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-CS2-d")
page = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-CS2-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in sections:
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (ROOT / f"tests/labs/CS2/{lab_id.replace('lab-CS2-project-', 'lab-CS2-project-')}.py").read_text(encoding="utf-8")
    same_exact = code == twin
    same_mod_nl = code.rstrip("\n") == twin.rstrip("\n")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/CS2/{lab_id}.py")], capture_output=True, text=True, cwd="/tmp/cs2r7")
    out = r.stdout
    print(f"== {lab_id}: exit={r.returncode} stderr={r.stderr!r}")
    print(f"   page code == twin exact: {same_exact}; modulo trailing newline: {same_mod_nl}; lens page={len(code)} twin={len(twin)}")
    print(f"   expected == output (stripped): {expected.strip() == out.strip()}; expected == output exact: {expected == out}")
    if expected.strip() != out.strip():
        print("   OUTPUT:\n" + out)
        print("   EXPECTED:\n" + expected)
    if not same_mod_nl:
        import difflib
        print("".join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page")))
    print("   output:"); print(out)
