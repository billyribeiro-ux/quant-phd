"""Round 7 (slice a): byte-compare each slice lab's page code with its twin, and the page expected block with the twin's stdout (twin run alone, python -I -W error)."""
import html, re, subprocess, sys
ROOT = sys.argv[1].rstrip('/') + '/'
PY = sys.argv[2]
for i in range(1, 7):
    page = open(f"{ROOT}course/modules/M/M2/L{i:02d}.html", encoding="utf-8").read()
    sec = re.search(r'<section class="lab" id="lab-M2-L%02d-1".*?</section>' % i, page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = f"{ROOT}tests/labs/M2/lab-M2-L{i:02d}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    r = subprocess.run([PY, "-I", "-W", "error", twin_path], capture_output=True, text=True, cwd=ROOT)
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    exp_eq = exp.rstrip("\n") == r.stdout.rstrip("\n")
    print(f"L{i:02d} code==twin {code_eq} expected==stdout {exp_eq} exit {r.returncode} stderr_bytes {len(r.stderr)}")
