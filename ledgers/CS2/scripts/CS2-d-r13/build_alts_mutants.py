"""Build r13 student-error mutants and correct alternatives from the reference solution (text edits, asserted)."""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB13-CS2-d")
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CS2/scripts/CS2-d-r13"
MUT = ROOT / "ledgers/CS2/mutants"


def sub(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (text.count(old), old[:60])
    return text.replace(old, new)


def no_compress(text: str) -> str:
    return re.sub(r"(    def _compress\(self\) -> None:\n)(.*?)(\n    def quantile)", r"\1        return\3", text, flags=re.S)


MUTANTS = {
    "r13_01_welford_skips_repeated_value.py": lambda t: sub(
        t, "        self._count += 1\n        delta = x - self._mean\n",
        "        if self._count and x == self._mean:\n            return\n        self._count += 1\n        delta = x - self._mean\n"),
    "r13_02_sample_variance_of_two_values_is_zero.py": lambda t: sub(
        t, "            return self._m2 / (self._count - 1)\n",
        "            if self._count == 2:\n                return 0.0\n            return self._m2 / (self._count - 1)\n"),
    "r13_03_rank_slack_uses_n_minus_one.py": lambda t: sub(
        t, "Fraction(q) * self._n - self._exact_epsilon * self._n))",
        "Fraction(q) * self._n - self._exact_epsilon * (self._n - 1)))"),
}

ALTS = {
    "alt_r13_A_sketch_never_compresses.py": no_compress,
    "alt_r13_B_rank_target_as_negated_floor.py": lambda t: sub(
        t, "math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n)",
        "-((Fraction(q) * self._n - self._exact_epsilon * self._n) * -1 // 1) * 1 * 1"
        if False else "-((self._exact_epsilon * self._n - Fraction(q) * self._n) // 1)"),
}

if __name__ == "__main__":
    for name, fn in MUTANTS.items():
        (MUT / name).write_text(fn(REF), encoding="utf-8")
        print("mutant", name)
    OUT.joinpath("alts").mkdir(exist_ok=True)
    for name, fn in ALTS.items():
        (OUT / "alts" / name).write_text(fn(REF), encoding="utf-8")
        print("alt", name)
    sys.exit(0)

# r13 second pass: replace the equivalent-under-guarantee mutant with a real violation, add a predecessor mutant
def second_pass() -> None:
    (MUT / "r13_03_rank_slack_uses_n_plus_one.py").write_text(
        sub(REF, "Fraction(q) * self._n - self._exact_epsilon * self._n))",
            "Fraction(q) * self._n - self._exact_epsilon * (self._n + 1)))"), encoding="utf-8")
    (MUT / "r13_04_quantile_returns_predecessor.py").write_text(
        sub(REF, "            if rank >= target:\n                return value\n        return self._values[-1]",
            "            if rank >= target:\n                return self._values[max(0, self._values.index(value) - 1)]\n        return self._values[-1]"),
        encoding="utf-8")
