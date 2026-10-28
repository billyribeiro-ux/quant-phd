"""Assemble the round-19 AC4-d fragment: carries byte-identical PASS rows from round 18, re-verifies the rest."""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC4-d.round18.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
S = "ledgers/AC4/scripts/AC4-d-r19/"
L7 = "course/modules/AC/AC4/L07.html"
L8 = "course/modules/AC/AC4/L08.html"
CARDS = "course/modules/AC/AC4/cards.json"

NEW = {}
def row(rid, check, location, status, evidence):
    NEW[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}

# ---- commands, re-run this round
row("AC4-d-cmd-pin", "2.9-structure", "repository", "PASS",
    f"git -C {root} log -1 --oneline = 51fa336 AC1, M1, AC4, CF1: fixes for verification round 18; git status: detached, only untracked .venv (symlink).")
row("AC4-d-r6-delta-coverage", "2.9-structure", f"git diff --stat 7143726 51fa336 for {L7}, {L8}, {CARDS}, tests/labs/AC4/lab-AC4-L07-1.py, tests/labs/AC4/lab-AC4-L08-1.py", "PASS",
    "Delta read hunk by hunk: L07.html lines 67-69 (def), 138-140 (hypothesis), 215-228 (helpers), 261-300 (main and output), 368-375 (E1, E2), 405-422 (key rows), 464 (L07q8); L08.html lines 96, 128-134 (paragraph, hypothesis, interpretation), 203-245 (lab), 281-289 (output), 294 (§7 bullet), 304-306 (misc), 393 (key row), 424-426 (quiz); cards.json items 73, 81, 94, 107 (L06 card 73 out of slice); L06 and L05 twins out of slice.")
row("AC4-d-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit AC4; tests/labs/AC4/*", "PASS",
    f"run_labs AC4: PASS (10/10), rc=0 ({S}run_labs output in session).")
row("AC4-d-cmd-twin-isolated", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py; tests/labs/AC4/lab-AC4-L08-1.py", "PASS",
    "python -I -W error on each twin: rc=0; L07 prints 18 lines, L08 19 lines (see embed_check.out).")
row("AC4-d-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit AC4 --pages L07 L08", "PASS",
    f"{S}page_smoke.out: modules/AC/AC4/L07.html PASS, L08.html PASS, AC4 PASS; lab timings 0.0 s each (under 10 s).")
row("AC4-d-cmd-check_pages", "2.9-structure", "tools/check_pages.py --all; L07.html, L08.html, cards.json", "PASS",
    f"{S}check_pages.out: check_pages AC4: PASS, rc=0.")
row("AC4-d-cmd-check_dag", "2.9-dag", "tools/check_dag.py --all", "PASS", f"{S}check_dag.out: check_dag AC4: PASS, rc=0.")
row("AC4-d-cmd-check_projects", "2.9-structure", "tools/check_projects.py --all", "PASS", f"{S}check_projects.out: check_projects AC4: PASS, rc=0.")
row("AC4-d-cmd-lint-mypy", "2.9-lint", "tests/labs/AC4/lab-AC4-L07-1.py; tests/labs/AC4/lab-AC4-L08-1.py", "PASS",
    f"ruff check on both twins: All checks passed (rc=0, {S}ruff.out); mypy --no-incremental on both: Success, no issues in 2 files (rc=0, {S}mypy.out).")
row("AC4-d-cmd-pytest", "2.9-tests", "tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py", "PASS",
    f"pytest -q on the three files: 32 dots, rc=0 ({S}pytest.out).")
row("AC4-d-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4", "PASS",
    f"offline: 'offline integrity: 560 entries, 0 problems', rc=0; live --unit AC4: 'live re-verification of AC4: 2 of 560 entries, 0 problems', rc=0 ({S}verify_refs_*.out). AC4 pages cite no registry key.")
row("AC4-d-r17-cmd-mutate_graders", "2.5-labs", "tools/mutate_graders.py --unit AC4 --seeds 0-4", "PASS",
    f"{S}mutate_graders.out: 'mutate_graders AC4: PASS (139/139 killed)', rc=0 (project graders, not the lab twins).")
row("AC4-d-r17-cmd-embed", "2.5-labs", f"{L7} and {L8} data-run blocks and class=expected blocks vs twins", "PASS",
    f"{S}embed_check.py: L07 and L08 code blocks equal the twin source (True); expected blocks equal a fresh python -I run (True).")
# ---- numbers, grades, math
row("AC4-d-2.2-numbers-L07", "2.2-numbers", f"{L7} §2 (line 100), §4 (lines 129-134), §5 (line 322 onward), §7, Lab 1 output", "PASS",
    "Recomputed: D=max(0,q+E-K); t_min=52 at K=10,000 (40+3000*20/5000); t_min=44 and Sigma=180,000 at K=12,000; Sigma=140,000; 14 pairs with q>K; 201-14=187; 75 empty and 112 feasible (187-75); 73/112=0.6518; 75/187=0.4011; all match Lab 1 output (run this round).")
