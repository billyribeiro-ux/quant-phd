"""Verifier J1 (E3 slice e, closing delta round 1, pin f0beac46): builds ledgers/E3/E3-e.json.

Re-verified rows get new evidence written from this round's outputs (ledgers/E3/scripts/E3-e-r1/out/J1_*).
Every other base row (from ~/.fanout/frags/I-E3-e.round1.json) is carried with the carry prefix; its cited
subject is not touched by the 85b109f8..f0beac46 hunks (course/modules/E/E3/L02.html 223-224, 330, 366;
tests/labs/E3/lab-E3-L02-1.py 14-15, 121).
"""
import json, os, sys
sys.path.insert(0, "tools")
import ledger  # noqa: E402

BASE = os.path.expanduser("~/.fanout/frags/I-E3-e.round1.json")
base = json.load(open(BASE, encoding="utf-8"))
OUT = "/Users/billyribeiro/.fanout/wt/verifyJ1-E3-e/ledgers/E3/E3-e.json"
O = "ledgers/E3/scripts/E3-e-r1/out/"
HUNKS = ("course/modules/E/E3/L02.html 223-224, 330, 366; tests/labs/E3/lab-E3-L02-1.py 14-15, 121")

fresh = {
 "E3e-r14-gate-check-pages": ("Re-run at f0beac46: `.venv/bin/python tools/check_pages.py --unit E3` printed 'check_pages E3: PASS' (" + O + "J1_check_pages.out, exit 0)."),
 "E3e-r14-gate-check-dag": ("Re-run at f0beac46: `tools/check_dag.py --unit E3` printed 'check_dag E3: PASS', exit 0 (" + O + "J1_check_dag.out)."),
 "E3e-r14-gate-check-projects": ("Re-run at f0beac46: `tools/check_projects.py --unit E3` printed 'check_projects E3: PASS', exit 0 (" + O + "J1_check_projects.out). The project slice is not judged here."),
 "E3e-r14-gate-run-labs-L05-L08": ("Re-run at f0beac46: `tools/run_labs.py --unit E3` printed 'run_labs E3: PASS (11/11)', exit 0 (" + O + "J1_run_labs.out). Covers the changed L02 twin and page code and expected block."),
 "E3e-r14-gate-page-smoke": ("Re-run at f0beac46: `tools/page_smoke.py --unit E3 --skip-sweep` printed 'page_smoke E3: PASS', exit 0 (" + O + "J1_page_smoke.out). The figure sweep is skipped: E3 has no live figure."),
 "E3e-r14-twins-L05-L08-run": ("Re-run at f0beac46: `.venv/bin/python -I -W error tests/labs/E3/lab-E3-L02-1.py` exit 0, stderr 0 bytes (/tmp/e3e_r1_l02.err); stdout equals the L02.html expected block: `" + O + "J1_check_l02.py` prints 'expected == twin stdout: True' (" + O + "J1_check_l02.out). The other E3 twins (L01, L03, L05, L06, L08) are byte-identical since 85b109f8 (no hunk) and run by run_labs 11/11."),
 "E3e-r14-twins-L05-L08-lint": ("Re-run at f0beac46 on the one changed twin: `ruff check` 'All checks passed!' (" + O + "J1_ruff_check.out), `ruff format --check` '1 file already formatted' (" + O + "J1_ruff_format.out), `mypy --no-incremental` 'Success: no issues found in 1 source file' (" + O + "J1_mypy.out). The other changed-lab twins are untouched by the delta and carried."),
 "E3e-r14-verify-refs-offline": ("Re-run at f0beac46: `.venv/bin/python tools/verify_refs.py --offline` printed 'offline integrity: 560 entries, 0 problems', exit 0 (" + O + "J1_verify_refs_offline.out). references/ and tools/ are unchanged by the delta (git diff --stat 85b109f8..HEAD empty for them)."),
 "E3e-r14-pytest-relevant": ("Re-run at f0beac46: `.venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E3 -q` exit 0, 15 dots (" + O + "J1_pytest_E3.out). `tools/build_site.py --check` printed 'site data current: 6 outputs', exit 0 (" + O + "J1_build_site_check.out). The page_smoke and check_dag runs are the rows above."),
 "E3e-r14-hub-data-and-labs-claims": ("Re-verified at f0beac46: no random import or call in tests/labs/E3/lab-E3-L02-1.py (grep 'random' no match; the L02 twin changed only at lines 14-15 and 121); L01 twin line 15 'No random draws are used' and L03 twin line 4 'No random numbers are drawn' are outside every hunk. index.html is unchanged (git diff empty)."),
 "E3e-r14-lesson-hours": ("Re-verified at f0beac46: `git diff -U0 85b109f8..HEAD` over the slice has no data-hours line (the 5 hunks listed in E3d9-delta-coverage are prose, code and expected-block lines). check_pages E3 PASS."),
 "E3e-r14-lesson-structure": ("Re-verified at f0beac46: check_pages E3 PASS and check_dag E3 PASS (" + O + "J1_check_pages.out, " + O + "J1_check_dag.out) cover tags, h1, data-hours and dfn ids. The delta (`git diff -U0 85b109f8..HEAD`) changes prose and code text only at L02.html 223-224, 330, 366 and the twin 14-15, 121; no tag, h1, dfn id or data-concept line is in it."),
 "E3e-r14-banned-strings": ("Re-verified at f0beac46: check_pages E3 PASS (" + O + "J1_check_pages.out) enforces the BANNED phrase list (tools/check_pages.py:58-125). The changed prose lines L02.html 223-224 and the twin 14-15 were read in full (" + O + "J1_delta_text_check.out): no banned phrase."),
 "E3e-r14-process-words": ("Re-verified at f0beac46: the 7 added lines of the delta (" + O + "J1_delta_text_check.out) were searched for verifier, fixer, ruling, round, pin, delta, ledger, builder, slice, audit, architect, rubric, checker, previous, todo, placeholder, batch, reviewer, agent: zero hits."),
 "E3e-r14-filler-and-rhetoric": ("Re-verified at f0beac46: the added lines (" + O + "J1_delta_text_check.out) contain no scope word (only, all, every, always, exactly, any, same, drives, never, none) and no rhetoric word. The sentence 'Other values are unrounded and printed with six decimal places' is judged in row E3e-r14-L02-lab-claims."),
 "E3e-r14-concept-dfn-and-links": ("Re-verified at f0beac46: check_dag E3 PASS (" + O + "J1_check_dag.out). The hunks add no dfn, data-concept or a.concept line (`git diff -U0 85b109f8..HEAD`)."),
 "E3e-r14-DAG-unlinked-names": ("Re-verified at f0beac46: check_dag E3 PASS (" + O + "J1_check_dag.out). The added words units, scales, checks, printed and dimensionless are not concept names: grep for quoted 'units', 'scales', 'dimensionless', 'printed', 'checks' over course/assets/data and course/concepts.html gives 0 matches."),
 "E3e-r14-forward-pointers-allowed": ("Re-verified at f0beac46: the added lines (" + O + "J1_delta_text_check.out) name no other lesson, unit, Problem or section; the forward pointer at L08.html:165 is outside every hunk."),
 "E3e-r14-grades": ("Re-verified at f0beac46: `git diff -U0 85b109f8..HEAD` shows no data-grade or data-cite attribute on any changed line (the changed lines are L02 prose and code only)."),
 "E3e-r14-scope-words": ("Re-verified at f0beac46: the added lines (" + O + "J1_delta_text_check.out) contain none of only, all, every, always, exactly (scope regex run). The universal lab sentence is judged in E3e-r14-L02-lab-claims, not here."),
 "E3e-r14-notation-registry": ("Re-verified at f0beac46: `.venv/bin/python -I ledgers/E3/scripts/E3-e-r1/symbol_sweep.py <checkout>` output (" + O + "J1_symbol_sweep.out) is byte-identical to the 85b109f8 sweep (" + O + "symbol_sweep_85b109f8.out), 480 lines. The new L02 prose and the wealth format are not math segments and add no symbol."),
 "E3e-r14-L02-numbers": ("Re-verified at f0beac46. The numeric tokens of the delta (" + O + "J1_delta_text_check.out) are unchanged in value: the only change is the wealth printed as 100 becomes 100.000000 (same value, six decimals, as the lab sentence states). The expected block equals the twin stdout (" + O + "J1_check_l02.out). Values recomputed in python: E sqrt(W) = 9.743416490, CE = 94.934164903, premium 5.065835097 (printed exact_premium_cu 5.065835, ce_cents 9493, premium_cents 507); r_A(100) = 0.005, Pratt approximation 0.5 * 0.005 * 1800 = 4.500000; r_R = 0.500000."),
 "E3e-r14-L02-lab-claims": ("Re-verified at f0beac46, Defects 1 and 2 of the base are fixed. (a) Every printed value now matches the sentence at L02.html:223-224 and twin 14-15: the gamble line prints mean_cu, variance_cu2 and wealth_cu all with six decimals (`" + O + "J1_check_l02.out`, run of `python -I -W error tests/labs/E3/lab-E3-L02-1.py`: exit 0, stderr 0 bytes); Part A/B/C money values are whole cents (ce_cents, premium_cents, linear_premium_cents); CU, CU squared, per CU and dimensionless (r_R) values are six decimals; eps scales are printed as given (1.0, 0.5, 0.25, 0.1, 0.01; 1.0, 0.5, 0.1); True/False checks as given. (b) The units list now reads 'CU, CU squared, per CU or dimensionless for r_R', so r_R 0.500000 and r_R 0.000000 are named. (c) The sentence is byte-identical on page and twin (check_l02 'page sentence in page: True | in twin: True'). (d) Page code block contains the wealth line with :.6f and equals the twin body (True). Ruling 26 'lab statement the code does not support' is cleared."),
 "E3e-r18-lab-exact": ("Re-verified at f0beac46: run_labs E3 PASS 11/11 (" + O + "J1_run_labs.out): each expected block equals its twin's output and page code equals twin (L02 by " + O + "J1_check_l02.out)."),
 "E3e-r18-numeric-delta": ("Re-verified at f0beac46 (" + O + "J1_delta_text_check.out): numeric tokens removed: 100 (and the 1 and 6 of unchanged text); added: 100.000000 (same value, six decimals). No number is added or removed in value; the format change is the one the L02 sentence states. cards.json and index.html are unchanged."),
 "E3e-r18-symbol-sweep": ("Re-verified at f0beac46: symbol sweep identical to the 85b109f8 sweep (" + O + "J1_symbol_sweep.out vs " + O + "symbol_sweep_85b109f8.out, byte-identical). No math segment in the changed lines."),
 "E3e-r18-katex-render": ("Re-verified at f0beac46: `tools/page_smoke.py --unit E3 --skip-sweep` PASS (" + O + "J1_page_smoke.out). The changed lines L02.html 223-224 and 330 and 366 are prose or code, with no math segment."),
 "E3e-r19-ruling37-no-mutants": ("Re-verified at f0beac46: plans/FINAL-ARCHITECT-RULINGS.md is not in the 85b109f8..HEAD delta (git diff --stat over plans/ empty). Rulings 26, 30, 37, 38a and 39 re-read at plans/FINAL-ARCHITECT-RULINGS.md:74-80, :97-101, :133-136, :137-150. No mutant is authored in this closing round; mutants list is empty (slice e has no grader)."),
 "E3d9-delta-coverage": ("Re-verified at f0beac46: `git diff --stat 85b109f8..HEAD -- course/modules/E/E3 tests/labs/E3 cards.json plans references tools notation` = 2 files, 7 insertions, 7 deletions: course/modules/E/E3/L02.html (223-224, 330, 366) and tests/labs/E3/lab-E3-L02-1.py (14-15, 121). All read via `git diff -U0` and mapped to rows E3e-r14-L02-lab-claims (now PASS), E3e-r14-L02-numbers, E3e-r18-numeric-delta, E3e-r14-scope-words, E3e-r18-lab-exact, E3e-r14-banned-strings, E3e-r14-process-words, E3e-r14-filler-and-rhetoric and the gates. Other slice paths are unchanged."),
}

