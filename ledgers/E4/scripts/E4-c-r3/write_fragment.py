"""E4-c round 3 fragment writer: carries round-2 rows whose cited lines are unchanged, re-verifies the rest.

Usage: python -I write_fragment.py <checkout-root> <round2-fragment.json>
Changed new-side lines come from: git diff -U0 67c47689 67a2d13e -- course/modules/E/E4/L07.html L08.html L09.html
"""
import datetime
import json
import sys

root, r2_path = sys.argv[1], sys.argv[2]
r2 = json.load(open(r2_path, encoding="utf-8"))
PIN_R2 = "67c47689c49435bc0e6639e3de4feded5eefdd64"
PIN = "67a2d13e7575608e95b2e34a9c7c2a82c61b117b"
CHANGED = "lines 51, 57, 127 (L07); 51, 59, 66, 79, 123, 175, 263, 328, 587 (L08); 51, 287, 311 (L09)"

# Rows re-verified this round: id -> (status, evidence, optional fix)
RE = {
 "E4c-cmd-check-pages": ("PASS", "Re-run on pin 67a2d13 alone: ledgers/E4/scripts/E4-c-r3/out/check_pages_L07.out, _L08.out, _L09.out each 'check_pages E4 Lnn: PASS', exit=0."),
 "E4c-cmd-check-dag": ("PASS", "Re-run: ledgers/E4/scripts/E4-c-r3/out/check_dag_E4.out 'check_dag E4: PASS', exit=0."),
 "E4c-cmd-check-projects": ("PASS", "Re-run: ledgers/E4/scripts/E4-c-r3/out/check_projects_E4.out 'check_projects E4: PASS', exit=0. Project content is outside this slice."),
 "E4c-cmd-run-labs": ("PASS", "Re-run: ledgers/E4/scripts/E4-c-r3/out/run_labs_L07.out, run_labs_L08.out, run_labs_L09.out each 'run_labs E4: PASS (1/1)', exit=0."),
 "E4c-cmd-twins-standalone": ("PASS", "Re-run from an empty scratch cwd with env -i and python -I -W error (ledgers/E4/scripts/E4-c-r3/run_gates.sh): out/twin-L07.exit, twin-L08.exit, twin-L09.exit = 0; out/twin-L0n.stderr 0 bytes."),
 "E4c-expected-equals-output": ("PASS", "ledgers/E4/scripts/E4-c-r3/embed_check.py (out/embed_check.out): for L07, L08, L09 the data-run code block equals the twin file and the <pre class=\"expected\"> block equals the twin's stdout (strip-equal), all True."),
 "E4c-cmd-page-smoke": ("PASS", "Re-run alone: out/page_smoke_L07_L08_L09.out 'page_smoke modules/E/E4/L07|L08|L09.html: PASS', 'page_smoke E4: PASS', exit 0; lab timings L07 0.0 s, L08 0.1 s, L09 5.0 s (under 10 s)."),
 "E4c-cmd-ruff-mypy-twins": ("PASS", "Re-run: out/ruff_check.out 'All checks passed!'; out/ruff_format.out '3 files already formatted'; out/mypy_twins.out 'Success: no issues found in 3 source files'. All exit 0."),
 "E4c-cmd-pytest-labs": ("PASS", "Re-run: out/pytest_labs_E4.out, 13 passing tests, exit=0."),
 "E4c-cmd-verify-refs": ("PASS", "Offline re-run: out/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', exit 0. The live Crossref run of round 2 is carried (Carried from round 2: references/ byte-identical since 67c47689; references/references.json:17288-17310 read this round: title 'Information, trade and common knowledge', year 1982)."),
 "E4c-cmd-run-graders": ("PASS", "Re-run: out/run_graders_E4.out 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.4 s)', exit=0. The project grader is outside this slice; it is re-run because grader/ changed in the delta."),
 "E4c-L07-structure": ("PASS", "Re-read: changed hunks at L07.html lines 51, 57, 127 only (section order, h2 ids and block order unchanged versus the round-2 read); check_pages E4 L07 PASS this round; the 1-610 read of round 2 stands for the unchanged lines."),
 "E4c-L07-def-correlation-noise-volume": ("PASS", "L07.html:57 now reads 'the <a class=\"concept\" data-concept=\"correlation\" href=\"../../../concepts.html#correlation\">correlation</a> is ...' and the only <dfn> on that line is <dfn>noise volume</dfn> (plain, no data-concept). grep of <dfn> across course/modules: the correlation definition is only course/modules/M/M4/L05.html:85 (def-correlation). concepts.html contains id=\"correlation\" (grep count 1). Math of Def 7.1 unchanged and correct."),
 "E4c-L07-remark-7.9-varp": ("PASS", "L07.html:127 re-read. Recomputed with Fraction in ledgers/E4/scripts/E4-c-r3/recheck_c_r3.py (out/recheck_c_r3.out): Var(p) = 729/1444, 27/49, 27/32, 729/338, 35937/4802 and rho2 = 4/9, 1/3, 1/6, 1/18, 1/66 for sd 1/4, 1/2, 1, 2, 4; Var(p) strictly increasing and rho2 strictly decreasing across the sweep. Twin output out/twin-L07.stdout Part B prints the same var_p and rho2 values. The claim 'on that sweep Var(p) rises while rho2 falls' holds. L07.html:378 carried from round 2 (unchanged line)."),
 "E4c-L07-define-before-use": ("PASS", "L07.html:37 links correlation (Uses row); L07.html:57 defines the noise volume with a plain <dfn> and links correlation (no second dfn); L07.html:62 the only data-concept definition on the page (price-informativeness, owned here). No term is used before its definition in L07.html lines 37-62."),
 "E4c-L07-process-and-banned": ("PASS", "grep -n -i over L07.html, L08.html, L09.html for TODO, FIXME, placeholder, builder, verifier, fixer, clearly, obviously, 'it is easy to see', 'as we saw', 'let us', 'we now', 'note that', 'trivially', 'round 2', 'round 3', draft: no hits. check_pages E4 L07 PASS."),
 "E4c-L08-structure": ("PASS", "check_pages E4 L08 PASS this round; changed hunks at L08.html lines 51, 59, 66, 79, 123, 175, 263, 328, 587 read in full (text only, no section, block or order change)."),
 "E4c-L08-cor-2.4-lemma-2.5": ("PASS", "L08.html:123 re-read: 'The posterior of v (Lesson L06) given an information set is its conditional law given that set' is now a reference to the L06 definition (L06.html:96 <dfn>posterior</dfn>), no second dfn. Corollary 2.4 formulas and Lemma 2.5 at L08.html:121-146 are byte-identical to round 2 (not in the delta) and were re-derived in round 2 (carried)."),
 "E4c-L08-cor-3.2-lemma-3.3": ("PASS", "L08.html:175 re-read: the statement now writes Corr(v, p*)^2 and names 'the price p* of Proposition 3.1'. Proof re-derived: Cov(v,p*) = beta sigma_v^2, Var(p*) = beta^2(sigma_v^2 + sigma_eta^2), so Corr^2 = sigma_v^2/(sigma_v^2 + sigma_eta^2) = tau_eta/(tau_v + tau_eta) = sigma_v^2/(sigma_v^2 + sigma_eps^2 + kappa^2 sigma_u^2). Exact Fraction check on 600 parameter tuples (sigma_v2, sigma_eps2, sigma_u2 incl. 0, a, lambda): 0 failures (ledgers/E4/scripts/E4-c-r3/recheck_c_r3.py, out/recheck_c_r3.out). Lemma 3.3 (L08.html:184-200) byte-identical, carried."),
 "E4c-L08-prop-5.2": ("PASS", "L08.html:328 re-read: 'the cost restricts the equilibrium informed fraction; costs strictly between G(1) and G(0) give interior equilibria under A5; costs at or above G(0) give lambda = 0; at or below G(1) give lambda = 1; the interior equilibrium is not claimed to be unique; Lab 1 checks monotonicity only on its grid'. Twin out/twin-L08.stdout: gain(0)=0.173287, gain(1)=0.127706; part C costs 0.12 -> lambda*=1 (boundary), 0.13..0.17 interior, 0.18 -> 0 (boundary); part B 'gain strictly decreasing on 999 interior grid points: True'. Lab statement matches output."),
 "E4c-L08-line51-zero-cost": ("PASS", "L08.html:51 re-read: 'no informed fraction lambda ... is an equilibrium at a cost c with 0 < c < G(0)' with G(0) = ln(2)/4 = 0.173287 (recheck_c_r3 / recheck_c_r3.out 'L08 G(0)'). Twin part D (sigma_u^2 = 0, cost 0.15): 'interior fractions with gain = cost: 0', 'lam = 0 is an equilibrium: False', 'lam = 1 is an equilibrium: False'. Consistent with Proposition 5.1(b). Line 301 carried."),
 "E4c-L08-line51-existence": ("PASS", "L08.html:51: 'equilibria exist outside (G(1), G(0))' and 'existence uses Assumption A5' inside. Matches Proposition 5.2 text at L08.html:328 and twin part C (costs 0.12 and 0.18 are boundary cases with lambda* = 1 and 0; 0.13 to 0.17 interior roots)."),
 "E4c-L08-G-before-definition": ("PASS", "L08.html:51 now reads 'the gain from information as a cost, G(lambda) (Definition 4.3; Lemma 4.5 for G(0))' and L08.html:79 reads 'Lemma 4.5 (Section 4) gives G(0)'. Every use of G before the definition at L08.html:232-235 (lines 51, 79) carries an explicit forward pointer to Definition 4.3 or Lemma 4.5 (grep 'G(' on lines below 235 returns only 51, 79, 234). Forward pointers stated in the why-it-matters and the example are accepted. Grade on Lemma 4.5 unchanged."),
 "E4c-L08-dfn-duplicates": ("PASS", "The three round-2 duplicates are removed: L08.html:59 CARA is plain text 'constant absolute risk aversion (CARA) utility (Definition 6.2 of Lesson L06)' (no dfn; L06.html:67 is the only dfn); L08.html:66 'signal' is now 'The signal of Lesson L06' (no dfn; L06.html:57 is the only dfn); 'noise traders' is plain text (L06.html:57 only dfn). Remaining plain dfns on L08 at lines 66 (noise-trader supply), 71 (informed, uninformed) are a definition-order problem, recorded in row E4c-r3-first-use-before-definition."),
 "E4c-L08-define-posterior": ("PASS", "L08.html:123 has no <dfn> for posterior now (grep <dfn> in L08.html lists lines 66, 71, 206, 233, 235, 267, 281 only). The only definition of posterior is L06.html:96 <dfn>posterior</dfn>. PASS."),
 "E4c-L08-misc-claims": ("PASS", "L08.html:587 re-read: 'At cost c below G(0) = ln(2)/4, Lab 1 gives a positive informed fraction for every cost on its grid from 0.12 to 0.17, and the value at cost 0.15 is lambda* approx 0.658. ... in Lab 1 the bisection root falls as the cost rises.' Twin out/twin-L08.stdout part C: 0.12 -> 1.000000000, 0.13 -> 0.965625410, 0.14 -> 0.815032329, 0.15 -> 0.657828572, 0.16 -> 0.480567912, 0.17 -> 0.231615819 (strictly decreasing, all positive on 0.12..0.17). ln(2)/4 = 0.173287. Recomputed independently: out/recheck_c_r3.out 'root falls as cost rises: True'; the round-2 bisection recheck re-run (out/recheck_c_r2_rerun.out, identical to round 2) agrees with the printed roots to 1e-9. L08.html:583, 591, 595 carried."),
 "E4c-L08-process-banned": ("PASS", "grep -i on L08.html for the banned process words (see E4c-L07-process-and-banned): no hits. check_pages E4 L08 PASS."),
 "E4c-L09-structure": ("PASS", "check_pages E4 L09 PASS this round; changed hunks at L09.html lines 51, 287, 311 read in full (text only; no section, block or order change)."),
 "E4c-L09-misc-2-3": ("PASS", "L09.html:311 re-read (misconception 2 now uses omega labels): exhaustive check in recheck_c_r3.py: w1 cell of P1 = {w1,w2} and P2 = {w1}, both inside E={w1,w2}; meet(w1) = {w1,w2,w3} (w2, w3 share a P2 cell), not a subset of E; so E is known by both at w1 but not common knowledge. 'b and c share a cell of P2' now reads 'w2 and w3 share a P2 cell': verified True. L09.html:315 carried from round 2 (unchanged line)."),
 "E4c-L09-state-labels-c-a": ("PASS", "L09.html:311 relabelled to omega_1, omega_2, omega_3 consistently in Omega, P1, P2, E and the text; the example is correct (see E4c-L09-misc-2-3). The round-2 defect (mixed letters a, b, c) is fixed; no remaining a, b, c state labels in the misconception."),
 "E4c-L09-dag": ("PASS", "L09.html:37 and 287: Remark 2.5 now links L02.html#def-arrow-debreu-equilibrium (grep: id=\"def-arrow-debreu-equilibrium\" exists once in L02.html:89, an earlier E4 lesson, allowed by the Earlier E4 lessons rule). pareto-efficiency and adverse-selection are in the prerequisite closure (E1, E2). check_dag E4 PASS this round. L09.html:290 carried (unchanged)."),
 "E4c-L09-process-banned": ("PASS", "grep -i on L09.html for the banned process words: no hits. check_pages E4 L09 PASS."),
 "E4c-dag-unlinked": ("PASS", "check_dag E4 PASS this round. The new links in the delta are the correlation link (L07.html:57, prerequisite closure M4) and the L02 link (L09.html:287, earlier lesson, allowed). No unlinked use of a concept outside the closure was found in the changed lines of L07-L09."),
 "E4c-notation-registered": ("PASS", "ledgers/E4/scripts/E4-c-r3/notation_scan.py -> out/notation_scan.out: unknown macros = [] for L07, L08, L09. notation/notation.json has 8 registered symbols (R^\\ast, R^{e\\ast}, R_f, Q and macros); none is used in L07-L09 with another meaning. \\R used (L08 4, L09 1); no \\mathbb{R} in the three pages (grep count 0)."),
 "E4c-r2-delta-read": ("PASS", "Round-3 delta read: git diff -U0 67c47689 67a2d13e for course/modules/E/E4/L07.html, L08.html, L09.html, index.html (cards and hub lines), tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py (0 changed lines: the twins are byte-identical to the round-2 pin). Every changed hunk read in full (L07: 51, 57, 127; L08: 51, 59, 66, 79, 123, 175, 263, 328, 587; L09: 51, 287, 311). index.html changes at 81, 83-84 and 132-133 are the hub quiz (lambda to zeta) and the L04/L05 card titles, outside this slice; the L07-L09 card titles (lines 135-137) and the hours (line 29) are byte-identical."),
}
RE_FAIL = {}
# Round-2 FAIL rows that are now PASS are in RE (def-correlation, define-posterior, dfn-duplicates, G-before-definition, state-labels).

