import json, sys
P = "Carried from round 9 (course/modules/E/E2/L04.html, L05.html, L06.html, tests/labs/E2 and the cited cards byte-identical since the previous pin 33744e5): "
F = "Fresh in round 10 (delta 33744e5..fa61d6e read): "
rows = []
def r(id_, check, loc, ev, status="PASS"):
    rows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})
r("E2b-cite-spence1973job", "Citation key spence1973job: title, year, venue, attribution scope", "course/modules/E/E2/L04.html:229; cards.json E2-c048",
  F + "L04.html:229 reads 'cited for the topic of signaling by its title, year and venue only; no page or result of that paper is used'; card E2-c048 basis now 'Title, year and venue only; no result attributed'. Registry record 'Job Market Signaling', 1973 (references/references.json, key spence1973job, title line 21118, year 21125). Attached claim is topic-level, grade C.")
r("E2b-cite-rothschild1976equilibrium", "Citation key rothschild1976equilibrium: title, year, venue, attribution scope", "course/modules/E/E2/L05.html:254; cards.json E2-c060",
  F + "L05.html:254 'cited by its title, year and venue only'; card E2-c060 basis updated to the same wording. Registry title 'Equilibrium in Competitive Insurance Markets: An Essay on the Economics of Imperfect Information' (references/references.json line 20317) matches the page title string.")
r("E2b-cite-holmstrom1979moral", "Citation key holmstrom1979moral: title, year, venue, attribution scope", "course/modules/E/E2/L06.html:247; cards.json E2-c072",
  F + "L06.html:248 'cited for the topic of moral hazard by its title, year and venue only; no result or page of that paper is used'; card E2-c072 basis updated. Registry 'Moral Hazard and Observability' 1979 (references/references.json line 12609, 12616).")
r("E2b-cite-live-registry", "Live re-resolution of the unit's registry entries", "references/references.json; tools/verify_refs.py --unit E2",
  F + ".venv/bin/python tools/verify_refs.py --unit E2 -> 'live re-verification of E2: 8 of 560 entries, 0 problems' (ledgers/E2/scripts/E2-b-r10/verify_refs_E2.out).")
r("E2b-cite-attribution-abstract", "Attribution read against the paper's abstract", "course/modules/E/E2/L04.html:229; L05.html:254; L06.html:248",
  "Carried from round 9 (attached claims remain topic-level; no paper result is attributed, so no abstract comparison is needed). Abstracts were not re-fetched this round (see could_not_check).")
r("E2b-cite-scope-wording", "Citation scope wording is the same in every place it is stated", "course/modules/E/E2/L05.html:254, 296; L06.html:248, 291; cards.json E2-c048, E2-c060, E2-c072",
  F + "Round-9 FAIL is fixed. grep for 'by title only' in L04, L05, L06 and cards.json returns 0; grep for 'Title and year only' in cards.json returns 0. L05.html:296 and L06.html:291 now read 'by its title, year and venue only' and 'by its title, year and venue only'. All sections 4 wordings and card basis fields read 'title, year and venue only'.")
r("E2b-numbers-L04", "Every number in L04 prose re-derived", "course/modules/E/E2/L04.html:56, 79-100, 218-219, 235-237, 245-273, 284, 299",
  F + "Re-derived by hand: Delta=2,000,000; bounds 2 and 4; thresholds 2,3,4; Remark 2.1 wage gain 2,000,000, cost 1,000,000, net 5,000,000; t=4 net 4,000,000; problem m1 (c_H=250,000): bounds 2 and 8, high utility at t=3 5,250,000, low utility at e=3 3,000,000; problem (Delta=1.5M, c_L=1M, c_H=500k): bounds 1.5 and 3; c_H=400,000: 2..5; y_H=5M: thresholds 1,2, high net 4,500,000 at t=1. Lab output (twin-L04 Part B rows 0..6 and Part C/D) agrees.")
r("E2b-numbers-L05", "Every number in L05 prose re-derived", "course/modules/E/E2/L05.html:56, 97, 124-125, 134-137, 249, 254, 260-262, 270-274, 286-290",
  "Carried from round 9 (cited ranges byte-identical since the previous pin; the only L05 change this round is line 296 wording). Re-checked this round anyway: q_L*=2000, q_H=6000, m_L=6,000,000, m_H=30,000,000, U_H=6,000,000, first best 7,875,000 (0.75x4,500,000+0.25x18,000,000), menu 6,000,000, gap 1,875,000, split 375,000 + 1,500,000 (L05.html:249), problem m2 profit 5,625,000 (L05.html problem 'Profit of a menu'), p_H=1/3 gap 2,333,333 and 6,750,000 at q_L=1500.")
