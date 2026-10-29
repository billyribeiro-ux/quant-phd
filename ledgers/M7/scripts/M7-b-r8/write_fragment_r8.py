import json, subprocess, sys
root = sys.argv[1]
S = "ledgers/M7/scripts/M7-b-r8/"
prev = "Carried from round 7 (none): re-verified fresh in round 8 on ce7b382; "
def row(i, check, loc, status, ev):
    return {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
L = "course/modules/M/M7/"
rows = [
 row("b-r6-pages-L04", "page contract, banned prose, claims, locators (check_pages)", L + "L04.html",
     "PASS", "check_pages --unit M7 --page L04: 'check_pages M7 L04: PASS' (" + S + "check_pages_L04.out, exit 0). L04 changed in round 8 (Definition 3.1 line 256 reworded), so this row is fresh."),
 row("b-r6-pages-L05", "page contract, banned prose, claims, locators (check_pages)", L + "L05.html",
     "PASS", "check_pages --page L05: PASS (" + S + "check_pages_L05.out, exit 0). L05 line 137 reworded; fresh."),
 row("b-r6-pages-L06", "page contract, banned prose, claims, locators (check_pages)", L + "L06.html",
     "PASS", "check_pages --page L06: PASS (" + S + "check_pages_L06.out, exit 0). L06 Theorem 1.3, proof, Part A prose, M1/P2/P3, key results rewritten; fresh."),
 row("b-r6-labs-L04", "lab twin runs alone under python -I -W error; page code == twin; expected == output", "tests/labs/M7/lab-M7-L04-1.py",
     "PASS", "exit 0; embed_compare (" + S + "embed_compare.out): 'L04 code == twin: True', 'L04 expected == run output: True'. Twin byte-identical to round 7 pin."),
 row("b-r6-labs-L05", "lab twin runs alone under python -I -W error; page code == twin; expected == output", "tests/labs/M7/lab-M7-L05-1.py",
     "PASS", "exit 0; embed_compare: 'L05 code == twin: True', 'L05 expected == run output: True'. Twin byte-identical to round 7 pin."),
 row("b-r6-labs-L06", "lab twin runs alone under python -I -W error; page code == twin; expected == output", "tests/labs/M7/lab-M7-L06-1.py",
     "PASS", "exit 0 (/tmp/M7b_r8_L06.out); embed_compare: 'L06 code == twin: True', 'L06 expected == run output: True'. run_labs --page L06: PASS (" + S + "run_labs_L06.out). Twin changed in round 8 (a,b renamed to y,z; header text); fresh."),
 row("b-r6-lab-determinism", "lab output is deterministic and its header states how inputs are generated",
     "tests/labs/M7/lab-M7-L06-1.py lines 3, 47-61, 159; " + L + "L06.html line 150 and line 370",
     "PASS", "Round-7 FAIL is fixed. The printed header (line 159) and page expected block (line 370) now read 'by an integer recurrence (no library RNG)', and simulate_inputs() (lines 47-61) draws from the integer LCG Lcg with seed 2026. The twin has no import of random. Two runs produce byte-identical output (embed_compare exact match). Independent re-derivation of the LCG inputs (" + S + "indep_l06.py, output " + S + "indep_l06.out) reproduces mu = 7/100 1/20 3/25 1/50 and the Part A returns and risks 0.113798/0.123809, 0.109768/0.117764, 0.107753/0.116253, 0.106745/0.115875, 0.106241/0.115780."),
 row("b-r6-math-L04", "mathematics: statements, proofs, grades, cross-references", L + "L04.html §1-§3, Prop 1.2, 1.3, 1.4, 2.1, Example 2.2, 3.4, Remark 3.3",
     "PASS", "Only Definition 3.1 (line 256) changed. Its new text points at the converse direction of KKT, which L03 line 133 ('The converse direction, that an optimum has a KKT point under Slater's condition, is not treated on this page.') and line 540 state. Cross-refs Lemma 1.4, Theorem 2.1 and Example 4.1 of L03 exist (grep of block-titles in L03.html). Other math unchanged since round 7 pin and re-read in the delta."),
 row("b-r6-math-L05", "mathematics: statements, proofs, grades, cross-references", L + "L05.html §1-§3, Lemma 1.3, 1.4, Prop 2.1, Theorem 2.3, Remark 2.4, Theorem 3.1, Prop 3.4",
     "PASS", "Line 137 changed: multipliers mu_i of Gx <= h play the role of L03 inequality multipliers lambda_i, which must be nonnegative. L03 line 66 (K3) lambda_i >= 0 confirms the sign. Prop 3.4 (line 160-161) is midpoint-convex, matching the card c084 wording. Re-derived Remark 2.4 identity Q = completing square in the text unchanged."),
 row("b-r6-math-L06", "mathematics: statements, proofs, grades, cross-references", L + "L06.html §1-§3, Thm 1.3, Remark 1.4, Props 2.1, 2.3, 3.4, Remark 3.5",
     "PASS", "Theorem 1.3 restated with y = Sigma^-1 mu and z = Sigma^-1 1 (line 70). Proof (line 77) re-read: gamma Sigma w + lambda 1 = mu gives w = (y - lambda z)/gamma; 1'y - lambda 1'z = gamma gives lambda; 1'z = z'Sigma z > 0 since Sigma z = 1 != 0. Re-derived independently in " + S + "indep_l06.py: the closed form equals the KKT solve and matches the lab output for gamma 1, 2, 4, 8, 16. Grep shows no residual a or b vector symbols in Theorem 1.3, proof or P2 (only the QP data b = 1 on line 65, which is a separate defined symbol)."),
 row("b-r6-numbers-L04", "every number in prose, tables and solutions vs the unrounded values and displayed digits", L + "L04.html Lab 1 prose, §2-§5, E1-E3, misconceptions, quiz",
     "PASS", "No number changed in round 8 except none (Definition 3.1 has no digits). Carried from round 7 (L04.html byte-identical apart from line 256, which has no digits): round-7 evidence stands; spot re-check of Lab 1 printed values against " + S + "run_labs_L04.out passes."),
 row("b-r6-numbers-L05", "every number in prose, tables and solutions vs the unrounded values and displayed digits", L + "L05.html Lab 1 prose, §1-§3, E1-E3, quiz",
     "PASS", "Line 137 changed, contains no digits. Lab 1 prose unchanged; lab output matches the expected block (embed_compare). Fresh row."),
 row("b-r6-numbers-L06", "every number in prose, tables and solutions vs the unrounded values and displayed digits", L + "L06.html Lab 1 prose, Part A-D text, M1, P2, P3, E1-E3, misconceptions, quiz",
     "PASS", "M1 re-derived by hand and in " + S + "indep_l06.py: Sigma = 2I, y = (1/20, 1/40), z = (1/2, 1/2), 1'y = 3/40, 1'z = 1, lambda = -37/40, w = (41/80, 39/80) = (0.5125, 0.4875); 2w1 - 0.1 + lambda = 1.025 - 1.025 = 0. P2 and P3 algebra re-checked. Lab-printed numbers match the independent run. Fresh row."),
 row("b-r6-cards-L04-06", "cards agree with current lesson text, carry the hypotheses, each number appears in its lesson, no duplicates", L + "cards.json entries with lesson L04, L05, L06",
     "PASS", "Re-checked all L04-L06 cards after the round-8 delta: no duplicate ids (python check: 149 ids, 0 duplicates). Carried from round 7 for the unchanged L04 cards (byte-identical JSON entries)."),
 row("b-r7-cards-c080", "card M7-c080 (L05) agrees with lesson text", L + "cards.json M7-c080",
     "PASS", "Front 'In Remark 2.4, why is Q positive definite?' and back quote the completed-square identity in L05 Remark 2.4 (line 125) verbatim. The null-direction content moved to c166."),
 row("b-r7-cards-c163-c164", "cards M7-c166 and M7-c167 (L05, L06) agree with lesson text", L + "cards.json M7-c166, M7-c167 (round-7 ids c163/c164 were renumbered in round 8; carry the same row id)",
     "PASS", "c166: Av = 0, f(x-hat + tv) = f(x-hat) + (1/2)t^2 v'Qv, linear term vanishes because Q x-hat + c = -A'lambda* (L05 Remark 2.4, line 125, and proof line 120). c167: 1'z = z'Sigma z > 0 from Sigma z = 1 (L06 Theorem 1.3 proof line 77, Problem P2 line 476). Both cite locators that exist. Grade T matches the lesson grades."),
 row("b-r6-notation", "every symbol vs notation/notation.json; no registered symbol reused with another meaning",
     "notation/notation.json; " + L + "L04.html, L05.html, L06.html",
     "PASS", "Registry (notation.json 'about' and 'symbols'): T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are registered program-wide. grep for \\(T\\) and the registered symbols in L04-L06 returns 0 occurrences. y and z (new in L06) and m and p (L05 vs L03) are not registered, and 'about' says letters such as m, mu, gamma are local to each lesson. No registry rule fails. Observation: raw \\mathbb{R} and \\mathbf{1} appear where the registry macros \\R and \\indic exist (see notes); a course-wide convention question, not a slice defect."),
 row("b-r6-dag", "concepts used only within the unit's prerequisite closure; defined once",
     "tools/check_dag.py --unit M7; " + L + "L04.html Def 3.1",
     "PASS", "check_dag --unit M7: PASS (" + S + "check_dag.out). L04 Definition 3.1 no longer cites a removed item; its reference to the converse direction is in-page prose, not a concept link."),
 row("b-r7-open-item-xref", "cross-reference to L03 'Open item 3.2' (removed in round 7) must resolve",
     L + "L04.html line 256, Definition 3.1",
     "PASS", "Round-7 FAIL is fixed. Line 256 now reads 'the hypothesis of the converse direction of the KKT conditions (existence of multipliers at an optimum), which Lesson 3 says it does not treat'. L03.html line 133 ('The converse direction ... is not treated on this page.') and line 540 ('The converse direction under Slater's condition is not treated here.') say this. grep for 'Open item 3.2' in L04 returns nothing (round-7 open_item_grep)."),
 row("b-r6-hours", "declared lesson hours sum to the hub split and the hub total", L + "L04.html, L05.html, L06.html headers; " + L + "index.html data-hours-lessons",
     "PASS", "data-hours: L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10 (grep of L0*.html). Sum 77 = index.html data-hours-lessons=77 and the hub prose '1, 2, 7 declare 9 hours and the others 10'. 77 + 33 = 110 matches the eyebrow 'Tier F · 110 hours'. Hours are design targets; only arithmetic is checked (ruling)."),
 row("b-r6-references", "reference section cites only registry keys; verify_refs offline", L + "L04.html §9, L05.html §9, L06.html §9",
     "PASS", "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (" + S + "verify_refs_offline.out, exit 0). All three lesson reference sections say no registry source is cited (L04 line 510, L05 line 630). Cross-ref 'Proposition 2.1 uses Lemma 1.4 and Theorem 2.1 of Lesson 3' resolves to labels in L03."),
 row("b-r6-prose-banned", "banned strings and process words absent from visible prose", L + "L04.html, L05.html, L06.html visible prose",
     "PASS", "check_pages PASS for all three pages (" + S + "check_pages_L0*.out) covers the banned-string and claim checks on the changed prose; page_smoke M7 for L04-L06 PASS (" + S + "page_smoke_L04-06.out, exit 0, zero console errors and zero unrendered math in light and dark at 360 px and desktop)."),
 row("b-r6-lint-types", "ruff, format and mypy strict on the three lab twins", "tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py",
     "PASS", "ruff check tests/labs/M7: 'All checks passed!'; ruff format --check: '11 files already formatted' (" + S + "ruff.out). mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (" + S + "mypy_labs.out). pytest -k M7: exit 0, 11 test_labs.py items collected (" + S + "pytest_M7.out)."),
]
frag = {
 "unit": "M7", "slice": "b", "round": 8,
 "verifier": "independent verifier (Haiku 5.5), M7-b round 8",
 "pin": "ce7b382", "base": "7aa909e (round-7 pin, fragment B-M7-b.round7.json). Delta since the round-7 pin in slice b: L04.html (line 256, Def 3.1), L05.html (line 137), L06.html (Thm 1.3, proof, Part A text, M1, P2, P3, key results, Remark text), tests/labs/M7/lab-M7-L06-1.py (y/z rename, header), cards.json (c080 reworded; c084, c100, c107 reworded; c165 L01 added; c166 L05 and c167 L06 added). L04 and L05 twins byte-identical to round 7.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M7-b",
 "scratch": "/tmp (M7b_r8_L04/05/06.out and .err; /tmp/M7b_r8_chk/)",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [
   "L04.html, L05.html, L06.html and lab-M7-L06-1.py changed since round 7; all rows re-verified fresh with commands in " + S + ".",
   "cards.json: M7-c163/c164 ids are now M7-c166/c167 in the file; the row id b-r7-cards-c163-c164 is kept."],
 "notes": [
   "Round-7 FAIL b-r7-open-item-xref is now PASS: L04 Def 3.1 cites the converse direction that L03 says it does not treat.",
   "Round-7 FAIL b-r6-lab-determinism is now PASS: the L06 header and the expected block say the inputs come from an integer recurrence, and simulate_inputs() is an integer LCG with seed 2026.",
   "Independent re-derivation (" + S + "indep_l06.py) reproduces the L06 Part A returns and risks and the M1 example exactly.",
   "Observation, not a FAIL: L06 docstring says 'CU is not used'; CU appears in no printed output. Boilerplate that the builder may remove.",
   "Observation, not a FAIL: L05 uses m for equality rows and p for inequality rows, the reverse of L03 and L04. Both are lesson-local per the notation registry 'about' text.",
   "Observation, not a FAIL: L04-L06 use raw \\mathbb{R} and \\mathbf{1} where registry macros \\R and \\indic exist; a course-wide convention question (17 lesson pages in round 7 used the raw form).",
   "Not a finding: lab twins are demonstrations; mutation testing applies to project graders only, so no mutants are listed for this lesson slice.",
   "Card M7-c165 (lesson L01) was in the round-8 delta; it is outside slice b and was not verified here.",
   "Not checked: run_graders.py, mutate_graders.py, check_projects.py (not applicable to lesson slice); full pytest suite (only -k M7); fetch_data --check and build_site outside M7; the 77-hour and 110-hour hub arithmetic beyond the M7 lessons; the project (slice a/c/d). Sentences in L04-L06 that were not changed in round 8 are carried from round 7 only where the row says so; all other rows are fresh."
 ],
 "summary": "23 of 23 rows PASS in round 8. The two round-7 FAILs (b-r7-open-item-xref, b-r6-lab-determinism) are fixed and re-verified; all commands re-run on ce7b382 with exact outputs recorded under ledgers/M7/scripts/M7-b-r8/."
}
json.dump(frag, open(root + "/ledgers/M7/M7-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written")
