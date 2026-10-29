"""Check the L05 lab claim 'The first 100 observations are a prefix of the 20000-observation run'.

Run: python -I ledgers/M4/scripts/M4-b-r4/l05_prefix_check.py
Executes the lab twin's definitions without its top-level main() call.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
src = (ROOT / "tests/labs/M4/lab-M4-L05-1.py").read_text(encoding="utf-8").replace("\nmain()", "\n")
ns: dict[str, object] = {}
exec(compile(src, "lab-M4-L05-1.py", "exec"), ns)
draws = ns["draws"]
SEED = ns["SEED"]
a = draws(100, SEED)  # type: ignore[operator]
b = draws(20000, SEED)[:100]  # type: ignore[index]
print("prefix equal:", a == b, "n", len(a), len(b))
sys.exit(0 if a == b else 1)
