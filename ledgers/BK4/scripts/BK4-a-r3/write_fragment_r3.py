"""Write the BK4-a round-3 verifier fragment (ledgers/BK4/BK4-a.json).

Keeps every round-2 row id (check and location from the round-2 fragment), sets the round-3 status and evidence,
and adds the round-3 rows. Run from the repo root: python3 -I ledgers/BK4/scripts/BK4-a-r3/write_fragment_r3.py
"""

import datetime
import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

R2 = json.load(open("/Users/billyribeiro/.fanout/frags/E-BK4-a.round2.json", encoding="utf-8"))
R2_ROWS = {r["id"]: r for r in R2["rows"]}

CARRY_FC1 = (
    "Carried from round 2 (course/modules/BK/BK4/L01.html:55 and course/modules/FC/FC1/L05.html byte-identical "
    "since the previous pin; FC1 changes this round were cards.json, grader and project.html only): "
)
CARRY_HUB_PREREQ = (
    "Carried from round 2 (course/modules/BK/BK4/index.html:35 and :61 and curriculum/*.yaml byte-identical since "
    "the previous pin; the round-3 diff touches no curriculum file): "
)

V = {}  # id -> (status, evidence, fix)


def ok(i, ev):
    V[i] = ("PASS", ev, None)


def bad(i, ev, fix):
    V[i] = ("FAIL", ev, fix)


# ---- hub ----
ok("BK4a-hub-hours-arithmetic",
   "Read index.html:29 (data-hours-lessons=\"35\", data-hours-project=\"15\"), :42 ('35 h lessons · 15 h project (30% of "
   "the 50 module hours)'), :164-176 hours table: 2+2+3+3+2+2+1 = 15, Total row 15. L01-L03 declare 7 h each "
   "(data-hours=\"7\", eyebrow '7 study hours'); L04-L05 cards show 7 h (index.html:145-146). 5 x 7 = 35. 15/50 = 30%.")
ok("BK4a-hub-placement-arithmetic",
   "Read index.html:71-73, 76-133: eight items Pq1-Pq8. 0.8 x 8 = 6.4, so seven correct needed; 6/8 = 75%, 7/8 = 87.5% "
   "(index.html:73). data-mastery=\"0.8\" (line 71). Skill items Pq7 (line 121, data-skill) and Pq8 (line 126, data-skill). "
   "Six prerequisite items: M1 (Pq1, Pq2), M2 (Pq3), E1 (Pq4), P0.1 (Pq5), FC1 (Pq6).")
ok("BK4a-hub-placement-keys",
   "Keys re-derived by hand this round: 110/1.1 = 100 (index.html:79 correct option); 1 + 1/2 + 1/4 = 1.75 (data-answer "
   "1.75, line 84); lim 2x at 3 = 6 (data-answer 6, line 89); Bertrand price = c (line 97); grade C (line 108); FC1 lifecycle "
   "clearing before settlement (line 116); rung 1 min(120-100, 50) = 20 (data-answer 20, line 121); rung 2 residual 1 cent, "
   "floor(1 x 1/3) = 0 for each survivor, leftover goes to the first survivor (line 129).")
ok("BK4a-hub-prereq-chain", CARRY_HUB_PREREQ +
   "BK4 prereqs [FC1] (curriculum/02-economics-finance-core.yaml:1075); FC1 prereqs [P0.1, E1] (yaml:367); "
   "E1 prereqs [M2] (yaml:22); M2 prereqs [M1] (curriculum/01-foundations.yaml:126).")
ok("BK4a-hub-P0.1-link",
   "Re-read index.html:35 'P0.1 is not yet released in this program.' (no link). ls course/modules shows no P directory "
   "(AC AP BK CF CS E FC LX M PC S SC).")
ok("BK4a-hub-financial-intermediary",
   "Re-read index.html:63-64: the FC1 list names clearing and settlement, the trade lifecycle and bank money creation, "
   "each linked to concepts.html; no financial-intermediary term is used in the hub prerequisites.")
ok("BK4a-hub-bertrand-trade-fee",
   "index.html:64 'Bertrand competition, which placement item 4 uses.' Item 4 is Pq4 (index.html:95-101, the Bertrand "
   "question). Consistent.")
ok("BK4a-hub-concept-anchors",
   "Re-checked this round: course/concepts.html contains id=\"clearing-and-settlement\", \"trade-lifecycle\", "
   "\"bank-money-creation\", \"bertrand-competition\", \"present-value\", \"geometric-series\", \"limit\", one each "
   "(ledgers/BK4/scripts/BK4-a-r3/out/concept_anchors.txt). Hub links index.html:63-66 and the L01/L02 links (L01.html:37, "
   "59, 64; L02.html:37, 275) resolve (link_check.py: 61 links checked, 0 problems).")
ok("BK4a-hub-ladder-vs-project",
   "Hub index.html:154 'four-member clearing house, with a seeded SIMULATED set of 40 scenario losses' matches "
   "project.html:45 (four-member clearing house, Lab 1 worked example), :54 (four members, SIMULATED), :107 (40 scenario "
   "losses from a seeded generator). project.html changed this round; these lines were re-read.")
