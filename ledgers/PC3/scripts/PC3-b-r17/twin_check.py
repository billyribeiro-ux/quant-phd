"""Round 17 PC3-b twin check: page data-run code equals twin; twin runs under python -I -W error; expected block equals stdout."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L04": "lab-PC3-L04-1", "L05": "lab-PC3-L05-1", "L06": "lab-PC3-L06-1"}
ok = True
for lesson, lab in PAGES.items():
    page = (ROOT / f"course/modules/PC/PC3/{lesson}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/PC3/{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    code = html.unescape(m.group(1))
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    m2 = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m2.group(1))
    # strip any inner tags
    expected = re.sub(r"<[^>]+>", "", expected)
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)],
        cwd="/tmp", capture_output=True, text=True, timeout=120,
    )
    out_lines = run.stdout.rstrip("\n").split("\n")
    exp_lines = expected.rstrip("\n").split("\n")
    same_out = [l.rstrip() for l in out_lines] == [l.rstrip() for l in exp_lines]
    print(f"{lesson} {lab}: page_code_eq_twin={same_code} twin_rc={run.returncode} stderr_bytes={len(run.stderr.encode())} "
          f"stdout_lines={len(out_lines)} expected_lines={len(exp_lines)} expected_eq_stdout={same_out}")
    if not same_out:
        import difflib
        print("\n".join(difflib.unified_diff(exp_lines, out_lines, lineterm="")))
    ok = ok and same_code and run.returncode == 0 and not run.stderr and same_out
print("ALL OK" if ok else "PROBLEM")