row("AC4-d-2.2-numbers-L08", "2.2-numbers", f"{L8} §1, §3, §4 (lines 115-122), §5, §6, §7, §8, Lab 1 output", "PASS",
    "Recomputed: RI=120-90=30, EVA=96-90=6, capitalized RI 102.8 (dRI 72.8), EVA 62.8 (dEVA 56.8); SIM-G RI 2250, EVA -486, tax term 2736; SIM-D/SIM-A -4130/-2440, OI/C 5.67%/4.86%; 4 of 28 discordant pairs (run); all match output of the twin this round.")
row("AC4-d-2.2-numbers-L07-E1-seed", "2.2-numbers", f"{L7} E1 solution", "PASS",
    f"Seed scan 1-40 (ledgers/AC4/scripts/AC4-d-r19/seed_scan.py, output seed_scan.out): no seed gives both 186 fits and 75 empty ranges (seeds 31, 33, 40 give 75 empty; seed 22 gives 186 fits). The sentence 'None of seeds 1 to 40 gives 186 pairs with q<=K and 75 empty ranges' holds.")
row("AC4-d-L08-E1-seed-claim", "2.2-numbers", f"{L8} E1 solution (line 346)", "PASS",
    "seed_scan.out: discordant counts of 28 for seeds 1-40: count 4 at seeds 14, 20, 26, 28; the other 36 seeds give other counts (0 to 9). Sentence matches.")
row("AC4-d-r17-indep-recompute", "2.2-numbers", "tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py generators; integer recomputation", "PASS",
    "Independent recomputation this round: L07 sign identity and supplier-zero hold on all 187 q<=K pairs; L08 identity holds on 8 of 8 (ties_check.out, seed_scan.out, transplant runs). Generators unchanged in this delta.")
row("AC4-d-2.3-grades-L07", "2.3-grades", f"{L7} §9 key-results table (lines 405-422) and grade spans", "PASS",
    "Row 'Of 187 pairs ... 75 empty ... supplier-gain and sign identities hold for all 187, sum identity for all 112 feasible' graded C, basis 'Lab 1 (SIMULATED), output lines ... four check lines': the output has those four lines (grade C is correct for a SIMULATED read-off). Other rows T by P/M/Theorem references.")
row("AC4-d-2.3-grades-L08", "2.3-grades", f"{L8} §10 key-results table (lines 375-386)", "PASS",
    "Row 'Lab 1 (SIMULATED): the identity ... 8 of 8 generated divisions, RI >= 0 ... 9 of 9 the boundary division included' graded C with basis naming the identity and sign lines (present in output). Remaining rows T with Lemma/Prop/P references.")
row("AC4-d-2.4-math-L07", "2.4-math", f"{L7} Lemma 7.2 (lines 89-96), proof (line 98), §2 (line 100), Theorem 7.3 (line 114), §3, §4 worked case", "PASS",
    "Re-derived: Delta_S(t)>=0 iff t>=t_min (q>0); Delta_B>=0 iff t<=r; Sigma identity; Theorem 7.3 part 2 (qv+D(p_m-v)<=qr); worked case D=3000, t_min=52, Sigma=140,000, Delta_S(52)=0, Delta_S(46)=-30,000; K=12,000 gives D=1000, t_min=44, Sigma=180,000. P2 bound t_min<=p_m holds since D<=q. All correct.")
row("AC4-d-2.4-math-L08", "2.4-math", f"{L8} Definition 8.1 (lines 65-76), Lemma 8.2 (86), Lemma 8.3 (88-92), Prop 8.4 (line 102-ish), §3 (line 96, 109), §4 (lines 115-122)", "PASS",
    "Re-derived: Lemma 8.2 EVA-RI=-tau*OI; Lemma 8.3 RI>=0 iff OI/C>=r for C>0; Prop 8.4 dRI=dOI-r dC, dEVA=(1-tau)dOI-r dC; RI-EVA gap tau*dOI; §3 'equal only when tau=0 or dOI=0' and 'lowers both' with r>0, tau<=1, dC>0 (checked both cases). §4 numbers 72.8/56.8 and M3 (66.4, 34.4, 36.4, 28.4) check.")
row("AC4-d-2.4-notation", "2.4-notation", f"notation/notation.json (8 symbols, macros); {L7}, {L8}", "PASS",
    "notation.json defines T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q and macros \\E, \\Prob, \\Var, \\Cov, \\Corr, \\R, \\N, \\indic, \\Normal; the AC4 pages define their own symbols (Sigma, Delta_S, tau, OI, RI, EVA, NOPAT) on first use and use none of the registry symbols with another meaning (grep of the pages for those macros: 0 hits, notation_read.out).")
row("AC4-d-r3-L07-s1-s5-s6-text", "2.4-math", f"{L7} §1 (line 70), §5 (line 322), §6 bullets (lines 327-331)", "PASS",
    "Re-read: §1 inputs and 'the firm's total gain' (Definition 7.1, line 69) consistent with §3 identity; §5 counts 201/14/187/75/112/73 match output; §6 bullets say the model has no tax term and capacity is hard, consistent with the model in §1.")
