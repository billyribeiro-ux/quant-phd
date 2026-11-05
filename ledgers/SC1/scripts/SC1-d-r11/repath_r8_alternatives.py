#!/usr/bin/env python3
"""Copy the round-8 alternatives that import the reference by an absolute path into the round-11 folder.

The round-8 copies point at the verifyE8 worktree, which does not exist in this round. The copies here point at this
round's checkout. The grader copies a solution to a temporary directory before running it, so __file__ cannot
locate the checkout; the reference path is therefore written out.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "ledgers/SC1/scripts/SC1-d-r8/alternatives"
DST = ROOT / "ledgers/SC1/scripts/SC1-d-r11/alternatives"
OLD = "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d/course/modules/SC/SC1/grader/reference.py"
NEW = str(ROOT / "course/modules/SC/SC1/grader/reference.py")


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for name in ("alt_r8_b_quadrature_tail.py", "alt_r8_c_dp_srw.py"):
        text = (SRC / name).read_text(encoding="utf-8")
        assert text.count(OLD) == 1, name
        text = text.replace(OLD, NEW)
        (DST / name).write_text(text, encoding="utf-8")
        print("repathed", name, "->", NEW)


if __name__ == "__main__":
    main()
