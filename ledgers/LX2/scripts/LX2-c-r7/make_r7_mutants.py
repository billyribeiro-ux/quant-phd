"""Write this round's Lab 2 student-error mutants as complete modules (the twin with both blanks filled, then one error)."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
twin = (ROOT / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
base = twin  # the twin is the completed solution
assert "hit_rate = Fraction(hits, horizon)" in base and "bias = Fraction(sum(errors), horizon)" in base
MUT = {
    "r7_lab2_one_sided_band": (
        "Student error: the hit test checks only the upper side of the band (error <= 2), so large negative errors count as hits.",
        "    return abs(predicted - realised) <= HIT_BAND",
        "    return predicted - realised <= HIT_BAND",
    ),
    "r7_lab2_edge_months_at_or_beyond_band": (
        "Student error: the edge list uses >= 2 where the page states exactly 2, so months outside the band are listed as edge months.",
        "if abs(e) == HIT_BAND]",
        "if abs(e) >= HIT_BAND]",
    ),
    "r7_lab2_window_one_month_early": (
        "Student error: the window starts at month 12, the last calibration month, so every forecast is read one month early.",
        "        t = START_MONTH + offset\n",
        "        t = START_MONTH + offset - 1\n",
    ),
    "r7_lab2_rounds_through_python_round": (
        "Student error: rounds each value with Python's round() on a binary float, which sends a tie to even where the page states half up.",
        '    print(f"Part B: hits {hits} of {horizon}; hit rate {decimal_text(hit_rate, 4)}")',
        '    print(f"Part B: hits {hits} of {horizon}; hit rate {round(float(hit_rate), 4):.4f}")',
    ),
}
for name, (doc, old, new) in MUT.items():
    assert base.count(old) == 1, (name, base.count(old))
    body = base.replace(old, new)
    first, rest = body.split('"""', 2)[1], body.split('"""', 2)[2]
    head = f'"""{doc}\n' + '\n'.join(first.split('\n')[1:]) + '"""' + rest
    (ROOT / f"ledgers/LX2/mutants/{name}.py").write_text(head, encoding="utf-8")
    print("wrote", name)
