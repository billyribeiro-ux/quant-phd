"""Round 9, slice E4-c: writes ledgers/E4/E4-c.json from the round-8 row ids (kept), round-9 evidence and new rows."""
import json
import re
from datetime import datetime, timezone

CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyE9-E4-c/"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-c.round8.json", encoding="utf-8"))
O = "ledgers/E4/scripts/E4-c-r9/out/"
PFX = ("Carried from round 8 (cited lines byte-identical since the previous pin 0dee921a; the delta "
       "0dee921a..c93dd526 touches only L07.html:459, L08.html:333, L08.html:596, L09.html:394 and cards.json "
       "among these files): ")

FRESH = {
 "E4c-r4-delta-read": ("delta", "Round 9 delta read hunk by hunk: `git --no-pager diff 0dee921a HEAD` over course/modules/E/E4 (L07.html:459, L08.html:333, L08.html:596, L09.html:394, cards.json, L06.html wording only, project.html, grader/test_project.py, curriculum.json M3 concept name only). Every hunk in the L07 to L09 slice was read; the L06 and curriculum hunks do not change any statement that L07 to L09 cite (Proposition 6.7, Assumption G, A1 to A4 read at L06.html:61-90, 173-200)."),
 "E4c-cmd-check-pages": ("2.9-structure", f"`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS' ({O}check_pages_E4.out, exit 0)."),
 "E4c-cmd-check-dag": ("2.9-structure", f"`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS' ({O}check_dag_E4.out, exit 0)."),
 "E4c-cmd-check-projects": ("2.6-projects", f"`tools/check_projects.py --unit E4` -> PASS ({O}check_projects_E4.out, exit 0)."),
 "E4c-cmd-run-labs": ("2.5-labs", f"`tools/run_labs.py --unit E4 --page L07|L08|L09` -> 'run_labs E4: PASS (1/1)' for each page ({O}run_labs_L07.out, run_labs_L08.out, run_labs_L09.out; page code equals twin byte for byte)."),
 "E4c-cmd-twins-standalone": ("2.5-labs", f"Each twin copied to an empty /tmp directory and run as `python -I -W error lab-E4-Lnn-1.py`: exit 0, stderr 0 bytes ({O}twin_L07-1.out, twin_L08-1.out, twin_L09-1.out and .err)."),
 "E4c-expected-equals-output": ("2.5-labs", f"ledgers/E4/scripts/E4-c-r9/expected_vs_output.py: the expected block of each page equals the twin's stdout line for line (L07 28 lines, L08 20 lines, L09 18 lines; identical True) ({O}expected_vs_output.out)."),
 "E4c-cmd-page-smoke": ("2.9-structure", f"`tools/page_smoke.py --unit E4 --pages L07 L08 L09` -> 'page_smoke modules/E/E4/L07.html: PASS', L08 PASS, L09 PASS (lab timings: L07 0.0 s, L08 0.1 s, L09 5.2 s, under 10 s), 'page_smoke E4: PASS' ({O}page_smoke_L07-9.out)."),
 "E4c-cmd-ruff-mypy-twins": ("2.5-labs", f"`ruff check tests/labs/E4` 'All checks passed!'; `ruff format --check tests/labs/E4` '12 files already formatted'; `mypy --no-incremental` on the three L07 to L09 twins 'Success: no issues found in 3 source files' ({O}ruff_check.out, mypy_twins.out)."),
 "E4c-cmd-pytest-labs": ("2.5-labs", f"`pytest tests/test_labs.py -k 'E4 and (L07 or L08 or L09)' -q` passed (3 tests) ({O}pytest_labs_E4c.out); `--collect-only -k E4` collects 13 E4 lab tests ({O}pytest_collect_E4.out)."),
 "E4c-cmd-verify-refs": ("2.1-citations", f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' ({O}verify_refs_offline.out); `tools/verify_refs.py --unit E4` (live Crossref) -> 'live re-verification of E4: 3 of 560 entries, 0 problems' ({O}verify_refs_unit_live.out)."),
 "E4c-cmd-run-graders": ("2.6-projects", f"`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)' ({O}run_graders_E4.out). The project grader itself is slice d/project; this run only confirms the grader gate for the unit."),
 "E4c-L07-structure": ("2.9-structure", "course/modules/E/E4/L07.html read in full (1-614) this round: header, Sections 1 to 8 in the BUILDER_RULES §4.2 order, lab section, canon-breaks (5 bullets), misconceptions (4), problem set (Mechanics 3, Proof 3, Empirical 3, Research 3), key-results table (7 rows), quiz (10 items with explanations), references, footer. check_pages PASS."),
 "E4c-L07-hours": ("2.9-hours", "L07.html:2 data-hours=\"8\"; the hub split (index.html:29 data-hours-lessons=\"72\", nine lessons of 8 h) is consistent."),
 "E4c-L07-problems-E1": ("2.2-numbers", "L07.html:459 (E1 solution, the round-8 FAIL) now reads 'the difference is 1/3 − 0.330625 = 13/4800 ≈ 0.002708, where 0.330625 is the sample value ... rounded to six decimals ... (13/4800)/0.02 = 13/96 ≈ 0.135 rounded to three decimals'. Recomputed with Fraction: 1/3 − 0.330625 = 13/4800 exactly; 13/96 = 0.13541…; the printed sample is formatted :.6f in lab Part F (L07.html:362 and the twin). The sentence now states the rounding rule, so the round-8 defect is fixed. Script: ledgers/E4/scripts/E4-c-r9/independent_checks.py (E1 rows)."),
 "E4c-L07-process-and-banned": ("2.9-structure", "L07.html body text read in full: no process words (build, builder, round, verifier, REQUEST, unit report); no banned phrase (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, it is important to note, studies show, experts agree, it is well known, obviously, clearly); the only ellipses are in code. Grep over L07.html/L08.html/L09.html: no matches outside code."),
 "E4c-L08-structure": ("2.9-structure", "course/modules/E/E4/L08.html read in full (1-813): header, Sections 1 to 11 with the canon-breaks (5 bullets), misconceptions (4), problem set (Mech 3, Proof 3, Emp 3, Res 3), key-results table (9 rows), quiz (9 items with explanations), references, footer; check_pages PASS."),
 "E4c-L08-hub-title": ("2.9-structure", "index.html:148 card title 'L08 · 8 h The Grossman–Stiglitz Paradox' vs L08.html:35 <h1>The Grossman–Stiglitz Paradox</h1>: identical."),
 "E4c-L08-process-banned": ("2.9-structure", "L08.html body text read in full: no process words; no banned string outside code; grep over the three pages: no TODO/TBD/lorem/omitted/well known/obviously/clearly/ellipsis in prose."),
 "E4c-L09-structure": ("2.9-structure", "course/modules/E/E4/L09.html read in full (1-525): header, Sections 1 to 9, lab section (Lab 1, expected block of 18 lines), canon-breaks (4 bullets), misconceptions (3), problem set (Mech 3, Proof 3, Emp 3, Res 3), key-results (6 rows), quiz (9 items), references, footer; check_pages PASS."),
 "E4c-L09-emp-1-3": ("2.2-numbers / 2.4-math", "L09.html:394 (Emp 3 solution, changed this round: adds 'The printed 625 counts bets nonnegative for both traders on the meet. By Theorem 2.1 those are exactly the bets with zero posteriors there'). Recomputed by exhaustive enumeration over all 15625 bets (ledgers/E4/scripts/E4-c-r9/independent_checks.py): the zero-posterior set on {1,2,3} equals {x(3)=0, x(2)=-x(1)} for every bet (iff holds, 0 mismatches) and has 625 members = 5·5³; the nonnegative-on-meet set has 625 members, none with a nonzero posterior. The argument is correct."),
 "E4c-L09-hub-title": ("2.9-structure", "index.html:149 card title 'L09 · 8 h The No-Trade Theorem' vs L09.html:35 <h1>The No-Trade Theorem</h1>: identical."),
 "E4c-L09-process-banned": ("2.9-structure", "L09.html body text read in full: no process words, no banned string outside code (Verify and Attempt are learner instructions)."),
 "E4c-r2-delta-read": ("delta", "Round 2 delta read is superseded by E4c9-delta-read and E4c-r4-delta-read; the L07 to L09 subjects were re-read in full in round 9 (see E4c9-delta-read)."),
 "E4c-r5-cards-duplicates": ("2.7-cards", f"ledgers/E4/scripts/E4-c-r9/cards_check.py: 243 cards, 0 duplicate ids, 0 duplicate fronts; Jaccard scan over all cards: 25 pairs above 0.55, none a duplicate of a card in L07 to L09 (the closest, E4-c201 vs E4-c233, are the state-1 and state-4 checks of Lab 1, distinct claims) ({O}cards_check.out)."),
 "E4c-r5-cards-L07": ("2.7-cards", "All 21 L07 cards read against L07.html: each definition, lemma, proposition and lab number matches the page (Lab 1 Part A to F values 1/3, 4/9, 1/6, 1/18, 1/66, 729/1444, 35937/4802, 1/6, 1/3, 9/22, 1/3 ... 0.330625 checked against the recomputation). No card number is absent from L07.html (cards_check.py)."),
 "E4c-r5-cards-L08": ("2.7-cards", "All 43 L08 cards read against L08.html and the lab output (twin_L08-1.out): G(0)=ln2/4, G(1)=ln(5/3)/4, the cost-grid roots 0.965625410, 0.815032329, 0.657828572, 0.480567912, 0.231615819, Corr² 0.013061 and 0.166667, the gap values, the Part D counts. No card number is absent from L08.html (cards_check.py)."),
 "E4c-r5-cards-L09": ("2.7-cards", "All 24 L09 cards read against L09.html and the lab output (twin_L09-1.out): counts 15625, 500, 625, 0, witness bet (-1,2,-2,-2,-2,-2), posteriors 1/2, 1/3, -2, the two-prior numbers 0.7/0.4 giving 0.4 and 0.2. E4-c211 states the midpoint construction with its relabelling sentence; it is correct, and its phrase 'lies strictly between nu_2 and nu_1' holds in either order (cards_check.py)."),
 "E4c8-L08-misc3-printed-range": ("2.2-numbers / 2.5-labs", "The round-8 FAIL at L08.html:596 is fixed. The misconception now reads: Lab 1, Part C prints Corr(v,p*)² from 0.013061 (cost 0.17) to 0.166667 (cost 0.12), rounded to six decimals. Verified against twin_L08-1.out: 'cost = 0.17 ... Corr(v,p)^2 = 0.013061', 'cost = 0.12 ... Corr(v,p)^2 = 0.166667'; 0.013061 = 0.01306113 and 1/6 = 0.16666667 (independent_checks.py). The rounding rule (six decimals) is stated on the page."),
 "E4c8-delta-read": ("delta", "Round 8 delta superseded; the round 9 delta is read in E4c9-delta-read and E4c-r4-delta-read."),
 "E4c8-scope-banned-dfn-notation": ("2.9-structure", "Scope words in L07 to L09 (every, all, always, never, only, any, exactly, same, in general): each use checked; see E4c9-scope-words. Banned strings: none. dfn ids: L07 def-price-informativeness, L08 def-grossman-stiglitz-paradox, L09 def-no-trade-theorem, each defined once (data-concept set). Notation: no collision with notation/notation.json (see E4c-r5-notation-scan)."),
 "E4c8-cards-L07-L09": ("2.7-cards", "All 88 L07 to L09 cards read this round (21 L07, 43 L08, 24 L09); every number in them appears in its own lesson (cards_check.py: none missing); no duplicate of another card (Jaccard scan over all 243 cards)."),
 "E4c8-twin-page-equal": ("2.5-labs", f"run_labs --page L07, L08, L09 PASS (page code equals twin byte for byte; expected equals output) ({O}run_labs_*.out, expected_vs_output.out)."),
 "E4c8-rederive-numbers": ("2.2-numbers", "Every printed and quoted number in L07 to L09 re-derived this round in ledgers/E4/scripts/E4-c-r9/independent_checks.py (55 PASS lines, 0 FAIL): L07 Parts A to F, E1, E2, R2, M3; L08 G(0), G(1), Corr² at λ = 1/2 (1/18), Monte Carlo Var(D_I) and Var(D_U) at λ = 1/2 (within 0.4%), the five printed roots at costs 0.13 to 0.17 (independent bisection agrees to 1e-6), Corr² at 0.17 and at λ = 1, Emp 3 values; L09 counts 500, 625, 0, the Example 2.4 posteriors, and the 5^6 enumeration."),
 "E4c-r5-notation-scan": ("2.4-mathematics", "Notation scan of L07 to L09 against notation/notation.json (symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q; macros E, Var, Cov, Corr, R, Normal, indic): no registered symbol is used with another meaning. Local symbols (rho, tau, theta, kappa, chi, varpi, eta, nu, pi, omega, N, M, D, W, EU, G) are not registered; \\ast is used only as p^*, lambda^*, and the registered R^\\ast is not used. No raw \\mathbb{E} or \\mathbb{R} in the three pages (grep)."),
 "E4c-r5-figures": ("2.8-data", "L07.html, L08.html, L09.html contain no svg, no figure and no chart (grep '<svg|<figure|<img' empty); the labs print text only. Nothing to check against 360 px or light/dark rendering; page_smoke reported the pages PASS."),
 "E4c-dag-unlinked": ("2.9-structure", "Plan §4 out-of-closure names (bayesian-inference, state price, stochastic discount factor, martingale, efficient markets, noise-trader risk, Banach, intermediate value, two-fund, diagnostic expectations, determinacy, informed trading) grepped in L07 to L09: no matches. 'common knowledge', 'posterior', 'noise traders', 'CARA', 'Walras' are plain prose or defined in L06 (no concept link)."),
 "E4c-r5-lab-sim-labels": ("2.8-data", "SIMULATED labels: L07 Part F (hypothesis L07.html:132, twin docstring line 14 and Part F), L08 Part A (span.simulated-label at L08.html:341, twin docstring), L09 none (no random draws: twin uses Fraction and itertools only, lab-E4-L09-1.py)."),
 "E4c-L08-misc-claims": ("2.2-numbers", "L08.html:583-595 misconceptions 1 to 3 (headers and first sentences) re-read this round: each claim checked (Prop 5.1(a), Corollary 3.2, G(1) = ln(5/3)/4, Definition 4.6(i), the seven-cost grid). Misconception 3 (line 596) is covered by E4c8-L08-misc3-printed-range."),
}

NEW = [
 ("E4c9-delta-read", "delta", "course/modules/E/E4/L07.html:459; L08.html:333, 596; L09.html:394; cards.json; L06.html wording; curriculum.json M3 concept name",
  "PASS", "git --no-pager diff 0dee921a HEAD read for every E4 file in the slice. The four slice-page hunks and the cards.json hunks were re-verified (rows E4c-L07-problems-E1, E4c8-L08-misc3-printed-range, E4c-L08-prop-5.2 and E4c9-L08-line333, E4c-L09-emp-1-3, E4c-r5-cards-*). The L06 hunks are wording only; Proposition 6.7 (L06.html:173-200), Assumption G and A1 to A4 (L06.html:61-90) are unchanged in content. tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py are byte-identical to the round-8 pin (not in the diff)."),
 ("E4c9-L08-line333-prop5.2-prose", "2.2-numbers / 2.9-prose", "course/modules/E/E4/L08.html:333",
  "PASS", "The changed paragraph: 'At the parameters of Example 1.1 the gain from information is still positive at lambda = 1, where G(1) = ln(5/3)/4 ≈ 0.127706 (Problem Emp 3); the page does not show that the gain is positive at every lambda.' G(1) recomputed = 0.127706405941 (independent_checks.py, 'L08 G(1)=ln(5/3)/4'); Emp 3 gives the closed form; the caveat is honest (no claim of positivity at every lambda). Also the text 'Costs strictly between G(1) and G(0) give an interior equilibrium under A4' matches Proposition 5.2(c)."),
 ("E4c9-independent-recompute", "2.2-numbers / 2.4-math / 2.5-labs", "ledgers/E4/scripts/E4-c-r9/independent_checks.py (out/independent_checks.out)",
  "PASS", "Independent re-derivation written from the page formulas (not from the lab code): 55 checks, 55 PASS, 0 FAIL (output in out/independent_checks.out; run with python -I -W error). Covers L07 Parts A to E and E1, E2, R2, M3; L08 Corr² = 1/18, Cor 3.2 by moments, the slope formula 0.160494, G(1), G(0), Prop 4.1 variances by seeded Monte Carlo (200000 draws, within 0.4%), the five printed bisection roots at costs 0.13 to 0.17 (independent bisection agrees to 1e-6), Corr² at 0.17 and at lambda = 1, Part D zero gain at sigma_u = 0, the Prop 5.2(a) limit; L09 meet(1), meet(4), 5^6 = 15625 bets, 500 strict and 0 nonnegative-on-meet, 625 nonnegative-on-meet with 0 nonzero posteriors, the iff of Emp 3 for all bets, the Example 2.4 values."),
 ("E4c9-L09-milgrom-no-claim", "2.1-citations", "course/modules/E/E4/L09.html:512; references/references.json:17291-17315",
  "PASS", "Registry record milgrom1982information: Milgrom & Stokey, 'Information, trade and common knowledge', Journal of Economic Theory, volume 26, issue 1, pages 17-27, 1982, DOI 10.1016/0022-0531(82)90046-1, verified_by crossref. L09.html:512 gives title, JET, volume 26, issue 1, pages 17-27, 1982: identical to the record. The page states no result of that paper ('The page states no result of that paper'), so no published claim is attributed; the abstract is therefore not needed for any row (see could_not_check)."),
 ("E4c9-L08-no-grossman-stiglitz-cite", "2.1-citations / 2.3-grades", "course/modules/E/E4/L08.html:800; L08.html:58-80, 283-285 (paradox definition)",
  "PASS", "L08 cites no registry key ('This lesson cites no registry source'); the sentence 'The attribution of the model and of the paradox to a published source is not made here' (L08.html:800). The paradox is defined as a model result (Definition at L08.html:279-282, Proposition 5.1 and 5.2 graded T under A1 to A3 or A4). No card cites Grossman and Stiglitz (cards_check.py: cite None for all L07 to L09 cards). B1 is respected."),
 ("E4c9-scope-words", "2.9-structure", "course/modules/E/E4/L07.html, L08.html, L09.html (prose, scope words)",
  "PASS", "Every scope word in prose (every, all, always, never, only, any, exactly, same, in every state, for every lambda, for every cost): each is backed by a proof, a finite enumeration (L09 counts over 15625 bets; L08 grid of 999 fractions; L07 sweeps) or an explicit limit (L07 'does not show that the sign pattern holds at every parameter value'; L08 'nothing on the page proves that G falls on (0,1) for every parameter choice'; L09 'The page makes no claim for infinite Omega')."),
 ("E4c9-L06-statements-used", "2.4-mathematics / 2.9-prose", "course/modules/E/E4/L06.html:61-90, 173-200, 213-225, 234-236",
  "PASS", "The L06 statements L07 and L08 use (Assumptions A1 to A4 and G, Definition 6.1, Proposition 6.7 with kappa = a sigma_eps^2/lambda, sigma_eta^2, tau_bar, theta_s = tau_bar/(tau_v+tau_bar), theta_u = kappa theta_s, Corollary 6.8, Remark 6.10) were read at their locators; the closed forms in L07 Proposition 7.6 and L08 Proposition 3.1 agree with them, and the base-instance values (theta_s = 3/7, sigma_eta^2 = 2, tau_eta = 1/2) reproduce in independent_checks.py."),
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        check, evid = FRESH[rid][0], FRESH[rid][1]
        rows.append({"id": rid, "check": check, "location": r["location"], "status": "PASS", "evidence": evid})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": PFX + r["evidence"]})
for rid, check, loc, status, evid in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": evid})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing_prev = [r["id"] for r in prev["rows"] if r["id"] not in ids]
assert not missing_prev, missing_prev
frag = {
 "unit": "E4",
 "slice": "c",
 "round": 9,
 "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 9 (did not build E4)",
 "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
 "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
 "checkout": CHECKOUT.rstrip("/"),
 "scratch": "/tmp/e4c9_* (twins run from empty directories with python -I -W error); /tmp/e4c9_indep (independent script)",
 "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [
   "grossman1980 / Grossman and Stiglitz (AER 1980): still no registry record (B1, REFERENCE_REQUEST R-E4-1). L08 cites no key, which is correct; the paradox is taught as a model result.",
   "mascolell1995microeconomic author conflict (B3) is outside this slice (L07 to L09 cite no Mas-Colell key).",
   "milgrom1982information: record matches L09.html:512 (title, JET 26(1), pages 17-27, 1982)."
 ],
 "freshness_flags": [],
 "notes": ("Scope: course/modules/E/E4/L07.html, L08.html, L09.html; tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py; "
   "the 88 L07 to L09 cards of course/modules/E/E4/cards.json. Pin c93dd526 (round-8 pin 0dee921a). The whole of each page was read, "
   "line by line, and every printed or quoted number was re-derived (independent_checks.py). Mutants: none. Lab twins are "
   "demonstrations and mutation testing does not apply to this slice (ruling; the project grader belongs to the project slice). "
   "Round-8 FAIL rows E4c-L07-problems-E1 (L07.html:459) and E4c8-L08-misc3-printed-range (L08.html:596) are fixed and re-verified PASS. "
   "Observations that are not FAIL rows: (1) L08 Proposition 5.2(c) and the bisection use A4, whose continuity part (A4(i)) is assumed and stated "
   "as assumed (L08.html:314-321). (2) L08 'Grossman-Stiglitz paradox' is a name for the model result; the page states that no attribution "
   "is made (L08.html:800). (3) L09 cards E4-c211 relies on the relabelling sentence for nu1 < nu2; the card is correct as written. "
   "(4) L09 why-it-matters uses 'common knowledge' and 'prior' with forward pointers, accepted as in round 7 and 8."),
 "summary": "PASS: 147 rows, 0 non-PASS. 140 round-8 ids kept: 101 carried with the round-8 evidence under the byte-identical rule, 39 re-verified this round with round-9 evidence. 7 new rows (E4c9-*).",
 "could_not_check": ("The Grossman and Stiglitz (1980) paper: no registry record (B1), and the lessons cite no key, so there is nothing to check against it. "
   "The abstract of Milgrom and Stokey (1982) was not read: L09 states no result of that paper (plain curl only, no bot-check bypass). "
   "The L06 statements used by L07 and L08 were read at the cited locators (L06 is slice a/b), not as a full slice. "
   "Browser rendering beyond page_smoke (no figure on these pages). Pyodide timing measured by page_smoke only (L09 lab 5.2 s, under the 10 s limit)."),
}
json.dump(frag, open(CHECKOUT + "ledgers/E4/E4-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "verdict", frag["verdict"])
