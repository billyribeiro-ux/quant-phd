"""Build the round-10 fragment for AC1-c from the round-9 fragment plus this round's re-verification.

Usage: python -I build_fragment_r10.py <checkout> <round9_fragment.json>
Rows whose cited subject is byte-identical since 96dd532 are carried with the required prefix;
rows whose subject changed or that were non-PASS are re-verified and carry fresh evidence.
"""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

checkout = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
CARRY = ("Carried from round 9 (course/modules/AC/AC1/L07.html, L08.html and cards.json cited lines "
         "byte-identical since the previous pin 96dd532; round-10 changed lines are L07.html:140, :452, "
         "L08.html:216, :394, tests/labs/AC1/lab-AC1-L07-1.py:17, cards c028, c029, c032, c040, c124): ")

fresh = {
    "AC1-c-cmd-run_labs": ("PASS", "tools/run_labs.py --unit AC1 (run this round): PASS (11/11); both twins under "
                           "python -I -W error rc=0 (see AC1-c-lab-twin-run)"),
    "AC1-c-lab-twin-run": ("PASS", "python -I -W error tests/labs/AC1/lab-AC1-L07-1.py rc=0 (stdout year rows 1-6, "
                           "4/4, 6/6 x4); lab-AC1-L08-1.py rc=0 (5/5 x3, deferred balance 0.00 SCU); outputs in "
                           "/tmp/AC1-v/AC1-c/lab_L07.out and lab_L08.out"),
    "AC1-c-lab-embed-equals-twin": ("PASS", "ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py re-run on "
                                    "af08ad1: L07 embedded code == twin True (embedded line 140 carries the new "
                                    "HORIZON comment); L08 True"),
    "AC1-c-lab-expected-output": ("PASS", "embed_and_expected_check.py re-run: expected == run output True for L07 "
                                  "(18 lines) and L08 (13 lines)"),
    "AC1-c-lab-seed-sweep": ("PASS", "ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py re-run: lab-AC1-L07-1 seeds "
                             "0-199 passing 200, failing none; lab-AC1-L08-1 passing 200, failing none"),
    "AC1-c-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit AC1 --pages L07 L08 (this round): PASS for "
                             "modules/AC/AC1/L07.html and L08.html (local Python, not Pyodide)"),
    "AC1-c-cmd-check_pages_dag": ("PASS", "tools/check_pages.py --unit AC1: PASS; tools/check_dag.py --unit AC1: PASS "
                                  "(this round)"),
    "AC1-c-cmd-pytest_ruff_mypy": ("PASS", "ruff check . PASS; ruff format --check . 212 files already formatted; "
                                   "mypy --no-incremental Success: no issues found in 153 source files; pytest -q "
                                   "tests/test_labs.py -k AC1 and tests/test_page_checks.py: no failures; pytest -k "
                                   "'notation or macro or banned' and tests/test_docs_figures.py: no failures"),
    "AC1-c-cit-verify_refs": ("PASS", "tools/verify_refs.py --unit AC1 (live): 2 of 560 entries, 0 problems, rc=0; "
                              "tools/verify_refs.py --offline: 560 entries, 0 problems, rc=0 (this round)"),
    "AC1-c-notation": ("PASS", "pytest -k 'notation or macro or banned' passed; the changed sentence L08.html:216 uses "
                       "\\(L\\), which notation/notation.json lists only as a letter defined locally in each lesson "
                       "(its 'about' field); L07 changed line 140 is a code comment"),
    "AC1-c-banned-phrases": ("PASS", "grep over L07.html and L08.html for roughly, about <number>, historically, "
                             "typically, ellipsis, half of, most firms, process words: one hit, 'typically' at "
                             "L07.html:412 inside a quiz distractor ('awards are typically forfeited at a stated "
                             "rate'), not a claim; none in L08.html:216 or either footer"),
    "AC1-c-cards-dup-scan": ("PASS", "course/modules/AC/AC1/cards.json (this round): 126 cards, no duplicate ids, no "
                             "duplicate fronts"),
    "AC1-c-lesson-structure": ("PASS", "tools/check_pages.py --unit AC1: PASS (this round); L07.html and L08.html "
                               "section order and lab blocks unchanged; the changed lines are a code comment, one "
                               "sentence at L08.html:216 and the footers"),
    "AC1-c-figures-none": ("PASS", "grep -c '<img|<svg|<canvas|data-figure' L07.html = 0, L08.html = 0 (this round)"),
    "AC1-c-r7-L08-216-so-clause": ("PASS", "course/modules/AC/AC1/L08.html:216 re-verified on the round-10 text: "
                                   "'The model has one asset and one tax schedule, so it cannot show how many "
                                   "temporary differences a real firm holds at once. Its balance is zero at year L "
                                   "by Theorem 2.1 (c).' The 'so' now links the one asset (Definition 1.1, L08.html:58) "
                                   "to the limit, a valid reason; the zero balance is a separate sentence, Theorem 2.1 "
                                   "(c) at L08.html:91-93. The round-9 defect (zero balance as cause) is gone"),
    "AC1-c-r5-L08-line216-scope": ("PASS", "course/modules/AC/AC1/L08.html:216 re-read on the round-10 text; scope and "
                                   "basis as stated in AC1-c-r7-L08-216-so-clause"),
    "AC1-c-L08-quiz-q10": ("PASS", "L08.html:372 explain ('Section 3: the signed form of Definition 1.2 includes an "
                           "asset, but the model states no recognition test for it') still matches L08.html:215-217; "
                           "the changed sentence at :216 does not alter the quiz claim"),
    "AC1-c-r7-lab-student-mutants": ("PASS", "UNVERIFIABLE in round 9 (scripts absent); now re-run: "
                                     "ledgers/AC1/scripts/AC1-c-r7/seed_sweep_and_mutants.sh with CHK rewritten to "
                                     "this checkout by sed (the script hardcodes /tmp/verify7-AC1-c): m8a rc=1, m7a "
                                     "rc=1, m7b rc=1 (all AssertionError); 10-seed sweep rc=0 for both twins"),
    "AC1-c-r8-lab-student-mutants": ("PASS", "UNVERIFIABLE in round 9; now re-run: ledgers/AC1/scripts/AC1-c-r8/"
                                     "new_mutants.sh and mutants_and_sweep.sh with CHK rewritten (hardcoded "
                                     "/tmp/verify8-AC1-c): n2life rc=1, n3sign rc=1, n4te rc=1 (killed); n1ceil rc=0 "
                                     "and n1b rc=0 (out of scope, see AC1-c-r10-m10c-survivor); 20 sweep runs rc=0"),
    "AC1-c-r7-alt-implementations": ("PASS", "tests/labs/AC1/lab-AC1-L07-1.py and lab-AC1-L08-1.py re-run with the "
                                     "alternative implementations alt9a, alt9b, alt9c, alt10a, alt10b (see "
                                     "AC1-c-r10-alt-correct-implementations): all rc=0"),
    "AC1-c-r9-new-mutants": ("PASS", "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py re-run on this checkout: m9a-m9g each "
                             "exit=1 (AssertionError), as expected"),
    "AC1-c-r9-alt-implementations-seeds": ("PASS", "mutants_r9.py alt9a, alt9b, alt9c exit=0 as expected; "
                                           "seed_sweep_r9.py 200/200 for both twins"),
    "AC1-c-r9-embed-expected": ("PASS", "embed_and_expected_check.py re-run on af08ad1 (see AC1-c-lab-embed-equals-twin "
                                "and AC1-c-lab-expected-output)"),
}

