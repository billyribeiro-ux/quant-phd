"""Round-9 verifier: baseline for the damaged-snapshot checks. Runs the committed lab 3 twin (unmutated) on the
embedded snapshot and on the three damaged snapshots, using the same runner as v9_kill_check.py. Expected: the
embedded run matches the page block exactly; each damaged run exits nonzero with the named ValueError on stderr
and prints nothing to stdout. Argument 1 is the checkout root."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(sys.argv[0]).resolve().parent))
import v9_kill_check as k
root = pathlib.Path(sys.argv[1])
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"
exp = k.expected("lab-LX1-project-3")
p = k.run(twin)
print("embedded rc", p.returncode, "stderr", repr(p.stderr[:80]), "matches page block:", p.stdout.rstrip("\n") == exp)
dmg = k.damaged_texts()
for kind in ("blank", "non_decimal", "gap"):
    q = k.run(twin, dmg[kind])
    msg = q.stderr.strip().splitlines()[-1] if q.stderr.strip() else ""
    print(kind, "rc", q.returncode, "stdout_empty", q.stdout == "", "last stderr line:", msg,
          "| names expected cell/month:", k.DAMAGE_MSG[kind] in q.stderr)
