"""Run the four round-13 lab-claim mutants from an empty directory with python -I -W error; killed when stdout differs from the twin's expected block."""
import html, re, subprocess, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1]); mdir = root / "ledgers/SC1/mutants"
pairs = {"L01": ("lab-SC1-L01-1", "SC1a-r13-lab-m1-L01-cov-max.py"),
         "L02": ("lab-SC1-L02-1", "SC1a-r13-lab-m2-L02-hat-peak-half.py"),
         "L03": ("lab-SC1-L03-1", "SC1a-r13-lab-m3-L03-var-divisor-n.py")}
extra = {"L03b": ("lab-SC1-L03-1", "SC1a-r13-lab-m4-L03-closed-form-H3.py")}
for key, (twin, mut) in list(pairs.items()) + list(extra.items()):
    page = key[:3]
    h = (root / f"course/modules/SC/SC1/{page}.html").read_text(encoding="utf-8")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', h, re.S).group(1)).rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(mdir / mut)], cwd=scratch, capture_output=True, text=True)
    out = p.stdout.rstrip("\n")
    print(f"{mut}: exit={p.returncode} killed={out != expected or p.returncode != 0} (first differing line: "
          + next((f"expected={a!r} got={b!r}" for a, b in zip(expected.splitlines(), out.splitlines()) if a != b), "none") + ")")