ROUND9_EVIDENCE_SUFFIX_NOTE = ""

new_rows = [
    {"id": "AC1-c-r10-delta-read", "check": "round-10 delta read",
     "location": "git diff --stat 96dd532 af08ad1 -- course/modules/AC/AC1 tests/labs/AC1",
     "status": "PASS",
     "evidence": "Slice hunks: L07.html:140 (HORIZON code comment, in the embedded lab and the twin line 17), L07.html:452 "
                 "(footer), L08.html:216 (Section 3 sentence re-ordered, 'so' now attached to the one asset), L08.html:394 "
                 "(footer). Other AC1 hunks are outside the slice (index.html:31 eyebrow; cards.json c028, c029, c032, c040, "
                 "c124; L01-L03, project and grader files). Every hunk in the slice was read."},
    {"id": "AC1-c-r10-L07-horizon-comment", "check": "2.5-labs code comment (round-10 change)",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py:17; course/modules/AC/AC1/L07.html:143",
     "status": "PASS",
     "evidence": "Comment reads 'the latest vesting year any grant can have is 3 + 4 - 1 = 6'. The generator (lab lines 55, "
                 "58) draws grant_year in randint(1, 3) and vest_years in choice((3, 4)), so the latest year is at most "
                 "3 + 4 - 1 = 6, and reached (grant 3, 4 years). The embedded copy equals the twin (AC1-c-lab-embed-equals-twin)."},
    {"id": "AC1-c-r10-L07-footer", "check": "1-citations footer statement",
     "location": "course/modules/AC/AC1/L07.html:452; :441-442",
     "status": "PASS",
     "evidence": "Footer: 'Lab data are SIMULATED. This page cites no registry key.' The lab draws every grant and income "
                 "figure with a seed (lab lines 3-4, 15); L07.html:441 says 'This page cites no registry key' and "
                 "<ol data-references></ol> at :442 is empty; grep finds no other registry citation in L07.html."},
    {"id": "AC1-c-r10-L08-footer", "check": "1-citations footer statement",
     "location": "course/modules/AC/AC1/L08.html:394; :383-384",
     "status": "PASS",
     "evidence": "Footer: 'Lab data are SIMULATED. This page cites no registry key.' The lab's asset, income and rate are "
                 "SIMULATED (lab docstring lines 3-5, 'the rate is a model parameter'); L08.html:383 says 'This page cites "
                 "no registry key' and the references list at :384 is empty."},
    {"id": "AC1-c-r10-L08-216-rewrite", "check": "2.1-numbers and 2.4-math (round-10 rewritten sentence)",
     "location": "course/modules/AC/AC1/L08.html:216; Definition 1.1 at :58; Theorem 2.1 (c) at :91-93",
     "status": "PASS",
     "evidence": "Sentence: 'The model has one asset and one tax schedule, so it cannot show how many temporary differences a "
                 "real firm holds at once. Its balance is zero at year L by Theorem 2.1 (c).' Definition 1.1 (:58) gives one "
                 "asset with a single schedule, so the model holds one temporary-difference series; the inference is "
                 "supported. Theorem 2.1 (c) states DTL_L = 0 and its proof gives K_L = 0 (lab assert previous_dtl == 0 at "
                 "lab line 84; the printed balance 0.00 SCU). No cause is attributed to the zero balance."},
    {"id": "AC1-c-r10-mutants-killed", "check": "2.5-labs student-error mutants (new round-10 set m10*)",
     "location": "ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py",
     "status": "PASS",
     "evidence": "Five new student-error mutants written by this verifier: m10a expense starts one year late (survives, see "
                 "AC1-c-r10-m10a-survivor); m10b APIC change one cent short (killed, AssertionError); m10c base divides by "
                 "vest+1 (survives, see AC1-c-r10-m10c-survivor); m10d deferred expense equals the balance (killed); m10e "
                 "current tax adds the difference (killed). Three killed, two survive as out of scope."},
    {"id": "AC1-c-r10-m10a-survivor", "check": "2.5-labs survivor classification",
     "location": "ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py (m10a); tests/labs/AC1/lab-AC1-L07-1.py:42",
     "status": "PASS",
     "evidence": "m10a survives with exit 0 because on seed 20260701 every grant's shifted schedule still ends by year 6 "
                 "(grant years 2, 1, 1, 3 with 3-4 vesting years), so the sum check still passes. It is out of scope: the "
                 "hypothesis at L07.html:126 claims only the schedule sums and the four identities, and no statement in the "
                 "contract (atlas/A15.contract.md has no vesting rule) or plans/AC1-build-plan.md row L07 (line 72) fixes the "
                 "timing. The lesson states the timing in Definition 1.1 (L07.html:59-64); the lab does not claim to check it. "
                 "Recorded as an out-of-scope mutant, not a FAIL, under the architect's rule that only the project page, "
                 "grader docstrings, plan or contract can make a survivor a FAIL."},
    {"id": "AC1-c-r10-m10c-survivor", "check": "2.5-labs survivor classification",
     "location": "ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py (m10c); tests/labs/AC1/lab-AC1-L07-1.py:45; "
                 "course/modules/AC/AC1/L07.html:63 and :81",
     "status": "PASS",
     "evidence": "m10c (and the round-8 n1ceil and n1b, and alt10a) change the base amount. Each still sums exactly, because the "
                 "last year takes the remainder, so the sum check passes. The lesson states the floor base at L07.html:63 and "
                 ":81; the lab checks only the sums (L07.html:126), so this is out of scope for the lab. The same class is "
                 "recorded in AC1-c-r10-alt-correct-implementations as a valid alternative (ceiling base). Not a FAIL."},
    {"id": "AC1-c-r10-alt-correct-implementations", "check": "2.5-labs over-constraint (alternative correct implementations)",
     "location": "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py (alt9a-c); ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py "
                  "(alt10a, alt10b)",
     "status": "PASS",
     "evidence": "All five pass (exit 0): alt9a round-half-up base; alt9b remainder in the first year; alt9c deferred from "
                 "rate times difference; alt10a ceiling base with the remainder in the last year; alt10b deferred from rate "
                 "times difference. None of these over-constrains the lab; the lab's checks are the sums and identities the "
                 "hypothesis names."},
    {"id": "AC1-c-r10-hours-sum", "check": "hours arithmetic",
     "location": "course/modules/AC/AC1/index.html:29 (data-hours-lessons=90); plans/AC1-build-plan.md:124; L07.html:2; L08.html:2",
     "status": "PASS",
     "evidence": "Lesson hours from index cards: L01 11, L02 12, L03 11, L04 11, L05 12, L06 12, L07 11, L08 10; sum 90 equals "
                 "data-hours-lessons=90 and the plan line 124 split. No pace estimate is used to fail (architect ruling)."},
]

