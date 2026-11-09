"""Write the slice-d round-1 student-error mutants (complete modules derived from grader/reference.py).

Each replacement must match exactly once in the reference text, so a mutant is never silently the reference.
Usage: python3 -I ledgers/M5/scripts/M5-d-r1/d_make_mutants.py
"""

import os

REPO = "/Users/billyribeiro/.fanout/wt/verifyS1-M5-d"
REF = os.path.join(REPO, "course/modules/M/M5/grader/reference.py")
OUT = os.path.join(REPO, "ledgers/M5/mutants")

MUTANTS = {
    "d1_01_top_grid_point_never_a_successor.py": (
        "Student-error mutant (M5 slice d round 1): the successor loop stops one point early, so the top grid point is never a saving, which is wrong on a grid wholly in (0, 1].",
        [
            (
                "        for successor, continuation in zip(grid, values, strict=True):\n",
                "        for successor, continuation in zip(grid[:-1], values[:-1], strict=True):\n",
            ),
        ],
    ),
    "d1_02_continuation_reads_the_current_state.py": (
        "Student-error mutant (M5 slice d round 1): the continuation term is beta times V at the current state k, not at the saving k'.",
        [
            (
                "    for k in grid:\n        available = k**alpha\n        best = -math.inf\n        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)\n",
                "    for index, k in enumerate(grid):\n        available = k**alpha\n        best = -math.inf\n        for successor in grid:\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * values[index])\n",
            ),
        ],
    ),
    "d1_03_value_is_the_penultimate_iterate.py": (
        "Student-error mutant (M5 slice d round 1): solve returns the vector before the last sweep while certified_error refers to the last sweep.",
        [
            (
                "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        values = new\n",
                "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        previous = values\n        values = new\n",
            ),
            (
                '        "value": values,\n',
                '        "value": previous if iterations > 0 else values,\n',
            ),
        ],
    ),
}


def main() -> None:
    with open(REF, encoding="utf-8") as handle:
        reference = handle.read()
    for name, (headline, replacements) in MUTANTS.items():
        text = reference
        for old, new in replacements:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: expected exactly one match, found {count}")
            text = text.replace(old, new)
        # the first docstring line describes the error
        marker = text.index('"""', 0)
        end_first_line = text.index("\n", marker)
        first_line_rest = text[marker + 3 : end_first_line]
        text = text[: marker + 3] + headline + "\n\n" + first_line_rest.strip() + text[end_first_line:]
        path = os.path.join(OUT, name)
        if os.path.exists(path):
            raise SystemExit(f"refusing to overwrite {path}")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        print("wrote", path)


if __name__ == "__main__":
    main()