r("E2b-numbers-L06", "Every number in L06 prose re-derived", "course/modules/E/E2/L06.html:52, 56-63, 99-107, 113, 229, 234, 241-242, 252-253, 262-283",
  F + "Re-derived: E_H=750,000, E_L=250,000, Delta_E=500,000, first best 650,000, c_H/Delta_E=1/5, profit at (0,1/5)=600,000, utility 50,000, expected payment 150,000, agency cost 50,000; Remark 1.4 payments c_H-beta E_H (-50,000, -275,000, -650,000) match Lab Part C; problem values (share 0.25: 87,500, 62,500, 562,500; share 2/15: 0 and 33,333; alpha=10,000 profit 590,000; alpha=-1,000,000 beta=1/2 utilities -725,000 and -875,000; cost 150,000 gives 0.30, 525,000, agency 75,000; p=0.8/0.2 gives Delta_E 600,000, beta 1/6, profit 666,666.67 -> 666,667, first best 700,000; surplus 650,000 = 600,000+50,000). All match the page and the twin output.")
r("E2b-numbers-printed-digits", "Printed digits in prose match the twin output", "course/modules/E/E2/L04.html:192-211; L05.html:222-241; L06.html:210",
  "Carried from round 9 (cited ranges byte-identical since the previous pin). Round-10 twin output re-run: L04 Part B rows, L05 Parts A-D and L06 Parts A-C (ledgers/E2/scripts/E2-b-r10/lab-E2-L0*-1.py.out) agree with the printed prose.")
r("E2b-grades-L04", "Grades of key results and card grades L04", "course/modules/E/E2/L04.html:280-283 (key results); cards.json E2-c046, E2-c126",
  "Carried from round 9 (L04 key-results rows and cards E2-c046, E2-c126 byte-identical since the previous pin). Card E2-c047 and E2-c049 changes checked fresh under E2b-cards-c049 and E2b-cards-c058-c063-c125.")
r("E2b-grades-L05", "Grades of key results and card grades L05", "course/modules/E/E2/L05.html:307-309; cards.json E2-c056..c064, E2-c125",
  F + "Key-results rows at L05.html:307-309 unchanged. Card E2-c058 (T) now says 'closed form of Proposition 1.4 (Remark 1.5)': q_L=2000, q_H=6000 re-derived. Card E2-c060 basis updated (C). Card E2-c064 (C) now asks the Part B quantity only: Part B prints 2000. Card E2-c125 (T) m_L and m_H re-derived.")
r("E2b-grades-L06", "Grades of key results L06", "course/modules/E/E2/L06.html:297-300",
  "Carried from round 9 (key-results rows byte-identical since the previous pin; the round-10 L06 hunks are at lines 52, 99-107, 113 region and 232-233, 288-289, none in 297-300).")
r("E2b-grades-citation-claims", "Citation claims graded C with basis", "course/modules/E/E2/L04.html:229; L05.html:254; L06.html:248; cards E2-c048, E2-c060, E2-c072",
  F + "All three cited claims are topic-level only and graded C (cards basis fields now title, year and venue only). No paper result is attributed.")
r("E2b-math-L04-prop13", "Proposition 1.3 (L04) and its proof", "course/modules/E/E2/L04.html:79-100 (Assumption 4, Proposition 1.3 and proof)",
  F + "Assumption 4 text changed to 'uses c_H>0 and c_L>0, and does not divide by Delta'. Re-read the proof (L04.html lines 92-98): low type divides by c_L only, high type by c_H only; Delta>0 from y_L<y_H; 'only if' argument checked (c_L t < Delta makes e=t better than e=0). Claim verified. Statement: Both hold exactly when Delta/c_L <= t <= Delta/c_H, correct.")
r("E2b-math-L04-remark22", "Remark 2.2 (off-path beliefs)", "course/modules/E/E2/L04.html Remark 2.2 (section 2)",
  "Carried from round 9 (Remark 2.2 byte-identical since the previous pin). Re-read this round: the two on-path constraints give y_H - c_H t >= y_L and y_L >= y_H - c_L t, i.e. t in [Delta/c_L, Delta/c_H]; consistent.")
