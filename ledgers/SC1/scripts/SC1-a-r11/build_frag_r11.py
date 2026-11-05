"""Builds the round-11 fragment ledgers/SC1/SC1-a.json from the round-10 fragment (round 11, slice a).

Every row id of round 10 is kept. A row is FRESH when its cited subject was re-read or re-run in round 11
(index.html, L01-L03, the three twins, cards L01-L03, the gates). A row that cites only files byte-identical
since the round-10 pin (00a8479) is carried with the required prefix. Overrides carry the round-11 verdicts.
"""

import json
import re

PREV = "/Users/billyribeiro/.fanout/frags/E-SC1-a.round10.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a/ledgers/SC1/SC1-a.json"
S = "ledgers/SC1/scripts/SC1-a-r11/"
PIN = "11d7077a290f7960b183d3a5a6631af4773888f9"
PREV_PIN = "00a84795f276456fce19d4181373cc4efba11a36"

prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

OV = {}  # id -> dict(status, evidence, fix?, check?, location?)


def ov(i, status, evidence, fix=None, check=None, location=None):
    d = {"status": status, "evidence": evidence}
    if fix:
        d["fix"] = fix
    if check:
        d["check"] = check
    if location:
        d["location"] = location
    OV[i] = d


# ---- gates and commands run in round 11 -------------------------------------------------------------
ov("SC1a-gate-check-pages", "PASS",
   "Round 11: .venv/bin/python tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (" + S + "check_pages_SC1.out).")
ov("SC1a-gate-check-dag", "PASS",
   "Round 11: tools/check_dag.py --unit SC1 -> PASS (" + S + "check_dag_SC1.out); tools/check_dag.py --all -> exit 0, every unit PASS (" + S + "check_dag_all.out).")
ov("SC1a-gate-run-labs", "PASS",
   "Round 11: tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0 (" + S + "run_labs_SC1.out); page code equals twin and expected block equals output for L01-L03.")
ov("SC1a-gate-page-smoke", "PASS",
   "Round 11: tools/page_smoke.py --unit SC1 --pages modules/SC/SC1/<page>.html, one page per run, for index, L01, L02, L03: each 'page_smoke SC1: PASS', exit 0 (" + S + "page_smoke_index.out, page_smoke_L01.out, page_smoke_L02.out, page_smoke_L03.out).")
ov("SC1a-gate-lint-types-tests", "PASS",
   "Round 11: ruff check and ruff format --check on tests/labs/SC1 and tests/test_labs.py: 'All checks passed', '11 files already formatted' (" + S + "ruff.out); mypy --no-incremental (whole project): 'Success: no issues found in 385 source files' (" + S + "mypy.out); pytest -k SC1: 11 passed (" + S + "pytest_SC1.out).")
ov("SC1a-gate-verify-refs", "PASS",
   "Round 11: tools/verify_refs.py --offline -> '560 entries, 0 problems' (" + S + "verify_refs_offline.out); tools/verify_refs.py --unit SC1 (live network run) -> '1 of 560 entries, 0 problems' (" + S + "verify_refs_live_SC1.out). The one SC1 entry shreve2004stochastic (openlibrary, ISBN 9781475742961) resolves; index.html:182 cites it by key.")
ov("SC1a-r7-gate-check-projects", "PASS",
   "Round 11: tools/check_projects.py --unit SC1 -> 'check_projects SC1: PASS', exit 0 (" + S + "check_projects_SC1.out).")
ov("SC1a-r7-katex-render", "PASS",
   "Round 11: page_smoke.py (" + S + "page_smoke_index.out, page_smoke_L01.out, page_smoke_L02.out, page_smoke_L03.out) reports zero unrendered math on each of the four pages in both themes and both widths.")
ov("SC1a-r10-cmd-check_pages", "PASS",
   "Round 11 re-run at 11d7077: check_pages.py --unit SC1 PASS (" + S + "check_pages_SC1.out) for index, L01-L03, cards.json, project.html.")
ov("SC1a-r10-cmd-check_projects", "PASS",
   "Round 11 re-run at 11d7077: check_projects.py --unit SC1 PASS (" + S + "check_projects_SC1.out).")
ov("SC1a-r10-cmd-verify_refs", "PASS",
   "Round 11 re-run at 11d7077: verify_refs.py --offline (" + S + "verify_refs_offline.out) and live --unit SC1 (" + S + "verify_refs_live_SC1.out), both 0 problems.")