row("AC4-d-r3-L08-why-and-s3-s5-text", "2.4-math", f"{L8} why-it-matters (line 52), §1 OI/C paragraph (line 78), §3 (lines 96-109), §5 (lines 127-130)", "PASS",
    "Round-18 FAILs resolved in the delta: §3 now states the first-year charge convention ('as in §4'; §4 gives the 20-SCU first-year charge and treats the outlay as charged in full in the reported period), §5 now defines ties. Why-it-matters and §1 sentences re-read: they state no claim beyond Lemma 8.2/8.3 and the inputs.")
row("AC4-d-r2-L08-lab-pair-scope", "2.5-labs", f"{L8} §5 paragraph after 'same base' sentence (line 128)", "PASS",
    "'Lab 1 counts how often the two orders disagree across all 28 pairs of its eight generated divisions, and a tie in either measure is not counted': code at tests/labs/AC4/lab-AC4-L08-1.py line 119 excludes by_ri==0 and by_ratio==0; tie count among the 28 pairs is 0 (ties_check.out), so the rule is accurate and untested on this seed only.")
row("AC4-d-L08-quiz-agreement-claim", "2.9-quiz", f"{L8} quiz L08q5 explanation (line 424-425)", "PASS",
    "Explanation now reads 'with a common base the orders agree. With different bases they can disagree, as 4 of the 28 pairs in Lab 1 do.' Matches P3 and the output count 4 of 28 (run).")
row("AC4-d-2.9-dag-definitions", "2.9-dag", f"{L7} dfn transfer-pricing (line 69); {L8} dfn residual-income (line 67) and economic-value-added", "PASS",
    "Each concept has one dfn: def-transfer-pricing (L07 line 69), def-residual-income and def-economic-value-added (L08 lines 67-68). check_dag AC4 PASS.")
row("AC4-d-2.9-hours", "2.9-hours", f"{L7}, {L8} data-hours (line 2) and eyebrow (line 35); course/modules/AC/AC4/index.html data-hours-lessons", "PASS",
    "data-hours: L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6 (sum 50) = index data-hours-lessons=50: arithmetic consistent. No hub split is re-estimated (architect ruling).")
row("AC4-d-2.9-prose-banned", "2.9-prose", f"{L7}, {L8} learner prose outside code and math (prose_scan.out)", "PASS",
    "Scan for roughly, about <digit>, historically, typically, usually, generally, ellipses, build/builder/verifier/round/REQUESTS/unit report, obviously, clearly: 0 banned phrases or process words in learner prose (prose_scan.out).")
row("AC4-d-r17-process-words", "2.9-prose", f"{L7}, {L8} learner text", "PASS", "Same scan as AC4-d-2.9-prose-banned: no process words in learner text.")
row("AC4-d-r17-prose-scope-words", "2.9-prose", f"{L7} line 322 ('excluded from every line'), line 347 ('Theorem 7.3 part 3 ... for every t')", "FAIL",
    "Scope words audited: two sentences overreach. See AC4-d-r19-L07-every-line-scope and AC4-d-r19-L07-theorem-part3-every-t. All other 'only/all/every/exactly/always' uses in L07/L08 were checked against code or proof.")
row("AC4-d-2.5-lab-L07", "2.5-labs", f"{L7} Lab 1 (§4, lines 136-293 and interpretation line 322); tests/labs/AC4/lab-AC4-L07-1.py", "FAIL",
    "Hypothesis and check lines now match the twin (checks printed; midpoint and nonempty tested at equality; boundary printed nonempty True). Remaining defect: the interpretation sentence 'excluded from every line' is false for the printed 'cases with q > K (no transfer): 14' line. See AC4-d-r19-L07-every-line-scope.")
row("AC4-d-2.5-lab-L08", "2.5-labs", f"{L8} Lab 1 interpretation (line 134 hypothesis, 279-281 interpretation), §6 (line 284), §5 (lines 128-130)", "PASS",
    "Hypothesis: boundary division at equality (OI/C=r, RI=0) is printed and checked (BOUNDARY, twin line 72 and 104-111); interpretation now says 'sign line holds for all nine divisions'; output 9/9. All sentences about the printed lines match the output of the run.")
row("AC4-d-r17-boundary-L07", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py lines 79 (nonempty), 87-89 (BOUNDARY), 114-160 (main)", "PASS",
    "Boundary pair: v=4000, p_m=6000, K=10000, E=8000, q=5000, r=5200: t_min=t_max=5200, Sigma=0; sign line 187/187 includes it; the nonempty test is run at equality (run output).")
row("AC4-d-r17-boundary-L08", "2.5-labs", f"tests/labs/AC4/lab-AC4-L08-1.py line 72 and 104-111; {L8} line 134 (hypothesis)", "PASS",
    "BOUNDARY = Division(1000, 90): OI/C=0.09=r, RI=0; sign_ok includes BOUNDARY; output 'RI >= 0 exactly when OI/C >= r holds for 9/9 divisions, boundary included' (run). Hypothesis states the equality case.")
