"""Build ledgers/E5/E5-d.json (round 1, pin 95f3f8cb) from the round-5 base fragment plus this round's re-verification."""
import json, subprocess, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF11-E5-d"
BASE = "/Users/billyribeiro/.fanout/frags/C-E5-d.round5.json"
base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}
CARRY = "Carried from round 5 (%s byte-identical since the previous pin): "

def carry(rid, files):
    r = dict(base_rows[rid])
    r["evidence"] = CARRY % files + r["evidence"]
    return r

def row(rid, check, location, status, evidence, fix=None):
    r = dict(base_rows[rid]) if rid in base_rows else {"id": rid}
    r.update({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})
    if status != "PASS":
        r["fix"] = fix
    elif "fix" in r:
        del r["fix"]
    return r

P = "course/modules/E/E5/project.html"
OUT = "ledgers/E5/scripts/E5-d-r1/out/"
rows = []
A = rows.append

# ---- re-verified rows (subject changed, or non-PASS base row, or gate) ----
A(row("proj-lab2-gap-survivor", base_rows["proj-lab2-gap-survivor"]["check"],
      "project.html ladder item 2 (Rung 2), Lab 2 hypothesis and interpretation; tests/labs/E5/lab-E5-project-2.py",
      "PASS",
      "Re-verified on 95f3f8cb. " + OUT + "standing_mutants.out: r4_m05_gap_percent_of_trend and m02_gap_percent_of_trend "
      "PASS the page's instant check (compare_output, tol 1e-6). ledgers/E5/scripts/E5-d-r1/lab2_gap_check.py recomputes the "
      "log gap -0.183842 and the percent-of-trend gap -0.183673; both print -0.18 at two decimals, as the twin prints. "
      "project.html line 45 says the check does not separate the two gaps and that the check is instant. The sentence is accurate."))
A(row("cards-c050-basis-fact-4-1", base_rows["cards-c050-basis-fact-4-1"]["check"],
      "cards.json E5-c050 basis; course/modules/E/E5/L03.html Assumption 4.1 block and Proposition 4.2",
      "PASS",
      "cards.json E5-c050 basis is now 'Proposition 4.2 (by Assumption 4.1)' (changed in the delta). L03.html contains "
      "'Assumption 4.1 (implicit-function theorem, used without proof)' and Proposition 4.2 cites it; grep -c 'Fact 4.1' L03.html = 0."))
A(row("cards-c095-holding-condition", base_rows["cards-c095-holding-condition"]["check"],
      "cards.json E5-c095 basis; course/modules/E/E5/L06.html Proposition 2.1 and the units sentence",
      "PASS",
      "cards.json E5-c095 basis is now 'Proposition 2.1' (back unchanged). L06.html Proposition 2.1 now reads 'Holding P_{t-1} and "
      "pi^e_t fixed, the inflation rate falls by beta_t for each rise of one unit in u_t, which is a rise of 100 percentage points', "
      "which the back's units statement matches."))
A(row("proj-honest-pending", base_rows["proj-honest-pending"]["check"],
      P + " section#data p.honest-pending (line 343); plans/E5-open-items.md DATA_REQUESTS",
      "PASS",
      "project.html line 343 says the request for a redistributable source is recorded in the DATA_REQUEST entry of "
      "plans/E5-open-items.md. That file now has a '## DATA_REQUESTS' section (lines 6-13) requesting real GDP, a price index, an "
      "unemployment rate and a policy rate, with the bring-your-own-CSV note. The learner text matches it."))
A(row("cmd-check-projects", base_rows["cmd-check-projects"]["check"], "tools/check_projects.py --all", "PASS",
      "Run on 95f3f8cb: 'check_projects E5: PASS', exit 0 (" + OUT + "check_projects.out)."))
A(row("cmd-check-dag", base_rows["cmd-check-dag"]["check"], "tools/check_dag.py --all", "PASS",
      "Run on 95f3f8cb: 'check_dag E5: PASS', exit 0 (" + OUT + "check_dag.out)."))
A(row("cmd-check-pages", base_rows["cmd-check-pages"]["check"], "tools/check_pages.py --all", "PASS",
      "Run on 95f3f8cb: 'check_pages E5: PASS', exit 0 (" + OUT + "check_pages.out)."))
A(row("cmd-run-labs", base_rows["cmd-run-labs"]["check"], "tools/run_labs.py --unit E5", "PASS",
      "Run on 95f3f8cb: 'run_labs E5: PASS (11/11)', exit 0. Covers twin == page code and page expected == twin stdout for "
      "L01-L08 and the three project labs (" + OUT + "run_labs_E5.out)."))
