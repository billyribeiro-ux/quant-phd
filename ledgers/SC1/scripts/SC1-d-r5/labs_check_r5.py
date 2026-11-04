"""Verifier r5 (SC1-d): page lab code vs twin, twin under python -I -W error, output vs expected block."""
import html, re, subprocess, sys
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-d")
page = (ROOT / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
PY = "/Users/billyribeiro/dev/quant-phd/.venv/bin/python"
for lab in ("project-1", "project-2", "project-3"):
    m = re.search(r'<section class="lab[^"]*" id="lab-SC1-%s".*?<pre><code[^>]*data-run>(.*?)</code></pre>' % lab, page, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / ("tests/labs/SC1/lab-SC1-%s.py" % lab)).read_text(encoding="utf-8")
    e = re.search(r'id="lab-SC1-%s".*?<pre class="expected"[^>]*>(.*?)</pre>' % lab, page, re.S)
    expected = html.unescape(e.group(1))
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    blanks = code.count("___")
    if blanks:
        # fill the blanks with the completed expressions from the twin for the completion lab
        out_src = twin
    else:
        out_src = twin
    p = subprocess.run([PY, "-I", "-W", "error", "-c", out_src], capture_output=True, text=True)
    out = p.stdout.rstrip("\n")
    print(lab, "page code == twin:", same_code, "blanks on page:", blanks, "exit:", p.returncode, "stderr bytes:", len(p.stderr))
    print("  output == expected:", out == expected.rstrip("\n"))
    if out != expected.rstrip("\n"):
        print("  got:", repr(out[:300])); print("  exp:", repr(expected[:300]))
