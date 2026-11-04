"""Write the round-5 student-error mutants of the M4 reference into ledgers/M4/mutants (one module each)."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ref = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OLD_DOC = ref.split('"""')[1]
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

MUTANTS = {
    "v9_01_chi_square_shared_by_even_draws": (
        "Verifier round-5 student-error mutant (v9). All even-indexed Student-t draws share one chi-square variable, so draws 2k and 2k+2 share it; the test of independent chi-square variables sees it on some seeds, the cross-term tests on all.",
        """    rng = random.Random(seed)
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
""",
    ),
    "v9_02_normal_vector_drawn_once_per_run": (
        "Verifier round-5 student-error mutant (v9). The standard normal vector Z is drawn once per run and reused for every draw, so the draws are not independent.",
        """    rng = random.Random(seed)
    losses: list[int] = []
    z_once = [rng.gauss(0.0, 1.0) for _ in range(n)]
    for _ in range(n_draws):
        z = z_once
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
""",
    ),
    "v9_03_gaussian_stream_draws_unused_chi_square": (
        "Verifier round-5 student-error mutant (v9). The Gaussian family also draws a chi-square variable it never uses, which shifts the frozen Gaussian stream.",
        """    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
        else:
            rng.gammavariate(1.0, 2.0)
""",
    ),
    "v9_04_student_t_scale_drops_chi_square_ratio": (
        "Verifier round-5 student-error mutant (v9). The Student-t family scales by the matched factor alone and drops the chi-square ratio, so its tails are Gaussian.",
        """    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched)
""",
    ),
}

out = ROOT / "ledgers/M4/mutants"
for name, (doc, loop) in MUTANTS.items():
    text = ref.replace(OLD_LOOP, loop).replace(OLD_DOC, doc + "\n\nMutant of the M4 reference (tail_risk.py). All inputs are SIMULATED.\n", 1)
    (out / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
