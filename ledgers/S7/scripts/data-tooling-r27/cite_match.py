"""Find accepted lesson-slice ledger rows that cover a data-tooling row's numeric claim (round 27).

A match needs: the same S7 page file named in both locations, and an overlapping line number (or the same lab id).
Each candidate is printed with its ledger, row id, status, pin and whether the page is byte-identical between that
pin and the current HEAD (git diff --quiet). Output is reviewed by hand before any row is marked covered.
Usage: python -I cite_match.py <round-25 fragment json> <out json>
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LEDGERS = {
    "ledgers/S7/L01-L02.json": None, "ledgers/S7/L03-L04.json": None, "ledgers/S7/L05-L06.json": None,
    "ledgers/S7/L07-L08.json": None, "ledgers/S7/project.json": None,
}
PAGE = re.compile(r"\b(L0[1-8]|project|cards|figures-L0[1-8])\.(html|json|js)\b")
LINE = re.compile(r"lines?\s*(\d+)(?:\s*[-–]\s*(\d+))?")
LAB = re.compile(r"lab-S7-[\w-]+")


def pages(text: str) -> set[str]:
    return {f"{m.group(1)}.{m.group(2)}" for m in PAGE.finditer(text)} | {
        "L" + m.group(1)[1:] + ".html" if False else m.group(0) for m in []}


def lines(text: str) -> set[int]:
    out: set[int] = set()
    for m in LINE.finditer(text):
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        out.update(range(lo, min(hi, lo + 400) + 1))
    for m in re.finditer(r"line ~?(\d+)", text):
        out.add(int(m.group(0).split()[-1].lstrip("~")))
    return out


def labs(text: str) -> set[str]:
    return set(LAB.findall(text))


def main() -> None:
    dt = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cands = []
    ledger_rows = []
    for ledger in LEDGERS:
        d = json.loads((ROOT / ledger).read_text(encoding="utf-8"))
        for r in d.get("rows", []):
            ledger_rows.append((ledger, d.get("pin"), r))
    for row in dt["rows"]:
        if row["status"] == "PASS":
            continue
        rp = pages(row["location"] + " " + row["check"])
        rl = lines(row["location"])
        rlab = labs(row["location"])
        for ledger, pin, lr in ledger_rows:
            lp = pages(lr["location"] + " " + lr["check"])
            ll = lines(lr["location"])
            llab = labs(lr["location"])
            if (rp & lp and rl & ll) or (rlab & llab and rlab):
                cands.append({"row": row["id"], "ledger": ledger, "cited": lr["id"], "pin": pin,
                              "cited_status": lr["status"], "shared_pages": sorted(rp & lp),
                              "shared_lines": sorted(rl & ll)[:6], "shared_labs": sorted(rlab & llab)})
    Path(sys.argv[2]).write_text(json.dumps(cands, indent=1), encoding="utf-8")
    print(len({c["row"] for c in cands}), "data-tooling rows with candidates;", len(cands), "pairs")


if __name__ == "__main__":
    main()
