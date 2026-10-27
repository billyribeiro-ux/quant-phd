"""Round 5 (AC2 project slice): builds ledgers/AC2/project.json from the round-4 fragment (context) and this round's checks."""
import json
from pathlib import Path

CHECKOUT = Path("/tmp/verify-ac2r5-p")
R4 = json.loads(Path("/tmp/ac2-frags/project.round4.json").read_text(encoding="utf-8"))
CARDS = json.loads((CHECKOUT / "course/modules/AC/AC2/cards.json").read_text(encoding="utf-8"))
CARRY = ("Carried from round 4 (course/modules/AC/AC2/project.html, course/modules/AC/AC2/index.html, "
         "course/modules/AC/AC2/grader/*, tests/labs/AC2/lab-AC2-project-{1,2,3}.py, atlas/A15.contract.md, "
         "references/references.json, course/assets/js/grader.js, course/assets/vendor/pyodide/pyodide-lock.json "
         "byte-identical since 2607c60; git diff --quiet verified this round): ")
RUNS = "re-run this round: see proj-r5-* rows (run_graders 0-49, collect 236, mutants 47/47, impls 50/50, page_smoke, run_labs, check_pages/check_projects/check_dag)."

rows = []
for r in R4["rows"]:
    if r["id"] == "proj-r4-cards-grades":
        continue  # replaced below by the re-verified row
    if r["status"] != "PASS":
        raise SystemExit(f"unexpected round-4 non-PASS row {r['id']}")
    basis = r["evidence"]
    rows.append({
        "id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS",
        "evidence": CARRY + RUNS + " Round-4 basis retained: " + basis,
    })

def lesson_ids(lesson):
    return [x["id"] for x in CARDS if x["lesson"] == lesson]

