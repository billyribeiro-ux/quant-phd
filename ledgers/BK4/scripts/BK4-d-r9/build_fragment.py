"""Writes the BK4-d round-9 ledger fragment from the rows verified in this round.

Every row cites a script under ledgers/BK4/scripts/BK4-d-r9/ or a command whose output is stored in out/.
Usage: python -I build_fragment.py   (run from the checkout root; writes ledgers/BK4/BK4-d.json)
"""
import json

OUT = "ledgers/BK4/scripts/BK4-d-r9/out"
S = "ledgers/BK4/scripts/BK4-d-r9"


def row(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}


rows = [
    row("cards-structure", "2.7-structure", "course/modules/BK/BK4/cards.json (100 cards)",
        f"python -I {S}/card_structure.py course/modules/BK/BK4/cards.json {OUT} -> {OUT}/card_structure.out: 100 cards, "
        "100 unique ids, all ids match BK4-c\\d{3}; per lesson L01 17, L02 25, L03 24, L04 19, L05 15; grades T 53, C 12, "
        "ungraded 35; two key sets (graded cards carry grade and basis; ungraded cards carry neither); id gaps c042, c045, c070, c082, c085 (ids need not be sequential, "
        "plan section 9). check_pages --unit BK4 PASS (rule-enforced: id prefix, lesson exists, grade set, registry keys, "
        "a non-T grade has cite or basis; every lesson has cards): " f"{OUT}/check_pages_bk4.out."),
    row("cards-duplicate-scan", "2.7-duplicates", "cards.json (full scan of front and back)",
        f"{OUT}/card_structure.out: 100 distinct fronts, 100 distinct backs. difflib pairs above 0.6 on front or back: 157; "
        "each read against its partner. Pairs that ask different facts: c049/c050 (9900 vs 9975 targets, 2961 vs 2992), "
        "c008/c101 (peak need vs net debit of A in Example 2.6), c029/c102 (range vs zero exactly), c030/c103 (netted amount "
        "vs reduction), c031/c092 (netted amount 5093600 vs gross notional 7596300), c005/c023 (Prop 2.3 on banks vs "
        "Prop 2.2(b) on members), c003/c091 (peak need vs net debit definitions), c086/c094 (expected cost vs its rounding), "
        "c080/c100 (Prop 2.1 vs Prop 2.4, same value under different laws). No card repeats another."),
    row("cards-coverage", "2.7-coverage", "L01-L05 Definitions, Propositions, Remarks, worked Examples, Problems, key-results rows, Misconceptions vs cards.json",
        f"Traced against {OUT}/L01.txt..L05.txt (full read of each lesson, line-numbered). L01: Def 1.1 c001, Def 1.2 c002, "
        "Def 2.1 c003 and c091, Prop 2.2 c004, Prop 2.3 c005, Prop 2.4 c006, P2 c007, Example 2.6 c008 and c101, Remark 2.7 c009, "
        "Remark 2.5 c015, Misconceptions c013 c014 c015, key rows c010 c011 c012 c014. L02: Def 1.1 c016, Def 1.2 c017, "
        "Assumption 1.3 c018, Def 2.1 c019 c020 c021 c095, Prop 2.2(a)-(d) c022-c025, Prop 2.3 c026, Example 2.4 c027 c028 c033, "
        "R1 c029 c102, P3 c030 c103, Lab D c031 c092, Duffie c032, Misconceptions c033 c034 c035 c099. L03: Def 1.1 c036-c038 "
        "and c058, Prop 1.2 c040, Prop 1.3 c041 c104, Example 1.5 c043, Example 1.6 c044, Def 2.1 c039 and c105, Remark 2.2 c055, "
        "Prop 2.3 c046, Cor 2.4 c047, Example 2.5 c048 c056, Remark 1.4 c057, Lab B c049 c050, layer and margin definitions "
        "c051-c054 c096, Misconceptions c055-c058. L04: Def 1.1 c059, reserve/claim/redemption c060-c062, Def 1.2 c063, "
        "Def 2.1 c064 c065 c097, Def 3.1 c066, Prop 2.2 c067, 2.4 c068, 2.5 c069, 2.6 c076, 2.7 c071, Remark 2.8 c072 c075, "
        "Remark 4.1 c073 c074, claims c093, Misconceptions c074 c075 c076. L05: Def 1.1 c077, Def 1.2 c078, Def 2.1 c079, "
        "Prop 2.1 c080, 2.2 c081, 2.4 c100, 2.5 c083, 2.6 c084, Example 2.7 c089, Example 2.8 c086 c094, Lab D c087, "
        "Assumption 1.3 joint law c098, Misconceptions c088 c089 c090. Every lesson contributes cards; "
        "no Definition, Proposition, Problem result or Misconception in L01-L05 lacks a card. Remark 2.6 (L03) and "
        "Remark 3.2 (L04) carry no card; BUILDER_RULES section 7 does not list remarks."),
    row("cards-numbers", "2.2-numbers-on-cards", "cards.json fronts and backs vs their lessons; every value recomputed",
        f"python -I {S}/card_numbers.py course/modules/BK/BK4/cards.json {OUT} -> {OUT}/card_numbers.out: total misses 0 "
        "(each number token in card text appears in its own lesson text; a negative test with 999999 and 4/7 reports misses, "
        "so the script is not vacuous). python -I "f"{S}/rederive.py -> {OUT}/rederive.out: 87 checks, 87 PASS, computed "
        "from the definitions with Fraction and integer arithmetic (not from the lab code): Example 2.6 needs 100 and debit 50, "
        "running sums 0,-100,-100,-50; Remark 2.7 need 50; netted 50 and 7826 bp; 7222 and 7826 bp (M1, M2); rho=21/20 at x=1/2 "
        "gives 11/10 = 11000 bp; rho=19/20 at x=1/2 gives 9/10 = 9000 bp, not rho/2 = 19/40; Remark 2.8 x=1/7 gives 113/120 "
        "and 9416 bp; threshold 1/(1-1/20)=20/19; Example 1.5 table rows 80-300 and conservation; Example 1.6 Z=1 and Z=2; "
        "k=198 (S=200, 9900), k=200 (9975), k=399 at S=400; E2 survivor shares 312,381,164 from residual 857 and total 1714; "
        "E[C]=4375/2 and 2188 rounded half up; closed form 1875 (equal delays 2); variances 57421875/4 and 133984375/4, "
        "difference 19140625 = 2 kappa^2 p(1-p) sum l_i l_j; P(at least one) 169/512 and 3p=3/8; P(C=0) 343/512 and 7/8; "
        "R2 bounds 5/8 and 7/8."),
    row("cards-xrefs", "2.7-xrefs", "cards.json cross-references to lesson labels and other lessons",
        f"python -I {S}/card_structure.py ... -> {OUT}/card_structure.out: label cross-reference misses 0 (every Definition, "
        "Proposition, Example, Remark, Problem, Corollary, Assumption and Section named on a card appears in that card's own "
        "lesson text; no label found only in another lesson). Forward pointer c035 to Lesson 3 Definition 1.1 (the CCP default "
        "waterfall) checked at out/L03.txt line 48."),
    row("cards-lab-outputs", "2.5-labs-as-cited-by-cards", "cards c010 c011 c012 c014 c031 c049 c050 c086 c087 c090 c092 c094 vs lab output",
        f"Each twin run as python -I -W error tests/labs/BK4/lab-BK4-Lnn-1.py: exit 0, stderr 0 bytes (L01-L05). "
        f"python -I {S}/lab_compare.py <checkout> {OUT} -> {OUT}/lab_compare.out: page code equals twin for all five labs; "
        "expected block equals twin stdout for all five. run_labs --unit BK4: PASS (8/8) (out/run_labs.out). Card values read "
        "from out/lab-BK4-L0n-1.stdout: c010 RTGS need 1533900 = DNS debit (L01 Part B); c011 112500; c012 1533900 of 2841600 "
        "(Part C); c014 Bank A net +379800, debit 0, need 112500; c031 5093600 (L02 Part D); c092 7596300 (Part B); c049 2961 "
        "and cover 9900 bp, brute force agrees; c050 2992 and cover 10000 bp, brute force agrees (L03 Part B); c086 and c094 "
        "4375/2 and 2188 (L05 Part B); c090 1875 (Part C); c087 133984375/4 vs 57421875/4 (Part D). Each matches."),
    row("cards-grades-vs-keyresults", "2.3-grades", "cards.json grade vs each lesson key-results row and BLUEPRINT section 3",
        "Every card grade compared to the lesson's key-results table (L01-L05 Result/Claim tables, out/L0n.txt) and to the grade "
        "rule of BLUEPRINT section 3. T rows (proved on the page) carry T cards: L01 Props 2.2-2.4, P2, Example 2.6; L02 Props "
        "2.2-2.3, Example 2.4, R1, P3; L03 Props 1.2, 1.3, Remark 1.4, Remark 2.2, Prop 2.3, Cor 2.4; L04 Props 2.2, 2.4-2.7, "
        "Remark 4.1; L05 Props 2.1, 2.2, 2.4-2.6, Example 2.7. C rows (read off a SIMULATED lab) carry C cards: L01 c010 c011 "
        "c012 c014; L02 c031 c032 c092; L03 c049 c050; L05 c086 c087 c094. Two cards are T though the L03 key-results row "
        "for the fixture is C: c043 and c044 are T because Example 1.5 (L03 line 82 onward: floor(20*40/100)=8, floor(20*60/100)=12) "
        "and Example 1.6 (Z=2, one cent each) are arithmetic shown on the page, which BLUEPRINT section 3 grades T. The "
        "L03 key-results row (C, lab source) covers the whole Lab 1 table of Example 1.5, of which only the L=200 and Z=2 rows "
        "are hand-derived, so the row stays C and is not in conflict. Plan section 2.2 (finite enumeration is C) is applied to "
        "the enumerations of Lab 1 (c086, c087) and to the printed rounding (c094), which is the lab's printed line "
        "'closed form rounded half up to the cent: 2188 cents'."),
    row("cards-hypotheses", "2.4-hypotheses", "cards.json fronts that say 'Assuming ...' vs the hypotheses of the named result",
        "The hypothesis lists of the cited results are on the lesson pages: L01 Prop 2.2 'Under Assumption 1.3 (A1 and A2)' "
        f"(out/L01.txt:68); L02 Prop 2.2 'Under Assumption 1.3 (A1 to A3)' (out/L02.txt:70); L03 Prop 1.2/1.3 'Assuming A1 and A2' "
        "(out/L03.txt:60,70), Prop 2.3 'Assuming A3 and A4' (out/L03.txt:234-236); L04 Props 2.2, 2.4-2.7 'Assuming Assumptions 1 to 3' "
        "(out/L04.txt:74-114); L05 Prop 2.1 'A1 and A2' (out/L05.txt:68-70), Prop 2.2 'A1, A2 and A3' (out/L05.txt:76-78), "
        "Prop 2.4 'A1, A2 and A4' (out/L05.txt:92-94), Prop 2.5 'A1 and A2; A3 for Var_3 and A4 for Var_4; 0<p<1; kappa>0' "
        "(out/L05.txt:100-102), Prop 2.6 'A1 and A2; A3 and A4; 0<p<1; l_i>=1; kappa>=1' (out/L05.txt:112-114). Cards c083 and "
        "c084 state 'A1, A2, 0 < p < 1 and kappa > 0' and 'A1, A2, 0 < p < 1, l_i >= 1 and kappa >= 1' with the finite space; "
        "c080, c081, c088, c100 carry A2 as well. c004 carries 'A1 fixed payments; A2 no intraday credit'. Cards with no "
        "hypothesis (c001-c003, definitions; c071 real-number fact; c030 and c103 cycle claims) state no result that needs one."),
    row("cards-attribution-duffie", "2.1-attribution", "BK4-c032 vs references/references.json duffie2011central",
        f"Registry record duffie2011central (references/references.json, entries): doi 10.1093/rapstu/rar001, title 'Does a Central "
        "Clearing Counterparty Reduce Counterparty Risk?', authors Duffie, Zhu, Review of Asset Pricing Studies 1(1) 74-95, 2011, "
        "verified_by crossref. Live re-check with plain curl: curl -sS https://api.crossref.org/works/10.1093/rapstu/rar001 -> "
        "HTTP 200; message.title equals the registry title; container 'Review of Asset Pricing Studies'; volume 1, issue 1, pages "
        "74-95; published 2011-07-18; authors Darrell Duffie, Haoxiang Zhu (out/crossref_duffie.json is not stored; the "
        "fetch was run and its result recorded here). Crossref carries no abstract, so the card's claim is limited to the question "
        "(the title), exactly as the card and the lesson (L02 section 4) state it. c032 grade C with the paper-level basis."),
    row("cards-banned-and-process-words", "2.9-banned-phrases", "cards.json and L01-L05 text",
        "grep -i (case-insensitive) over cards.json and out/L01.txt..out/L05.txt for TODO, TBD, lorem, for brevity, details omitted, "
        "beyond the scope, important to note, studies show, experts agree, well known, obviously, clearly, can be shown, left as an "
        "exercise, you can add, roughly, historically, ellipsis: 0 hits. Process words (builder, verifi, ledger as a process, draft, "
        "fixer, reviewer, architect, round, ruling, agent): 0 hits in cards; the only 'ledger' hits are the domain sense of a "
        "stablecoin record (c059, c066 definitions)."),
    row("cards-notation", "2.9-notation", "cards.json and BK4 math vs notation/notation.json",
        "notation/notation.json lists 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and macros including \\E, \\Prob, "
        "\\Var, \\indic. BK4 math segments (extracted from the 5 lesson pages by python -I "f"{S}/extract_text.py) contain none of "
        "the registered symbols as single letters (the only 'N' match is inside \\mathrm{Net}); the custom macros used (\\E, \\Prob, \\Var, \\Cov, \\indic) are registered; "
        "the other TeX commands (\\rho, \\kappa, \\Omega, \\mathcal and similar) are standard symbols, not registry macros. Per-lesson local letters (S, m, mu, D, C, K, A, G, L, M, Z, t, k) are defined in their lesson "
        "(notation.json 'about': conventionally local letters are defined where used). Cards use the same symbols as their lesson."),
    row("cards-dag", "2.9-dag", "cards.json concept references vs the BK4 prerequisite closure",
        f"check_dag.py --all: BK4 PASS (out/check_dag_all.out). Card-level: RTGS and DNS are defined on c001 (L01 Def 1.1) before "
        "any card uses them; CCP on c017 (L02 Def 1.2) before c026 and c034; the waterfall layers are defined on c036 (L03 Def 1.1) "
        "before c040-c058; coverage on c064 (L04 Def 2.1) before c067-c076; expected cost on c079 (L05 Def 2.1) before c080-c090. "
        "c035 points forward to Lesson 3 Definition 1.1 by name, as the lesson's own section 4 does; it uses no undefined concept."),
    row("cards-pages-gate", "2.9-pages-gate", "BK4 pages and cards via the repository gates",
        f"check_pages.py --unit BK4: PASS ({OUT}/check_pages_bk4.out). check_dag.py --all: exit 0, BK4 PASS. run_labs.py --unit BK4: "
        "PASS 8/8 (out/run_labs.out). page_smoke.py --unit BK4 --pages L01 L02 L03 L04 L05 (labs and figure sweep run, no skip): "
        "PASS for all five pages (out/page_smoke_labs.out). pytest tests/test_page_checks.py tests/test_build_site.py "
        "tests/test_curriculum.py: all pass. Not run: ruff, mypy, build_site --check, fetch_data --check, run_graders and "
        "mutate_graders, because no Python file outside tools/ and tests/labs/BK4 is in this slice and the 0dee921a..c93dd526 delta "
        "touches no Python file (git diff --stat)."),
    row("cards-c001-c010", "2.7-sample", "BK4-c001 to BK4-c010 (L01)",
        "Each card read in full against out/L01.txt: c001 Def 1.1 (out/L01.txt:44); c002 Def 1.2 and the T+1 non-statement (:48, :279); "
        "c003 Def 2.1 (:64); c004 Prop 2.2 (:68); c005 Prop 2.3 (:76); c006 Prop 2.4 and Example 2.6 strictness (:84, :88); c007 P2 "
        "(:339-343); c008 Example 2.6 (:96); c009 Remark 2.7 (:100); c010 Lab Part B and the equality (:237-245, :255). Numbers in "
        "rederive.out. Each matches the lesson."),
    row("cards-c011-c020", "2.7-sample", "BK4-c011 to BK4-c020 (L01 and L02)",
        "c011 112500 (out/L01.txt:237); c012 1533900 of 2841600, 0.5398 derived on the page (out/L01.txt:255, :376-377); c013 A2 and "
        "Def 2.1 (:64, :56); c014 Bank A net +379800 and need 112500 (:237, :291); c015 Remark 2.5 (:90-92); c016 Def 1.1 novation "
        "(out/L02.txt:44); c017 Def 1.2 CCP (:48); c018 Assumption 1.3 G (:60); c019 Def 2.1 n_i (:66); c020 A (:66). Each matches."),
    row("cards-c021-c030", "2.7-sample", "BK4-c021 to BK4-c030 (L02)",
        "c021 floor bp definition (out/L02.txt:66); c022-c025 Prop 2.2(a)-(d) (:82-88); c026 Prop 2.3 (:92-96); c027 Example 2.4 "
        "netted 50 (:100); c028 7826 bp (:100, rederive.out); c029 R1 range 0-10000 (:370); c030 P3 cycle zero (:334). Each matches."),
    row("cards-c031-c040", "2.7-sample", "BK4-c031 to BK4-c040 (L02 and L03)",
        "c031 5093600 (out/L02.txt:242 and lab stdout); c032 Duffie (see cards-attribution-duffie; out/L02.txt:254, :264); c033 Example 2.4 "
        "50 against 230 (:100); c034 Section 4 and Prop 2.2(c) (:252); c035 Prop 2.2(b) and Lesson 3 pointer (:278); c036 Def 1.1 "
        "waterfall layers (out/L03.txt:52-56); c037 Z >= D case (:58); c038 Z < D shares and leftover (:58); c039 Def 2.1 cover "
        "(:222); c040 Prop 1.2 conservation (:62-68). Each matches."),
    row("cards-c041-c050", "2.7-sample", "BK4-c041 to BK4-c050 (L03)",
        "c041 Prop 1.3 bounds (out/L03.txt:72-76); c043 Example 1.5 8 and 12 cents, residual 20 (:84); c044 Example 1.6 (:214); c046 "
        "Prop 2.3 L_(k) with k=ceil(tS/10000) (:236-242); c047 Cor 2.4 (:254); c048 Example 2.5 k=198 (:262); c049 and c050 Lab Part B "
        "2961, 2992, covers 9900 and 10000 (lab stdout lines 'target 9900 bps' and 'target 9975 bps'). Each matches."),
    row("cards-c051-c060", "2.7-sample", "BK4-c051 to BK4-c060 (L03)",
        "c051 initial margin, c052 default fund, c053 CCP capital, c054 surviving member: out/L03.txt:40 (definitions in section 1). "
        "c055 Remark 2.2 and Def 2.1 (:224-226); c056 Example 2.5 and Def 2.1 (:262, :509); c057 Remark 1.4 (:80); c058 Def 1.1 "
        "shares by DF (:58). Each matches."),
    row("cards-c061-c070", "2.7-sample", "BK4-c061 to BK4-c070 (L04)",
        "c061 claim, c062 redemption, c060 reserve (out/L04.txt:40); c063 Def 1.2 rho (:48-50); c064 Def 2.1 theta and x (:72); c065 bp "
        "floor (:72); c066 Def 3.1 (:326); c067 Prop 2.2 (:76-84); c068 Prop 2.4 (:92-96); c069 Prop 2.5 (:100-104). Each matches; "
        "c070 is a gap, not a card."),
    row("cards-c071-c080", "2.7-sample", "BK4-c071 to BK4-c080 (L04 and L05)",
        "c071 Prop 2.7 (out/L04.txt:116-120); c072 Remark 2.8 rho=21/20 x=1/2 gives 11000 bp (:124); c073 Remark 4.1 threshold 20/19 "
        "(:336); c074 Prop 2.4 and Remark 4.1 with rho=1 (:352); c075 Prop 2.2 and Remark 2.8 (:124, :356); c076 Prop 2.6 (:108-112); "
        "c077 Def 1.1 operational risk (out/L05.txt:44); c078 Def 1.2 (:48); c079 Def 2.1 (:66); c080 Prop 2.1 (:70-74). Each matches; "
        "c082 is a gap."),
    row("cards-c081-c090", "2.7-sample", "BK4-c081 to BK4-c090 (L05)",
        "c081 Prop 2.2 (out/L05.txt:78-86); c083 Prop 2.5 difference formula, rederived: 19140625 (:100-110); c084 Prop 2.6 (:112-118); "
        "c085 is a gap; c086 Example 2.8 and Lab Part B 4375/2 (:126, lab stdout); c087 Lab Part D variances (lab stdout); c088 "
        "Props 2.4 and 2.5 and misconception (:317-319); c089 Example 2.7, 169/512 and 3p=3/8 (:122); c090 Prop 2.1 with l=2 gives 1875 "
        "(:327). Each matches."),
    row("cards-c091-c094", "2.7-sample", "BK4-c091 to BK4-c094 (L01, L02, L04, L05)",
        "c091 Def 2.1 net debit (out/L01.txt:64); c092 gross notional 7596300 (lab stdout Part B; equals the four receivables 314500 + "
        "2067800 + 3340300 + 1873700); c093 claims outstanding (out/L04.txt:40); c094 2188 by the printed rounding rule (out/L05.txt:126; "
        "lab stdout 'closed form rounded half up'). Each matches."),
    row("cards-c095-c098", "2.7-sample", "BK4-c095 to BK4-c098 (L02, L03, L04, L05)",
        "c095 Def 2.1 multilateral netting (out/L02.txt:64); c096 variation margin excluded from the model (out/L03.txt:489-497, "
        "variation margin definition at :497); c097 admissibility, Def 2.1 and Remark 2.3 (out/L04.txt:70, :86-88); c098 joint law, "
        "Assumption 1.3 (out/L05.txt:52). Each matches."),
    row("cards-c099", "2.7-sample", "BK4-c099 (L02)",
        "Prop 2.2(b) with Def 2.1: A = 0 iff every n_i <= 0, and sum n_i = 0 then forces every n_i = 0 (out/L02.txt:270, :278; "
        "re-derived by hand). Matches."),
    row("cards-c100-c101", "2.7-sample", "BK4-c100 and BK4-c101 (L05 and L01)",
        "c100 Prop 2.4 under A4 gives the same E[C] (out/L05.txt:92-98); c101 Example 2.6 debit 50 from net position -50 (out/L01.txt:94, "
        "rederive.out 'c101 Debit_A'). Each matches."),
    row("cards-c102-c104", "2.7-sample", "BK4-c102, BK4-c103, BK4-c104 (L02 and L03)",
        "c102 R1 reduction equals 10000 iff A = 0 (out/L02.txt:366-370); c103 P3 cycle reduction 10000 bp (:334); c104 Prop 1.3 survivor "
        "bound x_i <= DF_i and x_i + 1 <= DF_i for leftover receivers (out/L03.txt:72-76). Each matches."),
    row("cards-c105", "2.7-sample", "BK4-c105 (L03, new in the round-9 delta)",
        "c105 scenario set: Definition 2.1 (out/L03.txt:220-222): S losses L_1..L_S, non-negative integers in cents, S >= 1 "
        "(the card's words 'a scenario is one loss in a fixed set' match the lesson intro, out/L03.txt:36). Matches; no grade, "
        "definition-level card as the builder rules require."),
    row("cards-scope-claims", "2.4-scope-words", "every card containing only, all, always, every, any, same, exactly, never, whatever, each",
        "Scope words listed by a python -I scan of cards.json (46 cards). Each use is backed by a computation or an explicit hypothesis: "
        "'never changes the net debit' (c015) by Remark 2.5 (order does not enter Net_i); 'every' in c003, c006, c040 are the definition's "
        "quantifiers; 'only if' in c007, c026, c046, c083, c099 are the proved iff statements; 'exactly' in c022, c048, c065, c102 "
        "are computed (tS/10000 = 198 exactly, floor(10000 * 180/230)); c074 'whatever the reserve assets are worth' quotes the "
        "misconception heading, and the card's answer is conditional on Assumption 4 with h > 0; c089 'neither equals 3p' holds "
        "for 0 < p < 1 by p^2(3-p) > 0; c049 and c050 'same' are the brute-force agreement printed by the lab."),
    row("cards-refs-live", "2.1-registry", "references/references.json entries used by BK4 (duffie2011central, bisndbasel)",
        "python tools/verify_refs.py --unit BK4 (live): 'live re-verification of BK4: 2 of 560 entries, 0 problems' "
        "(out/verify_refs_live.out). The offline run with --unit is rejected by the tool (live only), so the live run is the one that counts."),
    row("cards-delta-round7", "2.7-delta", "round-7 delta (c035 back, c043 and c044 front, c074 front, c075 back)",
        "Superseded by the full re-read this round: every card was read again (no carry). c043 and c044 now have T grades and "
        "hand-derivation bases (see cards-grades-vs-keyresults); c035, c074 and c075 re-checked against L01 Section 2 and L04 "
        "Remark 4.1 and Remark 2.8 and pass."),
    row("cards-delta-round8", "2.7-delta", "round-8 delta (0dee921a..c93dd526 for cards.json)",
        "Changed cards: c011 back (now '112500 cents.'), c013 back (now matches L01 misconception text), c043 and c044 (grade T, "
        "hand basis), c072 front and back (now rho=21/20, 11/10, 11000 bp, matching L04 Remark 2.8), c105 (new). Each re-read "
        "against its lesson and passes."),
    row("cards-delta-round9", "2.7-delta", "round-9 delta: git diff 0dee921a c93dd526 -- course/modules/BK/BK4 (L01, L02, L03, index, project)",
        "Lesson changes that cards touch: L01 misconception 'Net settlement removes the need for liquidity' (now 'Net settlement can "
        "lower the funds ... does not remove the settlement funding of a bank that is a net payer') vs c013 (agrees); L01 E2 wording "
        "(no card); L02 E2 wording (no card); L03 intro (now 'simulated losses ... in a fixed set'), agrees with c105; L03 quiz "
        "item 'member 1 pays 1 cent' vs c044 (agrees); index hub and project changes are owned by the hub and project slices. "
        "The L05 pages and L04 page are byte-identical in the delta."),
]

