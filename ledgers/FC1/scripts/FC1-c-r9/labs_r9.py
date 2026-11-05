"""Round-9 verifier (FC1-c): extract each project-page lab code block and compare it with its twin; run the twins with -I -W error."""
import html, re, subprocess, sys, pathlib
ROOT = pathlib.Path(sys.argv[1])
page = (ROOT / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-FC1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*(?:<pre class="expected"[^>]*>(.*?)</pre>)?', page, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    twin = (ROOT / f"tests/labs/FC1/lab-FC1-project-{lab_id[-1]}.py").read_text(encoding="utf-8")
    import difflib
    diff = [l for l in difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0) if not l.startswith(("---", "+++"))]
    print(f"== {lab_id}: page code vs twin differing lines: {len(diff)}")
    for l in diff:
        print("   ", l)
    out = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(ROOT / f"tests/labs/FC1/lab-FC1-project-{lab_id[-1]}.py")], capture_output=True, text=True)
    print(f"   twin exit {out.returncode}; stderr: {out.stderr.strip()[:200]!r}")
    got = out.stdout.rstrip("\n")
    exp = html.unescape(expected or "").rstrip("\n")
    print(f"   expected block == twin output: {got == exp}")
    if got != exp:
        print("   GOT:", got); print("   EXP:", exp)
