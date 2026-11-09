import json

CARRY = "Carried from round 8 ({files} byte-identical since the previous pin f618cf1): "
P = "PASS"
F = "FAIL"

def carry(files, text):
    return CARRY.format(files=files) + text

IDX = "course/modules/E/E5/index.html"
L01 = "course/modules/E/E5/L01.html"
L02 = "course/modules/E/E5/L02.html"
L03 = "course/modules/E/E5/L03.html"
TW = "tests/labs/E5/lab-E5-L01-1.py, lab-E5-L02-1.py, lab-E5-L03-1.py"

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

row("E5a-r3-hub-prereq-titles", "Hub prerequisite titles match curriculum strings", IDX + ":35", F,
    "Titles match: 'E1 Microeconomics' (concepts.html:299), 'M1 Precalculus & Mathematical Reasoning' (concepts.html:63), "
    "'M2 Single & Multivariable Calculus' (concepts.html:116), 'P0.1 How to Study This Program' (concepts.html:35). "
    "The same line says 'no page of E1 is built in this program yet', which is false at 95f3f8cb: course/modules/E/E1/index.html, "
    "project.html and L01-L09.html exist (git diff --name-status f618cf1..HEAD lists them as A), and concepts.html:302-303 "
    "mark E1 concepts 'defined here'. Scripts: scripts/E5-a-r1/hub_checks.out.",
    "In index.html:35 delete the clause 'and no page of E1 is built in this program yet' (or state that E1 is released). Titles need no change.")

row("E5a-r3-hub-card-titles", "Hub card titles equal lesson h1", IDX + ":146-153", P,
    "Re-read at 95f3f8cb: card titles equal the h1 of each lesson: L01.html:35, L02.html:35, L03.html:36, L04.html:36 "
    "'Business cycles and the IS–LM model', L05.html:36, L06.html:36 'The Phillips Curve and the Natural Rate', L07.html:36, "
    "L08.html:36 (scripts/E5-a-r1/hub_checks.out). No h1 line is in the L04-L06 hunks.")

row("E5a-r3-nav-titles-L02-L03", "Lesson-nav labels equal target h1", "course/modules/E/E5/L02.html:490; L03.html:618", P,
    "L02.html:490 'Next: L03 · The Solow growth model' equals L03.html:36 h1; L03.html:618 'Next: L04 · Business cycles and the IS–LM model' "
    "equals L04.html:36 h1. Fresh read at 95f3f8cb (the L03 nav is at :618, the base cited :617).")

row("E5a-r3-hub-grammar", "Learner prose is grammatical", IDX + ":33", P,
    carry(IDX, "the lede sentence re-read; the grammar is unchanged."))

row("E5a-r3-L02-exactly-when", "Claim about a theorem matches its statement", L02 + ":104 vs Theorem 2.3 at :107-110", P,
    carry(L02, "lines 104 and 107-110 unchanged."))

row("E5a-r3-L03-attribution-wording", "References paragraph consistent with page naming", L03 + ":611", P,
    "Fresh at 95f3f8cb: L03.html:611 says the lesson 'has not read that paper and attributes no result to it'; the only "
    "attribution is registry key solow1956contribution. references/references.json changed only at three entries "
    "(hunks @@ -2841, -2924, -19679: used_by of BK1, DV1, E9 and generated_at); the Solow entry is unchanged. "
    "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (scripts/E5-a-r1/verify_refs_offline.out).")

row("E5a-r3-L03-sign-lemma-first-use", "Terms defined before use", L03 + ":52 vs :138", P,
    carry(L03, "lines 52 and 138 unchanged."))

row("E5a-card-uniqueness-contradiction", "Cards agree with the current lesson statement (Prop 2.2 says exactly one POSITIVE steady state)",
    "course/modules/E/E5/cards.json (E5-c041); L03.html:97-98, :527", P,
    "Fresh: E5-c041 back (95f3f8cb) says 'exactly one positive steady state, k* = ... (Proposition 2.2)' (scripts/E5-a-r1/cards_L01_L03_diff.out). "
    "L03.html:97-98 Proposition 2.2 states 'exactly one positive steady state'; L03.html:527 table row agrees. Every card containing "
    "'steady state' (E5-c039, c040, c041, c042, c043, c044, c046, c050, c051) was read: none says zero or two.")

