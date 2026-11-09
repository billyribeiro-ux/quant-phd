"""Write round-4 student-error mutants of the E1 reference into ledgers/E1/mutants/ (one change each)."""

from pathlib import Path
import sys

CHK = Path(sys.argv[1]).resolve()
REF = (CHK / "course/modules/E/E1/grader/reference.py").read_text()
OUT = CHK / "ledgers/E1/mutants"


def mutate(name: str, description: str, old: str, new: str, extra_import: str = "") -> None:
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    end = body.index('"""', 3) + 3
    body = f'"""{description}"""' + body[end:]
    if extra_import:
        body = body.replace("import math\n", "import math\n" + extra_import, 1)
    (OUT / f"{name}.py").write_text(body)
    print("wrote", name)


mutate(
    "e1d_r4_m01_invalid_input_returns_zeros",
    "Invalid inputs return six zero outputs instead of raising ValueError, a silent fallback.",
    "    check_inputs(structure, a, b, c)\n",
    "    try:\n        check_inputs(structure, a, b, c)\n    except ValueError:\n"
    "        return {k: 0 for k in (\"volume_trades\", \"fee_cents\", \"profit_cents\", \"consumer_surplus_cents\","
    " \"welfare_cents\", \"deadweight_loss_cents\")}\n",
)
mutate(
    "e1d_r4_m02_volume_banker_rounding",
    "Trade volume rounded by Python round(), so an exact half trade goes to the even neighbour; money keys still go up.",
    '"volume_trades": half_up(volume),',
    '"volume_trades": round(volume),',
)
mutate(
    "e1d_r4_m03_cournot_three_exchanges",
    "Cournot computed for three exchanges (volume 3d/4, fee (a + 3bc)/(4b)) instead of two.",
    "        volume = 2 * d / 3\n        fee = Fraction(a + 2 * b * c, 3 * b)",
    "        volume = 3 * d / 4\n        fee = Fraction(a + 3 * b * c, 4 * b)",
)
mutate(
    "e1d_r4_m04_monopoly_profit_halved",
    "Profit computed as the margin times the volume divided by two, for every structure, so the monopoly profit is halved.",
    "    profit = (fee - c) * volume\n",
    "    profit = (fee - c) * volume / 2\n",
)