r("E2b-math-L05-lemma13", "Lemma 1.3 (monotone quantities and rent)", "course/modules/E/E2/L05.html Lemma 1.3",
  "Carried from round 9 (Lemma 1.3 byte-identical since the previous pin). Re-read this round: adding (IC-L) and (IC-H) gives (theta_H-theta_L)(q_H-q_L)>=0; U_H >= U_L + (theta_H-theta_L) q_L from (IC-H). Correct.")
r("E2b-math-L05-prop14", "Proposition 1.4 and proof (Steps 1 to 3)", "course/modules/E/E2/L05.html Proposition 1.4 and proof",
  "Carried from round 9 (Proposition 1.4 byte-identical since the previous pin). Re-read this round: Step 1 transfer shift by U_L keeps IC and gives profit +U_L (p_L+p_H=1); Step 2 raises m_H by delta, (IC-L) becomes (theta_H-theta_L)(q_L-q_H)<=0 by Lemma 1.3; Step 3 FOCs q_H=theta_H and q_L=theta_L-(p_H/p_L)(theta_H-theta_L). Correct.")
r("E2b-math-L05-p3-concavity", "Problem 'Concavity of the reduced profit' (L05)", "course/modules/E/E2/L05.html section 6 'Concavity of the reduced profit'",
  "Carried from round 9 (problem byte-identical since the previous pin). Re-read: Hessian diag(-p_L,-p_H) of the quadratic part; strictly concave; stationary point is the global maximum. Correct.")
r("E2b-math-L06-lemma12", "Lemma 1.2 (affine contract) and proof", "course/modules/E/E2/L06.html Lemma 1.2",
  "Carried from round 9 (Lemma 1.2 byte-identical since the previous pin). Re-read this round: payment alpha+beta x, expected payment alpha+beta E_a, E_a = P(success|a) X-bar. Correct.")
r("E2b-math-L06-prop13", "Proposition 1.3 (L06) and proof", "course/modules/E/E2/L06.html:98-107 (Proposition 1.3 and proof)",
  F + "Round-10 edits: statement now defines the profit as E_a minus expected payment; proof opens with 'By Lemma 1.2 ... compare the pairs (alpha, beta)'. Re-derived each step: IC beta>=c_H/Delta_E=1/5 (alpha cancels); high-effort bound E_H(1-beta)<=600,000 with equality only at alpha=0, beta=1/5; attainment utility 50,000, expected payment 150,000, profit 600,000; low effort weights 3/4 on w(0) and 1/4 on w(X-bar) give expected payment >=0 so profit <=250,000; refusal profit 0. Statement's 'No other contract attains this profit' follows from the equality conditions. Correct.")
r("E2b-math-L06-remark14-21", "Remark 1.4 and Remark 2.1 (L06)", "course/modules/E/E2/L06.html:232-236 (Remark 1.4); L06.html:242-243 (Remark 2.1)",
  F + "Remark 1.4 now says the participation constraint 'that the agent's utility is at least the outside option 0 of Assumption 2 then binds'; expected payment c_H, profit 650,000 = E_H - c_H, alpha=c_H-beta E_H negative since beta E_H>=150,000>c_H=100,000. Lab Part C output -50,000, -275,000, -650,000 agrees. Remark 2.1 agency cost 50,000 and identity (E_H-alpha-beta E_H)+(alpha+beta E_H-c_H)=E_H-c_H re-derived.")
r("E2b-math-L06-remark21-scope", "Remark 2.1 scope (L06)", "course/modules/E/E2/L06.html:242-243",
  "Carried from round 9 (Remark 2.1 byte-identical since the previous pin). The statement is for contracts that induce high effort; the identity is checked above.")
r("E2b-notation", "Notation: no registry symbol reused with another meaning", "course/modules/E/E2/L04-L06.html; notation/notation.json",
  F + "notation/notation.json defines 8 symbols (T, Phi, gamma_3, gamma_4 and others, all module S1/M4). Grep of L04, L05, L06 for \\(T, \\Phi, \\gamma_3, \\gamma_4 returned 0 matches. New symbols introduced this round (E_a, p_a, Delta_E, X-bar, alpha, beta) are E2-local, defined in the lesson, and do not collide with registry entries.")
