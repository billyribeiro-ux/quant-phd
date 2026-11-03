"""Write three round-4 student-error mutants of the reference into ledgers/CS2/mutants/ (verifier round 4)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CS2/mutants"

MUTANTS = {
    "r4v_01_rank_target_rounds_q_and_eps_separately.py": (
        "Rank target takes ceil(q n) minus floor(eps n), rounding the two products separately.",
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
        "        target = max(1, math.ceil(Fraction(q) * self._n) - math.floor(self._exact_epsilon * self._n))\n",
    ),
    "r4v_02_rank_target_rounds_to_nearest.py": (
        "Rank target rounds q n minus eps n to the nearest integer instead of up to the next integer.",
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
        "        target = max(1, round(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
    ),
    "r4v_03_sample_variance_of_two_values_uses_population_divisor.py": (
        "Sample variance with exactly two values divides by n instead of n - 1.",
        "            return self._m2 / (self._count - 1)\n",
        "            return self._m2 / (self._count - 1 if self._count > 2 else self._count)\n",
    ),
}


def main() -> None:
    for name, (description, old, new) in MUTANTS.items():
        assert REF.count(old) == 1, (name, REF.count(old))
        body = REF.replace(old, new, 1)
        first, sep, rest = body.partition("\n")
        header = f'"""{description}\n'
        body = header + rest.split("\n", 0)[0] if False else body
        # Replace the reference's module docstring with one whose first line describes the error.
        start = body.index('"""')
        end = body.index('"""', start + 3) + 3
        module_doc = f'"""{description}\n\nVerifier round-4 student-error mutant of the CS2 reference (streamstats.py).\n"""'
        body = body[:start] + module_doc + body[end:]
        (OUT / name).write_text(body, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
