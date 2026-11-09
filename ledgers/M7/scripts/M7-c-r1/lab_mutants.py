"""Lab-check mutation probe for M7 L07 and L08 twins (verifier, round 1).

The lessons say these labs check the recursion against brute force, check each tail, and check the
iterates against the n-period recursion. Each mutant is a plausible error in the recursion or the check;
a mutant is KILLED when the printed check line changes to False (or the run fails).
Run: python3 -I ledgers/M7/scripts/M7-c-r1/lab_mutants.py <checkout>
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out_dir = root / "ledgers/M7/scripts/M7-c-r1/lab_mutants"
out_dir.mkdir(parents=True, exist_ok=True)
L07 = (root / "tests/labs/M7/lab-M7-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/M7/lab-M7-L08-1.py").read_text(encoding="utf-8")

MUTANTS = [
    ("L07", "m1_recursion_min_not_max", L07,
     "max(period_reward(c) + values[t + 1][w - c] for c in feasible(w))",
     "min(period_reward(c) + values[t + 1][w - c] for c in feasible(w))",
     "recursion_matches_brute_force"),
    ("L07", "m2_brute_force_drops_bequest", L07,
     "        total += bequest(wealth)\n        checked += 1",
     "        checked += 1",
     "recursion_matches_brute_force"),
    ("L07", "m3_recursion_ignores_future", L07,
     "period_reward(c) + values[t + 1][w - c] for c in feasible(w))",
     "period_reward(c) for c in feasible(w))",
     "recursion_matches_brute_force"),
    ("L07", "m4_tail_check_always_true", L07,
     "    tails_optimal = all(plan_total(plan[k:], path[k]) == values[k][path[k]] for k in range(HORIZON))",
     "    tails_optimal = True",
     "optimal_plan_every_tail_optimal"),
    ("L07", "m5_greedy_check_always_false", L07,
     "    print(f\"greedy_plan_optimal {plan_total(greedy, 400) == values[0][400]}\")",
     "    print(f\"greedy_plan_optimal {plan_total(greedy, 400) != values[0][400]}\")",
     "greedy_plan_optimal"),
    ("L08", "m6_bellman_step_min", L08,
     "        top = max(candidates.values())",
     "        top = min(candidates.values())",
     "recursion_matches_brute_force"),
    ("L08", "m7_brute_force_no_discount_weight", L08,
     "            weight *= DISCOUNT\n",
     "",
     "recursion_matches_brute_force"),
    ("L08", "m8_iterate_starts_from_one", L08,
     "    iterates = [dict(terminal)]",
     "    iterates = [{s: Fraction(1) for s in STATES}]",
     "iterate_equals_n_period_recursion"),
    ("L08", "m9_discount_one_in_iteration_only", L08,
     "        new, _, _ = bellman_step(iterates[-1])",
     "        new = {s: max(reward(s, a) + u for a in ACTIONS for u in [iterates[-1][next_state(s, a)]]) for s in STATES}",
     "iterate_equals_n_period_recursion"),
    ("L08", "m10_tie_count_always_zero", L08,
     "    total_ties = 0\n    for t in range(HORIZON):\n        _, best, ties = bellman_step(values[t + 1])\n        total_ties += ties",
     "    total_ties = 0\n    for t in range(HORIZON):\n        _, best, ties = bellman_step(values[t + 1])\n        total_ties += 0",
     "tied_pairs_t0_to_5"),
]

BASE = {}
for lab, src in (("L07", L07), ("L08", L08)):
    base_path = out_dir / f"{lab}_baseline.py"
    base_path.write_text(src, encoding="utf-8")
    BASE[lab] = subprocess.run([sys.executable, "-I", "-W", "error", str(base_path)], capture_output=True,
                               text=True).stdout

for lab, name, src, old, new, check in MUTANTS:
    if src.count(old) != 1:
        print(f"{name}: SKIP, pattern count {src.count(old)}")
        continue
    mutated = src.replace(old, new)
    path = out_dir / f"{lab}_{name}.py"
    path.write_text(mutated, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
    line = [ln for ln in proc.stdout.splitlines() if ln.startswith(check)]
    # KILLED when the printed output differs from the unmutated twin's output (what the page's expected block records)
    killed = proc.returncode != 0 or proc.stdout != BASE[lab]
    print(f"{lab} {name}: check={check!r} line={line} exit={proc.returncode} KILLED={killed}"
          + (f" stderr={proc.stderr.strip().splitlines()[-1:]}" if proc.returncode else ""))