ok("BK4a-hub-data-status",
   "grep -c data-files on index.html, L01.html, L02.html, L03.html: 0 each. data_sources.yaml unchanged this round "
   "(ids fx_daily, fx_monthly, ust_daily). index.html:184 'No data is used in BK4' is consistent.")
ok("BK4a-hub-reading-list",
   "verify_refs.py --unit BK4 (live this round): '2 of 560 entries, 0 problems', exit 0. Plain curl to "
   "api.crossref.org/works/10.1093/rapstu/rar001 (out/crossref_duffie.txt): title 'Does a Central Clearing Counterparty "
   "Reduce Counterparty Risk?', Review of Asset Pricing Studies 1(1), 2011. index.html:193 matches curriculum yaml:1089-1092. "
   "No sec.gov record in references.json (grep count 0), so the SEC rule is not stated (index.html:193).")
ok("BK4a-hub-process-words",
   "ledgers/BK4/scripts/BK4-a-r3/banned_process_scan.py output (out/banned_process_scan.txt): hits 0 for index, L01, "
   "L02, L03 (BANNED and PROCESS lists).")
ok("BK4a-hub-P0.1-grade-source",
   "index.html:110 grade C definition = BLUEPRINT.md:161 row C (working paper, practitioner research, single-sample "
   "evidence). The parenthetical cites P0.1, which curriculum/01-foundations.yaml:6-17 lists as introducing "
   "'evidence-grade'. Note: P0.1 is unreleased (index.html:35), so the learner cannot read it; the grade definition is "
   "readable at BLUEPRINT.md:161 and on the lesson legend. Not a claim defect.")
ok("BK4a-hub-card-L02",
   "index.html:143 card text 'checked in Lab 1 on seeded SIMULATED trades' matches L02 section 3 heading 'Lab 1: netting for "
   "one seeded set of trades' and the lab title 'Lab 1 · Exposure before and after a central counterparty (SIMULATED)'.")

# ---- L01 ----
ok("BK4a-L01-numbers",
   "ledgers/BK4/scripts/BK4-a-r3/rederive_slice_a_r3.py (out/rederive_slice_a_r3.txt, all OK): nets +379800, -1533900, "
   "+1154100 (sum 0); RTGS needs 112500, 1533900, 0; debits 0, 1533900, 0; gross 2841600; moved 1533900. Ratio "
   "1533900/2841600 = 5113/9472 = 0.53980152..., which rounds half up to 0.5398 at four places (L01.html:286). The lab "
   "prints neither the ratio nor a percentage (twin stdout: out/twin_L01.stdout).")
ok("BK4a-L01-prop-2.2-2.4",
   "L01.html:84-111 re-read this round. Prop 2.2 (Need = max(0,-min S)): constraint o >= -S_k for all k, least o is "
   "max(0,-mu). Prop 2.3: each payment adds +a and -a, s != r by A1.3. Prop 2.4: k = m is in the minimum, so mu <= Net, "
   "and max(0,.) is nondecreasing; strictness by Example 2.6 (Need 100, Debit 50). Hypothesis 'Under Assumption 1.3' at "
   "L01.html:69-71 covers A1 and A2.")
ok("BK4a-L01-P2-iff",
   "L01.html:375-377 re-read this round. Case analysis with mu = min S, Need = max(0,-mu), Debit = max(0,-S_m), mu <= S_m: "
   "mu >= 0 gives both zero; mu < 0 and S_m = mu gives both -mu; mu < 0 and S_m > mu gives Need = -mu > Debit. "
   "Hypotheses named (mu <= S_m, Section 2 definitions).")
bad("BK4a-L01-examples-remarks",
    "Example 2.6 (L01.html:119-120) and Remark 2.7 (L01.html:124-125) re-derived: Need_A 100, Net_A -50, Debit_A 50, Need_A 50 "
    "after payment 3 is sent first (out/rederive_slice_a_r3.txt). BUT Remark 2.5 (L01.html:115) reads 'The order of payments "
    "changes the peak need, and so it changes the gap between the peak need and the net debit.' As a universal statement it "
    "is false: in Example 2.6 the order (payment 2, payment 1, payment 3) leaves Need_A at 100 "
    "(out/counterexamples_r3.txt line 1).",
    "L01.html:115: change 'The order of payments changes the peak need, and so it changes the gap' to 'The order of "
    "payments can change the peak need, and so it can change the gap'.")
ok("BK4a-L01-remark-3.1-order",
   "Round-2 FAIL fixed. L01.html:300 now reads 'The running minimum of S_{i,k} depends only on the order of the payments to "
   "or from i, because S_{i,k} changes only at those payments.' Re-derived: S_{i,k} changes only at payments involving i, so "
   "the running minimum depends only on their order; inflows-first gives min(0, Net) (re-derived in out/rederive_slice_a_r3.txt).")
