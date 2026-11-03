"""Build ledgers/M7/M7-e.json (round 3, slice e) from the round-2 fragment and the round-3 checks.

Usage: python3 -I build_fragment_r3.py <round2-fragment.json> <cards-r3.json> <out.json> <verified_at>

Rows are carried from round 2 only when the card entry (JSON object) and its lesson page are unchanged since the
round-2 pin c737272f. Every other card row is re-verified in this round and given fresh evidence.
"""
import json
import sys
from pathlib import Path

r2_path, cards_path, out_path, verified_at = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
r2 = json.loads(Path(r2_path).read_text(encoding="utf-8"))
cards = {c["id"]: c for c in json.loads(Path(cards_path).read_text(encoding="utf-8"))}
r2_cards = {}
for row in r2["rows"]:
    if row["id"].startswith("E-c"):
        r2_cards[row["id"]] = row
r2_slice = [row for row in r2["rows"] if row["id"].startswith("E-S")]

SCRIPTS = "ledgers/M7/scripts/M7-e-r3"
ALL_LESSONS_UNCHANGED = "course/modules/M/M7/L01.html..L08.html"

REMOVED = {
    "M7-c010": "M7-c191 (chord-gap definition) and M7-c189 (the value -1/2 of the same chord gap)",
    "M7-c048": "M7-c053 (the same unconstrained stationary point and its failure of feasibility)",
    "M7-c134": "M7-c135 and M7-c136 (the greedy plan and its optimality)",
    "M7-c146": "M7-c156 (Remark 1.5, the one-state example of non-uniqueness)",
    "M7-c180": "M7-c015 (negative eigenvalue refutes convexity whatever the diagonal) and M7-c165 (Q2 eigenvalues 3 and -1)",
    "M7-c188": "M7-c115 (the return does not rise as gamma rises)",
}

