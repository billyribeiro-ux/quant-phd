"""Compare each lab on L19-L21 with its twin.

For every <section class="lab" id="lab-M2-LNN-1"> the page's <code data-run> text must equal the twin source
(after HTML unescaping and stripping trailing spaces), and the <pre class="expected"> text must equal the
stdout of the twin run alone under python -I -W error. Usage: python -I page_vs_twin.py <repo-root>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
ok = True
for n in (19, 20, 21):
    lab = f"lab-M2-L{n}-1"
    page = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8")
    m = re.search(rf'<section class="lab"[^>]*id="{lab}"[^>]*>(.*?)</section>', page, re.S)
    if not m:
        print(f"{lab}: section not found")
        ok = False
        continue
    body = m.group(1)
    code = re.search(r"<code[^>]*data-run[^>]*>(.*?)</code>", body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code_text = html.unescape(re.sub(r"<[^>]+>", "", code.group(1))).rstrip()
    exp_text = html.unescape(re.sub(r"<[^>]+>", "", expected.group(1))).rstrip()
    twin = (root / f"tests/labs/M2/{lab}.py").read_text(encoding="utf-8").rstrip()
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M2/{lab}.py")],
        capture_output=True, text=True, check=False,
    )
    out = run.stdout.rstrip()
    same_code = code_text == twin
    same_out = exp_text == out
    print(f"{lab}: exit={run.returncode} code_equals_twin={same_code} expected_equals_output={same_out} "
          f"code_lines={len(twin.splitlines())} expected_lines={len(out.splitlines())}")
    if not same_code:
        for i, (a, b) in enumerate(zip(code_text.splitlines(), twin.splitlines()), 1):
            if a != b:
                print(f"  first code diff at line {i}: page={a!r} twin={b!r}")
                break
        else:
            print(f"  code length differs: page={len(code_text.splitlines())} twin={len(twin.splitlines())}")
    if not same_out:
        print(f"  expected block differs from twin stdout; page tail={exp_text[-80:]!r}")
    ok = ok and same_code and same_out and run.returncode == 0
print("PASS" if ok else "FAIL")
