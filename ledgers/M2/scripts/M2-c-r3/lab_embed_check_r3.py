"""For each lab in L13-L18: page code equals twin, expected block equals the twin's printed output (verifier round 3)."""
import html, re, subprocess, sys
ok = True
for n in range(13, 19):
    page = f"course/modules/M/M2/L{n:02d}.html"
    twin = f"tests/labs/M2/lab-M2-L{n:02d}-1.py"
    t = open(page, encoding="utf-8").read()
    sec = re.search(r'<section class="lab" id="lab-M2-L%02d-1".*?</section>' % n, t, flags=re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, flags=re.S).group(1))
    twin_src = open(twin, encoding="utf-8").read()
    same_code = code.strip("\n") == twin_src.strip("\n")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, flags=re.S).group(1))
    out = subprocess.run([sys.executable if False else ".venv/bin/python", "-I", "-W", "error", twin], capture_output=True, text=True).stdout
    same_out = expected.strip("\n") == out.strip("\n")
    print(f"L{n:02d} code_equals_twin={same_code} expected_equals_output={same_out} twin_lines={twin_src.count(chr(10))}")
    ok = ok and same_code and same_out
print("ALL", ok)
