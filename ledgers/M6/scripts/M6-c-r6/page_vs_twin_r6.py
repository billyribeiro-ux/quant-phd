# Compare each lab section's <code> block with its twin file, and the expected <pre> with the twin's real stdout.
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for L in ("09", "10", "11", "12"):
    page = (root / f"course/modules/M/M6/L{L}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-M6-L%s-1".*?<pre><code[^>]*>(.*?)</code></pre>.*?<pre class="expected"[^>]*>(.*?)</pre>' % L, page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/M6/lab-M6-L{L}-1.py").read_text(encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M6/lab-M6-L{L}-1.py")],
                         capture_output=True, text=True).stdout
    print(f"L{L} code_equals_twin {code.rstrip() == twin.rstrip()} expected_equals_stdout {expected.rstrip() == out.rstrip()} lines_expected {len(expected.splitlines())} lines_stdout {len(out.splitlines())}")