mutants = [
    {"id": "r9-m9a", "description": "L07 last vesting year takes the base, dropping the remainder", "killed_by": "AssertionError in lab-AC1-L07-1 (r9)"},
    {"id": "r9-m9b", "description": "L07 vesting window off by one (index > vest_years)", "killed_by": "AssertionError in lab-AC1-L07-1 (r9)"},
    {"id": "r9-m9c", "description": "L07 APIC change sign reversed", "killed_by": "AssertionError in lab-AC1-L07-1 (r9)"},
    {"id": "r9-m9d", "description": "L07 cash-flow statement without the SBC add-back", "killed_by": "AssertionError in lab-AC1-L07-1 (r9)"},
    {"id": "r9-m9e", "description": "L08 current tax ignores the temporary difference", "killed_by": "AssertionError in lab-AC1-L08-1 (r9)"},
    {"id": "r9-m9f", "description": "L08 deferred tax balance sign flipped", "killed_by": "AssertionError in lab-AC1-L08-1 (r9)"},
    {"id": "r9-m9g", "description": "L08 deferred tax balance without the tax rate", "killed_by": "AssertionError in lab-AC1-L08-1 (r9)"},
    {"id": "r7-m8a", "description": "L08 deferred expense from taxable income, not the balance change", "killed_by": "AssertionError in lab-AC1-L08-1 (r10 re-run)"},
    {"id": "r7-m7a", "description": "L07 last-year branch disabled", "killed_by": "AssertionError in lab-AC1-L07-1 (r10 re-run)"},
    {"id": "r7-m7b", "description": "L07 base amount plus one cent", "killed_by": "AssertionError in lab-AC1-L07-1 (r10 re-run)"},
    {"id": "r8-n2life", "description": "L08 book depreciation over LIFE minus one", "killed_by": "AssertionError in lab-AC1-L08-1 (r10 re-run)"},
    {"id": "r8-n3sign", "description": "L08 deferred expense sign reversed", "killed_by": "AssertionError in lab-AC1-L08-1 (r10 re-run)"},
    {"id": "r8-n4te", "description": "L08 total tax expense omits the deferred part", "killed_by": "AssertionError in lab-AC1-L08-1 (r10 re-run)"},
    {"id": "r10-m10b", "description": "L07 APIC change one cent short of the SBC expense", "killed_by": "AssertionError in lab-AC1-L07-1 (r10)"},
    {"id": "r10-m10d", "description": "L08 deferred expense equals the balance, not its change", "killed_by": "AssertionError in lab-AC1-L08-1 (r10)"},
    {"id": "r10-m10e", "description": "L08 current tax computed on pretax plus the difference", "killed_by": "AssertionError in lab-AC1-L08-1 (r10)"},
]

