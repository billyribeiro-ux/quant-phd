"""Writes the round-8 slice-d student-error mutants from grader/reference.py (one textual change each).

Each replacement must match exactly once, so a changed reference fails loudly. Output: ledgers/M4/mutants/r8d_*.py.
Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/make_mutants_r8.py
"""

import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M4/mutants"

MUTANTS = {
    "r8d_01_symmetry_checked_to_absolute_tolerance_1e9.py": (
        "Round-8 verifier (slice d) student-error mutant: symmetry is checked to an absolute tolerance of 1e-9, so a "
        "covariance whose off-diagonal entries differ by 1e-15 (entries of order 1e-14) is accepted as symmetric.",
        "            if cov[i][j] != cov[j][i]:\n",
        "            if abs(cov[i][j] - cov[j][i]) > 1e-9:\n",
    ),
    "r8d_02_gaussian_stream_reseeded_per_draw.py": (
        "Round-8 verifier (slice d) student-error mutant: each draw restarts the generator at seed plus the draw index, "
        "so the Gaussian stream is not the one Conventions item 5 freezes.",
        "        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n",
        "        rng = random.Random(seed + _)\n        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n",
    ),
    "r8d_03_positions_read_in_reverse_order.py": (
        "Round-8 verifier (slice d) student-error mutant: the positions are read in reverse order, so position i is "
        "weighted by the covariance row of the other asset in a two-asset portfolio.",
        "            total += position_cents[i] * ret\n",
        "            total += position_cents[n - 1 - i] * ret\n",
    ),
    "r8d_04_gaussian_draws_via_normalvariate.py": (
        "Round-8 verifier (slice d) student-error mutant: the normals are drawn with random.Random.normalvariate, "
        "a different transform of the same generator, instead of gauss, so the frozen Gaussian stream differs.",
        "        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n",
        "        z = [rng.normalvariate(0.0, 1.0) for _ in range(n)]\n",
    ),
}

if __name__ == "__main__":
    for name, (doc, old, new) in MUTANTS.items():
        assert REF.count(old) == 1, f"{name}: target text must occur exactly once (found {REF.count(old)})"
        body = REF.replace(old, new)
        first, _, rest = body.partition('"""')
        docstring_body, _, tail = rest.partition('"""')
        new_doc = doc + "\n\n" + docstring_body.split("\n", 1)[1].lstrip("\n") if "\n" in docstring_body else doc
        text = f'"""{doc}\n\n{docstring_body.strip()}\n"""' + tail
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)
