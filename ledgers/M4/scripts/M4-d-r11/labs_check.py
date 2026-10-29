"""Compare each project lab's page code and expected block with its twin and its run output."""
import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M4-d")
page = (root / "course/modules/M/M4/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    m = re.search(rf'id="lab-M4-project-{n}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/M4/lab-M4-project-{n}.py").read_text(encoding="utf-8")
    print(f"lab {n}: page code == twin: {code == twin}; page-vs-twin differing lines: {sum(1 for a,b in zip(code.splitlines(), twin.splitlines()) if a!=b)} (len page {len(code.splitlines())}, twin {len(twin.splitlines())})")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M4/lab-M4-project-{n}.py")], capture_output=True, text=True)
    print(f"lab {n}: twin exit {r.returncode} stderr {r.stderr.strip()[:200]!r}")
    print(f"lab {n}: output == expected: {r.stdout.strip() == expected.strip()}")
    if r.stdout.strip() != expected.strip():
        print(r.stdout); print("EXPECTED:"); print(expected)