A(row("cmd-page-smoke-project", base_rows["cmd-page-smoke-project"]["check"],
      "tools/page_smoke.py --unit E5 --pages L02 L03 L04 L05 L06 project", "PASS",
      "Run on 95f3f8cb (Chromium, light/dark, 360 px): every named page PASS, 'page_smoke E5: PASS', exit 0 "
      "(" + OUT + "page_smoke_changed_and_project.out)."))
A(row("cmd-pytest", base_rows["cmd-pytest"]["check"], "pytest tests/test_labs.py -k E5; pytest tests/test_page_checks.py", "PASS",
      "Run on 95f3f8cb: test_labs -k E5 exit 0 (11 tests), test_page_checks exit 0 (41 tests) (" + OUT + "pytest_*.out)."))
A(row("cmd-verify-refs", base_rows["cmd-verify-refs"]["check"], "tools/verify_refs.py --offline; tools/verify_refs.py --unit E5", "PASS",
      "Run on 95f3f8cb: 'offline integrity: 560 entries, 0 problems' exit 0; 'live re-verification of E5: 4 of 560 entries, 0 problems' exit 0 (" + OUT + "verify_refs_*.out)."))
A(row("proj-hours", base_rows["proj-hours"]["check"],
      P + " #hours-table; data-hours-project=30 (line 33); course/modules/E/E5/index.html data-hours-lessons=80, data-hours-project=30, eyebrow '110 hours'",
      "PASS",
      "index.html (changed in delta) line 29 data-hours-lessons=\"80\" and data-hours-project=\"30\"; line 31 eyebrow '110 hours' = 80 + 30; "
      "the eight lesson eyebrows L01-L08 each read '10 study hours' (8 x 10 = 80); project.html line 33 data-hours-project=\"30\"."))
A(row("proj-adversarial-and-mutants", base_rows["proj-adversarial-and-mutants"]["check"],
      P + " #spec Grading mode; course/modules/E/E5 and tests/labs/E5 grep", "PASS",
      "grep -i grader over course/modules/E/E5/*.html, tests/labs/E5/*.py and tests/test_labs.py: no matches. "
      "tools/mutate_graders.py --unit E5 exits 0 with no output (" + OUT + "mutate_graders_E5.out): E5 has no grader (rubric-only project)."))
A(row("proj-notation", base_rows["proj-notation"]["check"], P + " LaTeX spans; notation/notation.json", "PASS",
      "notation/notation.json unchanged in the delta. Token scan of every \\(...\\)/\\[...\\] span in E5 pages (changed lessons included) "
      "finds no use of registered T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\E or \\mathbb{R}. "
      "L06 writes expected inflation as \\pi^{e}_t (32 uses, 0 uses of \\E). The R_t of L01 Proposition 2.6 is unregistered."))
A(row("proj-dag", base_rows["proj-dag"]["check"], P + " (no data-concept link); tools/check_dag.py --all", "PASS",
      "check_dag --all: 'check_dag E5: PASS', exit 0 on 95f3f8cb (" + OUT + "check_dag.out)."))
A(row("proj-reading-list", base_rows["proj-reading-list"]["check"], P + " #reading; references/references.json", "PASS",
      "The four cited keys (solow1956contribution, hicks1937mr, phelps1968money, blanchard2020macroeconomics) have byte-identical records "
      "in references.json at 04626e9 and HEAD (python comparison of the entries). The file's delta is generated_at and module lists only. "
      "verify_refs --offline and --unit E5 PASS."))
A(row("proj-process-words", base_rows["proj-process-words"]["check"], P + " whole page; tools/check_pages.py banned strings", "PASS",
      "check_pages --all PASS on 95f3f8cb (banned strings). A scan of E5 learner text for process words (revised, round, fixer, architect, "
      "verifier, builder, ruling, slice, open item, planning) finds only the 'not yet released' status of P0.1 (which is not built)."))
A(row("cards-scope-and-duplicates", base_rows["cards-scope-and-duplicates"]["check"], "course/modules/E/E5/cards.json", "PASS",
      "139 cards; ids unique and sorted; no duplicate fronts or backs; lessons L01 23, L02 13, L03 17, L04 19, L05 20, L06 19, L07 14, "
      "L08 14. Id E5-c135 is absent (a gap; ruling 2 says gaps are not defects). 88 cards changed and 9 added (c131-c134, c136-c140)."))