LESSON_EVIDENCE = {
    "L01": "Checked each card against L01.html: Definition 2.1 (window 350-380), Remark 2.2 (364/371 pass, 91/730 fail), Definition 3.1, Proposition 3.2, Corollary 3.3, Proposition 4.3, Remark 3.4, Definition 4.1, Lab 1 output (lab-AC2-L01-1.out: 1,131.9 at 2023-06-30 cut-off, 1,145.5 with none; ratio 1.012 from the generator), Problem P1 and c013/c120 contract basis. No card contradicts its lesson.",
    "L02": "Checked against L02.html: Definition 1.1, Remark 2.1 (2(1+g)/(2+g) = 1.0909 at g=0.2, recomputed), Proposition 1.2, Theorem 3.2, Section 5, Definition 4.1 (DSO x365, current ratio, debt to assets, gross margin), Example 4.2; lab-AC2-L02-1.out: DSO 43.28 for 2022 vs 43.80 elsewhere, ROE 0.1925 vs 0.1820 (5.8% recomputed). c025 Penman C matches the lesson's stated grade.",
    "L03": "Checked against L03.html: Definition 1.1, Definition 2.1, Proposition 2.2, Remark 2.3, Definition 3.1, Proposition 3.2, Proposition 3.4, Remark 1.2 and Remark 3.5, Section 4, E2. Lab output recomputed from the lab's own functions (lab-AC2-L03-1 namespace): FY2023 ROIC 0.134941 on average capital, 0.129360 on year-end (gap 4.31%, c041 correct), zero-tax 2024 0.12989 so the 10% tax is 23.01% (c047 correct), 1,038.3 average. Printed 0.1239, 0.1349, 0.1287 match lab output.",
    "L04": "Checked against L04.html: Definition 1.1-1.3, Definition 2.1 (operating partition), Proposition 2.2, Corollary 2.3, Remark 2.4, Proposition 3.1, Proposition 4.1, Section 5 derivation (M4: 15/1600, 30/1600, -10/1600, sum 0.021875, recomputed), and the honest-pending text (c062). c058 now carries grade C and basis matching the data-grade C span in L04.html ('Crossref abstract; passage locator not confirmed').",
    "L05": "Checked against L05.html: Definition 1.1-1.2, Proposition 2.1, Proposition 2.3 (-2*phi(q)/0.2 = -2.7996 recomputed (scipy-free NormalDist, python -I)), Remark 2.2, E1 (binomial 0.0154 recomputed), E2-E3 (0.0022350/(0.011314/sqrt(120)) = 2.164), R1 (T = 200.99, i.e. 201, recomputed). Lab-AC2-L05-1.out: 0.00219 vs 0.00223, 0.060, 0.590, 2.155, -2.7937, seed 0 mean 0.00075 t 0.676. c064 now carries grade C and basis matching data-grade C in L05.html.",
    "L06": "Checked against L06.html: Definition 1.1-1.2, Definition 2.1, Proposition 3.1 and 3.3 and Remark 3.2, P2 scale result, Section 6 and E1-E2; lab-AC2-L06-1.out: a1 all-minus-nm 0.2084 = 0.1425 + 0.1965 - 0.1306 (sum recomputed), 0.2084/0.2824 = 0.738, 197/200 and 0.9850 TPR and FPR 0.0017 (strong), 71/200 = 0.355 and FPR 0.0717 (weak), flags_only 6 and 6 (12 changed), se 0.2781 on 1,800 rows and 0.0489 on 57,600 rows.",
    "L07": "Checked against L07.html: Section 1 and Definition 1.1, Section 2 departures (s7 EQOFFER proxy p. 9; NetIncomeLoss; LongTermDebtNoncurrent), Section 3 (p. 6, 7, 8, 11, 12 locators and 1,448/396 counts re-read in the Ivey text piotroski_pdftotext.txt; 7.5% and 23% at pp. 1 and 3), Section 5 (footnote 5 on p. 9 and footnote 2 on p. 7 re-read), Section 4 worked firm (F = 8 and the NI = -20 variant F = 7 checked against the stated signal vectors), Proposition P1-P2. Lab output: 400/400 unchanged under x1000. c103 (changed) and c130 (changed) re-verified: F = 2 variant and six-conditions wording match Section 6 and Section 2. c093 to c101 locators confirmed.",
    "L08": "Checked against L08.html: Definition 1.1, Section 2 (Wikipedia constants re-read by plain curl this round: -4.84, 0.92, 0.528, 0.404, 0.892, 0.115, -0.172, 4.679, -0.327 and threshold -1.78, with Scribd and ycharts cited), Section 3 worked M = -1.55927 (recomputed with Fractions and the candidate constants), Proposition 4.2 and 4.3 (PPV 0.0917 recomputed; AND 0.0050 and OR 0.1450), Section 5, Section 6, lab-AC2-L08-1.out (medians -2.4747 and -1.5067; PPV 0.0099 at p=0.001 and 0.3448 at p=0.05; 49.50 flags per 1,000). c109 D grade consistent with the lesson's D. c119 TATA wording matches Section 5 and the contract's TATA line (year-end total assets).",
}

LESSON_FAIL = {
    "L08": (
        "FAIL: course/modules/AC/AC2/cards.json AC2-c107 (back) says 'The paper could not be read: the publisher, ResearchGate and SSRN returned HTTP 403, and the JSTOR record did not load.' "
        "The publisher, ResearchGate and SSRN 403s reproduce this round (plain curl: tandfonline 403, researchgate.net 403, papers.ssrn.com 403; doi.org 302 to tandfonline). "
        "But L08.html section 2 reports a JSTOR challenge only for the companion Piotroski record ('the JSTOR record of the companion Piotroski paper returns a JavaScript client challenge'); "
        "no Beneish JSTOR attempt is reported in the lesson or the card's source. plans/AC2-open-items.md row for Beneish says 'JSTOR a bot check', which is not a recorded request. "
        "Every other L08 card re-verified (c106-c119, c129, c131-c133, c139, c140)."
    ),
}
LESSON_FAIL_FIX = {
    "L08": "Either state in L08.html section 2 the JSTOR request made for the Beneish record and its result, or delete the JSTOR clause from cards.json AC2-c107 back (keep the publisher, ResearchGate and SSRN 403s, which are re-observed). Re-run check_pages --unit AC2 after the edit.",
}