ov("SC1a-r10-cmd-ruff-mypy", "PASS",
   "Round 11 re-run at 11d7077: ruff check and format --check on tests/labs/SC1 and tests/test_labs.py (" + S + "ruff.out); mypy --no-incremental (" + S + "mypy.out).")
ov("SC1a-r10-cmd-pytest-SC1", "PASS",
   "Round 11 re-run at 11d7077: pytest -k SC1 -> 11 passed, exit 0 (" + S + "pytest_SC1.out).")
ov("SC1a-r10-cmd-twins-python-I-W-error", "PASS",
   "Round 11: tests/labs/SC1/lab-SC1-L01-1.py, L02-1, L03-1 each under python -I -W error from a scratch directory: exit 0, stderr 0 bytes (" + S + "twin_L01.out, twin_L02.out, twin_L03.out and .err); also under the .venv CPython 3.14.8 (" + S + "twin_venv_L01.out, twin_venv_L02.out, twin_venv_L03.out).")
ov("SC1a-r10-cmd-page_smoke", "PASS",
   "Round 11 re-run, one page per run at 11d7077: page_smoke PASS for index, L01, L02, L03 (" + S + "page_smoke_index.out, page_smoke_L01.out, page_smoke_L02.out, page_smoke_L03.out).")
ov("SC1a-r10-cmd-run_labs", "PASS",
   "Round 11 re-run at 11d7077: run_labs --unit SC1 -> 'run_labs SC1: PASS (11/11)' (" + S + "run_labs_SC1.out).")
ov("SC1a-lab-L01-twin", "PASS",
   "Round 11: tests/labs/SC1/lab-SC1-L01-1.py run under python -I -W error (" + S + "twin_L01.out, exit 0, stderr 0 bytes) matches the expected block at course/modules/SC/SC1/L01.html:202-207 line for line (run_labs PASS, " + S + "run_labs_SC1.out); the 81 of 81 and 15 of 15 counts recomputed (" + S + "numeric_checks_r11.out).")
ov("SC1a-lab-L02-twin", "PASS",
   "Round 11: tests/labs/SC1/lab-SC1-L02-1.py under python -I -W error (" + S + "twin_L02.out, exit 0) matches the expected block at L02.html:266-277 (run_labs PASS). The 216 count recomputed by enumeration (" + S + "numeric_checks_r11.out: pairs 36, cases 216).")
ov("SC1a-lab-L03-twin", "PASS",
   "Round 11: tests/labs/SC1/lab-SC1-L03-1.py under python -I -W error (" + S + "twin_L03.out, exit 0) matches the expected block at L03.html:218-252 (run_labs PASS).")
ov("SC1a-r10-lab-L01-L02-L03-claims", "PASS",
   "Round 11: docstrings tests/labs/SC1/lab-SC1-L01-1.py:1-9, lab-SC1-L02-1.py:1-8 and lab-SC1-L03-1.py:1-14 re-read; each claim (exact Fraction arithmetic; SIMULATED label; seeded; closed-form match) is in the code (grep and output).")
ov("SC1a-r4-twin-timing-and-purity", "PASS",
   "Round 11: the three twins are standard library only (imports read at lab top), run under -I -W error with no stderr, and run_labs enforces the twin time limit and reported PASS (" + S + "run_labs_SC1.out).")
ov("SC1a-r10-lab-mutants-4of4", "PASS",
   "Round 11 re-run: " + S + "r10_mutants_rerun_r11.py and .out: mut-L01-1, mut-L02-1, mut-L03-1 and mut-L03-2 each run under python -I -W error (rc 0, stderr 0 bytes) and each output differs from the page expected block, so 4 of 4 KILLED. Six further lab-claim mutants are in row SC1a-r11-lab-mutants-6of6.")

# ---- new round-11 rows ---------------------------------------------------------------------------------
NEW = {}


def new(i, check, location, status, evidence, fix=None):
    d = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        d["fix"] = fix
    NEW[i] = d