A(row("cards-numbers-in-lesson", base_rows["cards-numbers-in-lesson"]["check"], "cards.json; course/modules/E/E5/L01-L08.html", "PASS",
      "Every numeral token (decimals and fractions) in each card's front and back occurs in its cited lesson's text (0 misses over 139 cards). "
      "card_numbers.py: 'checked 139 cards; unmatched numeric tokens: 0' (" + OUT + "card_numbers.out)."))
A(row("cards-sample-2", base_rows["cards-sample-2"]["check"], "cards.json E5-c020; L01 Proposition 2.6 and misconception 4", "PASS",
      "E5-c020 (changed: 'Lab 1's SIMULATED example'): nominal growth 105/995 = 0.105528, deflator 4/23 = 0.173913, real growth "
      "-0.058254 (twin output line 'simple growth over periods 0 to 1: nominal 0.105528; real -0.058254'). Lesson says the same."))
A(row("cards-sample-3", base_rows["cards-sample-3"]["check"], "cards.json E5-c030; L02 Definition 2.2", "PASS",
      "E5-c030 (changed front): 'What is total factor productivity (TFP)?' Back 'The level A of Definition 1.1 ... (Definition 2.2)'. L02 Definition 2.2 says TFP is the level A of Definition 1.1."))
A(row("cards-sample-4", base_rows["cards-sample-4"]["check"], "cards.json E5-c040; L03 Remark 2.3", "PASS",
      "E5-c040 (basis changed): g(0)=0 by A1, zero is a fixed point, A4 excludes it (L03 Remark 2.3, unchanged)."))
A(row("cards-sample-5", base_rows["cards-sample-5"]["check"], "cards.json E5-c050; L03 Proposition 4.2 and Assumption 4.1", "PASS",
      "See cards-c050-basis-fact-4-1: basis cites Proposition 4.2 (by Assumption 4.1), which L03 states."))
A(row("cards-sample-6", base_rows["cards-sample-6"]["check"], "cards.json E5-c060; L04 Definition 3.1", "PASS",
      "E5-c060 (back changed): 'In this lesson the word has that sense (Definition 3.1)'. L04 Definition 3.1 defines equilibrium as a pair satisfying both relations."))
A(row("cards-sample-7", base_rows["cards-sample-7"]["check"], "cards.json E5-c070; L04 Proposition 3.2 and Remark 1.2", "PASS",
      "E5-c070: 'Under A1 to A4, Proposition 3.2 gives exactly one equilibrium ... that satisfies A2'. Matches L04 Proposition 3.2 and the changed A3/A4 text."))
A(row("cards-sample-8", base_rows["cards-sample-8"]["check"], "cards.json E5-c080; L05 Proposition 2.2", "PASS",
      "E5-c080 (back changed): hypotheses 'A1 and A2 (a, eta, nu > 0; P^e given)' and the formulas match L05 Proposition 2.2 (exact; output share strictly between 0 and 1)."))
A(row("cards-sample-9", base_rows["cards-sample-9"]["check"], "cards.json E5-c090; L06 section 1", "PASS",
      "E5-c090 (front changed): 'pi(t) = (P(t) - P(t-1))/P(t-1), annual rate, 0.03 is 3 percent' matches L06 section 1 (unchanged definition)."))
A(row("cards-sample-10", base_rows["cards-sample-10"]["check"], "cards.json E5-c100; L06 Definition 1.2; Lab 1 Part C", "PASS",
      "E5-c100: at 3 percent the change is 0.016667 (twin: 'unemployment 3.000000 percent change 0.016667'), exactly 1/60 = (5/6)(0.02); L06 section 5 says the same."))
A(row("cards-sample-11", base_rows["cards-sample-11"]["check"], "cards.json E5-c110; L07 Definition 1.4", "PASS",
      "E5-c110: rule as in L07 Definition 1.4 and 'No estimate of phi_pi, phi_y or r^n is given (Definition 1.4)', which the lesson says."))
A(row("cards-sample-13", base_rows["cards-sample-13"]["check"], "cards.json E5-c130; L08 page statement", "PASS",
      "E5-c130 (back changed): 'a property of the model under A1 to A3 (Proposition 2.2)'; L08 Assumptions block is 'for Propositions 2.1 to 2.4' with A1-A3."))
