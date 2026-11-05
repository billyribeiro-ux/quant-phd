"""Writes ledgers/BK4/BK4-d.json (round 10) from the rows recorded by the round-10 verification run."""
import json
import sys

OUT = "ledgers/BK4/BK4-d.json"
D = "ledgers/BK4/scripts/BK4-d-r10"
SRC_GEN = "course/modules/BK/BK4/cards.json"
GATE_CARDS = (
    "check_pages --unit BK4 PASS (ledgers/BK4/scripts/BK4-d-r10/out/check_pages_bk4.out); "
    "run_labs --unit BK4 PASS 8/8 (out/run_labs.out); page_smoke --unit BK4 --pages L01..L05 PASS (out/page_smoke_BK4_L01_L05.out)"
)

rows = [
    {"id": "cards-structure", "check": "2.7-structure", "location": f"{SRC_GEN} (100 cards)", "status": "PASS",
     "evidence": f"python -I {D}/card_structure.py {SRC_GEN} {D}/out -> out/card_structure.out: 100 cards, 100 unique ids, "
                 "all ids BK4-cNNN; per lesson L01 17, L02 25, L03 24, L04 19, L05 15; grades T 53, C 12, ungraded 35; "
                 "keys graded=grade+basis, ungraded=none; id gaps c042 c045 c070 c082 c085 (plan ids need not be sequential). "
                 "cards.json sha256 c7ddde2a...242a87e2, valid JSON."},
    {"id": "cards-duplicate-scan", "check": "2.7-duplicates", "location": f"{SRC_GEN} (full scan, front and back)",
     "status": "PASS",
     "evidence": f"out/card_structure.out: 100 distinct fronts, 100 distinct backs; 157 difflib pairs above 0.6 on front or back "
                 "(top list out/card_structure.out). Read each high pair in full: c049/c050 (9900 vs 9975 target), c008/c101 "
                 "(peak need vs net debit of A), c029/c102 (range vs zero exactly), c030/c103 (netted amount vs reduction), "
                 "c031/c092 (netted vs gross), c005/c023 (banks vs members), c003/c091 (peak need vs net debit), "
                 "c086/c094 (expected cost vs its rounding), c080/c100 (same value, different law), c075/c072 (different fact). No exact repeat."},
    {"id": "cards-coverage", "check": "2.7-coverage",
     "location": "L01-L05 Definitions, Propositions, Remarks, worked Examples, Problems, key-results rows, Misconceptions vs cards.json",
     "status": "PASS",
     "evidence": "Full read of out/L01.txt..L05.txt (extract_text.py of the current HTML, 3025 lines). Traced: L01 Def 1.1 c001, Def 1.2 c002, "
                 "Def 2.1 c003 c091, Prop 2.2 c004, 2.3 c005, 2.4 c006, P2 c007, Ex 2.6 c008 c101, Rem 2.7 c009, Rem 2.5 c015, Lab 1 "
                 "c010-c012 c014, misconceptions c013-c015. L02 Def 1.1 c016, Def 1.2 c017, A1.3 c018, Def 2.1 c019-c021 c095, "
                 "Prop 2.2(a)-(d) c022-c025, Prop 2.3 c026, Ex 2.4 c027 c028 c033, R1 c029 c102, P3 c030 c103, Lab 1 c031 c092, "
                 "Duffie c032, misconceptions c034 c035 c099. L03 Def 1.1 c036-c038 c058, Prop 1.2 c040, Prop 1.3 c041 c104, Ex 1.5 c043, "
                 "Ex 1.6 c044, Def 2.1 c039 c105, Rem 2.2 c055, Prop 2.3 c046, Cor 2.4 c047, Ex 2.5 c048 c056, Rem 1.4 c057, Lab 1 "
                 "c049 c050, A1-A2 layer/inputs c051-c054, variation margin c096, misconceptions c055-c058. L04 Def 1.1 c059, c060-c062, "
                 "Def 1.2 c063, Def 2.1 c064 c065 c097, Def 3.1 c066, Prop 2.2 c067, 2.4 c068, 2.5 c069, 2.6 c076, 2.7 c071, Rem 2.8 "
                 "c072 c075, Rem 4.1 c073 c074, claims c093, misconceptions c074 c075 c076. L05 Def 1.1 c077, Def 1.2 c078, Def 2.1 c079, "
                 "Prop 2.1 c080, 2.2 c081, 2.4 c100, 2.5 c083, 2.6 c084, Ex 2.7 c089, Ex 2.8 c086 c094, Lab 1 c086 c087 c090, "
                 "Assumption 1.3 joint law c098, misconceptions c088. Items with no card (L01 Rem 3.1, Problems M1-M3, P1, R1-R3, E1-E3; "
                 "L02 Problems M1-M3, P1-P2, E1-E3, R2-R3; L05 Problems M1-M3, P1-P3, E1-E3, R1-R3) are not required by the plan "
                 "card scope as stated in this round's inventory."},
    {"id": "cards-numbers", "check": "2.7-numbers", "location": f"{SRC_GEN} numbers vs lesson text",
     "status": "PASS",
     "evidence": f"python -I {D}/card_numbers.py -> out/card_numbers.out: total misses 0 (every number on every card appears in its "
                 f"lesson text). Independent re-derivation: {D}/seeded_rederive.py -> out/seeded_rederive.out: 53 checks, 53 pass "
                 "(c011 112500; c010 1533900 need=debit; c014 +379800; c012 2841600 and 0.53980152 digits; c031 5093600, 2502700, "
                 "3294 bps; c092 7596300; c028 7826; c027 50; c049/c050 k=198/200, 2961, 2992, brute force equal; c043/c044 8, 12, "
                 "20, 1 cent; c086 4375/2, 2188 half-up; c087 57421875/4, 133984375/4; E2 difference 19140625; c089 169/512, 192/512; "
                 "c084 343/512, 7/8; c072 11000; c075 9000 and 19/40; c073 20/19). Prior-round script rederive.py: 87/87 PASS (re-run)."},
    {"id": "cards-xrefs", "check": "2.7-xrefs", "location": f"{SRC_GEN} label references",
     "status": "PASS",
     "evidence": f"python -I {D}/card_structure.py -> out/card_structure.out: label cross-reference misses 0 (each cited Definition, "
                 "Proposition, Remark, Example, Problem, Corollary, Assumption label exists in its lesson text). Lab part references "
                 "(Part A1, A2, A3, B, C, D) checked against out/L0N.txt lab output headings."},
    {"id": "cards-lab-outputs", "check": "2.7-lab-outputs",
     "location": f"{SRC_GEN} C-graded cards and lesson Lab 1 blocks (L01-L05)", "status": "PASS",
     "evidence": "python -I ledgers/BK4/scripts/BK4-d-r10/lab_compare.py <checkout> out -> out/lab_compare.out: all 5 lesson labs: "
                 "page code equals twin True; twin exit 0; stderr 0 bytes under python -I -W error; expected block equals twin stdout True. "
                 "run_labs --unit BK4 PASS 8/8 (out/run_labs.out). C-graded card values read from out/lab-BK4-L0N-1.stdout: "
                 "c010/c011/c014 (L01 Part B), c012 (Part C amounts), c031/c092 (L02 Parts B, D), c049/c050 (L03 Part B), c086/c087 "
                 "(L05 Parts B, D), c090 (L05 Part C 1875), c094 (L05 Part B 4375/2)."},
    {"id": "cards-grades-vs-keyresults", "check": "2.7-grades-vs-keyresults",
     "location": f"{SRC_GEN} lines 346 and 355 (BK4-c043, BK4-c044) vs course/modules/BK/BK4/L03.html line 565 (key-results row)",
     "status": "FAIL",
     "evidence": "BK4-c043 and BK4-c044 are grade T (basis: Example 1.5 / Example 1.6 hand arithmetic). The L03 key-results row "
                 "(L03.html line 565) states 'The fixture rows of Example 1.5 and the remainder cases of Example 1.6 hold in exact integer "
                 "cents', graded C with source 'Lab 1, Parts A1 and A2 (fixed fixture, not seeded)'. The same claim carries two grades, "
                 "so the cards do not agree with the current lesson text. Round-9 fragment recorded this as an architect note, not a FAIL; "
                 "re-read this round, the mismatch is still present and the L03 row is C. Plan section 2.2 says a finite enumeration is "
                 "grade C with its basis named.",
     "fix": "Make the grades agree. Either regrade BK4-c043 and BK4-c044 to C with basis 'Lab 1, Parts A1 and A2 (fixed fixture)', "
            "or regrade the L03 key-results row to T with the hand arithmetic of Examples 1.5 and 1.6 as its source. Architect ruling "
            "needed, since plan 2.2 favours C for finite enumerations."},
    {"id": "cards-hypotheses", "check": "2.7-hypotheses", "location": f"{SRC_GEN} line 649 (BK4-c083) vs course/modules/BK/BK4/L05.html line 124 (Proposition 2.5 hypotheses)",
     "status": "FAIL",
     "evidence": "L05.html line 124: Proposition 2.5 hypotheses are 'the finite space of Assumption 1.3; A1 and A2; A3 for Var_3(C) and A4 "
                 "for Var_4(C); 0<p<1; kappa>0'. BK4-c083 front reads 'Assuming the finite probability space, A1, 0 < p < 1 and kappa > 0, "
                 "with A3 ... and A4 ...', so A2 is omitted. A2 is needed: C = kappa sum l_i 1{F_i} is the cost under A2 (Definition 2.1), "
                 "and the variance proof substitutes that C. Every other card with a Proposition hypothesis list (c004-c007, c022-c026, "
                 "c036-c041, c046-c047, c067-c076, c080-c081, c084, c088, c100, c102-c104) was checked against its lesson statement "
                 "and matches.",
     "fix": "BK4-c083 front: 'Assuming the finite probability space, A1, A2, 0 < p < 1 and kappa > 0, with A3 (independent failures) "
            "for the independent variance and A4 (comonotone failures) for the comonotone variance, ...'."},
    {"id": "cards-attribution-duffie", "check": "attribution", "location": "BK4-c032 (cite duffie2011central); references/references.json line 7411",
     "status": "PASS",
     "evidence": "Registry title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?' (references.json line 7416). "
                 "Live Crossref: curl -s https://api.crossref.org/works/10.1093/rapstu/rar001 (plain curl, no personal data) -> "
                 "title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', authors Duffie, Zhu, issued 2011-07-18, "
                 "container 'Review of Asset Pricing Studies' (out/crossref_duffie.json). Card text 'the question is whether a central "
                 "clearing counterparty reduces counterparty risk, the title' matches; no finding is attributed."},
    {"id": "cards-banned-and-process-words", "check": "2.2-banned-and-process-words",
     "location": f"{SRC_GEN} (all fronts and backs)", "status": "PASS",
     "evidence": "python -I scan of every card for scope words, process words (verifier, builder, round, draft, pending, placeholder, "
                 "TODO, agent, audit) and banned strings: none present. Scope words (only, all, every, exactly, never, any, whatever) "
                 "were each read against the lesson sentence it restates (see cards-scope-claims)."},
    {"id": "cards-notation", "check": "2.3-notation", "location": f"{SRC_GEN}; notation/notation.json (symbols T, Phi, gamma_3, gamma_4, R^ast, R^e-ast, R_f, Q)",
     "status": "PASS",
     "evidence": "Cards contain no registered symbol. 'T' appears only in 'the T+1 rule' (BK4-c002, plain text, a rule name; L01 "
                 "Definition 1.2 names it and does not state it), consistent with plan section 12 ruling 7 (T+1 only as a rule name). "
                 "Local letters (ell, D, C, S, x, k, t, G, A, K, Z, u) are defined in each lesson where used (L03 ell = leftover, "
                 "L05 ell = delay, stated 'the symbol ell is not the settlement cycle d of L01'); notation.json says conventionally "
                 "local letters are defined per lesson. Registered macros \\E, \\Prob, \\Var, \\indic appear in lessons; none are "
                 "redefined. No card uses LaTeX."},
    {"id": "cards-dag", "check": "4-dag", "location": f"{SRC_GEN}; check_dag BK4",
     "status": "PASS",
     "evidence": "python tools/check_dag.py --all -> out/check_dag_all.out: 'check_dag BK4: PASS'. Concept scan of cards (clearing, "
                 "present value, geometric, Bertrand, bank money, deposit, derivative, swap, option): only 'clearing house' and "
                 "'central clearing counterparty' as ordinary prose in BK4-c032 and BK4-c053. No card links or names an FC1, E1, M1, "
                 "M2 or P0.1 concept."},
    {"id": "cards-pages-gate", "check": "2.7-pages", "location": "tools/check_pages.py --unit BK4",
     "status": "PASS",
     "evidence": "python tools/check_pages.py --unit BK4 -> out/check_pages_bk4.out: 'check_pages BK4: PASS' (exit 0)."},
    {"id": "cards-c001-c010", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c001..c010 (lines ~1-120)", "status": "PASS",
     "evidence": "Each card read against L01 text (out/L01.txt lines 42-100 and 236-259 for Lab 1 Parts B/C). c003 peak need = least o_i>=0 with o_i+S_{i,k}>=0 (L01 line 64). c004/c005/c006/c007 match Propositions 2.2-2.4 and P2 (L01 lines 66-88, 337-343). c008/c009 match Example 2.6 and Remark 2.7 (lines 94-100) and rederive.py checks. c010 Bank B 1533900 (line 238). Grades T/C match the key-results rows (lines 407-453)."},
    {"id": "cards-c011-c020", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c011..c020", "status": "PASS",
     "evidence": "c011 112500 (L01 line 237). c012 1533900/2841600 share 0.5398 (L01 line 255; the ratio is hand arithmetic from printed amounts). c013 and c014 read against Misconceptions (L01 lines 285-291). c015 against Remark 2.5 (line 90-92). c016-c020 match Definitions 1.1, 1.2, Assumption 1.3 and Definition 2.1 of L02 (lines 42-66)."},
    {"id": "cards-c021-c030", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c021..c030", "status": "PASS",
     "evidence": "c021 floor(10000(G-A)/G) (L02 line 66). c022-c025 = Proposition 2.2(a)-(d) (lines 72-78, proof 82-88). c026 = Proposition 2.3 (line 92). c027/c028 = Example 2.4 (line 100; 7826 floored, 180/230). c029 = Problem R1 (line 366-370, range 0..10000). c030 = Problem P3 (line 330-334)."},
    {"id": "cards-c031-c040", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c031..c040", "status": "PASS",
     "evidence": "c031 5093600 (out/lab-BK4-L02-1.stdout line 'amount paid after netting'). c032 Duffie checked live (cards-attribution-duffie). c033-c035 vs Section 4 and Misconceptions (L02 lines 254-278). c036-c038 = Definition 1.1 (L03 lines 50-58) and c038 leftover ascending id rule. c039 = Definition 2.1 (line 222). c040 = Proposition 1.2 (lines 62-66)."},
    {"id": "cards-c041-c050", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c041..c050 (c043 and c044 graded T; see cards-grades-vs-keyresults)",
     "status": "FAIL",
     "evidence": "c041 = Proposition 1.3 (L03 line 72). c043/c044 values re-derived (Example 1.5 table row L=200: 8, 12; Example 1.6 Z=2: members 1 and 2). c046 = Proposition 2.3 (lines 236-242). c047 = Corollary 2.4 (line 254). c048 k=198 (line 262). c049/c050 2961/2992 (out/L03.txt lines 478-483 lab output; brute force agrees). Only the grade of c043/c044 disagrees with the L03 key-results row (line 565).",
     "fix": "BK4-c043 and BK4-c044: regrade to C with basis Lab 1 Parts A1/A2 (fixed fixture) to match the L03 key row, or regrade the L03 key row to T. Architect ruling needed (see cards-grades-vs-keyresults)."},
    {"id": "cards-c051-c060", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c051..c060", "status": "PASS",
     "evidence": "c051-c054 definitions in L03 lines 40 (initial margin, default fund, CCP capital, surviving member). c055 = Remark 2.2 (line 226) and Definition 2.1. c056 = Example 2.5 and Misconception (lines 262, 507-509). c057 = Remark 1.4 (line 80). c058 = Definition 1.1 residual by DF (line 58) and Misconception (line 517). c060 reserve (L04 line 40)."},
    {"id": "cards-c061-c070", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c061..c070", "status": "PASS",
     "evidence": "c061 claim, c062 redemption, c063 Definition 1.2 (line 48-52), c064/c065 Definition 2.1 (line 72), c066 Definition 3.1 (line 326), c067 Proposition 2.2 (lines 76-84), c068 Proposition 2.4 (lines 92-96), c069 Proposition 2.5 (lines 100-104), c070 gap. All re-derived by property_check.py (L04 block, 30402 exact cases)."},
    {"id": "cards-c071-c080", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c071..c080", "status": "PASS",
     "evidence": "c071 Proposition 2.7 (lines 116-120). c072 Remark 2.8 (line 124: 11/10, 11000). c073 Remark 4.1 threshold 1/(1-h), h=1/20 gives 20/19 (line 336). c074 and misconception (lines 350-352). c075 (changed round 10): front and back match Misconception line 354-356 and Remark 2.8 (ρ=19/20, x=1/2 gives 9/10 = 9000 bps; ρ/2 = 19/40). c076 Proposition 2.6 (lines 108-112). c077 Definition 1.1 L05 (line 44). c078 Definition 1.2 L05 (line 48). c079 Definition 2.1 L05 (line 66). c080 Proposition 2.1 (line 70)."},
    {"id": "cards-c081-c090", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c081..c090 (c083 FAIL, see cards-hypotheses)", "status": "FAIL",
     "evidence": "c081 Proposition 2.2 (lines 78-86). c083 values re-derived (2 kappa^2 p(1-p) sum l_i l_j; E2 difference 19140625; property_check.py L05 block passes 400 cases). c084 Proposition 2.6 hypotheses match (L05 lines 114, 118). c086 4375/2 (L05 Part B lab output, out/L05.txt). c087 57421875/4 and 133984375/4 (L05 Part D lab output). c088 (L05 line 320). c089 Example 2.7 (line 122, 169/512, 3p=192/512). c090 1875 (L05 Part C lab output). Only c083 fails: its hypothesis list omits A2 (L05.html line 124; see cards-hypotheses).",
     "fix": "BK4-c083 front: add A2 to the hypothesis list, as in Proposition 2.5 (L05.html line 124)."},
    {"id": "cards-c091-c094", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c091..c094", "status": "PASS",
     "evidence": "c091 Definition 2.1 net debit (L01 line 64). c092 7596300 = sum of receivables (out/lab-BK4-L02-1.stdout lines 226-231, re-summed). c093 claims outstanding (L04 line 40). c094 rounding half up to 2188 (L05 lines 126, 394; property_check and seeded_rederive c094 PASS)."},
    {"id": "cards-c095-c098", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c095..c098", "status": "PASS",
     "evidence": "c095 multilateral netting (L02 line 64). c096 variation margin excluded (L03 line 497). c097 admissible share (L04 line 72, Remark 2.3). c098 joint law (L05 line 52)."},
    {"id": "cards-c099", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c099", "status": "PASS",
     "evidence": "Misconception 'zero sum shows CCP cannot fail' and netted amount zero iff all n_i<=0 (L02 lines 270-278). Re-derived by property_check.py L02 block (3000 random trade sets)."},
    {"id": "cards-c100-c101", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c100, BK4-c101", "status": "PASS",
     "evidence": "c100 Proposition 2.4 (L05 lines 92-98). c101 Example 2.6 A's net debit 50 (L01 line 96)."},
    {"id": "cards-c102-c104", "check": "2.7-card-read", "location": f"{SRC_GEN} BK4-c102..c104", "status": "PASS",
     "evidence": "c102 Problem R1 L02 (line 370). c103 Problem P3 L02 reduction 10000 (line 334). c104 Proposition 1.3 survivor bound (L03 lines 72-76)."},
    {"id": "cards-c105", "check": "2.7-card-read", "location": f"{SRC_GEN} line 826 (BK4-c105, changed in this delta)", "status": "PASS",
     "evidence": "Back now 'A scenario is one simulated loss', matching L03 intro line 36 ('one simulated loss per scenario') and Definition 2.1 (line 222): S losses, each a non-negative integer in cents, S>=1. Read against the current lesson text."},
    {"id": "cards-scope-claims", "check": "2.7-scope", "location": f"{SRC_GEN} all scope words (only, all, every, exactly, never, any, whatever, same)",
     "status": "PASS",
     "evidence": "Each scope word was read against its sentence and the computation or lesson statement it rests on: e.g. c001 'each bank settles only its net position' (L01 line 44); c018 'all trades t'; c022 'exactly one receivable' (A2); c048 'exactly 198' (Example 2.5 arithmetic); c056 'depends only on how many losses' (Definition 2.1); c066 'technical meaning only' (L04 line 326); c074 'whatever' (misconception line 350); c076 'Only when x=0 or rho=1' (Proposition 2.6); c096 'contains no variation margin' (L03 line 497); c099 'only when every net obligation is zero'. No unsupported universal claim found."},
    {"id": "cards-refs-live", "check": "2.7-refs-live", "location": "references/references.json (duffie2011central, bisndbasel); tools/verify_refs.py",
     "status": "PASS",
     "evidence": "python tools/verify_refs.py --offline -> out/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. Live: Crossref for DOI 10.1093/rapstu/rar001 (out/crossref_duffie.json) matches the registry title and authors. bisndbasel (issuer page) not re-fetched in this round: the card cites no Basel III content (BK4-c032 only cites Duffie)."},
    {"id": "cards-delta-round7", "check": "2.7-delta", "location": "cards.json history before round 8 pin",
     "status": "PASS",
     "evidence": "Historical delta covered by this round's full re-read of all 100 cards (not carried): every card read against the current L01-L05 text in this round."},
    {"id": "cards-delta-round8", "check": "2.7-delta", "location": "cards.json history between round-7 and round-8 pins",
     "status": "PASS",
     "evidence": "Historical delta covered by this round's full re-read of all 100 cards; no carried PASS row."},
    {"id": "cards-delta-round9", "check": "2.7-delta", "location": "cards.json delta c93dd526..00a84795 (BK4-c075 front, BK4-c105 back) and lesson hunks L01-L05, index, project",
     "status": "PASS",
     "evidence": "git diff --word-diff=plain c93dd526 HEAD -- course/modules/BK/BK4 tests/labs/BK4 plans/BK4-build-plan.md (saved as /Users/billyribeiro/.fanout/scratch-BK4-d-r10/delta.txt, 32.5 KB, 60+ changed hunks): all hunks read. Lesson hunks: L01 (E3 solution rounding digits, canon-breaks wording), L02 (canon-breaks wording), L03 (why-it-matters, scenario wording, C2/C5 rubric, Example 1.5 table text), L04 (misconception wording, prerequisite text), L05 (Problem monotonicity wording, rubric). Card-affecting hunks: c075 front and c105 back, checked against current lesson text (see cards-c071-c080 and cards-c105). Lab twin lab-BK4-L05-1.py changed (docstring only); lab_compare PASS. Plan hunk (cover_bps empty-input error row, Period convention removed) and project/index hunks do not touch any card-cited statement."},
    {"id": "cards-delta-round10", "check": "2.7-delta", "location": "course/modules/BK/BK4 and tests/labs/BK4 at 00a84795 vs c93dd526",
     "status": "PASS",
     "evidence": "Re-read this round: the delta changes card text only at c075 and c105; L01 E3 ratio digits (card c012 unaffected, which gives 0.5398 only); index and project prose; plan rows for the project. Hypothesis list for Prop 2.5 (L05.html line 124) unchanged in this delta; the c083 omission predates round 10 (see cards-hypotheses)."},
    {"id": "cards-property-checks", "check": "2.7-T-propositions", "location": "T-graded propositions and lesson statements behind cards",
     "status": "PASS",
     "evidence": f"python -I {D}/property_check.py -> out/property_check.out: 10 of 10 blocks PASS: L01 Prop 2.2/2.3/2.4, Remark 2.5, P2 (3000 random days); L02 Prop 2.2(a)-(d), 2.3 iff, R1 (3000 trade sets), P3 cycles; L03 Def 1.1 conservation, Prop 1.2, 1.3, Remark 1.4 (4000), Prop 2.3 and Cor 2.4 (6000 cases); L04 Prop 2.2, 2.4, 2.5, 2.6, 2.7 (30402 exact cases), Remark 4.1 threshold; L05 Prop 2.1/2.2/2.4, 2.5 sign and difference, 2.6 (400 random parameter sets, exact fractions)."},
    {"id": "cards-gates", "check": "gates", "location": "run_labs, page_smoke, check_dag, verify_refs, ruff on BK4 twins",
     "status": "PASS",
     "evidence": f"{GATE_CARDS}; check_dag --all: 'check_dag BK4: PASS' (out/check_dag_all.out); ruff check tests/labs/BK4/: 'All checks passed!' (out/ruff_bk4_twins.out); verify_refs --offline: 0 problems."},
]

