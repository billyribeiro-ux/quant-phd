"""Builds ledgers/E3/E3-e.json for the closing delta round 1 (pin 85b109f8, base d9de2fe5).

Re-verified rows carry new evidence; every other base PASS row is carried with the carry prefix.
"""
import json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
BASE = pathlib.Path("/Users/billyribeiro/.fanout/frags/H-E3-e.round1.json")
base = json.loads(BASE.read_text(encoding="utf-8"))
O = "ledgers/E3/scripts/E3-e-r1/out/"
PIN = "85b109f8"
PREV = "d9de2fe5"

RE = {
 "E3e-r14-gate-check-pages": f"Re-run at {PIN}: `.venv/bin/python tools/check_pages.py --unit E3` printed 'check_pages E3: PASS', exit 0 ({O}check_pages.out). The gate does not test footer wording; footers are checked in the footer rows.",
 "E3e-r14-gate-check-dag": f"Re-run at {PIN}: `tools/check_dag.py --unit E3` printed 'check_dag E3: PASS', exit 0 ({O}check_dag.out).",
 "E3e-r14-gate-check-projects": f"Re-run at {PIN}: `tools/check_projects.py --unit E3` printed 'check_projects E3: PASS', exit 0 ({O}check_projects.out). The project slice itself is not judged here.",
 "E3e-r14-gate-run-labs-L05-L08": f"Re-run at {PIN}: `tools/run_labs.py --unit E3` printed 'run_labs E3: PASS (11/11)', exit 0 ({O}run_labs.out). This covers the changed L02 twin and the L01, L03, L05, L06, L08 labs.",
 "E3e-r14-gate-page-smoke": f"Re-run at {PIN}: `tools/page_smoke.py --unit E3 --skip-sweep` printed 'page_smoke E3: PASS', exit 0 ({O}page_smoke.out). The figure sweep is skipped: E3 has no live figure.",
 "E3e-r14-twins-L05-L08-run": f"Re-run at {PIN}: `.venv/bin/python -I -W error tests/labs/E3/lab-E3-L02-1.py` exit 0, stderr 0 bytes; stdout equals the L02.html expected block ('expected block == twin output: True', {O}check_l02_claim.out). The other E3 twins are run by run_labs (11/11, row E3e-r14-gate-run-labs-L05-L08).",
 "E3e-r14-twins-L05-L08-lint": f"Re-run at {PIN} on the one changed twin: `ruff check tests/labs/E3/lab-E3-L02-1.py` 'All checks passed!', `ruff format --check` '1 file already formatted', `mypy --no-incremental` 'Success: no issues found in 1 source file' ({O}ruff_check.out, ruff_format.out, mypy.out). The L01, L03, L05, L06, L08 twins are byte-identical since d9de2fe5 (git diff empty), so their lint is carried.",
 "E3e-r14-verify-refs-offline": f"Re-run at {PIN}: `.venv/bin/python tools/verify_refs.py --offline` printed 'offline integrity: 560 entries, 0 problems', exit 0 ({O}verify_refs_offline.out). references/ and tools/ are unchanged since d9de2fe5.",
 "E3e-r14-pytest-relevant": f"Re-run at {PIN}: `.venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E3 -q` exit 0, 15 dots ({O}pytest_E3.out). `tools/build_site.py --check` printed 'site data current: 6 outputs', exit 0 ({O}build_site_check.out).",
 "E3e-r14-lesson-structure": f"Re-run at {PIN}: check_pages E3 PASS and check_dag E3 PASS (above) cover tags, h1, data-hours and dfn ids. The delta d9de2fe5..{PIN} over the slice paths is two files, L02.html:222-224 (text only) and the L02 twin lines 13-15 (text only); no dfn id, h1, data-hours or data-concept line is in the diff ('git diff -U0' read).",
 "E3e-r14-banned-strings": f"Re-run at {PIN}: check_pages E3 PASS (enforces the BANNED phrase list, tools/check_pages.py:58-125). The three added prose lines of L02.html:222-224 were read: no banned phrase.",
 "E3e-r14-process-words": f"Re-run at {PIN}: the 6 added lines of the delta (L02.html:222-224 and the twin lines 13-15, `git diff -U0 d9de2fe5..{PIN}`) were searched for verifier, fixer, ruling, round, pin, delta, ledger, builder, slice, audit, architect, rubric, checker, previous, todo, placeholder, batch, reviewer, agent: the only hit is 'round' inside 'rounded' (ordinary word). No process word.",
 "E3e-r14-filler-and-rhetoric": f"Re-run at {PIN}: the 6 added lines were read. They add no rhetoric word and no scope word (only, all, every, always, exactly). The universal claim 'Other values are unrounded and printed with six decimal places' is judged in row E3e-r14-L02-lab-claims.",
 "E3e-r14-concept-dfn-and-links": f"check_dag E3 PASS at {PIN} ({O}check_dag.out). `git diff d9de2fe5..{PIN}` adds no dfn, data-concept or a.concept line.",
 "E3e-r14-DAG-unlinked-names": f"check_dag E3 PASS at {PIN} ({O}check_dag.out). The added lines use ordinary words (units, scales, checks, printed); none is a concept name or a concept link.",
 "E3e-r14-forward-pointers-allowed": f"Re-run at {PIN}: the added lines of L02.html:222-224 and the twin contain no pointer to another lesson, unit or Problem; the one forward pointer of the earlier delta (L08.html:165) is unchanged.",
 "E3e-r14-grades": f"Re-run at {PIN}: `git diff d9de2fe5..{PIN}` over the slice shows no data-grade attribute on any changed line (the changed lines are L02 prose and the twin docstring). The grades of the L03, L05 changed rows judged in the earlier round are unchanged.",
 "E3e-r14-scope-words": f"Re-run at {PIN}: the added L02 lines contain none of only, all, every, always, exactly. The universal 'Other values are ...' sentence is a lab statement judged under E3e-r14-L02-lab-claims (FAIL), not under this row.",
 "E3e-r14-lesson-hours": f"Re-run at {PIN}: `git diff d9de2fe5..{PIN}` shows no data-hours change on any slice file ({O}check_pages.out PASS covers the structure).",
 "E3e-r14-notation-registry": f"Re-run at {PIN}: `.venv/bin/python -I ledgers/E3/scripts/E3-e-r1/symbol_sweep.py <checkout>` output ({O}symbol_sweep_85b109f8.out) has the same 480 hits as the base sweep ({O}symbol_sweep.out) when the L02 line numbers are ignored (only L02 line numbers after 223 moved down by one). The new L02 prose has no math segment and adds no symbol.",
 "E3e-r14-L02-numbers": f"Re-verified at {PIN}. The changed L02 lines (L02.html:222-224; twin 13-15) contain no number change: the numeric tokens of the removed and added lines are identical (100 twice on each side, the cents factor 'by 100'; `git diff -U0 d9de2fe5..{PIN}`). The expected block equals the twin output ({O}check_l02_claim.out, 'expected block == twin output: True'). The Part A-C values were recomputed in round 1: sqrt utility CE = (1/4 sqrt 40 + 1/2 sqrt 100 + 1/4 sqrt 160)^2 = 94.934165, premium 5.065835, and 0.5 r_A(100) Var(X) = 0.5 * 0.005 * 1800 = 4.5; output line 'exact_premium_cu 5.065835 pratt_premium_cu 4.500000' matches.",
 "E3e-r14-L02-lab-claims": "FAIL",
 "E3e-r14-hub-data-and-labs-claims": f"Re-verified at {PIN}: the labs of Lessons 1 to 3 draw no random numbers. The L02 twin imports only itertools, math, collections.abc, dataclasses, decimal and fractions (grep 'random' in tests/labs/E3/lab-E3-L02-1.py: no match, {O}check_l02_claim.out); L01 twin line 15 'No random draws are used' and L03 twin line 4 'No random numbers are drawn' are byte-identical since d9de2fe5.",
 "E3e-r18-lab-exact": f"Re-run at {PIN}: run_labs E3 PASS (11/11, {O}run_labs.out): each expected block equals its twin's output under the page rule. The L02 expected block equals its output ({O}check_l02_claim.out).",
 "E3e-r18-numeric-delta": f"Re-run at {PIN}: the numeric tokens of the removed and added lines of `git diff -U0 d9de2fe5..{PIN}` over the slice are identical (100 twice each side). No number added or removed; the cards.json and index.html are unchanged.",
 "E3e-r18-symbol-sweep": f"Re-run at {PIN}: symbol sweep hits identical to the base sweep except L02 line numbers after 223 moved down by one ({O}symbol_sweep_85b109f8.out vs {O}symbol_sweep.out). No math segment in the changed lines.",
 "E3e-r18-katex-render": f"Re-run at {PIN}: `tools/page_smoke.py --unit E3 --skip-sweep` PASS ({O}page_smoke.out). The changed lines have no math segment.",
 "E3d9-delta-coverage": f"Re-verified at {PIN}: `git diff --stat d9de2fe5..{PIN} -- course/modules/E/E3 tests/labs/E3 cards.json plans/E3-open-items.md plans/FINAL-ARCHITECT-RULINGS.md plans/E3-build-plan.md references tools notation`: 2 files, 6 insertions, 4 deletions: course/modules/E/E3/L02.html (lines 222-224) and tests/labs/E3/lab-E3-L02-1.py (lines 13-15). Both are read in full (the diff) and mapped to rows E3e-r14-L02-lab-claims (FAIL), E3e-r14-L02-numbers, E3e-r18-numeric-delta, E3e-r14-scope-words and the gates. All other slice paths, cards.json, plans and references are unchanged since d9de2fe5. The earlier delta 2a805c83..d9de2fe5 remains covered by the base rows.",
 "E3e-r19-ruling37-no-mutants": f"Re-verified at {PIN}: `git diff d9de2fe5..{PIN} -- plans/FINAL-ARCHITECT-RULINGS.md` is empty, so rulings 26, 30, 37 read as in round 1 (plans/FINAL-ARCHITECT-RULINGS.md:74-80, :97-101, :133-136). No mutant is authored in this closing round; the mutants list is empty (slice e has no grader; the standing project mutant set belongs to the project slice).",
}