A(row("cards-derivations", base_rows["cards-derivations"]["check"],
      "cards.json E5-c014, c022, c035, c051, c052, c062, c064, c065, c079, c080, c099, c102, c122-c125, c128, c129", "PASS",
      "Re-derived: c014 and c018 (basket A 5/4 vs 27/23; basket B 11/10 vs 19/10, gap -4/5); c022 (7/92); c035 (1.1^0.3 = 1.029006, 0.3 ln 1.1 = 0.028593); "
      "c051 (10/7 = 1.4285714); c062, c064, c065 (Propositions 3.2, 4.2, 4.3; h/D <= 1/(1-c) iff bd >= 0); c079, c080 (Propositions 2.1, 2.2); "
      "c099 (-beta(u-un) with beta 5/6, gap -0.01 gives +1/120); c102 (13/600 = 0.021667; 1.226); c122-c125 (geometric sum; Bernoulli bound "
      "c^N <= 1/(1+N(1/c-1)) holds); c128, c129 (25,000 cents; -15,000 cents = -c/(1-c) x 10,000). All match the twin output."))
A(row("cards-lab-numbers", base_rows["cards-lab-numbers"]["check"],
      "cards.json c019-c021, c033-c034, c036, c048, c051-c052, c067-c069, c082-c087, c100-c104, c113-c117, c127-c129", "FAIL",
      "Every printed value cited by these cards matches the twin output of this round (" + OUT + "twin_lab-E5-L0*-1.out): e.g. 0.223144, 0.026856, "
      "160/20/180, 692 (recomputed independently with Decimal at 60 digits), 1.6752934513, 0.016667, 25000, -15000. "
      "The failing card is E5-c034: it says 'the residual is a different number for each alpha', which omits Proposition 2.4's hypothesis. See cards-c034-missing-hypothesis.",
      "Fix cards-c034 (see its row); the other cited numbers need no change."))
A(row("cmd-ruff-mypy", base_rows["cmd-ruff-mypy"]["check"], "tests/labs/E5/lab-E5-project-1..3.py, lab-E5-L04-1..L06-1 (twins)", "PASS",
      "ruff check tests/labs/E5 tests/test_labs.py: 'All checks passed!'; ruff format --check tests/labs/E5: 11 files already formatted; "
      "mypy --no-incremental tests/labs/E5: 'Success: no issues found in 11 source files' (" + OUT + "ruff_*_E5.out, mypy_E5.out)."))
A(row("proj-lab2-student-errors", base_rows["proj-lab2-student-errors"]["check"],
      "tests/labs/E5/lab-E5-project-2.py; ledgers/E5/mutants/project-2*/ (all)", "PASS",
      "Re-run of all 21 standing lab-2 files (" + OUT + "standing_mutants.out): 14 killed by the page's instant check, including the three r5 files "
      "(r5_m01, r5_m02, r5_m03). The two documented survivors (r4_m05, m02, percent-of-trend gap) are recorded in mutants with killed_by empty; "
      "project.html line 45 documents them. The alternatives alt01-03 (project-2/alt) and alt01-02 (project-2-r4) PASS, as they must. "
      "No new mutants were authored (ruling 37)."))
A(row("cmd-build-site", base_rows["cmd-build-site"]["check"], "tools/build_site.py --check", "PASS",
      "'site data current: 6 outputs', exit 0 on 95f3f8cb (" + OUT + "build_site_check.out)."))
A(row("cmd-render-curriculum", base_rows["cmd-render-curriculum"]["check"], "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "PASS",
      "render_curriculum.py exit 0 ('wrote ...'); git diff --exit-code on CURRICULUM.md and curriculum/curriculum.json is clean, so the committed outputs are current."))
A(row("cmd-fetch-data", base_rows["cmd-fetch-data"]["check"], "tools/fetch_data.py --check", "PASS",
      "'fetch_data: 3 datasets, 0 problems', exit 0 (" + OUT + "fetch_data_check.out)."))
A(row("cards-changed-c014-c016", base_rows["cards-changed-c014-c016"]["check"], "cards.json E5-c014, E5-c016; L01 Proposition 2.4 and 2.6", "PASS",
      "c014 back: 'Under (A1) of Proposition 2.4 ... baskets with P^L greater than P^P and ... less than' matches L01 Proposition 2.4 (basket A and basket B). "
      "c016 back: 'Under (A1) and (A2) of Proposition 2.6 ... D(0)=1, D(t)>0, N_0>0' matches L01 Proposition 2.6 and its proof."))