bad("BK4a-L01-problems-M-P-E-R",
    "M1 (L01.html:343-345: Need 200, Debit 200), M2 (349-352: 200, 100), M3 (357-359: 30, 20), P3 (381-384), E1 (393-395), "
    "E2 (400-402), E3 (407-409: 1533900/2841600 = 0.5398, base gross value), R2 (425-427), R3 (432-434) re-derived; all "
    "correct. R1 at L01.html:420 is corrected (see BK4a-L01-R1-order-claim). FAIL is P1 at L01.html:368-370: the prompt asks "
    "'state which part of Assumption 1.3 it uses', and the solution says only what the proof does not use (the sending order, "
    "and distinctness). It never states the part used (A1: the day's payments are a fixed finite list, so the sum is over a "
    "finite set).",
    "L01.html:370: add a sentence that states the part used, e.g. 'The proof uses only A1: the payments of the day form a "
    "fixed finite list, so the sum is finite.'")
ok("BK4a-L01-R3",
   "L01.html:432-434 unchanged this round. Each bank receives and sends 100 dollars; Net 0; Debit = max(0,-Net) = 0; "
   "A's running sums 0, -100, -100, 0 give Need 100 (re-derived).")
ok("BK4a-L01-remark-2.8",
   "L01.html:291 'Part B prints the inequality of Proposition 2.4 for each bank, and Part C prints the zero sum of Proposition "
   "2.3'. Printed output (twin stdout, out/twin_vs_page.txt): 'RTGS need at least DNS net debit: True' for each bank (Part B) "
   "and 'net positions sum to zero: True' (Part C).")
ok("BK4a-L01-interp-three-inequalities",
   "L01.html:286 'Part B shows the inequality of Proposition 2.4 for each bank on that day.' Part B prints the inequality for "
   "each of three banks (twin output lines 'RTGS need at least DNS net debit: True' x3). Consistent.")
ok("BK4a-L01-misconception-1",
   "L01.html:322: Bank A RTGS need 112500, DNS debit 0 (lab Part B); Bank B net -1533900, debit 1533900, RTGS need 1533900 "
   "(lab Part B). Both figures match the printed day.")
ok("BK4a-L01-misconceptions-2-3",
   "L01.html:326: Bank A net +379800, DNS debit 0, RTGS need 112500 (Part B). L01.html:330: Remark 2.7 values 100 to 50 and "
   "net debit 50 unchanged (re-derived). Claim 'only the peak need depends on order' (Remark 2.5 as stated) is consistent: "
   "Net and Debit are order-free (Net_A is -50 in every order, re-derived).")
ok("BK4a-L01-quiz",
   "Ten items at L01.html:463-534. Keys re-derived this round: net -200 gives debit 200 (L01.html:469); need 200 (474); "
   "Prop 2.4 'at least' and 'equality only in some cases' (483); doubled need 200 (488); 50 with payment 3 first (493); sum of "
   "net positions zero (502); net +50 gives debit 0 (511); lag 1 day, a lab parameter (520); 2841600 cents = 28416 dollars "
   "(525); T+1 named, not stated (534).")
ok("BK4a-L01-lab-twin",
   "tests/labs/BK4/lab-BK4-L01-1.py unchanged since the round-1 pin (git diff 1c1645f3..67a2d13 lists only L03-1.py). "
   "ledgers/BK4/scripts/BK4-a-r3/twin_vs_page.py: twin exit 0, stderr 0 bytes under python3 -I -W error; code block equals "
   "the twin file; expected block equals the twin stdout (out/twin_vs_page.txt).")
ok("BK4a-L01-notation",
   "ledgers/BK4/scripts/BK4-a-r3/notation_scan_r3.py (out/notation_scan_r3.txt): registered symbols T, \\Phi, \\gamma_3, "
   "\\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and \\mathbb{R}: none in any math chunk of index, L01, L02, L03. Macros "
   "used: \\mathrm, \\mathcal, \\ell, \\delta, \\mu (none registered-conflicting). Local letters d, o, k, S, L, M, A, G, K, Z, V "
   "are defined on their pages.")
ok("BK4a-L01-dag-defs",
   "L01.html:59 <dfn id=\"def-payment-system\" data-concept=\"payment-system\"> and L01.html:64 <dfn id=\"def-settlement-cycle\" "
   "data-concept=\"settlement-cycle\">; each defined once. Plain dfn for net debit and peak need at L01.html:80. Outside-closure "
   "terms: none used in L01 prose (grep for D1-D13 names: only 'T+1' as a rule name, L01.html:64).")
ok("BK4a-L01-why-words",
   "tools/check_pages.py --unit BK4 (out/check_pages_unit.txt): PASS; the why-it-matters limit (120 words) is enforced "
   "per lesson, and L01.html:51 is within it.")
ok("BK4a-L01-structure",
   "Order re-read this round: why it matters (L01.html:51); sections 1-4 (53-305); Lab 1 (128-287); canon breaks (308-313); "
   "misconceptions (318-330, three); problem set (336-438: M1-M3, P1-P3, E1-E3, R1-R3); key results (441-452); retrieval quiz "
   "(459-534, ten items); references (540-541). Hours 7 (data-hours=\"7\").")