def strip_carry(ev: str) -> str:
    while ev.startswith("Carried from round"):
        if ": " not in ev:
            break
        ev = ev.split(": ", 1)[1]
    return ev

rows = []
for r in base["rows"]:
    rid = r["id"]
    row = {"id": rid, "check": r["check"], "location": r["location"]}
    if rid in RE:
        if RE[rid] == "FAIL":
            row["status"] = "FAIL"
            row["evidence"] = (
                f"Sentence at tests/labs/E3/lab-E3-L02-1.py:13-15 and course/modules/E/E3/L02.html:222-224 (identical text; "
                f"the page code block is the twin). Run at {PIN}: `.venv/bin/python -I -W error tests/labs/E3/lab-E3-L02-1.py` "
                f"exit 0, stderr 0 bytes ({O}check_l02_claim.out). Defect 1: the line `gamble mean_cu 0.000000 variance_cu2 1800.000000 "
                f"wealth_cu 100` prints wealth_cu 100 as an integer; it is a CU value that is neither cents, nor a scale, nor a "
                f"True/False check, so 'Other values are unrounded and printed with six decimal places' is false for it (the "
                f"check script lists the non-six-decimal tokens). Defect 2: the parenthetical '(CU, CU squared or per CU)' omits "
                f"dimensionless, yet the lab names r_R dimensionless (twin relative() docstring line 259 'which is dimensionless'; "
                f"L02.html:144), and the output prints r_R 0.500000 and r_R 0.000000 under that name. Expected block equals output "
                f"(True); the defect is in the prose, not the output."
            )
            row["fix"] = (
                "In the twin lines 13-15 and the identical L02.html:222-224 text, either print the wealth with six decimals "
                "(change twin line 330 'wealth_cu {WEALTH}' to 'wealth_cu {WEALTH:.6f}' and refresh the expected block with "
                "`.venv/bin/python tools/embed_labs.py course/modules/E/E3/L02.html --refresh lab-E3-L02-1`) or name the wealth "
                "as an exception in the sentence; and add 'or dimensionless for r_R' to the unit list. Then re-run "
                "`tools/run_labs.py --unit E3`, `tools/check_pages.py --unit E3`, `tools/page_smoke.py --unit E3 --skip-sweep`, "
                "and ruff check, ruff format --check and mypy on the twin."
            )
        else:
            row["status"] = "PASS"
            row["evidence"] = RE[rid]
            row["check"] = r["check"].replace(PREV, PIN)
    elif r["status"] == "PASS":
        row["status"] = "PASS"
        files = r["location"]
        note = ""
        if "L02.html" in (r["location"] + r["evidence"]):
            note = " (L02.html lines after 223 moved down by one in this delta; the cited content is unchanged)"
        row["evidence"] = (f"Carried from round 1 ({files} byte-identical since the previous pin {PREV}{note}): "
                           + strip_carry(r["evidence"]).replace("(git diff empty)", "(the L02 diff hunk is at lines 222-224 only)") if note else f"Carried from round 1 ({files} byte-identical since the previous pin {PREV}): " + strip_carry(r["evidence"]))
    else:
        raise SystemExit(f"unexpected non-PASS base row without a re-verification: {rid}")
    rows.append(row)

