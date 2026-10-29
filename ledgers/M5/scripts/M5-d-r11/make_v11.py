import pathlib, sys
ref = pathlib.Path("course/modules/M/M5/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path("ledgers/M5/mutants")
specs = {
 "v11_01_utility_uses_capital_not_output.py": (
  "student-error: utility is sqrt(k - k') while feasibility still uses k**alpha, so the consumption in the utility ignores the production exponent.",
  "        available = k**alpha\n        best = -math.inf\n        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)",
  "        available = k**alpha\n        best = -math.inf\n        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(k - successor) + beta * continuation)"),
 "v11_02_operator_returns_the_best_successor_not_the_value.py": (
  "student-error: the Bellman operator returns the optimal successor capital k' (the policy) at each grid point instead of the maximised value.",
  "        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)\n        out.append(best)",
  "        arg = grid[0]\n        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                cand = math.sqrt(available - successor) + beta * continuation\n                if cand > best:\n                    best, arg = cand, successor\n        out.append(arg)"),
 "v11_03_converged_means_budget_not_exhausted.py": (
  "student-error: converged is read off the loop (iterations below the budget) instead of the certified error being within tol.",
  "        \"converged\": certified <= target,",
  "        \"converged\": iterations < budget,"),
}
for name, (desc, old, new) in specs.items():
    if name.startswith("v11_02"):
        body = ref.replace(old, new)
        assert body != ref
        # also the operator must still see the same _sweep signature: rename list comprehension ok
    else:
        assert ref.count(old) == 1, (name, ref.count(old))
        body = ref.replace(old, new)
    header = f'"""Student-error mutant (verifier-written, M5 slice d round 11): {desc}"""\n'
    if body.startswith('"""'):
        body = body.replace('"""', header, 1) if False else body
    (out / name).write_text(header + body.split('\n', 0)[0][0:0] + body, encoding="utf-8")
    print("wrote", name)