ok("BK4a-L01-grades",
   "Legend L01.html:43-48 (T, A, B, C, D, X; the B gloss 'published, not settled' is the shared template gloss, "
   "course/templates/lesson.html:47, a template-level wording and not a BK4 defect). Propositions carry data-grade T "
   "(L01.html:84, 94, 104). Lab-derived key rows are C and name Lab 1 Parts B and C (L01.html:451-452).")
ok("BK4a-L01-FC1-claim", CARRY_FC1 +
   "FC1 L05.html:63 lists the six ordered states from order entry to settlement and position update; L01.html:55 'FC1 Lesson 5 "
   "followed one trade through that sequence' (round-2 evidence, unchanged).")
ok("BK4a-L01-canon-breaks-wording",
   "L01.html:308 'Four places where the analyst must act:' and the four items at L01.html:310-313 (no queues; the day is given; "
   "settlement cycle a parameter; no real-system claim). Count matches. The 'only' wording at :313 is a separate row.")
bad("BK4a-L01-canon-bullet-only-designs",
    "L01.html:313: 'so the lesson describes the two designs only in Definitions 1.1 and 2.1.' False as written: the lede "
    "L01.html:51 describes both designs ('gross real-time settlement, where each payment settles when it is sent, and deferred "
    "net settlement, where each bank settles only its net position at the end of the day'). Scope word 'only' not backed by "
    "a computation (fixer-rules, scope words).",
    "L01.html:313: replace with 'so the lesson states no fact about which design any real system uses; the two designs are "
    "defined in Definitions 1.1 and 2.1.'")
ok("BK4a-L01-A2-forward-ref",
   "L01.html:71 (A2) says 'the net debit, defined in Definition 2.1'. Definition 2.1 at L01.html:79-80 defines net debit as "
   "max(0, -Net_i). A forward reference that names the definition is permitted by fixer-rules ('a forward reference names the "
   "lesson and definition'). Not a defect.")
ok("BK4a-L01-R1-order-claim",
   "Round-2 FAIL fixed. L01.html:420: 'Such an order exists, because the running minimum of S_{i,k} depends only on the order "
   "of the payments involving i. The other payments can be placed anywhere...' Re-derived: the proof of Need = Debit under "
   "the inflows-first order is correct; the false claim about other banks' payments is gone.")

# ---- L02 ----
ok("BK4a-L02-prop-2.2",
   "L02.html:85-99 re-read. Parts (a)-(d) re-derived from A1-A3 (proof lines 95-98): receivables and payables each sum to G; "
   "sum n_i = 0; (c) from max(0,x) - max(0,-x) = x; (d) n_i <= Rec_i and max(0,n_i) <= Rec_i, so A <= G.")
ok("BK4a-L02-prop-2.3-title",
   "L02.html:102-103: statement 'A = G if and only if, for every member i, Rec_i = 0 or Pay_i = 0' matches the title. Consistent.")
ok("BK4a-L02-prop-2.3-proof",
   "L02.html:106-109 re-derived: Rec_i = 0 gives term 0 = Rec_i; Rec_i > 0 and Pay_i = 0 gives Rec_i; Rec_i > 0 and Pay_i > 0 "
   "gives a term strictly below Rec_i. Converse by contrapositive (L02.html:348-349).")
ok("BK4a-L02-example-2.4",
   "L02.html:113 re-derived (out/rederive_slice_a_r3.txt): Rec (50, 100, 80), Pay (100, 80, 50), n (-50, 20, 30), sum 0, "
   "A = 50, G = 230, reduction 180, floor(10000 x 180/230) = 7826 (7826.08...). Member 1 both receives and pays (line 113).")
ok("BK4a-L02-lab-claims",
   "L02.html:123 'The lab checks the identities of Proposition 2.2 on that set.' The lab checks (Part B) gross exposure equals "
   "gross notional, (Part C) net obligations sum to zero, (Part D) payments in equal payments out, and that A <= G. "
   "L02.html:127 hypothesis matches the code and the printed lines (twin output out/twin_vs_page.txt).")
ok("BK4a-L02-lab-numbers",
   "L02.html:241-270 printed numbers equal the twin output (twin_vs_page). Independent re-derivation (seed 2026, six trades, "
   "four members): gross 7596300; receivables 314500, 2067800, 3340300, 1873700; net obligations -3627000, +1753300, +3340300, "
   "-1466600 (sum 0); A 5093600 (= payers' total); reduction 2502700; 10000 x 2502700/7596300 = 3294.63, floored 3294 "
   "(out/rederive_slice_a_r3.txt). L02.html:270 interpretation states the same values.")
ok("BK4a-L02-lab-numbering",
   "L02.html:121 and :126 heading 'Lab 1' and section id lab-BK4-L02-1 (L02.html:125) matches the twin name "
   "tests/labs/BK4/lab-BK4-L02-1.py.")
