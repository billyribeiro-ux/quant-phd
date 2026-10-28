"""Write one self-contained constrained_allocator.py per alternative route into a scratch directory.

Usage: .venv/bin/python ledgers/M7/scripts/M7-d-r1/make_workspaces.py <out-dir>
Each file is alt_core.py plus an allocate() alias, so it imports the standard library only.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    out = Path(sys.argv[1])
    reference = (HERE.parents[3] / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
    header = reference[: reference.index("def _dot(")]
    core = header + "\n" + (HERE / "alt_core.py").read_text(encoding="utf-8")
    for k in range(1, 6):
        target = out / f"alt{k}" / "constrained_allocator.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(core + f"\n\ndef allocate(instance: dict[str, Any]) -> dict[str, Any]:\n    return allocate_alt{k}(instance)\n", encoding="utf-8")
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
