"""Round 8 slice d: project.html lab code vs twin, twin run under python -I -W error, expected vs output."""
import difflib, html, pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(sys.argv[1])
page = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
sections = re.findall(
    r'<section class="lab[^"]*" id="(lab-CS2-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>',
    page, re.S)
print("labs found in page:", [s[0] for s in sections])
for lab_id, code, expected in sections:
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (ROOT / f"tests/labs/CS2/{lab_id}.py").read_text(encoding="utf-8")
    scratch = tempfile.mkdtemp(prefix="cs2r8-lab-")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/CS2/{lab_id}.py")],
                       capture_output=True, text=True, cwd=scratch)
    out = r.stdout
    print(f"== {lab_id}: exit={r.returncode} stderr={r.stderr!r}")
    print(f"   page code == twin exact: {code == twin}; modulo trailing newline: {code.rstrip() == twin.rstrip()}")
    print(f"   expected == output exact: {expected == out}; stripped: {expected.strip() == out.strip()}")
    if code.rstrip() != twin.rstrip():
        print("".join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page")))
    print("   output:")
    print(out)