ok("BK4a-L02-attribution",
   "L02.html:277, :285, :425; references.json:7411-7416 (duffie2011central). Crossref re-run this round (out/crossref_duffie.txt): "
   "title matches the registry and the 'question is their title' sentence. No finding is stated (L02.html:277, 425), so the "
   "abstract is not needed for this row. Paper-level attribution only.")
ok("BK4a-L02-canon-misconceptions",
   "L02.html:293-302: misconception 1 'A = 0 iff all n_i <= 0 iff (zero sum) all n_i = 0' re-derived; misconception 2 (CCP "
   "cannot fail) corrected by Proposition 2.2(b) being a bookkeeping identity.")
bad("BK4a-L02-problems",
    "M1 (L02.html:315-331: n (-10,-20,50,-20), A 50, G 180, 7222), M2 (322-324: 7826), M3 (329-331), P1 (340-342), P2 (347-349), "
    "P3 (354-356), E1-E3 (365-381), R2 (396-399), R3 (404-406) re-derived and correct. R1 (L02.html:389-392) is not: it claims "
    "that under Assumption 1.3 the reduction in basis points lies in [0, 10000] and equals 10000 exactly when A = 0. "
    "Definition 2.1 (L02.html:81) defines the basis-point reduction only with G > 0, and R1's solution divides by G. "
    "Assumption 1.3 (L02.html:69, trades numbered 1, ..., q) does not exclude q = 0, so G = 0 is not excluded. The "
    "hypothesis G > 0 is missing.",
    "L02.html:389-390: state R1 'under Assumption 1.3 with G > 0'; L02.html:421 gets the same hypothesis.")
bad("BK4a-L02-key-results",
    "Rows 418-420 and 422-425 re-checked against the proofs (T rows: Prop 2.2 a-d, Prop 2.3, P3, Example 2.4 worked by hand; "
    "C rows name Lab 1 Parts B to D and the question-only source). Row 421 is graded T 'Proved in Problem R1 under Assumption "
    "1.3' but its claim divides by G, which Definition 2.1 defines only for G > 0 (L02.html:81). Missing hypothesis.",
    "L02.html:421: add 'with G > 0' to the claim or to the 'Proved in' column.")
ok("BK4a-L02-quiz",
   "Ten items at L02.html:436-507. Keys re-derived: n_2 = 20 (442); A = 50 (447); sum zero (456); 7826 (461); netted equals "
   "gross iff no member both receives and pays (470); n_2 = 100 (475); CCP does not move money (484); zero sum does not show "
   "no default (493); 50936 dollars (498); cycle netted amount zero (507).")
ok("BK4a-L02-lab-twin",
   "tests/labs/BK4/lab-BK4-L02-1.py unchanged since the round-1 pin. twin_vs_page.py: exit 0, stderr 0 bytes under python3 -I "
   "-W error; code block equals the twin; expected block equals the twin stdout (out/twin_vs_page.txt).")
ok("BK4a-L02-why-structure",
   "L02.html:34-518: why it matters (L02.html:51, within the 120-word limit by check_pages); sections 1-4 (53-275); Lab 1 "
   "(121-271); misconceptions (290-302, three); problem set (308-407: M1-M3, P1-P3, E1-E3, R1-R3); key results (413-425); "
   "quiz (432-510, ten items); references (513-514). Hours 7.")
ok("BK4a-L02-meta-description",
   "L02.html:7 meta description 'Lab 1 on a seeded SIMULATED set of four members and six trades, in integer cents.' matches the "
   "lab (four members, six trades, SIMULATED, cents).")

# ---- L03 ----
ok("BK4a-L03-legend",
   "L03.html:43-48 identical to L01 and L02 and the shared template (course/templates/lesson.html:45-48).")
bad("BK4a-L03-four-resources",
    "L03.html:55 'Three resources pay a loss in this lesson, and the default funds of the surviving members pay what remains "
    "after them' matches Definition 1.1 (L03.html:66-73). But the same paragraph says 'does not model how it arises from closing "
    "out the defaulter's positions or from netting. Section 3 names that limit.' Section 3 (L03.html:416-421) names the "
    "close-out limit (L03.html:418) and no netting limit.",
    "L03.html:55: either add a Section 3 bullet that names the netting limit, or change 'Section 3 names that limit' to "
    "'Section 3 names the close-out part of that limit'.")
ok("BK4a-L03-notation-d",
   "L03.html:61 (A2 defaulter \\delta), :69-70 (layers with \\delta), :100 (Remark 1.4 IM_\\delta). grep for \\mathrm{IM}_d and "
   "\\mathrm{DF}_d: none. Notation scan (out/notation_scan_r3.txt): no registered symbol.")
ok("BK4a-L03-def-props-1.2-1.3",
   "L03.html:66-96 re-derived: Definition 1.1 layers a1 = min(L, IM), a2 = min(L - a1, DF), a3 = min(L - a1 - a2, K), Z; survivor "
   "shares floor(Z DF_i/D), leftover to the first survivors with DF_i > 0. Prop 1.2 and 1.3 proofs re-checked (p_i fractional "
   "parts; l <= n+ - 1; x_i + 1 <= DF_i). Rederive fixtures and the seeded survivor split 312/381/164 with residual 857 (OK).")