row("E5a-cmd-check-pages", "check_pages unit E5 and per page L01, L02, L03",
    "tools/check_pages.py --unit E5 [--page L01|L02|L03]", P,
    "Run at 95f3f8cb: 'check_pages E5: PASS'; 'check_pages E5 L01: PASS'; 'check_pages E5 L02: PASS'; 'check_pages E5 L03: PASS' "
    "(scripts/E5-a-r1/check_pages_*.out, rc 0 each).")

row("E5a-cmd-check-dag", "check_dag E5", "tools/check_dag.py --unit E5", P,
    "Run at 95f3f8cb: 'check_dag E5: PASS' (rc 0). 'check_projects E5: PASS' (rc 0). scripts/E5-a-r1/check_dag_E5.out, check_projects_E5.out.")

row("E5a-cmd-run-labs", "run_labs per page", "tools/run_labs.py --unit E5 --page L01|L02|L03", P,
    "Run at 95f3f8cb: 'run_labs E5: PASS (1/1)' for L01, L02, L03 (rc 0 each); unit run 'PASS (11/11)' (scripts/E5-a-r1/run_labs_*.out).")

row("E5a-cmd-page-smoke", "page_smoke index, L01-L03", "tools/page_smoke.py --unit E5 --pages index L01 L02 L03", P,
    "Run at 95f3f8cb (Chromium): 'page_smoke modules/E/E5/index.html: PASS', L01, L02, L03 PASS; 'page_smoke E5: PASS', rc 0 "
    "(scripts/E5-a-r1/page_smoke_E5_a.out).")

row("E5a-twins-isolated", "Twins run alone under python -I -W error",
    "tests/labs/E5/lab-E5-L01-1.py, lab-E5-L02-1.py, lab-E5-L03-1.py", P,
    "Run at 95f3f8cb: python -I -W error exit 0 for all three (scripts/E5-a-r1/twin-L0{1,2,3}.out, .err empty). L02 last line "
    "'log growth is at most simple growth in every period: True'; L03 last line 'equal_within_tolerance True'. The twins are "
    "byte-identical to f618cf1 (git diff --quiet).")

row("E5a-page-code-equals-twin", "Page code block equals twin", L01 + ", " + L02 + ", " + L03 + " data-run blocks", P,
    "run_labs E5 PASS for L01, L02, L03 at 95f3f8cb (its byte-identical check). The pages and twins are byte-identical to f618cf1.")

row("E5a-expected-equals-output", "Expected block equals output", L01 + ", " + L02 + ", " + L03 + " pre.expected", P,
    "run_labs E5 PASS for L01, L02, L03 at 95f3f8cb (expected block vs stdout under the page's rule). Twin outputs in scripts/E5-a-r1/twin-*.out.")

row("E5a-lint-and-tests", "Lint, types, tests for the E5 twins", "tests/labs/E5; mypy; pytest -k E5", P,
    "At 95f3f8cb: 'ruff check tests/labs/E5' All checks passed!; 'ruff format --check tests/labs/E5' 11 files already formatted; "
    "'mypy --no-incremental tests/labs/E5' Success: no issues found in 11 source files; 'pytest -k E5' collects 12 (test_fetch_data 1, "
    "test_labs 11), 12 pass (scripts/E5-a-r1/ruff_*.out, mypy_E5.out, pytest_E5.out).")

row("E5a-registry-keys", "Reading-list keys exist and match the registry", IDX + ":178-181; references/references.json", P,
    "Fresh: keys solow1956contribution, hicks1937mr, phelps1968money, blanchard2020macroeconomics are present in references/references.json "
    "(python -I check). The registry diff touches only BK1, DV1 and E9 used_by lines and generated_at, so these entries are byte-identical. "
    "verify_refs --offline: 560 entries, 0 problems.")

row("E5a-no-friedman", "No stray attribution", "index.html, L01-L03", P,
    "Fresh at 95f3f8cb: grep -i friedman over index.html, L01.html, L02.html, L03.html returns no lines.")

row("E5a-p01-concept-anchors", "P0.1 concept links resolve and read 'not yet released'",
    IDX + ":60,65; L01.html:37; concepts.html:39,40,44", P,
    "Fresh: index.html:65 links evidence-grade, notation-conventions and project-ladder resolve to concepts.html:39, :44, :40, which read "
    "'not yet released' at 95f3f8cb (scripts/E5-a-r1/hub_checks.out). L01.html:37 '(P0.1, not yet released)'. check_dag E5 PASS. "
    "The E1 and M2 clause of index.html:60 is a separate row (E5a-r5-hub-prereq-concept-status).")