rows = []
seen = set()
for row in prev["rows"]:
    rid = row["id"]
    seen.add(rid)
    if rid in fresh:
        status, ev = fresh[rid]
        rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": status, "evidence": ev})
    elif row["status"] == "PASS":
        rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": "PASS",
                     "evidence": CARRY + row["evidence"]})
    else:
        raise SystemExit(f"unhandled non-PASS row {rid}")
rows.extend(new_rows)
for row in rows:
    if row["status"] != "PASS":
        raise SystemExit(f"non-PASS row {row['id']}")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 10,
    "round_note": "round 10 (independent re-verification of AC1-c after the round-9 pin 96dd532, to af08ad1). Delta: "
                  "L07.html:140 (HORIZON comment, also in the twin), L07.html:452 and L08.html:394 (footers), L08.html:216 "
                  "(one rewritten sentence). Round-9 FAIL id AC1-c-r7-L08-216-so-clause is re-verified PASS; the two round-9 "
                  "UNVERIFIABLE mutant rows are re-run with the round-7 and round-8 scripts and now PASS. All 80 round-9 ids "
                  "are kept.",
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 10; did not build AC1 and shares no context with its "
                "builders or earlier verifiers",
    "pin": "af08ad1",
    "base": "96dd532 (round-9 pin, for the delta)",
    "checkout": str(checkout),
    "scratch": "/tmp/AC1-v/AC1-c",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": [
        "ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py",
        "ledgers/AC1/scripts/AC1-c-r10/build_fragment_r10.py",
        "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py",
        "ledgers/AC1/scripts/AC1-c-r7/seed_sweep_and_mutants.sh",
        "ledgers/AC1/scripts/AC1-c-r8/mutants_and_sweep.sh",
        "ledgers/AC1/scripts/AC1-c-r8/new_mutants.sh",
    ],
    "notes": [
        "Not checked: the Pyodide browser runtime; the 10 s bound was measured only in local Python via page_smoke.",
        "Not checked: other slices (L01-L06, project, grader, cards outside c091-c125 and the L07/L08 cards).",
        "The round-7 and round-8 shell scripts hardcode /tmp/verify7-AC1-c and /tmp/verify8-AC1-c, which are absent here; "
        "they were run with CHK and the output paths rewritten by sed to this checkout and /tmp/AC1-v/AC1-c.",
        "Judgement for the architect: n1ceil, n1b, m10c (base amount) and m10a (timing) survive. The lesson states the "
        "floor base and the timing (L07.html:59-64, :63, :81) and the lab docstring states the remainder rule, but the "
        "lab's stated checks (L07.html:126) are the sums and identities only, and no project, grader, plan or contract "
        "text fixes the rule. They are recorded as out-of-scope PASS rows; if the lab should check them, that is a FAIL "
        "for a builder to fix, not for this verifier.",
        "Hours: lesson-hour sum 90 equals the hub split; no per-hour pace estimate was used to fail a row (architect ruling).",
        f"Row counts: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}.",
    ],
    "summary": f"PASS: all {len(rows)} rows. Round-9 FAIL (L08:216 'so' clause) is re-verified PASS on the rewritten "
               f"sentence; the two round-9 UNVERIFIABLE mutant rows are re-run and PASS; footers and the HORIZON comment "
               f"verified; 16 mutants killed; four survivors classified out of scope.",
}
out = checkout / "ledgers/AC1/AC1-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "carried-ids-check", len(seen), counts, verdict)
