import html, re, subprocess, sys, pathlib, os
ROOT = pathlib.Path("/tmp/verify7-AC1-c")
out = {}
for lesson in ("L07", "L08"):
    page = (ROOT / f"course/modules/AC/AC1/{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/AC1/lab-AC1-{lesson}-1.py").read_text(encoding="utf-8")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    r = subprocess.run([sys.executable, "-I", "-W", "error", "-c", twin], capture_output=True, text=True, cwd="/tmp")
    stdout = r.stdout
    out[lesson] = (code.strip() == twin.strip(), stdout.strip() == expected.strip(), r.returncode)
    print(lesson, "embed==twin", code.strip() == twin.strip(), "stdout==expected", stdout.strip() == expected.strip(), "rc", r.returncode, len(code), len(twin))
    if stdout.strip() != expected.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), stdout.strip().splitlines(), lineterm="")))
