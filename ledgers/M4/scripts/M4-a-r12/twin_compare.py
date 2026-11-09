"""Compare each lesson page's lab code and expected block with its twin and with the twin's observed output.

Usage: python -I twin_compare.py <checkout> <outdir>. Reads the twin output files written by run_twins.sh.
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
for n in ("01", "02", "03", "04"):
    page = (root / f"course/modules/M/M4/L{n}.html").read_text(encoding="utf-8")
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin = (root / f"tests/labs/M4/lab-M4-L{n}-1.py").read_text(encoding="utf-8")
    code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(1))
    obs_raw = (out / f"twin_L{n}.out").read_text(encoding="utf-8")
    obs = obs_raw.rsplit("exit=", 1)[0]
    print(f"L{n}: code==twin {code == twin} (page {len(code)} chars, twin {len(twin)} chars); "
          f"code==twin ignoring final newline {code.rstrip(chr(10)) == twin.rstrip(chr(10))}; "
          f"expected==output {expected.rstrip(chr(10)) == obs.rstrip(chr(10))}")
    if expected.rstrip("\n") != obs.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(obs.splitlines(), expected.splitlines(), lineterm="")))
    if code != twin:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]))