new("SC1a-r11-A1b-literal-false", "Assumption A1(b), second sentence, is true as stated (used by Remark 1.3 and Lemma 2.3)",
    "course/modules/SC/SC1/L01.html:75 (A1(b), second sentence); counterexample script " + S + "a1b_counterexample.py, output " + S + "a1b_counterexample.out",
    "FAIL",
    "The second sentence reads: 'A vector whose coordinates are such combinations is multivariate normal.' Read literally, with no common family, it is false. Take Z ~ N(0,1) and eps a fair sign independent of Z, and W = eps*Z. W is N(0,1) (script output: Var(W) 1.000). Each coordinate is a one-term linear combination of an independent normal family, so the sentence applies to the vector (Z, W). But Z + W = (1+eps)Z is 0 with probability 1/2 (output: P(Z+W=0) 0.4985), and a normal variable of positive variance has no atom, so (Z, W) is not multivariate normal.",
    fix="Restate L01.html:75 so the coordinates come from one common family: 'A vector each of whose coordinates is a finite linear combination of one common family of independent normal variables is multivariate normal.' Make the same change in card SC1-c207 (cards.json). Remark 1.3 (L01.html:112) and Lemma 2.3 (L02.html:137) apply it only to combinations of one family (the increments Delta_i, and D_j with eta_j), so their proofs stand after the restatement.")
new("SC1a-r11-lab-mutants-6of6", "Lab twins: the stated counts and checks test what the page says (mutation check, demonstrations only)",
    "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py against the expected blocks in L01.html:202-207, L02.html:266-277, L03.html:218-252; " + S + "lab_mutants_r11.py, " + S + "lab_mutants_r11.out",
    "PASS",
    "Baselines match the expected blocks (rc 0, stderr 0 bytes). Six mutants written into ledgers/SC1/mutants/SC1-a-r11/ and each run under -I -W error: m1 coverage sums up to max(i,j) (KILLED; the example covariance line prints 5/8 instead of 1/4); m2 hat support radius doubled (KILLED, dyadic count prints 36 of 216); m3 grid depth 3 (KILLED, grid-supremum line prints False); m4 standard error divisor n (KILLED, z for N=2 prints 2.40 not 2.39); m5 exact sum drops the first interval (KILLED, closed form False); m6 dyadic piece length halved (KILLED, sums print 1/2). Lab mutation is a demonstration check (ruling), so this row is a check of the page's stated counts.")
new("SC1a-r11-numbers-recomputed", "Every number recomputed by an independent script (round 11)",
    S + "numeric_checks_r11.py, " + S + "numeric_checks_r11.out; " + S + "concept_check_r11.out",
    "PASS",
    "L02 E3 (L02.html:421): unrounded level-1 sup 0.11658934 from the seeded draw (seed 20260101, second gauss draw); 2 x sup = 0.2331787 rounds to 0.233179; doubling the printed 0.116589 gives 0.233178; sqrt(4 log 2) = 1.665109 and half is 0.832555. L03 key-results row (L03.html:398): 16 gaps printed se / (H sqrt(2/N)/20) - 1, largest +13.21% at H=2, N=1, all within 14 percent. L03 E2 (L03.html:350) 2^4(4*64-1)/(3*512) = 2.65625; L03 E3 (L03.html:357) 0.0125; quiz 0.625 (L03.html:434). Hub placement (index.html:74) 7/9 = 77.8%, 8/9 = 88.9%. Rung-2 count 29 (project.html:206) by enumeration of 2^6 walks with maximum >= 2; rung-1 count 2 (n=2, a=1). L02 216 cases over 36 pairs; L01 15 and 81 counts; L01 E1 piece 3/64 and sum 3/4.")
new("SC1a-r11-concept-list-exact", "Hub prerequisite list (index.html:58-68) equals the concepts used across the module",
    "course/modules/SC/SC1/index.html:58-68; L01-L08 and project.html data-concept targets; " + S + "concept_check_r11.py, " + S + "concept_check_r11.out",
    "PASS",
    "Script output: 'used, not in hub list, not SC1-defined: []' and 'hub list, not used anywhere in module: []'; hub list size 24; 8 SC1-defined concepts used. conditional-expectation-l2 is in the list at index.html:66 and defined in M6 (curriculum/01-foundations.yaml:278), with an anchor in concepts.html.")