CHANGED_FRESH = {
    "M7-c002": "PASS. Back ('convexity is relative to that stated set') matches Definition 2.1 and the sentence at "
    "L01.html text line L01 0030 ('A function is convex or not only relative to a stated set S, which is why the "
    "definition names S'). The chord inequality in the back equals L01 0029. Grade T, no lab value.",
    "M7-c012": "PASS. Basis now reads 'Lab 1 (SIMULATED), exact count on the 25-point grid'; the SIMULATED header is at "
    "L01 0069. 552 = 3125 - 2573 re-derived exactly: "
    f"{SCRIPTS}/l01_check.out ('Q2 cases 3125 identity 3125 chord 2573 fail 552'). Grade C is a lab result.",
    "M7-c013": "PASS. Back cites Definition 2.1 and Problem R2 (L01 0134, 'one failing triple is enough'). Grade T. "
    "Consistent with L01 0030 and the quiz at L01 0192.",
    "M7-c015": "PASS. Q2 = [[1,2],[2,1]] has positive diagonal and eigenvalue -1 (Example 3.3, L01 0066; Problem P3, "
    f"L01 0110-0112). Recomputed in {SCRIPTS}/l01_check.out: (1,-1)'Q2(1,-1) = -2. Grade T.",
    "M7-c020": "PASS. Feasible points (0,-y), y > 0 (h = x = 0), satisfy f(0,-y) = -y^3 < 0 = f(0,0) (Example 2.6, "
    "L02 0038). Grade T.",
    "M7-c026": "PASS. Sigma = diag(1,2): w* = (2/3,1/3), multiplier 2/3 (Problem M2, L02 0091). Recomputed exactly in "
    f"{SCRIPTS}/l02_check.out (the M2 line (u = (1, 1/2), s = 3/2, lambda = 2/3, w* = (2/3, 1/3), f(w*) = 1/3)). Grade T.",
    "M7-c030": "PASS. Basis labelled SIMULATED. 36 of 36 for the identity and 36 of 36 for non-negativity (L02 0066, "
    f"0117); recomputed exactly in {SCRIPTS}/l02_check.out ('identity holds 36 of 36 nonneg 36'). Grade C.",
    "M7-c049": "PASS. Basis labelled 'Lab 1 (SIMULATED), exact arithmetic'; L03 0052 labels Sigma and mu SIMULATED. "
    "All four residuals are exactly zero at both candidates: labout/L03.out ('all four KKT conditions hold exactly: "
    f"True' for both instances) and {SCRIPTS}/l03_check.out (K1 residual zero in both components). Grade C.",
    "M7-c050": "PASS. Basis labelled SIMULATED. Stationarity residual (-1/2, 1/2) at (1/2,1/2) with the active "
    "multipliers, and dual residual 3/10 for lambda2 = -3/10 (L03 0060-0061). Recomputed in "
    f"{SCRIPTS}/l03_check.out (stationarity residual at (1/2,1/2) with the active multipliers, and the dual residual for lambda2 = -3/10). Grade C.",
    "M7-c063": "PASS. Basis labelled SIMULATED. 1331 dual points, 21 primal points, 27951 pairs, all satisfying weak "
    f"duality (L04 0042-0043). Recomputed in {SCRIPTS}/l04_check.out ('dual points 1331 primal 21 pairs 27951', "
    "'weak duality pairs holding 27951'). Grade C.",
    "M7-c069": "PASS. Back cites Problem M3 for g(0,0) = -199/300 (L04 0080) and 49/300 below p* = -1/2 (L04 0061). "
    f"Recomputed in {SCRIPTS}/l04_check.out ('g(0,0) -199/300 diff -49/300'). Grade T.",
    "M7-c110": "PASS. Return 0.113798 and risk 0.123809 at gamma = 1 with weights (0.434783, 0.526836, 0.562535, "
    "-0.524154). Recomputed exactly in "
    f"{SCRIPTS}/l06_check.out (printed-style 6dp line: risk 0.123809 ret 0.113798). Basis labelled SIMULATED. Grade C.",
    "M7-c113": "PASS. The constrained objective is at least the budget-only objective at gamma = 1, 2, 4, 8, 16 "
    f"(Proposition 2.3; {SCRIPTS}/l06_check.out, Part B, constrained objective at least equality objective for each gamma). Basis labelled SIMULATED. "
    "Grade C.",
    "M7-c115": "PASS. Return falls from 0.113798 (gamma = 1) to 0.106241 (gamma = 16), to six places (L06 0069; "
    f"{SCRIPTS}/l06_check.out). Proposition 2.1 (L06 0032). Grade C with SIMULATED basis.",
    "M7-c132": "PASS. 70 = C(8,4) = 70 (l07_l08_small_check.out 'C(8,4) 70'); the enumeration count in "
    "labout/L07.out ('plans_checked_from_0_400 70'). Basis labelled SIMULATED. Grade C.",
    "M7-c152": "PASS. Tie count 0: labout/L08.out 'tied_pairs_t0_to_5 0' and "
    f"{SCRIPTS}/l08_check.out 'ties 0' (recomputed from the Bellman recursion). Basis labelled SIMULATED. Grade C.",
    "M7-c154": "PASS. Changes 6.0, 3.6, 2.74, 2.466, 2.2194, 1.99746 (labout/L08.out; "
    f"{SCRIPTS}/l08_check.out). 2.466/2.74 = 0.9, 2.2194/2.466 = 0.9, 1.99746/2.2194 = 0.9. Basis labelled SIMULATED. "
    "Grade C.",
    "M7-c170": "PASS. Largest grid dual value -1/2 at one point (lambda = (0, 3/10), nu = -1/2); smallest primal -1/2 at "
    f"(1,0); grid gap 0 ({SCRIPTS}/l04_check.out, line 'max dual -1/2 attained at ...' with lambda = (0, 3/10), nu = -1/2). Basis labelled SIMULATED. "
    "Grade C.",
    "M7-c173": "PASS. Grid minima -1/2 at w1 = 1 (active) and -1/4 at w1 = 1/2 (inactive) over 101 points "
    f"({SCRIPTS}/l03_check.out 'grid min -1/2 at w1= 1 count 101', 'grid min -1/4 at w1= 1/2 count 101'). Basis labelled "
    "SIMULATED. Grade C.",
    "M7-c178": "PASS. 184 ordered pairs with negative form and 3 x 184 = 552 (L01 0115-0117; "
    f"{SCRIPTS}/l01_check.out 'ordered pairs ... 184 3*neg= 552'). Basis labelled SIMULATED. Grade C.",
    "M7-c189": "PASS. Midpoint value 3/2, chord 1, chord minus midpoint -1/2, equal to (1/4)(x-y)'Q2(x-y) = -1/2 (L01 0070, "
    f"0174; {SCRIPTS}/l01_check.out). Basis labelled SIMULATED. Grade C.",
}