row("AC4-d-r17-mutants-killed", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17/ (9 files) and AC4-d-r18 (31 files), transplanted onto the current twin (transplant.out)", "PASS",
    "Each one-line mutant transplanted to 51fa336 twin and run (transplant.out, mutants_rerun.out). 24 killed (output differs or rc 1); the rest are not transplantable or equivalent and are recorded individually in AC4-d-r19-mutants-rerun. No survivor is a grader defect in this slice (lab twins: architect ruling).")
row("AC4-d-r17-mutant-L08-m04-ties", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17/r17_L08_m04_discord_ignores_ties.py (transplant)", "PASS",
    "Survives on the current twin: output identical. Equivalent on this seed: ties_check.out shows 0 tie pairs among the 28, so the tie rule never fires. The page's sentence 'a tie in either measure is not counted' is accurate for the code (line 119). Out of scope as a lab-twin mutant.")
row("AC4-d-r17-alternatives", "2.5-labs", f"ledgers/AC4/scripts/AC4-d-r19/alts/ (four alternative correct implementations) and ledgers/AC4/scripts/AC4-d-r18/alts/", "PASS",
    "Alternatives run this round: nonempty via firm_surplus>=0, midpoint as t_min+(t_max-t_min)/2, sign by integer cross-multiplication, discordance by product sign: each prints the same output as the embedded expected block (new_mutants_and_alts.out).")
row("AC4-d-r18-L07-boundary-both-strict", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py line 79 (nonempty) and the sign line 147", "PASS",
    "A both-sides-strict mutant (nonempty = t_min < t_max) now changes the printed 'nonempty True' and the sign line (187/187 to 186/187, and 'empty range' count 76): killed (new_mutants_and_alts.out, r18_carry_L07_nonempty_strict).")
row("AC4-d-r18-L07-checks-not-in-output", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py lines 146-160 and output lines 157-160; L07.html line 140 hypothesis", "PASS",
    "The checks now print: supplier zero at t_min, sign, midpoint inside, sum identity. The hypothesis sentences match the printed lines.")
row("AC4-d-r18-L07-midpoint-test-point", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py line 143-155 (midpoint), output 'midpoint of the range lies inside it: 112/112'", "PASS",
    "The sum identity is tested at t_min, t_max and midpoint(c)=(t_min+t_max)/2; a not-halved midpoint mutant prints 'midpoint ... 0/112' and is killed (r18_carry_L07_midpoint_not_halved).")
row("AC4-d-r18-L07-E1-wording", "2.9-prose", f"{L7} E1 solution (line 370)", "PASS",
    "E1 wording re-read: 'none of the 75 is the boundary pair', 'None of seeds 1 to 40 gives 186 pairs with q <= K and 75 empty ranges'. Both verified (seed_scan.out; output 75 and 187).")
row("AC4-d-r18-L08-section3-later-periods", "2.4-math", f"{L8} §3 line 96 ('as in §4'); §4 'A capitalized outlay' paragraph", "PASS",
    "§3 now says the asset's cost is charged 'starting with the first-year charge in the period of the outlay, as in §4'. §4 gives the first-year charge (20 SCU) and the outlay as charged in full in the reported period. Lab docstring line 76 says 'first year only'. Consistent; the lesson's §7 bullet states that later years are not modeled.")
row("AC4-d-r18-L08-section7-tax-effect", "2.4-math", f"{L8} §7 bullet 'Tax and book treatment' (line 294); tests/labs/AC4/lab-AC4-L08-1.py lines 75-81 docstring", "PASS",
    "Bullet now says the tax rate applies to the changed operating income and the model does not represent a tax-book difference. Twin docstring line 79-80 says the same. capitalized() applies tau through eva(d) on the changed OI (run: capitalized RI 4840, EVA 2666).")
row("AC4-d-r18-mutants-run", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r18/ (31 files) transplanted to 51fa336 (transplant.out)", "PASS",
    "All 31 round-18 mutants re-run (transplanted or hand-carried). See AC4-d-r19-mutants-rerun for the per-mutant verdicts and the equivalence/out-of-scope reasons.")
row("AC4-d-r18-equiv-L08-n09", "2.5-labs", "tests/labs/AC4/lab-AC4-L08-1.py line 116 (a.name < b.name); mutant L08_n09 uses <=", "PASS",
    "Equivalent on this data: with a == b, by_ri = 0 and by_ratio = 0, so the tie rule (line 119) excludes the self pair; the output is unchanged (transplant.out: SURVIVED). Out of scope.")
row("AC4-d-r18-L08-mutants-killed", "2.5-labs", "tests/labs/AC4/lab-AC4-L08-1.py; L08_n01 to L08_n08 transplanted", "PASS",
    "Eight L08 student-error mutants killed on the current twin (transplant.out: n01 EVA+tax, n02 tax as percent, n03 no add-back, n04 full amortization base, n05 rate as fraction, n06 OI/C scale, n08 gap sign; n07 RI strict killed by hand carry r18_carry_L08_ri_side_strict). n09 equivalent (see AC4-d-r18-equiv-L08-n09).")