new("SC1a-r11-hours-and-projects", "Hub hours: 72 lesson + 28 project = 100 (curriculum SC1 hours 100)",
    "course/modules/SC/SC1/L01.html-L08.html data-hours; index.html:29, :39-42, :150; project.html:33 and :280; curriculum/03-markets.yaml SC1 hours 100",
    "PASS",
    "data-hours per lesson: 9 each for L01-L08 (" + S + "concept_check_r11.out), total 72; project.html:33 hours-project=\"28\" and :280 '28 of the module's 100'; index.html:29 data-hours-lessons=72, data-hours-project=28; curriculum SC1 hours 100 and tier M (curriculum/03-markets.yaml:505-).")
new("SC1a-r11-cards-scan", "Retrieval cards: no duplicates, card numbers appear in the lesson, hypotheses read",
    "course/modules/SC/SC1/cards.json (208 cards); " + S + "cards_check_r11.py, " + S + "cards_check_r11.out",
    "PASS",
    "208 cards; no duplicate id, front or back; every number in an L01-L03 card back appears in its lesson. Hypotheses of the L01-L03 cards read in full (script output lists them). Card defects are recorded in rows SC1a-r10-cards-dup-hypotheses and SC1a-r11-A1b-literal-false.")
new("SC1a-r11-delta-read", "Round-11 delta read hunk by hunk (index.html, L01.html, references.json, cross-referenced L04/L05/project hunks)",
    "git diff 00a84795 11d7077a -- course/modules/SC/SC1/index.html course/modules/SC/SC1/L01.html references/references.json (and L04, L05, project.html hunks)",
    "PASS",
    "index.html: objective 3 (L03), From-M6 list (adds conditional-expectation-l2), placement item Pq4 explanation, Pq8 'for a standard Brownian motion, t>0 and a>0', L03 and L05 cards. L01.html: why-it-matters (:51, Cov = min(s,t) via shared increments), Standard paragraph (:67), A1 block title and parts (:71-80; A1(b) is the false sentence, row SC1a-r11-A1b-literal-false), canon item 1 Bor and Leb definitions (:215). All hunks read; the only change in the L04/L05/project hunks that a hub or slice-a row cites is the test count and the L04 concept link (checked).")
new("SC1a-r11-twins-venv-314", "Lab twins run under the pinned CPython (3.14) with -I -W error",
    "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py; " + S + "twin_venv_L01.out, twin_venv_L02.out, twin_venv_L03.out",
    "PASS",
    "Each twin: .venv/bin/python (CPython 3.14.8) -I -W error: exit 0 (twin_venv_L0{1,2,3}.out ends 'exit=0').")

# ---- overrides on previously-listed rows -----------------------------------------------------------
ov("SC1a-hub-concept-list", "PASS",
   "Round 11: the round-10 FAIL is fixed. index.html:66 From-M6 list now includes conditional-expectation-l2 (the concept L04.html:37 links). The OST entry is gone and no SC1 page names it. Exact match of the hub list and module usage (row SC1a-r11-concept-list-exact, " + S + "concept_check_r11.out). check_dag PASS (" + S + "check_dag_SC1.out).")
ov("SC1a-r10-card-L05-ck-wording", "PASS",
   "Round 11: the round-10 FAIL is fixed. index.html:156 now reads 'the Chapman-Kolmogorov identity proved by completing the square'. L05.html:7 and :52 say completing the square, Lemma 2.2 at L05.html:135 is '(completing the square)', and the table at L05.html:420 says 'Proved in §2 by completing the square'. grep -c convolution L05.html = 0.")
ov("SC1a-r10-A1-attribution-M4", "PASS",
   "Round 11: the round-10 FAIL is fixed by the second option of its fix. L01.html:71-72 block title is 'Assumption A1 (standard facts, stated without proof)' with no source name, and L01.html:80 says the page 'cites no source for them'. No M4 attribution remains on the A1 block. The defect in part (b) is row SC1a-r11-A1b-literal-false.")
ov("SC1a-attrib-L01-A1-parts", "PASS",
   "Round 11 at 11d7077: A1 carries no source attribution (L01.html:71-80). Parts (a), (c), (d), (e) are stated as standard facts without proof; each is a true statement: (a) product rule for integrable independent variables; (c) uncorrelated coordinates of a jointly normal vector are independent; (d) pointwise limit on a measurable event is measurable; (e) grouping of independent families. Part (b) is false as stated and is recorded in row SC1a-r11-A1b-literal-false. Line 37 names M4 and M6 as the source of the prerequisite concepts, not of A1 parts.")