NEW_FRESH = {
    "M7-c190": ("PASS", "Definition 1.1 (L01 0017): the convex combination lambda x + (1 - lambda) y, lambda in [0, 1], "
                "and the segment between x and y. Grade T."),
    "M7-c191": ("PASS", "Left side of Lemma 3.1 (L01 0041-0042): lambda q(x) + (1 - lambda) q(y) - q(lambda x + (1 - lambda) y). "
                "The back's words 'weighted chord value minus the value at the weighted point' describe that expression. Grade T."),
    "M7-c192": ("PASS", "Definition 2.1 (L02 0020): a feasible point with grad f = lambda grad h for some real lambda. The "
                "back's 'necessary, not sufficient under Assumption 1' matches L02 0070 and Example 2.6 (L02 0038). Grade T."),
    "M7-c193": ("PASS", "Local minimizer defined in Section 1 (L02 0016): f(x*) <= f(x) for every feasible x in some open ball. "
                "Grade T."),
    "M7-c194": ("PASS", "Problem (P) in Definition 1.1 (L03 0016-0017): minimize f over R^n subject to g_i <= 0 and h_j = 0, with "
                "differentiable data. Grade T."),
    "M7-c195": ("PASS", "p* is the infimum over the feasible set when it is non-empty (L03 0017, Definition 1.1). Grade T."),
    "M7-c196": ("PASS", "Lagrangian dual: maximize g over dual feasible pairs, optimal value d*; p* of (P) (L04 0018, Definition 1.1). "
                "Grade T."),
    "M7-c197": ("PASS", "Zero gap d* = p*; L04 0048 says strong duality under Slater's condition is not stated as a numbered "
                "result on the page. Grade T."),
    "M7-c198": ("PASS", "Active set defined in L05 Section 3 (line 0049): the inequality rows of Gx <= h holding with equality at "
                "x. Grade T."),
    "M7-c199": ("PASS", f"Lab 1 Part A policy lines: s0=run and s1=run at every t from 0 to 5 "
                f"(labout/L08.out, 'policy t 0' to 'policy t 5' lines; {SCRIPTS}/l08_check.out, policy lines for t 0 to 5 with run in states 0 and 1). "
                "Basis labelled 'Lab 1 (SIMULATED), Part A'. Grade C."),
}

