"""Write three alternative correct engines (CF1 round 18, slice d) from grader/reference.py by text edits.

Each replacement must match exactly once; the alternatives keep every contract number (4001 grid points,
window [1e-4, 1e4], 1e-7 root precision, the validation rules) and change only the numerical algorithm or style.
"""

import sys
from pathlib import Path

ref = Path(sys.argv[1]) / "course/modules/CF/CF1/grader/reference.py"
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
src = ref.read_text(encoding="utf-8")


def edit(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    return text


alt1 = edit(
    src,
    [
        (
            "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
            "    df = 1.0\n    terms = []\n    for cf in flows:\n        terms.append(cf * df)\n        df /= 1.0 + rate\n    return math.fsum(terms)",
        ),
    ],
)
alt2 = edit(
    src,
    [
        ("                if hi - lo <= 1e-15 * hi:", "                if hi - lo <= 1e-13 * hi:"),
        (
            "    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n    cumulative = discounted[0]",
            "    discounted = [cf * (1.0 + rate) ** (-t) for t, cf in enumerate(flows)]\n    cumulative = discounted[0]",
        ),
    ],
)
alt3 = edit(
    src,
    [
        (
            '    if not _finite(rate) or rate <= -1.0:',
            "    if not (rate > -1.0) or not math.isfinite(rate):",
        ),
    ],
)
(out / "alt_d18_1_running_discount_factor_fsum.py").write_text(alt1, encoding="utf-8")
(out / "alt_d18_2_tighter_bisection_and_multiplied_discount.py").write_text(alt2, encoding="utf-8")
(out / "alt_d18_3_inverted_rate_guard.py").write_text(alt3, encoding="utf-8")
print("wrote", sorted(p.name for p in out.glob("alt_d18_*.py")))
