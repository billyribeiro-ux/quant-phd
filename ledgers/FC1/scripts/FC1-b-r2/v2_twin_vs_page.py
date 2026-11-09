# Round-2 verifier check: page code block == twin, pre.expected == twin stdout (run alone, python -I -W error).
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
pairs = {
    "L04": ("course/modules/FC/FC1/L04.html", "tests/labs/FC1/lab-FC1-L04-1.py"),
    "L05": ("course/modules/FC/FC1/L05.html", "tests/labs/FC1/lab-FC1-L05-1.py"),
}
ok = True
for name, (page_rel, twin_rel) in pairs.items():
    page = (ROOT / page_rel).read_text(encoding="utf-8")
    twin = (ROOT / twin_rel).read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_text = html.unescape(code.group(1)).strip("\n")
    twin_text = twin.strip("\n")
    same_code = code_text == twin_text
    markers = len(re.findall(r"@@(LAB|OUT):", page))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / twin_rel)], capture_output=True, text=True, cwd="/tmp")
    exp_text = html.unescape(expected.group(1)).strip("\n")
    out_text = run.stdout.strip("\n")
    same_out = exp_text == out_text
    print(f"{name}: code_bytes page={len(code_text.encode())} twin={len(twin_text.encode())} identical={same_code}")
    print(f"{name}: twin rc={run.returncode} stderr_bytes={len(run.stderr.encode())} expected==stdout={same_out} markers={markers}")
    ok = ok and same_code and same_out and run.returncode == 0 and not run.stderr and markers == 0
print("ALL OK" if ok else "MISMATCH")