row("E5a-notation", "Symbols match notation/notation.json (no registered symbol reused)", "index.html, L01-L03 math; cards.json changed cards", P,
    "notation/notation.json (8 symbols, macros \\E, \\Prob, \\R, ...) is byte-identical since f618cf1. The changed cards use k, g, alpha, delta, "
    "n, s, Y, K, L, A, P^L, P^P, D(t), pi, lambda and partial derivatives; none is a registered symbol, and none uses \\E, T, R_f, \\Phi, "
    "\\gamma_3 or \\gamma_4. L02.html:365-368 and L03.html:389 are byte-identical.")

row("E5a-banned-and-process-words", "No process words in learner text",
    IDX + ":33; L02.html:133, :272, :365-368; L03.html:389, :611", P,
    "Pages carried (byte-identical since f618cf1). The 26 changed L01-L03 cards and E5-c133 were scanned for round, fixer, verifier, ledger, slice, "
    "builder, delta, fix, audit, sweep, mutant, plan, ruling, verified: only the mathematical 'fixed point' and 'delta' (depreciation, δ) occur.")

row("E5a-hours-arithmetic", "Hours arithmetic", IDX + ":29, :39-42, :146-153", P,
    carry(IDX, "data-hours-lessons 80, data-hours-project 30, 80 + 30 = 110; 72.7% + 27.3% = 100%; eight cards at 10 h = 80 h. "
          "curriculum/*.yaml, curriculum.json and CURRICULUM.md changed only in non-E5 modules (grep of their diffs for E5: no hunk)."))

row("E5a-placement-arithmetic", "Placement counts and fractions", IDX + ":70-139 (quiz), :72", P,
    carry(IDX, "7/9 = 77.8 percent, 8/9 = 88.9 percent."))

row("E5a-data-status-basis", "Data status matches the registry", IDX + ":171; tools/data_sources.yaml:91-107", P,
    carry(IDX + " and tools/ (git diff --name-only f618cf1 HEAD -- tools is empty)", "index.html:171 unchanged."))

row("E5a-r5-index-data-line", "Data line on the hub is accurate", IDX + ":37", P,
    carry(IDX, "index.html:37 unchanged."))

row("E5a-r5-hub-prereq-concept-status", "Prereq paragraph agrees with concept index status",
    IDX + ":60 vs course/concepts.html:39, :40, :44, :302-303, :120, :125", F,
    "index.html:60 says 'The concepts of P0.1, E1 and M2 are not yet released in this program, and their links open entries reading "
    "not yet released'. At 95f3f8cb the E1 and M2 links open defined entries: concepts.html:302 comparative-statics and :303 "
    "competitive-equilibrium read 'defined here' (E1/L04, E1/L03); :120 derivative (M2/L04) and :125 implicit-function-theorem (M2/L21) "
    "read 'defined here'. Only the P0.1 entries (concepts.html:39, :40, :44) still read 'not yet released'. The statement is false for E1 and M2 "
    "(scripts/E5-a-r1/hub_checks.out). The base round carried this row because index.html is byte-identical, but concepts.html changed.",
    "In index.html:60 replace 'The concepts of P0.1, E1 and M2 are not yet released' with 'The concepts of P0.1 are not yet released'; "
    "say that the E1 and M2 links open their defining entries. Keep the P0.1 clause.")

row("E5a-L01-numbers", "Prose numbers match unrounded values and lab output", L01 + ":107-130, 156, 262-289, 298-310, 336-343, 355-439, 504-530", P,
    carry(L01 + " and " + TW, "re-checked the numbers the changed cards cite (0.026856, 0.223144, 105/995, 0.105528, 0.058254, 0.173913, 7/92, 11/10, 19/10) "
          "against L01.html and the twin output (basket A 5/4 and 27/23; basket B 11/10 and 19/10; x - ln(1+x) 0.026856 at x = 0.25)."))

row("E5a-L01-theorems", "Theorems, propositions and proofs are correct", L01 + ":70-152", P,
    carry(L01, "Theorem 1.4, Prop 1.7, Def 2.2, Props 2.4-2.6 and their proofs re-read this round; consistent with the changed cards."))

row("E5a-L01-lab-claims", "Sentences about what the lab prints and checks match code and output", L01 + ":156, :157-292, :311", P,
    carry(L01 + " and " + TW, "twin output re-printed this round: Part C prints x - ln(1+x) at 0.01, 0.05, 0.25 (0.000050, 0.001210, 0.026856); Part B prints basket A and B fractions."))

