"""Round-3 re-derivations for slice d (CS2 project, grader, cards, mutants). Usage: python -I checks_r3.py <repo_root>
Prints: the card duplicate scan (also written to cards_dup_scan.txt), the learner-text process-word scan, the rank
witness and project-number re-derivations, the Welford lab offsets, the card-number re-derivations, and writes the
L05, L09, L11 and L02 lab twin outputs (lab_<L>.out) by running each twin under python -I -W error."""

import difflib
import json
import math
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1]).resolve()
S = root / "ledgers/CS2/scripts/CS2-d-r3"
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))

print("== card duplicate scan")
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()  # noqa: E731
lines = [f"cards {len(cards)} unique ids {len({c['id'] for c in cards})}"]
seen: dict[str, list[str]] = {}
for c in cards:
    seen.setdefault(norm(c["front"]), []).append(c["id"])
lines.append(f"duplicate normalised fronts: {[v for v in seen.values() if len(v) > 1]}")
back: dict[str, list[str]] = {}
for c in cards:
    back.setdefault(norm(c["back"]), []).append(c["id"])
lines.append(f"duplicate normalised backs: {[v for v in back.values() if len(v) > 1]}")
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, norm(cards[i]["front"]), norm(cards[j]["front"])).ratio()
        if r > 0.8:
            pairs.append((round(r, 2), cards[i]["id"], cards[j]["id"]))
lines.append(f"front pairs with similarity > 0.8: {len(pairs)}")
lines += [str(p) for p in pairs]
(S / "cards_dup_scan.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:3]), f"(and {len(pairs)} pairs, see cards_dup_scan.txt)")

print("== process words in learner text")
words = ["builder", "verifier", "round", "architect", "ledger", "reviewer", "agent", "fragment", "pin", "slice", "iteration", "orchestrat", "workflow"]
for f in ["course/modules/CS/CS2/project.html", "course/modules/CS/CS2/cards.json", "course/modules/CS/CS2/grader/test_project.py",
          "course/modules/CS/CS2/grader/reference.py", "course/modules/CS/CS2/grader/instance.py", "course/modules/CS/CS2/grader/starter.py",
          "tests/labs/CS2/lab-CS2-project-1.py", "tests/labs/CS2/lab-CS2-project-2.py", "tests/labs/CS2/lab-CS2-project-3.py"]:
    t = (root / f).read_text(encoding="utf-8").lower()
    hits = {w: len(re.findall(r"\b" + re.escape(w), t)) for w in words}
    print(f, {k: v for k, v in hits.items() if v})

print("== witnesses and project numbers")
t1 = Fraction(0.1) * 20 - Fraction(0.05) * 20
print("q=0.1 n=20 eps=0.05: exact target", max(1, math.ceil(t1)), "float target", max(1, math.ceil(0.1 * 20 - 0.05 * 20)))
q2 = Fraction(0.2500004) * 20
print("q=0.2500004: qn =", float(q2), "exact target", max(1, math.ceil(q2 - Fraction(0.05) * 20)),
      "six-place q target", max(1, math.ceil(Fraction(0.25) * 20 - Fraction(0.05) * 20)))
off = [2, 5, 1, 4, 9, 3, 6, 0]
mu = sum(off) / 8
print("lab 2 offsets: sum", sum(off), "mean", mu, "sum of squared deviations", sum((x - mu) ** 2 for x in off), "/7 =", sum((x - mu) ** 2 for x in off) / 7)
print("lab 3 sum", sum(Fraction(s) for s in ["10003.2", "10001.7", "10007.5", "10000.4", "10004.9", "10002.1", "10009.6", "10001.0", "10006.3", "10003.8", "10005.5"]))
print("log_phi 65 =", round(math.log(65) / math.log((1 + 5 ** 0.5) / 2), 4))
print("c151 bounds: n=1e9 (L=29, eps=1/20):", (30 * 31 * 32) / (3 * 0.05) + 30, " n=5000 (L=12):", (13 * 14 * 15) / (3 * 0.05) + 13)
print("c196 ratio", round(1.418e-2 / 8.852e-11, -6), " c197 ratio", round(1.000 / 7.449e-8, -5))
print("c155 totals: 2.0078*128 =", round(2.0078 * 128), " 3.0156*256 =", round(3.0156 * 256), " 193/64 - 257/128 =", Fraction(193, 64) - Fraction(257, 128))
print("rotation calls: 63 + 53 + 2*55 + 2*57 =", 63 + 53 + 2 * 55 + 2 * 57)

print("== lab twins (python -I -W error)")
for L in ["L02", "L05", "L09", "L11"]:
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/CS2/lab-CS2-{L}-1.py")],
                         capture_output=True, text=True, check=False)
    (S / f"lab_{L}.out").write_text(res.stdout, encoding="utf-8")
    print(L, "exit", res.returncode, "stderr", repr(res.stderr[:80]), "->", f"lab_{L}.out")