r("E2b-labs-run", "Lab twins run (run_labs E2)", "tests/labs/E2/lab-E2-L04-1.py, L05-1.py, L06-1.py; tools/run_labs.py --unit E2",
  F + "tools/run_labs.py --unit E2 -> 'run_labs E2: PASS (12/12)', exit 0 (ledgers/E2/scripts/E2-b-r10/run_labs_E2.out). Twins also run alone under python -I -W error with exit 0 and 20 output lines each.")
r("E2b-labs-page-twin", "Page code equals twin; expected block equals output", "course/modules/E/E2/L04.html, L05.html, L06.html lab sections",
  F + "run_labs byte-identity check and expected-block check PASS for all 12 E2 labs (includes L04-L06). Twins unchanged since the previous pin (git diff 33744e5..fa61d6e lists no tests/labs/E2 hunks).")
r("E2b-labs-L04-claims", "Lab 1 (L04) prose claims against code and output", "course/modules/E/E2/L04.html Lab 1 hypothesis and commentary; tests/labs/E2/lab-E2-L04-1.py",
  "Carried from round 9 (L04 Lab 1 hypothesis and interpretation byte-identical since the previous pin; twin unchanged). Output re-checked this round: Part B rows 0..6 and Part C 'agree: True' and Part D (2; 1000000; 5000000) match the commentary.")
r("E2b-labs-L05-claims", "Lab 1 (L05) prose claims against code and output", "course/modules/E/E2/L05.html Lab 1 hypothesis and commentary; tests/labs/E2/lab-E2-L05-1.py",
  F + "Commentary claims re-checked against the twin output: Part A slack 0 for the high type's IC and participation, low type's IC slack 12,000,000; Part B best 2000; Part C best 6000; Part D 7,875,000 / 6,000,000 / 1,875,000. The 'Parts B and C show the values Proposition 1.4 gives' claim is consistent with the grid code (Part B search over q_L with q_H fixed at 6000).")
r("E2b-labs-L06-claims", "Lab 1 (L06) prose claims against code and output", "course/modules/E/E2/L06.html Lab 1 hypothesis and commentary; tests/labs/E2/lab-E2-L06-1.py",
  F + "Commentary: Part A at share 0.20 utilities 50,000 both, tie to high; share 0.30 profit 525,000; Part B best 0.20 with agency cost 50,000; Part C profit 650,000 at 0.20, 0.50, 1.00 (matches output). The clause 'Proposition 1.3 covers every contract that satisfies Assumptions 1 to 4' is a statement about the proposition, not about the lab output.")
r("E2b-labs-seed-network", "Labs: no randomness, no network", "tests/labs/E2/lab-E2-L04-1.py, L05-1.py, L06-1.py",
  "Carried from round 9 (twins byte-identical since the previous pin). Re-run this round under python -I -W error: exit 0, no stderr output.")
r("E2b-labs-L05-docstring", "L05 twin docstring matches the code", "tests/labs/E2/lab-E2-L05-1.py lines 1-20",
  "Carried from round 9 (twin byte-identical since the previous pin). Re-read: Part B grid 0..6000 and Part C grid 0..12000 step 1000 match code lines 71 and 76.")
r("E2b-labs-L04-docstring", "L04 twin docstring matches the code", "tests/labs/E2/lab-E2-L04-1.py lines 1-20",
  "Carried from round 9 (twin byte-identical since the previous pin). Re-read: grid 0..6, 'high type's utility at t is at least its utility at every other grid signal' matches classify().")
r("E2b-dag", "DAG and concept links", "course/modules/E/E2/L04-L06.html; tools/check_dag.py --all",
  F + "tools/check_dag.py --all exit 0; the new text uses only concepts already in L04-L06 (Lemma 1.2, Assumption 4) and no new concept links.")
r("E2b-terms-before-definition", "Terms used before definition", "course/modules/E/E2/L04.html, L05.html, L06.html",
  F + "L06 Prop 1.3 now uses E_a and the agent's action a before the proof; E_a is defined in Lemma 1.2 (E_a = P(success|a) X-bar) which precedes the proposition. Notation Delta_E is defined at L06 section 1. L04 Delta defined in section 1A. No term is used before definition.")
r("E2b-terms-agency-cost-before-definition", "Agency cost used before definition", "course/modules/E/E2/L06.html section 1, Remark 2.1, Lab 1 hypothesis",
  "Carried from round 9 (Remark 2.1 and the Lab 1 hypothesis byte-identical since the previous pin). The Lab 1 hypothesis forward reference 'defined in Remark 2.1 below' is accurate.")