A(row("cards-changed-c041-c045", base_rows["cards-changed-c041-c045"]["check"], "cards.json E5-c041, c042, c043, c044, c045; L03 Proposition 2.2, Remark 2.5, Proposition 4.2", "PASS",
      "c041 hypotheses A1-A3 and k* formula match L03 Proposition 2.2; c042 and c044 match Remark 2.5 (i) and (ii); c043 and c045 carry 'under A1 to A3 and Assumption 4.1' matching Proposition 4.2."))
A(row("cards-remark-labels", base_rows["cards-remark-labels"]["check"], "cards.json basis and back fields; L01-L08.html", "PASS",
      "Script scan: every 'Definition/Proposition/Remark/Assumption/Derivation/Theorem/Corollary/Problem/Example x.y' label in a card's back or basis occurs in its lesson (or in L04 when cited as 'Lesson 4'); 0 misses."))

# ---- carried rows (cited subject byte-identical since 04626e9) ----
for rid, files in [
    ("proj-exA-c2-annotation", P),
    ("proj-exA-length", P),
    ("proj-lab2-one-pair", P + "; tests/labs/E5/lab-E5-project-2.py"),
    ("proj-spec-ladder", P),
    ("proj-rubric-observable", P),
    ("proj-calib-exB", P + " #exemplar-b (no E5 blind scorer file in ~/.fanout/blind/, ruling 23)"),
    ("proj-calib-exA-blind", P + " #exemplar-a (no E5 blind scorer file in ~/.fanout/blind/, ruling 23)"),
    ("proj-conventions-gaps", P),
    ("proj-lab1-numbers", P + "; tests/labs/E5/lab-E5-project-1.py"),
    ("proj-lab3-table", P + "; tests/labs/E5/lab-E5-project-3.py"),
    ("proj-lab3-expected-prose", P),
    ("proj-lab3-days-and-spread", P + "; course/assets/data/market/ (unchanged)"),
    ("proj-data-licence", P + "; tools/data_sources.yaml; course/assets/data/market/MANIFEST.json (unchanged)"),
    ("proj-basis-claims", P),
    ("proj-taylor-exA", P),
    ("proj-exB-numbers", P),
    ("proj-atlas-disclosure", P + "; curriculum/02-economics-finance-core.yaml E5 block lines 155-195 (its two changed hunks, lines 391 and 428, are other units)"),
    ("proj-page-length-and-voice", P),
    ("proj-no-network-no-file-input", P),
    ("proj-delta-window-definition", P),
    ("proj-delta-exA-limits", P),
    ("cards-sample-1", "cards.json E5-c010 and course/modules/E/E5/L01.html Definition 2.1"),
    ("cards-sample-12", "cards.json E5-c120 and course/modules/E/E5/L08.html Definition 1.2"),
]:
    A(carry(rid, files))

# ---- new rows (this round) ----
A(row("cards-c033-missing-hypothesis", "E5-c033 (T-graded, changed in the delta): the back states a result of Proposition 2.4 without its hypothesis",
      "course/modules/E/E5/cards.json E5-c033 back; course/modules/E/E5/L02.html Proposition 2.4 and the misconception 'The Solow residual measures technology'",
      "FAIL",
      "Back: 'the residual depends on that alpha (Proposition 2.4)'. L02 Proposition 2.4 gives the change in the average residual, and the paragraph after it says the residual is a different number 'whenever the average growth of capital "
      "and of labour differ'; the statement gives the coincidence 'if and only if the average growth of capital equals the average growth of labor'. With equal growth rates "
      "(Problem P2) the residual does not depend on alpha. Rule 10 requires cards to carry a proposition's hypotheses; ruling 26 lists a missing hypothesis as a defect.",
      "In E5-c033 back, replace 'and the residual depends on that alpha (Proposition 2.4)' with 'and the residual depends on that alpha whenever the average growth of capital and of labour differ (Proposition 2.4)'."))
A(row("cards-c034-missing-hypothesis", "E5-c034 (C-graded, unchanged text, inside the cards-lab-numbers scope): 'a different number for each alpha' omits Proposition 2.4's hypothesis",
      "course/modules/E/E5/cards.json E5-c034 back; course/modules/E/E5/L02.html Proposition 2.4",
      "FAIL",
      "Back: 'the residual is a different number for each alpha'. The lesson's paragraph after Proposition 2.4 (and misconception 2) gives the dependence only 'whenever the average growth of capital and of labour differ'; "
      "for equal growth rates (Problem P2) the residual is the same for every alpha, so the universal claim is false in that case. The card's own question is about "
      "the general choice of alpha, so the hypothesis is needed.",
      "In E5-c034 back, replace 'but the residual is a different number for each alpha' with 'but the residual is a different number for each alpha whenever the average growth of capital and of labour differ (Proposition 2.4)'."))
