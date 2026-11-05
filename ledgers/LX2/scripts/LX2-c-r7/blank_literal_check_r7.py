"""Rung 2 disclosure check: blanks filled with the printed values as typed literals, and with a round-half-even rule
(the two classes the page now discloses), run under python -I -W error and compared with the completed twin."""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
src = (root / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
assert "hit_rate = Fraction(hits, horizon)" in src and "bias = Fraction(sum(errors), horizon)" in src
typed = src.replace("hit_rate = Fraction(hits, horizon)", "hit_rate = 0.6667").replace(
    "bias = Fraction(sum(errors), horizon)", "bias = 0.1667")
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "typed_literal.py").write_text(typed, encoding="utf-8")


def run(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True,
                          cwd=str(scratch), timeout=60)


completed = run(root / "tests/labs/LX2/lab-LX2-project-2.py")
literal = run(scratch / "typed_literal.py")
print("completed exit", completed.returncode, "| typed-literal exit", literal.returncode)
print("typed-literal stdout identical to completed stdout:", literal.stdout == completed.stdout)
print("typed-literal stderr bytes:", len(literal.stderr))
