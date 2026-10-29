"""Verifier r8: writes three new student-error mutants of the M4 reference into ledgers/M4/mutants/."""
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-M4-d")
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M4/mutants"


def swap(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, old
    return src.replace(old, new)


MUTANTS = {
    "r8_01_student_t_chi_square_drawn_once_per_run.py": (
        "Verifier round-8 student-error mutant. The chi-square variable W is drawn once for the whole run, "
        "not once per draw, so every Student-t draw shares one scale.",
        [("    rng = random.Random(seed)\n    losses: list[int] = []\n    for _ in range(n_draws):\n",
          "    rng = random.Random(seed)\n    losses: list[int] = []\n"
          "    shared = rng.gammavariate(nu / 2, 2.0) if student and nu is not None else None\n"
          "    for _ in range(n_draws):\n"),
         ("            chi_square = rng.gammavariate(nu / 2, 2.0)\n",
          "            chi_square = shared\n")],
    ),
    "r8_02_quantile_index_one_low_at_multiples_of_100.py": (
        "Verifier round-8 student-error mutant. The 99% index is one too low when n is a multiple of 100, "
        "a boundary slip in the ceiling of 0.99 n.",
        [("    index = (99 * len(losses_cents) + 99) // 100\n",
          "    index = (99 * len(losses_cents) + 99) // 100\n"
          "    if len(losses_cents) % 100 == 0:\n"
          "        index -= 1\n")],
    ),
    "r8_03_student_t_matched_scale_on_first_asset_only.py": (
        "Verifier round-8 student-error mutant. The matched scale is applied to the first asset's return only, "
        "so the other assets' Student-t returns are unscaled.",
        [("            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))\n",
          "            ret = (scale if i == 0 or not student else 1.0) * sum(factor[i][k] * z[k] for k in range(i + 1))\n")],
    ),
}

for name, (doc, edits) in MUTANTS.items():
    src = REF
    for old, new in edits:
        src = swap(src, old, new)
    src = src.replace('"""Reference solution', '"""' + doc + "\n\nReference solution", 1)
    (OUT / name).write_text(src)
    print("wrote", name)