A(row("idx-prereq-build-status", "E5 index.html build-status statements about E1 and M2 agree with the released-module list and with the links on the same page",
      "course/modules/E/E5/index.html line 35 ('no page of E1 is built in this program yet') and line 60 ('The concepts of P0.1, E1 and M2 are not yet released in this program, and their links open entries reading \"not yet released\"')",
      "FAIL",
      "course/index.html line 41 lists 'Released modules' including M2 and E1 (E1 and M2 are not in the not-yet-released set). course/modules/E/E1/ (L01-L09, project) and "
      "course/modules/M/M2/ (L01-L11, grader) are built. course/concepts.html line 303 gives competitive-equilibrium as 'defined here' (modules/E/E1/L03.html) and line 125 gives implicit-function-theorem as "
      "'defined here' (modules/M/M2/L21.html). The same index.html lines 61-62 link to those definitions. So line 60 is false for E1 and M2, and line 35 is false for E1 (changed text in line 60 is from this delta; line 35 is older text). "
      "P0.1 is not built (no P0 module), so the P0.1 statements are true.",
      "Line 35: replace 'and no page of E1 is built in this program yet' with 'and P0.1 is not yet released'. Line 60: replace 'The concepts of P0.1, E1 and M2 are not yet released in this program, and their links open entries reading \"not yet released\".' with 'The concept of P0.1 is not yet released in this program, and its link opens an entry reading \"not yet released\".'"))
A(row("lessons-delta-hunks", "Every changed hunk of L02-L06 that a card cites or that carries a number is re-read and its numbers re-derived",
      "course/modules/E/E5/L02.html (emp-3 solution, honest-pending note, limitation bullet); L03.html (section 5 bullet, references); L04.html (why-it-matters, A3, Remark 1.2 benchmark, Parts B-D interpretation, quiz); L05.html (why-it-matters, Remark 1.2, Lab 1 intro, section 4 bullet 2, L05-P2 title); L06.html (section 1, Proposition 2.1 units, section 5, E2/E3 solutions, references)",
      "PASS",
      "Re-derived with own scripts: L02 emp-3: mean dlnK = 0.0355561807, 0.3 x mean = 0.010666854 (prints 0.010667), 0.4 x mean = 0.0142224723 (0.014222), 0.4 x 0.035557 = 0.0142228 (0.014223); the page text matches. "
      "L03: first period with gap below 1e-12 is 692 (Decimal, prec 60, independent of the twin); gap at 500 is 3.4e-9. L04: IS-LM closed forms, D = 5/4, Y* = 28/5, i* = 4/5, the Part B and C steps (2/25, 1/25, 4/5, 4/5, 2/5, 4/5 multiplier, -1/10, -1/5), b/D = 8/5, -(1-c)/D = -1/5, Part D = 4; the M1-M3 and E1-E3 solutions reproduce. "
      "L05: dP = (da + nu dPe)/(eta+nu) and dY = nu(da - eta dPe)/(eta+nu) follow from Proposition 2.1; Part D shares and changes (50..800) match; L05-E2 differences match; R2 gives P* = 1.5, Y* = 1040; R3 gap 60. "
      "L06: 13/600 = 0.021667; 1/120 and 1/60; 58 bp = 0.0058; -(5/6)(0.0058) = -0.004833; 5.5% row -0.004167; signs of the 12 periods (9 positive gaps, 3 negative) match the twin; R2 gives 0.062. "
      "Limits sentences checked against the propositions. No defect in these hunks except the index file (row idx-prereq-build-status)."))
A(row("lab-twins-L04-L06-delta", "The three changed lab twins run alone and match their pages",
      "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py; course/modules/E/E5/L04.html, L05.html, L06.html",
      "PASS",
      "Each of the 11 twins run as 'python -I -W error' from /tmp/e5r1run: exit 0 and empty stderr (" + OUT + "twin_*.out, .err). run_labs --unit E5 PASS (page code == twin; page expected == output under the page's rule). "
      "The L04 print label changed (keynesian_cross_multiplier -> goods_market_benchmark) and the L04 page expected block matches it; no other reference to the old label remains. ruff and mypy PASS on the twins."))
