"""Lab probe: apply student-style errors to the L07 and L08 twins and record which printed claim flips.

Labs are demonstrations (ruling), so a surviving mutant is a finding only when a lesson sentence claims the lab
checks that property. Each mutant is written to lab_mutants/ and run with python -I -W error."""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = root / "ledgers/M7/scripts/M7-c-r3/lab_mutants"
out.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    "L07": [
        ("L07-min-for-max", "values[t][w] = max(period_reward(c)", "values[t][w] = min(period_reward(c)"),
        ("L07-strict-feasibility", "return tuple(c for c in GRID if c <= w)", "return tuple(c for c in GRID if c < w)"),
        ("L07-brute-ignores-bequest", "        total += bequest(wealth)\n        checked += 1", "        checked += 1"),
        ("L07-optimal-uses-same-period", "key=lambda x: period_reward(x) + values[t + 1][w - x])",
         "key=lambda x: period_reward(x) + values[t][w - x])"),
        ("L07-tail-check-vs-start-value", "plan_total(plan[k:], path[k]) == values[k][path[k]] for k in range(HORIZON)",
         "plan_total(plan[k:], path[k]) == values[0][path[k]] for k in range(HORIZON)"),
        ("L07-greedy-uses-min", "c = max(feasible(w), key=period_reward)", "c = min(feasible(w), key=period_reward)"),
    ],
    "L08": [
        ("L08-min-for-max-step", "    for s in STATES:\n        candidates = {a: reward(s, a) + DISCOUNT * u[next_state(s, a)] for a in ACTIONS}\n        top = max(candidates.values())",
         "    for s in STATES:\n        candidates = {a: reward(s, a) + DISCOUNT * u[next_state(s, a)] for a in ACTIONS}\n        top = min(candidates.values())"),
        ("L08-brute-drops-discount", "            weight *= DISCOUNT\n", "            weight *= 1\n"),
        ("L08-iterate-discount-squared", "    for _ in range(6):\n        new, _, _ = bellman_step(iterates[-1])",
         "    for _ in range(6):\n        new, _, _ = bellman_step({s: iterates[-1][s] * DISCOUNT for s in STATES})"),
        ("L08-brute-misses-terminal", "        total += weight * Fraction(0)\n", "        total += weight * Fraction(1)\n"),
        ("L08-policy-wrong-state-next", "    return 0\n", "    return 1\n"),
        ("L08-repair-cost-sign", "return Fraction(-REPAIR_COST)", "return Fraction(REPAIR_COST)"),
    ],
}

rows = []
for lid, items in MUTANTS.items():
    base = (root / f"tests/labs/M7/lab-M7-{lid}-1.py").read_text(encoding="utf-8")
    for name, old, new in items:
        if base.count(old) != 1:
            rows.append((lid, name, f"REPLACEMENT NOT UNIQUE ({base.count(old)})", ""))
            continue
        src = base.replace(old, new)
        path = out / f"{name}.py"
        path.write_text(src, encoding="utf-8")
        proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
        rows.append((lid, name, f"exit={proc.returncode}", proc.stdout.replace("\n", " | ") + (" STDERR:" + proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "")))
for lid, name, status, line in rows:
    print(f"{lid} {name} {status}")
    for token in line.split(" | "):
        if token.startswith(("recursion_", "optimal_plan_every", "greedy_plan_optimal", "iterate_equals", "tied_pairs", "plans_", "optimal_total", "optimal_consumption", "greedy_total", "greedy_tail", "policy t 0", "n 0 change", "n 5 change")):
            print("    ", token)