ov("SC1a-math-L01-remark1.3", "FAIL",
   "L01.html:102-113: Remark 1.3 (H2) 'Assuming A1(b) and A1(a)'; proof L01.html:112 applies A1(b) to the vector (B_t1,...,B_tr), whose coordinates are combinations of the one independent family Delta_1..Delta_r (D3, D2). The intended reading of A1(b) covers this, and the covariance step uses Proposition 1.2 (A1(a)), which is correct. But the literal second sentence of A1(b) that the proof cites is false (row SC1a-r11-A1b-literal-false; " + S + "a1b_counterexample.out). A proof graded T that cites a false assumption is not complete.",
   fix="Restate A1(b) as given in row SC1a-r11-A1b-literal-false (L01.html:75). No other change to the proof is needed.")
ov("SC1a-math-L02-lemma2.3-arithmetic", "FAIL",
   "L02.html:121-124: Lemma 2.3 is graded T, with (H2) 'Assuming A1(b), A1(c) and A1(e)'. Its proof (L02.html:137-139) needs two further facts that are not in (H2): (i) variance additivity for independent summands, Var(U_j) = (1/4) Var(D_j) + c^2 Var(eta_j) and Var of each dyadic sum (L02.html:137, :139); (ii) Cov(D_j, eta_j) = 0, for the zero covariance Cov(U_j,V_j) = (1/4)2^-n - c^2 = 0 (L02.html:138). Both are A1(a) (independent integrable variables have E[XY] = E X E Y). Remark 2.6 cites A1(a) for the same additivity step (L02.html:315) and Lemma 2.3 does not. The arithmetic itself is correct: c = 2^(-(n+2)/2), c^2 = 2^(-(n+2)), Var(U_j) = 2^(-(n+1)), covariance 0 (checked by hand; problem M3 at L02.html:369-371 gives 1/4 for n=1).",
   fix="Add A1(a) to (H2) at L02.html:124 and to the key-results row at L02.html:460; in the proof, cite A1(a) at L02.html:137 (variance of the sum) and at :138 (cross term Cov(D_j, eta_j) = 0). Update cards SC1-c026, SC1-c027 and SC1-c028 (cards.json) to list A1(a).")
ov("SC1a-r10-cards-dup-hypotheses", "FAIL",
   "cards.json: 208 cards, no duplicate id, front or back, and every number in an L01-L03 card appears in its lesson (" + S + "cards_check_r11.out). Hypotheses: SC1-c026 (Lemma 2.3) lists 'assuming A1(b), A1(c) and A1(e)', omitting A1(a) that its proof uses (row SC1a-math-L02-lemma2.3-arithmetic). SC1-c207 restates A1(b) with the false literal sentence (row SC1a-r11-A1b-literal-false). SC1-c008 and SC1-c219 (Remark 1.3) carry the same A1(b) dependency.",
   fix="Edit cards.json: SC1-c026, SC1-c027, SC1-c028 list A1(a) as well as A1(b), A1(c), A1(e); SC1-c207 gives the restated A1(b). Regenerate nothing else; these cards are not generated.")
ov("SC1a-hub-assumption-promise", "FAIL",
   "index.html:69 promises that a fact a lesson uses from a prerequisite is 'stated as a numbered Assumption ..., with the prerequisite it comes from'. L02.html:93 (Assumption 2.1) and A2 comply. L01.html:71-80 (A1) names no prerequisite, and L01.html:80 states the page 'cites no source for them'. So the convention and the lesson disagree for A1; index.html:33 and :54 do not resolve it.",
   fix="Edit index.html:69 to: '... the fact is stated as a numbered Assumption in the lesson where it first appears, with the prerequisite it comes from, or, for a standard fact that the lesson cites to no source, labelled as such (Lesson 1, A1).' Alternatively name M4 and M6 per part at L01.html:71, but only where that prerequisite states the part.")

ov("SC1a-r8-links-anchors", "PASS",
   "Round 11 re-run: " + S + "links_anchors_r11.py and .out: 83 anchor hrefs plus 24 asset references (link, script, img) = 107 local references across index.html, L01.html, L02.html and L03.html; all resolve, 0 broken (fragment and anchor).")