A(row("cards-delta-coverage", "Every card changed or added in the delta (88 changed, 9 added) is read against its cited lesson text",
      "course/modules/E/E5/cards.json (ids E5-c001..c140 without c135)",
      "PASS",
      "All 97 changed or added ids were read as word-level diffs against 04626e9 (script ledgers/E5/scripts/E5-d-r1/cardsdiff.py; output /tmp/e5r1/cards_delta.txt) and checked against the current lesson text. "
      "Defects found: E5-c033 and E5-c034 (rows cards-c033-missing-hypothesis, cards-c034-missing-hypothesis). The E5-c099 wording 'so inflation is not stable (§5)' is a note, not a row: "
      "L06 section 5 now says 'inflation changes in that period'; the claim is not contradicted. New cards c131-c134 and c136-c140 match their lessons; c131 and c132 match Lab 1 Part A and Part D output."))

# ---- mutants: standing set, no new mutants (ruling 37) ----
def killed(name, desc, line):
    return {"id": name, "description": desc, "file": line[0], "killed_by": line[1]}
K = "compare_output token mismatch against the page's expected block (" + OUT + "standing_mutants.out)"
mutants = [
    {"id": "r4_m01_spread_sign_reversed", "description": "spread sign reversed (round-4 mutant)", "file": "ledgers/E5/mutants/project-2-r4/r4_m01_spread_sign_reversed.py", "killed_by": K},
    {"id": "r4_m02_spread_previous_quarter", "description": "spread uses previous quarter (round-4 mutant)", "file": "ledgers/E5/mutants/project-2-r4/r4_m02_spread_previous_quarter.py", "killed_by": K},
    {"id": "r4_m03_gap_time_index_off_by_one", "description": "gap time index off by one (round-4 mutant)", "file": "ledgers/E5/mutants/project-2-r4/r4_m03_gap_time_index_off_by_one.py", "killed_by": K},
    {"id": "r4_m04_gap_trend_at_window_start", "description": "trend evaluated at window start (round-4 mutant)", "file": "ledgers/E5/mutants/project-2-r4/r4_m04_gap_trend_at_window_start.py", "killed_by": K},
    {"id": "r4_m05_gap_percent_of_trend", "description": "percent-of-trend gap instead of log gap: survives the instant check; documented on project.html line 45, so not a grader finding (lab twins are demonstrations)", "file": "ledgers/E5/mutants/project-2-r4/r4_m05_gap_percent_of_trend.py", "killed_by": ""},
    {"id": "r5_m01_spread_sum_not_difference", "description": "spread as sum, not difference (round-5 file, added in 04626e9..HEAD)", "file": "ledgers/E5/mutants/project-2-r5/r5_m01_spread_sum_not_difference.py", "killed_by": K},
    {"id": "r5_m02_gap_growth_not_level", "description": "gap from growth not level (round-5 file, added in 04626e9..HEAD)", "file": "ledgers/E5/mutants/project-2-r5/r5_m02_gap_growth_not_level.py", "killed_by": K},
    {"id": "r5_m03_gap_trend_window_19", "description": "trend window 19 quarters (round-5 file, added in 04626e9..HEAD)", "file": "ledgers/E5/mutants/project-2-r5/r5_m03_gap_trend_window_19.py", "killed_by": K},
    {"id": "m01_gap_intercept_only", "description": "gap uses intercept only", "file": "ledgers/E5/mutants/project-2/m01_gap_intercept_only.py", "killed_by": K},
    {"id": "m02_gap_percent_of_trend", "description": "percent-of-trend gap (earlier round copy): survives the instant check; documented on project.html line 45, not a grader finding", "file": "ledgers/E5/mutants/project-2/m02_gap_percent_of_trend.py", "killed_by": ""},
    {"id": "m03_gap_lagged_output", "description": "gap uses lagged output", "file": "ledgers/E5/mutants/project-2/m03_gap_lagged_output.py", "killed_by": K},
    {"id": "m04_gap_window_24", "description": "gap window 24 quarters", "file": "ledgers/E5/mutants/project-2/m04_gap_window_24.py", "killed_by": K},
    {"id": "m05_spread_reversed", "description": "spread reversed", "file": "ledgers/E5/mutants/project-2/m05_spread_reversed.py", "killed_by": K},
    {"id": "m06_spread_fixed_offset", "description": "spread with fixed offset", "file": "ledgers/E5/mutants/project-2/m06_spread_fixed_offset.py", "killed_by": K},
    {"id": "m07_gap_sign_flipped", "description": "gap sign flipped", "file": "ledgers/E5/mutants/project-2/m07_gap_sign_flipped.py", "killed_by": K},
    {"id": "m08_gap_log10", "description": "gap uses log10", "file": "ledgers/E5/mutants/project-2/m08_gap_log10.py", "killed_by": K},
]

