"""Round-4 mutant and alternative runs for LX1 project labs. Each mutant/alternative run in a scratch dir with data/."""
import difflib, html, pathlib, re, shutil, subprocess, sys, tempfile, os
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c")
S = ROOT / "ledgers/LX1/scripts/LX1-c-r4"
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
DATA = ROOT / "course/assets/data/market/fx_monthly.csv"
expected = {}
for n in (1, 2, 3):
    lab_id = f"lab-LX1-project-{n}"
    body = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab_id, PAGE, re.S).group(0)
    expected[n] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)).rstrip()

def run(script):
    wd = tempfile.mkdtemp(prefix="lx1c-r4-")
    os.makedirs(f"{wd}/data")
    shutil.copy(DATA, f"{wd}/data/fx_monthly.csv")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(script)], cwd=wd, capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin"}, timeout=120)
    shutil.rmtree(wd)
    return r.returncode, r.stdout.rstrip(), r.stderr.strip()

def verdict(script):
    res = {}
    for n in (1, 2, 3):
        rc, out, err = run(script)
        res[n] = (rc == 0 and out == expected[n] and err == "")
    return res

print("== alternatives (must pass against the page expected block)")
for alt, lab in (("alt_lab1_integer_cents.py", 1), ("alt_lab2_decimal.py", 2), ("alt_lab3_welford.py", 3)):
    rc, out, err = run(S / "gen" / alt)
    ok = rc == 0 and out == expected[lab] and err == ""
    print(f"{alt} -> lab {lab}: rc={rc} stderr={err[:80]!r} matches expected: {ok}")
    if not ok:
        print("--- got\n" + out + "\n--- expected\n" + expected[lab])

print("== mutants (killed = output differs from expected block of a lab, or nonzero exit, or stderr)")
mut_dir = ROOT / "ledgers/LX1/mutants"
for m in sorted(mut_dir.glob("*.py")):
    src = m.read_text(encoding="utf-8")
    twin_scores = {n: difflib.SequenceMatcher(None, src, (ROOT / f"tests/labs/LX1/lab-LX1-project-{n}.py").read_text(encoding="utf-8")).ratio() for n in (1, 2, 3)}
    target = max(twin_scores, key=twin_scores.get)
    rc, out, err = run(m)
    killed = not (rc == 0 and out == expected[target] and err == "")
    print(f"{m.name}: target lab {target} (similarity {twin_scores[target]:.3f}); killed={killed}; rc={rc}; first diff line: {next((a for a, b in zip(out.splitlines()+[''], expected[target].splitlines()+['']) if a != b), None)!r}")
