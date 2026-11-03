"""Build the round-4 fragment for M7 slice e (verifier round 4, pin 4eb6788).

Carried rows copy the round-3 evidence verbatim behind the round-carry prefix; only for cards whose
cards.json entry and lesson page are byte-identical since a007712f. Re-verified rows are written here
from the evidence this round produced (outputs/ and text/ under this folder).
Run: python3 -I ledgers/M7/scripts/M7-e-r4/build_fragment_r4.py
"""
import json
import pathlib
import subprocess

ROOT = pathlib.Path.cwd()
HERE = ROOT / "ledgers/M7/scripts/M7-e-r4"
r3 = json.loads((HERE / "input_round3_fragment.json").read_text(encoding="utf-8"))
r3_rows = {r["id"]: r for r in r3["rows"]}
cards = {c["id"]: c for c in json.loads((ROOT / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))}

# Cards whose cards.json entry changed between a007712f and 4eb6788 (git diff), plus the whole L05 page subject.
CHANGED_ENTRIES = {"M7-c087", "M7-c088", "M7-c089", "M7-c093", "M7-c165", "M7-c171", "M7-c172", "M7-c182", "M7-c186"}
L05_IDS = {c for c, v in cards.items() if v["lesson"] == "L05"}
REVERIFIED = CHANGED_ENTRIES | L05_IDS

GRADE_NOTE = "re-verified in round 4 (cards.json entry changed or lesson L05 changed)"