ok("BK4a-L03-remark-1.4",
   "L03.html:99-101: a2 > 0 gives L - a1 > 0 so a1 < L, so a1 = IM; a3 > 0 gives a2 = DF; Z > 0 gives a3 = K. Re-derived.")
ok("BK4a-L03-example-1.5",
   "L03.html:104-121 and table L03.html:108-117: eight rows (80, 120, 170, 180, 181, 200, 205, 300) re-derived with the lab's "
   "waterfall and conservation check (out/rederive_slice_a_r3.txt, 'L03 Ex1.5 row' and 'conservation row' lines, all OK). Lab "
   "Part A1 rows (twin output) match. Example 1.5 prose (L=200: 8 and 12; L=300: uncovered 20; L=181 leftover to member 1) OK.")
ok("BK4a-L03-example-1.6",
   "L03.html:124-126: D = 3; Z = 1 gives member 1 one cent; Z = 2 gives members 1 and 2 one cent each (re-derived, OK). "
   "Lab Part A2 output matches.")
ok("BK4a-L03-def-2.1-prop-2.3",
   "L03.html:132-165: Definition 2.1 (c(M) = count of L_s <= M; cover = floor(10000 c/S)); Remark 2.2 (min(L,M) = L iff L <= M). "
   "Prop 2.3 parts 1-3 re-derived: k in [1, S]; cover(M) >= t iff c(M) >= k iff M >= L_(k); smallest margin L_(k).")
ok("BK4a-L03-cor-2.4-ex-2.5",
   "L03.html:168-180 Corollary 2.4 argument correct (ceiling nondecreasing; sorted losses nondecreasing). Example 2.5: 9900 x 200 / "
   "10000 = 198 exactly (k = 198); 9975 x 200 / 10000 = 199.5 (k = 200). Lab Part B (twin output, L03.html:404-409) prints 2961 and "
   "2992 with brute-force agreement; re-derived with an independent draw (out/rederive_slice_a_r3.txt).")
ok("BK4a-L03-R1-note",
   "L03.html:529-533: the proof of Prop 2.3 Part 2 uses only that M is real and that c(M) is an integer. For real M, c(M) >= k iff "
   "M >= L_(k); smallest margin L_(k), attained. Re-read; argument correct.")
bad("BK4a-L03-canon-bullet-6",
    "L03.html:421 'A low target leaves a tail. At 9900 ... the two largest scenarios are above the sized margin. ... The sized "
    "margin does not depend on how large these two losses are.' The first part is correct (198 covered, 2 above, out/"
    "rederive_slice_a_r3.txt). The last sentence is false as written: for the seed 2026 draw (two largest losses 2981 and 2992), "
    "setting both to 0 moves the 9900-bps sized margin from 2961 to 2938 (out/counterexamples_r3.txt line 2). The claim holds "
    "only while each loss stays above the sized margin.",
    "L03.html:421: replace the last sentence with 'While each of these two losses stays above the sized margin, lowering or "
    "raising it does not change the sized margin; lowering either below the margin does.'")
ok("BK4a-L03-uses-meta",
   "L03.html:37: 'Uses: central counterparty and multilateral netting (L02)' with links to L02.html#def-central-counterparty and "
   "#def-multilateral-netting, which exist (L02.html:64, 81). 'Introduces: CCP default waterfall; margin cover level' matches "
   "dfn at L03.html:67 and :134.")
ok("BK4a-L03-misconceptions",
   "L03.html:429-442: four misconceptions each refuted on the page (Def 2.1 + Remark 2.2; Example 2.5 and Def 2.1 count "
   "statement; Remark 1.4 and Lab Part A3 within-margin scenario; Def 1.1 DF shares only). Re-read; consistent.")
ok("BK4a-L03-problems",
   "L03.html:448-546 re-derived: M1 (455-457: 100, 50, 30, 8, 12, total 200); M2 (462-464: c(4000) = 3, cover 7500, k = 3, "
   "margin 3000, cover(2999) = 5000); M3 (469-471: 40, 50, 50); P1 (480-482), P2 (487-489), P3 (494-496); E1 (505-507: 3058, "
   "102, 0); E2 (512-514: 857, 312+381+164); E3 (519-521: c = 198, 2 above); R1 (530-532); R2 (537-539: k = 99 and 100; "
   "exactly one above iff L_(99) < L_(100)); R3 (544-546: k = S iff S <= 399; S = 400 gives k = 399). All consistent.")
ok("BK4a-L03-key-results",
   "L03.html:558-565: T rows match Prop 1.2, 1.3, Remark 1.4, Remark 2.2, Prop 2.3, Corollary 2.4. C rows (564-565) name Lab 1 "
   "Parts A1, A2 and B and are labelled 'fixed fixture, not seeded' / 'seeded SIMULATED losses'. Values 2961 and 2992 match "
   "the printed output.")
