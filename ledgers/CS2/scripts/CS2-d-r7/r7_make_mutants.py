"""Write the verifier's round-7 student-error mutants as complete modules (each a one-change copy of reference.py)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CS2/mutants"

def change(src, old, new, count=1):
    assert src.count(old) == count, (old, src.count(old))
    return src.replace(old, new)

mutants = {
    # the answer is read by position in the stored list instead of by rank (stored index is not the rank once tuples merge)
    "r7v_01_quantile_returns_stored_position_not_rank.py": (
        "Quantile answer taken as the stored tuple at position target-1 instead of the first tuple whose running rank reaches the target.",
        change(REF,
               "        rank = 0\n        for value, g in zip(self._values, self._g, strict=True):\n            rank += g\n            if rank >= target:\n                return value\n        return self._values[-1]",
               "        if target - 1 < len(self._values):\n            return self._values[target - 1]\n        return self._values[-1]"),
    ),
    # compression ignores the uncertainty delta of the tuple it folds into its successor
    "r7v_02_compression_ignores_delta_in_cap.py": (
        "Compression folds a tuple into its successor whenever g_i + g_{i+1} fits the cap, ignoring the successor's delta.",
        change(REF,
               "            if self._g[i] + self._g[i + 1] + self._delta[i + 1] <= cap:",
               "            if self._g[i] + self._g[i + 1] <= cap:"),
    ),
    # a new interior tuple is stored with delta 0, so its rank is recorded as exact when it is not
    "r7v_03_interior_insert_stores_delta_zero.py": (
        "A value inserted between two stored values is recorded with delta 0, claiming its rank is exact.",
        change(REF,
               "        delta = 0 if position == 0 or position == len(self._values) else self._g[position] + self._delta[position] - 1",
               "        delta = 0"),
    ),
    # the rolling window keeps values from the window before the last one (off by one at the expiry test only)
    "r7v_04_welford_mean_update_uses_new_count_for_delta.py": (
        "Welford mean update divides the old-mean deviation by the old count, so the mean drifts on every update after the first.",
        change(REF,
               "        self._mean += delta / self._count",
               "        self._mean += delta / (self._count - 1 if self._count > 1 else 1)"),
    ),
}
for name, (desc, src) in mutants.items():
    body = f'"""{desc}"""\n' + src.split('"""', 2)[2]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