REVERIFIED_EVIDENCE = {
    "M7-c073": "L05 0024-0026 Definition 1.1 (QP data; p = 0 is the equality-constrained case); T.",
    "M7-c074": "L05 0027-0028 Remark 1.2: x'Qx = x'Q'x, so only the symmetric part matters; answer 'No' matches; T.",
    "M7-c075": "L05 0029-0032 Lemma 1.3 expansion, gradient Qx + c, Hessian Q; proof 0034; T.",
    "M7-c076": "L05 0035-0036 Lemma 1.4 (Q PSD gives the tangent-plane bound); proof 0038 applies Lemma 1.3 with d = y - x; T.",
    "M7-c077": "L05 0042-0045 Proposition 2.1 (Q SPD, A full row rank, K nonsingular); proof 0045: Kv = 0 forces v = 0; T.",
    "M7-c078": "L05 0046-0047 Remark 2.2; recompute_r4.py block 'Remark 2.2' prints rows (1,0,1,1),(0,1,0,0),(1,0,0,0),(1,0,0,0), det K = 0, rows 3 and 4 equal; T.",
    "M7-c079": "L05 0048-0051 Theorem 2.3 (hypotheses Q SPD and A full row rank; unique minimiser over {Ax = b}); proof uses Lemma 1.3 and the first block row (0051); T.",
    "M7-c080": "L05 0053 Remark 2.4 completing-the-square identity; recompute_r4.py checks it exactly on 2000 rational points ('holds ... True'); Q = [[4,1,0],[1,3,1],[0,1,2]] from L05 0097-0100; T.",
    "M7-c081": "L05 0061-0064 Theorem 3.1 (Q PSD; x̄ in F; λ̄, μ̄ >= 0; stationarity; complementary slackness); proof 0064 uses Lemma 1.4; card's hypotheses match; T.",
    "M7-c082": "L05 0065-0066 Remark 3.2; recompute_r4.py 'Remark 3.2': f(0) = 0, f(1) = -1/2, stationarity gives mu = -1 < 0; T.",
    "M7-c083": "L05 0067-0068 Definition 3.3 (S-candidate) and the identification condition (Q SPD; rows of A and G_i, i in S, independent); T.",
    "M7-c084": "L05 0069-0072 Proposition 3.4 hypotheses (Q SPD; F midpoint convex) match the card; identity f(z) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y) at 0072; T.",
    "M7-c085": "L05 0073-0074 Remark 3.5: constraints x >= 0 linear; x'Qx = (x1+x2)^2 + x1^2 + x2^2 for Q = [[2,1],[1,2]] (expanded by hand: 2x1^2 + 2x1x2 + 2x2^2); T.",
    "M7-c086": "L05 0075-0077 Example 3.6 (x̄ = (3/2, 0), μ̄ = (0, 5/2), f = -9/4); recompute_r4.py Part B prints xhat 3/2 0 and objective -9/4; T.",
    "M7-c087": "L05 0240 prints 'x 13/19 3/19 3/19' and 0242-0243 print both residual maxima 0.0e+00; recompute_r4.py: exact x = (13/19, 3/19, 3/19), residuals exactly zero; basis 'Lab 1, Part A (SIMULATED), exact arithmetic' matches the SIMULATED label at L05 0079 and docstring 0081; C.",
    "M7-c088": "L05 0244 prints objective 0.7631578947; derivation 0305 gives 551/722; recompute_r4.py: objective 29/38 = 551/722 exactly, float 0.7631578947368, x'Qx = 43/19 = 817/361; basis SIMULATED as at 0079/0081; C.",
    "M7-c089": "L05 0248-0252 candidate lines: {} primal False; {2} primal True dual True; {1} False False; {1,2} True False; passing_candidates 1 (0252); recompute_r4.py reproduces the four rows and the single passing set {2}; basis SIMULATED; C.",
    "M7-c090": "L05 0068 ('enumerates all 2^p sets S') and 0263 ('Lab 1 uses p = 2, so four candidates'); the twin enumerates product((0,1), repeat=2), four masks; T.",
    "M7-c091": "L05 0267-0268 misconception 1: Q = diag(1,-1), f(0,t) = -t^2/2 has no minimiser; Theorem 2.3 needs Q SPD (0268); T.",
    "M7-c092": "L05 0269-0270 misconception 2: Remark 3.2 (0065-0066) and Theorem 3.1 (0061-0062) need mu̅ >= 0 and complementary slackness; T.",
    "M7-c093": "L05 0271-0272 misconception 3: gradient at x̂ is -A'λ*; λ* printed at 0241 (-36/19, 11/19); recompute_r4.py: gradient (36/19, 25/19, 47/19) equals -A'λ* and is nonzero; basis SIMULATED; C.",
    "M7-c165": "L01 0072 Example 3.3 (Q2(1,1) = 3(1,1), Q2(1,-1) = -1(1,-1), eigenvalues 3 and -1; recompute_r4.py prints Q2(1,1) = (3,3), Q2(1,-1) = (-1,1)); L01 0231-0234 Problem P3 shows a negative eigenvalue refutes convexity using only Lemma 3.1 (0046-0054, proved for every x, y and λ, with no Assumption 1) and Definition 2.1; the Assumption 1 spectral theorem (0057-0058) is not used there; recompute_r4.py gap = -1/2 for v = (1,-1), x = v, y = 0, λ = 1/2; T.",
    "M7-c166": "L05 0053 Remark 2.4 null direction v = (-2,1,1): recompute_r4.py Av = (0,0), Qv = (-7,2,3), vᵀQv = 19; F is the line x̂ + tv; Qx̂ + c = -Aᵀλ* (recompute gradient); T.",
    "M7-c171": "L05 0237 kkt_size 5 and 0239 kkt_determinant 19; recompute_r4.py: det of the 5 by 5 KKT matrix = 19; basis SIMULATED; C.",
    "M7-c172": "L05 0256-0257 grid_points 1089 and grid_points_below_candidate 0; recompute_r4.py: 33^2 = 1089 points on {k/16: 0 <= k <= 32}^2, none below -9/4; basis SIMULATED; C.",
    "M7-c182": "L05 0241 prints 'lambda -36/19 11/19'; recompute_r4.py gives the same exact values; basis SIMULATED; C.",
    "M7-c186": "L08 0036 Theorem 1.3 is stated for β >= 0 (the back states this hypothesis); L08 0216 counterexample H = 2, β = -1, r(x) = 0, r(y) = 1, B = 0: plan totals 0, -1, 1, 0 so V_0 = 1, U_1 = 1, U_0 = 0 (recompute_r4.py 'L08' block prints these); the lesson's §3 header is at 0212; the answer 'No' is supported for Theorem 1.3 only; T.",
    "M7-c198": "L05 0055 active-set definition (inequality rows holding with equality at x); T.",
}

