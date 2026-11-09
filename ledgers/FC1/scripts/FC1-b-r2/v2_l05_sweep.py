# Round-2: parameter sweep on scratch copies of the L05 twin. Reports which output lines change per parameter,
# to check the lesson's sentences (E3, interpretation line, offsets_nondecreasing claim).
import re, subprocess, sys, tempfile, shutil
from pathlib import Path
twin = Path(sys.argv[1]) / "tests/labs/FC1/lab-FC1-L05-1.py"
src = twin.read_text(encoding="utf-8")
def run(sub):
    d = Path(tempfile.mkdtemp(prefix="v2sweep_"))
    f = d / "lab.py"
    text = src
    for name, val in sub.items():
        text, n = re.subn(rf"^{name} = [^#\n]+", f"{name} = {val}", text, count=1, flags=re.M)
        assert n == 1, name
    f.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=str(d))
    shutil.rmtree(d)
    assert r.returncode == 0, r.stderr
    return r.stdout.splitlines()
base = run({})
print("baseline offsets line:", [l for l in base if l.startswith("offsets_nondecreasing")])
for label, sub in [("SETTLEMENT_LAG=3", {"SETTLEMENT_LAG": 3}), ("CLEARING_OFFSET=1", {"CLEARING_OFFSET": 1}),
                   ("CLEARING_OFFSET=2 (equal to lag)", {"CLEARING_OFFSET": 2}), ("CLEARING_OFFSET=3 (above lag)", {"CLEARING_OFFSET": 3})]:
    out = run(sub)
    changed = [i for i, (a, b) in enumerate(zip(base, out)) if a != b]
    print(f"== {label}: lines changed = {len(changed)} of {len(base)} (same length: {len(out) == len(base)})")
    for i in changed:
        print("   base:", base[i][:110])
        print("   new :", out[i][:110])
    print("   offsets_nondecreasing:", [l for l in out if l.startswith("offsets_nondecreasing")])
    print("   batch lines unchanged:", all(a == b for a, b in zip(base[-12:], out[-12:])))
