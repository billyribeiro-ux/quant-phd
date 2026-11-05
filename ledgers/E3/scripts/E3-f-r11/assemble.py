"""E3 slice f round 11: assemble and validate the fragment ledgers/E3/E3-f.json (run from the checkout root)."""
import json
import sys
from pathlib import Path

S = "ledgers/E3/scripts/E3-f-r11"
card_rows = json.loads(Path(f"{S}/card_rows.json").read_text(encoding="utf-8"))
SC = f"{S}/"

def P(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}

rows = list(card_rows) + [
    P("E3f-lesson-numbers-L01", "2.2-numbers", "course/modules/E/E3/L01.html (Example 1.4, Example 3.4, Misconceptions, M1, R3, quiz, Lab 1 prose)",
      f"Changed prose this round: Problem R3 solution (L01.html:455, outcomes 100 and 200 CU) and the quiz explanations. Re-derived in {SC}rederive_numbers.out: EV 15000/12500/15000 cents; quadratic EU 45000/21250/37500; R3 E u(X) = 25000 > E u(Y) = 22500; M1 EX 59, E u 4030. Quiz numerics 150, 4030, 30, 50 re-derived. No unrounded value is displayed differently."),
    P("E3f-lesson-numbers-L02", "2.2-numbers", "course/modules/E/E3/L02.html (Example 1.5, Example 2.3, Section 3 text, canon-breaks, misconceptions, M1-R3, E1-E3, quiz, key results)",
      f"Re-derived in {SC}rederive_numbers.out: E sqrt(W) 9.743416, CE 94.934165, premium 5.065835 (Example 1.5); r_A 0.005, r_R 0.5; approximation 4.5; error 0.565835; error share 0.11170 -> 11.17 percent (canon-breaks, E2); Part B premium/eps^2 5.065835, 4.619495, 4.528811, 4.504565, 4.500046 (E1 gap 0.004565 and factor 6.31 = 0.028811/0.004565; (0.25/0.1)^2 = 6.25); E3 cents 9493.4165 -> 9493 and 506.5835 -> 507. The changed sentences add no number."),
    P("E3f-lesson-numbers-L03", "2.2-numbers", "course/modules/E/E3/L03.html (Example 1.5, Example 2.5, Propositions 1.2-2.7, Remark 2.8, canon-breaks, misconceptions, M1-R3, E1-E3, quiz, key results)",
      f"Re-derived in {SC}rederive_numbers.out: CE values 11250, 10000, 10615.8009 (gamma 0.5), 10931.7733 (0.25), 8888.8889 (2), 7337.6161 (4); M = 9/80000 and CE_2 = 80000/9; Example 2.5 values 1600 and 2000; M2 3000 cents, M3 9000 cents; E3 bound (10+1)/2 = 5.5 cents; M1 r_A(4) = 1/8. Changed Example 1.5 and Proposition 2.7 text states no new number."),
    P("E3f-lesson-numbers-L04", "2.2-numbers", "course/modules/E/E3/L04.html (Lemma 1.2, Examples 1.7, 2.5, 2.6, Lemma 2.2, Theorem 2.3 proof, Problem R3, canon-breaks, misconceptions, M1-R3, quiz, key results)",
      f"Re-derived in {SC}rederive_numbers.out: I_X = (0,0,500,1000,2000) and I_Y = (0,250,500,1250,2000) at 2000..5000 (Example 2.5); F_X(2000)=1/2 > F_Y(2000)=1/4; F_Y(3000)=3/4 > F_X(3000)=1/2; Example 2.6 I_X(1000,3000,5000) = (0,1000,2000) and I_Y = (0,0,2000). Lab 1 counts (24 FOSD, 8 SOSD, 3 + 2 named, 37 agreements) match the printed output (L04.html:480-484) and the 10 and 2 no-ranking statements in canon-breaks."),
    P("E3f-coverage-cards", "2.7-cards-coverage", "course/modules/E/E3/L01.html-L04.html (labelled Definition, Proposition, Theorem, Lemma, Remark and Assumption blocks) vs cards.json slice",
      f"{SC}coverage_scan.py -> coverage_scan.out (a number-and-keyword scan, so a hit is a mention, not a judgement): every labelled block of L01-L04 is mentioned by a slice card except Example 3.4 (L01) and Example 1.5 (L02), which BUILDER_RULES 7 does not require. Definition, Proposition, Theorem, Lemma and Remark blocks each have a card whose back cites them (checked by reading, rows E3f-E3-cNNN)."),
    P("E3f-dag-L02-crra-forward-use", "2.9-define-before-use", "course/modules/E/E3/L02.html; L03.html; L04.html (concept links and forward references)",
      "ledgers/E3/scripts/E3-f-r11/check_dag.out: 'check_dag E3: PASS'. Grep of the four lessons: L02 links only L01 and concepts.html; L03 links L01/L02 and M1/M2/M4 concepts; no lesson links a later lesson. Changed sentences add no concept use."),
    P("E3f-dag-other-links", "2.9-define-before-use", "course/modules/E/E3/L01.html-L04.html (Uses and Introduces lines, concept links)",
      "Uses/Introduces meta rows (L01.html:36-39, L02.html:36-39, L03.html:36-39, L04 header) are unchanged since 47a36d8 (hunks in the delta touch prose only). check_dag PASS (check_dag.out)."),
    P("E3f-notation", "2.13-notation", "course/modules/E/E3/L01.html-L04.html vs notation/notation.json",
      (SC + "notation_scan.out: math commands used in the four lessons. Registered macros \\E, \\Prob, \\R, \\Var, \\indic all used as registered. Standard KaTeX commands (\\lfloor, \\rfloor, \\times, \\sum, \\frac, \\ln, \\exp, \\min, \\max, \\text) are not custom macros. Local letters alpha, eta, phi, kappa, xi, upsilon, chi, gamma (declared locally) are not registry symbols. Registry symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur. The letter a in card E3-c049 clashes with the lesson's exponent a, recorded in row E3f-E3-c049.")),
    P("E3f-banned-and-process", "1.3-1.4-banned", "course/modules/E/E3/L01.html-L04.html (visible prose)",
      "grep -n -i -E over L01-L04 for TODO, TBD, lorem, for brevity, omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, well known, obviously, clearly, it can be shown, ellipsis, builder, architect, verifier, ruling, round N, fixer, revised: no prose hit (only code type hints tuple[...]). Process words absent."),
    P("E3f-hours", "2.12-hours", "course/modules/E/E3/index.html:29,127; L01-L04 eyebrows and data-hours",
      "data-hours=\"7\" on L01-L04 (grep, round 11). index.html:29 data-hours-lessons=56, data-hours-project=14; eight lessons x 7 = 56; 56 + 14 = 70 equals the curriculum hours of E3 (curriculum/curriculum.json, E3 hours 70). index.html is byte-identical to 47a36d8."),
    P("E3f-references", "2.1-citations", "course/modules/E/E3/L02.html:616 (pratt1964risk); L01.html:564; L03.html:564; L04.html:717",
      "L02 names pratt1964risk only for the name; the registry record (references/references.json, pratt1964risk: Pratt, 'Risk Aversion in the Small and in the Large', Econometrica 32, 1964, DOI 10.2307/1913738, status verified) matches the citation string. references.json changed since the previous pin only for used_by entries of BK1/BK4 and E9/LX1; pratt1964risk is unchanged. verify_refs --offline: 560 entries, 0 problems (ledgers/E3/scripts/E3-f-r11/verify_refs_offline.out)."),
    P("E3f-L03-references", "2.1-citations", "course/modules/E/E3/L03.html:564",
      "L03 cites no registry key; the sentence names Module M1 results and Lab 1 (graded C), consistent with the references section. verify_refs --offline PASS."),
    P("E3f-cards-near-duplicates", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (full scan of 178 cards, slice cards involved)",
      f"{SC}check_cards_slice.py (token Jaccard, front >= 0.4 or front+back >= 0.5) lists pairs only where the questions differ: e.g. E3-c047/c180 (gamma 2 vs gamma 1 of the same lottery), E3-c067/c181 (integrated values of X vs Y), E3-c070/c183 (first vs second order), E3-c160/c171 (two different checks), E3-c174/c175 (A5 of L02 vs A2 of L03). None is a duplicate. The round-10 duplicate E3-c186 (of c020) is removed (see E3f-E3-c186)."),
    P("E3f-cards-slice-scan", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (90 slice cards, L01 18, L02 22, L03 26, L04 24)",
      "Slice card counts re-counted (check_cards_slice.py output): L01 18, L02 22, L03 26, L04 24 = 90 (round 10: 91, minus the removed E3-c186). All 90 cards are individually checked in rows E3f-E3-cNNN. Integrity over 178 cards: 178 unique ids, every lesson exists, no invalid grade (check_pages E3 PASS)."),
    P("E3f-cards-integrity", "2.7-cards-integrity", "course/modules/E/E3/cards.json (178 cards)",
      "check_pages.py --unit E3: PASS (includes cards.json checks: unique ids, lesson exists, grade valid, cite keys known, non-T grade has cite or basis). Per-lesson counts 18, 22, 26, 24, 22, 19, 19, 28 = 178."),
    P("E3f-cards-numbers", "2.2-numbers", "course/modules/E/E3/cards.json (slice cards) vs L01-L04",
      "check_cards_slice.py: every number in every slice card's front and back occurs in its lesson HTML (no output lines flagged), and each numeric result was re-derived (rederive_numbers.out)."),
    P("E3f-cards-xrefs", "2.7-cards", "course/modules/E/E3/cards.json (slice cards: Definition/Proposition/Remark/Problem/section cross-references)",
      "Every cross-reference in slice card backs resolves to an item of the named lesson (card_rows.json locations): e.g. c022 -> Proposition 1.3(a) L02.html:103; c053 -> Problem R3 L03.html (res-3); c052 -> L01 Proposition 3.3 L01.html:147; c077 -> Section 3 L04.html canon-breaks; c074 -> Section 4 third misconception L04.html:512. The one card whose symbols lag the lesson is E3-c049 (row E3f-E3-c049)."),
    P("E3f-cards-grades", "2.7-cards-grades", "course/modules/E/E3/cards.json (grade and basis, slice cards)",
      "Grades: T cards state Proposition, Lemma, Remark, Example (hand-computed) or Problem results that the lesson grades T (key results tables); C cards (c016, c017, c032-c035, c054, c073, c075, c076, c160, c161, c171) cite Lab 1 with the lesson's own grade C (lesson Key-results rows and labs); SIMULATED is named in the basis of c073, c075, c076. Every non-T grade has a basis. c034 is C for a derived arithmetic fact, conservative and not a defect."),
    P("E3f-delta", "0-delta", "git diff -U0 47a36d8c..ccaeeaf for the slice files",
      "Changed new-side lines since the round-10 pin 47a36d8c: L01.html lines 236, 453, 455, 508, 511; L02.html lines 51, 63, 94, 99, 106, 387, 434, 436, 445, 447, 609; L03.html lines 107, 174, 179, 393; L04.html lines 51, 98, 512; tests/labs/E3/lab-E3-L01-1.py line 73 (docstring); cards.json new-side lines 369 (E3-c055), 390 (E3-c058), 626 (E3-c094), 641 (E3-c096), 866 and 868 (E3-c131), 1129 (E3-c169), 1137 (E3-c170), 1226 (E3-c184), 1239-1244 (E3-c186 removed, E3-c187 added); references/references.json used_by entries only. Every changed hunk in L01-L04 was read in full; L02-L04 lab blocks and twins are byte-identical to 47a36d8 (script check)."),
    P("E3f-E3-r7-independent-rederivation", "2.2-numbers", f"{SC}rederive_numbers.py",
      "Independent Fraction and Decimal recomputation (rederive_numbers.out) of every lesson and card number listed in the four numbers rows, not using the lab code."),
    P("E3f-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit E3 (and --page L01)",
      f"{SC}check_pages_unit.out: 'check_pages E3: PASS', exit 0; check_pages_L01.out: 'check_pages E3 L01: PASS'."),
    P("E3f-cmd-check_dag", "2.9-define-before-use", "tools/check_dag.py --unit E3", f"{SC}check_dag.out: 'check_dag E3: PASS', exit 0."),
    P("E3f-cmd-check_projects", "2.6-projects", "tools/check_projects.py --unit E3 (project slice owns the content)", f"{SC}check_projects.out: 'check_projects E3: PASS', exit 0 (run as a gate, outside the lesson slice)."),
    P("E3f-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 (run alone)",
      f"{SC}page_smoke_L01-L04.out: each of L01-L04 PASS, lab lab-E3-L0n-1 runs in the in-page runtime, 'page_smoke E3: PASS', exit 0."),
    P("E3f-cmd-pytest-labs", "2.5-labs", "python -m pytest tests/test_labs.py -k E3 -q",
      f"{SC}pytest_labs_E3.out: 15 tests passed, exit 0."),
    P("E3f-cmd-ruff-labs", "2.5-labs", "ruff check and ruff format --check on tests/labs/E3/lab-E3-L01-1.py .. lab-E3-L04-1.py",
      f"{SC}ruff_check.out: 'All checks passed!' exit 0; ruff_format.out: '4 files already formatted' exit 0."),
    P("E3f-cmd-mypy-twins", "2.5-labs", "mypy --no-incremental on the four L01-L04 twins", f"{SC}mypy_twins.out: 'Success: no issues found in 4 source files', exit 0."),
    P("E3f-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline", f"{SC}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. The live run is the scheduled job, not run here (no network use)."),
    P("E3f-cmd-run_labs-L01-L04", "2.5-labs", "tools/run_labs.py --unit E3 --page L01 .. L04",
      f"{SC}run_labs_L01.out .. run_labs_L04.out: each 'run_labs E3: PASS (1/1)', exit 0."),
    P("E3f-banned-cards", "1.3-1.4-banned", "course/modules/E/E3/cards.json (slice cards)",
      "grep -i over cards.json for banned strings and process words, and a scan for '...' or the ellipsis character in front and back: no hit."),
    P("E3f-lab-L01", "2.5-labs", "course/modules/E/E3/L01.html lab block (lines 161-326); tests/labs/E3/lab-E3-L01-1.py",
      f"{SC}lab_twin_check.out: page code equals the twin (after html unescape); twin run alone with python -I -W error exits 0 with empty stderr; expected block equals the printed output (Parts A-D, lines 302-324). The changed docstring (page line 236, twin line 70) is identical in both. Hypothesis and interpretation claims (45000, 21250, 37500; six True comparisons; ValueError messages) match the output."),
    P("E3f-lab-L02", "2.5-labs", "course/modules/E/E3/L02.html lab block (lines 207-382); tests/labs/E3/lab-E3-L02-1.py",
      f"{SC}lab_twin_check.out: page code equals the twin; twin alone under -I -W error exit 0, empty stderr; expected block equals output. Lab block byte-identical to 47a36d8 (script). Interpretation numbers (4.500046, 0.565835, gaps shrink True, zero linear premium) match the output."),
    P("E3f-lab-L03", "2.5-labs", "course/modules/E/E3/L03.html lab block (lines 187-327); tests/labs/E3/lab-E3-L03-1.py",
      f"{SC}lab_twin_check.out: page code equals the twin; twin alone under -I -W error exit 0, empty stderr; expected block equals output (lines 307-325). Lab block byte-identical to 47a36d8. Hypothesis 80000/9 and 8888.89 -> 8889 and the interpretation's 10931.7733 match the output."),
    P("E3f-lab-L04", "2.5-labs", "course/modules/E/E3/L04.html lab block (lines 176-486); tests/labs/E3/lab-E3-L04-1.py",
      f"{SC}lab_twin_check.out: page code equals the twin; twin alone under -I -W error exit 0, empty stderr; expected block equals output (lines 440-484). Lab block byte-identical to 47a36d8. Verdict counts and the 37 agreements match the printed lines."),
]