# Carry: round-2 PASS rows whose cited lines are not in CHANGED (or whose subject files are byte-identical).
# A carried row keeps its id and round-2 evidence behind the carry prefix.
rows = []
for r in r2["rows"]:
    rid = r["id"]
    if rid in RE:
        status, ev = RE[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"round-2 non-PASS row not re-verified: {rid}")
    pre = (f"Carried from round 2 (cited lines unchanged since the previous pin {PIN_R2[:8]}; delta changed lines are {CHANGED}; "
           "cited lines do not intersect them):")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": pre + " " + r["evidence"]})

rows.append({
 "id": "E4c-r3-first-use-before-definition",
 "check": "2.9-structure (define before use, rule 5)",
 "location": "course/modules/E/E4/L08.html:66 (plain dfn of 'noise-trader supply'), L08.html:71 (plain dfn of 'informed' and 'uninformed'); first uses in course/modules/E/E4/L06.html:673 (learner prompt 'the variance sigma_u^2 of the noise-trader supply') and L06.html:72 ('A fraction lambda ... of the investors is informed', no dfn)",
 "status": "FAIL",
 "evidence": "grep -n 'noise-trader supply' L06.html shows the term at L06.html:673 inside a learner-facing prompt, before its only definition at L08.html:66; grep -n 'informed' L06.html shows that the bare terms 'informed' and 'uninformed' first appear in the body at L06.html:72 with no <dfn> (L06.html:57 defines only 'informed fraction'); the plain <dfn> for both terms comes later at L08.html:66 and L08.html:71. Rule 5 (define at first use with a plain <dfn>) is not met for these terms. The terms are not concepts (no data-concept), so the defect is definition order, not a duplicate.",
 "fix": "Move the plain definitions to first use: in L06.html:57 wrap 'noise-trader supply' (the random net supply u) in <dfn>, and in L06.html:72 wrap 'informed' and 'uninformed' in <dfn> at their first use; then delete the <dfn> tags at L08.html:66 and L08.html:71 (keep the words plain). Alternatively reword L06.html:673 to 'the variance of the noise supply u' and keep the L08 definitions. Re-run check_pages E4 L06 and L08."
})

