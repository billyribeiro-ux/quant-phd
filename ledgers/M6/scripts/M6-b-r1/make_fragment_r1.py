import json
import sys

CARRY = ("Carried from round 8 (course/modules/M/M6/L05.html, L06.html, L07.html, L08.html and "
         "tests/labs/M6/lab-M6-L05..L08-1.py byte-identical since f618cf1: git diff --stat f618cf1 HEAD over them is empty, "
         "ledgers/M6/scripts/M6-b-r1/delta_slice_b.txt): ")
S = "ledgers/M6/scripts/M6-b-r1/"


def carry(rid, check, location, text):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": CARRY + text}


def rerun(rid, check, location, text):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": text}


rows = [
    carry("M6b-r3-L08-lab-part-labels", "prose names lab Parts that the printed output does not label",
          "course/modules/M/M6/L08.html lines 129-130, 230-262; tests/labs/M6/lab-M6-L08-1.py",
          "the cited L08 lines are unchanged; " + S + "twin-L08.out lines 1 and 5 print 'Part A:' and 'Part B:'."),
    carry("M6b-r3-cards-c081-lab-part-B", "card number-and-lab claim matches the printed output",
          "course/modules/M/M6/cards.json M6-c081",
          "card M6-c081 is unchanged: per-id JSON compare f618cf1 vs HEAD (" + S + "cards_per_id_compare.txt) lists changed ids "
          "M6-c062, M6-c102, M6-c141 and added M6-c149 only. Card text 'passes all 1023 cells at levels 0 to 9 (Lab 1 Part B)' "
          "matches " + S + "twin-L08.out line 17 'cells_agreeing 1023 of 1023' (re-run this round); 1+2+...+512 = 1023."),
    carry("M6b-r3-L05-R2-unnamed-fact", "facts assumed without proof are named (Assumption or section 9 standard-fact list)",
          "course/modules/M/M6/L05.html line 374 (R2 solution); line 489 (section 9)",
          "L05.html line 374 reads 'a standard fact used without proof (listed in §9)'; line 489 names both facts (integral of a bounded "
          "continuous function on a closed square minus an open disk; invariance of the integral under a measure-preserving map)."),
    rerun("M6b-r3-page-smoke", "page_smoke on L05-L08 (console, KaTeX, 360px, dark theme)",
          "tools/page_smoke.py --unit M6 --pages L05 L06 L07 L08",
          "Run this round at 95f3f8cb: 'page_smoke modules/M/M6/L05.html, L06, L07, L08: PASS', 'page_smoke M6: PASS' (" + S + "page_smoke_M6_L05-L08.txt, exit 0)."),
    rerun("M6b-r3-check-pages", "tools/check_pages.py --unit M6",
          "course/modules/M/M6/*.html, cards.json",
          "Run this round at 95f3f8cb: 'check_pages M6: PASS', exit 0 (" + S + "check_pages_M6.txt)."),
    rerun("M6b-r3-check-dag", "tools/check_dag.py --unit M6", "course/modules/M/M6/*.html",
          "Run this round at 95f3f8cb: 'check_dag M6: PASS', exit 0 (" + S + "check_dag_M6.txt). check_dag does not test the source locator; see M6b-r3-dag-references."),
    rerun("M6b-r3-run-labs", "run_labs M6: every inline lab equals its twin and its expected block",
          "course/modules/M/M6/L05-L08.html; tests/labs/M6/lab-M6-L05..L08-1.py",
          "Run this round at 95f3f8cb: 'run_labs M6: PASS (15/15)', exit 0 (" + S + "run_labs_M6.txt)."),
    rerun("M6b-r3-twins-isolated-run", "twins run alone under python -I -W error with empty stderr",
          "tests/labs/M6/lab-M6-L05..L08-1.py",
          "Run this round from a fresh mktemp directory with .venv/bin/python -I -W error: exit 0 for L05, L06, L07, L08; "
          "each .err is 0 bytes (" + S + "twin_isolated.txt, twin-L0*.err, twin-L0*.out)."),
    rerun("M6b-r3-ruff-mypy-twins", "ruff and mypy on the four twins", "tests/labs/M6/lab-M6-L05..L08-1.py",
          "Run this round: ruff check tests/labs/M6 'All checks passed!'; ruff format --check '15 files already formatted'; "
          "mypy --no-incremental on the four twins 'Success: no issues found in 4 source files' (" + S + "ruff_M6.txt, " + S + "mypy_twins_M6.txt)."),
    rerun("M6b-r3-pytest-lab-suites", "pytest subset -k 'page or lab or card or dag or concept or figure or docs'", "tests/",
          "Run this round with tests/test_lx1_project_lab3.py deselected (--ignore): 470 passed, exit 0 (" + S + "pytest_subset_excl_lx1.txt). "
          "The unfiltered subset run has one failure outside this slice: test_a_population_sd_variant_of_the_two_pass_check_raises "
          "in tests/test_lx1_project_lab3.py (LX1; " + S + "pytest_subset.txt). The LX1 fix commit 9a85e9e8 is not in pin 95f3f8cb "
          "(git merge-base --is-ancestor is false), and no M6-b path is involved. Recorded in notes."),
    rerun("M6b-r3-katex-strict", "strict KaTeX re-parse of every rendered expression on L05-L08",
          "course/modules/M/M6/L05-L08.html; tools/katex_strict.js (used by page_smoke.py)",
          "Covered by 'page_smoke M6: PASS' run this round (" + S + "page_smoke_M6_L05-L08.txt); no standalone result claimed."),
    carry("M6b-r3-numbers-L05", "numbers in L05 prose equal the lab and closed forms",
          "course/modules/M/M6/L05.html lines 52, 106, 140-194 of the text extraction (Remark 3.3), line 149, lines 347-349 (Problem E2)",
          "twin-L05 output re-run this round (" + S + "twin-L05.out): dy_first_closed 0.7853981634, block_integral_closed 0.3217505544, "
          "six partial sums 0.3217505544 x 1..6, partial_sums_equal_count_times_block True; matches the prose digits. "
          "Base re-derivation (pi/4, -pi/4, arctan 2 - pi/4 = 0.32175055439664, N = 10 for E2) carried."),
    carry("M6b-r3-math-L05", "proofs and statements in L05 are correct and carry their hypotheses",
          "course/modules/M/M6/L05.html lines 82, 135, 374, 393, 407, 413",
          "L05 is byte-identical; the R2 and Proposition 3.2 proofs were re-derived in the base round (dyadic blocks disjoint, f >= 0 on each block, "
          "integral arctan 2 - pi/4 > 0 for every k; swap tau gives 0 by invariance named in §9)."),
    carry("M6b-r3-numbers-L06", "numbers in L06 prose equal the lab output",
          "course/modules/M/M6/L06.html lines 63, 65, 146, 155, 190, 194, 198, 243, 255, 453; twin-L06.out",
          S + "twin-L06.out (re-run this round) prints 'density 2 1/2 2 1/3', 'events_checked 16', 'events_checked 32', "
          "'absolute_continuity_failures 1', 'candidate_density_misses 16'; the L06 prose lines match these."),
    carry("M6b-r3-math-L06", "proofs and statements in L06 are correct",
          "course/modules/M/M6/L06.html lines 74, 105, 107, 257 and the proofs",
          "L06 is byte-identical to f618cf1; base round re-checked the statements and proofs (Prop 2.3, Remark 2.4, Theorem 2.2 hypotheses)."),
    carry("M6b-r3-numbers-L07", "numbers in L07 prose equal the lab output",
          "course/modules/M/M6/L07.html lines 276-296, 312, 316, 320, 385, 392, 459, 482, 513-516",
          "L07 is byte-identical to f618cf1; " + S + "twin-L07.out re-run this round with exit 0 and empty stderr."),
    carry("M6b-r3-math-L07", "proofs and statements in L07 are correct and carry hypotheses",
          "course/modules/M/M6/L07.html lines 53, 100, 105, 136, 422-423, 490-493",
          "L07 is byte-identical to f618cf1; the Remark 2.3 hypothesis p(omega) > 0 wording was checked in the base round."),
    carry("M6b-r3-numbers-L08", "numbers in L08 prose equal the lab output",
          "course/modules/M/M6/L08.html lines 52, 124, 263, 270, 354, 361, 368, 409, 458, 463, 472; twin-L08.out",
          S + "twin-L08.out line 2 'paths 1024 steps 10' (2^10 = 1024); line 17 'cells_agreeing 1023 of 1023'; line 31 'cells_agreeing 0 of 1023' "
          "for the biased walk with increment -1/3 = 2(1/3)-1; the prose matches."),
    carry("M6b-r3-math-L08", "proofs and statements in L08 are correct and carry hypotheses",
          "course/modules/M/M6/L08.html lines 52, 56, 108-120 (Prop 2.3), 271, 289, 336, 343, 481, 490",
          "L08 is byte-identical to f618cf1; the base round checked the §2 fair-walk definition (p = 1/2) and Definition 1.2 locators; increment 2p-1 matches twin-L08.out."),
    carry("M6b-r3-notation-L08-w", "notation: every symbol in L05-L08 against notation/notation.json",
          "course/modules/M/M6/L08.html line 56 (w(omega)); L05-L08 math",
          "notation/ and tools/ are unchanged since f618cf1 (git diff --stat empty), so notation.json is the same registry; "
          "none of its 8 registered symbols is used with another meaning in L05-L08 (base scan); w is lesson-local, as in L06."),
    rerun("M6b-r3-cards-L05-L08", "cards for L05-L08 agree with current lesson text; card numbers appear in lesson",
          "course/modules/M/M6/cards.json (45 cards whose lesson is L05-L08)",
          "Subject changed: the per-id compare (" + S + "cards_per_id_compare.txt) shows 45 in-slice cards and exactly one changed, M6-c062, "
          "which is re-verified in row M6b-r1-cards-c062-lab-part-B. The other 44 in-slice cards are identical to f618cf1."),
    carry("M6b-r3-process-words", "no process words in learner text (round/verifier/fix/previous/etc.)",
          "course/modules/M/M6/L05.html..L08.html",
          "L05-L08 are byte-identical to f618cf1; re-grep this round for round, verifier, ledger, fix, reviewer finds nothing in the slice files (see " + S + "delta_slice_b.txt)."),
    {
        "id": "M6b-r3-dag-references",
        "check": "DAG: concepts used outside prerequisite closure; references section sources",
        "location": "course/modules/M/M6/L05.html:489, L06.html:472, L07.html:523, L08.html:506 (locator '01-foundations.yaml:286-288'); curriculum/01-foundations.yaml lines 287-289 at HEAD",
        "status": "FAIL",
        "evidence": "Subject changed in the delta. The source entries moved: at f618cf1 curriculum/01-foundations.yaml has 'sources:' at line 286, Williams at 287, Billingsley at 288; at HEAD (95f3f8cb) they are at 287 ('sources:'), 288 (Williams) and 289 (Billingsley). The shift comes from a +1-line edit at line 183 of that file in the delta (git diff f618cf1..HEAD -- curriculum/01-foundations.yaml; grep -n run this round). "
                    "Each of the four lesson pages still cites the locator '01-foundations.yaml:286-288', which at HEAD covers 'doubling-strategy', 'sources:' and Williams but not Billingsley. The locator was correct at f618cf1 and is stale now. check_dag M6 PASS does not check this locator. The sentence itself (two sources listed) is still true.",
        "fix": "In course/modules/M/M6/L05.html line 489, L06.html line 472, L07.html line 523 and L08.html line 506, change '01-foundations.yaml:286-288' to '01-foundations.yaml:288-289' (the two source entries at HEAD). Then re-run check_pages M6 and page_smoke M6 for L05-L08.",
    },
    carry("M6b-r3-grades", "grade labels on claims match the proof status",
          "course/modules/M/M6/L05.html..L08.html key-results tables and data-grade attributes",
          "L05-L08 are byte-identical to f618cf1; no data-grade attribute changed since the pin."),
    carry("M6b-r5-L07-quiz-q6-hypothesis", "L07 quiz Q6 states the hypothesis p(omega)>0 that the theorem uses",
          "course/modules/M/M6/L07.html lines 487-493",
          "L07 is byte-identical to f618cf1; the quiz text is unchanged."),
    {
        "id": "M6b-r6-cards-changed-c058-c062-c073-c080-c140",
        "check": "cards changed in round 6 still agree with lessons",
        "location": "course/modules/M/M6/cards.json (c058, c062, c073, c080, c140)",
        "status": "PASS",
        "evidence": "Subject changed (c062), so re-verified from scratch: M6-c062 in row M6b-r1-cards-c062-lab-part-B. M6-c058, c073, c080 and c140 are identical to f618cf1 in the per-id compare (" + S + "cards_per_id_compare.txt: changed ids are M6-c062, M6-c102, M6-c141 only), and their lessons L06 are byte-identical.",
    },
    rerun("M6b-r8-verify-refs-and-pytest", "verify_refs --offline and pytest subset on the slice tooling (re-run for this round)",
          "tools/verify_refs.py; tests/",
          "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline.txt). Pytest subset: see M6b-r3-pytest-lab-suites."),
    rerun("M6b-r1-cards-c062-lab-part-B", "card M6-c062: number, lab claim, grade and basis match the lesson and the printed output",
          "course/modules/M/M6/cards.json M6-c062; course/modules/M/M6/L06.html lines 59-60, 157-158, 241-249",
          "Card changed since f618cf1 (" + S + "cards_per_id_compare.txt). Back: 'One: the event {point 5}, with μ = 0 and ν = 1/8. Lab 1 Part B counts 32 events and prints one failure (Definition 1.1).' "
          "Printed (" + S + "twin-L06.out lines 6-9): 'events_checked 32', 'absolute_continuity_failures 1', 'failing_event_mask 16 mu 0 nu 1/8'. "
          "Mask 16 is bit 4, i.e. point 5; L06.html line 249 maps it to {point 5}. L06.html line 158 states 'Exactly one of the 32 events fails the absolute-continuity test'. "
          "Definition 1.1 (line 59-60) is absolute continuity. 32, one, 1/8 and point 5 all appear in the lesson. Basis 'Lab 1, Part B: exact enumeration' names the lab, as the grade C requires. "
          "Observation only (not a ruling-26 kind): the fact is provable on the page (mu(A)=0 iff A is contained in {point 5}), so C is a conservative grade."),
]

