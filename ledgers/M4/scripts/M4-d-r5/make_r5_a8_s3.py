"""Scratch variants A8 (chi-square from squared normals) and S3 (pairwise sharing 4j/4j+2), built from reference.py."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
ref = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OLD = """            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
"""
A8 = """            chi_square = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
            scale = math.sqrt(matched * nu / chi_square)
"""
assert ref.count(OLD) == 1
d = OUT / "A8_chi_from_squared_normals"
d.mkdir(parents=True, exist_ok=True)
(d / "tail_risk.py").write_text(ref.replace(OLD, A8), encoding="utf-8")
S3_LOOP = """    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
"""
S3 = """    rng = random.Random(seed)
    losses: list[int] = []
    chis: list[float] = []
    for k_draw in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            if k_draw % 4 == 2:
                chi_square = chis[k_draw - 2]
            else:
                chi_square = rng.gammavariate(nu / 2, 2.0)
            chis.append(chi_square)
            scale = math.sqrt(matched * nu / chi_square)
"""
assert ref.count(S3_LOOP) == 1
d = OUT / "S3_pairwise_even"
d.mkdir(parents=True, exist_ok=True)
(d / "tail_risk.py").write_text(ref.replace(S3_LOOP, S3), encoding="utf-8")
print("wrote A8 and S3")