row("AC4-d-r17-cards-scope", "2.7-cards", f"{CARDS} AC4-c082..c134 (L07 and L08)", "FAIL",
    "Every card re-read against its lesson. c082, c108 match; c095 basis is stale. See AC4-d-r19-cards-c095-basis.")
row("AC4-d-r17-cards-cover", "2.7-cards", f"{CARDS}: L07 cards c082..c096 and c117, L08 cards c097..c116, c129, c134", "PASS",
    "Coverage re-counted: 134 cards; ids unique; L07 and L08 ranges present (run cards_scan.out).")
row("AC4-d-r6-cards-dup-scan", "2.7-cards", f"{CARDS} (134 cards)", "PASS",
    "Duplicate fronts: none (case-insensitive); duplicate ids: none (cards_scan.out).")
row("AC4-d-2.7-cards-L07-L08", "2.7-cards", f"{CARDS}: L07 c082..c096, c117; L08 c097..c109, c113..c116, c129, c134", "FAIL",
    "Cards agree with the current lesson text except c095 basis (line 674 'the exact-check line' names a line the lab no longer prints). See AC4-d-r19-cards-c095-basis.")
row("AC4-d-r17-cards-c102-changed", "2.7-cards", f"{CARDS} AC4-c102 (back); {L8} misconception 3 (line 306) and §5 (lines 127-130)", "PASS",
    "c102 back: 'For two divisions with the same return on capital above the rate, the larger has the larger RI, because RI = (OI/C - r)C'; agrees with misconception 3 and with §5 (same-base orders agree). Re-read this round.")
row("AC4-d-r3-L08-cards-c113-c116", "2.7-cards", f"{CARDS} AC4-c113..c116; {L8} §4 (lines 117-122), §5-§6 (lines 127-130)", "PASS",
    "c113 (SIM-D 124,000 vs SIM-A 59,000; RI -4130 vs -2440; 5.67% vs 4.86%) matches output; c114 (SIM-G 2250 and -486) matches; c115 (72.8, 30 to 102.8) and c116 (56.8, 6 to 62.8) match §4 arithmetic.")
row("AC4-d-r17-cards-c129-c134-new", "2.7-cards", f"{CARDS} AC4-c129, AC4-c134; {L8} §5 example (line 127)", "PASS", "Carried from round 18 (course/modules/AC/AC4/cards.json and L08.html line 127 byte-identical since the previous pin, cited text unchanged): " + prev_rows["AC4-d-r17-cards-c129-c134-new"]["evidence"])
row("AC4-d-r17-cards-c091-changed", "2.7-cards", f"{CARDS} AC4-c091 (back); {L7} Theorem 7.3 part 1 (line 114), Lemma 7.2", "PASS", "Carried from round 18 (course/modules/AC/AC4/cards.json and L07.html lines 89-114 byte-identical since the previous pin): " + prev_rows["AC4-d-r17-cards-c091-changed"]["evidence"])
row("AC4-d-r3-L07-cards-c117", "2.7-cards", f"{CARDS} AC4-c117; {L7} §4 line 134 and M2", "PASS", "Carried from round 18 (course/modules/AC/AC4/cards.json and L07.html §4 and M2 byte-identical since the previous pin): " + prev_rows["AC4-d-r3-L07-cards-c117"]["evidence"])
row("AC4-d-2.7-cards-c088-outside-option", "2.7-cards", f"{CARDS} AC4-c088 (back); {L7} misconception 2", "PASS", "Carried from round 18 (course/modules/AC/AC4/cards.json and L07.html §7 misconception 2 byte-identical since the previous pin): " + prev_rows["AC4-d-2.7-cards-c088-outside-option"]["evidence"])
row("AC4-d-2.7-cards-c100-lemma83", "2.7-cards", f"{CARDS} AC4-c100 (back); {L8} §4, Lemma 8.3", "PASS", "Carried from round 18 (course/modules/AC/AC4/cards.json and L08.html §4 and Lemma 8.3 byte-identical since the previous pin): " + prev_rows["AC4-d-2.7-cards-c100-lemma83"]["evidence"])
row("AC4-d-r17-cards-scope-ok", "2.7-cards", f"{CARDS} AC4-c082, AC4-c095, AC4-c108 (changed this round)", "PASS",
    "c082 back (transfer price 'total gain ... a fact that Section 3 proves') matches Definition 7.1 line 69; c108 back matches key-results row line 422/?? and the sign and identity lines; checked against output (run).")