fragment = {
    "unit": "BK4",
    "slice": "BK4-d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-d (cards.json against L01-L05), round 10; did not build BK4",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36 (detached; HEAD of the checkout)",
    "base": "c93dd526 (round-9 pin). Delta: cards.json (c075 front, c105 back); L01-L05 prose; index; project; lab-BK4-L05-1 twin docstring; plan line",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-BK4-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-BK4-d-r10 (delta.txt, word-diff of the BK4 delta); outputs in ledgers/BK4/scripts/BK4-d-r10/out/",
    "verified_at": "2026-11-05T07:10:57+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "duffie2011central: live Crossref matched; no new registry entry touched",
        "bisndbasel: cited at index level by L05 only; not re-fetched this round (no card depends on it)",
    ],
    "freshness_flags": [
        "Only cited work with a card: Duffie and Zhu (2011), question-level; no 2025-2026 literature checked for freshness",
    ],
    "notes": (
        "Slice d is cards.json only: no grader, so no mutants (no project grader changed in this slice). "
        "Two FAIL rows: BK4-c083 omits A2 from the Proposition 2.5 hypotheses (L05.html line 124); BK4-c043 and BK4-c044 are "
        "graded T while the L03 key-results row (L03.html line 565) grades the same fixture claim C. "
        "Not checked: the lesson prose outside what cards cite (owned by the lesson slices, rows there not re-verified); project.html, "
        "the grader and the project labs; ruff/mypy on the whole repo; build_site --check; fetch_data --check; run_graders; "
        "mutate_graders; verify_refs live beyond Duffie; Basel III operational-risk section (not cited by any card)."
    ),
    "summary": (
        "BK4-d round 10: FAIL. 100 cards re-read in full against the current L01-L05; 53 seeded/printed-number checks, "
        "10 property blocks and 87 prior-script checks, all PASS; 2 FAIL rows: BK4-c083 hypothesis omission (A2) and the "
        "BK4-c043/c044 grade mismatch with the L03 key-results row."
    ),
}

if __name__ == "__main__":
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
    for r in rows:
        if r["status"] != "PASS":
            r.setdefault("fix", r.get("fix", ""))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote", OUT, counts)