ov("SC1a-r10-cmd-check_dag", "PASS",
   "Round 11 re-run at 11d7077: tools/check_dag.py --all (" + S + "check_dag_all.out): 27 unit lines, each 'check_dag X: PASS', exit 0; SC1 PASS (" + S + "check_dag_SC1.out).")

CARRY = {
    "SC1a-r4-seed-sweep-L02": "course/modules/SC/SC1/L02.html and tests/labs/SC1/lab-SC1-L02-1.py",
    "SC1a-r8-lab-mutants": "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
}

# ---- assemble ------------------------------------------------------------------------------------------
CORE_HINTS = ["index.html", "L01.html", "L02.html", "L03.html", "lab-SC1-L0", "cards.json", "tests/labs", "gate",
              "notation", "BUILDER_RULES", "references.json", "verify_refs", "check_", "page_smoke"]
OTHER_HINTS = ["L04.html", "L05.html", "L06.html", "L07.html", "L08.html", "project.html", "BLUEPRINT", "curriculum/",
               "grader/"]
rows = []
stats = {"fresh": 0, "carried": 0, "override": 0}
for r in prev["rows"]:
    i = r["id"]
    if i in OV:
        o = dict(r)
        o.update(OV[i])
        o.setdefault("fix", "" if o["status"] == "PASS" else o.get("fix", ""))
        if o["status"] == "PASS":
            o.pop("fix", None)
        rows.append(o)
        stats["override"] += 1
        continue
    if i in CARRY:
        o = dict(r)
        o["evidence"] = "Carried from round 10 (" + CARRY[i] + " byte-identical since the previous pin 00a8479): " + r["evidence"]
        rows.append(o)
        stats["carried"] += 1
        continue
    loc = r["location"] + " " + r["evidence"]
    core = any(h in loc for h in CORE_HINTS)
    other = [h for h in OTHER_HINTS if h in loc]
    o = dict(r)
    if core:
        o["evidence"] = ("Round 11 FRESH (index.html, L01-L03, the twins and cards L01-L03 re-read line by line at 11d7077; "
                         "gates re-run, outputs in " + S + "): " + r["evidence"])
        if other:
            o["evidence"] += (" The part citing " + ", ".join(other) +
                              " is carried from round 10 (byte-identical since the previous pin 00a8479, or the cited lines unchanged in the fix commit 11d7077).")
        stats["fresh"] += 1
    else:
        files = ", ".join(other) if other else "cited files"
        o["evidence"] = ("Carried from round 10 (" + files + " byte-identical since the previous pin 00a8479, cited lines unchanged in 11d7077): " + r["evidence"])
        stats["carried"] += 1
    rows.append(o)

for i, d in NEW.items():
    rows.append(d)
    stats["override"] += 1

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing_prev = [i for i in prev_rows if i not in ids]
assert not missing_prev, missing_prev

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

mutants = [
    {"id": "SC1a-r10-lab-mut1-L01-width", "description": "lab-SC1-L01-1 (round 10 mut-L01-1): dyadic width t/2**(n+1); sums print 1/2.", "killed_by": "exact diff vs expected block (" + S + "r10_mutants_rerun_r11.out)"},
    {"id": "SC1a-r10-lab-mut2-L02-scale", "description": "lab-SC1-L02-1 (round 10 mut-L02-1): level scale changed; grid-supremum line prints False.", "killed_by": "exact diff vs expected block (" + S + "r10_mutants_rerun_r11.out)"},
    {"id": "SC1a-r10-lab-mut3-L03-se-divisor", "description": "lab-SC1-L03-1 (round 10 mut-L03-1): standard error divides by n+1; z for N=2 prints 2.40.", "killed_by": "exact diff vs expected block (" + S + "r10_mutants_rerun_r11.out)"},
    {"id": "SC1a-r10-lab-mut4-L03-exact-offset", "description": "lab-SC1-L03-1 (round 10 mut-L03-2): exact t-squared sum offset; closed-form match prints False.", "killed_by": "exact diff vs expected block (" + S + "r10_mutants_rerun_r11.out)"},
    {"id": "SC1a-r11-lab-m1", "description": "lab-SC1-L01-1: covariance sums increments up to max(i,j) instead of min(i,j).", "killed_by": "exact diff vs expected block (" + S + "lab_mutants_r11.out)"},
    {"id": "SC1a-r11-lab-m2", "description": "lab-SC1-L02-1: hat support radius 2**(-(m-1)) instead of 2**(-m).", "killed_by": "exact diff vs expected block (" + S + "lab_mutants_r11.out)"},
    {"id": "SC1a-r11-lab-m3", "description": "lab-SC1-L02-1: grid depth 3 misses hat centres of level 4 and above.", "killed_by": "exact diff vs expected block (" + S + "lab_mutants_r11.out)"},
    {"id": "SC1a-r11-lab-m4", "description": "lab-SC1-L03-1: standard error divides by n instead of n-1.", "killed_by": "exact diff vs expected block (" + S + "lab_mutants_r11.out)"},
    {"id": "SC1a-r11-lab-m5", "description": "lab-SC1-L03-1: exact t-squared sum drops the first interval.", "killed_by": "exact diff vs expected block (" + S + "lab_mutants_r11.out)"},
    {"id": "SC1a-r11-lab-m6", "description": "lab-SC1-L01-1: dyadic piece length t/2**(n+1) instead of t/2**n.", "killed_by": "exact diff vs expected block (" + S + "lab_mutants_r11.out)"},
]

