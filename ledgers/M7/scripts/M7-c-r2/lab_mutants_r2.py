"""Lab-check mutation probe, round 2, for the M7 L07 and L08 twins.

Round-2 mutants are plausible student or builder errors in the recursion, the brute force, the optimal-plan
reconstruction, the greedy comparison and the iteration. A mutant is KILLED when its stdout differs from the
unmutated twin's stdout (the page's expected block) or it exits non-zero. Round-1 mutants (ledgers/M7/scripts/
M7-c-r1/lab_mutants.py) are re-run here as well, unchanged.

Run: python3 -I ledgers/M7/scripts/M7-c-r2/lab_mutants_r2.py <checkout>
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out_dir = root / "ledgers/M7/scripts/M7-c-r2/lab_mutants"
out_dir.mkdir(parents=True, exist_ok=True)
L07 = (root / "tests/labs/M7/lab-M7-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/M7/lab-M7-L08-1.py").read_text(encoding="utf-8")

MUTANTS = [
    # L07: optimal-plan reconstruction takes the minimising action (plausible sign error)
    ("L07", "r2_optimal_plan_min_not_max", L07,
     "    c = max(feasible(w), key=lambda x: period_reward(x) + values[t + 1][w - x])",
     "    c = min(feasible(w), key=lambda x: period_reward(x) + values[t + 1][w - x])",
     "optimal_consumption"),
    # L07: the recursion's terminal condition is zero instead of the bequest (V_H = 0)
    ("L07", "r2_terminal_value_zero", L07,
     "    values[HORIZON] = {w: bequest(w) for w in GRID}",
     "    values[HORIZON] = {w: 0 for w in GRID}",
     "recursion_matches_brute_force"),
    # L07: value table reads V_{t} instead of V_{t+1} (off-by-one in time)
    ("L07", "r2_recursion_reads_same_time", L07,
     "            values[t][w] = max(period_reward(c) + values[t + 1][w - c] for c in feasible(w))",
     "            values[t][w] = max(period_reward(c) + values[t + 1][w] for c in feasible(w))",
     "recursion_matches_brute_force"),
    # L07: brute force allows infeasible consumption (no wealth check)
    ("L07", "r2_brute_force_no_feasibility", L07,
     "            if c > wealth:\n                feasible_plan = False\n                break",
     "            if c > wealth:\n                wealth = wealth",
     "plans_checked_from_0_400"),
    # L07: greedy plan takes the smallest period reward (wrong direction)
    ("L07", "r2_greedy_takes_smallest", L07,
     "    c = max(feasible(w), key=period_reward)",
     "    c = min(feasible(w), key=period_reward)",
     "greedy_total"),
    # L07: tail check compares with the wrong state index
    ("L07", "r2_tail_check_wrong_index", L07,
     "    tails_optimal = all(plan_total(plan[k:], path[k]) == values[k][path[k]] for k in range(HORIZON))",
     "    tails_optimal = all(plan_total(plan[k:], path[k]) == values[k][path[0]] for k in range(HORIZON))",
     "optimal_plan_every_tail_optimal"),
    # L08: discount applied twice in the Bellman step (beta^2 instead of beta)
    ("L08", "r2_bellman_discount_squared", L08,
     "        candidates = {a: reward(s, a) + DISCOUNT * u[next_state(s, a)] for a in ACTIONS}",
     "        candidates = {a: reward(s, a) + DISCOUNT * DISCOUNT * u[next_state(s, a)] for a in ACTIONS}",
     "recursion_matches_brute_force"),
    # L08: brute force starts the discount weight at the discount factor (wrong first weight)
    ("L08", "r2_brute_weight_starts_at_beta", L08,
     "        weight = Fraction(1)\n",
     "        weight = DISCOUNT\n",
     "recursion_matches_brute_force"),
    # L08: the terminal reward in the brute force is ignored
    ("L08", "r2_brute_ignores_terminal", L08,
     "        total += weight * Fraction(0)\n",
     "        total += weight * Fraction(1)\n",
     "recursion_matches_brute_force"),
    # L08: iterate compares with V_(n) instead of V_(H-n)
    ("L08", "r2_iterate_compares_wrong_horizon", L08,
     "    matches = all(iterates[n][s] == values[HORIZON - n][s] for n in range(7) for s in STATES)",
     "    matches = all(iterates[n][s] == values[n][s] for n in range(7) for s in STATES)",
     "iterate_equals_n_period_recursion"),
    # L08: value iteration applies the operator without the discount (undiscounted iterate)
    ("L08", "r2_iteration_no_discount", L08,
     "        new, _, _ = bellman_step(iterates[-1])",
     "        new = {s: max(reward(s, a) + iterates[-1][next_state(s, a)] for a in ACTIONS) for s in STATES}",
     "n 0 change"),
]

# round-1 mutants, copied verbatim from ledgers/M7/scripts/M7-c-r1/lab_mutants.py
R1_SRC = (root / "ledgers/M7/scripts/M7-c-r1/lab_mutants.py").read_text(encoding="utf-8")
ns: dict = {"L07": L07, "L08": L08}
start = R1_SRC.index("MUTANTS = [")
end = R1_SRC.index("]\n\nBASE = {}")
exec(R1_SRC[start:end + 2], ns)
MUTANTS += ns["MUTANTS"]

BASE = {}
for lab, src in (("L07", L07), ("L08", L08)):
    base_path = out_dir / f"{lab}_baseline.py"
    base_path.write_text(src, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(base_path)], capture_output=True, text=True)
    BASE[lab] = proc.stdout
    print(f"baseline {lab}: exit={proc.returncode} lines={len(proc.stdout.splitlines())}")

killed_count = 0
total = 0
for lab, name, src, old, new, check in MUTANTS:
    total += 1
    if src.count(old) != 1:
        print(f"{name}: SKIP, pattern count {src.count(old)}")
        continue
    mutated = src.replace(old, new)
    path = out_dir / f"{lab}_{name}.py"
    path.write_text(mutated, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
    line = [ln for ln in proc.stdout.splitlines() if ln.startswith(check)]
    killed = proc.returncode != 0 or proc.stdout != BASE[lab]
    killed_count += killed
    print(f"{lab} {name}: check={check!r} line={line} exit={proc.returncode} KILLED={killed}"
          + (f" stderr={proc.stderr.strip().splitlines()[-1:]}" if proc.returncode else ""))
print(f"killed {killed_count}/{total}")
