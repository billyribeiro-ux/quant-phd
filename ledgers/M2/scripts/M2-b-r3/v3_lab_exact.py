"""Compare each slice lab section in the raw page with its twin and with the twin's observed stdout.

Usage: python -I v3_lab_exact.py <repo_root> <twin_out_dir>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
ok = True
for L in ["07", "08", "09", "10", "11", "12"]:
    page = (root / f"course/modules/M/M2/L{L}.html").read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab"[^>]*id="lab-M2-L%s-1".*?</section>' % L, page, re.S)
    if not sec:
        print(f"L{L}: lab section not found")
        ok = False
        continue
    body = sec.group(0)
    code = re.search(r"<code[^>]*data-run[^>]*>(.*?)</code>", body, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    cls = re.search(r'<section class="([^"]*)"', body)
    code_txt = html.unescape(code.group(1)) if code else None
    exp_txt = html.unescape(exp.group(1)) if exp else None
    twin = (root / f"tests/labs/M2/lab-M2-L{L}-1.py").read_text(encoding="utf-8")
    code_is_twin = code_txt is not None and code_txt.strip() == twin.strip()
    stdout = (outdir / f"lab-M2-L{L}-1.py.out").read_text(encoding="utf-8")
    exp_is_stdout = exp_txt is not None and exp_txt.strip() == stdout.strip()
    rerun = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M2/lab-M2-L{L}-1.py")],
                           capture_output=True, text=True, cwd=str(root))
    rerun_ok = rerun.returncode == 0 and rerun.stdout.strip() == (exp_txt or "").strip()
    ok = ok and code_is_twin and exp_is_stdout and rerun_ok
    print(f"L{L}: section class={cls.group(1) if cls else None} code==twin:{code_is_twin} "
          f"expected==saved-stdout:{exp_is_stdout} expected==fresh-rerun(-I -W error):{rerun_ok} "
          f"code_has_blank:{'___' in (code_txt or '')} stderr_len={len(rerun.stderr)}")
print("ALL OK" if ok else "MISMATCH")