for lesson in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"):
    ids = lesson_ids(lesson)
    row = {
        "id": f"proj-r5-cards-{lesson}",
        "check": "2.7-cards",
        "location": f"course/modules/AC/AC2/cards.json ({len(ids)} cards: {', '.join(ids)}) vs course/modules/AC/AC2/{lesson}.html",
        "status": "FAIL" if lesson in LESSON_FAIL else "PASS",
        "evidence": (LESSON_FAIL[lesson] if lesson in LESSON_FAIL else LESSON_EVIDENCE[lesson]),
    }
    if lesson in LESSON_FAIL:
        row["fix"] = LESSON_FAIL_FIX[lesson]
    rows.append(row)

rows.append({
    "id": "proj-r4-cards-grades", "check": "2.7-cards", "location": "cards.json AC2-c058, AC2-c064; L04.html and L05.html claim spans",
    "status": "PASS",
    "evidence": ("Re-verified round 5 (round-4 FAIL fixed): cards.json AC2-c058 and AC2-c064 now carry \"grade\": \"C\" and \"basis\": \"Crossref abstract; passage locator not confirmed\", "
                 "the same grade and locator as data-grade=\"C\" data-cite=\"sloan1996stock\" data-locator=\"Crossref abstract; passage locator not confirmed\" in L04.html and L05.html (grep this round). "
                 "The card wording matches the lesson text (L04 Section 1, L05 Definition 1.1): no finding and no sample period quoted."),
})

rows.append({
    "id": "proj-r5-cards-count-schema", "check": "2.7-cards", "location": "course/modules/AC/AC2/cards.json (140 cards)",
    "status": "PASS",
    "evidence": ("140 cards, ids AC2-c001 to AC2-c140 contiguous; no duplicate fronts; lessons L01-L08 counts 17,18,17,16,15,17,20,20 (sum 140); "
                 "check_pages --unit AC2 PASS (grade/cite/basis rule and lesson coverage); every grade C or D card has a cite or a basis; "
                 "banned-word scan (about, roughly, approximately, around) hits only computed or quoted numbers (c022, c047, c070, c075, c113, c067, c068, c125) or non-numeric uses."),
})

rows.append({
    "id": "proj-r5-hub-placement", "check": "2.9-structure", "location": "course/modules/AC/AC2/index.html lines 66-133 (placement) and line 70",
    "status": "PASS",
    "evidence": ("Counted the placement items in the hub: four AC1 items (balance-sheet identity, articulation of net income, depreciation add-back, gross margin arithmetic) and two S0 items (median, MNAR) = six prerequisite items, plus three skill checks (rung 1 as-of, rung 2 leverage 0.20/(0.10x0.50)=4.0, rung 2 ROIC 150/1000) = nine items. "
                 "Bar 80% of nine = 7.2, so eight correct is the bar and seven is 77.8% (hub text says 78%: consistent). No placement item tests S2 and the hub says so (line 70). Rung wording matches project.html line 42."),
})

rows.append({
    "id": "proj-r5-hub-l05-card", "check": "2.9-structure", "location": "course/modules/AC/AC2/index.html line 148 (L05 card body, outside the ladder/placement text)",
    "status": "FAIL",
    "evidence": ("The L05 card body reads 'Accrual-sorted portfolios, the evidence from Sloan (1996), and a SIMULATED portfolio study'. "
                 "L05.html Definition 1.1 says: 'The lesson states no finding of that paper: no sample period, return level or spread is quoted from it'; Section 3 and Key results state no Sloan finding. "
                 "The card therefore presents Sloan's evidence as lesson content that the lesson says it does not contain."),
    "fix": "Change index.html line 148 body text to 'Accrual-sorted portfolios, the question Sloan (1996) asks, and a SIMULATED portfolio study with the honest-pending note for real data.' The card title may keep the name; re-run check_pages --unit AC2.",
})

