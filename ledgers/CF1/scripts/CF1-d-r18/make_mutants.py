"""Write the round-18 (slice d) student-error mutants of grader/reference.py into ledgers/CF1/mutants/.

Each mutant is the reference with one plausible student error; the one-line docstring is the description that
mutate_graders prints. Each replacement must match exactly once.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
dest = root / "ledgers/CF1/mutants"


def edit(old: str, new: str, header: str) -> str:
    assert ref.count(old) == 1, old
    text = ref.replace(old, new)
    return f'"""{header}\n\nMutant of the reference solution for the CF1 capital-budgeting engine (capbudget.py).\n"""' + text.split('"""', 2)[2]


m1 = edit(
    "def payback_period(flows: Sequence[float], rate: float = 0.0) -> float:\n"
    '    """Payback in fractional years. rate = 0 is simple payback; rate > 0 discounts each flow first.\n\n'
    "    The first year t with cumulative (discounted) flow >= 0 gives (t - 1) + (-cumulative at t - 1) / flow at t.\n"
    '    Returns math.inf when the outlay is never recovered within the horizon.\n    """\n    _check_rate(rate)\n',
    "def payback_period(flows: Sequence[float], rate: float = 0.0) -> float:\n"
    '    """Payback in fractional years. rate = 0 is simple payback; rate > 0 discounts each flow first.\n\n'
    "    The first year t with cumulative (discounted) flow >= 0 gives (t - 1) + (-cumulative at t - 1) / flow at t.\n"
    '    Returns math.inf when the outlay is never recovered within the horizon.\n    """\n'
    "    if rate <= -1.0:\n        raise ValueError('rate must be above -1')\n",
    "d18_m01: A discounted payback with a rate of nan is accepted: the rate check tests only rate <= -1, not finiteness.",
)
m2 = edit(
    "    _check_rate(real)\n    _check_rate(inflation)\n",
    "    _check_rate(real)\n    if inflation <= -1.0:\n        raise ValueError('inflation must be above -1')\n",
    "d18_m02: A Fisher conversion with an inflation of nan is accepted: the inflation check tests only inflation <= -1.",
)
m3 = edit(
    "    _check_project(project)\n    _check_rate(rate)\n    if not isinstance(seed, int)",
    "    _check_project(project)\n    if rate <= -1.0:\n        raise ValueError('rate must be above -1')\n    if not isinstance(seed, int)",
    "d18_m03: A Monte Carlo request with a rate of nan is accepted: the rate guard is rate <= -1 and no finiteness test.",
)
m4 = edit(
    "    _check_rate(real)\n    _check_rate(inflation)\n    return",
    "    _check_rate(real)\n    return",
    "d18_m04: A Fisher conversion with inflation of -1 or below is accepted: the inflation argument is never checked.",
)
for name, text in [
    ("d18_m01_payback_nan_rate_accepted.py", m1),
    ("d18_m02_fisher_nan_inflation_accepted.py", m2),
    ("d18_m03_monte_carlo_nan_rate_accepted.py", m3),
    ("d18_m04_fisher_inflation_never_checked.py", m4),
]:
    (dest / name).write_text(text, encoding="utf-8")
print("wrote 4 mutants")