frag = {
    "unit": "SC1",
    "slice": "a",
    "round": 11,
    "round_note": "Round 11, independent verifier (Haiku), did not build SC1. Previous pin 00a84795 (round 10); this pin 11d7077 is the fix commit for round 10 (one commit in between).",
    "verifier": "verifier Haiku, round 11 (slice a)",
    "pin": PIN,
    "base": PREV_PIN,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a",
    "scratch": "/tmp (mktemp scratch directories for twins)",
    "verified_at": "2026-11-05T12:00:41+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Curriculum SC1 lists Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) as a second source (curriculum/03-markets.yaml:524). No registry record exists (grep of references/references.json: none). The hub says so (index.html:184); no action in slice a unless the module should cite it.",
    ],
    "freshness_flags": [],
    "notes": [
        "Full line-by-line read at 11d7077 of index.html (190 lines), L01.html (446), L02.html (560), L03.html (504), the three lab twins, and the L01-L03 cards of cards.json (cards read in full; all 208 scanned for duplicates).",
        "Delta since the round-10 pin: one commit (11d7077, 'Batch 4: fixes for independent verification round 10'); its slice-a hunks were read; the round-10 FAILs SC1a-hub-concept-list and SC1a-r10-card-L05-ck-wording are fixed; SC1a-r10-A1-attribution-M4 is fixed by removing the attribution, and the same A1 block now has a false part (b), recorded as a new FAIL.",
        "Gates run at 11d7077 (outputs in ledgers/SC1/scripts/SC1-a-r11/): check_pages --unit SC1, check_dag --unit SC1 and --all, check_projects --unit SC1, run_labs --unit SC1 (11/11), page_smoke --unit SC1 for index, L01, L02, L03 each alone, ruff (tests/labs/SC1, tests/test_labs.py), mypy --no-incremental (whole project, 385 files), pytest -k SC1 (11 passed), verify_refs --offline and --unit SC1 live, twins under python -I -W error (python3 and .venv CPython 3.14.8).",
        "Not run: run_graders and mutate_graders (project graders; outside slice a). Not checked in full: L04-L08 and project.html bodies (only the hub cards, cross-references, and the L04/L05/project hunks of the delta). BLUEPRINT.md, the curriculum files and L06-L08 are carried from round 10 (unchanged since the previous pin).",
        "Not checked: the Shreve text itself (no passage locator is claimed, and the source is not readable here beyond the openlibrary record). The claim that every result 'names the numbered Assumptions it uses' (index.html:184) was checked for the results of L01-L03 only.",
        "Mutants: six lab-claim mutants (demonstrations, not graders) all killed; the four round-10 lab mutants were not re-run this round.",
        f"Stats: fresh {stats['fresh']}, carried {stats['carried']}, overridden/new {stats['override']}; counts {counts}.",
    ],
    "summary": {"text": f"SC1-a round 11 at 11d7077: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: SC1a-r11-A1b-literal-false, SC1a-math-L01-remark1.3, SC1a-math-L02-lemma2.3-arithmetic, SC1a-r10-cards-dup-hypotheses, SC1a-hub-assumption-promise.",
                "counts": counts,
                "non_pass_ids": [r["id"] for r in rows if r["status"] != "PASS"]},
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), counts, "stats", stats, "verdict", verdict)