registry_flags = list(base["registry_flags"]) + [
    "plans/E5-open-items.md NOTATION_REQUESTS (line 24) still names u^{\\ast} for the natural rate; L06 uses u^n (stale planning note, not learner text)."]
freshness_flags = [
    "ledgers/E5/scripts/E5-d-r5/ and ledgers/E5/mutants/project-2-r5/ are cited as round-5 evidence but were added between 04626e9 and HEAD (git diff --name-status). Present and re-run here.",
    "plans/E5-open-items.md 'Slice b' log says the lab docstring round left printed output unchanged; the L04 print label did change (keynesian_cross_multiplier -> goods_market_benchmark), and the page was re-embedded. Plan log only.",
    "References: course/index.html and E5 index build-status text (see idx-prereq-build-status) went stale when E1 and M2 were released.",
]
notes = (
    "Round 1 delta verification, pin 95f3f8cb, base 04626e9 (round-5 fragment). Scope per ruling 30 and the base notes: project.html, cards.json, "
    "lesson passages cited by cards and the changed lesson hunks (L02-L06), index.html, lab twins L04-L06, project lab twins and standing mutants. "
    "project.html and the three project twins are byte-identical to 04626e9 (git diff --quiet), so the project rows are carried. "
    "Ruling 37: no new mutants were authored; the 16 standing mutants were re-run (14 killed, 2 documented survivors). "
    "Ruling 26 kinds only: the FAIL rows are missing hypotheses (c033, c034) and a false statement (index build status). "
    "Ruling 23: no E5 blind scorer file exists in ~/.fanout/blind/, so the base rubric calibration rows are carried. "
    "Not checked: the blind rubric calibration itself (no scorer output); the live part of verify_refs was run only through the tool's own --unit E5 path; "
    "lesson prose outside the hunks and the cards that cite them was not re-read (base slices a-c own it). "
    "Observations, not rows: E5-c099 says 'inflation is not stable (§5)' where §5 now says 'inflation changes' (same claim); the L05 Part B line is printed as price_share while the docstring says price change per unit of a (the value is 1/(eta+nu)); "
    "E5-c135 is absent (ruling 2 allows gaps). "
    "Scripts: ledgers/E5/scripts/E5-d-r1/ (run_standing_mutants.py, lab2_gap_check.py, card_numbers.py, build_fragment_r1.py) and out/ (gate outputs, twin outputs, standing_mutants.out)."
)
summary = (
    "E5-d round 1: verdict FAIL. 69 rows: 65 PASS (including carried rows), 4 FAIL. FAIL rows: cards-c033-missing-hypothesis, "
    "cards-c034-missing-hypothesis (missing Proposition 2.4 hypothesis on T/C cards), idx-prereq-build-status (E1 and M2 called not yet released/not built). "
    "cards-lab-numbers is FAIL because it contains c034. All gates PASS on 95f3f8cb (check_pages, check_dag, check_projects, run_labs, page_smoke, pytest E5, verify_refs, ruff, mypy, build_site, render_curriculum, fetch_data). "
    "Mutants: 14 of 16 standing killed; 2 documented survivors recorded with killed_by empty."
)

# Ensure every base row id is present exactly once
ids_out = [r["id"] for r in rows]
missing = [i for i in base_rows if i not in ids_out]
extra = [i for i in ids_out if i not in base_rows and i not in (
    "cards-c033-missing-hypothesis", "cards-c034-missing-hypothesis", "idx-prereq-build-status",
    "lessons-delta-hunks", "lab-twins-L04-L06-delta", "cards-delta-coverage")]
assert not missing, missing
assert not extra, extra
assert len(ids_out) == len(set(ids_out)), "duplicate ids"
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag = {
    "unit": "E5",
    "slice": "E5-d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for E5-d, round 1 (delta verification, ruling 30; did not build E5)",
    "pin": "95f3f8cb",
    "base": "04626e9 (round-5 fragment C-E5-d.round5.json, pin 04626e9)",
    "checkout": ROOT,
    "scratch": "/tmp/e5r1run (twins, data/ust_daily.csv), /tmp/e5r1 (lesson text extracts, scripts)",
    "verified_at": "2026-11-09T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": summary,
}
out = ROOT + "/ledgers/E5/E5-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "pass", n_pass, "fail", n_fail, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