row("E5a-L01-simulated-label", "Lab labelled SIMULATED where it is generated", L01 + ":51, :156, :161, :311, :546", P,
    carry(L01, "lines unchanged."))

row("E5a-L02-numbers", "Prose numbers match unrounded values and lab output", L02 + ":365-368 (E3 solution); other L02 numbers", P,
    carry(L02, "the E3 numbers were re-derived in the base round (scripts/E5-a-r8/recompute_l02.out); the card numbers 1.029006, 0.029006, 0.028593, 0.030000 "
          "re-checked against L02.html:289 this round."))

row("E5a-L02-theorems", "Theorems and proofs are correct", L02 + ":72-131", P,
    carry(L02, "Theorem 1.4, Prop 1.5, Def 2.1-2.2, Thm 2.3, Prop 2.4 and their proofs re-read; consistent with the changed cards E5-c026 to E5-c035 (except E5-c033, row E5a-r5-cards-L01-L03)."))

row("E5a-L02-lab-claims", "Sentences about what the lab prints and checks match code and output", L02 + ":137, :138-247, :262, :51", P,
    carry(L02 + " and " + TW, "twin output re-printed: average residual 0.016254 at alpha 0.2 and 0.010665 at alpha 0.4; 'the residual depends on the chosen alpha: True'."))

row("E5a-L02-simulated-label", "Lab labelled SIMULATED where it is generated; honest-pending note accurate", L02 + ":51, :133, :137, :138-141, :494", P,
    carry(L02, "lines unchanged; the twin prints 'SIMULATED economy: seed 2026, horizon 40 periods, capital share alpha 0.3'."))

row("E5a-L02-table-row-simple-growth", "Key-results rows match the page", L02 + ":405-408", P,
    carry(L02, "key-results rows unchanged."))

row("E5a-L03-numbers", "Prose numbers match unrounded values and lab output", L03 + ":52, :116, :147, :161-187, :383, :402-410, :430-500", P,
    carry(L03 + " and " + TW, "re-run this round: steady_state_capital 5.5843115042, output_per_worker_at_steady_state 1.6752934513, "
          "first_period_gap_below_tolerance 692, elasticity 1.4285714286 (scripts/E5-a-r1/twin-L03.out)."))

row("E5a-L03-theorems", "Theorems, propositions and proofs are correct", L03 + ":70-187, 184-187, 527-531", P,
    carry(L03, "Definition 1.1, Derivation 1.2, Remarks 1.3, 2.3, 2.5, Props 2.2, 3.1, 4.2, Remark 4.3 re-read; consistent with the changed cards E5-c038 to E5-c051."))

row("E5a-L03-lab-claims", "Sentences about what the lab prints and checks match code and output", L03 + ":52, :192, :376-381, :383", P,
    carry(L03 + " and " + TW, "Parts A-E match the twin output at 95f3f8cb ('residual_at_steady_state 0.000e-56', 'equal_within_tolerance True')."))

row("E5a-r5-L03-misconceptions", "Misconceptions and their numbers", L03 + ":399-411", P,
    carry(L03, "unchanged; 39.8879393156 and -132.9597977186 re-printed by the twin this round."))

row("E5a-r5-L03-R1-solution", "R1 solution is correct and states the right step", L03 + ":497-500", P,
    carry(L03, "unchanged."))

row("E5a-r5-L03-remark-4.3", "Remark 4.3 elasticity", L03 + ":187", P,
    carry(L03, "1/(1-0.3) = 10/7 = 1.4285714286; the twin prints elasticity_of_k_with_respect_to_s 1.4285714286."))

row("E5a-r5-L01-R2-cards", "Cards that restate L01 propositions match the lesson", "course/modules/E/E5/cards.json:88, :104 (E5-c014, E5-c016)", P,
    "Fresh: E5-c014 basis now 'Proposition 2.4' and its back cites (A1) of Proposition 2.4 (L01.html:124-131). E5-c016 back cites (A1) and (A2) of "
    "Proposition 2.6 (L01.html:145-152), with D(0) = 1, D(t) > 0 and N_0 > 0; the basis and back match the lesson.")