L05_SIMULATED_FAIL = {
    "M7-c087": "Lab 1, Part A, card basis 'Lab 1, Part A (exact arithmetic)' omits the SIMULATED label. The same kind of "
    "hand-chosen illustrative input carries that label on L01 0069 ('SIMULATED: ... illustrative inputs ... not data') and "
    "L03 0052 ('chosen by hand as illustrative numbers. They are SIMULATED'). L05.html text 0073 says only 'not data'. "
    f"{SCRIPTS}/scan_cards_r3.out lists this card.",
    "M7-c088": "Same defect as M7-c087: lab-result card, Part A inputs hand-chosen (L05 0073, 'not data' only), basis lacks SIMULATED.",
    "M7-c089": "Same defect as M7-c087: lab-result card (Part B enumeration), basis 'Lab 1, Part B (enumeration and 33 x 33 grid)' lacks SIMULATED.",
    "M7-c093": "Same defect as M7-c087: lab-result card cites Lab 1, Part A multipliers; basis lacks SIMULATED.",
    "M7-c171": "Same defect as M7-c087: lab-result card (determinant 19); basis lacks SIMULATED.",
    "M7-c172": "Same defect as M7-c087: lab-result card (grid 1089 points); basis lacks SIMULATED.",
    "M7-c182": "Same defect as M7-c087: lab-result card (multipliers -36/19, 11/19); basis lacks SIMULATED.",
}
L05_FIX = (
    "Add the word SIMULATED to the card basis (for example 'Lab 1, Part A (SIMULATED, exact arithmetic)') and make the "
    "L05.html lab sentence (text line 0073, 'The inputs are small integers chosen for this lab, not data') read "
    "'SIMULATED: the inputs are small integers chosen by hand for this lab, not data'. Judgement call stated in notes: "
    "round 2 passed these cards on the reading that 'not data' needs no label; BUILDER_RULES 1.7 and the L01/L03 precedent "
    "favour the label."
)

rows = []
# card rows, in id order
card_ids = sorted({f"E-c{cid[-3:]}" for cid in cards} | set(r2_cards))
for rid in card_ids:
    cid = "M7-c" + rid[-3:]
    if cid in REMOVED:
        base = r2_cards[rid]
        rows.append({
            "id": rid,
            "check": base["check"],
            "location": f"course/modules/M/M7/cards.json ({cid} removed after the round-2 pin c737272f)",
            "status": "PASS",
            "evidence": f"No subject to check: {cid} is not in cards.json at a007712f (removed after the round-2 pin). Its "
                        f"content is checked on the replacement card(s): {REMOVED[cid]}.",
        })
        continue
    if cid in L05_SIMULATED_FAIL:
        base = r2_cards[rid]
        rows.append({
            "id": rid,
            "check": "2.5/2.7 lab-result card: SIMULATED label (BUILDER_RULES 1.7); card-vs-lesson re-verified this round",
            "location": f"course/modules/M/M7/cards.json ({cid}, lesson L05, grade C); course/modules/M/M7/L05.html text line L05 0073",
            "status": "FAIL",
            "evidence": f"{L05_SIMULATED_FAIL[cid]} Card content otherwise matches L05 (re-derived, {SCRIPTS}/l05_check.out).",
            "fix": L05_FIX,
        })
        continue
    if cid in CHANGED_FRESH:
        base = r2_cards.get(rid, {})
        check = base.get("check", "card-vs-lesson: front, back, grade, basis, locator, numbers, duplicates, process words, SIMULATED label")
        rows.append({
            "id": rid,
            "check": check,
            "location": f"course/modules/M/M7/cards.json ({cid}, lesson {cards[cid]['lesson']}, grade {cards[cid]['grade']}); "
                        f"course/modules/M/M7/{cards[cid]['lesson']}.html text",
            "status": "PASS",
            "evidence": CHANGED_FRESH[cid],
        })
        continue
    if cid in NEW_FRESH:
        status, evidence = NEW_FRESH[cid]
        rows.append({
            "id": rid,
            "check": "card-vs-lesson: front, back, grade, basis, locator, numbers, duplicates, process words, SIMULATED label",
            "location": f"course/modules/M/M7/cards.json ({cid}, lesson {cards[cid]['lesson']}, grade {cards[cid]['grade']}); "
                        f"course/modules/M/M7/{cards[cid]['lesson']}.html text",
            "status": status,
            "evidence": evidence,
        })
        continue
    # unchanged card: carry the round-2 row when it was PASS
    base = r2_cards[rid]
    assert base["status"] == "PASS", rid
    rows.append({
        "id": rid,
        "check": base["check"],
        "location": base["location"],
        "status": "PASS",
        "evidence": "Carried from round 2 (cards.json entry " + cid + " and course/modules/M/M7/" + cards[cid]["lesson"]
                    + ".html byte-identical since the previous pin c737272f; the entry is a JSON object equal to its "
                    "round-2 value): " + base["evidence"],
    })