CARD_CHECK = "card-vs-lesson: front, back, grade, basis, locator, numbers, SIMULATED label"
rows = []
for cid in sorted(cards):
    eid = "E-" + cid[3:]
    card = cards[cid]
    loc = f"course/modules/M/M7/cards.json ({cid}, lesson {card['lesson']}, grade {card['grade']})"
    if cid in REVERIFIED:
        rows.append({
            "id": eid, "check": CARD_CHECK + " (round 4)", "location": loc, "status": "PASS",
            "evidence": REVERIFIED_EVIDENCE[cid],
        })
    else:
        prev = r3_rows[eid]
        assert prev["status"] == "PASS", eid
        rows.append({
            "id": eid, "check": prev["check"], "location": loc, "status": "PASS",
            "evidence": (f"Carried from round 3 (course/modules/M/M7/{card['lesson']}.html and the cards.json entry "
                         f"{cid} byte-identical since the previous pin a007712f): " + prev["evidence"]),
        })

STALE_EVIDENCE = ("Card removed before the round-3 pin: no entry with this id in cards.json at a007712f or at 4eb6788 "
                  "(ledgers/M7/scripts/M7-e-r4/outputs/stale_ids.out). Nothing remains to verify; round-2 row kept for id continuity.")
for stale in ["M7-c010", "M7-c048", "M7-c134", "M7-c146", "M7-c180", "M7-c188"]:
    eid = "E-" + stale[3:]
    rows.append({
        "id": eid, "check": "card-vs-lesson (round-2 id; card removed before round 3)",
        "location": f"course/modules/M/M7/cards.json ({stale}: absent at 4eb6788)", "status": "PASS",
        "evidence": STALE_EVIDENCE,
    })

SCRIPTS = "ledgers/M7/scripts/M7-e-r4"
def s(rid):
    return r3_rows[rid]