ok("BK4a-L03-quiz",
   "Ten items at L03.html:576-641. Keys re-derived: DF is step 2 (583); member 1 pays 8 (588); 8 + 12 = 20 (593); Remark 2.2 "
   "(603); cover 7500 (608); k = 3 (613); 8001 gives k = 5 and 50 cents (623); floor(2/3) = 0 with leftover to member 1 (628); "
   "198 of 200 (638); k = 399 at 400 scenarios (643).")
ok("BK4a-L03-lab-twin",
   "tests/labs/BK4/lab-BK4-L03-1.py changed only in round 2 (not in the round-3 delta). twin_vs_page.py: exit 0, stderr 0 bytes; "
   "code block equals the twin; expected block equals the twin stdout (out/twin_vs_page.txt, L03 line). 192-line twin, "
   "main() at top level (line 192).")
ok("BK4a-L03-why-structure",
   "L03.html:34-657: why it matters (L03.html:51, check_pages PASS); sections 1-3 (53-416); Lab 1 (187-411); canon breaks "
   "(414-421); misconceptions (426-445, four); problem set (448-546: M1-M3, P1-P3, E1-E3, R1-R3); key results (553-565); quiz "
   "(572-646, ten items); references (649-650).")

# ---- gates (re-run this round) ----
ok("BK4a-gate-check-pages",
   "tools/check_pages.py --unit BK4 (out/check_pages_unit.txt): 'check_pages BK4: PASS', exit 0; --page L01, L02, L03 each PASS "
   "(out/check_pages_L01.txt, L02, L03). The index is covered by the unit-wide run (--page is lesson-only, tools/check_pages.py:431-437).")
ok("BK4a-gate-check-dag",
   "tools/check_dag.py --unit BK4 (out/check_dag.txt): 'check_dag BK4: PASS', exit 0.")
ok("BK4a-gate-run-labs",
   "tools/run_labs.py --unit BK4 (out/run_labs.txt): 'run_labs BK4: PASS (8/8)', exit 0.")
ok("BK4a-gate-page-smoke",
   "tools/page_smoke.py --unit BK4 --pages index L01 L02 L03 (out/page_smoke.txt): index, L01, L02, L03 each PASS; "
   "'page_smoke BK4: PASS', exit 0; lab timings 0.0 s.")
ok("BK4a-gate-ruff-mypy",
   "ruff check on the three twins: 'All checks passed!' (out/ruff_check.txt, exit 0). ruff format --check: '3 files already "
   "formatted' (out/ruff_format.txt). mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' "
   "(out/mypy.txt, exit 0).")
ok("BK4a-gate-pytest-labs",
   "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py (out/pytest.txt): 100% progress, no F, "
   "exit 0 (exit status captured this round; the round-2 status was not captured).")
ok("BK4a-gate-verify-refs",
   "tools/verify_refs.py --unit BK4 (live, out/verify_refs_unit.txt): 'live re-verification of BK4: 2 of 560 entries, 0 "
   "problems', exit 0.")
ok("BK4a-banned-and-process",
   "ledgers/BK4/scripts/BK4-a-r3/banned_process_scan.py (out/banned_process_scan.txt): 'hits 0' over index, L01, L02, L03 "
   "(BANNED: TODO, TBD, lorem, 'for brevity', ..., ellipsis outside code; PROCESS words).")
bad("BK4a-scope-words",
    "Scope words in the four pages were read in context. Failures: L01.html:313 'describes the two designs only in "
    "Definitions 1.1 and 2.1' (row BK4a-L01-canon-bullet-only-designs); L01.html:115 'The order of payments changes the peak "
    "need' (row BK4a-L01-examples-remarks); L03.html:421 'does not depend on how large these two losses are' (row "
    "BK4a-L03-canon-bullet-6). Others backed by computation or proof: 'every d' (L01.html:305, 312, no d in Props 2.2-2.4), "
    "'every order' (L01.html:115, Prop 2.4 proof uses k = m only), 'any set of trades' and 'however many members' (L02.html:118), "
    "'every scenario' (L03.html:316, c(M) = S for M >= max), 'every statement ... concerns initial margin' (L03.html:420, the "
    "model has no variation margin).",
    "Fix the three named sentences (rows above); no other scope-word change needed.")

