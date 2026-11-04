"""Write five new student-error mutants of the M7 reference as complete solution modules (round 7, M7-d).

Each mutant is reference.py with one plausible error injected by an exact string replacement (the replacement must
match exactly once). Run: python -I make_mutants_r7.py <reference.py> <out_dir>
"""
import sys
from pathlib import Path

ref = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

mutants = {
    "r7_01_sector_cap_measured_from_starting_sector_weight.py": (
        '"""Student error r7_01: each sector cap is measured from the starting sector weight, so the cap is loosened by the starting sector sum."""\n',
        [(
            "        rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap, (\"sector\", k)))",
            "        start_sector = sum((problem.w0[j] for j in range(n) if problem.sector[j] == k), Fraction(0))\n"
            "        rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap + start_sector, (\"sector\", k)))",
        )],
    ),
    "r7_02_start_box_checked_to_1e-8_not_1e-9.py": (
        '"""Student error r7_02: the starting weights are checked against their box bounds with a tolerance of 1e-8, not the 1e-9 the page states."""\n',
        [(
            "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):",
            "    if any(w0[i] < lower[i] - Fraction(1, 10**8) or w0[i] > upper[i] + Fraction(1, 10**8) for i in range(n)):",
        )],
    ),
    "r7_03_gamma_refused_below_one_millionth.py": (
        '"""Student error r7_03: gamma is refused below one millionth, although the page accepts any positive gamma (the suite tests one billionth)."""\n',
        [(
            "    if gamma <= 0:\n        raise ValueError(\"gamma must be positive\")",
            "    if gamma <= 0:\n        raise ValueError(\"gamma must be positive\")\n"
            "    if gamma < Fraction(1, 10**6):\n        raise ValueError(\"gamma is too small to use\")",
        )],
    ),
    "r7_04_active_set_drops_first_working_row.py": (
        '"""Student error r7_04: a negative multiplier removes the first working constraint, not the one with the most negative multiplier."""\n',
        [("            working.pop(min(negative)[1])", "            working.pop(0)")],
    ),
    "r7_05_sector_cap_sign_reversed.py": (
        '"""Student error r7_05: each sector cap is written as a lower bound on the sector sum (the inequality sign is reversed)."""\n',
        [(
            "        rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap, (\"sector\", k)))",
            "        rows.append(([Fraction(-1) if problem.sector[j] == k else Fraction(0) for j in range(n)], -cap, (\"sector\", k)))",
        )],
    ),
}
for name, (doc, reps) in mutants.items():
    text = ref
    # replace the module docstring (the first triple-quoted block) with the error description
    start = text.index('"""')
    end = text.index('"""', start + 3) + 3
    text = doc + text[end:].lstrip("\n").join(["", ""]) if False else doc + text[end:]
    for old, new in reps:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", out / name)