rows_s = [
    {"id": "E-S01", "check": "unit gate: check_pages", "location": "course/modules/M/M7/ (check_pages.py --unit M7)",
     "status": "PASS", "evidence": f"Run at 4eb6788: 'check_pages M7: PASS' ({SCRIPTS}/outputs/gates.out)."},
    {"id": "E-S02", "check": "unit gate: check_dag, check_projects, run_labs",
     "location": "tools/check_dag.py, check_projects.py, run_labs.py --unit M7",
     "status": "PASS", "evidence": f"Run at 4eb6788: 'check_dag M7: PASS', 'check_projects M7: PASS', 'run_labs M7: PASS (11/11)' ({SCRIPTS}/outputs/gates.out)."},
    {"id": "E-S03", "check": "lab twins under python -I -W error; page code equals twin; expected block equals output",
     "location": "tests/labs/M7/lab-M7-L01-1.py .. lab-M7-L08-1.py; course/modules/M/M7/L01.html .. L08.html",
     "status": "PASS", "evidence": f"{SCRIPTS}/labcheck.py at 4eb6788: for all eight labs, page code equals twin text (trailing newline ignored): True; twin run rc 0 with empty stderr; expected block equals real output: True ({SCRIPTS}/outputs/labcheck.out)."},
    {"id": "E-S04", "check": "every number a card states recomputed independently",
     "location": "course/modules/M/M7/cards.json (all 174 cards); L05, L08 and L01 examples",
     "status": "PASS", "evidence": f"Changed and L05 cards recomputed exactly in {SCRIPTS}/recompute_r4.py (outputs/recompute_r4.out). Carried cards: the round-3 script ledgers/M7/scripts/M7-e-r3/v3_card_numbers.py re-run at 4eb6788 gives output identical to the committed round-3 output ({SCRIPTS}/outputs/r3_v3_card_numbers.out)."},
    {"id": "E-S05", "check": "every number on a card occurs in its lesson page",
     "location": "ledgers/M7/scripts/M7-e-r3/v3_card_numbers_in_lesson.py (re-run)",
     "status": "PASS", "evidence": f"Re-run at 4eb6788 ({SCRIPTS}/outputs/r3_v3_card_numbers_in_lesson.out): identical to the round-3 output. The one flagged token '00' (card M7-c130) is a regex artefact of 'W400' and 'V_0(400)'; the value 400 occurs in L07 0197-0201 (the W400 column)."},
    {"id": "E-S06", "check": "banned phrases and process words in cards",
     "location": "course/modules/M/M7/cards.json",
     "status": "PASS", "evidence": f"Re-run of ledgers/M7/scripts/M7-e-r3/v3_card_scan.py at 4eb6788 ({SCRIPTS}/outputs/r3_v3_card_scan.out): the ten hits are mathematical ellipses in sequences (for example (a_t, ..., a_{{H-1}}), 'c'_1 + ... + c'_4') and the words 'round' and 'around'; no banned phrase in the sense of BUILDER_RULES 1.3. Re-read for this round's changed cards: none."},
    {"id": "E-S07", "check": "duplicates and near-duplicates in cards",
     "location": "course/modules/M/M7/cards.json",
     "status": "PASS", "evidence": f"{SCRIPTS}/outputs/r3_v3_card_scan.out: 174 unique ids; no exact duplicate fronts (round-4 check); no identical backs (the only 60-character back prefix shared, c042 and c061, states different theorems). The 32 near-duplicate front pairs (Jaccard >= 0.5) were re-read from their fronts: each pair asks a different quantity. The pair M7-c122 (L07, undiscounted J_t) and M7-c142 (L08, discounted J_t with β) is distinct content. The round-3 pair M7-c009/M7-c165 is gone because c165 changed."},
    {"id": "E-S08", "check": "grade and basis rules (BLUEPRINT 3; BUILDER_RULES 7)",
     "location": "cards.json grades and basis fields",
     "status": "PASS", "evidence": f"{SCRIPTS}/outputs/r3_v3_card_scan.out: 126 T cards carry no basis; 48 C cards all carry a basis; 'C cards without basis: []'; 'T cards carrying basis: []'; 'C cards from SIMULATED-lab lessons without SIMULATED in basis: []'."},
    {"id": "E-S09", "check": "coverage: each definition, theorem, proposition, lemma, remark, misconception and key-results row has a card",
     "location": "course/modules/M/M7/L01..L08.html sections 4-7 (key-results tables)",
     "status": "PASS", "evidence": "Round-3 coverage check carried for lessons whose text is unchanged (round-3 row E-S09). Re-checked for L05 this round: Lemma 1.3 (c075), Lemma 1.4 (c076), Prop 2.1 (c077), Remark 2.2 (c078), Thm 2.3 (c079), Remark 2.4 (c080, c166), Thm 3.1 (c081), Remark 3.2 (c082), Def 3.3 (c083), Prop 3.4 (c084), Remark 3.5 (c085), Example 3.6 (c086), the three L05 misconceptions (c091, c092, c093), and the Lab 1 results (c087-c089, c171, c172, c182). L08 Theorem 1.4 is covered by c145; L01 Example 3.3 non-convexity by c165."},
    {"id": "E-S10", "check": "theorem and proposition cards carry the lesson's hypotheses",
     "location": "theorem-type cards of L05 (c077, c079, c081, c084) and L08 (c186)",
     "status": "PASS", "evidence": "L05 c077 (Q SPD, A full row rank) matches 0042-0043; c079 (Q SPD, A full row rank) matches 0048-0049; c081 (Q PSD, mu̅ >= 0, complementary slackness) matches 0062; c084 (Q SPD, midpoint-convex F) matches 0070. L08 c186 states the β >= 0 hypothesis of Theorem 1.3 (L08 0036). Other theorem cards carried from round 3."},
    {"id": "E-S11", "check": "round-2 failing rows (M7-c012, c049, c050, c063, c170, c173, c178, c189) stay fixed",
     "location": "cards.json entries listed",
     "status": "PASS", "evidence": "Carried from round 3 (the eight card entries and their lesson pages are byte-identical since a007712f; none appears in the git diff of cards.json). Their basis fields carry '(SIMULATED)' in the current cards.json (for example M7-c012 'Lab 1 (SIMULATED), exact count on the 25-point grid')."},
    {"id": "E-S12", "check": "lab SIMULATED labels in the lesson pages that cards cite",
     "location": "course/modules/M/M7/L01..L08.html lab hypotheses and docstrings",
     "status": "PASS", "evidence": f"Round 4 grep of SIMULATED per lesson (text/L0n.txt): L01 0078; L02 0075; L03 0064 and 0074; L04 0061; L05 0079 and 0081; L06 0063, 0065, 0184, 0239, 0360; L07 0075 and 0077; L08 0072 and 0074. Every basis that cites a lab carries SIMULATED. L05 now complies (see E-S13)."},
    {"id": "E-S13", "check": "SIMULATED label consistency for the L05 lab (hand-chosen integers)",
     "location": "course/modules/M/M7/L05.html lab hypothesis line 0079 and docstring line 0081; tests/labs/M7/lab-M7-L05-1.py docstring",
     "status": "PASS", "evidence": "Round-3 FAIL is fixed at 4eb6788. L05 text 0079 reads 'The inputs are SIMULATED: small integers chosen by hand as illustrative values for this lab, not data'; the embedded docstring (0081) and the twin docstring both begin with 'SIMULATED:' (labcheck.out: page code equals twin). The seven L05 lab-result cards (c087, c088, c089, c093, c171, c172, c182) now carry '(SIMULATED)' in basis (cards.json diff, 9 hunks). Round-3 judgement adopted: L01 and L03 label the same kind of input SIMULATED."},
    {"id": "E-S14", "check": "notation against notation/notation.json",
     "location": "notation/notation.json; cards and L05/L08 symbols",
     "status": "PASS", "evidence": "notation.json registers T, Φ, γ3, γ4, R*, R^{e*}, R_f and \\mathbb{Q}, and macros; the symbols on the nine changed cards (Q, Q2, c, A, B, H, V_0, U_0, β, λ, μ) do not reuse any registered meaning. β, μ and λ are lesson-local (notation.json 'about' says alpha, beta, gamma, mu, sigma are local). notation/ is byte-identical since a007712f."},
    {"id": "E-S15", "check": "DAG: cards use only prerequisite or own-unit concepts",
     "location": "cards.json (concept words) against the M7 prerequisite closure in plans/M7-build-plan.md section 2",
     "status": "PASS", "evidence": f"Changed cards: c165 uses convex function (L01) and eigenvalues (M3, in closure); c186 uses the Bellman equation and discount factor (L08). check_dag M7: PASS ({SCRIPTS}/outputs/gates.out)."},
    {"id": "E-S16", "check": "atomicity: one fact per card (BUILDER_RULES 7)",
     "location": "cards.json fronts and backs of the changed cards",
     "status": "PASS", "evidence": "Changed cards each test one claim: c165 (Q2 is not convex, with its eigenvalue reason), c186 (Theorem 1.3 fails at β = -1), c087-c093 and c171-c182 (one printed lab value each). c088 gives one objective value with its decomposition."},
    {"id": "E-S17", "check": "registry keys cited by cards",
     "location": "cards.json cite field (absent)",
     "status": "PASS", "evidence": "No card has a 'cite' key (keys: back, basis, front, grade, id, lesson). L05 0400 and L08 0343 state that the lesson cites no outside source; no registry key is used by slice e."},
    {"id": "E-D01", "check": "delta hunk: L05.html lab section (lines 180-190 of the page at 4eb6788)",
     "location": "course/modules/M/M7/L05.html lines 0079 and 0081 (hypothesis and embedded docstring)",
     "status": "PASS", "evidence": f"Changed hunk read in full (git diff a007712f 4eb6788). Embedded code equals tests/labs/M7/lab-M7-L05-1.py (labcheck.out); expected block equals the real output of the twin under python -I -W error (labcheck.out: True); the only output-bearing lines (0239-0258) are unchanged; page_smoke L05 PASS ({SCRIPTS}/outputs/page_smoke_L05.out)."},
    {"id": "E-D02", "check": "delta hunk: tests/labs/M7/lab-M7-L05-1.py docstring (Python twin, ruff and mypy strict)",
     "location": "tests/labs/M7/lab-M7-L05-1.py",
     "status": "PASS", "evidence": f"ruff check tests/labs/M7: 'All checks passed!'; ruff format --check tests/labs/M7: '11 files already formatted'; mypy --no-incremental on the file: 'Success: no issues found in 1 source file' ({SCRIPTS}/outputs/twin_lint_L05.out); run under python -I -W error: rc 0, empty stderr (labcheck.out)."},
    {"id": "E-D03", "check": "page_smoke for the eight lesson pages (lessons alone and together)",
     "location": "course/modules/M/M7/L01.html .. L08.html",
     "status": "PASS", "evidence": f"tools/page_smoke.py --unit M7 --pages L01 .. L08: each page PASS and 'page_smoke M7: PASS' ({SCRIPTS}/outputs/page_smoke_L01-L08.out); L05 alone: PASS ({SCRIPTS}/outputs/page_smoke_L05.out)."},
    {"id": "E-D04", "check": "relevant pytest subset (labs, run_labs, page checks, curriculum, docs figures)",
     "location": "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py, test_docs_figures.py",
     "status": "PASS", "evidence": f"pytest exit 0, '381 passed in 44.38s' ({SCRIPTS}/outputs/pytest_subset.out)."},
]