# slice-level rows
slice_rows = {row["id"]: row for row in r2_slice}
fresh_slice = {
    "E-S01": ("2.6-gate (check_pages)", "tools/check_pages.py --unit M7; cards.json",
              "PASS", f"`.venv/bin/python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 ({SCRIPTS}/gates/check_pages.log)."),
    "E-S02": ("2.9-gate (check_dag)", "tools/check_dag.py --all",
              "PASS", f"`.venv/bin/python tools/check_dag.py --all` exit 0; line 'check_dag M7: PASS' ({SCRIPTS}/gates/check_dag_all.log, 21 PASS lines)."),
    "E-S03": ("2.6-gate (check_projects)", "tools/check_projects.py --unit M7",
              "PASS", f"`check_projects.py --unit M7` -> 'check_projects M7: PASS', exit 0 ({SCRIPTS}/gates/check_projects.log)."),
    "E-S04": ("2.5-labs (run_labs)", "tools/run_labs.py --unit M7; tests/labs/M7/lab-M7-L01-1.py .. lab-M7-L08-1.py",
              "PASS", f"`run_labs.py --unit M7` -> 'run_labs M7: PASS (11/11)' ({SCRIPTS}/gates/run_labs.log). Each L01-L08 twin run alone under `python3 -I -W error`, exit 0; output saved to {SCRIPTS}/labout/L0n.out and identical to the round-2 labout files."),
    "E-S05": ("2.7-cards (banned and process phrases)", "cards.json front/back; L01-L08 extracts",
              "PASS", f"{SCRIPTS}/scan_cards_r3.out: 'banned/process hits: []' over 174 cards. Lesson extracts scanned for the BUILDER_RULES 1.3-1.4 strings (TODO, TBD, lorem, for brevity, beyond the scope, obviously, clearly, it is important, studies show, can be shown, roughly, historically): none. Ellipses are math ranges or lab-docstring ranges, not omitted content."),
    "E-S06": ("2.7-cards (duplicates)", "cards.json; card_checks_r3.py",
              "PASS", f"{SCRIPTS}/card_checks_r3.out: 174 cards, 174 unique ids, no exact duplicate fronts or backs. Ten near-duplicate pairs (ratio > 0.75): c009/c165, c014/c177, c028/c151, c032/c051, c038/c187, c042/c081, c046/c047, c087/c182, c131/c175, c168/c181. Each pair asks about a different matrix, misconception, theorem, instance or lab (for example L07 vs L08 brute-force checks, 20 vs 18 pairs), so none is a duplicate card."),
    "E-S07": ("2.7-cards (basis and grade)", "cards.json front/back/basis; scan_cards_r3.out",
              "PASS", f"Every C card has a non-empty basis and every T card has no basis field ({SCRIPTS}/card_checks_r3.out: 'C cards without basis []', 'T cards with a basis field []'). Grades T 126, C 48. The SIMULATED-label defect on seven L05 lab cards is a separate FAIL row (E-c087 etc.)."),
    "E-S08": ("2.2-numbers (numbers in cards vs lesson text)", "cards.json numbers; card_checks_r3.out; L01-L08 extracts",
              "PASS", f"{SCRIPTS}/card_checks_r3.out: 12 numeric tokens absent as plain text; all 12 are present in the lesson LaTeX (\\tfrac{{a}}{{b}} form, checked for each: 2/3 L02, 1/8 L03 and L05, 11/30 and 14/15 L03, 7/300, 49/300, 199/150 L04, 4/11, 18/11, 11/4 L05). 0 references missing. Card numbers recomputed by l01..l08 scripts ({SCRIPTS}/l0n_check.out)."),
    "E-S09": ("2.8 / notation (notation/notation.json)", "notation/notation.json (7 registered symbols and macros); cards.json; L01-L08.html",
              "PASS", "Registered symbols: T (return observations), Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (blackboard). The M7 pages use none of them with another meaning: no T as a count, no Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f or blackboard Q. Local letters (beta, gamma, H, S, F, U, V, B, K, L, G) are defined in the lesson where first used, as the notation file requires for non-registered letters."),
    "E-S10": ("2.1-references (verify_refs offline)", "tools/verify_refs.py --offline",
              "PASS", f"`verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({SCRIPTS}/gates/verify_refs_offline.log). cards.json has no 'cite' field (grep count 0), and the lessons cite no registry key."),
    "E-S11": ("2.3-grades (rule 9: T cards carrying lab-printed numbers)", "cards.json T cards; scan_cards_r3.out",
              "PASS", f"{SCRIPTS}/scan_cards_r3.out 'T-graded cards carrying lab-printed values: []'. The T cards that name Lab 1 (M7-c060, c085, c090, c099, c101, c117) use the lab only for a description or for a value the page derives (7/300 by R3, -199/300 by M3). c064's 0.6633 is the decimal of 199/300."),
    "E-S12": ("2.8-smoke (page_smoke)", "tools/page_smoke.py --unit M7",
              "PASS", f"`page_smoke.py --unit M7` -> 'page_smoke M7: PASS', exit 0; all 14 pages PASS, including L01-L08, project.html, index.html, concepts.html and review.html ({SCRIPTS}/gates/page_smoke.log)."),
    "E-S13": ("code gates (ruff check, mypy, pytest) scoped to M7", "ruff check .; mypy --no-incremental; pytest tests/test_curriculum.py tests/test_docs_figures.py tests/test_page_checks.py",
              "PASS", f"ruff check: 'All checks passed!' ({SCRIPTS}/gates/ruff_check.log). mypy --no-incremental: 'Success: no issues found in 331 source files' ({SCRIPTS}/gates/mypy.log). pytest: 29 passed (test_curriculum, test_docs_figures) and test_page_checks all passed ({SCRIPTS}/gates/pytest_relevant.log, pytest_page_checks.log). Out of this slice and noted in notes: `ruff format --check .` reports one file under ledgers/M3/retired/ (not M7); M7 files are formatted."),
    "E-S14": ("2.5-labs (independent recomputation)", "l01_check.py .. l08_check.py, l07_l08_small_check.py, card_checks_r3.py",
              "PASS", f"Scripts in {SCRIPTS}/ run with `python3 -I`; outputs beside them. They recompute every number the lab-result and derived cards state: L01 2573, 552, 184, identities, the Q2 example; L02 Sigma, lambda 177/55, w, f 177/110, residuals, 36/36, M2/M3; L03 grid minima -1/2 and -1/4 on 101 points, KKT residuals, the Example 4.1 lower bound identity, norm sqrt(1/2); L04 1331/21/27951, -199/300, grid gap 0, R3 7/300, -157/300; L05 det 19, x, lambda, objective 551/722 = 29/38, x'Qx 43/19, v'Qv 19, the four active sets, 1089 grid points; L06 every printed equality and constrained row, 0.5722548, 0.5588607, one passing set per gamma; L07 and L08 recursions, brute force, 70, 378, change sequence, ratios; L07 M1-M3 and Remark 2.5 and R2 by plan enumeration; L08 M2-M3 and the beta = -1 example."),
    "E-S15": ("2.5-mutants (not applicable to a card slice)", "cards.json",
              "PASS", "Slice e is cards.json plus lesson pages. It contains no executable grader and no student-code mutant target, so no mutant applies to this slice. ledgers 'mutants' is empty. The project mutant rules belong to the project slices."),
    "E-S16": ("2.2-count (card count vs task)", "cards.json (174 entries); round-2 fragment (170 card rows)",
              "PASS", "174 cards at a007712f = 170 round-2 cards - 6 removed (c010, c048, c134, c146, c180, c188) + 10 added (c190-c199). The round-1 pin had 169. Card-id gaps are stable ids, not defects."),
    "E-S17": ("2.9-structure (lab-label on lesson page, BUILDER_RULES 1.7)", "course/modules/M/M7/L05.html text line L05 0073",
              "FAIL", "The L05 lab section says 'The inputs are small integers chosen for this lab, not data.' L01 (0069) and L03 (0052) describe the same kind of hand-chosen inputs as SIMULATED. L05 never uses the label, so its lab-result cards (E-c087, c088, c089, c093, c171, c172, c182) cannot carry it either."),
    "E-S18": ("2.5-labs (printed expected block equals output)", f"{SCRIPTS}/output_vs_page.py; labout/L01.out..L08.out",
              "PASS", f"{SCRIPTS}/output_vs_page.out: every printed output line of each twin (14, 13, 22, 12, 23, 35, 20, 26 lines) occurs verbatim in its lesson page text."),
    "E-S19": ("2.5-labs (page code equals twin)", f"{SCRIPTS}/twin_vs_page.py",
              "PASS", f"{SCRIPTS}/twin_vs_page.out: every non-empty line of each twin tests/labs/M7/lab-M7-L0n-1.py occurs in course/modules/M/M7/L0n.html (104, 102, 101, 83, 155, 175, 120, 112 lines; 0 missing)."),
    "E-S20": ("2.9-hours (hours split sums to curriculum figure)", "index.html data-hours; L01-L08 study hours",
              "PASS", "Lesson hours 9 + 9 + 10 + 10 + 10 + 10 + 9 + 10 = 77 = data-hours-lessons 77. Project 33 = data-hours-project. 77 + 33 = 110 = curriculum hours (curriculum/01-foundations.yaml:298-302). Project share 33/110 = 30%, not above the 30% limit."),
    "E-S21": ("2.9-structure (template sections present)", "L01-L08.html text",
              "PASS", "Each lesson has the header (lesson n of 8, study hours), Uses/Introduces, the grade legend, numbered sections, the key-results table, the retrieval quiz, the references section, the mark-complete control, and previous/next links. Problem sets with M, P, E and R problems and worked solutions are present in all eight lessons."),
    "E-S22": ("2.2 / 2.4 / 2.5 / 2.9 lesson prose and mathematics (L01-L08)", "course/modules/M/M7/L01.html..L08.html (text extracts)",
              "PASS", f"Each lesson text was read in full (extracts in {SCRIPTS}/L01.txt..L08.txt, about 280 KB), including lab docstrings, every theorem, proposition, lemma, remark, example, problem solution, empirical E-problem and research R-problem, and the quiz. Every numbered claim, proof step and printed value was recomputed by the scripts above. Specific checks: Lemma 3.1 identity (L01); Prop 3.2 (ii)->(iii) step via x = V e_i (L01 0062); Theorem 2.2 (L02) construction d_k = -sum g_j d_j / g_k (L02 0031); Example 2.3 midpoint -1/8 > -1/2 (L03 0044); Example 4.1 ν = -1/2, λ2 = 3/10, f = -1/2 (L03 0054); Example 3.4 g(lambda) = -1/(4 lambda) (L04 0052); R3 grid gap 7/300 (L04 0119); Remark 2.4 completing the square and v'Qv = 19 (L05 0047, 0194); Prop 3.4 midpoint identity (L05 0066); Example 3.6 f = -9/4 (L05 0070); M1-M3 L06 (0080-0088); Prop 2.1 two-inequality proof (L06 0036); R3 turnover region [0.4, 0.6] (L06 0127); L07 V1(400) = 220 witness 200,100,100 (L07 0162); L08 M1 V4(0)=9.6 (L08 0069); beta = -1 counterexample (L08 0054). No lesson-level error was found in the prose, the mathematics or the lab-quoted values, except the L05 SIMULATED label (E-S17)."),
    "E-S23": ("2.9-DAG (concepts used before definition or outside the closure)", "check_dag.py; L01-L08 'Uses' lines",
              "PASS", f"`check_dag.py --all` (M7 PASS, {SCRIPTS}/gates/check_dag_all.log). Read by hand: each lesson's 'Uses' line names only earlier lessons, M1-M3 prerequisites or concepts of M2/M3 (gradient, Hessian, PSD, eigendecomposition, implicit function theorem, induction). Slater's condition is defined in L03 (inline) and again in L04 Definition 3.1; midpoint convexity is defined in L05 Proposition 3.4 before L06 uses it."),
}

