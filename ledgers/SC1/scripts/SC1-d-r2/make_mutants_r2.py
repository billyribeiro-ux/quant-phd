"""Generate the round-2 verifier mutants (m18 to m21) as single-change copies of grader/reference.py."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/SC/SC1/grader/reference.py"
OUT = ROOT / "ledgers/SC1/mutants"

MUTANTS = {
    "m18_nested_coarse_count_copies_fine.py": (
        "Nested coarse count copied from the fine count: nested_grid_counts returns the fine count twice, so the coarse grid is never used.",
        "    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)\n",
        "    coarse = fine\n",
    ),
    "m19_grid_estimate_uses_endpoint_only.py": (
        "Running maximum forgotten: discrete_max_exceedance tests only the last grid value, not the maximum over the grid.",
        "    indicators = [1.0 if max(values) >= level else 0.0 for values in paths]\n",
        "    indicators = [1.0 if values[-1] >= level else 0.0 for values in paths]\n",
    ),
    "m20_draws_seeded_with_zero_for_every_instance.py": (
        "Seed ignored: _grid_paths seeds the Gaussian draws with 0 for every instance instead of instance seed.",
        '    rng = random.Random(int(instance["seed"]))\n    sd = math.sqrt(float(instance["H"]) / n_steps)\n',
        '    rng = random.Random(0)\n    sd = math.sqrt(float(instance["H"]) / n_steps)\n',
    ),
    "m21_coarse_stride_uses_n_coarse.py": (
        "Wrong subgrid: nested_grid_counts takes every n_coarse-th fine point instead of every n_fine / n_coarse-th.",
        "    stride = n_fine // n_coarse\n",
        "    stride = n_coarse\n",
    ),
}

source = REF.read_text(encoding="utf-8")
for name, (description, old, new) in MUTANTS.items():
    assert source.count(old) == 1, f"{name}: target line not found exactly once"
    body = source.replace(old, new)
    head, sep, rest = body.partition('"""')
    assert sep, "reference docstring not found"
    _, sep2, tail = rest.partition('"""')
    assert sep2, "reference docstring close not found"
    text = '"""' + description + '"""' + tail
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