fragment = {
    "unit": "M7",
    "slice": "e",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-e, round 4 (did not build M7; delta from a007712f read hunk by hunk; every changed card and every L05 card re-verified; every other card carried)",
    "pin": "4eb6788",
    "base": "a007712f (round-3 pin). Delta for slice e: course/modules/M/M7/L05.html (hypothesis line 0079 and docstring 0081 gain a SIMULATED label; one line added); tests/labs/M7/lab-M7-L05-1.py (docstring); course/modules/M/M7/cards.json (9 entries: M7-c087, c088, c089, c093, c165, c171, c172, c182, c186). L01-L04, L06-L08 HTML and notation/ are byte-identical to a007712f.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-M7-e",
    "scratch": "ledgers/M7/scripts/M7-e-r4/text/ (lesson text with line numbers, regenerable by ledgers/M7/scripts/M7-e-r4/extract_text.py)",
    "verified_at": "2026-11-03T14:21:08+00:00",
    "verdict": "PASS",
    "rows": rows + rows_s,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Carried rows (146 cards) are byte-identical in cards.json and their lesson page since a007712f; their round-3 evidence is carried with the prefix. "
        "Re-verified in full this round: all 26 L05 cards (every locator now uses the L05 text numbering at 4eb6788, which is one line longer after line 0080), "
        "the 2 other changed cards (c165 L01, c186 L08). Round-3 FAIL rows (E-c087, E-c088, E-c089, E-c093, E-c171, E-c172, E-c182, E-c186, E-S13) are re-verified and now PASS. "
        "Observation, not a FAIL: L05 line 0077 says 'the data of Remark 2.4' while line 0079 says the inputs are 'not data'; 'data' in 0077 means the problem data (Q, c, A, b), so the SIMULATED label is not contradicted, but a reader could take the two sentences as conflicting. Optional wording fix: 'the problem data of Remark 2.4'. "
        "Not checked: verify_refs (no card or lesson on this slice cites a registry key); the rendered card deck course/review.html; a visual check of the lessons beyond page_smoke; the L02-L04, L06-L08 card and prose text, which is carried from round 3 by the byte-identity rule and not re-read this round; the M7-c178/c189 and other round-2 card texts beyond their unchanged state."
    ),
    "summary": (
        "M7-e round 4 (pin 4eb6788): delta-verified. Rows: "
        f"{len(rows) + len(rows_s)} (cards 180 incl. 6 removed-id rows; 17 unit rows E-S01..E-S17; 4 delta rows E-D01..E-D04). "
        "All 9 round-3 non-PASS rows (E-c087, E-c088, E-c089, E-c093, E-c171, E-c172, E-c182, E-c186, E-S13) are fixed and re-verified. "
        "Lab twin, expected blocks, page_smoke, check_pages, check_dag, check_projects, run_labs, ruff, mypy and the pytest subset all pass at 4eb6788."
    ),
}

out = HERE.parent.parent / "M7-e.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(fragment["rows"]))
