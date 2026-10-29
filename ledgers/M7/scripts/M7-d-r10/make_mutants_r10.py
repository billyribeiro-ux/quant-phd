"""Write three new student-error mutants of the M7 reference solver into ledgers/M7/mutants (round 10)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"
src = REF.read_text(encoding="utf-8")

def make(name: str, description: str, old: str, new: str) -> None:
    assert src.count(old) == 1, (name, src.count(old))
    body = src.replace(old, new)
    body = body.replace('"""Reference solution', f'"""{description}\n\nReference solution', 1)
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")

make(
    "v10_01_dual_residual_ignores_sector_and_turnover_multipliers",
    "Student error v10_01: the dual residual checks only the box multipliers, so a negative sector or turnover multiplier is reported as dual-feasible.",
    '''    mult_ineq: list[Fraction] = [
        *sol["lower"],
        *sol["upper"],
        *sol["sector"],
        *sol["plus"],
        *sol["minus"],
        sol["kappa"],
    ]''',
    '''    mult_ineq: list[Fraction] = [
        *sol["lower"],
        *sol["upper"],
    ]''',
)
make(
    "v10_02_complementary_slackness_signed_not_absolute",
    "Student error v10_02: the complementary-slackness residual is the largest signed product of a multiplier and its constraint, with the absolute value left out.",
    '''    complementary = max(
        abs(m * g)''',
    '''    complementary = max(
        (m * g)''',
)
make(
    "v10_03_turnover_total_sign_in_stationarity",
    "Student error v10_03: the turnover-variable stationarity residual adds the two turnover multipliers to the total instead of subtracting them, a sign slip in the certificate.",
    '''        r_t = sol["kappa"] - sol["plus"][i] - sol["minus"][i]''',
    '''        r_t = sol["kappa"] + sol["plus"][i] - sol["minus"][i]''',
)
print("wrote 3 mutants")
