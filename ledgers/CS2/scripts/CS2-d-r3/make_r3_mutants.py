"""Write the round-3 student-error mutants as single-change copies of the reference grader solution.

Each mutant's docstring first line (written below) describes the error. Usage: python -I make_r3_mutants.py <repo_root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ref = (root / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/CS2/mutants"

CHANGES = {
    "r3_01_welford_mean_divides_by_count_minus_one.py": (
        "The Welford mean update divides the deviation by count - 1 instead of count.",
        "        self._mean += delta / self._count\n",
        "        self._mean += delta / (self._count - 1) if self._count > 1 else 0.0\n",
    ),
    "r3_02_compression_drops_removed_weight.py": (
        "Sketch compression removes an interior tuple but does not add its g to the successor, so the stored weight falls below n.",
        "                self._g[i + 1] += self._g[i]\n",
        "                pass\n",
    ),
    "r3_03_quantile_returns_last_value_within_target.py": (
        "quantile(q) returns the last stored value whose running rank is still at most the target, not the first at or past it.",
        "            if rank >= target:\n                return value\n        return self._values[-1]\n",
        "            if rank > target:\n                return previous\n            previous = value\n        return self._values[-1]\n",
    ),
    "r3_04_new_tuple_weight_zero.py": (
        "Sketch add stores the new value with g = 0, so the stored weights no longer sum to the count.",
        "        self._g.insert(position, 1)\n",
        "        self._g.insert(position, 0)\n",
    ),
}

for name, (doc, old, new) in CHANGES.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new)
    if name.startswith("r3_03"):
        # the loop must remember the previous stored value; the first-index loop starts with previous = values[0]
        text = text.replace("        rank = 0\n        for value, g in zip(self._values, self._g, strict=True):\n",
                            "        rank = 0\n        previous = self._values[0]\n        for value, g in zip(self._values, self._g, strict=True):\n")
        text = text.replace("            rank += g\n", "            rank += g\n", 1)
        assert "previous = self._values[0]" in text
    # replace the module docstring with the mutant's description (first line is the error)
    body = text.split('"""', 2)[2]
    text = f'"""{doc}\n\nSingle-change copy of the reference solution.\n"""' + body
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