row("E5a-r5-cards-L01-L03", "Cards agree with the current lesson text and carry the hypotheses", "course/modules/E/E5/cards.json E5-c001 to E5-c052 and E5-c133", F,
    "Fresh re-check of the 26 changed L01-L03 cards (scripts/E5-a-r1/cards_L01_L03_diff.out): E5-c004, c009, c012, c014-c019, c022, c023, c026, c027, "
    "c031, c032, c035, c038, c040, c041, c042, c044, c045, c046, c050, c051 agree with their lesson statement and carry their hypotheses. "
    "E5-c033 (grade C to T, basis 'Definition 2.1; Proposition 2.4; Theorem 2.3') says 'the residual depends on that alpha (Proposition 2.4)' "
    "without the proposition's hypothesis. Proposition 2.4 (L02.html:120-124) gives the dependence only 'whenever the average growth of capital and of labour differ'; "
    "with equal average growth the residual does not depend on alpha (Problem P2, L02.html:332-337). The page keeps the qualifier at L02.html:281 and :285. "
    "E5-c033 is a missing-hypothesis defect (ruling 26 kind). E5-c133 is byte-identical and matches L03.html:83-86 (Remark 1.3).",
    "In cards.json E5-c033 back, change 'and the residual depends on that alpha (Proposition 2.4)' to 'and the residual depends on that alpha "
    "whenever the average growth of capital and of labour differ (Proposition 2.4)'. Then re-run check_pages E5 L02 and check_dag E5.")

row("E5a-r5-cards-numbers-in-lessons", "Every card number appears in its lesson", "course/modules/E/E5/cards.json E5-c019..c052, c133", P,
    "Fresh: numbers in the changed cards appear in their lessons: 0.223144 and 0.026856 (L01.html:338); 11/10, 19/10 (L01.html:334); 3, 10, 13 CU (L01.html:330); "
    "7/92 (L01.html proof of Prop 2.4); 1.029006, 0.029006, 0.028593, 0.030000 (L02.html:289); 1.4285714286 (L03.html:507); 10/7 (L03.html:187). "
    "The removed E5-c033 numbers (0.016254, 0.010665) are no longer on the card.")

row("E5a-r5-DAG-concept-links", "Concept links and DAG closure", IDX + "; L01-L03 data-concept links", P,
    "check_dag E5 PASS at 95f3f8cb. index.html:33 contains no data-concept link (byte-identical). No new data-concept links in the changed cards.")

row("E5a-r7-delta-read", "Delta read hunk by hunk", "slice paths, f618cf1..95f3f8cb", P,
    "Read at 95f3f8cb: cards.json (26 L01-L03 changes; E5-c133 unchanged; c135 (L06) removed and c139, c140 (L05) added, outside slice a); "
    "references/references.json (3 entries, E5 keys untouched); course/concepts.html (E1 and M2 entries now 'defined here'; P0.1 unchanged); "
    "E1 and M2 pages added (cited by the two index rows); L04-L06 pages and twins (outside slice a; read where the hub cites them: L05.html:59, :79; "
    "L06.html:73, :278, all unchanged); plans/E5-build-plan.md, E5-open-items.md, pyproject.toml, CURRICULUM.md and curriculum yaml "
    "(no E5 page or card hunk). index.html, L01-L03, the L01-L03 twins, notation/, tools/ and course/assets/data/market/ are byte-identical.")

row("E5a-r7-hub-card-bodies", "Hub card bodies agree with the lessons they describe", IDX + ":150, :151", P,
    "Fresh: index.html:150 (L05 card) 'A linear aggregate-demand curve taken as the model's specification' matches L05.html:59 (Assumption A1, "
    "'aggregate demand is linear in the price level') and L05.html:79 (Remark 1.2, the linear form is taken as the model). index.html:151 (L06 card) "
    "'the natural rate ... under adaptive expectations' matches L06.html:73 (Assumption A3, adaptive expectations) and L06.html:278 (Corollary 3.2). "
    "The L05 hunks (:49-53, :77-80, :121-124, :319) and L06 hunks (:60, :79, :131, :262, :307-311, :387-392) do not touch :59, :73 or :278; "
    "the cited titles are unchanged.")

row("E5a-r6-hub-lede-static-claim", "Hub lede claims about the model's dynamics are accurate", IDX + ":33", P,
    "Fresh at 95f3f8cb: the lede says the module is 'static except for the Solow recursion and the adaptive-expectations path of Lesson 6'. "
    "L03.html:59-62 defines the recursion; L06.html:113-127 has the seeded 12-period adaptive-expectations path; L04.html:65 (Remark 1.2: the static model 'does not generate a path') and L04.html:339 (canon-breaks: 'A static model') say the IS-LM model is static (no path); L05.html:56 'The model is static: it describes one period, with no dynamics'. "
    "L07 and L08 are unchanged (single-period rule; summed series with no time assigned).")