# ---- assemble ----
rows = []
for rid, r in R2_ROWS.items():
    if rid not in V:
        raise SystemExit(f"no round-3 verdict for {rid}")
    status, ev, fix = V[rid]
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)
extra = [k for k in V if k not in R2_ROWS]
NEW_CHECK = {
    "BK4a-hub-P0.1-grade-source": ("2.3-grades", "index.html:110"),
    "BK4a-hub-card-L02": ("2.9-prose", "index.html:143"),
    "BK4a-L01-canon-bullet-only-designs": ("2.9-prose", "L01.html:313"),
    "BK4a-L01-A2-forward-ref": ("2.4-mathematics", "L01.html:71; L01.html:79-80"),
    "BK4a-L01-R1-order-claim": ("2.4-mathematics", "L01.html:420"),
    "BK4a-L02-meta-description": ("2.9-prose", "L02.html:7"),
}
for rid in extra:
    status, ev, fix = V[rid]
    chk, loc = NEW_CHECK[rid]
    row = {"id": rid, "check": chk, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

n_fail = sum(1 for r in rows if r["status"] != "PASS")
verdict = "PASS" if n_fail == 0 else "FAIL"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
frag = {
    "unit": "BK4",
    "slice": "BK4-a",
    "round": 3,
    "round_note": (
        "Round 3 of BK4-a (hub index.html, L01, L02, L03, lab twins 1-3). Delta from the round-2 pin 67c47689 to 67a2d13: "
        "index.html:143 (L02 card), L01.html:71, 115, 286, 296, 300, 313, 420, 447, 496, L02.html:7, 51, 123, 284, 324, "
        "L03.html:51 (edits, one line each); tests/labs/BK4 twins unchanged this round. Every "
        "round-2 row id is kept. Every line of the four pages was re-read this round as plain text "
        "(ledgers/BK4/scripts/BK4-a-r2/strip_lines.py), with raw markup checked where a tag mattered; every number and "
        "proof was re-derived by ledgers/BK4/scripts/BK4-a-r3/rederive_slice_a_r3.py; the two counterexamples are in "
        "counterexamples_r3.py; all gates were re-run."
    ),
    "verifier": "Haiku independent verifier, BK4-a round 3 (did not build BK4)",
    "pin": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b",
    "base": "67c47689c49435bc0e6639e3de4feded5eefdd64 (round-2 pin; round-2 fragment /Users/billyribeiro/.fanout/frags/E-BK4-a.round2.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-BK4-a (detached at 67a2d13; .venv symlinked; vendor copied)",
    "scratch": "/tmp/bk4a_r3_*.txt (working copies); kept copies under ledgers/BK4/scripts/BK4-a-r3/out/",
    "verified_at": now,
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "SEC T+1 settlement rule (curriculum yaml:1092): no registry record and no sec.gov record in references/references.json "
        "(grep count 0); review_queue.json:830 requires manual admission from an authoritative sec.gov URL. Index and lessons "
        "correctly say the rule is not stated (index.html:193; L01.html:64, 312). Needed before any settlement fact is stated (B1).",
        "duffie2011central: Crossref verified this round (ledgers/BK4/scripts/BK4-a-r3/out/crossref_duffie.txt). The publisher "
        "abstract (DOI resolves with HTTP 302) was not read; no finding is stated in the slice, so none is required for this slice.",
        "bisndcpmi: index-level only (references.json:2853, issuer, no report title); the hub and L02 use it only at index level.",
    ],
    "freshness_flags": [
        "Duffie and Zhu (2011) is the only CCP-risk source the slice cites, at paper level. The slice states no finding, so no "
        "2025-2026 literature is needed here; a debate brief on CCP risk would need post-2011 work, none of which is in the registry.",
    ],
    "notes": [
        "Slice inventory: course/modules/BK/BK4/index.html (199 lines), L01.html (554), L02.html (527), L03.html (663); lab twins "
        "tests/labs/BK4/lab-BK4-L01-1.py (123), lab-BK4-L02-1.py (113), lab-BK4-L03-1.py (192). Every line of each page was read as "
        "numbered plain text and every sentence in the slice was checked against its lab, its proof or its registry key.",
        "Forward references: L01.html:71 ('net debit, defined in Definition 2.1') and L02.html:51 ('net obligation ... (Definition "
        "2.1)') name the definition they point to. Fixer rules permit this. Accepted, not a defect.",
        "Placement-item grade C (index.html:110) cites P0.1, which is unreleased in the program (index.html:35); the grade "
        "definition is also at BLUEPRINT.md:161. Accepted, noted.",
        "Template gloss 'B published, not settled' (course/templates/lesson.html:47, shown on every lesson legend) is shorter than "
        "BLUEPRINT.md:162 row B. Template-level, outside the slice; not a BK4 defect.",
        "Not in slice and not verified here: L04, L05, project.html (except the hub's ladder claim and the L03 mention), the grader, "
        "cards.json, the project labs. The mutation test and the alternative implementations are not part of this slice.",
        "Could not check: the Duffie and Zhu publisher abstract (not needed; no finding stated). The live Pyodide runtime beyond "
        "page_smoke's own timing lines (page_smoke reports 0.0 s per lab).",
    ],
    "summary": (
        f"BK4-a round 3: {len(rows)} rows, {n_fail} non-PASS. Non-PASS: L01 Remark 2.5 quantifier (L01.html:115), L01 P1 "
        "missing assumption part (L01.html:368-370), L01 'only' at L01.html:313, L02 R1 missing G > 0 (L02.html:389-390 and "
        "421), L03 netting limit not named in Section 3 (L03.html:55), L03 false sensitivity sentence (L03.html:421), and the "
        "scope-word aggregate. All gates PASS. The round-2 Remark 3.1 and R1 defects are fixed."
    ),
}
json.dump(frag, open("ledgers/BK4/BK4-a.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "non-PASS", n_fail, "verdict", verdict)
print("validate:", ledger.validate(frag, "BK4-a"))
