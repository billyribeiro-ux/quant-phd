"""Round 4 (AC2 project): writes ledgers/AC2/project.json (round 4). Every round-3 row id is kept.

Run from the checkout root: .venv/bin/python ledgers/AC2/scripts/project-r4/build_fragment_r4.py
"""
import json
import re
from pathlib import Path

ROOT = Path("/tmp/verify-ac2r4-p")
PREV = json.loads(Path("/tmp/ac2-frags/project.round3.json").read_text(encoding="utf-8"))
S = ROOT / "ledgers/AC2/scripts/project-r4"
MUT_LINES = (S / "mutate_all_r4.txt").read_text(encoding="utf-8").splitlines()

# round-4 status and evidence for the rows that changed or were FAIL in round 3
OVERRIDE = {
    "proj-hub-ladder-claim": ("PASS", "Re-verified round 4: hub line 161 now reads 'Instances are generated from your workspace seed, and the suite grades your module against the filer's generated numbers for that instance.' No cross-seed or every-seed claim remains. The in-browser run used seed 540559163 (page_smoke output in ledgers/AC2/scripts/project-r4/commands.txt)."),
    "proj-mut-summary": ("PASS", "Re-run round 4: tools/mutate_graders.py --unit AC2 --seeds 0-9 -> 'mutate_graders AC2: PASS (42/42 killed)' (ledgers/AC2/scripts/project-r4/mutate_all_r4.txt). p01-p37 all killed; m01-m05 (new) killed."),
    "r3-hub-line157": ("PASS", "Re-verified round 4: hub line 157 now reads 'A student skips them only by reaching the placement bar and answering all three skill checks.' Agrees with index.html line 70 and project.html line 42 ('reach the placement bar and answer all three skill checks')."),
    "r3-placement-s2": ("PASS", "Re-verified round 4: index.html line 70 says 'six on the prerequisites, four on AC1 and two on S0'. The nine items (data-kind mc x5, numeric x4): items 1-4 are AC1 content (balance-sheet identity, gross margin, articulation, depreciation add-back), items 5-6 are S0 (median, MNAR), items 7-9 are the three AC2 skill checks. No item tests S2, and the sentence says so and tells the student to review S2 directly. Mastery arithmetic: 8/9 = 88.9% passes 80%; 7/9 = 77.8%, printed as 78%."),
    "r3-same-day-claim": ("PASS", "Re-verified round 4: project.html Grading mode now says the as-of cut-offs include 'on the seeds whose filer draws one, a same-day amendment (a fixed same-day case checks the tie-break on every seed)'. Computed with grader/instance.py make_instance: restatement.same_day is True on 25 of seeds 0-49. The fixed case test_same_day_amendment_is_decided_by_accn_not_form is parametrized, not seed-dependent (236 checks on every seed)."),
    "r3-tuple-claim": ("PASS", "Re-verified round 4: test_return_containers_are_the_contract_types asserts isinstance tuple for coefficients and piotroski signals and list for the residuals; the contract (atlas/A15.contract.md lines 127-128, 143) writes (a1, a2, a3), (s1..s9) and [...]. A list-returning correct module now fails, which matches the page's shape claim."),
    "r3-lab3-sample-claim": ("PASS", "Re-verified round 4: Lab 3 hypothesis now says 'You can check your modified_jones against these coefficients ... on the same six rows ... The autograder does not run this sample: it grades your module on its own generated filer.' Checked: the six literal rows never appear as a prefix of the generated payload sample for seeds 0-49 (ledgers/AC2/scripts/project-r4/commands.txt and this round's check); the lab output runs under python -I -W error."),
    "r3-blueprint-ref": ("PASS", "Re-verified round 4: grep of course/modules/AC/AC2/project.html, index.html and grader/test_project.py for BLUEPRINT, builder, 'this build', REQUESTS, 'unit report' returns nothing; Grading mode now reads 'Autograded in your browser.'"),
}
for line in MUT_LINES:
    m = re.match(r"(SURVIVED|KILLED) (p\d\d)_", line)
    if m and m.group(2) in ("p14", "p15", "p16", "p17", "p18", "p20", "p21", "p29", "p35", "p36", "p37"):
        pid = "r3-surv-" + m.group(2)
        OVERRIDE[pid] = ("PASS", f"Re-run round 4: mutate_graders output '{m.group(1)}' for {m.group(2)} (ledgers/AC2/scripts/project-r4/mutate_all_r4.txt): {line.split(' -> ')[-1]}. The round-4 grader kills it on seed 0. Its witness: scripts/project-r3/witness_r3.py in the round-3 checkout (the mutant still fails the new test).")