ids_base = [r["id"] for r in base["rows"]]
assert [r["id"] for r in rows] == ids_base, "row ids must be kept in order"
missing = [k for k in RE if k not in ids_base]
assert not missing, missing

fail = sum(1 for r in rows if r["status"] == "FAIL")
passed = sum(1 for r in rows if r["status"] == "PASS")
verdict = "PASS" if fail == 0 and passed == len(rows) else "FAIL"

out = {
 "unit": "E3",
 "slice": "e",
 "round": 1,
 "verifier": f"Haiku independent verifier, E3-e closing delta round 1 at {PIN} (did not build E3)",
 "pin": PIN,
 "base": f"{PREV} (base fragment ~/.fanout/frags/H-E3-e.round1.json, FAIL with 1 non-PASS row E3e-r14-L02-lab-claims)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyI1-E3-e",
 "scratch": "/tmp/e3e_r1/",
 "verified_at": "2026-11-09",
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  f"Delta: `git diff d9de2fe5..{PIN}` over course/modules/E/E3, tests/labs/E3, cards.json, plans/E3-open-items.md, plans/FINAL-ARCHITECT-RULINGS.md, plans/E3-build-plan.md, references, tools, notation: 2 files, 6 insertions, 4 deletions (L02.html:222-224, lab-E3-L02-1.py:13-15). The fix commit 85b109f8 applied the sentence the base row proposed; the verifier re-checked it against the output.",
  "Rulings applied: 30 (closing delta: the one non-PASS row and every row whose subject changed were re-verified from scratch; the rest carried with the carry prefix; row ids kept); 37 (no mutants authored; the list is empty; slice e has no grader, so mutate_graders was not run); 26 (FAIL only for a lab statement the code does not support: row E3e-r14-L02-lab-claims, two defects in the new sentence).",
  "Carried rows that cite L02.html lines after 223 carry the line-shift note: those lines moved down by one because the changed sentence now spans three lines. Their cited content is byte-identical (symbol sweep multiset compare).",
  "Live Crossref was not re-run (references/ unchanged since d9de2fe5; registry row carried, as in the base). Full pytest suite not run (relevant subset of 15 tests and build_site --check run). The T-grade proofs not touched by the delta were carried, not re-read.",
  "Scripts: ledgers/E3/scripts/E3-e-r1/closing_delta_r1_85b109f8.py builds this fragment; check_l02_claim.py checks the expected block and the six-decimal claim; outputs in ledgers/E3/scripts/E3-e-r1/out/ (*_85b109f8.out and the check_*.out, run_labs.out, page_smoke.out files written this round).",
 ],
 "summary": {
  "rows": len(rows),
  "pass": passed,
  "fail": fail,
  "unverifiable": 0,
  "mutants": 0,
  "mutants_killed": 0,
 },
}
(ROOT / "ledgers/E3/E3-e.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", passed, "fail", fail, "verdict", verdict)