for rid in ["E-S01", "E-S02", "E-S03", "E-S04", "E-S05", "E-S06", "E-S07", "E-S08", "E-S09", "E-S10", "E-S11",
            "E-S12", "E-S13", "E-S14", "E-S15", "E-S16", "E-S17", "E-S18", "E-S19", "E-S20", "E-S21", "E-S22", "E-S23"]:
    check, location, status, evidence = fresh_slice[rid][0], fresh_slice[rid][1], fresh_slice[rid][2], fresh_slice[rid][3]
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = L05_FIX if rid == "E-S17" else ""
        row["fix"] = ("Add the word SIMULATED to the L05 lab sentence (course/modules/M/M7/L05.html text line 0073): "
                      "'SIMULATED: the inputs are small integers chosen by hand for this lab, not data.' Then add the "
                      "SIMULATED label to the seven lab-result cards listed in E-c087 to E-c182.")
    rows.append(row)

fragment = {
    "unit": "M7",
    "slice": "e",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-e, round 3 (did not build M7; read all eight lessons and every card of the current cards.json)",
    "pin": "a007712f",
    "base": "c737272f (round-2 pin). Delta for this slice: cards.json only (M7-c010, c048, c134, c146, c180, c188 removed; c190-c199 added; 21 entries changed). L01.html to L08.html, tests/labs/M7/lab-M7-L01..L08 and notation/ are byte-identical to c737272f.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M7-e",
    "scratch": "/tmp/m7e-r3 (lesson text extracts, regenerable with ledgers/M7/scripts/M7-e-r3/extract_text.py)",
    "verified_at": verified_at,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Verdict FAIL on one defect class, the SIMULATED label on lab-result cards in L05: seven cards (M7-c087, c088, c089, c093, c171, c172, c182) "
        "and the L05 lab sentence (L05.html text 0073). Round 2 passed these on the reading that 'not data' needs no label; this round "
        "overturns that reading on BUILDER_RULES 1.7 and the L01/L03 precedent, and says so in each row. If the orchestrator rules the L05 inputs "
        "are not simulated data, these eight rows (E-c087, c088, c089, c093, c171, c172, c182 and E-S17) can be set to PASS; every other row stands. "
        "All eight round-2 FAIL rows (E-c012, c049, c050, c063, c170, c173, c178, c189) are fixed and re-verified here. "
        "Out-of-slice observation: `ruff format --check .` fails at this pin on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py "
        "(not an M7 file; the M3 builder should format it). The M7 gate set is otherwise green. "
        "Carried rows: 136 card rows carried from round 2 because their cards.json entry and lesson page are unchanged since c737272f (seven further unchanged L05 lab cards are re-judged, see FAIL rows); "
        "21 changed entries, 10 new entries and the 8 round-2 FAIL rows were re-verified. Round-2 row ids are all kept; the six removed cards keep their ids as PASS rows whose subject no longer exists."
    ),
    "summary": "",
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for row in rows:
    counts[row["status"]] += 1
fragment["summary"] = (
    f"M7-e round 3 (pin a007712f): {len(rows)} rows (pass={counts['PASS']}, fail={counts['FAIL']}, "
    f"unverifiable={counts['UNVERIFIABLE']}). Cards: 174 entries, every entry checked this round. FAIL rows: "
    "seven L05 lab-result cards and the L05 lab sentence, all for the SIMULATED label. Lesson prose, proofs, labs and "
    "gates otherwise pass."
)
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
Path(out_path).write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "verdict", fragment["verdict"])
