"""Witnesses for two claims on project.html (line 268) that the CF8 suite does not enforce (CF8-c r1).

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r1/witness_unenforced.py
Builds a copy of the reference engine whose forecast() prints on every call and which imports instance.py, then runs the
suite on seeds 0-2 with run_solution_suite.py. Both pass, so the suite does not enforce "never prints" or "does not import
instance.py". Exit status 0 means the witness passed the suite (the claim is unenforced).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "CF" / "CF8" / "grader" / "reference.py"
RUNNER = ROOT / "ledgers" / "CF8" / "scripts" / "CF8-c-r1" / "run_solution_suite.py"


def main() -> int:
    source = REF.read_text(encoding="utf-8")
    old = '    """Thirteen weekly rows of the capped revolver forecast, in cents."""\n    _check_case(case)'
    new = '    """Thirteen weekly rows of the capped revolver forecast, in cents."""\n    print("forecast called")\n    _check_case(case)'
    assert source.count(old) == 1
    witness = source.replace(old, new).replace("import math\n", "import math\nimport instance  # noqa: F401\n", 1)
    with tempfile.TemporaryDirectory(prefix="cf8-witness-") as tmp:
        path = Path(tmp) / "witness_engine.py"
        path.write_text(witness, encoding="utf-8")
        result = subprocess.run([sys.executable, str(RUNNER), str(path), "0-2"], capture_output=True, text=True, check=False)
        print(result.stdout.strip())
        return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
