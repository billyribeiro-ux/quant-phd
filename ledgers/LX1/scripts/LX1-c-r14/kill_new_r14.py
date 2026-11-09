"""Round-14 verifier: runs the three new mutants (ledgers/LX1/mutants/r14n*.py) through the round-13 kill check.
Argument 1 is the checkout root. Reuses the round-13 harness functions unchanged."""
import importlib.util, pathlib, sys, glob, os
root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("k13", root / "ledgers/LX1/scripts/LX1-c-r13/kill_check_all_mutants.py")
k13 = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], str(root)]
spec.loader.exec_module(k13)
import re
exp = {lab: k13.expected(lab) for lab in ("lab-LX1-project-1", "lab-LX1-project-2", "lab-LX1-project-3")}
dmg = k13.damaged_texts()
for path in sorted(glob.glob(str(root / "ledgers/LX1/mutants/r14n*.py"))):
    text = open(path, encoding="utf-8").read()
    lab = "lab-LX1-project-" + re.search(r"project lab ([123])", text[:600]).group(1)
    p = k13.run(path)
    reasons = []
    if p.returncode != 0 or p.stderr:
        reasons.append(f"rc={p.returncode} stderr_tail={p.stderr.strip().splitlines()[-1:] or ''}")
    elif p.stdout.rstrip("\n") != exp[lab]:
        reasons.append("expected-block differs")
        import difflib
        diff = [l for l in difflib.unified_diff(exp[lab].splitlines(), p.stdout.rstrip("\n").splitlines(), lineterm="", n=0)][2:]
        reasons.append("diff: " + " | ".join(diff[:6]))
    print("KILLED" if reasons else "SURVIVED", "|", os.path.basename(path), "|", "; ".join(reasons))