fragment = {
 "unit": "E4",
 "slice": "E4-c",
 "round": 3,
 "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 3 (did not build E4)",
 "pin": PIN,
 "base": f"{PIN_R2} (round-2 pin; delta read hunk by hunk, see E4c-r2-delta-read)",
 "checkout": root,
 "scratch": "/tmp/e4c-r3-XXXX (twin runs, removed after each run)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [
   "B1: no registry record for Grossman & Stiglitz (1980); L08.html:795 cites none and says the attribution is not made here (honest). Still open in the registry, not a defect of this slice.",
   "milgrom1982information (L09.html:511): the abstract was not read by the builder; the page states no result of it. Live Crossref re-verification not repeated this round (carried from round 2)."
 ],
 "freshness_flags": [],
 "notes": (
   "Scope: course/modules/E/E4/L07.html, L08.html, L09.html; tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py (byte-identical to round 2); "
   "index.html only where a row cites a card title or hours. Delta 67c47689..67a2d13e read hunk by hunk; new-side changed lines: L07 51, 57, 127; L08 51, 59, 66, 79, 123, 175, 263, 328, 587; L09 51, 287, 311. "
   "Carry rule applied per row: a round-2 PASS row is carried only when every line it cites is outside the changed lines (the row prefix says so); rows citing a changed line, or whole-file rows, were re-verified. "
   "Scripts: ledgers/E4/scripts/E4-c-r3/ (run_gates.sh, embed_check.py, notation_scan.py (reused from r2), recheck_c_r3.py, write_fragment.py). "
   "Cross-slice observations (not scored here, for the owning slices): (1) course/modules/E/E4/project.html:259 defines <dfn>constant absolute risk aversion (CARA) utility</dfn>, a second definition of the CARA concept owned by L06.html:67; "
   "(2) the L06 first-use order problem recorded as E4c-r3-first-use-before-definition; "
   "(3) the cards (course/modules/E/E4/cards.json) and the hub prose beyond cited lines are not in this slice. Not checked by this slice: cards, the project and grader rows, mutants, alternatives, page_smoke for other E4 pages, and the full unit ledger."
 ),
 "summary": None,
}
n = len(rows)
passn = sum(1 for r in rows if r["status"] == "PASS")
fail = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = (f"E4-c round 3 on {PIN[:7]}: verdict FAIL. {n} rows: {passn} PASS, {fail} FAIL, 0 UNVERIFIABLE. "
  "The five round-2 non-PASS rows are fixed and re-verified PASS (E4c-L07-def-correlation-noise-volume, E4c-L08-define-posterior, "
  "E4c-L08-dfn-duplicates, E4c-L08-G-before-definition, E4c-L09-state-labels-c-a). One new FAIL: E4c-r3-first-use-before-definition "
  "(noise-trader supply, informed, uninformed are defined in L08 after their first use in L06). Mutants: none (lab twins, not project graders).")
out = "/Users/billyribeiro/.fanout/wt/verifyE3-E4-c/ledgers/E4/E4-c.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, n, "rows", passn, "pass", fail, "fail")
