#!/usr/bin/env python3
"""Validate and merge a unit's verification-ledger fragments (VERIFIER_RULES §3).

Independent verifiers may split a unit between them; each writes a fragment
``ledgers/<UNIT>/<part>.json`` in the ledger format. This tool validates every
fragment, refuses duplicate row ids, and writes ``ledgers/<UNIT>.verification.json``
with the verdict computed, never asserted: PASS only if every row is PASS
(an UNVERIFIABLE row counts as a failure). It never edits a row.

Usage::

    python3 tools/ledger.py --unit S7            # merge and print the summary
    python3 tools/ledger.py --unit S7 --check    # non-zero unless the merged ledger exists, is current and PASSES
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from coursekit import LEDGERS, unit

STATUSES = frozenset({"PASS", "FAIL", "UNVERIFIABLE"})
ROW_FIELDS = ("id", "check", "location", "status", "evidence")


def validate(fragment: dict[str, Any], name: str) -> list[str]:
    problems: list[str] = []
    rows = fragment.get("rows")
    if not isinstance(rows, list) or not rows:
        return [f"{name}: needs a non-empty rows list"]
    for row in rows:
        missing = [f for f in ROW_FIELDS if not str(row.get(f, "")).strip()]
        if missing:
            problems.append(f"{name}: row {row.get('id', '?')} missing {missing}")
        if row.get("status") not in STATUSES:
            problems.append(f"{name}: row {row.get('id')} has status {row.get('status')!r}")
        if row.get("status") != "PASS" and not str(row.get("fix", "")).strip():
            problems.append(f"{name}: row {row.get('id')} is not PASS but gives no fix")
        if str(row.get("evidence", "")).strip().lower() in {"looks correct", "ok", "fine", "verified"}:
            problems.append(f"{name}: row {row.get('id')} evidence must name the source, command or test used")
    for mutant in fragment.get("mutants", []):
        if not mutant.get("description"):
            problems.append(f"{name}: a mutant has no description")
    return problems


def merge(unit_id: str) -> tuple[dict[str, Any], list[str]]:
    folder = LEDGERS / unit_id
    fragments = sorted(p for p in folder.glob("*.json")) if folder.exists() else []
    problems: list[str] = []
    rows: list[dict[str, Any]] = []
    mutants: list[dict[str, Any]] = []
    registry_flags: list[str] = []
    freshness_flags: list[str] = []
    sources: list[str] = []
    for path in fragments:
        fragment = json.loads(path.read_text(encoding="utf-8"))
        problems += validate(fragment, path.name)
        rows += fragment.get("rows", [])
        mutants += fragment.get("mutants", [])
        registry_flags += fragment.get("registry_flags", [])
        freshness_flags += fragment.get("freshness_flags", [])
        sources.append(path.name)
    if not fragments:
        problems.append(f"no ledger fragments in ledgers/{unit_id}/")
    duplicates = [i for i, n in Counter(r.get("id") for r in rows).items() if n > 1]
    problems += [f"duplicate row id {i!r} across fragments" for i in duplicates]
    counts = Counter(r.get("status") for r in rows)
    killed = sum(1 for m in mutants if m.get("killed_by"))
    verdict = "PASS" if rows and counts["PASS"] == len(rows) and killed == len(mutants) and not problems else "FAIL"
    ledger = {
        "unit": unit_id,
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": verdict,
        "fragments": sources,
        "summary": {
            "rows": len(rows),
            "pass": counts["PASS"],
            "fail": counts["FAIL"],
            "unverifiable": counts["UNVERIFIABLE"],
            "mutants_killed": killed,
            "mutants": len(mutants),
        },
        "rows": rows,
        "mutants": mutants,
        "registry_flags": sorted(set(registry_flags)),
        "freshness_flags": sorted(set(freshness_flags)),
    }
    return ledger, problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    u = unit(args.unit)
    ledger, problems = merge(u.id)
    out = LEDGERS / f"{u.id}.verification.json"
    if args.check:
        if not out.exists():
            print(f"FAIL {u.id}: no ledger at {out.relative_to(LEDGERS.parent)}")
            return 1
        stored = json.loads(out.read_text(encoding="utf-8"))
        same = {k: v for k, v in stored.items() if k != "verified_at"} == {
            k: v for k, v in ledger.items() if k != "verified_at"
        }
        ok = same and stored["verdict"] == "PASS"
        print(f"ledger {u.id}: {'PASS' if ok else 'FAIL'}{'' if same else ' (stale: re-run tools/ledger.py)'}")
        return 0 if ok else 1
    for problem in problems:
        print(f"FAIL {u.id}: {problem}")
    Path(out).write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    s = ledger["summary"]
    print(
        f"ledger {u.id}: {ledger['verdict']} · rows {s['rows']} (pass {s['pass']}, fail {s['fail']}, "
        f"unverifiable {s['unverifiable']}) · mutants {s['mutants_killed']}/{s['mutants']}"
    )
    return 0 if ledger["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