row("AC4-d-L07-misconception2-market-price", "2.4-math", f"{L7} §7 misconception 2 and L07q7 explanation", "PASS", "Carried from round 18 (L07.html §7 misconception 2 and quiz L07q7 byte-identical since the previous pin): " + prev_rows["AC4-d-L07-misconception2-market-price"]["evidence"])
row("AC4-d-L07-opportunity-cost-def", "2.4-math", f"{L7} §1 (line 72), §2 (lines 98, 100), §6 (line 303)", "PASS", "Carried from round 18 (L07.html §1, §2, §6 byte-identical since the previous pin; line numbers below 215 shifted by the lab edit): " + prev_rows["AC4-d-L07-opportunity-cost-def"]["evidence"])
row("AC4-d-L07-extra-capacity-scope", "2.4-math", f"{L7} §4 (line 134)", "PASS", "Carried from round 18 (L07.html §4 byte-identical since the previous pin): " + prev_rows["AC4-d-L07-extra-capacity-scope"]["evidence"])
row("AC4-d-L07-why-line52", "2.4-math", f"{L7} why-it-matters (line 52)", "PASS", "Carried from round 18 (L07.html line 52 byte-identical since the previous pin): " + prev_rows["AC4-d-L07-why-line52"]["evidence"])
row("AC4-d-L07-R1-title", "2.9-structure", f"{L7} R1 title and solution", "PASS", "Carried from round 18 (L07.html R1 byte-identical since the previous pin; lines shifted): " + prev_rows["AC4-d-L07-R1-title"]["evidence"])
row("AC4-d-L07-uses-undeclared", "2.9-dag", f"{L7} line 38 (meta 'Uses:')", "PASS", "Carried from round 18 (L07.html line 38 byte-identical since the previous pin): " + prev_rows["AC4-d-L07-uses-undeclared"]["evidence"])
row("AC4-d-L08-uses-undeclared", "2.9-dag", f"{L8} line 38 (meta 'Uses:')", "PASS", "Carried from round 18 (L08.html line 38 byte-identical since the previous pin): " + prev_rows["AC4-d-L08-uses-undeclared"]["evidence"])
row("AC4-d-L08-tau-zero-scope", "2.4-math", f"{L8} §3 line 109 (after Proposition 8.4)", "PASS", "Carried from round 18 (L08.html line 109 byte-identical since the previous pin): " + prev_rows["AC4-d-L08-tau-zero-scope"]["evidence"])
row("AC4-d-L08-base-sign-scope", "2.2-numbers", f"{L8} §7 line 291 ('The base decides the level')", "PASS", "Carried from round 18 (L08.html line 291 byte-identical since the previous pin): " + prev_rows["AC4-d-L08-base-sign-scope"]["evidence"])
row("AC4-d-L08-size-claim", "2.7-cards", f"{L8} §8 misconception 3 (lines 305-306); cards AC4-c102 (back)", "PASS", "Carried from round 18 (L08.html misconception 3 and cards.json AC4-c102 byte-identical since the previous pin): " + prev_rows["AC4-d-L08-size-claim"]["evidence"])
row("AC4-d-L08-misconception1-C-positive", "2.4-math", f"{L8} §8 misconception 1 (line 302)", "PASS", "Carried from round 18 (L08.html misconception 1 byte-identical since the previous pin): " + prev_rows["AC4-d-L08-misconception1-C-positive"]["evidence"])
row("AC4-d-L08-why-capital-charge-rate", "2.9-dag", f"{L8} why-it-matters, line 52", "PASS", "Carried from round 18 (L08.html line 52 byte-identical since the previous pin): " + prev_rows["AC4-d-L08-why-capital-charge-rate"]["evidence"])
row("AC4-d-2.8-data", "2.8-data", f"{L7}, {L8} (no data-files attribute)", "PASS", "Carried from round 18 (L07.html and L08.html have no data-files attribute; attribute lines unchanged since the previous pin): " + prev_rows["AC4-d-2.8-data"]["evidence"])
row("AC4-d-2.1-citations-L07-L08", "2.1-citations", f"{L7} References (line ~492); {L8} References", "PASS", "Carried from round 18 (both References sections byte-identical since the previous pin); live and offline verify_refs re-run this round (AC4-d-cmd-verify_refs).")

# ---- NEW FAIL rows this round
row("AC4-d-r19-L07-every-line-scope", "2.9-prose", f"{L7} line 322 (interpretation after Lab 1 output): 'The 14 pairs with q > K have no transfer and are excluded from every line.'", "FAIL",
    "Scope overreach: the printed line 'cases with q > K (no transfer): 14' (Lab 1 output, twin line 136) counts those 14 pairs, and the first six rows of the table show q>K cases too. The claim is true only for the check lines (supplier-gain, sign, midpoint, sum). Fix: replace 'excluded from every line' with 'excluded from every check line'.")
row("AC4-d-r19-L07-theorem-part3-every-t", "2.4-math", f"{L7} §7 misconception 3, line 347: 'Theorem 7.3 part 3 shows that Delta_S + Delta_B = Sigma for every t.'", "FAIL",
    "Citation scope: Theorem 7.3 part 3 (line ~143) states the sum identity 'for every t in the range'. The identity for every t is the display in §3 (line ~127-130) and P1; the claim is true but the locator is wrong. Fix: cite '§3 identity (and P1)' for every t, or 'Theorem 7.3 part 3' for t in the range.")
row("AC4-d-r19-cards-c095-basis", "2.7-cards", f"{CARDS} line 674 (AC4-c095 basis)", "FAIL",
    "basis = 'Lab 1 (SIMULATED), output lines for the counts and the exact-check line'. The current output has no 'exact checks passed' line; it prints four check lines (lab output, L07.html line 322 region). Fix: 'output lines for the counts and the four check lines', matching the key-results row.")
