"""Round-15 LX1-c verifier harness (written by the verifier, not the builder).

Usage: python -I harness.py <checkout_root> <mode> [files...]
  mode 'twins'    : page code == twin (modulo blanks), twin run under -I -W error, stdout == page expected block.
  mode 'cands'    : run each candidate file (mutant or alternative) for the lab named in its docstring; print
                    KILLED/SURVIVED with the reason. Lab 3 candidates run in a scratch dir holding data/fx_monthly.csv.
"""
import html
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1]).resolve()
MODE = sys.argv[2]
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
SNAPSHOT = ROOT / "course/assets/data/market/fx_monthly.csv"


def section(lab_id: str) -> str:
    start = PAGE.index(f'id="{lab_id}"')
    end = PAGE.index("</section>", start)
    return PAGE[start:end]


def page_code(lab_id: str) -> str:
    sec = section(lab_id)
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S)
    return html.unescape(m.group(1))


def expected(lab_id: str) -> str:
    sec = section(lab_id)
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    return html.unescape(m.group(1))


def lab_of(text: str) -> str:
    m = re.search(r"project lab ([123])", text[:800])
    if not m:
        raise SystemExit("no lab number in docstring")
    return f"lab-LX1-project-{m.group(1)}"


def run(path: pathlib.Path, lab_id: str):
    with tempfile.TemporaryDirectory(prefix="lx1c_r16_") as tmp:
        if lab_id == "lab-LX1-project-3":
            (pathlib.Path(tmp) / "data").mkdir()
            shutil.copy(SNAPSHOT, pathlib.Path(tmp) / "data" / "fx_monthly.csv")
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], cwd=tmp,
                           capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def main() -> None:
    if MODE == "twins":
        for n in (1, 2, 3):
            lab = f"lab-LX1-project-{n}"
            twin = (ROOT / f"tests/labs/LX1/{lab}.py").read_text(encoding="utf-8")
            pc = page_code(lab).rstrip("\n").splitlines()
            tw = twin.rstrip("\n").splitlines()
            diffs = []
            if len(pc) != len(tw):
                diffs.append(f"line count page={len(pc)} twin={len(tw)}")
            for i, (a, b) in enumerate(zip(pc, tw), 1):
                if a != b and "___" not in a:
                    diffs.append(f"line {i}: page={a!r} twin={b!r}")
            rc, out, err = run(ROOT / f"tests/labs/LX1/{lab}.py", lab)
            exp = expected(lab).rstrip("\n")
            print(f"{lab}: page-vs-twin diffs={len(diffs)} {diffs[:3]}")
            print(f"{lab}: twin rc={rc} stderr_bytes={len(err)} stdout==expected: {out.rstrip(chr(10)) == exp}")
            print(f"{lab}: expected lines={len(exp.splitlines())} stdout lines={len(out.splitlines())}")
    elif MODE == "cands":
        for f in sys.argv[3:]:
            path = pathlib.Path(f).resolve()
            text = path.read_text(encoding="utf-8")
            lab = lab_of(text)
            exp = expected(lab).rstrip("\n")
            rc, out, err = run(path, lab)
            if rc != 0 or err.strip():
                reason = f"rc={rc} stderr_tail={err.strip().splitlines()[-1:] if err.strip() else ''}"
                print(f"KILLED | {path.name} | {reason}")
            elif out.rstrip("\n") != exp:
                print(f"KILLED | {path.name} | expected-block differs")
            else:
                print(f"SURVIVED | {path.name} | stdout equals expected block, rc 0")


main()
