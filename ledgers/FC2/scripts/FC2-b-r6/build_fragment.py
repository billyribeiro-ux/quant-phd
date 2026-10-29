import json, sys
sys.path.insert(0, "tools")
import ledger

P = "PASS"
F = "FAIL"
rows = []

def row(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

def carried(id_, check, location, subject):
    row(id_, check, location, P, "Carried from round 5 (" + subject + " byte-identical since the previous pin; no hunk of the 04626e9..9fd6aed delta touches them): PASS in round 5, subject re-read in round 6 and unchanged.")

# ---- gates, re-run on pin 9fd6aed
row("FC2-b-gate-check-pages", "gate", "L04.html, L05.html, L06.html", P,
    "Re-run at 9fd6aed: .venv/bin/python tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS'.")
row("FC2-b-gate-check-dag", "gate", "L04-L06 links and definitions", P,
    "Re-run: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS'.")
row("FC2-b-banned-and-process-words", "prose", "L04-L06 pages", P,
    "check_pages banned-string check PASS (re-run). Read of every delta hunk (L04:248,258; L05:119,286,329,391,458; L06:379): no process words in learner text.")
row("FC2-b-page-smoke", "gate", "L04, L05, L06", P,
    "Re-run: tools/page_smoke.py --unit FC2 --pages L04 L05 L06 --skip-sweep -> 'page_smoke modules/FC/FC2/L04.html: PASS', 'L05 ... PASS', 'L06 ... PASS', 'page_smoke FC2: PASS' (Chromium).")
row("FC2-b-hours", "arithmetic", "L04.html:2 (7 h), L05.html:2 (8 h), L06.html:2 (8 h); index.html:29,31,138-140", P,
    "data-hours of L01..L08 = 6,8,9,7,8,8,8,6 sum 60 = hub 'totalling 60 hours'; hub card kickers L04 7 h, L05 8 h, L06 8 h match. Hub line 133 'six to nine study hours each' matches.")
row("FC2-b-lab-run-L04", "lab", "L04.html lab-FC2-L04-1; tests/labs/FC2/lab-FC2-L04-1.py", P,
    "Re-run: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; twin under python -I -W error exit 0, stderr 0 bytes.")
carried("FC2-b-lab-L04-hypothesis", "lab", "L04.html:125", "L04.html line 125")
carried("FC2-b-lab-L04-exact", "lab", "tests/labs/FC2/lab-FC2-L04-1.py:22, :68", "the L04 twin")
carried("FC2-b-lab-L04-header", "lab", "L04.html:233, :242; twin part_two print", "L04.html lines 233 and 242")
row("FC2-b-lab-L05-run", "lab", "L05.html lab-FC2-L05-1", P,
    "Re-run run_labs PASS; twin exit 0 stderr 0 bytes; printed output (spot 10000, D = 9/10 exact, five strikes, parity cost [0,0,0,0,0], planted -300 at index 2, 3 violated triples at 9000) matches the expected block.")
row("FC2-b-lab-L05-claims", "lab", "L05.html:133, :286; lab-FC2-L05-1", P,
    "L05:133 hypothesis (five strikes zero parity cost; 40 pairs; -300 cents at 100 USD; three triples at 90 USD) matches output. L05:286 interpretation re-checked: 30.00,20.00,10.00,1.00,0.00 USD and 2.00,1.00,0.00,0.00,8.00 USD equal cents (3000,2000,1000,100,0) and (200,100,0,0,800); payoff nonzero 0 of 40; -300 at 100 USD; intrinsic count 0.")
row("FC2-b-lab-L05-D-claim", "lab", "tests/labs/FC2/lab-FC2-L05-1.py:1-7, :21, :154; L05.html:286", P,
    "Twin defines DISCOUNT = Fraction(9, 10) (twin tests/labs/FC2/lab-FC2-L05-1.py:21; same line in the page code block at L05.html:154) and no other D value; the new L05:286 sentence 'the lab tests no other value of D' is true. The intrinsic check (line 215-217) does not depend on D; sentence is not false. The lab docstring 'D >= 1/40' threshold re-derived by script (see ledgers/FC2/scripts/FC2-b-r6/threshold.py): bounds fail for D < 1/40 (largest failing scanned D = 3/125) and hold at D = 1/40, 9/10, 2.")
row("FC2-b-lab-L06-run", "lab", "L06.html lab-FC2-L06-1", P,
    "Re-run run_labs PASS; twin exit 0 stderr 0 bytes; output 30, 45, shares 1/2, bond -20, shares 3/4 bond -30, 5/6 bond -50 all re-derived by hand (Example 1.5, 3.4, Lab holdings).")
carried("FC2-b-lab-L06-claims", "lab", "L06.html:162, :309", "L06.html lines 162 and 309")
carried("FC2-b-num-L04", "numbers", "L04.html:116, :120, :242, :335, :342, :349, :358, :360, :372-374, :445; Remark 2.6", "those L04.html lines")
carried("FC2-b-num-L05", "numbers", "L05.html:352, :359, :366, :402, :416, :434, :441, :480, :494, :508, :526, :531", "those L05.html lines")
carried("FC2-b-num-L06", "numbers", "L06.html:94, :99, :157, :327, :337, :345, :365, :369, :373, :383, :385", "those L06.html lines")
row("FC2-b-num-L05-table-five-strikes", "numbers", "L05.html:458, :325", P,
    "'parity cost is zero at each of the five strikes' (458, 325): lab prints five residuals [0,0,0,0,0] at 80..120 USD; 'five strikes, 80 to 120 USD' correct. Grade C names Lab 1 output.")
row("FC2-b-grades", "grades", "L04.html:386-390; L05.html:453-458; L06.html:396-400", P,
    "L04 and L06 rows carried (unchanged lines). L05 row 458 re-read: C grade, source names Lab 1 printed output, not a theorem: correct.")
row("FC2-b-math-L04-canon-date0", "math", "L04.html:248", P,
    "Round-5 FAIL resolved: L04.html:248 now reads 'at date 0, an equality for an American call with no income and a non-negative rate (Theorem 4.1 there)', matching L05 Theorem 4.1 (V_A(0)=V_E(0), r >= 0).")
carried("FC2-b-math-L04-lemma-prop", "math", "L04.html:77-125, :320-323", "L04.html lines 77-125 and 320-323")
row("FC2-b-math-L04-thm41-hyp", "math", "L04.html:111, :258", P,
    "L04:258 (misconception 1) re-read: 'the date-0 early-exercise premium, V_A(0)-V_E(0), is zero' under Theorem 4.1 hypotheses (no income, r >= 0): consistent with L05 Theorem 4.1. L04:111 carried.")
carried("FC2-b-math-L05-T1.2-T2.2", "math", "L05.html:59, :67, :76-103", "L05.html lines 59, 67, 76-103")
row("FC2-b-math-L05-T3.2-C3.4-P3", "math", "L05.html:111-128, :290-295, :375-391, :437-441", P,
    "Re-derived Theorem 3.2 cases (i)-(iv) by hand: (iii) g(s)=-(1-lambda)s+(1-lambda)K3=(1-lambda)(K3-s)>=0 on [K2,K3]; (iv) g=K2-lambda K1-(1-lambda)K3=0. Corollary 3.4 proof unchanged. P3 solution (L05:391) re-derived: P(K2)-[lambda P1+(1-lambda)P3] = [C-gap] + D[K2-lambda K1-(1-lambda)K3] - S(0); D-bracket zero by P1; leaves call convexity gap <=0 by Thm 3.2. Correct after the edit that names the call gap.")
row("FC2-b-math-L05-Z-butterfly", "math", "L05.html:119", P,
    "New sentence 'Z is a butterfly spread: long calls at the two outer strikes and short the call at the middle strike'. Z has weights lambda, 1-lambda and -1; at lambda=1/2 it is half of the standard 1:-2:1 butterfly, so the name is accurate for the stated portfolio. Term is defined in place; no earlier use.")
row("FC2-b-math-L05-interp-D", "math", "L05.html:286", P,
    "'The intrinsic check prints zero violations at D = 9/10.' The intrinsic check (lab line 215-217) compares C with S-K and has no D; the sentence is true and the lab uses only D=9/10 (DISCOUNT line). It tests S-K, which L05:337/Theorem 4.1 proof use at date t.")
row("FC2-b-math-L05-misconc-N", "math", "L05.html:329", P,
    "'A3 excludes under (N)': sell call + buy share has V0 = S - C < 0 by the proof-(a) convention and payoff min(S_tau, K) >= 0 only with S_tau >= 0 (N). Correct.")
carried("FC2-b-math-L05-misconception-deep-itm", "math", "L05.html:337", "L05.html line 337")
row("FC2-b-math-L05-P3-solution", "math", "L05.html:391", P,
    "Re-derived; see FC2-b-math-L05-T3.2-C3.4-P3. The old wording 'the remaining term is the convexity gap of the calls' is replaced by the explicit C-gap expression; correct.")
carried("FC2-b-math-L05-T4.1", "math", "L05.html:301, :304-306, :309-310", "L05.html lines 301, 304-306, 309-310")
carried("FC2-b-math-L06-T1.4ab", "math", "L06.html:69-88, :99, :111-118", "L06.html lines 69-88, 99, 111-118")
carried("FC2-b-math-L06-T1.4c", "math", "L06.html:79, :89", "L06.html lines 79 and 89")
carried("FC2-b-math-L06-T2.2-T3.3", "math", "L06.html:117-158", "L06.html lines 117-158")
row("FC2-b-math-L06-examples", "math", "L06.html:94-106, :314-327, :365, :377-387", P,
    "Re-derived Example 1.5, 1.6, 3.4, misconception 3 (156.25, 56.25, 36, 70.3125), E1, E2, E3 (quote 28 arbitrage: cash 2, payoffs 5/2 both states), M1-M3, R2, R3 numbers. Changed hunk L06:379 (R1) re-derived: with R_f=5/4, B=-100/(5/4)=-80, payoffs 150-100=50, 100-100=0, 50-100=-50 = claim; now states R_f=5/4 explicitly.")
row("FC2-b-math-L06-R1", "math", "L06.html:379", P,
    "The added hypothesis 'At R_f = 5/4' is the only R_f under which the stated B=-80 and R_f B=-100 hold; the section 4 example names no R_f, so the explicit hypothesis is required and is now supplied. Payoff table checked.")
row("FC2-b-notation", "notation", "L04.html, L05.html, L06.html; notation/notation.json", P,
    "Registry (8 symbols plus macros) read in full. Slice symbols against registry: R_f (AP1: gross riskless return) used with same meaning at L06:59, :64, :69, :98; \\mathbb{Q} (AP1 risk-neutral measure) used at L06:111, :114, :119 with the same meaning. No registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}) used in the slice. D, lambda, Delta, B, V, N, A1..A6 are unregistered and not reused with another registered meaning.")
carried("FC2-b-dag-AP1", "dag", "L06.html:114", "L06.html line 114")
carried("FC2-b-dag-convex", "dag", "L04.html:320-323 (P3)", "L04.html lines 320-323")
carried("FC2-b-terms-L05", "terms", "L04.html:73; L05.html:59; L06.html:111", "those lines")
carried("FC2-b-data-figures", "data", "L04.html, L05.html, L06.html", "all three pages' figure and data sections")
carried("FC2-b-refs", "refs", "L04.html:468-472; L05.html:536-540; L06.html:476-480", "those reference sections")
carried("FC2-b-quiz", "quiz", "L04.html:401-464; L05.html:469-532; L06.html:409-472", "the three quiz sections")
row("FC2-b-quiz-numerics-recheck", "quiz", "L04 q2,q4,q6,q7; L05 q2,q4,q5,q8,q9 numeric answers; L06 q2,q3,q5,q9", P,
    "All numeric data-answers re-derived (17, 20, 77, 6.56, 9.85, 12, 1, 40.48, 0.5, 30, 0.75, 45, 75).")
carried("FC2-b-cards-L04", "cards", "cards.json FC2-c051..c062, c135, c142, c143", "cards.json lines of those cards")
carried("FC2-b-card-c059", "cards", "cards.json:410 (FC2-c059)", "cards.json:410")
row("FC2-b-cards-L05", "cards", "cards.json FC2-c063..c080, c132, c145 (c069 at 478, c074 at 515)", P,
    "c069 (478) now says 'butterfly position' which L05:119 now names: round-5 FAIL resolved. c074 (515) matches Lab 1 output (planted convexity error, parity cost [0,0,0,0,0]). FC2-c077 is absent (removed before 04626e9; no card line changed in the delta); the numbering gap 77 is left as a stable-key gap, not a defect. c078 and c145 are separate rows below.")
row("FC2-b-card-c078", "cards", "cards.json:539 (FC2-c078)", F,
    "Card back: 'C <= S (Theorem 2.2(a)) ... a non-negative payoff, which A3 excludes.' The lesson (L05.html:329, changed in this delta) now says the exclusion 'under (N)'. Theorem 2.2(a) needs A1-A5 and (N) (L05:85); the card carries neither the hypotheses nor (N), so it disagrees with the current lesson. Fix: back should read 'Under A1 to A5 and (N), C <= S (Theorem 2.2(a)); selling the call and buying the share has initial value S - C < 0 and a payoff min(S_tau, K) >= 0 (uses (N)), which A3 excludes.'")
row("FC2-b-card-c145", "cards", "cards.json:1017 (FC2-c145, new since 04626e9)", F,
    "New card, L05 misconception 1 (L05.html:324-325). Back: 'No. Theorem 1.2 holds for every strike K > 0, and its proof uses no property of the strike (Theorem 1.2).' Theorem 1.2 is stated 'Under A1, A2, A3, A4 and A5' (L05.html:64), and the card carries none of these hypotheses. Rule (10) requires a card to carry a proposition's hypotheses. Content is otherwise consistent with L05:325 and Lab 1 (cost zero at 80..120 USD). Fix: back 'No. Under A1 to A5, Theorem 1.2 holds for every strike K > 0, and its proof uses no property of the strike (Theorem 1.2).'")
carried("FC2-b-cards-L06", "cards", "cards.json FC2-c081..c098, c136, c137", "cards.json lines of those cards")
carried("FC2-b-card-c085", "cards", "cards.json FC2-c085", "that card")
carried("FC2-b-card-c132", "cards", "cards.json:925 (FC2-c132)", "cards.json:925 and L05.html:337")
carried("FC2-b-cards-refs", "cards", "cards.json FC2-c076 '(Section 5)'", "cards.json FC2-c076 and L05.html Section 5")
row("FC2-b-cards-duplicates", "cards", "course/modules/FC/FC2/cards.json", P,
    "Re-run scripts/FC2-b-r6/cards_check.py: 143 cards, 0 duplicate ids, 0 duplicate fronts. Gaps at c031 (not slice) and c077 (removed, see FC2-b-cards-L05).")
row("FC2-b-cards-new-L04-L06", "cards", "cards.json new since 04626e9: FC2-c145 (L05); c030 (L02) and c049 (L03) are out of slice", F,
    "The only new card in slice b is FC2-c145, which fails (see FC2-b-card-c145). c030 and c049 are outside slice b and not judged here.")
row("FC2-b-cards-removed-c077", "cards", "cards.json (between FC2-c076 and FC2-c078)", P,
    "FC2-c077 absent; no L04-L06 card references it (grep of cards.json and L05 for 'c077' empty). Removal predates the 04626e9 pin.")
row("FC2-b-cards-L04-L06-hypothesis-audit", "cards", "cards.json FC2-c059, c060, c078, c145 (misconception and proposition cards)", F,
    "Hypothesis carrying (rule 10): c078 and c145 FAIL (rows above). c059 (cards.json:410) and c060 state Proposition 2.3 / Proposition 2.2 without A2, A3, A5; these were PASS in round 5 with unchanged subjects and are carried, but they are the same defect class. Fail-closed reading would flag them too; recorded here so the hub owner sees it.")

# carried row prefixes must be exact: already in CARRY
FIX = {
 "FC2-b-card-c078": "Back should read: Under A1 to A5 and (N), C <= S (Theorem 2.2(a)); selling the call and buying the share has initial value S - C < 0 and payoff min(S_tau, K) >= 0 (uses (N)), which A3 excludes.",
 "FC2-b-card-c145": "Back should read: No. Under A1 to A5, Theorem 1.2 holds for every strike K > 0, and its proof uses no property of the strike (Theorem 1.2).",
 "FC2-b-cards-new-L04-L06": "Fix FC2-b-card-c145.",
 "FC2-b-cards-L04-L06-hypothesis-audit": "Add the hypotheses to FC2-c078 and FC2-c145 (see their fixes); decide the hub convention for FC2-c059 and FC2-c060 (Proposition 2.3 and 2.2 hypotheses A2, A3, A5) and apply it to all misconception cards.",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIX[r["id"]]
out = {
    "unit": "FC2",
    "slice": "b",
    "round": 6,
    "verifier": "Haiku independent verifier (FC2 slice b, round 6; did not build FC2)",
    "pin": "9fd6aed",
    "base": "04626e9 (round-5 pin; delta 04626e9..9fd6aed read for every L04-L06 hunk, card and lab twin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC6-FC2-b",
    "scratch": "/tmp",
    "verified_at": "2026-10-29T05:10:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 04626e9..9fd6aed in slice b: L04.html:248 and :258; L05.html:119, :286, :329, :391, :458; L06.html:379; cards.json c030 (L02, out of slice), c049 (L03, out of slice), c145 (new, L05). Every hunk read in context.",
        "Round-5 FAIL rows resolved: FC2-b-math-L04-canon-date0 (L04:248 now says 'at date 0'), FC2-b-cards-L05 c069 (L05:119 now names the butterfly).",
        "Round-5 FAIL-row locator 'FC2-c074 at :514' re-checked: c074 matches Lab 1 output; no defect.",
        "Mutants: none. Labs are demonstrations; mutation testing does not apply to lab twins (verifier-rules ruling). The L05 lab docstring threshold claim (D >= 1/40) was re-derived by script instead.",
        "Hypothesis convention: c059 and c060 (round-5 PASS, unchanged) and c078/c145 (fail) are the same class; see FC2-b-cards-L04-L06-hypothesis-audit.",
        "Read in full: L04.html (483 lines), L05.html (551 lines), L06.html (491 lines). Cards for L04-L06 read in full via scripts/FC2-b-r6/cards_check.py output.",
        "Out of slice, not checked: L01-L03, L07-L08 pages and cards (other than hours cross-check), project page, grader, project labs 1-3, hub index.html text beyond hours and the concept list (index.html:59 added geometric-series and annuity links; check_dag PASS covers them).",
        "Not run: full project gate (ruff/mypy whole repo, full pytest), check_projects, run_graders, mutate_graders, render_curriculum, fetch_data --check, build_site --check. Not needed for slice b. Ran verify_refs --offline (560 entries, 0 problems).",
    ],
    "summary": "",
}
bad = [r for r in rows if r["status"] == F]
out["summary"] = (f"FC2 slice b round 6: {len(rows)} rows, {len(rows)-len(bad)} PASS, {len(bad)} FAIL. "
                  "FAIL rows: FC2-b-card-c078 (cards.json:539 back omits (N) that L05:329 now states), "
                  "FC2-b-card-c145 (cards.json:1017 new card omits Theorem 1.2 hypotheses A1-A5); "
                  "FC2-b-cards-new-L04-L06 and FC2-b-cards-L04-L06-hypothesis-audit follow from them. "
                  "Round-5 FAIL rows FC2-b-math-L04-canon-date0 and the c069 part of FC2-b-cards-L05 are now PASS.")
path = "ledgers/FC2/FC2-b.json"
import os
os.makedirs("ledgers/FC2", exist_ok=True)
json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(ledger.validate(json.load(open(path)), "FC2-b"))
print(len(rows), len(bad))
