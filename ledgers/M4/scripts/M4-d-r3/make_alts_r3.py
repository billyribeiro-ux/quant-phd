"""Round-3 verifier D (M4 slice d): three alternative correct implementations of the M4 reference, each a valid reading of
project.html (Conventions items 2 to 5 leave the order of the Student-t draws, the rounding call, and the index formula
open, and the Standard-library rule allows any algorithm). Each is written from the checkout's reference.py by replacement;
every replacement must match exactly once. Usage: python -I make_alts_r3.py <checkout_root>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/M/M4/grader/reference.py").read_text()
out = root / "ledgers/M4/scripts/M4-d-r3"
HEADER = '"""Alternative correct implementation (round-3 verifier D). {}\n\nStandard library only. All inputs are SIMULATED.\n"""\n'


def build(name, desc, reps):
    src = ref
    for old, new in reps:
        assert src.count(old) == 1, (name, old[:70], src.count(old))
        src = src.replace(old, new)
    body = src.split('"""', 2)[2].lstrip("\n")
    (out / name).write_text(HEADER.format(desc) + body)
    print("wrote", out / name)


build(
    "alt_r3_a.py",
    "Student-t chi-square drawn before the normals of each draw; quantile by heapq.nsmallest; losses rounded half up.",
    [
        ("import math\nimport random\n", "import heapq\nimport math\nimport random\n"),
        ("        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n        scale = 1.0\n        if student and nu is not None:\n"
         "            chi_square = rng.gammavariate(nu / 2, 2.0)\n            scale = math.sqrt(matched * nu / chi_square)\n",
         "        scale = 1.0\n        if student and nu is not None:\n"
         "            chi_square = rng.gammavariate(nu / 2, 2.0)\n            scale = math.sqrt(matched * nu / chi_square)\n"
         "        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n"),
        ("        losses.append(round(-total))", "        losses.append(math.floor(-total + 0.5))"),
        ("    index = (99 * len(losses_cents) + 99) // 100\n    return sorted(losses_cents)[index - 1]",
         "    index = -((-99 * len(losses_cents)) // 100)\n    return heapq.nsmallest(index, losses_cents)[-1]"),
    ],
)
build(
    "alt_r3_b.py",
    "Validation by isinstance; positive-definite test with a pivot floor of 1e-300 instead of zero.",
    [
        ("    return type(value) is int", "    return isinstance(value, int) and not isinstance(value, bool)"),
        ("                if not pivot > 0.0:", "                if not pivot > 1e-300:"),
    ],
)
build(
    "alt_r3_c.py",
    "Student-t normals read from a second seeded stream, random.Random(seed + 1); the Gaussian stream is unchanged.",
    [
        ("    rng = random.Random(seed)\n    losses: list[int] = []",
         "    rng = random.Random(seed)\n    rng_t = random.Random(seed + 1)\n    losses: list[int] = []"),
        ("        z = [rng.gauss(0.0, 1.0) for _ in range(n)]",
         "        z = [(rng_t if student else rng).gauss(0.0, 1.0) for _ in range(n)]"),
    ],
)
