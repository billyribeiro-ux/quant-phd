"""Round-12 edge-case mutants of reflection_tail, each a single-change copy of the reference (asserts each edit once)."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
ref = (root / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/SC1/mutants"


def edit(name: str, doc: str, old: str, new: str) -> None:
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new).split('"""', 2)[2]
    (out / name).write_text(f'"""{doc}\n\nSingle-change copy of the reference (round 12, verifier-written)."""' + body, encoding="utf-8")


edit(
    "r12_05_tiny_level_guard_returns_one.py",
    "Tiny-level guard: reflection_tail returns 1.0 for any level below 1e-6, although erfc(a / sqrt(2 t)) differs from 1 there.",
    '    return math.erfc(a / math.sqrt(2.0 * t))',
    '    if a < 1e-6:\n        return 1.0\n    return math.erfc(a / math.sqrt(2.0 * t))',
)
edit(
    "r12_06_tiny_time_guard_returns_zero.py",
    "Tiny-time guard: reflection_tail returns 0.0 for any time below 1e-6, although the tail at a small level and a small time is not zero.",
    '    return math.erfc(a / math.sqrt(2.0 * t))',
    '    if t < 1e-6:\n        return 0.0\n    return math.erfc(a / math.sqrt(2.0 * t))',
)
print("written")
