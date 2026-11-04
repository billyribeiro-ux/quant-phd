"""Round-7 verifier (slice d): five alternative correct implementations of tail_risk.py, per plan 5.5.

Each variant is derived from grader/reference.py by a textual edit; the edit is asserted to apply exactly once.
Variants 1, 2 and 4 change only the Student-t random stream (plan 5.5); the Gaussian family keeps random.gauss.
"""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1]).read_text()
OUT = pathlib.Path(__file__).resolve().parent


def sub(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, old[:60]
    return src.replace(old, new)


LOOP_OLD = "        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n"
assert REF.count(LOOP_OLD) == 1

BOX = (
    "        if student:\n"
    "            z = []\n"
    "            while len(z) < n:\n"
    "                u1 = rng.random()\n"
    "                u2 = rng.random()\n"
    "                while u1 <= 0.0:\n"
    "                    u1 = rng.random()\n"
    "                r = math.sqrt(-2.0 * math.log(u1))\n"
    "                z.append(r * math.cos(2.0 * math.pi * u2))\n"
    "                if len(z) < n:\n"
    "                    z.append(r * math.sin(2.0 * math.pi * u2))\n"
    "        else:\n"
    "            z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n"
)
POLAR = (
    "        if student:\n"
    "            z = []\n"
    "            while len(z) < n:\n"
    "                while True:\n"
    "                    a = 2.0 * rng.random() - 1.0\n"
    "                    b = 2.0 * rng.random() - 1.0\n"
    "                    s = a * a + b * b\n"
    "                    if 0.0 < s < 1.0:\n"
    "                        break\n"
    "                m = math.sqrt(-2.0 * math.log(s) / s)\n"
    "                z.append(a * m)\n"
    "                if len(z) < n:\n"
    "                    z.append(b * m)\n"
    "        else:\n"
    "            z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n"
)
alt1 = sub(REF, LOOP_OLD, BOX)
alt2 = sub(REF, LOOP_OLD, POLAR)
(OUT / "alt1_box_muller_student.py").write_text(alt1)
(OUT / "alt2_polar_student.py").write_text(alt2)

# alt3: Cholesky factor computed column by column (different order, same factor)
REF_CHOL = REF[REF.index("    factor = [[0.0] * n for _ in range(n)]\n"): REF.index("    return factor\n")]
assert REF.count(REF_CHOL) == 1
COL = (
    "    factor = [[0.0] * n for _ in range(n)]\n"
    "    for j in range(n):\n"
    "        pivot = cov[j][j] - sum(factor[j][k] * factor[j][k] for k in range(j))\n"
    "        if not pivot > 0.0:\n"
    "            raise ValueError(\"cov must be positive definite: every Cholesky pivot must be above zero\")\n"
    "        factor[j][j] = math.sqrt(pivot)\n"
    "        for i in range(j + 1, n):\n"
    "            factor[i][j] = (cov[i][j] - sum(factor[i][k] * factor[j][k] for k in range(j))) / factor[j][j]\n"
)
alt3 = sub(REF, REF_CHOL, COL)
(OUT / "alt3_column_cholesky.py").write_text(alt3)

# alt4: integer-nu chi-square as a sum of nu squared normals (Student-t stream only)
CHI_OLD = "            chi_square = rng.gammavariate(nu / 2, 2.0)\n"
CHI_NEW = "            chi_square = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))\n"
alt4 = sub(REF, CHI_OLD, CHI_NEW)
(OUT / "alt4_chi_square_sum_of_normals.py").write_text(alt4)

# alt5: quantile by heapq.nsmallest (same order statistic)
Q_OLD = "    return sorted(losses_cents)[index - 1]\n"
assert REF.count(Q_OLD) == 1
Q_NEW = "    import heapq\n\n    return heapq.nsmallest(index, losses_cents)[-1]\n"
alt5 = sub(REF, Q_OLD, Q_NEW)
(OUT / "alt5_heapq_quantile.py").write_text(alt5)
print("wrote 5 alternatives")
