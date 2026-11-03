"""Compare each lab section's code and expected block with its twin and with the twin's real output.

Run from the checkout root: .venv/bin/python ledgers/M7/scripts/M7-e-r4/labcheck.py
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
MOD = ROOT / "course/modules/M/M7"
TWINS = ROOT / "tests/labs/M7"
out = []
for page in sorted(MOD.glob("L0*.html")):
    text = page.read_text(encoding="utf-8")
    for m in re.finditer(r'<section class="lab"[^>]*id="([^"]+)"[^>]*>(.*?)</section>', text, re.S):
        lab_id, body = m.group(1), m.group(2)
        code = re.search(r"<code[^>]*data-run[^>]*>(.*?)</code>", body, re.S)
        expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        code_txt = html.unescape(code.group(1)) if code else None
        exp_txt = html.unescape(expected.group(1)) if expected else None
        out.append(f"{page.name} {lab_id} code_len={len(code_txt or '')} expected_len={len(exp_txt or '')}")
        twin_refs = re.findall(r"@@LAB:([^@]+)@@", body)
        out_refs = re.findall(r"@@OUT:([^@]+)@@", body)
        out.append(f"  markers LAB={twin_refs} OUT={out_refs}")
        twin = TWINS / f"{lab_id}.py"
        if code_txt is not None and twin.exists():
            tw = twin.read_text(encoding="utf-8")
            out.append(f"  page code == twin text (trailing newline ignored): {code_txt.rstrip(chr(10)) == tw.rstrip(chr(10))}  (twin {twin.name})")
            if code_txt.rstrip(chr(10)) != tw.rstrip(chr(10)):
                import difflib
                out.extend("    " + l.rstrip() for l in list(difflib.unified_diff(tw.splitlines(), code_txt.splitlines(), lineterm=""))[:30])
        else:
            out.append(f"  twin missing or code missing: twin={twin} exists={twin.exists()}")
        if twin.exists():
            r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=str(TWINS), timeout=120)
            real = r.stdout
            out.append(f"  twin run rc={r.returncode} stderr_len={len(r.stderr)}")
            if exp_txt is not None:
                same = exp_txt.strip("\n") == real.strip("\n")
                out.append(f"  expected block == real output (stripped): {same}  expected_lines={exp_txt.count(chr(10))+1} output_lines={real.count(chr(10))+1}")
                if not same:
                    import difflib
                    out.extend("    " + l.rstrip() for l in list(difflib.unified_diff(exp_txt.strip("\n").splitlines(), real.strip("\n").splitlines(), lineterm=""))[:30])
print("\n".join(out))