frag = {
    "unit": "E3",
    "slice": "f",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-f, round 11 (did not build E3)",
    "pin": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "base": "47a36d8c78633793ccc762ae19dcd5e19b780d19 (round-10 pin; the round-10 fragment recorded pin 47a36d8c)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-E3-f",
    "scratch": "ledgers/E3/scripts/E3-f-r11/",
    "verified_at": "2026-11-05T14:20:00+00:00",
    "verdict": "",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice f is the lesson and card slice: cards of L01-L04 against the lessons. There is no project grader in this slice, so the mutation test and the five alternative implementations (plan 6.4, 6.5) do not apply; mutants is empty by design (project slices own them).",
        "The round-10 slice row set (126 rows) is kept: every row id is present. Rows whose subject changed this round (every card row, every lesson-numbers row, lab rows for L01) were re-verified from scratch. Lab blocks and twins of L02-L04 are byte-identical to 47a36d8, but their lab rows were re-run anyway.",
        "E3f-E3-c186 (round-10 FAIL) is resolved: the card is removed. Its replacement E3-c187 is in L07 and outside this slice.",
        "Not checked in this slice: project.html and grader/ (other slice); run_graders and mutate_graders (no project grader here); the live verify_refs run (network not used); the full text of cited published works (only registry records; no locator is quoted from them); L05-L08 cards (outside slice f); the Lab 1 simulated counts were not re-derived by an independent simulation (the lab's own printed output is the evidence, plus exact recomputation of the named pairs).",
        "Observation outside the card rows (not a row here, for the slice that owns L01): L01 quiz explanation for L01q4 calls x^2 'the nondecreasing u given by x^2', which is nondecreasing only on the nonnegative outcomes used in Example 1.4. Harmless, but the lesson could say 'on nonnegative outcomes'.",
        "Observation: card E3-c034 grades an arithmetic consequence of Lab 1 as C; conservative, not a defect.",
    ],
    "summary": "",
}
fails = [r for r in rows if r["status"] != "PASS"]
passes = [r for r in rows if r["status"] == "PASS"]
frag["verdict"] = "PASS" if not fails else "FAIL"
frag["summary"] = (f"Slice f round 11 at ccaeeaf: {len(rows)} rows: {len(passes)} PASS, {len(fails)} FAIL, 0 UNVERIFIABLE. "
                   f"FAIL: {', '.join(r['id'] for r in fails)} (card E3-c049 back uses the letter a, which the lesson now uses for the power exponent; the lesson re-lettered Proposition 2.7 to phi and eta this round). "
                   "All 90 slice cards were re-read against the current lessons; the round-10 FAIL on the removed card E3-c186 is resolved; the duplicate scan is clean; every command gate PASS.")
out = Path("ledgers/E3/E3-f.json")
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("written", out, len(rows), "rows", len(fails), "fail")
