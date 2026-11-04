"""Build scratch variants of the M4 reference for the round-5 checks (never written to the mutant directory)."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
ref = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")

OLD_LOOP = """    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
"""
assert ref.count(OLD_LOOP) == 1

def variant(name, new_loop, extra_fix=None):
    text = ref.replace(OLD_LOOP, new_loop)
    if extra_fix:
        old, new = extra_fix
        assert text.count(old) == 1, name
        text = text.replace(old, new)
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "tail_risk.py").write_text(text, encoding="utf-8")
    return d

# S1: one chi-square variable shared by draws 2k and 2k+2 (all even-indexed draws share it); odd draws own theirs.
S1 = """    rng = random.Random(seed)
    losses: list[int] = []
    shared_even = None
    for k_draw in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            if k_draw % 2 == 0:
                if shared_even is None:
                    shared_even = rng.gammavariate(nu / 2, 2.0)
                chi_square = shared_even
            else:
                chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
"""
# S2: draws 2k and 2k+1 share (the r9_03 pattern, reproduced as a scratch check).
S2 = """    rng = random.Random(seed)
    losses: list[int] = []
    last_chi = 1.0
    for k_draw in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            if k_draw % 2 == 0:
                last_chi = rng.gammavariate(nu / 2, 2.0)
            chi_square = last_chi
            scale = math.sqrt(matched * nu / chi_square)
"""
# M9_01: the normal vector Z is drawn once per run and reused for every draw (student error).
M9_01 = """    rng = random.Random(seed)
    losses: list[int] = []
    z_once = [rng.gauss(0.0, 1.0) for _ in range(n)]
    for _ in range(n_draws):
        z = z_once
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
"""
# M9_02: the Gaussian family also draws a chi-square variable it never uses (student error: changes the frozen stream).
M9_02 = """    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
        else:
            rng.gammavariate(1.0, 2.0)
"""
# A6: alternative correct implementation: float ceiling for the quantile index (equal to the exact index for n <= 200000).
A6 = ("    index = (99 * len(losses_cents) + 99) // 100\n", "    index = math.ceil(0.99 * len(losses_cents))\n")
# A7: alternative correct implementation: the matched factor via the explicit sqrt(s) sqrt(nu / W) product.
A7 = None

for name, loop, fix in [
    ("S1_shared_even", S1, None),
    ("S2_shared_adjacent", S2, None),
    ("M9_01_z_once", M9_01, None),
    ("M9_02_gaussian_unused_chi", M9_02, None),
    ("A6_float_ceil", OLD_LOOP, A6),
]:
    d = variant(name, loop, fix)
    print("wrote", d / "tail_risk.py")