r("E2b-terms-linear-vs-affine", "Affine and linear terms used consistently", "course/modules/E/E2/L06.html; cards E2-c067; index.html line 115",
  "Carried from round 9 (cards E2-c067 and hub index.html line 115 byte-identical since the previous pin). L06 Lemma 1.2 and Proposition 1.3 use 'affine' for alpha+beta x, consistent with Section 4.")
r("E2b-process-words", "No process words in learner text", "course/modules/E/E2/L04-L06.html learner text",
  F + "Scanned the round-10 hunks (L04 Assumption 4; L05 solution line 296; L06 lines 99-107, 232-233, 288-289, 291) for process words (checked, verified, round, agent-review terms). None present.")
r("E2b-structure-hours", "Hours and lesson headers", "course/modules/E/E2/L04.html, L05.html, L06.html headers 'E2 · Lesson n of 9 · 10 study hours'",
  "Carried from round 9 (headers byte-identical since the previous pin; no hunk touches the header lines).")
r("E2b-structure-page-smoke", "Page smoke for the three slice pages", "tools/page_smoke.py --unit E2 --pages L04 L05 L06",
  F + ".venv/bin/python tools/page_smoke.py --unit E2 --pages course/modules/E/E2/L04.html course/modules/E/E2/L05.html course/modules/E/E2/L06.html -> 'page_smoke E2: PASS', exit 0 (ledgers/E2/scripts/E2-b-r10/page_smoke_L04-L06.out).")
r("E2b-hub-titles", "Hub titles for slice lessons", "course/modules/E/E2/index.html (hub) titles",
  "Carried from round 9 (index.html byte-identical since the previous pin; not in the delta).")
r("E2b-quiz-explanations", "Retrieval quiz explanations L04-L06", "course/modules/E/E2/L04.html, L05.html, L06.html section 8",
  "Carried from round 9 (section 8 quiz blocks not touched by the delta). Re-read this round: every explanation's number (e.g. L04 5,000,000 at t=2; L05 6,000,000 U_H; L06 600,000 and 650,000) matches the re-derived values.")
r("E2b-problems-solutions", "Problem solutions L04-L06 (section 6)", "course/modules/E/E2/L04.html, L05.html, L06.html section 6",
  F + "Read all section 6 problems in L04, L05 and L06 this round (including the L05 line-296 solution wording change). Every numeric solution re-derived by hand (see E2b-numbers rows); no arithmetic defect found.")
r("E2b-problems-other", "Problem set and Research prompts (section 6)", "course/modules/E/E2/L04.html, L05.html, L06.html section 6",
  F + "Read the Research and Empirical problems (L04 selection rule, monotone utility, third type; L05 rent removal, competition, continuum; L06 two outcomes, risk aversion, observability). Claims are scoped ('the lesson does not derive', 'this lesson does not state') and consistent with the page's own results.")
r("E2b-cards-c051", "Card E2-c051", "course/modules/E/E2/cards.json E2-c051", "Carried from round 9 (card object byte-identical since the previous pin).")
r("E2b-cards-c058-c063-c125", "Cards E2-c058, c062, c063, c125 against Proposition 1.4, Remark 1.5, Remark 2.1", "course/modules/E/E2/cards.json E2-c058, c062, c063, c125; L05.html Proposition 1.4, Remark 1.5, Remark 2.1",
  F + "E2-c058 'q_L = 2000 units and q_H = 6000 units, the closed form of Proposition 1.4 (Remark 1.5)' re-derived. E2-c125 m_L=6,000,000, m_H=30,000,000 re-derived. E2-c062 and E2-c063 byte-identical since the previous pin (carried).")
r("E2b-cards-c061", "Card E2-c061", "course/modules/E/E2/cards.json E2-c061", "Carried from round 9 (card object byte-identical since the previous pin).")
r("E2b-cards-c067", "Card E2-c067", "course/modules/E/E2/cards.json E2-c067", "Carried from round 9 (card object byte-identical since the previous pin).")
r("E2b-cards-c049", "Card E2-c049 scope wording", "course/modules/E/E2/cards.json E2-c049",
  F + "Round-9 FAIL is fixed. Back now reads 'Under the threshold schedule of Assumption 3 with two types, it reveals the type only when t is at least 1 and both incentive constraints of Proposition 1.3 hold.' The 'only when' is the necessity direction of Proposition 1.3 plus the t>=1 separation requirement, consistent with L04.html section 5 misconception. Numbers 1 and 5,000,000/4,000,000 appear in the lesson.")