rows.append({
    "id": "proj-r5-beneish-source-reread", "check": "2.1-source", "location": "L08.html section 2; references/references.json beneish1999detection; cards AC2-c107..c109",
    "status": "PASS",
    "evidence": ("Plain curl this round: https://en.wikipedia.org/wiki/Beneish_M-score HTTP 200 and its text gives M = -4.84 + 0.92 DSRI + 0.528 GMI + 0.404 AQI + 0.892 SGI + 0.115 DEPI - 0.172 SGAI + 4.679 TATA - 0.327 LVGI and threshold -1.78 citing 'Beneish 1999' with two other works, Scribd and ycharts references: matches L08 section 2 and is graded D/UNCONFIRMED there (ruling 1, not failed). "
                 "https://doi.org/10.2469/faj.v55.n5.2296 HTTP 302 to tandfonline.com; tandfonline 403, researchgate.net 403, papers.ssrn.com 403 (match the lesson). The Beneish JSTOR record was NOT probed by this verifier (no Beneish JSTOR URL is known from the registry); see proj-r5-cards-L08. "
                 "Registry: title 'The Detection of Earnings Manipulation', container Financial Analysts Journal, volume 55, issue 5, pages 24-36 (matches card AC2-c108)."),
})

new_mutants = []
mut_dir = CHECKOUT / "ledgers/AC2/mutants"
for path in sorted(mut_dir.glob("*.py")):
    import ast
    doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    new_mutants.append({"description": doc.splitlines()[0] if doc else "", "file": f"ledgers/AC2/mutants/{path.name}"})

rows.append({
    "id": "proj-r5-mutants-47", "check": "2.6-mutation", "location": "ledgers/AC2/mutants/ (47 files: m01-m05 round 4, p01-p37 builder, m06-m10 this round); tools/mutate_graders.py --unit AC2 --seeds 0-9",
    "status": "PASS",
    "evidence": "mutate_graders AC2: PASS (47/47 killed); output ledgers/AC2/scripts/project-r5/mutate_all_r5.txt. The previous survivors p14, p15, p16, p17, p18, p20, p21, p29, p35, p36, p37 are all KILLED in this run (e.g. p14 by test_money_tag_in_another_unit_is_not_read[shares], p17 by test_modified_jones_accepts_exactly_four_firm_years, p37 by test_same_filing_date_without_accn_and_different_values_raise).",
})

rows.append({
    "id": "proj-r5-mutants-new-m06-m10", "check": "2.6-mutation", "location": "ledgers/AC2/mutants/m06-m10 written by ledgers/AC2/scripts/project-r5/make_new_mutants_r5.py",
    "status": "PASS",
    "evidence": "Five NEW student-error mutants, one edit each from reference.py: m06 ROIC divides by year-end invested capital (killed by test_roic_number, seed 0); m07 accruals_cash_flow scaled by year-end total assets (test_accruals_cash_flow_number, seed 0); m08 Piotroski signal 3 scales last year's NI by last year's assets (test_piotroski_signals_match_the_definitions, seed 1); m09 Beneish TATA over average assets (test_beneish_variables_and_score_match_the_definitions, seed 0); m10 standardize keeps the earliest filing (test_standardize_matches_the_final_numbers, seed 0). All five killed.",
})

rows.append({
    "id": "proj-r5-impls-50", "check": "2.6-autograder", "location": "ledgers/AC2/scripts/project-r5/impls_0-49.txt; /tmp/verify-ac2-p/ledgers/AC2/scripts/project-r3/impls/V1-V5",
    "status": "PASS",
    "evidence": "Five alternative correct implementations (SVD 1e-8, SVD 1e-12, condition number 1e12, Cholesky pivot, strict bool-rejecting SVD 1e-10) each pass the AC2 suite on seeds 0-49: 50/50 seeds for every candidate (harness_r5.py). No over-constraint found.",
})

rows.append({
    "id": "proj-r5-run-graders-50", "check": "2.6-autograder", "location": "tools/run_graders.py --unit AC2 --seeds 0-49",
    "status": "PASS",
    "evidence": "run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s; the starter fails the suite; reference, instance and starter clean under mypy --strict per the run_graders typecheck). Output ledgers/AC2/scripts/project-r5/run_graders_0-49.txt.",
})

rows.append({
    "id": "proj-r5-collect-236", "check": "2.6-autograder", "location": "grader/test_project.py; pytest --collect-only on the reference (seeds 0, 1, 7, 12345)",
    "status": "PASS",
    "evidence": "collected=236 on every seed checked (ledgers/AC2/scripts/project-r5/collect_only_r5.py); project.html line 245 says 236 checks.",
})

