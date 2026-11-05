"""Round-9 lab check for E3 project labs: page code equals twin, twin runs under python -I -W error, expected equals output."""
import html, re, subprocess, sys, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-E3-e")
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
for lab in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = ROOT / "tests/labs/E3" / f"{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    print(f"{lab}: page code equals twin (stripped): {same}; len page {len(code)} twin {len(twin)}")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    out = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp/e3e_r9")
    print(f"  twin exit {out.returncode} stderr {out.stderr.strip()[:300]!r}")
    got = out.stdout.rstrip("\n")
    print(f"  expected block equals output: {got.strip() == exp.strip()}")
    if got.strip() != exp.strip():
        print("  --- got\n" + got + "\n  --- expected\n" + exp)
    print("  output:\n" + got)