fragment = {
    "unit": "M6",
    "slice": "b",
    "round": 1,
    "verifier": "Haiku independent verifier, M6-b round 1 (closing delta, did not build M6)",
    "pin": "95f3f8cb",
    "base": "f618cf1 (round-8 fragment ~/.fanout/frags/C-M6-b.round8.json, verdict PASS, pin f618cf1). Delta f618cf1..95f3f8cb over slice paths: cards.json only (changed M6-c062 in slice; M6-c102, M6-c141 are L10; M6-c149 added, L03). L01.html and L04.html and lab-M6-L04-1.py are slice a.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M6-b (detached at 95f3f8cb, .venv symlinked)",
    "scratch": "ledgers/M6/scripts/M6-b-r1/",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lesson slice, no grader in slice b: mutants [] is intentional (round-6 ruling); ruling 37 writes no new mutants and no standing mutant set exists for this slice.",
        "Out of slice, observed: tests/test_lx1_project_lab3.py::test_a_population_sd_variant_of_the_two_pass_check_raises fails at 95f3f8cb (" + S + "pytest_subset.txt, " + S + "pytest_lx1_lab3_observed.txt). The LX1 owner must triage it; fix commit 9a85e9e8 is not in this pin. Not an M6-b defect.",
        "Out of slice: cards M6-c102 and M6-c141 (L10) changed in the delta and were not verified by this slice; M6-c149 (L03) added, slice a.",
        "Not checked: check_projects and run_graders (no project or grader in slice b); hours arithmetic (no hour figure changed in slice b); the full repo diff of 30019 files was not read beyond the slice paths and the curriculum and references hunks, which were read only for their effect on the M6 locator.",
        "The FAIL row (M6b-r3-dag-references) is a delta regression: it was PASS at f618cf1 and is caused by a curriculum edit outside this slice. Fix in the four lesson pages, then delta-verify once more (ruling 30).",
    ],
    "summary": "M6 slice b closing delta at 95f3f8cb: verdict FAIL with one row. The cited locator '01-foundations.yaml:286-288' in L05, L06, L07 and L08 is stale after an edit to curriculum/01-foundations.yaml (sources now at 288-289). Card M6-c062 (changed to grade C) re-verified PASS. All other base rows PASS: carried by byte-identity or re-run this round (check_pages, check_dag, run_labs 15/15, page_smoke L05-L08, twins isolated, ruff/mypy, pytest subset excluding an out-of-slice LX1 test, verify_refs offline).",
}

out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "FAIL", sum(r["status"] == "FAIL" for r in rows))
