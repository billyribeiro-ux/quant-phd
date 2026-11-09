"""Builds ledgers/E3/E3-f.json (round 12). Every row was re-verified this round; evidence cites r12 scripts or lesson locators."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1])
R = "ledgers/E3/scripts/E3-f-r12/"
ev_cards = (
    "Round 12: card read in full and checked against the current lesson text at {loc}; statement, hypotheses, "
    "grade and every number agree (numbers re-derived in {rd}; cards_scan.out: no number absent from its lesson)."
)
RD = R + "rederive.out"

# id -> (lesson locator, extra note)
cards = {
    "E3-c001": ("L01.html:59 (Definition 1.1)", ""),
    "E3-c002": ("L01.html:64 (Definition 1.2)", ""),
    "E3-c003": ("L01.html:69 (Definition 1.3)", ""),
    "E3-c004": ("L01.html:74 (Assumption A1)", ""),
    "E3-c005": ("L01.html:86 (Definition 2.1)", "The card and the lesson both write the mixture weight as alpha; the notation clash is row E3f-notation-alpha, not a card defect."),
    "E3-c006": ("L01.html:143 (Definition 3.2)", ""),
    "E3-c007": ("L01.html:91 (Proposition 2.2)", ""),
    "E3-c008": ("L01.html:104-108 (Proposition 2.3)", ""),
    "E3-c009": ("L01.html:126 (Remark 2.4)", ""),
    "E3-c010": ("L01.html:133 (Proposition 3.1)", ""),
    "E3-c011": ("L01.html:148 (Proposition 3.3)", ""),
    "E3-c012": ("L01.html:396-398 (Problem P2)", ""),
    "E3-c013": ("L01.html:439-441 (Problem R1)", ""),
    "E3-c014": ("L01.html:79 (Example 1.4) and L01.html:343 (misconception 1)", "u(EX)=150^2=22500, E u(X)=45000 (rederive.out)."),
    "E3-c015": ("L01.html:347 (misconception 2)", ""),
    "E3-c016": ("L01.html:302-305 (Lab 1 Part A expected block)", "Values equal the lab output (run_labs and lab_twin_check.out)."),
    "E3-c017": ("L01.html:306-313 (Lab 1 Part B expected block)", "Six True lines (run_labs)."),
    "E3-c018": ("L02.html:74 (Assumption A2)", ""),
    "E3-c019": ("L02.html:89-94 (Proposition 1.1)", ""),
    "E3-c020": ("L02.html:99 (Definition 1.2)", ""),
    "E3-c021": ("L02.html:99 (Definition 1.2, last sentences)", ""),
    "E3-c022": ("L02.html:103-124 (Proposition 1.3(a) and proof)", ""),
    "E3-c023": ("L02.html:106 and L02.html:126 (Proposition 1.3(b))", ""),
    "E3-c024": ("L02.html:144 (Definition 2.1)", ""),
    "E3-c025": ("L02.html:149 and L02.html:154 (Proposition 2.2)", ""),
    "E3-c026": ("L02.html:159 (Example 2.3)", "r_A(100)=0.005, r_R=0.5 (rederive.out)."),
    "E3-c027": ("L02.html:173 (Proposition 3.1)", ""),
    "E3-c028": ("L02.html:204 (Remark 3.2)", ""),
    "E3-c029": ("L02.html:399 (misconception 1)", "1800/2=900; 4.5; 5.065835 (rederive.out)."),
    "E3-c030": ("L02.html:403 (misconception 2) and L02.html:159", ""),
    "E3-c031": ("L02.html:407 (misconception 3)", ""),
    "E3-c032": ("L02.html:367 (Lab 1 Part A expected block)", "Matches run_labs output; ce_cents 9493, premium 507 (rederive.out)."),
    "E3-c033": ("L02.html:370-375 (Lab 1 Part B expected block)", "Ratios 5.065835 and 4.500046 re-derived (rederive.out)."),
    "E3-c034": ("L02.html:387 (section 4) and L02.html:479 (E2)", "0.565835/5.065835 = 11.1696 percent, printed 11.17 (rederive.out)."),
    "E3-c035": ("L02.html:377-380 (Lab 1 Part C expected block)", ""),
    "E3-c159": ("L02.html:131 (Remark 1.4)", ""),
    "E3-c160": ("L03.html:321 and L03.html:273 (gamma = 1 +/- 1e-6 check)", ""),
    "E3-c161": ("L02.html:381 and L02.html:502-504 (Lab 1 Part B; problem R2)", ""),
    "E3-c162": ("L02.html:131 (Remark 1.4)", ""),
    "E3-c167": ("L04.html:85 (Definition 1.4)", ""),
    "E3-c168": ("L03.html:184 (Remark 2.8)", "Derivation |R(kv)-kR(v)| <= 1/2 + k/2 checked; (k+1)/2 = 5.5 at k=10 (rederive.out)."),
    "E3-c171": ("L03.html:324-325 and L03.html:326 (homogeneity and cents-bound lines)", ""),
    "E3-c173": ("L01.html:351 (misconception 3)", ""),
    "E3-c174": ("L02.html:168 (Assumption A5)", ""),
    "E3-c175": ("L03.html:59 (Assumption A2) and course/modules/M/M1/L03.html (Lesson 3 does not derive the limit: no lim in the lesson)", "M1 L03 defines e as e^1 (text read)."),
    "E3-c177": ("L03.html:95 (Proposition 1.4) and L03.html:349 (misconception 2)", ""),
    "E3-c178": ("L03.html:112 (Definition 1.6)", "E3-c178 appears once in cards.json (cards_scan.out: 178 unique ids)."),
    "E3-c180": ("L03.html:159 (Example 2.5)", "exp(0.5 ln1000 + 0.5 ln4000) = 2000 (rederive.out)."),
    "E3-c036": ("L03.html:73 (Definition 1.1)", ""),
    "E3-c037": ("L03.html:78 and L03.html:83 (Proposition 1.2 and proof)", "Cites M1 L03 Prop 1.4 and 1.6(b) and A2: verified in course/modules/M/M1/L03.html:60 (A2 addition), 61 (A3 inverse), 92 (Prop 1.4), 112 (Prop 1.6)."),
    "E3-c038": ("L03.html:89 (Definition 1.3)", ""),
    "E3-c039": ("L03.html:90 (Definition 1.3, normalization sentence)", ""),
    "E3-c040": ("L03.html:95 and L03.html:101-102 (Proposition 1.4 and proof)", ""),
    "E3-c041": ("L03.html:117 and L03.html:122 (Proposition 1.7 and proof)", ""),
    "E3-c043": ("L03.html:129 and L03.html:134 (Theorem 2.1 and proof)", ""),
    "E3-c044": ("L03.html:139 (Remark 2.2)", ""),
    "E3-c045": ("L03.html:144 (Definition 2.3)", ""),
    "E3-c046": ("L03.html:149 and L03.html:154 (Proposition 2.4 and proof)", ""),
    "E3-c047": ("L03.html:159 (Example 2.5)", "M = 1/1600, CE = 1600 (rederive.out)."),
    "E3-c048": ("L03.html:164 (Proposition 2.6)", ""),
    "E3-c049": ("L03.html:173-175 (Proposition 2.7) and L03.html:178-180 (proof)", "Round-11 FAIL fixed: the back now uses phi and eta, the letters of L03.html:173-175."),
    "E3-c050": ("L03.html:184 (Remark 2.8)", ""),
    "E3-c051": ("L03.html:345 (misconception 1)", ""),
    "E3-c052": ("L03.html:107 (Example 1.5)", ""),
    "E3-c053": ("L03.html:455-457 (Problem R3)", ""),
    "E3-c054": ("L03.html:309-314 (Lab 1 expected block)", "Values equal the lab output (run_labs)."),
    "E3-c055": ("L03.html:425 (Problem E2) and L03.html:149", "80000/9 and 9/80000 (rederive.out)."),
    "E3-c056": ("L04.html:65 (Definition 1.1)", ""),
    "E3-c057": ("L04.html:70 (Lemma 1.2)", ""),
    "E3-c058": ("L04.html:80 (Definition 1.3)", ""),
    "E3-c059": ("L04.html:85 (Definition 1.4)", ""),
    "E3-c060": ("L04.html:90 (Theorem 1.5)", ""),
    "E3-c061": ("L04.html:103 (Lemma 1.6)", ""),
    "E3-c062": ("L04.html:118 (Proposition 1.8)", ""),
    "E3-c063": ("L04.html:130 (Definition 2.1)", ""),
    "E3-c064": ("L04.html:135 (Lemma 2.2)", ""),
    "E3-c065": ("L04.html:145 (Theorem 2.3)", ""),
    "E3-c066": ("L04.html:160 (Remark 2.4)", ""),
    "E3-c067": ("L04.html:166 (Example 2.5)", "I_X = 0, 0, 500, 1000, 2000 (rederive.out)."),
    "E3-c068": ("L04.html:166-168 (Example 2.5)", ""),
    "E3-c070": ("L04.html:113 (Example 1.7)", ""),
    "E3-c071": ("L04.html:614-616 (Problem R3)", ""),
    "E3-c072": ("L04.html:173 (Example 2.6) and L04.html:504 (misconception 1)", ""),
    "E3-c073": ("L04.html:508 (misconception 2) and L04.html:472, L04.html:475 (Lab 1 pairs 16 and 19)", ""),
    "E3-c074": ("L04.html:512 (misconception 3)", ""),
    "E3-c075": ("L04.html:480 (Lab 1 FOSD counts)", "3, 10, 1, 10 sum to 24 (Problem E2 arithmetic)."),
    "E3-c076": ("L04.html:483-484 (Lab 1 SOSD counts)", "3, 2, 1, 2 sum to 8."),
    "E3-c077": ("L04.html:492-495 (section 3 limits)", ""),
    "E3-c181": ("L04.html:167 (Example 2.5)", "I_Y = 0, 250, 500, 1250, 2000 (rederive.out)."),
    "E3-c183": ("L04.html:173 (Example 2.6)", "I_Y(t)=(t-3000)^+ <= I_X(t) at 1000..5000 (rederive.out). The card states a result but has no grade field; see row E3f-E3-c183."),
}

rows = []
for cid, (loc, note) in cards.items():
    n = int(cid[-3:])
    rd = RD
    evidence = ev_cards.format(loc=loc, rd=rd)
    if note:
        evidence += " " + note
    location = f"course/modules/E/E3/cards.json ({cid}); {loc}"
    row = {"id": f"E3f-{cid}", "check": "2.7-cards", "location": location, "status": "PASS", "evidence": evidence}
    rows.append(row)

# the card rows with a fix
for r in rows:
    if r["id"] == "E3f-E3-c183":
        r["status"] = "FAIL"
        r["evidence"] = (
            "Round 12: cards.json E3-c183 (lesson L04, Example 2.6) states that Y dominates X in the second order and that "
            "neither dominates in the first order. The claim is right (L04.html:173; rederive.out: I_Y(t)=(t-3000)^+ <= I_X(t) at "
            "every support point 1000..5000). But the card has no grade field, while the key-results row it mirrors "
            "(L04.html:632, Named pairs of Examples 1.7, 2.5 and 2.6) is graded T. BUILDER/Architect ruling 13 (plans/FINAL-ARCHITECT-RULINGS.md item 13): "
            "a card and the key-results row it mirrors carry the same grade and basis."
        )
        r["fix"] = (
            'Add "grade": "T" to E3-c183 in course/modules/E/E3/cards.json (its basis is Example 2.6, derived by hand; '
            "no basis field is needed for a T card). Do not change the wording."
        )

# c049 fixed row (kept PASS, evidence updated)
for r in rows:
    if r["id"] == "E3f-E3-c049":
        r["evidence"] = (
            "Round 12: round-11 FAIL is resolved. cards.json E3-c049 back reads 'for phi > 0 and real eta, the certainty equivalent "
            "under phi u + eta equals the one under u (Proposition 2.7)', which uses the letters of L03.html:173-175 and the proof "
            "L03.html:178-180. No letter a is used with a new meaning. Checked against the current lesson text."
        )

extra = [
    {
        "id": "E3f-lesson-numbers-L01", "check": "2.2-numbers",
        "location": "course/modules/E/E3/L01.html (Example 1.4, Example 3.4, Misconceptions, M1-M3, E1-E3, R1-R3, quiz, Lab 1 prose)",
        "status": "PASS",
        "evidence": "Round 12: every number re-derived with Fraction in " + RD + " (L01 EX1.4 150 and 45000; MisC1 22500; EX3.4 37500; M1 59 and 4030 and 3481; M2 175; M3 65 and 95; E1 7500; E2 40000; E3 5/6; q7 5/12; Lab A/B/C quadratic 45000, 21250, 37500) and matched to lesson text. Changed quiz q4 explanation (L01.html:511) read: no number changed.",
    },
    {
        "id": "E3f-lesson-numbers-L02", "check": "2.2-numbers",
        "location": "course/modules/E/E3/L02.html (Example 1.5, Example 2.3, Section 3 text, misconceptions, M1-R3, E1-E3, quiz, key results)",
        "status": "PASS",
        "evidence": "Round 12: " + RD + ": E sqrt(W) = 9.7434164902..., CE = 94.9341649..., premium 5.0658350975 CU; cents 9493.4165 -> 9493 and 506.5835 -> 507 (half-up, once); r_A(100)=0.005, r_R=0.5; approximation 4.5; error 0.565835; 0.565835/5.065835 = 11.1696 percent (printed 11.17); 0.565835/4.5 = 12.574 percent; E1 gap 0.004565 and ratio 6.311 vs eps^2 factor 6.25; M1 CE 9, premium 1. Changed Example 1.5 wording (L02.html:136) and E3 solution (L02.html:486) re-read: 507 and rounding wording agree with the arithmetic.",
    },
    {
        "id": "E3f-lesson-numbers-L03", "check": "2.2-numbers",
        "location": "course/modules/E/E3/L03.html (Example 1.5, Example 2.5, Propositions 1.2-2.7, Remark 2.8, misconceptions, M1-R3, E1-E3, quiz, key results)",
        "status": "PASS",
        "evidence": "Round 12: " + RD + ": CE values 11250 (gamma 0), 10931.7733 (0.25), 10615.8009 (0.5), 10000 (1), 8888.8889 = 80000/9 (2), 7337.6161 (4); geometric mean 10000 exact; M = 9/80000 (E2), 1/1600 (Example 2.5), 1/3000 (M2), 1/9000 (M3); CE 1600 and 2000 (Example 2.5); cents bound 11/2 at k=10; r_A(4)=1/8 (M1). All match the lesson text and lab output.",
    },
    {
        "id": "E3f-lesson-numbers-L04", "check": "2.2-numbers",
        "location": "course/modules/E/E3/L04.html (Lemma 1.2, Examples 1.7, 2.5, 2.6, Lemma 2.2, Theorem 2.3 proof, Problem R3, canon-breaks, misconceptions, M1-R3, quiz, key results)",
        "status": "PASS",
        "evidence": "Round 12: " + RD + ": Example 2.5 I_X = (0,0,500,1000,2000), I_Y = (0,250,500,1250,2000); pair B I_Y = (0,0,0,500,1500); pair C I_X = (0,500,1000,1500,2000), I_Y = (0,0,0,1000,2000); means 2500/2000 (M1), 3000/3500 (Example 1.7), 3000/3000 (Examples 2.5, 2.6); M3 I(3000)=500; E1 I_Y(4000)=500. Lab counts 24/8 and 3/2 and the 10 and 2 no-ranking counts agree with lab output (run_labs).",
    },
    {
        "id": "E3f-coverage-cards", "check": "2.7-cards-coverage",
        "location": "course/modules/E/E3/L01.html-L04.html (labelled Definition, Proposition, Theorem, Lemma, Remark and Assumption blocks; key-results rows)",
        "status": "PASS",
        "evidence": "Round 12, by reading all four lessons: every key-results row of L01-L04 has at least one card of the same grade (L01 rows -> c007, c008, c010, c011/c012, c013; L02 rows -> c019, c022/c023, c024/c025, c026, c027; L03 rows -> c037, c040, c041, c043, c046/c047/c055/c180, c048, c049, c168, c054/c160/c171; L04 rows -> c057, c060, c062, c065, c067/c068/c070/c181/c183, c073/c075/c076). The only mirror with a grade mismatch is c183 (row E3f-E3-c183). Not every labelled block needs a card.",
    },
    {
        "id": "E3f-dag-L02-crra-forward-use", "check": "2.9-define-before-use",
        "location": "course/modules/E/E3/L02.html; L03.html; L04.html (concept links and forward references)",
        "status": "PASS",
        "evidence": "Round 12: grep -c -i crra L02.html = 0; L02 uses only concepts of M4 (expectation, variance), M2 (derivative) and L01 (expected-utility), all in the closure (plan §0.1). ledgers/E3/scripts/E3-f-r12/check_dag.out: 'check_dag E3: PASS', exit 0.",
    },
    {
        "id": "E3f-dag-other-links", "check": "2.9-define-before-use",
        "location": "course/modules/E/E3/L01.html-L04.html (Uses and Introduces lines, concept links)",
        "status": "PASS",
        "evidence": "Round 12: Uses/Introduces meta rows L01-L04 (lines 36-39) read; each link points to a defined concept (L01 expected-utility; L02 certainty-equivalent and arrow-pratt-risk-aversion; L03 crra-utility; L04 first- and second-order dominance) or to M1/M2/M4 closure concepts. check_dag.out PASS.",
    },
    {
        "id": "E3f-notation", "check": "2.13-notation",
        "location": "course/modules/E/E3/L01.html-L04.html vs notation/notation.json and plans/E3-build-plan.md §4",
        "status": "PASS",
        "evidence": "Round 12: macro census of the four lessons (grep -o '\\\\[A-Za-z]*'): \\E, \\Prob, \\Var, \\R, \\indic used as registered; no raw \\mathbb{E}; no T, R_f, R^\\ast, \\Phi, \\gamma_3, \\gamma_4 or \\mathbb{Q} used. gamma (CRRA coefficient, plan §4 local), pi (premium, plan §4 allows as word or local), \\mathrm{CE} and \\varepsilon are used as the plan says. Two letters clash with plan §4 and are separate rows: E3f-notation-kappa and E3f-notation-alpha.",
    },
    {
        "id": "E3f-notation-kappa", "check": "2.13-notation",
        "location": "course/modules/E/E3/L02.html:434-436 (M3), :445-447 (P1), :607-609 (quiz q10); clash with course/modules/E/E3/index.html:114 and course/modules/E/E3/project.html:53, 57, 153, 205",
        "status": "FAIL",
        "evidence": "Round 12: plans/E3-build-plan.md §4 (binding, BUILDER_RULES §2.1 item 7) assigns kappa to the logit choice precision. L02 uses kappa as the absolute risk aversion of the exponential utility u(w)=-e^{-kappa w} (M3, P1, quiz q10; lines 434-436, 445-447, 607-609). index.html:114 uses kappa > 0 as the choice precision and project.html uses it the same way. One letter has two meanings in the unit. L08.html:598-600 already writes the same exponential utility with nu, so L02 is the outlier.",
        "fix": "In course/modules/E/E3/L02.html rename the exponential-utility coefficient kappa to nu in M3 (lines 434-436), P1 (445-447) and quiz q10 (607-609), as L08.html:598-600 does. No other change. Keep kappa for choice precision in index.html and project.html.",
    },
    {
        "id": "E3f-notation-alpha", "check": "2.13-notation",
        "location": "course/modules/E/E3/L01.html:86 (Definition 2.1), :91-121 (Propositions 2.2-2.3 and proofs), :389-421 (P1, E2), :468 (key results), :216-312 (Lab 1 code and expected block, twin tests/labs/E3/lab-E3-L01-1.py); clash with course/modules/E/E3/L06.html:79-89",
        "status": "FAIL",
        "evidence": "Round 12: plans/E3-build-plan.md §4 assigns alpha to the value and weighting exponents of the Tversky-Kahneman form. L01 uses alpha for the mixture weight alpha L + (1 - alpha) M (30 uses in the lesson text and lab, first at L01.html:86). L06.html:79-89 uses alpha as the gains exponent in v(x) = x^alpha. The same letter has two meanings across the unit. The round-11 notes did not report this.",
        "fix": "Rename the mixture weight in L01 (Definition 2.1 and every later use in L01 named in the location, key results row L01.html:468, the Lab 1 code and its twin tests/labs/E3/lab-E3-L01-1.py followed by tools/embed_labs.py refresh, and cards E3-c005, E3-c007 and E3-c008) to q, which plan §4 does not assign. Keep alpha for the prospect exponent in L06-L08. Owner of L06 may confirm.",
    },
    {
        "id": "E3f-banned-and-process", "check": "1.3-1.4-banned",
        "location": "course/modules/E/E3/L01.html-L04.html (visible prose)",
        "status": "PASS",
        "evidence": "Round 12: grep -n -i -E 'TODO|TBD|lorem|\\.\\.\\.|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|well known|obviously|clearly|round|verifier|builder|placeholder|build' over L01-L04: only 'round' in mathematical and code context (Remark 2.8, Lab code). No banned phrase and no process word in learner text.",
    },
    {
        "id": "E3f-hours", "check": "2.12-hours",
        "location": "course/modules/E/E3/index.html:29,127; L01-L04 eyebrows and data-hours",
        "status": "PASS",
        "evidence": "Round 12: grep data-hours in L01-L04 = 7 each (L01.html:2, L02.html, L03.html, L04.html); eyebrows read '7 study hours'. check_pages.out: PASS (hub 56 + 14 = 70; eight lessons x 7 = 56).",
    },
    {
        "id": "E3f-references", "check": "2.1-citations",
        "location": "course/modules/E/E3/L02.html:616 (pratt1964risk); references/references.json (pratt1964risk)",
        "status": "PASS",
        "evidence": "Round 12: registry record pratt1964risk: title 'Risk Aversion in the Small and in the Large', author Pratt, John W., year 1964, container Econometrica, volume 32, status verified (crossref). L02.html:616 cites the same title, the journal and year, and names the work for the name only (no passage or result attributed). verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'.",
    },
    {
        "id": "E3f-L03-references", "check": "2.1-citations",
        "location": "course/modules/E/E3/L03.html:564; course/modules/M/M1/L03.html (Propositions 1.4, 1.6(b), A2, A3)",
        "status": "PASS",
        "evidence": "Round 12: L03 cites no registry key. Its module citations were read in course/modules/M/M1/L03.html: Proposition 1.4 (ln(e^x)=x, line 92), Proposition 1.6(b) (ln(ab)=ln a + ln b, line 112), the addition rule A2 (e^{a+b}=e^a e^b, line 60), the uniqueness in A3 (line 61), and 'e is defined as e^1' (line 63). The lesson does not derive lim (e^h-1)/h = 1 (no limit in M1 L03), so A2 of L03 is taken as given, as L03.html:59 says.",
    },
    {
        "id": "E3f-cards-near-duplicates", "check": "2.7-cards-duplicates",
        "location": "course/modules/E/E3/cards.json (full scan of 178 cards)",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/cards_scan.py -> cards_scan.out: no exact duplicate front or back among 178 cards. Token-Jaccard pairs with a slice card (front >= 0.4 or front+back >= 0.5) were read; each pair asks a different question (e.g. c047 gamma=2 vs c180 gamma=1 for the same lottery; c067 vs c181 integrated values of X and Y; c035 vs c127 Part C of different lab labels).",
    },
    {
        "id": "E3f-cards-slice-scan", "check": "2.7-cards-duplicates",
        "location": "course/modules/E/E3/cards.json (90 slice cards: L01 18, L02 22, L03 26, L04 24)",
        "status": "PASS",
        "evidence": "Round 12: cards_scan.out 'slice counts ... total 90' (L01 18, L02 22, L03 26, L04 24). Every slice card is read in full in this round and matched to its lesson location (locators in the rows E3f-E3-c001 to c183).",
    },
    {
        "id": "E3f-cards-integrity", "check": "2.7-cards-integrity",
        "location": "course/modules/E/E3/cards.json (178 cards)",
        "status": "PASS",
        "evidence": "Round 12: check_pages.py --unit E3 printed 'check_pages E3: PASS', exit 0 (includes cards.json checks: unique ids, lesson exists, grade valid, cite keys known, non-T grade has cite or basis). cards_scan.out: 178 unique ids.",
    },
    {
        "id": "E3f-cards-numbers", "check": "2.2-numbers",
        "location": "course/modules/E/E3/cards.json (slice cards) vs L01-L04",
        "status": "PASS",
        "evidence": "Round 12: cards_scan.py printed 'numbers absent from lesson html: []' over all 90 slice cards; each numeric result of the cards was re-derived in rederive.out.",
    },
    {
        "id": "E3f-cards-xrefs", "check": "2.7-cards",
        "location": "course/modules/E/E3/cards.json (slice cards: Definition, Proposition, Remark, Problem, section and misconception references)",
        "status": "PASS",
        "evidence": "Round 12: each cross-reference in the slice cards was checked against the lesson locator above, e.g. c022 -> Proposition 1.3(a) (L02.html:103), c053 -> Problem R3 (L03.html:455), c055 -> Problem E2 (L03.html:425), c071 -> Problem R3 (L04.html:614), c077 -> section 3 (L04.html:492), c168 -> Remark 2.8 (L03.html:184), c014 -> section 5 first misconception (L01.html:343).",
    },
    {
        "id": "E3f-cards-grades", "check": "2.7-cards-grades",
        "location": "course/modules/E/E3/cards.json (grade and basis, slice cards)",
        "status": "FAIL",
        "evidence": "Round 12: grades were checked against plans/FINAL-ARCHITECT-RULINGS.md item 13 and the key-results tables. Every C card (c016, c017, c032-c035, c054, c073, c075, c076, c160, c161, c171) names its lab and carries a basis, and every T card cites a proof, example or key-results row. One result card has no grade: E3-c183 (Example 2.6 result; its mirror key row L04.html:632 is T). Row E3f-E3-c183.",
        "fix": 'Add "grade": "T" to E3-c183 in course/modules/E/E3/cards.json (see row E3f-E3-c183).',
    },
    {
        "id": "E3f-delta", "check": "0-delta",
        "location": "git diff ccaeeaf44bea94b37d912ec1da3c660bb2c55d87..329c1d7f -- course/modules/E/E3 plans tests/labs/E3",
        "status": "PASS",
        "evidence": "Round 12: git diff --stat for slice files: L01.html (quiz q4 explanation, line 511), L02.html (Example 1.5 wording line 136; E3 solution line 486), cards.json (E3-c049 back, FIXED; E3-c130 is L07, outside slice). Every hunk in slice f was read. Lab twins L01-L04 and their expected blocks: unchanged in this delta (lab_twin_check.out re-run). plans/FINAL-ARCHITECT-RULINGS.md item 13 read. Out-of-slice hunks (L05, L07, grader, project.html, lab-E3-L05-1.py, lab-E3-project-3.py, PC3, E4, LX1, BK4, SC1) not checked here.",
    },
    {
        "id": "E3f-E3-r7-independent-rederivation", "check": "2.2-numbers",
        "location": "ledgers/E3/scripts/E3-f-r12/rederive.py",
        "status": "PASS",
        "evidence": "Round 12: independent Fraction and Decimal (50 digits) recomputation of every lesson number in the four numbers rows, not using the lab code: " + RD + " (exit 0). Lab output rederived with a float copy of the lab formulas (lab recompute lines).",
    },
    {
        "id": "E3f-cmd-check_pages", "check": "2.9-structure",
        "location": "tools/check_pages.py --unit E3",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/check_pages_unit.out: 'check_pages E3: PASS', exit 0.",
    },
    {
        "id": "E3f-cmd-check_dag", "check": "2.9-define-before-use",
        "location": "tools/check_dag.py --unit E3",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/check_dag.out: 'check_dag E3: PASS', exit 0.",
    },
    {
        "id": "E3f-cmd-check_projects", "check": "2.6-projects",
        "location": "tools/check_projects.py --unit E3 (project slice owns the content)",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/check_projects.out: 'check_projects E3: PASS', exit 0 (run as a gate, outside the lesson slice).",
    },
    {
        "id": "E3f-cmd-page_smoke", "check": "2.9-structure",
        "location": "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 (run alone)",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/page_smoke_L01-L04.out: each of L01-L04 PASS, lab lab-E3-L0n-1 runs in the in-page runtime, 'page_smoke E3: PASS', exit 0.",
    },
    {
        "id": "E3f-cmd-pytest-labs", "check": "2.5-labs",
        "location": "python -m pytest tests/test_labs.py -k E3 -q",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/pytest_labs_E3.out: 15 tests passed, exit 0.",
    },
    {
        "id": "E3f-cmd-ruff-labs", "check": "2.5-labs",
        "location": "ruff check and ruff format --check on tests/labs/E3/lab-E3-L01-1.py .. lab-E3-L04-1.py",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/ruff_check.out: 'All checks passed!', exit 0; ruff_format.out: '4 files already formatted', exit 0.",
    },
    {
        "id": "E3f-cmd-mypy-twins", "check": "2.5-labs",
        "location": "mypy --no-incremental on the four L01-L04 twins",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/mypy_twins.out: 'Success: no issues found in 4 source files', exit 0.",
    },
    {
        "id": "E3f-cmd-verify_refs", "check": "2.1-citations",
        "location": "tools/verify_refs.py --offline",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. The live run is the scheduled job, not run here.",
    },
    {
        "id": "E3f-cmd-run_labs-L01-L04", "check": "2.5-labs",
        "location": "tools/run_labs.py --unit E3 --page L01 .. L04",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/run_labs_L01.out .. run_labs_L04.out: each 'run_labs E3: PASS (1/1)', exit 0.",
    },
    {
        "id": "E3f-banned-cards", "check": "1.3-1.4-banned",
        "location": "course/modules/E/E3/cards.json (slice cards)",
        "status": "PASS",
        "evidence": "Round 12: the banned-phrase and process-word grep above run over cards.json as well; no hit. No ellipsis character and no '...' in front or back (cards_scan.py).",
    },
    {
        "id": "E3f-lab-L01", "check": "2.5-labs",
        "location": "course/modules/E/E3/L01.html lab block (lines 161-326); tests/labs/E3/lab-E3-L01-1.py",
        "status": "PASS",
        "evidence": "Round 12: ledgers/E3/scripts/E3-f-r12/lab_twin_check.out: page code equals the twin (after html unescape); expected block equals the output of the twin run alone under python -I -W error (exit 0, empty stderr). Hypothesis read: quadratic values 45000, 21250, 37500 match Part A; the 'negative' and 'short' ValueError messages match Part D; the interpretation (L01.html:325) names only what is printed.",
    },
    {
        "id": "E3f-lab-L02", "check": "2.5-labs",
        "location": "course/modules/E/E3/L02.html lab block (lines 207-382); tests/labs/E3/lab-E3-L02-1.py",
        "status": "PASS",
        "evidence": "Round 12: lab_twin_check.out: page code equals the twin; expected equals output; exit 0, empty stderr. Hypothesis and interpretation read against the printed numbers: gap 0.565835 at eps=1, gaps shrink (gaps_shrink_as_eps_falls True), linear premium zero, 'five scales' and 'not a proof' sentences agree with Part B.",
    },
    {
        "id": "E3f-lab-L03", "check": "2.5-labs",
        "location": "course/modules/E/E3/L03.html lab block (lines 187-327); tests/labs/E3/lab-E3-L03-1.py",
        "status": "PASS",
        "evidence": "Round 12: lab_twin_check.out: page code equals the twin; expected equals output; exit 0, empty stderr. Hypothesis: 11250, 10000, 8889 rounding, 80000/9 and the falling grid match the printed lines. The interpretation (L03.html:326) says the grid checks are numerical and not proofs, which the code and output support.",
    },
    {
        "id": "E3f-lab-L04", "check": "2.5-labs",
        "location": "course/modules/E/E3/L04.html lab block (lines 176-486); tests/labs/E3/lab-E3-L04-1.py",
        "status": "PASS",
        "evidence": "Round 12: lab_twin_check.out: page code equals the twin; expected equals output; exit 0, empty stderr. Named pairs A, B, C and the 24 seeded pairs: printed FOSD and SOSD counts, the 10 and 2 no-ranking counts, pairs 16 and 19, and the 37 agreements match the output lines 440-484. SIMULATED label present (lab docstring and output header).",
    },
]

# the card rows must cover the 90 slice cards exactly
slice_ids = {
    "E3-c001","E3-c002","E3-c003","E3-c004","E3-c005","E3-c006","E3-c007","E3-c008","E3-c009","E3-c010","E3-c011","E3-c012",
    "E3-c013","E3-c014","E3-c015","E3-c016","E3-c017","E3-c018","E3-c019","E3-c020","E3-c021","E3-c022","E3-c023","E3-c024",
    "E3-c025","E3-c026","E3-c027","E3-c028","E3-c029","E3-c030","E3-c031","E3-c032","E3-c033","E3-c034","E3-c035","E3-c036",
    "E3-c037","E3-c038","E3-c039","E3-c040","E3-c041","E3-c043","E3-c044","E3-c045","E3-c046","E3-c047","E3-c048","E3-c049",
    "E3-c050","E3-c051","E3-c052","E3-c053","E3-c054","E3-c055","E3-c056","E3-c057","E3-c058","E3-c059","E3-c060","E3-c061",
    "E3-c062","E3-c063","E3-c064","E3-c065","E3-c066","E3-c067","E3-c068","E3-c070","E3-c071","E3-c072","E3-c073","E3-c074",
    "E3-c075","E3-c076","E3-c077","E3-c159","E3-c160","E3-c161","E3-c162","E3-c167","E3-c168","E3-c171","E3-c173","E3-c174",
    "E3-c175","E3-c177","E3-c178","E3-c180","E3-c181","E3-c183"}
assert len(slice_ids) == 90, len(slice_ids)
assert set(cards) == slice_ids, (set(cards) ^ slice_ids)
# the previous round's card row set plus the two removed-card rows, kept
card_row_ids = {r["id"] for r in rows}

extra_keep = [
    {"id": "E3f-E3-c186", "check": "2.7-cards", "location": "course/modules/E/E3/cards.json (E3-c186 absent)",
     "status": "PASS", "evidence": "Round 12: grep -c '\"E3-c186\"' course/modules/E/E3/cards.json returns 0 (card removed; replacement E3-c187 is in L07, outside slice f)."},
    {"id": "E3f-E3-c178-b", "check": "2.7-cards", "location": "course/modules/E/E3/cards.json (E3-c178) vs L03.html:112",
     "status": "PASS", "evidence": "Round 12: cards_scan.out: 178 unique ids over 178 cards; E3-c178 appears once. Definition 1.6 at L03.html:112 states the card's back."},
]

# c183 is FAIL and the notation rows are FAIL: their fixes are present
all_rows = rows + extra + extra_keep
ids = [r["id"] for r in all_rows]
assert len(ids) == len(set(ids)), "duplicate ids"

frag = {
    "unit": "E3",
    "slice": "f",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-f, round 12 (did not build E3)",
    "pin": "329c1d7f",
    "base": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87 (round-11 pin; round-11 fragment at /Users/billyribeiro/.fanout/frags/D-E3-f.round11.json)",
    "checkout": str(ROOT),
    "scratch": R,
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": all_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice f: lessons L01-L04 and the 90 slice cards. There is no project grader in this slice, so the five alternative implementations and the student-error mutants (plan 6.4, 6.5) do not apply; mutants is empty by design (project slices own them).",
        "Round-12 delta (ccaeeaf -> 329c1d7) read for every slice hunk: L01.html quiz q4 explanation, L02.html Example 1.5 wording and its E3 solution, cards.json E3-c049 (round-11 FAIL, fixed). Every row was re-verified this round; no row is carried from round 11.",
        "Lab twins L01-L04 and their expected blocks are byte-identical to the previous pin in this delta; they were re-run anyway (run_labs, python -I -W error, page-vs-twin comparison).",
        "New findings this round (not in round 11): notation clashes for kappa (L02 vs index.html and project.html) and alpha (L01 vs L06), both against plan §4; and card E3-c183 without a grade where ruling 13 requires T.",
        "Not checked in this slice: project.html and grader/ (other slice); run_graders and mutate_graders (no project grader here); the live verify_refs run (network not used); the full text of cited published works (only registry records are read; no locator is quoted from them); L05-L08 cards and lessons (outside slice f), and the L05-L08 notation uses beyond the kappa and alpha clashes; Lab 1 simulated counts were checked against the printed output and by a re-run of the lab, not by an independent simulation of the seeded draws.",
        "Observation (not a row): L01 uses a and b as affine constants and L03 Proposition 1.2 uses a and b as exponents. Both are local to their lesson and neither letter is assigned by plan §4; no defect, but a reader could confuse them.",
    ],
    "summary": "",
}
n = len(all_rows)
fails = [r for r in all_rows if r["status"] != "PASS"]
passes = [r for r in all_rows if r["status"] == "PASS"]
frag["summary"] = (
    f"Slice f round 12 at 329c1d7: {n} rows: {len(passes)} PASS, {len(fails)} FAIL, 0 UNVERIFIABLE. "
    "FAIL: E3f-notation-kappa (L02 uses kappa for the exponential-utility coefficient; plan §4 and index/project use kappa for choice precision; fix: nu as in L08); "
    "E3f-notation-alpha (L01 mixture weight alpha vs L06 prospect exponent; plan §4 assigns alpha to the exponents; fix: rename L01 mixture weight); "
    "E3f-E3-c183 and E3f-cards-grades (result card with no grade where its mirror key row is T; fix: add grade T). "
    "The round-11 FAIL on E3-c049 is resolved. All 90 slice cards, all four lessons' numbers, labs, DAG, banned phrases, references and gates re-run and PASS."
)
out = ROOT / "ledgers/E3/E3-f.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", n, "fails", len(fails))
