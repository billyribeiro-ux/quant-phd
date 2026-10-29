"""Round 20 fragment builder for AC4-d (L07, L08 and their lab twins). Writes ledgers/AC4/AC4-d.json.

Every status and evidence string below was produced by a command or read in this round; the outputs are in
ledgers/AC4/scripts/AC4-d-r20/. Previous round-19 row ids are all kept (see the id coverage check at the end).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/AC4/scripts/AC4-d-r20/"
prev = json.loads(Path("/tmp/fanout-frags/AC4-d.round19.json").read_text(encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]

P = "PASS"
F = "FAIL"
rows: dict[str, dict] = {}


def row(rid, check, location, status, evidence, fix=""):
    rows[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        rows[rid]["fix"] = fix


# ---- commands, re-run this round ----
row("AC4-d-cmd-pin", "2.9-structure", "repository", P,
    "git rev-parse --short HEAD = fd9a9b7; git symbolic-ref -q HEAD prints nothing (detached); git status shows only "
    "untracked .venv (symlink) and this round's ledgers/AC4/scripts/AC4-d-r20 and ledgers/AC4/mutants/AC4-d-r20.")
row("AC4-d-r6-delta-coverage", "2.9-structure", "git diff --stat 51fa336 fd9a9b7 for course/modules/AC/AC4/L07.html, L08.html, tests/labs/AC4/*, cards.json", P,
    "Delta since round 19: L07.html 4 hunks (lines 65, 322, 347, 378); L08.html 1 hunk (line 52). tests/labs/AC4/*, cards.json, "
    "notation/notation.json and course/modules/AC/AC4/index.html are byte-identical (git diff empty). All five hunks were read and are covered by rows AC4-d-r20-L07-hunk-*, AC4-d-r20-L08-line52.")
row("AC4-d-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit AC4; tests/labs/AC4/*", P,
    f"{S}run_labs.out: 'run_labs AC4: PASS (10/10)'.")
row("AC4-d-cmd-twin-isolated", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py; tests/labs/AC4/lab-AC4-L08-1.py", P,
    f"python -I -W error on each twin: exit 0. Embedded <pre class=expected> equals the run output for L07 and L08 (round-20 comparison; {S}twin_L07_r20.out, twin_L08_r20.out). The page code block equals the twin file byte for byte.")
row("AC4-d-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit AC4 --pages L07 L08", P,
    f"{S}page_smoke.out: 'page_smoke modules/AC/AC4/L07.html: PASS', 'page_smoke modules/AC/AC4/L08.html: PASS', 'page_smoke AC4: PASS'; lab timings 0.0 s each after boot 1.1 s.")
row("AC4-d-cmd-check_pages", "2.9-structure", "tools/check_pages.py --all; L07.html, L08.html, cards.json", P,
    f"{S}check_pages.out: 'check_pages AC4: PASS' (exit 0).")
row("AC4-d-cmd-check_dag", "2.9-dag", "tools/check_dag.py --all", P, f"{S}check_dag.out: 'check_dag AC4: PASS' (exit 0).")
row("AC4-d-cmd-check_projects", "2.9-structure", "tools/check_projects.py --all", P, f"{S}check_projects.out: 'check_projects AC4: PASS' (exit 0).")
row("AC4-d-cmd-lint-mypy", "2.9-lint", "tests/labs/AC4/lab-AC4-L07-1.py; tests/labs/AC4/lab-AC4-L08-1.py", P,
    "ruff check on both twins: 'All checks passed!'; ruff format --check tests/labs/AC4/: '10 files already formatted'; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files'.")
row("AC4-d-cmd-pytest", "2.9-tests", "pytest -k AC4 on tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py", P,
    "pytest -q with -k 'AC4 or ac4': 10 passed; collect-only on tests/test_labs.py -k AC4 gives 10 tests. The whole suite was not run (slice scope).")
row("AC4-d-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit AC4; tools/verify_refs.py --offline", P,
    f"{S}vr_live.out: 'live re-verification of AC4: 2 of 560 entries, 0 problems'; {S}vr_off.out: 'offline integrity: 560 entries, 0 problems'. Neither page cites a registry key.")
row("AC4-d-r17-cmd-mutate_graders", "2.5-labs", "tools/mutate_graders.py --unit AC4 --seeds 0-4 (project grader, cited as a command row)", P,
    f"{S}mutate_graders_r20.out: 'mutate_graders AC4: PASS (139/139 killed)', exit 0. Project-slice command; this round's run is the project verifier's remit and is repeated here only because the row existed.")
row("AC4-d-r17-cmd-embed", "2.5-labs", "course/modules/AC/AC4/L07.html and L08.html data-run and expected blocks", P,
    "Re-compared this round: the embedded expected block of each page equals the run of its twin (exact string equality after html.unescape), and the data-run code block equals the twin (round-20 script inline, outputs in twin_L07_r20.out, twin_L08_r20.out).")

# ---- numbers and grades ----
row("AC4-d-2.2-numbers-L07", "2.2-numbers", "course/modules/AC/AC4/L07.html §2 (line 76-78), §4 (lines 126-134), §5 (line 327), interpretation (line 322)", P,
    "Re-derived by hand and in the integer script (" + S + "indep_integer_recompute_r20.out): D = max(0,q+E-K); worked K=10000 gives D=3000, t_min=52, Sigma=140000; K=12000 gives D=1000, t_min=44, Sigma=180000; t=46 gives Delta_S=-30000; 73/112=0.6518, 75/187=0.4011; lab counts 14/75/112/73 reproduced.")
row("AC4-d-2.2-numbers-L08", "2.2-numbers", "course/modules/AC/AC4/L08.html §1, §3, §4 (lines 115-122), §5 (line 128), §6 (line 296-298), §7 (line 303), §8, Lab 1", P,
    "Re-derived: worked division RI 30, EVA 6, Lemma 8.2 check -24=-0.20*120; capitalized outlay RI 102.8, EVA 62.8 (dRI 72.8, dEVA 56.8); SIM-G gap 0.20*13680=2736 and 2250-2736=-486; SIM-A change 7280/5680; base 1400 gives RI -6. Integer script reproduces every EVA and RI cell of the Lab 1 table (" + S + "indep_integer_recompute_r20.out).")
row("AC4-d-2.2-numbers-L07-E1-seed", "2.2-numbers", "course/modules/AC/AC4/L07.html E1 solution (line 387)", P,
    f"{S}seed_scan_r20.out: seeds 1-40 give (fits,empty) pairs (22,186,73), (31,194,75), (33,188,75), (40,189,75); no seed gives 186 fits with 75 empty. The claim 'None of seeds 1 to 40 gives 186 pairs with q<=K and 75 empty ranges' holds.")
row("AC4-d-L08-E1-seed-claim", "2.2-numbers", "course/modules/AC/AC4/L08.html E1 solution (line 358)", P,
    f"{S}seed_scan_r20.out: discordant counts for seeds 1-40; seeds with 4 discordant: [14, 20, 26, 28]; 36 seeds give other counts. The E1 claim holds word for word.")
row("AC4-d-r17-indep-recompute", "2.2-numbers", "tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py generators; integer recomputation", P,
    f"{S}indep_integer_recompute_r20.py (own transcription of the seeded generators, cross-multiplied integer tests, no Fraction): L07 q>K 14, fits 187, empty 75, feasible 112, binding 73; L08 discordant 4 of 28, EVA and RI cells equal the printed table.")
row("AC4-d-2.3-grades-L07", "2.3-grades", "course/modules/AC/AC4/L07.html §9 key-results table (lines 419-425) and grade spans", P,
    "Each T row is a theorem or a hand computation on stated inputs (Lemma 7.2, Theorem 7.3 parts 2 and 3, P2, §4, M1, M2). The two C rows name Lab 1 (SIMULATED) and its output lines; the 187 row's 'four check lines' matches the four check lines printed in the output (lines 318-321 of the expected block).")
row("AC4-d-2.3-grades-L08", "2.3-grades", "course/modules/AC/AC4/L08.html §10 key-results table (lines 390-396)", P,
    "T rows: Lemma 8.2, Lemma 8.3, Proposition 8.4, P3 and the §4 arithmetic. C rows: Lab 1 identity and sign lines (8 of 8, 9 of 9) and the 4 of 28 pair count with SIM-G; each matches the output (lines 282-285).")
row("AC4-d-2.4-math-L07", "2.4-math", "course/modules/AC/AC4/L07.html Lemma 7.2 (lines 89-96), proof (line 98), §2 (lines 76-86), Theorem 7.3 (111-118), proof (line 120)", P,
    "Re-derived: D=E-min(E,K-q)=max(0,q+E-K) for q<=K; Delta_S(t)>=0 iff t>=t_min since q>0; Delta_B(t)>=0 iff t<=r; Sigma = q(r-v)-D(p_m-v) independent of t; t_min<=p_m by P2. No error found.")
row("AC4-d-2.4-math-L08", "2.4-math", "course/modules/AC/AC4/L08.html Definition 8.1 (lines 65-76), Lemma 8.2 (86), Lemma 8.3 (92), Proposition 8.4 (103-107), §3 (109)", P,
    "Re-derived: EVA-RI=-tau*OI; RI>=0 iff OI>=rC iff OI/C>=r for C>0; dRI=dOI-r dC and dEVA=(1-tau)dOI-r dC; dRI-dEVA=tau dOI, so equality only at tau=0 or dOI=0; with dOI<=0, tau<=1, r>0, dC>0 both fall. No error found.")
row("AC4-d-2.4-notation", "2.4-notation", "notation/notation.json (8 symbols, macros); course/modules/AC/AC4/L07.html, L08.html", P,
    "notation.json is byte-identical since 51fa336 and holds no AC4 symbol. The round-19 delta adds no symbol: L07 line 322 and 347 and P3 use only existing symbols (Sigma, Delta_S, Delta_B, t_min, D, q, K). L08 line 52 uses only OI and C, defined in §1.")

# ---- L07 concepts and text ----
row("AC4-d-L07-opportunity-cost-def", "2.4-math", "course/modules/AC/AC4/L07.html §1 (line 72), §2 (lines 98, 100)", P,
    "Definitions of displaced units, opportunity cost D(p_m-v) and per-unit cost D(p_m-v)/q match Lemma 7.2; the D=q and D=0 limits (line 100) are correct.")
row("AC4-d-L07-extra-capacity-scope", "2.4-math", "course/modules/AC/AC4/L07.html §4 (line 134)", P,
    "'When capacity binds (D > 0) and p_m > v, extra capacity lowers the supplier's floor and raises the surplus; when D = 0, it changes neither.' Re-derived: one more unit of K with D>0 lowers D by 1, so t_min falls by (p_m-v)/q and Sigma = q(r-v)-D(p_m-v) rises by (p_m-v) > 0; with D=0 extra K leaves D=0 and changes neither t_min nor Sigma. K=10000 to 12000 gives t_min 52 to 44 and Sigma 140000 to 180000 (matches). The buyer ceiling r does not move (t_max=r).")
row("AC4-d-L07-why-line52", "2.4-math", "course/modules/AC/AC4/L07.html why-it-matters (line 52)", P,
    "Re-read: 'the firm's gain from the sale does not depend on the price' matches Sigma (§3). Unchanged since 51fa336 (not in the delta).")
row("AC4-d-L07-misconception2-market-price", "2.4-math", "course/modules/AC/AC4/L07.html §7 misconception 2 (line 345) and L07q7 explanation (line 480)", P,
    "v=40, p_m=60, K=10000, E=8000, q=2000, r=55: D=0, t_min=40; Delta_B(60)=2000*(55-60)=-10000; Sigma=2000*15=30000 > 0; 40 to 55 is the feasible range. Matches the page.")
row("AC4-d-L07-R1-title", "2.9-structure", "course/modules/AC/AC4/L07.html R1 (lines 399-402)", P,
    "R1 solution: outside contribution p_m-v-c; Lemma 7.2 with that substitution gives t_min=v+D(p_m-v-c)/q; t_max=r unchanged since Delta_B does not involve outside sales. Consistent with §1 and §6.")
row("AC4-d-r3-L07-s1-s5-s6-text", "2.4-math", "course/modules/AC/AC4/L07.html §1 (line 70), §5 (lines 327), §6 bullets (lines 332-335)", P,
    "§5 counts 201=200+1, 14 with q>K, 187=75+112, 73/112=0.6518, and the 0.6518 is the generator's share; §6 bullets state the model limits (one period, outside sale available, no tax, hard capacity) and match §2's assumptions.")
row("AC4-d-r3-L08-why-and-s3-s5-text", "2.4-math", "course/modules/AC/AC4/L08.html why-it-matters (line 52), §1 OI/C paragraph (line 78), §3 (lines 98-109), §5 (lines 126-130)", P,
    "Re-read this round after the line-52 change (see AC4-d-r20-L08-line52): every term named (RI, EVA, OI/C, C, r, tau) is defined in §1 and the statements agree with Lemmas 8.2-8.3 and Proposition 8.4.")
row("AC4-d-L08-tau-zero-scope", "2.4-math", "course/modules/AC/AC4/L08.html §3 line 109 (after Proposition 8.4)", P,
    "'equal only when the tax rate is zero or the operating income does not change': dRI-dEVA = tau*dOI = 0 iff tau=0 or dOI=0 (tau >= 0). 'a choice that raises the base without raising operating income lowers both': dRI = dOI - r dC < 0 when dOI<=0, dC>0, r>0; dEVA = (1-tau)dOI - r dC < 0 when 0<=tau<=1. Scope words are justified.")
row("AC4-d-L08-base-sign-scope", "2.2-numbers", "course/modules/AC/AC4/L08.html §7 line 303 ('The base decides the level')", P,
    "At OI=120, r=9%: C=1000 gives RI=30; C=1400 gives RI=120-126=-6. Both values reproduced.")
row("AC4-d-L08-size-claim", "2.7-cards", "course/modules/AC/AC4/L08.html §8 misconception 3 (lines 318-319); cards AC4-c102", P,
    "RI = OI - rC: SIM-D 7030 - 0.09*124000 = -4130 and SIM-A 2870 - 0.09*59000 = -2440, both reproduced; returns 7030/124000 = 5.67% and 2870/59000 = 4.86% (both below 9%, so both RI negative by Lemma 8.3); §5 X and Y values 15 and 20 reproduced.")
row("AC4-d-L08-quiz-agreement-claim", "2.9-quiz", "course/modules/AC/AC4/L08.html quiz L08q5 explanation (line 438)", P,
    "'With a common base the orders agree. With different bases they can disagree, as 4 of the 28 pairs in Lab 1 do.' The eight SIMULATED bases are all distinct (C column of Lab 1 output), so each of the 4 discordant pairs has different bases; statement holds.")
row("AC4-d-r2-L08-lab-pair-scope", "2.5-labs", "course/modules/AC/AC4/L08.html §5 paragraph after 'same base' sentence (line 130)", P,
    "Lab 1 counts all 28 pairs of 8 divisions; a tie in either measure is not counted (code: 'and by_ri != 0 and by_ratio != 0'); zero ties occur on seed 20261027 (" + S + "ties_and_equiv_r20.out: 'pairs with a tie in either measure 0'). The C column has eight distinct values.")
row("AC4-d-L07-uses-undeclared", "2.9-dag", "course/modules/AC/AC4/L07.html line 38 (meta 'Uses:')", P,
    "'Uses: contribution margin' is defined at course/modules/AC/AC4/L01.html (dfn id def-contribution-margin), an earlier lesson of the same unit. check_dag.py --all: PASS.")
row("AC4-d-L08-uses-undeclared", "2.9-dag", "course/modules/AC/AC4/L08.html line 38 (meta 'Uses:')", P,
    "'Uses: the income statement, the balance sheet' are defined in course/modules/AC/AC1/L02.html (def-income-statement, def-balance-sheet), a prerequisite unit. check_dag.py --all: PASS.")
row("AC4-d-2.9-dag-definitions", "2.9-dag", "L07.html dfn transfer-pricing (line 69); L08.html dfn residual-income and economic-value-added (lines 67, 71)", P,
    "Each concept is defined once (dfn with data-concept) in the module that introduces it; 'Introduces' lines 39 (L07) and 39 (L08) agree.")
row("AC4-d-L08-misconception1-C-positive", "2.4-math", "course/modules/AC/AC4/L08.html §8 misconception 1 (line 314)", P,
    "'residual income is nonnegative exactly when OI/C >= r' for C>0 (Lemma 8.3); 30 to 102.8 SCU reproduced (§4).")
row("AC4-d-2.9-hours", "2.9-hours", "course/modules/AC/AC4/L07.html and L08.html data-hours (line 2); course/modules/AC/AC4/index.html data-hours-lessons=50, data-hours-project=20", P,
    "Lesson hours L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6 sum to 50 = hub data-hours-lessons; 50+20=70 = curriculum hours (curriculum/02-economics-finance-core.yaml (AC4 entry, hours: 70)). No hub-to-lesson arithmetic inconsistency. Pace estimate not used as a failure (architect ruling).")
row("AC4-d-2.8-data", "2.8-data", "course/modules/AC/AC4/L07.html, course/modules/AC/AC4/L08.html (no data-files attribute)", P,
    "grep -c data-files on both pages: 0 and 0 (re-run this round).")
row("AC4-d-2.9-prose-banned", "2.9-prose", "course/modules/AC/AC4/L07.html, course/modules/AC/AC4/L08.html learner prose outside code blocks", P,
    "Grep this round for roughly, about <digit>, historically, typically, usually, ellipses, builder, verifier, round, requests, build, most, often, half: no learner-text hit in either page (only code comments and the word 'round' inside ROUND_HALF_UP). Every scope word in the two pages was read in context (see AC4-d-r20-scope-words).")
row("AC4-d-r20-scope-words", "2.9-prose", "course/modules/AC/AC4/L07.html and L08.html: every only/all/every/always/exactly/same/none-type word in learner text", P,
    "Grep of the learner text (pattern: only, all, every, always, exactly, same, drives, offsets, raises, as much as) this round; every returned line was read in context. Each use is true as written, or is a stated model assumption or a labelled misconception. The two previously overreaching sentences are fixed (AC4-d-r17-prose-scope-words). See the rows AC4-d-r20-L07-hunk-* and AC4-d-r20-L08-line52 for the changed sentences.")
row("AC4-d-r17-process-words", "2.9-prose", "course/modules/AC/AC4/L07.html, course/modules/AC/AC4/L08.html learner text", P,
    "No process words (build, builder, round, verifier, REQUESTS, unit report) in learner text; re-checked after the delta.")
row("AC4-d-r17-prose-scope-words", "2.9-prose", "course/modules/AC/AC4/L07.html line 322 and line 347 (the two sentences flagged in round 19)", P,
    "Both sentences now read 'excluded from every check line' (line 322) and 'holds for every t, by the computation in §3 and P1 (Theorem 7.3 part 3 states it for t in the range)' (line 347). Both are true: the 14 q>K pairs appear in the printed count line 'cases with q > K (no transfer): 14' and the table, and the four check lines exclude them (twin lines 286-300).")
row("AC4-d-2.5-lab-L07", "2.5-labs", "course/modules/AC/AC4/L07.html Lab 1 hypothesis (line 140), §4 lead-in (line 136), interpretation (line 322); tests/labs/AC4/lab-AC4-L07-1.py", P,
    "Hypothesis matches the twin: supplier-gain zero at t_min (exact Fraction), nonempty iff Sigma>=0 (integer surplus), sum identity at t_min, t_max and the midpoint, boundary pair with Sigma=0 printed 'nonempty True'. Interpretation sentence now reads 'every check line' and matches the output.")
row("AC4-d-2.5-lab-L08", "2.5-labs", "course/modules/AC/AC4/L08.html Lab 1 hypothesis (line 134), interpretation (line 291); tests/labs/AC4/lab-AC4-L08-1.py", P,
    "Hypothesis: identity holds for each generated division (8/8 printed); sign identity at equality for the boundary (9/9 printed, boundary RI 0.00 True True); pair count 4 of 28 and the capitalization lines. Each sentence matches a printed line; 'does not evaluate Proposition 8.4' is true (no Prop 8.4 line in the code).")
row("AC4-d-r17-boundary-L07", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py lines 218-219 (nonempty), 229 (BOUNDARY), 254 (cases list)", P,
    "nonempty(c) is t_min<=t_max; BOUNDARY is v=4000, p_m=6000, K=10000, E=8000, q=5000, r_net=5200 so t_min=t_max=5200 and Sigma=0; output 'nonempty True, firm-wide surplus 0 cents'. Equality tested.")
row("AC4-d-r17-boundary-L08", "2.5-labs", "tests/labs/AC4/lab-AC4-L08-1.py BOUNDARY (line 206) and sign_ok (line 238)", P,
    "BOUNDARY = Division(C=1000, OI=90): OI/C = 9% = r, RI = 0; sign_ok includes it; printed 'RI >= 0 exactly when OI/C >= r holds for 9/9 divisions, boundary included'.")
row("AC4-d-r17-mutants-killed", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17 (9), AC4-d-r18 (26), AC4-d-r19 (11), AC4-d-r20 (4)", P,
    f"Transplant of every one-line lab mutant onto the current twins (" + S + "transplant_r20.out): 30 KILLED output-differs, 2 SURVIVED (both equivalent, see AC4-d-r20-equivalent-survivors), 14 NOT-TRANSPLANTABLE because their target line no longer exists in the current twin (the current twins contain no assert statement; each is superseded by a carried semantic mutant that is killed, see AC4-d-r20-superseded-mutants).")
row("AC4-d-r17-mutant-L08-m04-ties", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17/r17_L08_m04_discord_ignores_ties.py", P,
    "Equivalent on the shipped seed: ties_and_equiv_r20.out shows 0 pairs with a tie in either measure among 28 pairs; the mutant only differs when a tie exists. Out of the mutants list (equivalent).")
row("AC4-d-r17-alternatives", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r19/alts/ (4) and ledgers/AC4/scripts/AC4-d-r20/alts/ (3)", P,
    "Seven alternative correct implementations (midpoint as offset, nonempty via Sigma, discord by product sign, sign by cross-multiplied integers, displaced via min, nonempty via integer cross-product, EVA via Lemma 8.2) all run with exit 0 and print the embedded expected output exactly (outputs this round). No over-constraint.")
row("AC4-d-r18-L07-boundary-both-strict", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py nonempty (line 218-219) and sign line (line 147)", P,
    "Both the nonempty test and the sign test are non-strict at equality; the boundary pair is printed nonempty True and counted in the sign line. Mutants r18_carry_L07_nonempty_strict and r17/n10-style strict counts are killed (mutants_rerun / transplant_r20.out).")
row("AC4-d-r18-L07-checks-not-in-output", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py lines 286-300 (printed check lines); page expected block lines 318-321", P,
    "The four check lines are printed from computed counts (supplier_zero, sign_match, midpoint_inside, sum_identity); the page's key-results and interpretation sentences name the four lines correctly.")
row("AC4-d-r18-L07-midpoint-test-point", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py midpoint (line 222-224) and sum identity (lines 289-296); output line 320", P,
    "midpoint(c) = (t_min+t_max)/2 and the sum identity is tested at (t_min, t_max, midpoint). The output 'midpoint of the range lies inside it: 112/112' is produced from this code. Mutant r18_carry_L07_midpoint_not_halved is killed.")
row("AC4-d-r18-L07-E1-wording", "2.9-prose", "course/modules/AC/AC4/L07.html E1 solution (line 387)", P,
    "'75/187 = 0.4011' (recomputed); 'the boundary pair is not empty' (t_min=t_max); 'a different seed could give a different share' (seed scan shows shares change: seed 22 has 73 empty of 186 fits).")
row("AC4-d-r18-L08-section3-later-periods", "2.4-math", "course/modules/AC/AC4/L08.html §3 line 98 ('starting with the first-year charge in the period of the outlay, as in §4') and §4 capitalized case (lines 117-122)", P,
    "§4 charges 20 SCU in the first year (outlay 100 over five years) and applies the change to the period's operating income; §3 does not claim later-period charges are modelled (§7 bullet 3 says so).")
row("AC4-d-r18-L08-section7-tax-effect", "2.4-math", "course/modules/AC/AC4/L08.html §7 bullet 'Tax and book treatment' (line 306); tests/labs/AC4/lab-AC4-L08-1.py capitalized() docstring", P,
    "The lab's capitalized() applies TAX_BP to the changed OI and does not model a book/tax difference; the page says the same.")
row("AC4-d-r18-mutants-run", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r18/ (26 files)", P,
    "Transplanted and re-run this round (" + S + "transplant_r20.out). Direct runs of the old-pin copies (" + S + "mutants_rerun_r20.out) differ from the embedded output only because each copy is the old twin; the transplant is the valid method (ledger note from round 19 retained).")
row("AC4-d-r18-equiv-L08-n09", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r18/L08_n09_discord_pairs_same_name_order.py", P,
    "The mutant includes self pairs (a.name <= b.name). A self pair has zero differences in both measures (ties_and_equiv_r20.out: 'self-pair differences (0, 0) counted ... False'), so the strict-disagreement test never counts it. Equivalent; out of the mutants list.")
row("AC4-d-r18-L08-mutants-killed", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r18/L08_n01..n08 (transplanted)", P,
    "L08_n01 to L08_n08 each transplanted and killed by output difference (transplant_r20.out).")

# ---- cards ----
row("AC4-d-r17-cards-scope", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c082..c134 (L07 and L08)", F,
    "Every L07/L08 card re-read against the current lesson text this round. Only AC4-c095 has a stale basis (line 674, 'the exact-check line' names a line the lab does not print) and AC4-c089 has an attribution that now overreaches (see AC4-d-r20-card-c089). Other cards agree with the lesson.",
    "In course/modules/AC/AC4/cards.json line 674 replace 'the exact-check line' with 'the four check lines'; and fix AC4-c089 as in AC4-d-r20-card-c089; then re-run check_pages and check_projects.")
row("AC4-d-r17-cards-cover", "2.7-cards", "course/modules/AC/AC4/cards.json: L07 cards c082..c096 and c117, L08 cards c097..c109, c113..c116, c129, c134", P,
    f"{S}cards_scan_r20.out: 134 cards, no duplicate id, front or back; L07 16 cards (c082-c096, c117); L08 19 cards (c097-c109, c113-c116, c129, c134). Re-counted this round.")
row("AC4-d-r6-cards-dup-scan", "2.7-cards", "course/modules/AC/AC4/cards.json (134 cards)", P,
    f"{S}cards_scan_r20.out: duplicate ids [], duplicate fronts [], duplicate backs []; grade C cards all carry a basis.")
row("AC4-d-r17-cards-c091-changed", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c091 (back); course/modules/AC/AC4/L07.html Theorem 7.3 part 1 (line 114)", P,
    "'Exactly the prices t in [t_min, t_max]... outside it at least one gain is negative (Theorem 7.3, part 1)' matches the theorem (both gains nonnegative exactly on the interval, Lemma 7.2).")
row("AC4-d-r17-cards-c102-changed", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c102 (back); course/modules/AC/AC4/L08.html misconception 3", P,
    "'For two divisions with the same return on capital above the rate, the larger one has the larger residual income, because RI = (OI/C - r)C' matches misconception 3 (line 318).")
row("AC4-d-r17-cards-c129-c134-new", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c129, AC4-c134; course/modules/AC/AC4/L08.html §5 (lines 128)", P,
    "X: C=500, OI=60, r=9%, RI=15 (60-45); Y: C=2000, OI=200, RI=20 (200-180). Matches §5.")
row("AC4-d-r17-boundary-probe", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r18/seeds.py (equality scan) re-read; tests/labs/AC4/lab-AC4-L07-1.py", P,
    "Equality scan re-run this round (" + S + "equality_scan_r20.py, equality_scan_r20.out): no generated pair with q<=K has t_min == t_max for seeds 1..40 or for the shipped seed; the hand-built BOUNDARY is the only equality pair. The nonempty test is non-strict (twin line 219).")
row("AC4-d-2.7-cards-L07-L08", "2.7-cards", "course/modules/AC/AC4/cards.json: L07 c082..c096, c117; L08 c097..c109, c113..c116, c129, c134", F,
    "Re-checked each card against the current lesson text. Failing cards: AC4-c095 (basis names a line the output does not print) and AC4-c089 (Theorem 7.3 part 3 cited for 'every price'). All other cards in the range agree.",
    "Fix AC4-c095 basis (line 674) and AC4-c089 back, as in AC4-d-r17-cards-scope and AC4-d-r20-card-c089.")
row("AC4-d-2.7-cards-c088-outside-option", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c088 (back); course/modules/AC/AC4/L07.html §7 misconception 2 (line 345)", P,
    "v=40, p_m=60, K=10000, E=8000, q=2000, r=55: D=0, t_min=40, buyer gain -10000, Sigma 30000. Card back matches the lesson.")
row("AC4-d-2.7-cards-c100-lemma83", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c100 (back); course/modules/AC/AC4/L08.html §8 misconception 1 (line 314)", P,
    "Card back matches the lesson: RI nonnegative iff OI/C >= r for C>0; 30 to 102.8 SCU.")
row("AC4-d-r3-L07-cards-c117", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c117; course/modules/AC/AC4/L07.html §4 line 134 and M2 (line 361)", P,
    "K=12000: D=1000, t_min=40+1000*20/5000=44; matches M2 and the §4 extra-capacity paragraph.")
row("AC4-d-r3-L08-cards-c113-c116", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c113..c116; course/modules/AC/AC4/L08.html §4, §5, §6", P,
    "c113 (SIM-A/SIM-D rows), c114 (SIM-G row), c115 (72.8, 30 to 102.8), c116 (56.8, 6 to 62.8) all match the lesson and the output.")
row("AC4-d-2.1-citations-L07-L08", "2.1-citations", "course/modules/AC/AC4/L07.html References (line 509); course/modules/AC/AC4/L08.html References (line 480)", P,
    "Both pages state that they cite no registry source; no citation key appears in either page. verify_refs live and offline PASS (" + S + "vr_live.out, vr_off.out).")
row("AC4-d-L08-why-capital-charge-rate", "2.9-dag", "course/modules/AC/AC4/L08.html why-it-matters, line 52", P,
    "Re-read after the change (AC4-d-r20-L08-line52): the capital-charge rate and tax rate are named as inputs defined in §1; residual income and EVA are defined in §1; no concept is used before its definition.")
row("AC4-d-r17-cards-scope-ok", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c082, AC4-c095, AC4-c108", F,
    "c082 and c108 agree with the lesson and the output. c095 does not: its basis ('the exact-check line') names a line the lab no longer prints, so the card is not correct as written.",
    "Fix AC4-c095 basis (cards.json line 674): 'output lines for the counts and the four check lines'.")
row("AC4-d-r19-L07-every-line-scope", "2.9-prose", "course/modules/AC/AC4/L07.html line 322 (interpretation after Lab 1 output)", P,
    "Now reads 'excluded from every check line'. The 14 q>K pairs are excluded from the four check lines (supplier-gain and sign over fits, midpoint and sum over feasible), and are counted in 'cases with q > K (no transfer): 14', which is not a check line. True as written.")
row("AC4-d-r19-L07-theorem-part3-every-t", "2.4-math", "course/modules/AC/AC4/L07.html §7 misconception 3, line 347", P,
    "Now cites the §3 computation and P1 for 'every t' and says Theorem 7.3 part 3 states it for t in the range. Matches Theorem 7.3 part 3 (line 116) and P1 (line 372). True as written.")
row("AC4-d-r19-cards-c095-basis", "2.7-cards", "course/modules/AC/AC4/cards.json line 674 (AC4-c095 basis)", F,
    "Still 'Lab 1 (SIMULATED), output lines for the counts and the exact-check line' in the round-20 checkout (cards.json is byte-identical since 51fa336). The printed output ends with four check lines (supplier gain, sign, midpoint, sum) and has no 'exact-check' line (" + S + "twin_L07_r20.out, last four lines).",
    "Replace 'the exact-check line' with 'the four check lines' in cards.json line 674; re-run check_pages and check_projects.")
row("AC4-d-r19-mutants-rerun", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17 (9), AC4-d-r18 (26), AC4-d-r19 (11)", P,
    "All re-run this round through the transplant method (" + S + "transplant_r20.out): 30 killed, the 2 equivalent survivors recorded, the rest superseded or killed by carries.")
row("AC4-d-r19-m19-new-mutants", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r19/m19_*.py (4 new student-error mutants)", P,
    "m19_L07_t_min_divides_by_capacity, m19_L07_firm_surplus_uses_buyer_ceiling_price, m19_L08_first_year_charge_over_life_plus_one, m19_L08_residual_income_after_tax: all four transplanted and killed by output difference (transplant_r20.out).")
row("AC4-d-r19-alts", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r19/alts/ (4 alternatives)", P,
    "Re-run this round: all four exit 0 and match the embedded expected output exactly.")
row("AC4-d-r19-seed-scan", "2.2-numbers", "ledgers/AC4/scripts/AC4-d-r20/seed_scan_r20.py and seed_scan_r20.out (round-19 seed_scan.py superseded by this re-derivation)", P,
    "Re-derived for seeds 1 to 40 from the twins' own generators: the L08 seeds giving 4 discordant pairs are 14, 20, 26, 28; the L07 seeds with 186 fits and 75 empty are none.")
row("AC4-d-r19-L08-period-convention", "2.4-math", "course/modules/AC/AC4/L08.html §3 line 98 and §4 worked capitalization (lines 115-122)", P,
    "'starting with the first-year charge in the period of the outlay, as in §4' matches §4: reported OI 120 already charges the outlay in full; the capitalized first-year charge is 20; the lab docstring says 'first year only'.")

# ---- new rows this round ----
row("AC4-d-r20-L07-hunk-line65", "2.4-math", "course/modules/AC/AC4/L07.html line 65 (§1 after the list)", P,
    "'The model assumes that the fixed costs of both divisions do not change with the sale.' Consistent with §2 (no fixed cost enters Delta_S or Delta_B) and misconception 1 (line 343: 'Full cost includes fixed overhead, which does not change with the sale'). A stated assumption, not a derived claim.")
row("AC4-d-r20-L07-hunk-line322", "2.9-prose", "course/modules/AC/AC4/L07.html line 322 (interpretation of Lab 1)", P,
    "Re-derived: supplier-gain and sign lines count over fits (187 = 186 generated with q<=K + boundary); midpoint and sum lines over feasible (112). 'excluded from every check line' is true for all four check lines (twin lines 286-296 use fits or feasible only).")
row("AC4-d-r20-L07-hunk-line347", "2.4-math", "course/modules/AC/AC4/L07.html §7 misconception 3, line 347", P,
    "'The identity holds for every t, by the computation in §3 and P1 (Theorem 7.3 part 3 states it for t in the range).' §3 line 104-108 derives the identity for any t; P1 proves it for every t; Theorem 7.3 part 3 (line 116) is for t in the range. Statement and locators are correct.")
row("AC4-d-r20-L07-hunk-P3", "2.4-math", "course/modules/AC/AC4/L07.html P3 (lines 377-380)", P,
    "Now 'Suppose v = 0 and q <= K'. The solution uses Lemma 7.2, which needs q > 0 (a standing input in §1 line 62); t_min = D p_m/q; t_min <= r iff D p_m <= q r; Sigma = qr - D p_m. Correct; the added q <= K is the Lemma hypothesis.")
row("AC4-d-r20-L08-line52", "2.4-math", "course/modules/AC/AC4/L08.html why-it-matters (line 52)", P,
    "Now: 'A division's profit is an amount, and its operating income per unit of capital is a ratio.' The ratio is defined at line 78 as operating income earned per unit of capital (OI/C). The old 'return' wording is gone. The rest of the paragraph (two measures defined in §1, rate and tax rate as inputs, identities) agrees with §1-§3. No new claim.")
row("AC4-d-r20-card-c089-theorem-scope", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c089 (back)", F,
    "The back says 'The two gains sum to the firm-wide surplus for every price: ... (Theorem 7.3, part 3)'. Theorem 7.3 part 3 (L07.html line 116) states the sum identity 'for every t in the range'. The lesson's corrected misconception 3 (line 347) now says the identity holds for every t by §3 and P1 and that Theorem 7.3 part 3 states it for t in the range. The card attributes the every-price scope to the theorem alone, the same overreach the lesson fix removed.",
    "In cards.json AC4-c089 back, replace '(Theorem 7.3, part 3)' with '(the identity in Section 3 and P1; Theorem 7.3, part 3, states it for prices in the range)'.")
row("AC4-d-r20-equivalent-survivors", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17/r17_L08_m04_discord_ignores_ties.py; ledgers/AC4/mutants/AC4-d-r18/L08_n09_discord_pairs_same_name_order.py", P,
    "Both survive the transplant but are output-equivalent on the shipped seed: 0 ties (ties_and_equiv_r20.out) and self pairs have zero differences in both measures, so neither mutant changes any printed line. Out of the mutants list (equivalent). The lesson sentence 'a tie in either measure is not counted' is true of the shipped code.")
row("AC4-d-r20-superseded-mutants", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17/r17_L07_m03, r17_L08_m02; AC4-d-r18/boundary_strict_only, del_biconditional, del_buyer_assert, del_sum_assert, del_supplier_assert, L08_n07, n03, n07, n08, n10, n11, n12", P,
    "Their target lines are absent from the current twins (no assert statement exists in tests/labs/AC4/lab-AC4-L07-1.py or L08; grep -c assert = 0). Each semantic change is carried on the current twin and killed: r18_carry_L07_empty_count_ge (n10, r17_L07_m03), r17_carry_L08_ratio_ge_strict (r17_L08_m02), r18_carry_L08_ri_side_strict (L08_n07), r18_carry_L07_nonempty_strict (boundary_strict_only, n03), r18_carry_L07_midpoint_not_halved (n07), r18_carry_L07_feasible_strict (n11), r18_carry_L07_skip_boundary_checks (n12). The del_* removals of assert statements have no counterpart in the current twins (the checks are printed counts, and removing one changes a printed line).")
row("AC4-d-r20-lab-midpoint-survivor", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r20/m20_L07_midpoint_check_uses_lower_end.py; tests/labs/AC4/lab-AC4-L07-1.py lines 289-296", P,
    "Survives: replacing the midpoint by t_min leaves the printed output unchanged, because the printed midpoint line is computed from the same counts. The lesson hypothesis (line 140) and the printed line claim the sum identity is checked at the midpoint, and the shipped code does check it (sum_identity iterates over (t_min, t_max, midpoint(c))). The claim holds for the shipped twin; a lab-twin survivor that does not falsify a shipped claim is out of scope (architect ruling). Recorded here, not in the mutants list.")
row("AC4-d-r20-new-mutants", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r20/ (m20_L07_displaced_forgets_internal_order, m20_L07_sign_check_strict_at_zero, m20_L08_eva_taxes_residual_income, m20_L07_midpoint_check_uses_lower_end)", P,
    "Four new student-error mutants written this round. Three are killed by output difference (m20_L07_displaced_forgets_internal_order: D drops to the external-only excess; m20_L07_sign_check_strict_at_zero: sign line 187/187 becomes 186/187 at the boundary; m20_L08_eva_taxes_residual_income: EVA values change). The fourth survives and is recorded as AC4-d-r20-lab-midpoint-survivor.")
row("AC4-d-r20-alts", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r20/alts/ (alt20_L07_displaced_via_min, alt20_L07_nonempty_via_integer_cross_product, alt20_L08_eva_via_lemma_8_2)", P,
    "Three fresh alternative correct implementations; each exits 0 and prints the embedded expected output exactly (no over-constraint).")
row("AC4-d-r20-indep-recompute", "2.2-numbers", "ledgers/AC4/scripts/AC4-d-r20/indep_integer_recompute_r20.py", P,
    "Independent integer-only recomputation of the Lab 1 counts (L07: 14/75/112/73, boundary surplus 0; L08: discordant 4 of 28, every printed EVA and RI cell reproduced) and of the worked-case figures.")
row("AC4-d-r20-delta-hunk-check", "2.9-structure", "git diff 51fa336 fd9a9b7 for L07.html and L08.html (5 hunks)", P,
    "Every hunk read in full context; the five changed sentences are covered by AC4-d-r20-L07-hunk-line65, -line322, -line347, -P3 and AC4-d-r20-L08-line52. No other change in the slice.")

# ---- previous ids not rewritten above: carry or re-verify ----
missing = [i for i in prev_ids if i not in rows]
for i in missing:
    raise SystemExit(f"no decision for previous id {i}")

out_rows = [rows[i] for i in prev_ids] + [rows[i] for i in rows if i not in prev_ids]

mutant_list = []
text = (ROOT / "ledgers/AC4/scripts/AC4-d-r20/transplant_r20.out").read_text(encoding="utf-8")
for line in text.splitlines():
    m = re.match(r"^(r17|r18|r19) (\S+): KILLED (.*?)(\s*\|.*)?$", line)
    if m:
        rnd, name, verdict = m.group(1), m.group(2), m.group(3)
        folder = {"r17": "AC4-d-r17", "r18": "AC4-d-r18", "r19": "AC4-d-r19"}[rnd]
        mutant_list.append({
            "id": f"{rnd}:{name}",
            "description": f"Lab-twin mutant ({rnd} round), transplanted onto the current twin (round 20)",
            "file": f"ledgers/AC4/mutants/{folder}/{name}",
            "killed_by": f"transplanted onto current twin: {verdict}",
        })
for name, desc in [
    ("m20_L07_displaced_forgets_internal_order.py", "Student error: displaced units ignore the internal order q (max(0, E - K))."),
    ("m20_L07_sign_check_strict_at_zero.py", "Student error: sign check uses Sigma > 0 instead of Sigma >= 0."),
    ("m20_L08_eva_taxes_residual_income.py", "Student error: EVA computed as (OI - rC)(1 - tau)."),
]:
    mutant_list.append({
        "id": "r20:" + name[:-3],
        "description": desc,
        "file": f"ledgers/AC4/mutants/AC4-d-r20/{name}",
        "killed_by": "output differs from the embedded expected block (direct run, round 20)",
    })

n_killed = len(mutant_list)
frag = {
    "unit": "AC4",
    "slice": "AC4-d",
    "round": 20,
    "verifier": "round-20 independent Haiku verifier for slice AC4-d (L07, L08 and their lab twins); did not build AC4 and shares no context with its builders",
    "pin": "fd9a9b7",
    "base": "51fa336 (previous pin; round-19 fragment /tmp/fanout-frags/AC4-d.round19.json used as context; its PASS rows re-verified or carried only where the cited passage is byte-identical)",
    "checkout": "/tmp/verify20-AC4-d (detached worktree at fd9a9b7, .venv symlink, vendor copied)",
    "scratch": "/tmp/ac4d-r20 (command outputs; copies in ledgers/AC4/scripts/AC4-d-r20/)",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": out_rows,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 51fa336..fd9a9b7 for the slice: L07.html hunks at lines 65, 322, 347 and P3 (378); L08.html hunk at line 52. tests/labs/AC4/*, cards.json, notation.json unchanged.",
        "Round-19 FAILs resolved: AC4-d-r17-prose-scope-words, AC4-d-2.5-lab-L07, AC4-d-r19-L07-every-line-scope, AC4-d-r19-L07-theorem-part3-every-t (all four fixed in L07.html and re-verified).",
        "Still FAIL: the AC4-c095 basis ('the exact-check line') in cards.json line 674 (AC4-d-r19-cards-c095-basis, AC4-d-r17-cards-scope, AC4-d-2.7-cards-L07-L08, AC4-d-r17-cards-scope-ok). cards.json is unchanged since round 19, so the defect persists.",
        "New FAIL: AC4-c089 back cites Theorem 7.3 part 3 for 'every price' (AC4-d-r20-card-c089-theorem-scope).",
        "Lab-twin survivor AC4-d-r20-lab-midpoint-survivor (midpoint replaced by lower end) is recorded as PASS under the architect ruling: the shipped code checks the midpoint and the claim holds for it. The orchestrator may wish to decide whether a lab survivor of a claimed check needs a stronger twin.",
        "Equivalent survivors (r17_L08_m04, L08_n09) and superseded/not-applicable mutants (del_* assert removals, the twins contain no assert) are documented in rows, not in the mutants list.",
        "ledgers/AC4/mutants/AC4-d-r20 holds four files; the m20_L07_midpoint file is a survivor and is not counted as killed.",
        "The round-20 run_mutants_r20.py output lists also the project-slice grader mutants (fx*, m*, r13e-r18e, AC4-e and AC4-a folders) as 'page ?'; they belong to other verifiers' slices and were not counted.",
    ],
    "summary": {},
    "mutants": mutant_list,
}
counts = {"PASS": 0, "FAIL": 0}
for r in out_rows:
    counts[r["status"]] += 1
frag["summary"] = {"rows": len(out_rows), "pass": counts["PASS"], "fail": counts["FAIL"], "mutants_killed": n_killed}
Path(ROOT / "ledgers/AC4/AC4-d.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(out_rows), "pass", counts["PASS"], "fail", counts["FAIL"], "mutants killed", n_killed)
print("previous ids covered:", all(i in rows for i in prev_ids))