rows.append({
    "id": "proj-r5-page-smoke", "check": "2.6-autograder", "location": "tools/page_smoke.py --unit AC2 --pages project",
    "status": "PASS",
    "evidence": "page_smoke modules/AC/AC2/project.html: PASS; 'in-browser grader: All 236 tests pass on seed 40402595'; labs lab-AC2-project-1/2/3 loaded (ledgers/AC2/scripts/project-r5/page_smoke_project.txt).",
})

rows.append({
    "id": "proj-r5-run-labs-and-gates", "check": "2.5-labs", "location": "tests/labs/AC2/lab-AC2-*.py; tools/run_labs --unit AC2; check_pages, check_projects, check_dag",
    "status": "PASS",
    "evidence": "run_labs AC2: PASS (11/11). Each twin run alone under python -I -W error: rc=0 for L01-L08 and project-1/2/3 (outputs in ledgers/AC2/scripts/project-r5/labs/). check_pages AC2 PASS; check_projects AC2 PASS; check_dag AC2 PASS. ruff check on grader and labs: All checks passed.",
})

rows.append({
    "id": "proj-r5-hub-ladder-text", "check": "2.9-structure", "location": "course/modules/AC/AC2/index.html lines 157-161; project.html lines 42 and 293",
    "status": "PASS",
    "evidence": "Re-read: hub 'The project ladder' (line 157) says a student skips rungs 1 and 2 only by reaching the placement bar and answering all three skill checks; project.html line 42 says the same and points to the hub; line 161 says instances are generated from the workspace seed. No cross-seed or every-seed claim. Consistent with the placement section (line 70).",
})

fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
pass_n = sum(r["status"] == "PASS" for r in rows)
fragment = {
    "unit": "AC2",
    "slice": "project",
    "round": 5,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 5; did not build AC2; fresh context)",
    "pin": "11b3477",
    "base": "round-4 fragment (pin 2607c60) read as context; its one FAIL (proj-r4-cards-grades) re-verified and PASS; its PASS rows carried by byte-identical subjects (git diff --quiet 2607c60 HEAD) and every command row re-run",
    "checkout": "/tmp/verify-ac2r5-p (detached at 11b3477)",
    "scratch": "/tmp/ac2-v/project-r5/",
    "verified_at": "2026-10-27",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": new_mutants,
    "registry_flags": R4["registry_flags"] + [
        "beneish1999detection: the registry holds title, journal, volume 55, issue 5, pages 24-36; the model's constants are UNCONFIRMED (Wikipedia, re-read by curl this round, is the only reproduction)."
    ],
    "freshness_flags": [],
    "notes": [
        "Round 5 delta for this slice: cards.json only (c058, c064 grade fixed; c103, c107, c119, c123, c130, c134 wording). project.html, index.html, grader/*, project labs, atlas and references are byte-identical since 2607c60.",
        "All 140 cards were checked against their lessons (grouped by lesson rows); numbers recomputed or matched to lab output (lab-AC2-L0x-1.out). Lessons were read as text (prose and lab prose).",
        "Not re-checked: the Beneish JSTOR record (no request made by this verifier); the Ivey-hosted Piotroski text was re-grepped for page-level locators only (pp. 1, 3, 6, 7, 8, 9, 11, 12 and footnotes 2 and 5 confirmed).",
        "Observation (not a FAIL): project.html line 241 uses ellipsis notation in return-shape descriptions, carried from round 4.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": pass_n,
        "fail": len(fail_ids),
        "unverifiable": 0,
        "fail_ids": fail_ids,
        "mutants": len(new_mutants),
        "mutants_killed": 47,
        "survivors": [],
        "sentence": (f"Round 5 project: 236 checks (collect on 4 seeds, reference 50/50, page_smoke 236 in-browser); 47/47 mutants killed (5 new, m06-m10); "
                     f"five alternative implementations 50/50 seeds; cards 140 checked against lessons, 2 FAIL rows (proj-r5-cards-L08 for c107 JSTOR attribution, proj-r5-hub-l05-card for the L05 hub body); "
                     f"proj-r4-cards-grades fixed and PASS."),
    },
}
out = CHECKOUT / "ledgers/AC2/project.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", pass_n, "fail", len(fail_ids), fail_ids)
