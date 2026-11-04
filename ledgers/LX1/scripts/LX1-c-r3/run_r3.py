"""Round-3 LX1-c: run every mutant in ledgers/LX1/mutants/ and every alternative in scripts/LX1-c-r3/gen/
against the page expected block of its lab. Mutant killed = nonzero exit or stdout != expected. Alternatives must NOT be killed."""
import html, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(sys.argv[1])
t = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
def expected(lab):
    s = t.index(f'id="{lab}"')
    seg = t[s:t.index("</section>", s)]
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', seg, re.S).group(1)).rstrip()
def target(name):
    return "lab-LX1-project-2" if ("rung2" in name or "lab2" in name or name.startswith("lx1c_r2n01") or name.startswith("lx1c_r2n02")) else "lab-LX1-project-3"
def run(path, lab):
    wd = tempfile.mkdtemp(prefix="lx1c-r3-mut-")
    os.makedirs(os.path.join(wd, "data"))
    shutil.copy(ROOT / "course/assets/data/market/fx_monthly.csv", os.path.join(wd, "data", "fx_monthly.csv"))
    shutil.copy(path, os.path.join(wd, "m.py"))
    p = subprocess.run([sys.executable, "-I", "-W", "error", "m.py"], cwd=wd, capture_output=True, text=True, timeout=120)
    shutil.rmtree(wd)
    return p.returncode, p.stdout.rstrip(), p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []
killed = 0; files = sorted((ROOT / "ledgers/LX1/mutants").glob("*.py"))
for f in files:
    lab = target(f.name)
    rc, out, err = run(f, lab)
    k = rc != 0 or out != expected(lab)
    killed += k
    print(f"MUT {f.name}: target={lab} rc={rc} killed={k} err={err}")
    if f.name.startswith("lx1c_m02") or f.name.startswith("lx1c_r3n04") or f.name.startswith("lx1c_r3n03") or f.name.startswith("lx1c_r3n01"):
        print("   output:", out.replace("\n", " | "))
print(f"mutants killed {killed}/{len(files)}")
alts = sorted((ROOT / "ledgers/LX1/scripts/LX1-c-r3/gen").glob("*.py"))
passed = 0
for f in alts:
    lab = target(f.name)
    rc, out, err = run(f, lab)
    ok = rc == 0 and out == expected(lab)
    passed += ok
    print(f"ALT {f.name}: target={lab} rc={rc} passes_expected={ok} err={err}")
print(f"alternatives passing {passed}/{len(alts)}")
