"""Compare each embedded lab on L13 to L18 with its twin and with the twin's printed output (verifier scratch, round 1).

For each page: the <code> block of section id lab-M2-Lnn-1 must equal the twin file text (HTML-unescaped, modulo
trailing newline); the <pre class="expected"> block must equal the stdout of the twin run under python -I -W error.
Run from the checkout root: .venv/bin/python -I ledgers/M2/scripts/M2-c-r1/check_labs_embed.py
"""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
ok = True
for n in range(13, 19):
    page = open(f"{ROOT}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    sec_m = re.search(rf'<section class="lab"[^>]*id="lab-M2-L{n}-1"[^>]*>(.*?)</section>', page, re.S)
    if not sec_m:
        print(f"L{n}: lab section missing")
        ok = False
        continue
    sec = sec_m.group(0)
    head = re.search(r"<section[^>]*>", sec).group(0)
    code_m = re.search(r"<code[^>]*>(.*?)</code>", sec, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", code_m.group(1)))
    expected = html.unescape(re.sub(r"<[^>]+>", "", exp_m.group(1)))
    twin = open(f"{ROOT}/tests/labs/M2/lab-M2-L{n}-1.py", encoding="utf-8").read()
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/M2/lab-M2-L{n}-1.py"],
                         capture_output=True, text=True, cwd="/tmp")
    code_eq = code.strip("\n") == twin.strip("\n")
    exp_eq = expected.strip("\n") == run.stdout.strip("\n")
    print(f"L{n}: rc={run.returncode} stderr={run.stderr.strip()!r} code_equals_twin={code_eq} "
          f"expected_equals_output={exp_eq} head={head[:120]!r}")
    for lab_flag, cond in (("hypothesis", 'class="hypothesis"' in sec), ("interpretation", 'class="interpretation"' in sec),
                           ("data-run", "data-run" in sec), ("tolerance", "data-tolerance" in sec)):
        print(f"    {lab_flag}: {cond}")
    if not (code_eq and exp_eq and run.returncode == 0 and not run.stderr.strip()):
        ok = False
        if not code_eq:
            print("    CODE DIFF (first 400 chars of page vs twin):")
            print("    page:", code[:400].replace("\n", "\\n"))
            print("    twin:", twin[:400].replace("\n", "\\n"))
        if not exp_eq:
            print("    EXPECTED DIFF:")
            print("    page:", expected[:300].replace("\n", "\\n"))
            print("    out :", run.stdout[:300].replace("\n", "\\n"))
print("ALL MATCH" if ok else "MISMATCH FOUND")