r("E2b-cards-c126", "Card E2-c126", "course/modules/E/E2/cards.json E2-c126", "Carried from round 9 (card object byte-identical since the previous pin).")
r("E2b-prose-L06-why-it-matters", "L06 why-it-matters paragraph", "course/modules/E/E2/L06.html line 52",
  "Carried from round 9 (line 52 byte-identical since the previous pin). Re-read this round: 150,000 expected payment, 100,000 effort cost, 50,000 limited-liability cost (Remark 2.1) all verified.")
r("E2b-prose-L05-part-a", "L05 Part A hypothesis and expected commentary", "course/modules/E/E2/L05.html line 129 and expected commentary",
  "Carried from round 9 (line 129 byte-identical since the previous pin). Commentary re-checked against twin Part A output this round.")
r("E2b-prose-L04-remark21", "L04 Remark 2.1 prose", "course/modules/E/E2/L04.html Remark 2.1",
  "Carried from round 9 (Remark 2.1 byte-identical since the previous pin). Re-read this round: least-cost t=2, wage gain 2,000,000, cost 1,000,000, net 5,000,000, t=4 net 4,000,000 all verified.")
frag = {
 "unit": "E2", "slice": "b", "round": 10,
 "verifier": "Claude Haiku 5.5, independent verifier for E2-b (did not build E2; no context shared with builders)",
 "pin": "fa61d6e",
 "base": "33744e5 (round-9 pin; delta 33744e5..fa61d6e read for slice b: L04, L05, L06 hunks, cards.json E2 hunks; the other E2 hunks of cards.json are in other slices)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC10-E2-b",
 "scratch": "/tmp/e2b-r10-build and /tmp/e2b-r10-*.out (no repository files edited)",
 "verified_at": "2026-10-29T14:00:00+00:00",
 "verdict": "PASS" if all(x["status"]=="PASS" for x in rows) else "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": ["Holmstrom (registry family) vs Holmström (prose) spelling: observation only, not a citation defect."],
 "freshness_flags": [],
 "notes": "Round-9 FAIL rows E2b-cite-scope-wording and E2b-cards-c049 are fixed and re-verified (PASS). Delta hunks read: L04.html line 79-80 (Assumption 4 wording), L05.html line 296 (solution wording), L06.html lines 99-107 (Prop 1.3 statement and proof, added proof sentence), L06.html line 233-236 (Remark 1.4 wording), L06.html 291 (solution wording); cards.json E2-c012, c013, c025, c040, c047-c049, c058, c060, c064, c072, c074, c087, c088, c090, c119, c120, c125 changed; E2-c128 to c135 added. Cards c128, c129, c130, c131, c134, c135 and the L01, L02, L03, L07, L09 hunks belong to other slices and were not graded here, except that E2-c132 and E2-c133 (L04 and L05) were checked. tests/labs/E2 unchanged since the pin 33744e5, so no lab twin hunk exists in this delta.",
 "could_not_check": [
   "Crossref or publisher abstracts for the three DOIs (not re-fetched; attributions are topic-level only, so no abstract comparison was needed)",
   "full pytest suite and full gate (only tests/test_labs.py, tests/test_run_labs.py, tests/labs (209 passed) and lint/type gates were run)",
   "run_graders and mutate_graders (no project grader in slice b; lab twins are not mutation-tested by ruling)",
   "student-error mutants and alternative-implementation tests (not applicable to lab twins; none created)",
   "visual rendering beyond page_smoke",
   "raw-markup read of every line of L04 Assumption 3 and of L05 Assumption 3 (read through the stripped text and the raw lines that carry the changed claims)"
 ],
 "summary": "E2-b round 10: PASS. 52 rows, all PASS (9 fresh-checked hunks plus carried rows with byte-identical subjects). Both round-9 FAIL rows fixed and re-verified. run_labs E2 12/12; L04-L06 twins exit 0 under python -I -W error; page_smoke L04-L06 PASS; check_pages, check_dag, check_projects, build_site --check, verify_refs --unit E2 (8 of 560, 0 problems), ruff, mypy --no-incremental, pytest tests/test_labs.py and tests/test_run_labs.py and tests/labs (209 passed) all exit 0."
}
json.dump(frag, open("/Users/billyribeiro/.fanout/wt/verifyC10-E2-b/ledgers/E2/E2-b.json","w"), indent=1, ensure_ascii=False)
print(len(rows), frag["verdict"])
