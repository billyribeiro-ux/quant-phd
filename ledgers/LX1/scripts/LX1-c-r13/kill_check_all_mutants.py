"""Round-9 verifier: runs every ledgers/LX1/mutants/*.py that mutates an LX1 project lab (project lab 1, 2 or 3,
identified by the docstring) alone under python -I -W error, in a scratch dir, and reports KILLED or SURVIVED.
Killed = any of: nonzero exit or stderr; stdout (trailing newlines aside) differs from the page's expected block;
for project lab 3 only, a damaged snapshot (blank GBP cell, non-decimal GBP cell, removed month) does not raise
ValueError with a message naming the cell or month. Argument 1 is the checkout root."""
import glob, html, os, pathlib, re, shutil, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
SNAP = root / "course/assets/data/market/fx_monthly.csv"
PY = str(root / ".venv/bin/python")

def expected(lab):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).rstrip("\n")

def run(script, csv_text=None):
    wd = tempfile.mkdtemp(prefix="v9kill-")
    try:
        os.makedirs(f"{wd}/data")
        if csv_text is None:
            shutil.copy(SNAP, f"{wd}/data/fx_monthly.csv")
        else:
            open(f"{wd}/data/fx_monthly.csv", "w", encoding="utf-8", newline="").write(csv_text)
        shutil.copy(script, f"{wd}/lab.py")
        return subprocess.run([PY, "-I", "-W", "error", f"{wd}/lab.py"], cwd=wd, capture_output=True, text=True,
                              env={"PATH": "/usr/bin:/bin"}, timeout=120)
    finally:
        shutil.rmtree(wd)

def damaged_texts():
    lines = SNAP.read_text(encoding="utf-8").splitlines()
    head = lines[0].split(",")
    gi = head.index("GBP")
    out = {}
    for kind in ("blank", "non_decimal", "gap"):
        ls = list(lines)
        if kind in ("blank", "non_decimal"):
            for i, l in enumerate(ls):
                f = l.split(",")
                if f[0] == "2000-06":
                    f[gi] = "" if kind == "blank" else "n/a"
                    ls[i] = ",".join(f)
        else:
            ls = [l for l in ls if not l.startswith("1990-06,")]
        out[kind] = "\n".join(ls) + "\n"
    return out

DAMAGE_MSG = {"blank": "2000-06: GBP cell '' is blank", "non_decimal": "2000-06: GBP cell 'n/a' is blank",
              "gap": "month 1990-07 does not follow 1990-05"}

if __name__ == "__main__":
    exp = {lab: expected(lab) for lab in ("lab-LX1-project-1", "lab-LX1-project-2", "lab-LX1-project-3")}
    dmg = damaged_texts()
    names = sorted(glob.glob(str(root / "ledgers/LX1/mutants/*.py")))
    killed = survived = 0
    for path in names:
        text = open(path, encoding="utf-8").read()
        m = re.search(r"project lab ([123])", text[:600])
        if not m:
            print("SKIP (not a project lab) |", os.path.basename(path))
            continue
        lab = f"lab-LX1-project-{m.group(1)}"
        p = run(path)
        reasons = []
        if p.returncode != 0 or p.stderr:
            reasons.append(f"rc={p.returncode} stderr={p.stderr.strip().splitlines()[-1:] or ''}")
        elif p.stdout.rstrip("\n") != exp[lab]:
            reasons.append("expected-block differs")
        if lab == "lab-LX1-project-3":
            for kind in ("blank", "non_decimal", "gap"):
                q = run(path, dmg[kind])
                ok_raise = q.returncode != 0 and DAMAGE_MSG[kind] in q.stderr and q.stdout == ""
                if not ok_raise:
                    reasons.append(f"damaged:{kind} did not raise as expected (rc={q.returncode})")
        status = "KILLED" if reasons else "SURVIVED"
        killed += bool(reasons)
        survived += not reasons
        print(status, "|", os.path.basename(path), "|", "; ".join(reasons) if reasons else "")
    print(f"TOTAL killed={killed} survived={survived}")