# Re-verified rows: the base row's status is PASS unless it is the one base FAIL row.
rows = []
carried = 0
for r in base["rows"]:
    rid = r["id"]
    if rid in fresh:
        new = dict(r)
        new["status"] = "PASS"
        new["check"] = r["check"].replace("[re-verified at d9de2fe5]", "[re-verified at f0beac46]").replace("[re-verified at 85b109f8]", "[re-verified at f0beac46]")
        new["evidence"] = fresh[rid]
        new.pop("fix", None)
        rows.append(new)
        continue
    ev = r["evidence"]
    assert ev.startswith("Carried from round 1 ("), rid
    depth, i = 1, len("Carried from round 1 (")
    while depth:
        depth += {"(": 1, ")": -1}.get(ev[i], 0)
        i += 1
    assert ev[i:i + 2] == ": ", (rid, ev[i:i + 4])
    remainder = ev[i + 2:]
    new = dict(r)
    new["evidence"] = ("Carried from round 1 (" + r["location"] + " cited subject byte-identical since the previous pin 85b109f8: "
                       "no hunk of 85b109f8..f0beac46 touches the cited lines; the hunks are " + HUNKS + "): " + remainder)
    assert new["status"] == "PASS", rid
    rows.append(new)
    carried += 1

notes = [
    "Closing delta round 1 at pin f0beac46 (base 85b109f8; base fragment ~/.fanout/frags/I-E3-e.round1.json, one FAIL row E3e-r14-L02-lab-claims).",
    "Delta `git diff 85b109f8..f0beac46` over the slice paths: 2 files, 7 insertions, 7 deletions: L02.html 223-224 (sentence), 330 and 366 (wealth print and its expected block); tests/labs/E3/lab-E3-L02-1.py 14-15 (sentence) and 121 (wealth print). No net line shift: the sentence now wraps to two lines, so later L02 lines keep their numbers at the base pin.",
    "The base FAIL row is fixed and re-verified from scratch: wealth_cu is printed with six decimals and the units list names dimensionless for r_R. Every printed value conforms to the sentence (evidence in E3e-r14-L02-lab-claims).",
    "Rulings applied: 30 (closing delta: the base FAIL row and every row whose subject changed were re-verified; the rest carried with the carry prefix; row ids kept); 37 (no mutants authored; slice e has no grader; mutants list empty); 26 (FAIL only for the lab-statement and wrong-number kinds, none remains); 38a and 39 checked as in the base (E3e-r19-notation-Lambda, E3e-r15-footers-registry-claim carried, plans unchanged).",
    "Not run: the full pytest suite (relevant subset: 15 tests, E3), live Crossref (references unchanged since 85b109f8; registry row carried), verify_refs live run, mutate_graders (no grader in slice e), the project slice. The T-grade proofs not touched by the delta were carried, not re-read.",
    "The file ledgers/E3/E3-e.json previously held an unrelated round-13 fragment in this checkout; it is overwritten here as the round-1 closing fragment (not committed).",
]

frag = {
    "unit": "E3", "slice": "e", "round": 1,
    "verifier": "Haiku independent verifier J1, E3-e closing delta round 1 at f0beac46 (did not build E3)",
    "pin": "f0beac46",
    "base": "85b109f8 (base fragment ~/.fanout/frags/I-E3-e.round1.json; its own base d9de2fe5; FAIL with 1 non-PASS row E3e-r14-L02-lab-claims)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyJ1-E3-e",
    "scratch": "/tmp/e3e_r1_l02.out, /tmp/e3e_r1_l02.err; ledgers/E3/scripts/E3-e-r1/out/J1_*",
    "verified_at": "2026-11-09",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
                "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0,
                "mutants": 0, "mutants_killed": 0, "carried": carried, "reverified": len(fresh)},
}
problems = ledger.validate(frag, "E3-e")
print("validate:", problems)
print("rows", len(rows), "carried", carried, "reverified", len(fresh), "verdict", frag["verdict"])
missing = set(fresh) - {r["id"] for r in base["rows"]}
print("fresh ids not in base:", missing)
if not problems and not missing:
    json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(OUT, "a", encoding="utf-8").write("\n")
    print("written", OUT)
