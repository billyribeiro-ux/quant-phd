"""Writes the round-3 fragment for E1 slice E1-b (rows, statuses and evidence cited in the verifier report)."""
import json
import sys

S = "ledgers/E1/scripts/E1-b-r3/"
rows = []


def row(rid, check, loc, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("E1b-L04-quotient-def", "2.9-prose",
    "course/modules/E/E1/L04.html Lab 1 hypothesis (line ~134) and Proposition 3.1 (section 3)", "PASS",
    "Re-read this round. The hypothesis line defines the forward quotient (p(a+h)-p(a))/h and the central quotient "
    "(p(a+h)-p(a-h))/(2h) before section 3 uses them; the code in tests/labs/E1/lab-E1-L04-1.py computes the same "
    "quotients (forward=(upper-p0)/h, central=(upper-lower)/(2h)). Diff vs previous pin: no hunk in this span.")
row("E1b-L05-lerner-sign", "2.4-math",
    "course/modules/E/E1/L05.html why-it-matters paragraph (line 49-53)", "PASS",
    "Re-read. Markup (p-c)/p is nonnegative for p>=c; the sentence equates it with 1/|eps| at the chosen price, which "
    "Proposition 5.4 proves for an interior optimum. Checked numerically in lab output (Part B equal True in all cases).")
row("E1b-L05-prop52-between", "2.4-math",
    "course/modules/E/E1/L05.html Proposition 5.2 statement and proof (lines ~80-90)", "PASS",
    "Re-derived: pi(p)=-b p^2+(a+bc)p-ac; completing the square gives (a-bc)^2/(4b)-b(p-p_m)^2. "
    "p_m-c=(a-bc)/(2b)>0 and a/b-p_m=(a-bc)/(2b)>0, so p_m is strictly between c and a/b. Lab 1 Part A/C output "
    "(exact Fractions) agrees at the three cases.")
row("E1b-L05-method-attribution", "2.4-math",
    "course/modules/E/E1/L05.html why-it-matters (line 49-53) and Problem P3 (line ~290-300)", "PASS",
    "Re-read. No attribution to a source; the methods named (completing the square, product rule, second derivative) "
    "are each proved on the page (Proposition 5.2 proof, Proposition 5.4 proof, Problem P3).")
row("E1b-L05-R3-midpoint", "2.4-math",
    "course/modules/E/E1/L05.html Problem R3 solution (line ~365)", "PASS",
    "Re-read: a/(2b) is the midpoint of 0 and a/b; p_m-a/(2b)=c/2>0; Proposition 1.4 of L04 gives |eps|>1 above a/(2b) "
    "with 0<p<a/b; Corollary 5.5 gives (a+bc)/(a-bc)>1 when bc>0. Each step checked.")
row("E1b-L06-remark26-xref", "2.9-prose",
    "course/modules/E/E1/L06.html Remark 2.6 (line ~135) and the cross-reference to Proposition 2.8", "PASS",
    "Re-read. R(x)=max(0,(d-x)/2) has slope -1/2 where R>0 (Lemma 2.4). The iteration reference (Proposition 2.8) "
    "exists on the page and matches the 1/2 factor.")
row("E1b-L06-L03-equilibrium-claim", "2.4-math",
    "course/modules/E/E1/L06.html line ~192; course/modules/E/E1/L03.html line 57 (Setting)", "PASS",
    "Read L03 at the current pin: line 57 gives C(q)=F+cq+kq^2 with k>0 and the supply max(0,(p-c)/(2k)). The L06 "
    "claim that the L03 equilibrium is derived for a quadratic-cost term k>0 that L06 does not have matches L03.")
row("E1b-L06-twice-attribution", "2.4-math",
    "course/modules/E/E1/L06.html Remark 3.4 (line ~196), Misconception 3 (line ~438), Lab 1 Part C output",
    "PASS",
    "Recomputed: sharing at r earns (r-c)(a-br)/2 = h(r)/2; undercut limit h(r); ratio 2 exactly. Lab Part C prints "
    "undercut/sharing ratios of 1.9996 (ref case r=25: 474.91/237.5) which match 2 to the displayed digits.")
row("E1b-L04-numbers-lab", "2.2-numbers",
    "course/modules/E/E1/L04.html Lab 1 interpretation (line ~244), Example 3.2 (line ~262), Remark 3.3 (line ~277)",
    "PASS",
    "Recomputed with Decimal at 60 digits: " + S + "num_L04_L05_L06.py. Forward error 9.391046955e-7 and central "
    "3.880758281e-11 at h=0.01; ratio 24198.99998 (Remark 3.3 correct). Ratios of unrounded forward errors per tenfold "
    "fall: 9.963005, 9.996283, 9.999628 (page 9.9630, 9.9963, 9.99963). Central: 100.002958, 100.0000296, 100.0000003 "
    "(page 100.003, 100.00003, 100.0000003). Example 3.2: 0.999995868 (page 0.99999587), 1.0000299 central and 0.99589 "
    "forward at h=1. Exact change for a 120->121.2: p=10.0544108843, +0.5441088% (page). Elasticity 6/11 = 0.5454545.")
row("E1b-L04-math-prop-proofs", "2.4-math",
    "course/modules/E/E1/L04.html Definition 1.1, Remark 1.2, Example 1.3, Proposition 1.4, Remark 1.5, Remark 2.2, "
    "Proposition 2.3, Example 2.4, Proposition 3.1 (lines 60-270)", "PASS",
    "Re-derived each: eps=-bp/(a-bp) (Example 1.3; eps(10)=-0.2, eps(40)=-2 by recomputation); Prop 1.4 by the three "
    "equivalences; Prop 2.3 with F_p<0 and F_a=D_a>0 AT the equilibrium (the changed hypothesis, line ~114, is what the "
    "proof uses); Example 2.4 p*=sqrt(1+a)-1, dp/da=1/22, dQ/da=10/11; Prop 3.1 p''(120)=-1/5324, p'''(120)=3/1288408 "
    "recomputed; leading terms -h/10648 and h^2/2576816 recomputed.")
row("E1b-L04-lab-twin", "2.5-labs",
    "tests/labs/E1/lab-E1-L04-1.py and course/modules/E/E1/L04.html Lab 1 section", "PASS",
    "run_labs.py --unit E1: PASS (12/12). Twin identical to the page's data-run block (" + S + "twin_vs_page.py: "
    "identical). python -I -W error runs with exit 0. page_smoke --pages L04: PASS, lab 0.0 s.")
row("E1b-L04-lab-claims", "2.5-labs",
    "course/modules/E/E1/L04.html Lab 1 hypothesis (line ~134) and interpretation (line ~244)", "PASS",
    "Hypothesis: closed form 10 cents, 100 units, 1/22 = 0.0454545455, error orders 10 and 100 per tenfold fall. "
    "Printed output agrees (Part A, B, C ratios 9.9630..100.000). Interpretation's 'within 10^-30' and "
    "'central quotient far more accurate' match the code and output.")
row("E1b-L04-hypotheses-cards", "2.7-cards",
    "course/modules/E/E1/cards.json E1-c038..E1-c053 against the CURRENT L04 text", "FAIL",
    "E1-c045 back: 'Assume D and S are continuously differentiable, D_a > 0, D_p < 0 and S'(p) > 0.' The current "
    "Proposition 2.3 (L04 line ~114, changed in aa3c26c) says D_a > 0 AT THE EQUILIBRIUM (a higher intercept raises "
    "quantity demanded at the equilibrium price). The card states the hypothesis unqualified, a stronger assumption than "
    "the proposition, so it disagrees with the current text. The other 15 cards in the range match their lesson text "
    "(each number recomputed: 1/22, 10/11, -h/10648, h^2/2576816, 9.391047e-7, 3.880758e-11).",
    fix="In E1-c045 (course/modules/E/E1/cards.json) change the back to: 'Assume D and S are continuously "
        "differentiable, D_a > 0 at the equilibrium, D_p < 0 and S'(p) > 0. Then dp*/da = D_a/(S' - D_p) > 0 and "
        "dQ*/da = S'(p*) dp*/da > 0 (Proposition 2.3).'")
row("E1b-L04-quiz-key", "2.9-prose",
    "course/modules/E/E1/L04.html section 8 quiz (lines ~431-510) and section 7 key results (lines ~415-428)", "PASS",
    "Each quiz numeric key recomputed: eps(10)=-0.2, |eps(40)|=2, eta=2, dp/da=0.0454545, dQ/da=10/11, elasticity 6/11, "
    "tolerance 0.0001 and 0.000001 adequate. The explanations cite the right items.")
row("E1b-L04-problems", "2.4-math",
    "course/modules/E/E1/L04.html section 6 problems M1-M3, P1-P3, E1-E3, R1-R3 (lines ~315-410)", "PASS",
    "Each solution recomputed: M1 -2/3, M3 eps=-0.1p and -2 at p=20, E2 6/11 and 0.5441088%, E3 ratio 10, "
    "R1 dp/da=-1/2 with S'=-3, R2 p*=sqrt(a), R3 6/11.")
row("E1b-L04-scope-words", "2.9-prose",
    "course/modules/E/E1/L04.html line 56 (section 1 opening paragraph)", "FAIL",
    "Line 56 now reads 'Every derivative in §1 is a derivative of a function of price ..., and the derivatives in §2 and "
    "§3 are taken with respect to the demand intercept a.' That second clause is false on the page: Remark 2.2 uses the "
    "partial derivative F_p, Proposition 2.3 uses D_p and S'(p*) (derivatives in price), and Example 2.4 uses S'(10)=20 "
    "and D_p=-2. Only dp*/da, dQ*/da and p'(a), p''(a) are taken with respect to a.",
    fix="Replace line 56 with: 'Every derivative in §1 is a derivative of a function of price, as in M2. In §2 the "
        "derivatives dp*/da and dQ*/da and in §3 the derivatives of p(a) are taken with respect to the demand intercept "
        "a, while D_p, F_p and S'(p) are taken with respect to price.'")
row("E1b-L05-numbers-lab", "2.2-numbers",
    "course/modules/E/E1/L05.html Lab 1 hypothesis (line ~127) and interpretation (line ~233)", "PASS",
    "Recomputed exactly: prices 70, 20, 27.5; quantities 50, 30, 90; profits 2500, 300, 2025; Lerner 5/7, 1/2, 9/11; "
    "second difference -2b = -2, -6, -8; c/2 = 10, 5, 2.5. Printed values match the exact fractions.")
row("E1b-L05-lab-twin", "2.5-labs",
    "tests/labs/E1/lab-E1-L05-1.py and course/modules/E/E1/L05.html Lab 1 section", "PASS",
    "run_labs.py --unit E1: PASS. Twin identical to the page block (" + S + "twin_vs_page.py). python -I -W error exit 0.")
row("E1b-L05-lab-claims", "2.5-labs",
    "course/modules/E/E1/L05.html Lab 1 interpretation, line ~233 ('The profit has a unique maximum, so the grid cannot "
    "return a different price.')", "FAIL",
    "The sentence gives uniqueness of the maximum as the reason the grid cannot return a different price. Uniqueness "
    "alone does not do that: a grid argmax differs from the maximiser whenever the maximiser is off the 1/10-cent grid. "
    "The agreement holds because each closed-form price (70, 20, 27.5) is a multiple of 1/10, so the grid contains the "
    "maximiser. The Lab hypothesis (line ~127) states that reason; the interpretation does not.",
    fix="In the Part A interpretation replace 'The profit has a unique maximum, so the grid cannot return a different "
        "price.' with 'Each closed-form price is a multiple of 1/10 cent, so the grid contains the unique maximiser, and "
        "the best grid price is that maximiser.'")
row("E1b-L05-proofs", "2.4-math",
    "course/modules/E/E1/L05.html proof of Proposition 5.4 (line ~109) and Corollary 5.5 proof", "PASS",
    "Re-read the changed proof. Q + (p-c)Q' = 0; divide by Q: (p-c)Q'/Q = -1; Q'/Q = eps/p by definition; so "
    "(p-c)eps/p = -1; eps<0 because Q'<0; hence (p-c)/p = -1/eps = 1/|eps|. Every step is valid. Corollary 5.5 "
    "re-derived: eps(p_m) = -(a+bc)/(a-bc). The changed proof text now matches.")
row("E1b-L05-scope-words", "2.9-prose",
    "course/modules/E/E1/L05.html line ~233 (Part A interpretation: 'cannot return a different price')", "FAIL",
    "Scope claim 'cannot' is universal and is not backed by a computation on the page: it holds only because the three "
    "closed-form prices lie on the 1/10 grid (see E1b-L05-lab-claims). Other scope words in L05 are backed: 'every "
    "case' (Part A/B/C output, three cases checked), 'every a, b, c' (Misconception 2 algebra: (a-bc)/2 is half of "
    "a-bc for all a, b, c), 'for any differentiable demand' (Prop 5.4 proof uses only Q>0, Q'<0).",
    fix="Replace 'so the grid cannot return a different price' with 'because each closed-form price is a multiple of "
        "1/10 cent, so the grid contains the maximiser' (same change as the lab-claims fix).")
row("E1b-L05-quiz-multiplier", "2.9-prose",
    "course/modules/E/E1/L05.html quiz item Q5 explanation (line ~428)", "FAIL",
    "The explanation ends: 'substituting Q'/Q = eps/p ... gives (p-c)/p * eps = -1, which is this identity.' The quiz "
    "option is (p-c)/p = 1/|eps(p)|. The step from (p-c)eps/p = -1 to 1/|eps| needs eps<0 (divide by eps and use "
    "|eps| = -eps); the explanation does not state it. The derivation is correct in Proposition 5.4 (which has the sign "
    "step) but not in the quiz pointer, so 'which is this identity' is a gap.",
    fix="End the explanation: '... gives ((p-c)/p) eps = -1; since eps < 0, (p-c)/p = -1/eps = 1/|eps|, which is this "
        "identity.'")
row("E1b-L05-cards", "2.7-cards",
    "course/modules/E/E1/cards.json E1-c054..E1-c066 against the CURRENT L05 text", "PASS",
    "Each card compared with its lesson item: c057 (c/2 gap; elastic region), c058 (hypotheses of Proposition 5.4 "
    "match the statement), c059 (Corollary 5.5), c061 (R1 with beta, c), c062 (changed back: 'For linear demand, the "
    "price with unit elasticity maximizes revenue, but p_m exceeds a/(2b) by c/2' matches Misconception 1 and Remark "
    "5.3; |eps(70)|=1.4 recomputed), c063 (benchmark 100 and monopoly 50 in Misconception 2), c064 (5/7, 9/11 recomputed "
    "as (a-bc)/(a+bc)), c065 and c066 (Lab 1 Parts A-C output).")
row("E1b-L06-numbers-lab", "2.2-numbers",
    "course/modules/E/E1/L06.html Example 1.5, Example 2.7 (line ~142), reference table (section 4), Lab 1 interpretation",
    "PASS",
    "Recomputed: d=100; Cournot each 100/3, total 200/3, fee 160/3 (53.33), profit 10000/9 = 1111.11 (1111 rounded to "
    "the whole cent), total profit 20000/9 = 2222.22; monopoly 50, 70, 2500; Bertrand 100, 20, 0. Lab grid counts "
    "1001 of 1201, 201 of 301, 451 of 501 (= (a/b-c)*10+1) recomputed. Undercut profits 474.909999 etc. recomputed "
    "exactly.")
row("E1b-L06-lab-twin", "2.5-labs",
    "tests/labs/E1/lab-E1-L06-1.py and course/modules/E/E1/L06.html Lab 1 section", "PASS",
    "run_labs.py --unit E1: PASS. Twin identical to the page block (" + S + "twin_vs_page.py). python -I -W error exit 0. "
    "page_smoke --pages L06: PASS, lab 0.2 s. Part B first step within 1e-6 recomputed: 25, 25, 26.")
row("E1b-L06-lab-claims", "2.5-labs",
    "course/modules/E/E1/L06.html Lab 1 hypothesis (line ~201), docstring (lines ~202-230), interpretation (lines ~391-395)",
    "PASS",
    "Hypothesis (1)-(4) each match a printed or asserted check in the code: Part A asserts grid==closed form for each "
    "rival output tested (the list is filtered by q<=d, so 6/5/6 outputs for d=100/60/180, as printed); Part B exact "
    "match at 31 steps; Part C counts winners and prints whether all are >= c; undercut vs sharing printed for four "
    "rival fees per case. 'The lab does not prove these for all inputs' is true (finite grids).")
row("E1b-L06-proofs", "2.4-math",
    "course/modules/E/E1/L06.html Lemma 1.3, Proposition 1.4, Lemma 2.4, Theorem 2.5, Proposition 2.8, Lemma 3.2, "
    "Theorem 3.3 (all four steps), Proposition 4.1, Problems P1-P3, R1-R2", "PASS",
    "Re-derived: Lemma 2.4 R(x)=max(0,(d-x)/2) including the D<=0 branch; Theorem 2.5 symmetry and d/3, fee (a+2bc)/(3b), "
    "profit d^2/(9b); Proposition 2.8 induction (x_t in [0,d/2] so Lemma 2.4 applies) and error (d/3)(1/2)^t; Theorem 3.3 "
    "Steps 1-4 incl. Case B continuity argument; Proposition 4.1 differences d/6, d/3, d/(6b), d/(3b), d^2/(36b) "
    "recomputed with fractions. R1 n-firm q=d/(n+1) recomputed. P2 pair (c, c+delta) not equilibrium checked.")
row("E1b-L06-cards", "2.7-cards",
    "course/modules/E/E1/cards.json E1-c067..E1-c091 against the CURRENT L06 text", "PASS",
    "All 25 cards compared with their lesson text. E1-c090 (changed) now says 'For a rival volume x at most d ... 0 for "
    "x >= d (Lemma 2.4)', matching Misconception 2 line ~434. c083 and c091 match Remark 3.4 and Misconception 3. c078 "
    "rounding matches Example 2.7. c084 and c085 match Lab 1 Parts A-C. Numbers recomputed.")
row("E1b-L06-scope-words", "2.9-prose",
    "course/modules/E/E1/L06.html Remark 3.4 (line ~196): 'Undercutting pays only when the cheaper fee still earns a "
    "margin.'", "FAIL",
    "The word 'only' is a converse (an undercut does not pay when the cheaper fee earns no margin). The page proves "
    "only the direction 'h(g)>0 for c<g<a/b' (Lemma 3.2). For g<=c, h(g)=(g-c)(a-bg) <= 0 because a-bg>0 when g<a/b, "
    "but the page does not state or prove this, and the lemma does not cover it.",
    fix="Add after Lemma 3.2 in Remark 3.4: 'For g <= c, h(g) = (g - c)(a - bg) is zero or negative, because a - bg > 0 "
        "for g < a/b, so an undercut to a fee at or below c earns no more than sharing.' Or replace 'only when' with 'when' "
        "and drop the converse.")
row("E1b-L06-misconception-prose", "2.9-prose",
    "course/modules/E/E1/L06.html Misconception 2 (line ~434) and Proposition 2.8 statement (line ~147)", "PASS",
    "Changed text re-read. Misconception 2: 'For a rival volume x at most d, the reaction is (d-x)/2 ... it is 0 for "
    "x >= d (Lemma 2.4)' is correct by Lemma 2.4 (max(0,(d-x)/2)). Proposition 2.8's added clause ('since both start at "
    "zero and use the same reaction function') follows from the induction. No banned phrase; the earlier unqualified "
    "'falls by half a unit' is now qualified.")
row("E1b-citations", "2.1-citations",
    "course/modules/E/E1/L04.html, L05.html, L06.html section 9/7/9 References", "PASS",
    "All three pages say 'This lesson cites no outside source' and carry an empty data-references list (grep: no "
    "data-ref entries, no registry key). tools/verify_refs.py --unit E1 (live): '1 of 560 entries, 0 problems'. "
    "tools/verify_refs.py --offline: '560 entries, 0 problems'. No registry key is attached to a slice claim.")
row("E1b-grades", "2.3-grades",
    "course/modules/E/E1/L04.html section 7, L05.html section 5, L06.html section 8 key results", "PASS",
    "Every T row is a proposition proved on its page, and each hypothesis it needs is in the statement (checked "
    "against the changed Proposition 2.3 hypothesis and Proposition 5.4 hypotheses). No empirical claim is graded.")
row("E1b-dag", "2.9-dag",
    "course/modules/E/E1/L04.html, L05.html, L06.html 'Uses' lines; check_dag.py --unit E1", "PASS",
    "tools/check_dag.py --unit E1: PASS. Uses: L04 competitive-equilibrium (L03), derivative, partial-derivative, "
    "implicit-function-theorem, taylor-theorem (M2 closure); L05 profit-maximization (L02), price-elasticity (L04), "
    "competitive-equilibrium (L03); L06 monopoly (L05), profit-maximization (L02), competitive-equilibrium (L03), "
    "mathematical-induction (closure). Forward references to L07 are to a lesson title only.")
row("E1b-hours", "2.6-hours",
    "course/modules/E/E1/L04.html, L05.html, L06.html headers (data-hours=10); course/modules/E/E1/index.html hub split",
    "PASS",
    "data-hours=\"10\" on each of the three pages; hub data-hours-lessons=90 and data-hours-project=30 sum to 120 "
    "= curriculum hours (curriculum/02-economics-finance-core.yaml:21). Design targets not paced (architect ruling).")
row("E1b-structure", "2.9-structure",
    "course/modules/E/E1/L04.html, L05.html, L06.html section order and lab markup", "PASS",
    "Each page has: why-it-matters, numbered sections, definitions/propositions with proofs, a lab section with "
    "hypothesis, data-run block and expected block, canon-breaks, misconceptions, problem set (mechanics, proof, "
    "empirical, research), key results, quiz with cards link, references, lesson nav. page_smoke and check_pages: PASS.")
row("E1b-L05-quiz-tolerance-unused", "2.9-prose",
    "course/modules/E/E1/L05.html quiz numeric items (tolerance 1e-6 and 0.005)", "PASS",
    "Numeric keys: 0.7142857 vs 5/7 (diff 1.4e-8 <= 1e-6), 1.2222222 vs 11/9 (diff 2.2e-8 <= 1e-6), 20 with tolerance "
    "0.005, 2500 with 0.5. Quiz grading (course/assets/js/quiz.js) uses absolute tolerance; all admit the stated answers.")
row("E1b-L06-quiz-tolerance", "2.9-prose",
    "course/modules/E/E1/L06.html quiz items Q2 (line ~579, data-answer 53.3333, data-tolerance 0.005) and Q4 (66.6667)",
    "PASS",
    "Checked against quiz.js (absolute tolerance). With 0.005: 53.33 (diff 0.0033) accepted, 53.34 (diff 0.0067) rejected; "
    "66.67 (diff 0.0033) accepted, 66.66 (diff 0.0067) rejected. The previous 0.001 rejected the two-decimal answer "
    "53.33, so the change corrects the item. Fix verified.")
row("E1b-cards-dup-scan", "2.7-cards",
    "course/modules/E/E1/cards.json (132 cards, all lessons)", "PASS",
    "Scripted scan: 132 cards; no duplicate id; no duplicate front (case-insensitive). Every card has id, lesson, front, back; "
    "grade present on 'T'/'C' cards only (None on definitions, as in earlier lessons).")

# Slice-b rows whose subject changed in this pin were re-verified above; no PASS row is carried by byte identity,
# except the three lab twins (byte-identical to the round-2 pin: git diff 1817191 aa3c26c lists no tests/labs/E1/lab-E1-L0[456]-1.py).

fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "E1",
    "slice": "E1-b",
    "round": 3,
    "verifier": "independent verifier (Haiku), unit E1 slice E1-b, round 3; did not build E1; no shared context with builders or earlier verifiers",
    "pin": "aa3c26c",
    "base": "1817191",
    "checkout": "/tmp/verifyB3-E1-b (detached at aa3c26c; .venv symlink)",
    "scratch": "/tmp/e1b3-v/",
    "verified_at": "2026-10-28T16:45:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 1817191..aa3c26c for slice E1-b: course/modules/E/E1/L04.html (lines 56, 114, 277), L05.html (lines 52, 89, 109, 428), L06.html (lines 147, 155, 201, 419, 434, 579, 593), cards.json (c004 L01, c062, c090). Lab twins tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py and lab-E1-L06-1.py are not in the delta.",
        "Round-2 FAIL rows re-verified from scratch: E1b-L04-scope-words (still FAIL, new fix text), E1b-L05-proofs (PASS), E1b-L06-cards (PASS), E1b-L06-misconception-prose (PASS), E1b-L05-quiz-multiplier (FAIL, the identity step is now correct but the sign step is missing), E1b-L05-cards (PASS), E1b-L06-quiz-tolerance (PASS).",
        "No round-2 PASS row was carried by byte identity; every row was re-read on the current text. The rows were checked against the full text of L04, L05 and L06 (all lines read).",
        "New defects this round (not in round 2): E1b-L04-hypotheses-cards (card c045 unqualified D_a>0), E1b-L05-lab-claims and E1b-L05-scope-words ('cannot return a different price'), E1b-L06-scope-words ('only when' in Remark 3.4).",
        "Mutants: none. Slice E1-b has lesson pages and lab twins only; ARCHITECT RULING on mutation applies to project graders only.",
        "Scripts: " + S + "num_L04_L05_L06.py (numbers), " + S + "twin_vs_page.py (twin identity). Commands run: tools/run_labs.py --unit E1 (PASS 12/12); tools/check_pages.py --unit E1 --page L04/L05/L06 (PASS); tools/check_dag.py --unit E1 (PASS); tools/page_smoke.py --unit E1 --pages L04 L05 L06 --skip-sweep (PASS); tools/verify_refs.py --unit E1 (live, 1 of 560, 0 problems); tools/verify_refs.py --offline (560, 0 problems); python -I -W error on each twin (exit 0).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(fails),
        "unverifiable": 0,
        "mutants": 0,
        "fail_ids": fails,
    },
}
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
print("rows", len(rows), "fail", fails)