row("AC4-d-r19-mutants-rerun", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17 (9), AC4-d-r18 (31), AC4-d-r19 (9 new/carried); scripts AC4-d-r19/transplant.out, new_mutants_and_alts.out, mutants_rerun.out", "PASS",
    "Verdicts: killed on current twin: r17 m01, m02, m04, m05; r17 L08 m01, m03; r18 L08 n01-n08; r18 n01, n02, n04, n05, n06, n09; r18 hand carries (nonempty strict, empty count >=, feasible strict, skip boundary, midpoint not halved, RI strict, ratio >) and all 4 new m19 mutants. Not transplantable (the construct they edit no longer exists as one line; each has a hand carry above): r17 m03, r17 L08 m02, r18 boundary_strict_only, del_biconditional, del_buyer_assert, del_sum_assert, del_supplier_assert, n03, n07, n08, n10, n11, n12, L08 n07. Survivors on current twin, equivalent on the data or output-invisible: r17 L08 m04 (no ties on seed: ties_check.out), r18 L08 n09 (self pairs excluded by tie rule). The del_* and n08 removals replace an identity check by a hardcoded count that still prints the same line; this is output-invisible and not a plausible student error, and lab twins are demonstrations under the architect ruling. Recorded as PASS out of scope; flagged to the orchestrator as a judgement call.")
row("AC4-d-r19-m19-new-mutants", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r19/m19_*.py (4 new student-error mutants)", "PASS",
    "Four new student-error mutants (t_min divides by K; firm surplus uses the buyer ceiling as price; first-year charge over life+1; RI uses after-tax OI) all killed by output difference on the current twin (new_mutants_and_alts.out).")
row("AC4-d-r19-alts", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r19/alts/ (four alternative correct implementations)", "PASS",
    "Alternatives produce identical printed output to the embedded expected blocks: nonempty via firm surplus, midpoint as offset, integer cross-multiplied sign test, discordance by product sign. No over-constraint on the twin's observable output.")
row("AC4-d-r19-seed-scan", "2.2-numbers", "ledgers/AC4/scripts/AC4-d-r19/seed_scan.py (+ seed_scan.out)", "PASS", "Independent 40-seed scan for both labs (see AC4-d-2.2-numbers-L07-E1-seed and AC4-d-L08-E1-seed-claim).")
row("AC4-d-r19-L08-period-convention", "2.4-math", f"{L8} §3 line 96 and §4 worked capitalization", "PASS",
    "The phrase 'starting with the first-year charge in the period of the outlay' is consistent with §4 (reported OI already charges the outlay in full; first year's charge 20 SCU; the period OI 120 is the reported one) and with the lab docstring (first year only). No new claim.")

row("AC4-d-r17-boundary-probe", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r18/seeds.py (equality scan) re-read; tests/labs/AC4/lab-AC4-L07-1.py", "PASS",
    "Re-run this round as the generator-level check: the L07 sign line (187/187 on q<=K pairs, including the boundary pair at Sigma=0) covers the equality probe; seeds.py itself is unchanged since round 18 and was not needed for the verdict (seed_scan.py covers seeds 1-40).")

# ---- assemble, requiring every previous id to be covered
rows = []
for rid, prow in prev_rows.items():
    if rid in NEW:
        rows.append(NEW[rid])
    else:
        raise SystemExit(f"NOT COVERED: {rid} (previous status {prow['status']})")
for rid in NEW:
    if rid not in prev_rows:
        rows.append(NEW[rid])

