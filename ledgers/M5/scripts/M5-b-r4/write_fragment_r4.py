import json, sys
from pathlib import Path
root = Path("/tmp/verifyB4-M5-b")
cards_lines = (root / "course/modules/M/M5/cards.json").read_text().split("\n")
def card_line(cid):
    for i, l in enumerate(cards_lines, 1):
        if f'"id": "{cid}"' in l:
            return i
    raise SystemExit("missing " + cid)
c089, c105 = card_line("M5-c089"), card_line("M5-c105")
P = "PASS"; F = "FAIL"
def row(id_, check, loc, status, ev, fix=None):
    r = {"id": id_, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != P:
        r["fix"] = fix
    return r
rows = [
 row("M5-b-html-L05-math-lt","L05 strict inequalities and proofs","course/modules/M/M5/L05.html:215, :220, :315",P,
     "Re-read L05.html:214-221 (Prop 2.5 and proof: 0<=x^n<=a^n; (1+h)^n>=1+nh by induction; a^n<eps for n>1/(h eps)) and :315 key-results row. Re-derived; correct."),
 row("M5-b-html-L06-math-lt","L06 strict inequalities and proofs","course/modules/M/M5/L06.html:56, :70, :234, :282",P,
     "Re-read L06.html:56, 70, 234, 282: Lemma 1.2 uniqueness via |t-s|<=b_k-a_k; EVT Step 2 M-1/n_k<f(x_{n_k})<=M; unit-ball boundedness via triangle inequality. Re-derived; correct."),
 row("M5-b-L06-partB-lower-bound-claim","Part B: grid maximum is a lower bound; equality only when 1/2 on grid","course/modules/M/M5/L06.html:221; tests/labs/M5/lab-M5-L06-1.py Part B",P,
     "Identity x(1-x)=1/4-(x-1/2)^2 checked algebraically; run output 'grid_tenths argmax 1/2 maximum 1/4', 'grid_sevenths argmax 3/7 maximum 12/49 lower_bound_for_true True' (ledgers/M5/scripts/M5-b-r4/lab_compare_r4.out). Only-when claim holds because max=1/4 forces x=1/2."),
 row("M5-b-L06-partC-proposition-number","Part C interpretation vs Proposition 3.4 scope","course/modules/M/M5/L06.html:221 and :325",P,
     "Page now says Prop 3.4 'states this for the unit vectors of B(N), and its argument applies verbatim to these truncations'. The Prop 3.4 proof uses only |e_m(k)-e_n(k)|<=1 (both entries in [0,1]) and the value 1 at k=m; both hold for the length-20 truncations of e_0..e_9. Scope claim now backed by the argument; no claim that the proposition itself covers index 0."),
 row("M5-b-L06-mech2-citation","Mechanics 2 cites Corollary 2.2 and derivative argument","course/modules/M/M5/L06.html:307",P,
     "f(-2)=-2, f(-1)=2, f(1)=-2, f(2)=2 recomputed; critical points +-1 from 3x^2-3; the one-sided quotient argument is correct; Corollary 2.2 at :239-245."),
 row("M5-b-L06-mech2-typo","Mechanics 2 arithmetic and typo check","course/modules/M/M5/L06.html:307",P,
     "Same locator; recomputed values match the stated maximum 2 and minimum -2 and their points."),
 row("M5-b-L06-ex1.5-subsequence-citation","Example 1.5 subsequence argument after change to 1/(n+1)","course/modules/M/M5/L06.html:96 and :383",P,
     "Changed to x_n=1/(n+1). Recomputed: x_n in (0,1) for n>=1; for n_k>=k, 0<x_{n_k}=1/(n_k+1)<=1/k. Quiz item L06q4 at :383 uses the same sequence. Consistent."),
 row("M5-b-L07-partC-no-fixed-point-claim","Part C grid sign check and the statement that it does not prove no fixed point","tests/labs/M5/lab-M5-L07-1.py part_c; course/modules/M/M5/L07.html:186, :193, canon-breaks item 2",P,
     "Lab prints 'f(x) - x is positive at every grid point on either window'; the page says the grid check does not prove no fixed point and points to canon-breaks item 2, where sqrt(x^2+1) > |x| >= x gives no fixed point (recomputed)."),
 row("M5-b-L07-tolerance-claim","Tolerance statement in lab hypothesis matches code","tests/labs/M5/lab-M5-L07-1.py lines 83-85 and TOL; course/modules/M/M5/L07.html:186",P,
     "TOL=1e-12 is used in part_a (err > bound + TOL) and part_b (best > BETA + TOL); part_c gap <= 0.0 check has no tolerance. Matches the hypothesis sentence."),
 row("M5-b-L07-M1-general-linear-map","Problem M1 values (beta, fixed point, x1, x2, bound, error)","course/modules/M/M5/L07.html Problem M1 solution (line ~336)",P,
     "Recomputed: beta=1/2, x*=2, x1=1, x2=1.5, bound at n=2 is (1/2)^2*1/(1/2)=0.5, error |1.5-2|=0.5. Correct."),
 row("M5-b-L07-completeness-attribution","Completeness of R attributed to L02 Theorem 2.5 and L01 Definition 1.1","course/modules/M/M5/L07.html:67 and :136; read course/modules/M/M5/L02.html:125-134, L01.html:58-59",P,
     "L01 Def 1.1 is the supremum property (completeness of R); L02 Thm 2.5 proof uses the supremum of {b_k} (H2). Both read; the attribution matches what the lesson texts prove. No bibliographic data cited."),
 row("M5-b-L07-most-maps-scope","'Not every map guarantees that' scope claim with witness","course/modules/M/M5/L07.html:52",P,
     "Witness x -> -x: iterates from 1 are 1,-1,1,-1,... (no limit). The claim is witnessed."),
 row("M5-b-L07-bellman-term-before-definition","No term used before definition; forward pointer to Lesson 8","course/modules/M/M5/L07.html:52; grep of L05-L07 for Bellman/utility/dynamic programming",P,
     "The only forward reference is 'The operator defined by formula in Lesson 8 needs the same theorem' (a pointer, not a term use). No M7/CS2 concept name in L05-L07; check_dag M5 PASS."),
 row("M5-b-L07-R1-general-condition","R1 solution: bound equals error for phi x = beta x; no general condition claimed","course/modules/M/M5/L07.html Problem R1 solution",P,
     "Recomputed: x_n = beta^n, d(x0,x1)=1-beta, bound = beta^n(1-beta)/(1-beta) = beta^n = error. The solution explicitly says no general condition is stated."),
 row("M5-b-L07-E3-strict-monotonicity","E3 quotient on (0.995,1) and strict bound below sin 1","course/modules/M/M5/L07.html E3 solution (line ~400); Assumption 2(a) at :159",P,
     "Recomputed: (cos 0.995 - cos 1)/0.005 = 0.840116725732564; sin 1 - q = 0.0013542590753 (unrounded). Printed 0.840117 is the lab maximum at pair (0.995, 1) (ledgers/M5/scripts/M5-b-r4/nums_b4.out). Strictness from Assumption 2(a) as stated."),
 row("M5-b-L05-why-it-matters-prop13","Why-it-matters claim about Lesson L08 applying L05 section 3","course/modules/M/M5/L05.html:52",F,
     "Sentence says 'Lesson L08 applies the completeness results of §3 to a space of functions.' L08.html Uses line lists only L01, L04, L07 concepts and no link to L05; grep of L08.html finds no L05 reference and no use of Prop 3.1 or 3.2. L08's own Proposition 1.3 proves completeness of R^G (finite grid, sup norm) from L01 completeness. The cross-lesson claim is unsupported.",
     "Replace with: 'Lesson L08 proves completeness of a space of functions on a finite grid (its Proposition 1.3) and applies Lesson 7's theorem to the Bellman operator.' Or drop the sentence."),
 row("M5-b-L05-interpretation-prop13a","Part A/B interpretation: sup distance 1 on [0,1], (1/2)^n on [0,1/2]","course/modules/M/M5/L05.html:174",P,
     "Run output: sup_distance 1 for all orders on [0,1]; sup 1/2^n on [0,1/2] with equals_half_power True. Prop 1.3(a) and Prop 2.5 with a=1/2 are the cited results; the page says the grid output shows grid values only."),
 row("M5-b-L05-lab-partC-label","Part C docstring and printed content","tests/labs/M5/lab-M5-L05-1.py lines 98-99 and main() Part C",P,
     "Docstring says Part C prints f_n(0.99) for n=10,100,1000 as floats and a True check for f_n(1)=1 for n=1,10,100,1000; main() prints exactly that (embedded output lines 169-173 match run)."),
 row("M5-b-L05-lab-run","L05 twin runs and embedded output matches","tests/labs/M5/lab-M5-L05-1.py; course/modules/M/M5/L05.html:156-173",P,
     "python -I -W error: exit 0; embedded expected == run output (ledgers/M5/scripts/M5-b-r4/lab_compare_r4.out)."),
 row("M5-b-L06-lab-run","L06 twin runs and embedded output matches","tests/labs/M5/lab-M5-L06-1.py; course/modules/M/M5/L06.html:204-220",P,
     "exit 0; embedded == run (lab_compare_r4.out)."),
 row("M5-b-L07-lab-run","L07 twin runs and embedded output matches","tests/labs/M5/lab-M5-L07-1.py; course/modules/M/M5/L07.html:282-295",P,
     "exit 0; embedded == run (lab_compare_r4.out)."),
 row("M5-b-cmd-run_labs-check_pages-dag-smoke","Gate commands for M5 and page smoke","tools/run_labs.py --unit M5; tools/check_pages.py --unit M5; tools/check_dag.py --unit M5; tools/page_smoke.py --unit M5 --pages L05 L06 L07",P,
     "Outputs: 'run_labs M5: PASS (13/13)'; 'check_pages M5: PASS'; 'check_dag M5: PASS'; page_smoke L05, L06, L07 each PASS and 'page_smoke M5: PASS' (ledgers/M5/scripts/M5-b-r4/page_smoke_L05_L07.out, 11.8 s wall)."),
 row("M5-b-hours","Declared hours and hub arithmetic","course/modules/M/M5/L05.html, L06.html, L07.html data-hours; L01-L10 data-hours; index.html:29",P,
     "data-hours: L05 10, L06 10, L07 11 (eyebrows agree). All ten lessons: L01-L06 10 each, L07-L10 11 each, sum 104 = index.html data-hours-lessons 104; project 26; total 130. Pace not judged (architect ruling)."),
 row("M5-b-numbers-prose","Every displayed number in L05-L07 prose and solutions","L05 Emp-3, Part B/C text; L06 Emp-2, Emp-1; L07 M2, R2, E1, E2, E3, Misc 3, Part B/C text",P,
     "Recomputed in ledgers/M5/scripts/M5-b-r4/nums_b4.py (output nums_b4.out): 0.99^100 = 0.36603; (1/2)^9 and (1/2)^10; 1/4-12/49 = 1/196 = 0.00510; 3/3^14 = 6.2723e-7; 3/3^13 = 1.8817e-6; R2 n=91 (threshold 90.71); 2.661258/0.05439523 = 48.92; E2 f'(5)=0.980581, f'(50)=0.999800; window maxima 0.980390 and 0.999798; Part B max 0.840117 at (0.995,1). Explanation issue in E2 is row M5-b-r4-L07-E2-sign-and-maximiser."),
 row("M5-b-grades-and-theorems","Grades and proof completeness of T-graded results","course/modules/M/M5/L05.html Props 1.3, 2.1, 2.4, 2.5, 3.1, 3.2; L06.html Prop 1.3, 1.4, 2.1, Cor 2.2, 3.1, Cor 3.2, 3.4; L07.html Thm 2.1, Prop 1.4, Prop 2.4, Prop 3.1, Cor 3.2",P,
     "Every T-graded proof re-read and re-derived. The L05 Prop 2.1 hypothesis defect is fixed (row M5-b-r3-L05-prop21-continuity-definition). Prop 3.1 of L07 is T under the explicitly listed Assumption 1. Note (not a FAIL): L07 Lemma 2.2 carries no data-grade attribute; its proof is complete."),
 row("M5-b-l07-canon-breaks-and-misconceptions","Canon-break items and misconceptions in L07","course/modules/M/M5/L07.html canon-breaks items 1-3 and misconceptions 1-3",P,
     "Item 1 (x/2 on (0,1]) recomputed; item 2 identity |phi x - phi y| = |x+y||x-y|/(phi x+phi y) and limit 1 recomputed; item 3 Cor 3.2 self-map condition. Misconception 2 reverse triangle inequality correct; misconception 3 ratio 2.661258/0.05439523 = 48.92 recomputed."),
 row("M5-b-scope-and-process-words","Scope words (only, all, always, every, any, same, drives, about) and process words in L05-L07","course/modules/M/M5/L05.html, L06.html, L07.html (grep); L07.html:52, :102",F,
     "Process words (build, builder, round, verifier, REQUESTS, unit report) absent. Scope words checked in context: all remaining uses have a computation or proof behind them except L07 timing words 'before any iteration is run' (:52) and 'known before the iteration runs' (:102). Those are the same defect as row M5-b-r4-L07-before-iteration.",
     "See M5-b-r4-L07-before-iteration: say 'from the first iterate x_1 onward' instead of 'before any iteration'."),
 row("M5-b-citations-registry","Registry keys and cross-references cited by L05-L07","course/modules/M/M5/L05.html:389-392, L06.html:421-424, L07.html:512-516 (data-references); tools/verify_refs.py",P,
     "No registry key or data-locator in L05-L07. 'python tools/verify_refs.py --unit M5': '2 of 560 entries, 0 problems'. 'python tools/verify_refs.py --offline': '560 entries, 0 problems'. Internal cross-references (L01 Def 1.1, L02 Def 2.1 and Thm 2.5, L03 Def 1.1, L04 Def 1.1, 3.1, 3.2, 3.3, 4.1, 4.2, Ex 1.6, Prop 1.7) read and match."),
 row("M5-b-l07-input-facts","Assumptions 1 and 2 and their use","course/modules/M/M5/L07.html Assumption 1 (:154), Assumption 2 (:159), Example 3.3 (:181)",P,
     "Assumed facts are explicitly labelled as assumed. Numerically cos t in (0,1] on [0,1] (min 0.5403) and sin strictly increasing on [0,1] were checked by the lab output. No external number is cited."),
 row("M5-b-mutants-not-applicable","Mutation testing scope for slice b","ledgers/M5/mutants/ (not part of slice b)",P,
     "Slice b is lab twins and pages. ARCHITECT RULING: mutation testing applies to project graders only (slice d). No mutants were required for this slice."),
 row("M5-b-r3-L05-prop21-continuity-definition","Prop 2.1 hypothesis for a general metric space","course/modules/M/M5/L05.html:181 and :38; L04.html:302-304 (Def 4.1)",P,
     "Hypothesis (2) now says continuous 'in the sense of L04, Definition 4.1' for maps X->R on a metric space X; L04 Def 4.1 is defined for metric spaces (X,d_X),(Y,d_Y). The proof's d(x0,z)<delta matches. Uses lines at L05:38, L06:38, L07:38 updated."),
 row("M5-b-r3-L06-partC-scope","Part C scope claim (round-3 FAIL)","course/modules/M/M5/L06.html:221; lab lines 95-96",P,
     "See row M5-b-L06-partC-proposition-number: the sentence now claims only that the argument applies verbatim; verified."),
 row("M5-b-r3-L06-lab-pool-wording","Lab hypothesis wording of the kept half (round-3 FAIL)","course/modules/M/M5/L06.html:101; tests/labs/M5/lab-M5-L06-1.py bisect_prefix (pool, in_left/in_right)",P,
     "Hypothesis now keeps 'the half that contains more of the remaining prefix indices (those after the last chosen index) inside the current interval', which is the code's pool = indices after last_index with value in the interval; ties go to the left half (code), which the hypothesis does not need to state."),
 row("M5-b-r3-L07-strictly-closer","'strictly closer' wording for x = y (round-3 FAIL)","course/modules/M/M5/L07.html:52; Definition 1.1 at :60-62",P,
     "Now 'pulls every pair of distinct points strictly closer together'. For distinct points d(phi x,phi y) <= beta d(x,y) < d(x,y) since d>0 and beta<1; the x=y case is excluded."),
 row("M5-b-r4-cards-scan","Cards for L05-L07 against the current lesson text; duplicate scan","course/modules/M/M5/cards.json (52 cards for L05-L07; 190 total)",P,
     "All 52 slice cards read against their lesson text. Full duplicate scan of cards.json: 0 duplicate ids and 0 duplicate fronts. Cards that disagree with the current text are the rows M5-b-r4-card-c089 and M5-b-r4-L07-before-iteration (card M5-c105). Other cards (including M5-c073, which states continuity without the L04 Def 4.1 wording, a shorthand of the hypothesis) agree with the text."),
 row("M5-b-r4-card-c089","Card M5-c089 agrees with the current Example 1.5",f"course/modules/M/M5/cards.json:{c089} (M5-c089); course/modules/M/M5/L06.html:96",F,
     "The card says 'The sequence 1/n in (0, 1) has every subsequence converging to 0'. Example 1.5 now uses x_n=1/(n+1) because 1/1 is not in (0,1); 1/n with n=1 gives 1 outside K. The card contradicts the current lesson text.",
     "Change the card back to: 'The sequence 1/(n+1) in (0, 1) has every subsequence converging to 0, which is not in (0, 1) (Example 1.5).'"),
 row("M5-b-r4-L07-before-iteration","Timing claim about the a priori bound","course/modules/M/M5/L07.html:52 and :102; course/modules/M/M5/cards.json:%d (M5-c105)" % c105,F,
     "L07:52 says the distance 'is bounded before any iteration is run'; L07:102 says the bound 'uses only x_0 and x_1, so it is known before the iteration runs'. The bound needs d(x_0,x_1)=|x_1-x_0| with x_1=phi(x_0), i.e. one application of the iteration map, so it is available only after the first iterate is computed."
     ,
     "Rewrite L07:52 as 'the distance to it is bounded from the first iterate onward' and L07:102 as 'it uses only x_0 and x_1, so it is known once x_1 is computed, before the later iterates'. Make card M5-c105 say the same."),
 row("M5-b-r4-L07-E2-sign-and-maximiser","E2 explanation names the maximising pair and the sign","course/modules/M/M5/L07.html:393 (E2 solution)",F,
     "Recomputed: the window maximum on [-5,5] is attained at the pair (-5.0,-4.95) with ratio 0.9803902718 (nums_b4.out), the left end, not the right end. The solution argues with signed f' at the right end (x=5 and x=50) and says 'the average of f' over a pair lies below its value at the right end'. The printed value equals |avg f'| on that pair; the inequality holds (0.980390 < f'(5)=0.980581), but the page never names the maximiser and the argument compares signed values for a quantity defined with absolute values.",
     "Name the maximising pair (-5,-4.95) and use f' odd with |f'| increasing in |x|, so |avg f'| on the pair is below |f'(-5)| = f'(5) = 5/sqrt(26); state f'(50) and the 50 window likewise."),
 row("M5-b-r4-continuity-unproved-steps","Continuity of x^n and of a maximum asserted without proof or locator","course/modules/M/M5/L05.html:200 (Example 2.3); course/modules/M/M5/L05.html:299 (Research 2 solution)",F,
     "Example 2.3 (in the key results row for a T result) says 'Each f_n is a polynomial, hence continuous' with no proof or locator; L03 proves only sums (Prop 1.5) and x^2 at 2 (Prop 1.4), no product result. Research 2 says 'Each f_n is a maximum of continuous functions, so it is continuous' with no locator; L03.html:339-341 contains this as a problem with a solution.",
     "Example 2.3: prove continuity of x^n by induction using the product of continuous functions, or cite an M2 locator that proves polynomial continuity. Research 2: cite L03 problem (max of continuous functions) with its locator."),
 row("M5-b-r4-lab-twins-run","Twins run under -I -W error; embedded outputs match; lint and tests","tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py; ledgers/M5/scripts/M5-b-r4/lab_compare_r4.py",P,
     "exit 0 for all three; embedded == run True for L05, L06, L07 (lab_compare_r4.out). ruff check and ruff format --check pass on the three twins; .venv/bin/python -m pytest -k 'M5 or lab' passed (all dots, no failures)."),
]
frag = {
 "unit": "M5", "slice": "M5-b", "round": 4,
 "verifier": "round-4 independent verifier (Haiku), slice M5-b (L05-L07 and lab twins); did not build M5; shares no context with the builders",
 "pin": "2657ab5", "base": "aa3c26c",
 "checkout": "/tmp/verifyB4-M5-b (detached at 2657ab5; .venv symlink)",
 "scratch": "/tmp/M5-b4-scratch",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "FAIL",
 "mutants": [], "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta since round 3 (aa3c26c..2657ab5, git diff --stat): course/modules/M/M5/L05.html, L06.html, L07.html and cards.json changed (cards for L05-L07 c069-c120 re-read). Lab twins lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py are byte-identical to aa3c26c (not in the diff). L04.html and lab-M5-L04-1.py changed but are not in this slice; L05-L07 depend on L04 Def 4.1, Def 3.2, Prop 3.3, Prop 4.2 and Ex 1.6, which were read at 2657ab5.",
  "No previous PASS row is carried by byte-identity: the pages changed, so every row was re-verified from the 2657ab5 text.",
  "Gaps: L08 was read only for the cross-reference in L05:52; L09/L10 are not in this slice. The project grader (slice d) is not verified here. No Abbott or Rudin claim exists in L05-L07; no web source was read.",
  "Not run: full gate (ruff over whole repo, mypy strict, full pytest, render_curriculum, verify_refs live over all units). Run for this slice only, per the targeted-check rule.",
  "Lemma 2.2 in L07 has no data-grade attribute (its proof is complete): a layout note, not a row.",
 ],
 "summary": "M5-b round 4 (2657ab5): 40 rows, 6 non-PASS (FAIL). The L05 why-it-matters row was PASS in round 3 and is FAIL now (the L08 cross-reference was not checked before): L05 why-it-matters cross-reference to L08 (unsupported), card M5-c089 contradicting Example 1.5 (1/n vs 1/(n+1)), L07 timing claim 'before any iteration' (L07:52, :102, card M5-c105; also the scope row), L07 E2 explanation not naming the maximising pair, and unproved continuity steps in L05 Example 2.3 and Research 2. Round-3 FAILs (7) re-verified: 6 now PASS (Prop 2.1 hypothesis, Part C scope, lab pool wording, 'strictly closer'; the grades row and the 'partC proposition number' row), scope row still FAIL for the timing words. Lab twins run exit 0 and embedded outputs match; check_pages, check_dag, run_labs (13/13) and page_smoke for L05-L07 pass; verify_refs live (M5) and offline pass.",
 "rows": rows,
}
out = root / "ledgers/M5/M5-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
print("rows", len(rows), "fail", sum(r["status"] == F for r in rows))
