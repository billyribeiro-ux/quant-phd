"""Round 9: page lab code vs twin, twin run under python -I -W error, and expected block vs output (M7 project labs)."""
import html, re, subprocess, sys, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-M7-d")
PAGE = ROOT / "course/modules/M/M7/project.html"
text = PAGE.read_text(encoding="utf-8")
for n in (1, 2, 3):
    m = re.search(rf'<section[^>]*id="lab-M7-project-{n}"[^>]*>(.*?)</section>', text, re.S)
    body = m.group(1)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    code = html.unescape(code)
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / f"tests/labs/M7/lab-M7-project-{n}.py").read_text(encoding="utf-8")
    print(f"lab {n}: page code == twin (trailing newline ignored): {code.rstrip(chr(10)) == twin.rstrip(chr(10))}; twin lines {len(twin.splitlines())}, page lines {len(code.splitlines())}")
    if code.rstrip(chr(10)) != twin.rstrip(chr(10)) and n != 2:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    r = subprocess.run([sys.executable, "-I", "-W", "error", "-c", twin], capture_output=True, text=True, cwd="/tmp")
    print(f"lab {n}: twin exit {r.returncode}, stderr {r.stderr.strip()[:200]!r}")
    print(f"lab {n}: output == expected block: {r.stdout.strip() == exp.strip()}")
    if r.stdout.strip() != exp.strip():
        print("OUT:", r.stdout); print("EXP:", exp)