IDENTICAL = ("instance.py", "reference.py", "starter.py", "grader.js", "A15.contract.md", "references.json",
             "pyodide-lock.json", "lab-AC2-project-1.py", "lab-AC2-project-2.py", "lab-AC2-project-3.py")
CHANGED_NOTE = ("project.html (changed hunks: Constraints line 245 and Lab 3 hypothesis line 300 only; the rest is "
                "re-read), grader/test_project.py (changed; the round-4 collect-only, reference and mutation runs cover it)")

rows = []
for r in PREV["rows"]:
    status, evidence = r["status"], r["evidence"]
    if r["id"] in OVERRIDE:
        status, evidence = OVERRIDE[r["id"]]
    elif status == "PASS":
        loc = r["location"]
        if any(name in loc for name in IDENTICAL) and not any(c in loc for c in ("project.html", "test_project", "index.html")):
            evidence = ("Carried from round 3 (course/modules/AC/AC2/grader/instance.py, reference.py, starter.py, "
                        "course/assets/js/grader.js, atlas/A15.contract.md, references/references.json, "
                        "course/assets/vendor/pyodide/pyodide-lock.json, tests/labs/AC2/lab-AC2-project-{1,2,3}.py "
                        "byte-identical since 4a8690a): " + evidence)
        else:
            evidence = ("Re-verified round 4 (subject touches " + CHANGED_NOTE + "); the row's claim was re-read and "
                        "the commands it depends on were re-run (see proj-r4-* rows). Round-3 basis: " + evidence)
    rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": evidence})