frag = {
    "unit": "AC4",
    "slice": "AC4-d",
    "round": 19,
    "verifier": "round-19 independent Haiku verifier for slice AC4-d (L07, L08 and their lab twins); did not build AC4 and shares no context with its builders",
    "pin": "51fa336",
    "base": "7143726 (previous pin; round-18 fragment /tmp/fanout-frags/AC4-d.round18.json used as context; its PASS rows carried only where the cited subject is byte-identical, otherwise re-verified)",
    "checkout": "/tmp/verify19-AC4-d (detached worktree at 51fa336, .venv symlink)",
    "scratch": "/tmp/verify19-AC4-d-scratch",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 7143726..51fa336 for the slice: L07.html, L08.html, cards c082, c095, c108 (cards.json), tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py. L05 and L06 twins and L06 card 73 are out of this slice.",
        "Round-18 FAIL rows that the delta fixed are re-verified PASS with evidence (E1 seed claim, boundary and checks printed, §3/§7 tax wording, E1 wording, boundary at equality in L08).",
        "Three new FAILs: scope sentence 'excluded from every line' (L07 interpretation), Theorem 7.3 part 3 cited for every t (L07 §7 misconception 3), card AC4-c095 basis names a removed 'exact-check line'.",
        "Mutants: 4 new student-error mutants (m19) all killed; 5 hand carries of round-18 mutants all killed; 1 transplanted L08 mutant killed; the equivalence-on-data survivors are recorded with proof (ties_check.out).",
        "Judgement call for the orchestrator: removals of identity checks that are replaced by a hardcoded printed count (del_* and n08 analogues) are output-invisible; recorded as out of scope under the architect ruling for lab twins.",
        "Not checked: no access to external sources (none cited on these pages); tools/fetch_vendor and the full repo gate were not run (slice-only scope); no screenshot of the built pages was taken.",
    ],
    "summary": {},
    "mutants": [
        {"id": "m19_L07_t_min_divides_by_capacity", "description": "Student error: t_min divides the displaced contribution by K, not q.", "file": "ledgers/AC4/mutants/AC4-d-r19/m19_L07_t_min_divides_by_capacity.py", "killed_by": "output differs (row 3: t_min 5956.00 vs 4823-era value; first differing line 'empty range' row 3)"},
        {"id": "m19_L07_firm_surplus_uses_buyer_ceiling_price", "description": "Student error: firm surplus uses r minus p_m in place of r minus v.", "file": "ledgers/AC4/mutants/AC4-d-r19/m19_L07_firm_surplus_uses_buyer_ceiling_price.py", "killed_by": "output differs (boundary firm-wide surplus -10000000 cents)"},
        {"id": "m19_L08_first_year_charge_over_life_plus_one", "description": "Student error: first-year charge uses SPEND // (LIFE_YEARS + 1).", "file": "ledgers/AC4/mutants/AC4-d-r19/m19_L08_first_year_charge_over_life_plus_one.py", "killed_by": "output differs (capitalized C 67334, OI 11204)"},
        {"id": "m19_L08_residual_income_after_tax", "description": "Student error: RI computed on after-tax OI.", "file": "ledgers/AC4/mutants/AC4-d-r19/m19_L08_residual_income_after_tax.py", "killed_by": "output differs (SIM-A RI -3014.00)"},
        {"id": "r18_carry_L07_nonempty_strict", "description": "Round-18 boundary_strict_only and n03 carried: nonempty tested strictly.", "file": "ledgers/AC4/mutants/AC4-d-r19/r18_carry_L07_nonempty_strict.py", "killed_by": "output differs (empty count 76)"},
        {"id": "r18_carry_L07_empty_count_ge", "description": "Round-18 n10 carried: empty count uses >= (boundary counted empty).", "file": "ledgers/AC4/mutants/AC4-d-r19/r18_carry_L07_empty_count_ge.py", "killed_by": "output differs (empty count 76)"},
        {"id": "r18_carry_L07_feasible_strict", "description": "Round-18 n11 carried: feasible count strict.", "file": "ledgers/AC4/mutants/AC4-d-r19/r18_carry_L07_feasible_strict.py", "killed_by": "output differs (feasible 111)"},
        {"id": "r18_carry_L07_skip_boundary_checks", "description": "Round-18 n12 carried: exact checks skip the boundary pair.", "file": "ledgers/AC4/mutants/AC4-d-r19/r18_carry_L07_skip_boundary_checks.py", "killed_by": "output differs (186/187)"},
        {"id": "r18_carry_L07_midpoint_not_halved", "description": "Round-18 n07 carried: test point is lo+hi, not the midpoint.", "file": "ledgers/AC4/mutants/AC4-d-r19/r18_carry_L07_midpoint_not_halved.py", "killed_by": "output differs (midpoint inside 0/112)"},
        {"id": "r18_carry_L08_ri_side_strict", "description": "Round-18 L08_n07 carried: RI >= 0 written as RI > 0 in the sign line.", "file": "ledgers/AC4/mutants/AC4-d-r19/r18_carry_L08_ri_side_strict.py", "killed_by": "output differs (8/9 boundary included)"},
        {"id": "r17_carry_L08_ratio_ge_strict", "description": "Round-17 L08_m02 carried: OI/C >= r written as strict.", "file": "ledgers/AC4/mutants/AC4-d-r19/r17_carry_L08_ratio_ge_strict.py", "killed_by": "output differs (8/9 boundary included)"},
        {"id": "r17_L08_m04_discord_ignores_ties", "description": "Round-17 mutant: ties counted as disagreements.", "file": "ledgers/AC4/mutants/AC4-d-r17/r17_L08_m04_discord_ignores_ties.py", "killed_by": None, "note": "survives on current twin; equivalent on seed 20261027 (0 ties, ties_check.out); PASS"},
        {"id": "L08_n09_discord_pairs_same_name_order", "description": "Round-18 mutant: self pairs included (a.name <= b.name).", "file": "ledgers/AC4/mutants/AC4-d-r18/L08_n09_discord_pairs_same_name_order.py", "killed_by": None, "note": "equivalent: self pair has zero differences and the tie rule excludes it; PASS"},
        {"id": "del_sum_assert", "description": "Round-18 mutant: sum identity check removed; count hardcoded.", "file": "ledgers/AC4/mutants/AC4-d-r18/del_sum_assert.py", "killed_by": None, "note": "output-invisible hardcoding; out of scope per architect ruling (judgement call); PASS"},
    ],
}

out = root / "ledgers/AC4/AC4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "non-PASS", sum(1 for r in rows if r["status"] != "PASS"), "previous ids", len(prev_rows))