fragment = {
    "unit": "BK4",
    "slice": "BK4-d",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-d (slice d: course/modules/BK/BK4/cards.json against the current L01-L05 lessons), round 9; did not build BK4 and shares no context with its builders",
    "pin": "c93dd526 (HEAD, detached)",
    "base": "0dee921a (round-8 pin). cards.json and L01/L02/L03/index/project changed in the delta (see cards-delta-round9); every card re-read this round, no row carried forward",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-BK4-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-BK4-d-r9 (dumps copied to ledgers/BK4/scripts/BK4-d-r9/out/)",
    "verified_at": "2026-11-05T04:05:49+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d is cards.json only. No grader, so no mutation testing; ledgers/BK4/mutants/ is untouched and no mutant is listed. "
        "Round-8 non-PASS row cards-grades-vs-keyresults is PASS now: c043 and c044 are T and their basis is the arithmetic on the page. "
        "Grade-policy note for the architect (not a FAIL): plan section 2.2 grades finite enumerations C; the L03 key-results row for the "
        "fixture stays C because it covers the lab-printed table, while c043 and c044 are hand arithmetic (T). If the architect rules "
        "that a fixed-fixture example is C naming the lab, both cards and the L03 hand-derivation need the same ruling. "
        "Not checked: lesson prose outside what the cards cite (owned by the lesson slices); project.html and the grader (project slice); "
        "ruff, mypy, build_site --check, fetch_data --check, run_graders, mutate_graders (no Python in the slice changed); the 2025-2026 "
        "literature for freshness (the only cited work is Duffie and Zhu 2011, question-level, no finding stated); the Basel III and SEC "
        "T+1 sources (not cited by cards; the T+1 rule is named and not stated, consistent with the plan)."
    ),
    "summary": (
        "BK4-d round 9: PASS. 100 cards read in full against L01-L05; 87 independent re-derivations, 0 fail; 5 lab twins exit 0 "
        "with empty stderr and match the page code and expected output; 0 number misses; 0 label misses; duplicate scan clean; "
        "Duffie attribution confirmed by live Crossref; verify_refs live 2 of 560, 0 problems; check_pages, check_dag, run_labs 8/8, "
        "page_smoke (with labs) PASS on L01-L05."
    ),
}

if __name__ == "__main__":
    with open("ledgers/BK4/BK4-d.json", "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote ledgers/BK4/BK4-d.json rows", len(rows))