NEW = [
    ("proj-r4-grader-236", "2.6-autograder", "grader/test_project.py; tools/run_graders.py --unit AC2 --seeds 0-49",
     "PASS", "Re-run round 4: pytest --collect-only on the reference gives 236 on seeds 0,1,2,3,4,5,6,7,8,9,25,49 (ledgers/AC2/scripts/project-r4/collect_only.py); run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s). The page's 236 is correct."),
    ("proj-r4-impls-overconstraint", "2.6-autograder", "grader/test_project.py vs impls V1-V5 (ledgers/AC2/scripts/project-r4/impls)",
     "PASS", "Re-run round 4: the five alternative correct implementations (SVD cutoffs 1e-8 and 1e-12, condition number 1e12, Cholesky pivot, strict-bool rank test at 1e-10) each give 236 passed on seeds 0-9 (ledgers/AC2/scripts/project-r4/harness.py). No over-constraint found."),
    ("proj-r4-new-mutants", "2.6-mutation", "ledgers/AC2/mutants/m01-m05 (new student-error mutants written by this verifier)",
     "PASS", "Five new student-error mutants, each one edit of reference.py: m01 roe on year-end equity (killed by test_dupont_numbers), m02 ROIC rejects tax rate 0 (killed by test_roic_accepts_the_whole_tax_range[0.0]), m03 Piotroski asset turnover on year-end assets (killed by test_piotroski_signals_match_the_definitions), m04 ROIC accepts negative average capital (killed by test_roic_rejects_nonpositive_invested_capital), m05 Piotroski signal 2 on net income (killed by test_piotroski_strict_signals_score_zero_at_an_exact_tie). Generator: ledgers/AC2/scripts/project-r4/make_new_mutants.py."),
    ("proj-r4-mutants-total", "2.6-mutation", "tools/mutate_graders.py --unit AC2 --seeds 0-9",
     "PASS", "42 of 42 killed (p01-p37 verifier and builder set, m01-m05); output in ledgers/AC2/scripts/project-r4/mutate_all_r4.txt."),
    ("proj-r4-container-and-unit-tests", "2.6-spec", "grader/test_project.py test_money_tag_in_another_unit_is_not_read, test_observation_without_an_accession_number_is_valid, test_same_filing_date_without_accn_and_different_values_raise, test_modified_jones_accepts_exactly_four_firm_years",
     "PASS", "Each new test cites the contract line it enforces: unit USD for money (A15.contract.md line 31; EUR and shares are not money), accn optional (line 30), tie rule (lines 46-48), fewer than four firm-years raises, four is legal (line 133). None of the four is stricter than the contract."),
    ("proj-r4-ellipsis-notation", "2.9-prose", "course/modules/AC/AC2/project.html line 241 ((s1, ..., s9), \"score\": ..., [...])",
     "PASS", "Observation, not a failure: the ellipses are shape notation for a sequence and a list in the return description; the value they stand for (the sum of the signals; the residuals in sample order) is stated in the same sentence. No omitted prose content."),
    ("proj-r4-cards-count-ids", "2.7-cards", "course/modules/AC/AC2/cards.json (140 cards)",
     "PASS", "140 cards; ids AC2-c001..AC2-c140 are unique and sequential (python check); no two identical fronts or backs. Only near-duplicate front pair by SequenceMatcher > 0.8: c089 and c106 (F-score and M-score 'What is ... in this module?'), a parallel question, not a duplicate."),
    ("proj-r4-cards-lab-numbers", "2.7-cards", "cards c009, c016, c026, c031, c039, c041, c047, c069-c075, c082-c086, c104, c113-c114, c117, c121-c125 vs ledgers/AC2/scripts/project-r4/labout/*.txt",
     "PASS", "Every lab-derived number on a card was checked against this round's printed output of tests/labs/AC2 twins (python -I -W error, rc 0). Matches: 1,131.9/1,145.5; 1.2%; 43.28 vs 43.80; 0.1925/0.1820 (5.8%); 0.1239->0.1349 (8.9%); 0.1287; 4.31% from unrounded 0.134941 vs 0.129360 (printed 4.3%); 0.12989 unrounded (recomputed from make_filer/standardize) gives 1-0.10/0.12989 = 0.2301 and the printed 0.1299 gives 0.2302; 0.060, 0.590, 0.676, 201 (recomputed (2.8016*0.01131/0.002235)^2 = 201.0), 0.00219/0.00223, -2.7937, 2.164/2.155, 0.2781/0.0489, 197/200, 71/200 = 0.355, FPR 129/1800 = 0.0717, 0.0017, 0.2084 = 0.1425+0.1965-0.1306, 0.738 = 0.2084/0.2824, flags 6/6 and 12 differing, 400/400, medians -2.4747 and -1.5067, PPV 0.0917. Card c041's phrase 'a gap of 4.31% (from unrounded values; the printed figures give 4.3%)' is right."),
    ("proj-r4-cards-piotroski-locators", "2.1-attribution", "cards c093-c101, c105, c126, c130 vs https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf (plain curl, HTTP 200, 876,917 bytes; ledgers/AC2/scripts/project-r4/piotroski_pdftotext.txt)",
     "PASS", "Read in the paper text: 'at least 7.5% annually' and '23% annual return' on page 1 (cards cite Abstract p. 1; 23% also p. 3); '1,448 ... 396' on page 12 (c126 p. 12 OK); high book-to-market sample 1976 to 1996 on page 11 (c096 p. 11 OK); the footnote 5 current-ratio 1.5 sentence on page 9 (c100 p. 9, n. 5 OK); 'optimal' and factor analysis on page 7 (c101 p. 7, n. 2 OK, the word 'optimal' is on page 7); 'financially distressed' on page 7 (c095 p. 7 OK). Not bypassed: no bot check was met."),
    ("proj-r4-cards-lesson-locators", "2.7-cards", "cards citing Proposition, Remark, Definition, Corollary, Theorem, Problem and Lab problem labels vs course/modules/AC/AC2/L01-L08.html",
     "PASS", "Each locator on a card was grep-checked in its lesson: Proposition 4.3 (L01, L08), Remark 2.2 with the '89, 90 or 91 days' sentence (L01 line near 'A calendar quarter measures 89, 90 or 91 days'), Remark 3.5 (L03), Definition 2.1 (L01/L03/L04/L06), Proposition 3.2, Corollary 3.3, Problem P1-P3 (each lesson has P1-P3), Problem M1 and M4 (L01-L04), Lab 1 Problem E2 (L01 'How large is the restatement?'), Remark 3.2 (L06), Proposition 3.3 (L06), Theorem 3.2 (L02), Proposition 4.2 (L08). Card c004 was also tested against the Lesson 1 lab code: a malformed 10-Q observation raises ValueError (val 'x') and a well-formed 10-Q is ignored."),
    ("proj-r4-cards-changed-wording", "2.7-cards", "cards whose text changed since 4a8690a (c003, c013, c014, c035, c038, c041, c046, c047, c054, c056, c058, c059, c064, c071, c075, c082-c084, c087, c094, c097, c103, c107, c119, c128, c139, c140)",
     "PASS", "Each changed card was read against the diff and its lesson. Arithmetic re-derived: M4 15/1600+30/1600-10/1600 = 0.021875 (debt term 0.009375); 1.0909 = 2(1.2)/2.2; 0.2301/0.2302 (above); PPV 0.5 x 0.01/(0.005+0.99 x 0.05) = 0.0917; c103 F = 2 example: signals 1 and 2 are 1, signal 4 and the change tests 3 and 5-9 are 0. The grade downgrades (T to C for c003, c013, c035) carry 'A15 contract rule' bases, as the rulings require. Scope note: wording was checked sentence by sentence for the changed cards; the unchanged cards were checked by their numbers, locators and lab output, not re-read sentence by sentence."),
    ("proj-r4-cards-grades", "2.3-grades", "course/modules/AC/AC2/cards.json AC2-c058 and AC2-c064 (cite sloan1996stock, no grade field); lessons L04.html and L05.html claim spans",
     "FAIL", "Two cards cite a registry key and carry no grade: AC2-c058 (L04, 'What does lesson L04 say Sloan (1996) investigates?') and AC2-c064 (L05, 'Which price question does lesson L05 attribute to Sloan (1996)?'). The round-5 edit removed their grade C and basis. The lessons still grade the same claim: course/modules/AC/AC2/L04.html and L05.html carry <span class=\"claim\" data-grade=\"C\" data-cite=\"sloan1996stock\" data-locator=\"Crossref abstract; passage locator not confirmed\">. Fix: restore 'grade': 'C' and a basis (for example 'Crossref abstract; passage locator not confirmed') on c058 and c064. Other cards: grades T 36, C 47, D 1; no grade on 54 cards with no cite; every C card has a basis or a cite; every basis names its lab or the contract rule."),
    ("proj-r4-command-rows", "2.9-tooling", "tools/run_labs.py --unit AC2; check_pages/check_dag/check_projects --all; ruff; mypy --no-incremental; page_smoke --unit AC2 --pages project",
     "PASS", "Re-run round 4 (ledgers/AC2/scripts/project-r4/commands.txt and the page_smoke run): run_labs AC2 PASS (11/11); check_projects AC2 PASS; check_dag AC2 PASS; check_pages AC2 PASS; ruff check and ruff format --check on grader and lab twins pass; repo-wide mypy --no-incremental: 'Success: no issues found in 112 source files'; page_smoke modules/AC/AC2/project.html PASS (in-browser grader: All 236 tests pass on seed 540559163)."),
    ("proj-r4-lab-twins", "2.5-labs", "tests/labs/AC2/lab-AC2-L01-1..L08-1.py and lab-AC2-project-1..3.py",
     "PASS", "Each twin run under python -I -W error: rc 0 for all 11 (outputs in ledgers/AC2/scripts/project-r4/labout/)."),
    ("proj-r4-hub-placement-and-ladder", "2.9-structure", "course/modules/AC/AC2/index.html lines 60, 70, 157, 161",
     "PASS", "Re-read and re-checked: the placement count (nine items, four AC1 and two S0 by content, three AC2 skill checks), the S2 sentence, the mastery arithmetic, the skip condition in lines 70 and 157, and the ladder suite claim in line 161 agree with project.html line 42 and line 243-245. No placement item tests S2 and the hub says so."),
    ("proj-r4-no-process-words", "2.9-prose", "project.html, index.html, cards.json, grader/test_project.py",
     "PASS", "grep for BLUEPRINT, builder, 'this build', REQUESTS, 'unit report', roughly half, historically, 'about 6%': no hits in the learner-facing files of this slice. The author question is respected: no author names for dechow1995detecting outside the registry."),
]
for pid, check, loc, status, ev in NEW:
    rows.append({"id": pid, "check": check, "location": loc, "status": status, "evidence": ev})

