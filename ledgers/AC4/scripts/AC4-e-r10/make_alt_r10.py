"""Round-10 alternative correct implementation (alt_l): the reference plus extra informational keys in the
master and flexed budgets, which the specification does not forbid, and a validation message change only.
Each replacement must match exactly once, or the script stops."""
from pathlib import Path

ROOT = Path("/tmp/verify10-AC4-e")
REF = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("/tmp/ac4-v/e10/alt_l.py")
edits = [
    ('        "profit_cents": total_revenue - total_variable - fixed,\n',
     '        "profit_cents": total_revenue - total_variable - fixed,\n        "note": "informational extra key",\n'),
    ('        "profit_cents": revenue - variable - fixed,\n',
     '        "profit_cents": revenue - variable - fixed,\n        "source": "flexed",\n'),
]
text = REF
for old, new in edits:
    assert text.count(old) == 1, old
    text = text.replace(old, new, 1)
OUT.write_text(text, encoding="utf-8")
print("wrote", OUT)
