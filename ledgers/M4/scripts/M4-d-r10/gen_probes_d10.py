"""Round-10 verifier D: writes chi-square sharing probes (Student-t draws whose chi-square variable is taken from an owner draw).

Each probe is the reference module with one owner rule: draw i uses the chi-square of draw owner(i). A draw that owns its
chi-square draws a fresh gamma variate; every other draw reuses the stored value of its owner. Every draw stores the value it
used, so a chain (owner of owner) resolves. Probes: the reference (owner(i) = i), lag-one, lag-two and lag-three pairs,
all-even sharing, the lag-four chain (draws 4j and 4j+4), and disjoint lag-four pairs (draws 8j and 8j+4).
"""

from pathlib import Path
import shutil

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
GRADER = ROOT / "course/modules/M/M4/grader"
PROBES = ROOT / "ledgers/M4/scripts/M4-d-r10/probes"
REF = (GRADER / "reference.py").read_text(encoding="utf-8")
OWNERS = {
    "ref": "i",
    "lag1_pairs_2k_2k1": "i - (i % 2)",
    "lag2_pairs_4j_4j2": "(i - 2) if i % 4 == 2 else i",
    "lag3_pairs_6j_6j3": "(i - 3) if i % 6 == 3 else i",
    "even_all_share": "0 if i % 2 == 0 else i",
    "chain_lag4_4j_4j4": "(i - 4) if (i % 4 == 0 and i >= 4) else i",
    "disjoint_lag4_8j_8j4": "(i - 4) if i % 8 == 4 else i",
}
OLD_LOOP = """    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
"""
NEW_LOOP = """    chi_values: dict[int, float] = {}
    for draw in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            owner = OWNER(draw)
            if owner == draw:
                chi_values[draw] = rng.gammavariate(nu / 2, 2.0)
            chi_square = chi_values[owner]
            chi_values[draw] = chi_square
            scale = math.sqrt(matched * nu / chi_square)
"""


def main() -> None:
    assert REF.count(OLD_LOOP) == 1
    for name, expr in OWNERS.items():
        folder = PROBES / name
        folder.mkdir(parents=True, exist_ok=True)
        text = REF.replace(OLD_LOOP, NEW_LOOP)
        text = text.replace("def simulate_losses(", "def OWNER(i: int) -> int:\n    return " + expr + "\n\n\ndef simulate_losses(", 1)
        (folder / "tail_risk.py").write_text(text, encoding="utf-8")
        shutil.copy(GRADER / "instance.py", folder / "instance.py")
        shutil.copy(GRADER / "test_project.py", folder / "test_project.py")
        print("wrote", name, "owner:", expr)


if __name__ == "__main__":
    main()