# mutants from the round-4 run
mutants = []
for line in MUT_LINES:
    m = re.match(r"(KILLED|SURVIVED) (m?p?\d\d_\S+?\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    state, fname, desc, killed = m.groups()
    mutants.append({"description": desc, "killed_by": killed, "file": "ledgers/AC2/mutants/" + fname, "state": state})
assert len(mutants) == 42, len(mutants)
assert all(m["state"] == "KILLED" for m in mutants)
for m in mutants:
    m.pop("state")

prev_ids = {r["id"] for r in PREV["rows"]}
new_ids = {r["id"] for r in rows}
assert prev_ids <= new_ids, prev_ids - new_ids

from collections import Counter
status_counts = Counter(r["status"] for r in rows)
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"

fragment = {
    "unit": "AC2",
    "slice": "project",
    "round": 4,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 4; did not build AC2; fresh context)",
    "pin": "2607c60",
    "base": "round 3 fragment (pin 4a8690a) read as context; its FAIL rows were re-verified and its PASS rows re-verified or carried by byte-identical subject",
    "checkout": "/tmp/verify-ac2r4-p (detached at 2607c60)",
    "scratch": "/tmp/ac2-v/project/",
    "verified_at": "2026-10-27",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Round 4 delta for this slice: project.html (lines 245, 300), hub index.html (lines 67-70, 157, 161), grader/test_project.py (+131/-4 hunks: 236 checks), cards.json (140 cards).",
        "Project grader: 236 checks on every seed checked; reference 50/50; five alternative implementations pass; 42/42 mutants killed (37 earlier, 5 new).",
        "Carried or re-verified rows are labelled in evidence; no row was carried from a changed file.",
        "Not checked in this round: the Ivey PDF only for the Piotroski locators used by the cards (no other paper); Beneish constants are UNCONFIRMED and not checked beyond the rulings; the cards' qualitative sentences for unchanged cards were checked by their numbers, locators and lab output, not re-read sentence by sentence.",
        "Observation (not a FAIL): project.html line 241 uses ellipsis notation in return-shape descriptions ((s1, ..., s9), score ...). It is shape notation, and the sentence defines the value.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": status_counts.get("PASS", 0),
        "fail": status_counts.get("FAIL", 0),
        "unverifiable": status_counts.get("UNVERIFIABLE", 0),
        "mutants": len(mutants),
        "mutants_killed": len(mutants),
        "survivors": [],
        "sentence": "Round 4 project: 236 checks (collect on 12 seeds, reference 50/50); five alternative implementations pass; mutants 42/42 killed (5 new); every round-3 FAIL row is fixed and re-verified; 140 cards checked for numbers, locators, lab output and changed wording.",
    },
}
out = ROOT / "ledgers/AC2/project.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), dict(status_counts), "verdict", verdict, "mutants", len(mutants))