row("E5a-r6-L03-refs-all-T", "References paragraph grades and lab values", L03 + ":611", P,
    "Fresh: L03.html:611 'the first period at which the gap is below 1e-12, which is 692'; the re-run twin prints "
    "'first_period_gap_below_tolerance 692' (scripts/E5-a-r1/twin-L03.out). The lab values are graded C and name the lab, as stated.")

row("E5a-r7-L02-E3-instruction", "E3 instruction and solution agree with the printed output and the 'printed only' condition", L02 + ":365-368 (E3)", P,
    carry(L02, "the E3 instruction and solution are byte-identical to the round-8 fix."))

row("E5a-r8-new-card-c133", "New card E5-c133 agrees with L03 Remark 1.3", "course/modules/E/E5/cards.json E5-c133 vs L03.html Remark 1.3", P,
    carry("cards.json E5-c133 object and " + L03, "E5-c133 is not in the changed-card list (scripts/E5-a-r1/cards_cmp.out); Remark 1.3 at L03.html:83-86 unchanged."))

row("E5a-r8-canon-breaks-389", "L03 canon-breaks sentence on output per worker along the transition", L03 + ":389", P,
    carry(L03, "line 389 unchanged; Proposition 3.1 unchanged."))

row("E5a-r8-l02-e3-numbers-scripted", "E3 numbers re-derived by script", "ledgers/E5/scripts/E5-a-r8/recompute_l02.py", P,
    carry(L02 + " and the E5-a-r8 script output", "recompute_l02.out (ledgers/E5/scripts/E5-a-r8/recompute_l02.out) is present in the checkout."))

assert len(rows) == 53, len(rows)
ids = [r["id"] for r in rows]
assert len(set(ids)) == 53

fragment = {
    "unit": "E5",
    "slice": "a",
    "round": 1,
    "verifier": "Haiku independent verifier (F11), E5-a round 1 closing delta (ruling 30) against the round-8 base; did not build E5",
    "pin": "95f3f8cb",
    "base": "f618cf1 (round-8 pin; base fragment ~/.fanout/frags/C-E5-a.round8.json, verdict PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF11-E5-a (detached at 95f3f8cb, .venv symlinked)",
    "scratch": "/tmp/e5a",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "index.html:35 and :60 went stale when the E1 and M2 pages were added after f618cf1 (concepts.html E1 and M2 entries now 'defined here'). "
        "The round-8 ledger carried these rows because index.html is byte-identical, but its subject (concepts.html and the E1 pages) changed."
    ],
    "notes": (
        "Ruling 30 closing delta: non-PASS base rows (none) and rows whose subject changed were re-verified from scratch; others carried with the "
        "carry prefix. Ruling 37: no new mutants; E5 slice a has no project grader, so the standing mutant set is empty. Not run: the global gates that "
        "do not concern slice a (build_site --check, render_curriculum diff, fetch_data --check, full pytest, full ruff/mypy on the repo, "
        "run_graders and mutate_graders, which have no E5 project). The E5-c033 card and the index.html:35 and :60 sentences are the only defects found; "
        "no new-defect hunting outside the listed rows (ruling 30). Observation (not graded): E5-c031 cites only Problem P2 for the same-rate identity, "
        "while L02.html:117 also cites Theorem 1.4; not a defect."
    ),
    "summary": (
        "E5-a round 1 closing delta at 95f3f8cb (base f618cf1): 53 rows; 50 PASS, 3 FAIL. FAIL: E5a-r3-hub-prereq-titles (index.html:35, "
        "'no page of E1 is built' is false), E5a-r5-hub-prereq-concept-status (index.html:60, E1 and M2 concepts described as not yet released; "
        "concepts.html:302-303, :120, :125 read 'defined here'), E5a-r5-cards-L01-L03 (E5-c033 drops Proposition 2.4's hypothesis). "
        "Gates at 95f3f8cb all pass: check_pages (unit and L01-L03), check_dag, check_projects, run_labs (pages and unit), page_smoke "
        "(index, L01-L03), twins under python -I -W error, ruff check and format, mypy --no-incremental, pytest -k E5 (12), verify_refs --offline (560, 0 problems)."
    ),
}

import sys
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "FAIL", sum(1 for r in rows if r["status"] == F), "PASS", sum(1 for r in rows if r["status"] == P))
