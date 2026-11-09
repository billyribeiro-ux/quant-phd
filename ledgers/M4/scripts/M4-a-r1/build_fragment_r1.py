import json
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M4-a")
S = "ledgers/M4/scripts/M4-a-r1/"
base = json.load(open("/Users/billyribeiro/.fanout/frags/D-M4-a.round12.json"))
base_rows = {r["id"]: r for r in base["rows"]}

PREFIX = "Carried from round 12 ({files} byte-identical since the previous pin): "

# carried rows: id -> files whose cited subject is byte-identical between 329c1d7f and HEAD
CARRY = {
    "A-H02": "course/modules/M/M4/index.html:29 and the data-hours attributes of L01..L10 (lines unchanged; L08-L10 data-hours unchanged)",
    "A-H03": "course/modules/M/M4/index.html:48-56",
    "A-H04": "course/modules/M/M4/index.html:58-66 and curriculum/01-foundations.yaml lines 88 and 123 (unchanged) and the M4 entry (text identical, now at lines 191-195 after a one-line insertion above it at 183-190)",
    "A-H07": "course/modules/M/M4/index.html:73-131",
    "A-H08": "course/modules/M/M4/index.html:140 and course/modules/M/M4/L06.html:59,:158",
    "A-H12": "course/modules/M/M4/index.html:37,:175,:187 and course/modules/M/M4/L02.html:146 and L03.html:122",
    "A-H13": "references/references.json record blitzstein2019introduction (record compared: identical to 329c1d7f)",
    "A-H14": "curriculum/01-foundations.yaml M4 entry (text identical; now lines 191-195)",
    "A-H15": "course/modules/M/M4/index.html:162-170 and course/modules/M/M4/project.html:42-47",
    "L01-PROSE": "course/modules/M/M4/L01.html:51-99",
    "L01-MATH": "course/modules/M/M4/L01.html:80-135",
    "L01-DELTA-86": "course/modules/M/M4/L01.html:85-86",
    "L01-PROBLEMS": "course/modules/M/M4/L01.html:302-404",
    "L01-QUIZ": "course/modules/M/M4/L01.html:424-494",
    "L01-GRADES": "course/modules/M/M4/L01.html:43-48,:103,:113,:119,:413-418",
    "L01-FWD": "course/modules/M/M4/L01.html:37-38,:95,:505",
    "L01-LAB": "course/modules/M/M4/L01.html:138-271 and tests/labs/M4/lab-M4-L01-1.py",
    "L02-PROSE": "course/modules/M/M4/L02.html:51-101",
    "L02-MATH": "course/modules/M/M4/L02.html:63-142",
    "L02-PROBLEMS": "course/modules/M/M4/L02.html:298-401",
    "L02-QUIZ": "course/modules/M/M4/L02.html:421-492",
    "L02-CANON": "course/modules/M/M4/L02.html:269-272",
    "L02-MISC": "course/modules/M/M4/L02.html:279-296",
    "L02-FWD-COVARIANCE": "course/modules/M/M4/L02.html:345-347",
    "L02-FOOTER-SCOPE": "course/modules/M/M4/L02.html:494-507",
    "L03-PROSE": "course/modules/M/M4/L03.html (whole file)",
    "L03-MATH": "course/modules/M/M4/L03.html (whole file)",
    "L03-LAB": "course/modules/M/M4/L03.html (whole file) and tests/labs/M4/lab-M4-L03-1.py",
    "L03-NUMBERING": "course/modules/M/M4/L03.html (whole file)",
    "L03-STD-NORMAL-DUP": "course/modules/M/M4/L03.html (whole file)",
    "L03-CANON": "course/modules/M/M4/L03.html (whole file)",
    "L03-MISC": "course/modules/M/M4/L03.html (whole file)",
    "L03-PROBLEMS": "course/modules/M/M4/L03.html (whole file)",
    "L03-QUIZ": "course/modules/M/M4/L03.html (whole file)",
    "L03-GRADES": "course/modules/M/M4/L03.html (whole file)",
    "L03-FOOTER-SCOPE": "course/modules/M/M4/L03.html (whole file)",
    "L03-PROP28-SCOPE": "course/modules/M/M4/L03.html (whole file)",
    "L04-PROSE": "course/modules/M/M4/L04.html (whole file)",
    "L04-TERM-ORDER": "course/modules/M/M4/L04.html (whole file)",
    "L04-REMARK-1-3": "course/modules/M/M4/L04.html (whole file) and tests/labs/M4/lab-M4-L04-1.py",
    "L04-MATH": "course/modules/M/M4/L04.html (whole file)",
    "L04-DELTA-53": "course/modules/M/M4/L04.html (whole file)",
    "L04-PROBLEMS": "course/modules/M/M4/L04.html (whole file)",
    "L04-QUIZ": "course/modules/M/M4/L04.html (whole file)",
    "L04-CANON-MISC": "course/modules/M/M4/L04.html (whole file)",
    "L04-FOOTER": "course/modules/M/M4/L04.html (whole file)",
    "L04-FWD": "course/modules/M/M4/L04.html (whole file)",
    "L04-LAB": "course/modules/M/M4/L04.html (whole file) and tests/labs/M4/lab-M4-L04-1.py",
    "CARDS-L01": "course/modules/M/M4/cards.json entries M4-c001..c016, c173, c192..c195, c197, c198, c245 (dict-compared identical)",
    "CARDS-L03": "course/modules/M/M4/cards.json entries M4-c034..c048, c183, c200, c212, c214, c215, c222..c229 (dict-compared identical)",
    "NOTATION-REG": "course/modules/M/M4/L03.html:75-86 and notation/notation.json (both unchanged)",
    "DAG-L02-L04-USES": "course/modules/M/M4/L02.html:37-39 and L03/L04 meta lines",
    "DAG-SD-TWICE": "course/modules/M/M4/L02.html:100-101 and L05.html:79-80",
}

FRESH = {}

def gate(name, body):
    FRESH[name] = body

gate("A-G01", "check_pages --unit M4 -> 'check_pages M4: PASS' exit 0 (" + S + "check_pages.out)")
gate("A-G02", "check_dag --unit M4 -> 'check_dag M4: PASS' exit 0 (" + S + "check_dag.out)")
gate("A-G03", "check_projects --unit M4 -> 'check_projects M4: PASS' exit 0 (" + S + "check_projects.out); project.html unchanged in this delta")
gate("A-G04", "run_labs --unit M4 -> 'run_labs M4: PASS (13/13)' exit 0 (" + S + "run_labs.out)")
gate("A-G05", "twin_compare.py run from /tmp: each of tests/labs/M4/lab-M4-L01..L04-1.py executed as python -I -W error, exit 0, empty stderr; page code equals twin (True x4, L02 included after the delta); expected block equals stdout (True x4) (" + S + "twin_compare.out)")
gate("A-G06", "page_smoke --unit M4 --pages index L01 L02 L03 L04 -> 'page_smoke M4: PASS' exit 0 (" + S + "page_smoke.out)")
gate("A-G07", "ruff check tests/labs/M4 course/modules/M/M4 -> 'All checks passed!'; ruff format --check tests/labs/M4 -> '13 files already formatted' (" + S + "ruff_check.out, ruff_format.out)")
gate("A-G08", "mypy --no-incremental -> 'Success: no issues found in 386 source files' exit 0 (" + S + "mypy.out)")
gate("A-G09", "git status after all gate runs: no tracked file modified; only untracked ledgers/ scratch and the .venv symlink (render_curriculum rewrote its outputs byte-identically, git diff --exit-code exit 0)")
gate("A-G10", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py tests/test_page_smoke.py tests/test_curriculum.py tests/test_refs.py -> 100% dots, exit 0 (" + S + "pytest.out)")
gate("A-G11", "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' exit 0; verify_refs.py --unit M4 (live Crossref, plain HTTP) -> '1 of 560 entries, 0 problems' exit 0 (" + S + "verify_refs_offline.out, verify_refs_live_M4.out)")
gate("A-G12", "card gate: " + S + "recheck_slice_a.py: 'cards: ids unique', 'no duplicate fronts', 'no duplicate backs', 'every card number appears in its lesson ... missing=[]' all OK. Its count line reports MISMATCH n=88 because the constant it hard-codes is stale (83); the true count is 88 = L01 23 + L02 20 + L03 27 + L04 18 (slice_cards_head.txt). grep over repo outside ledgers for M4-c028 and M4-c065: no hits. Ids M4-c028/M4-c065 are removed, no dangling reference")
gate("A-G13", "build_site --check -> 'site data current: 6 outputs' exit 0 (" + S + "build_site_check.out)")
gate("A-G14", "fetch_data --check -> 'fetch_data: 3 datasets, 0 problems' exit 0 (" + S + "fetch_data_check.out)")
gate("A-G15", "render_curriculum.py -> 'curriculum valid' and 'wrote' exit 0, then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (" + S + "render_curriculum.out, render_curriculum_diff.out)")

FRESH["A-H01"] = "index.html section ids at lines 45 (objectives), 58 (prerequisites), 68 (placement), 145 (lessons), 162 (ladder), 173 (data), 178 (reading), same as the round-12 locators (grep -n '<section'); the delta changed only the text of lines 70 and 135 (line counts preserved). check_pages PASS"
FRESH["A-H05"] = "re-verified: the delta's added lines (" + S + "delta_added_lines.txt, 11 lines) contain no M3 concept word (eigen, semidefinite, projection, singular, vector space, principal, PCA, covariance matrix, SVD: grep, no hits); check_dag PASS"
FRESH["A-H06"] = "re-verified: index.html placement section (lines 68-143) has 10 'li class=item' entries, 2 with data-skill (lines 132, 137); mastery data-mastery=0.8. Line 70 changed text only; M1 L01.html:79 unchanged"
FRESH["A-H09"] = "re-verified: index.html:132-135 key data-answer=1, tolerance 0; F(0)=1/4 < 1/2 <= F(1)=3/4 so the 0.5 quantile is 1 (Prop 3.2). Explanation sentence at line 135 re-verified under A-H16"
FRESH["A-H10"] = "re-verified: hub card descriptions index.html:147-160 unchanged; lesson headings unchanged; the L02 claim 'shortcut and scale rule checked on die and loss' still matches the lab (" + "course/modules/M/M4/L02.html:146-156 and output in twin_compare.out L02 stdout)"
FRESH["A-H11"] = "re-verified: index.html:70 now links <a href=\"#ladder\"> and index.html:162 is <section id=\"ladder\"> (anchor resolves); project.html:42 unchanged (answered both skill checks)"
FRESH["DELTA-HUB-LADDER-LINK"] = "index.html:70 new anchor <a href=\"#ladder\"> resolves to index.html:162 <section id=\"ladder\">; its claim that rungs 1 and 2 are described in The project ladder matches index.html:165-167 (Worked example = rung 1, Completion problem = rung 2)"
FRESH["DATA-A"] = "re-verified: index.html:37, :175, :187 and L02.html:146, :507 (SIMULATED labelling and no-real-data statements unchanged); L03.html:122, :477 unchanged; L01 meta now says 'no data is read' and lab-M4-L01-1.py performs no file read (grep for open/read/csv/json: no hits)"
FRESH["NOTATION-A"] = "re-verified: delta adds symbols n, \\lceil, \\rceil, mu, E[X^2] only; registered symbols (notation/notation.json: \\gamma_3, \\gamma_4, \\Phi, T, R^*, R^{e*}, R_f, \\mathbb{Q}) do not appear in the delta; 'n' is a local letter (not registered)"
FRESH["NOTATION-MACRO"] = "re-verified: new macro \\lceil in index.html:135 is already used in M4 pages (L01.html:454 and project.html rung 1) and is standard LaTeX; no unregistered custom macro in the delta"
FRESH["PROCESS-A"] = "re-verified: grep of the delta's added lines (" + S + "delta_added_lines.txt) and of index/L01..L04 for builder, verifier, round, ledger, slice, ruling, fragment, todo, placeholder, draft: no learner-text hits"
FRESH["SCOPE-A"] = "re-verified: scope words in the delta's added lines: only 'same' (index.html:135, 'The same convention as rung 1 applies'), backed by Prop 3.2 (hub item is a finite law with distinct values) and rung 1 (project.html:58-60 rank rule); no new every/all/only/always/any/exactly"
FRESH["STRUCT-A"] = "re-verified: delta to L01.html changes line 7 (meta description) only; delta to L02.html changes prose lines 151-158 and docstring text only; no section, heading or lab tag is added or removed (added-line tag grep: only the anchor in index.html:70)"
FRESH["NUM-A"] = "re-verified: " + S + "recompute.out (recompute.py, exact fractions and float): '58 OK, 0 MISMATCH'; the only new number in the delta is 0.99 (index.html:135), matching project.html:58-60 (rank (99 n + 99)//100)"
FRESH["GRADE-A"] = "re-verified: the only card whose text changed is M4-c023 (T, Proposition 2.3, a proved result; L02.html:116-117); L01 meta and L02 lab prose carry no grade change"
FRESH["ASSUMP-A"] = "re-verified: index.html:135 states the convention with Prop 3.2 hypotheses met by the hub law (weights 1/4, 1/2, 1/4; distinct values 0,1,2); no numbered Assumption added in the delta. The Prop 3.4 citation at line 135 is the defect recorded in A-H16"
FRESH["DAG-A"] = "re-verified: check_dag PASS; the delta adds no dfn tag; new internal link #ladder resolves (index.html:162)"
FRESH["DAG-HUB-PREVIEW"] = "re-verified: index.html:147-160 unchanged and matches lesson headings and labs (see A-H10)"
FRESH["CARDS-L02"] = "re-verified: course/modules/M/M4/cards.json L02 entries at HEAD: M4-c017..c027, c029..c033, c181, c182, c199, c243 (20 entries; c028 removed; c023 changed); each card number appears in L02.html (Prop 2.3 text L02.html:116-117 matches c023)"
FRESH["CARDS-L04"] = "re-verified: cards.json L04 entries at HEAD: M4-c049..c064, c201, c204 (18 entries; c065 removed); no other L04 card changed (dict compare against 329c1d7f)"
FRESH["CARDS-DELTA"] = "re-verified (dict compare of cards.json, 329c1d7f vs HEAD): slice-a changes are M4-c023 (text changed, hypotheses and conclusion restated), M4-c028 and M4-c065 removed; M4-c192 and M4-c245 identical; M4-c244 absent. L08-L10 card changes (c122, c126, c128, c140, c143, c157, c158, c162, c165..c172, c185, c188..c190, c217, c233..c241, c246..c257) are outside slice a"
FRESH["CARDS-NUMBERS"] = "re-verified: recheck_slice_a.py 'every card number appears in its lesson text' OK missing=[] over the 88 slice cards (" + S + "recheck_slice_a.out)"
FRESH["CARD-M4-c219"] = "re-verified: no M4-c219 in cards.json at HEAD (grep over course/ and tests/: no hits)"
FRESH["CARDS-DUP"] = "re-verified from scratch (88 slice cards at HEAD in " + S + "slice_cards_head.txt): the two same-question, same-answer pairs of round 12 are gone (M4-c028 removed; M4-c065 removed). Pairwise similarity scan (difflib over fronts and backs, top 14 pairs) finds only parallel facts (mean/variance, skewness/kurtosis, m_1/m_2, shortcut for variance/covariance, Var(Z)/E[Z]), none with the same question and answer"

FRESH["A-H16"] = "re-verified from scratch. The round-12 defect (index.html:135 'This is the worked example of rung 1.') is gone: the sentence was replaced. The replacement says 'rung 1 uses the rank ceil(0.99 n) of equally likely losses (Lesson 1, Proposition 3.4)'. The rank rule is right (project.html:58-60, (99 n + 99)//100 = ceil(0.99 n)), but Proposition 3.4 (L01.html:119-121) assumes 'distinct real numbers y_1 < ... < y_n'. The rung-1 losses are whole cents (project.html:61 'rounded once with round()') and repeat: running tests/labs/M4/lab-M4-project-1.py simulate() for both families, n = 20000 gives 616 repeated entries (Gaussian, 19384 distinct values) and 680 (Student-t, 19320 distinct). The hub sentence therefore cites Prop 3.4 for a sample whose distinct-values hypothesis fails. Ruling 26 kind: missing hypothesis."

FRESH["DELTA-L01-META"] = "L01.html:7 meta description changed from 'SIMULATED: no data.' to 'The law is a stated table, and no data is read.' Checked: lab-M4-L01-1.py docstring 'The law is a stated table, not data'; no randomness and no file read in the lab (grep for open/read/csv/json: no hits); accurate"
FRESH["DELTA-CARD-C023"] = "cards.json M4-c023 (L02, grade T) now: front 'Does scaling X by a constant a multiply its variance by a?' back 'No. Hypothesis: finite probability space with positive weights. Var(aX + b) = a^2 Var(X) ... (Proposition 2.3).' Checked: L02.html:116-117 Prop 2.3 'For constants a, b, Var(aX+b) = a^2 Var(X). In particular Var(X+b)=Var(X)'; the positive-weights hypothesis is the standing one of L02 section 2 (L02.html:55). Correct"
FRESH["DELTA-CARD-REMOVALS"] = "M4-c028 and M4-c065 removed (the round-12 CARDS-DUP fix). Repo grep for both ids outside ledgers/.venv: no hits, so no dangling reference"
FRESH["L02-LAB"] = "re-verified: L02.html:144-263 and tests/labs/M4/lab-M4-L02-1.py (changed prose and docstring lines 4-11). Page code equals twin (True); expected block equals stdout (True) (" + S + "twin_compare.out). Every claim in the new paragraph checked against the code: 'Each exact variance is computed two ways' (variance_by_definition and variance_shortcut, Fraction arithmetic); 'checks that the two agree' (prints True/False, lines 'definition and shortcut agree'); 'the scale rule Var(2X) = 4 Var(X) on the die' (printed True); seeds 2026/2027 and the printed counts (489 losses, 122250000 cents) match the output; 'standard library only' (imports: __future__, math, random, collections.abc, fractions). Hypothesis figures (7/2, 91/6, 35/12) recomputed: 91/6 - 49/4 = 35/12"

rows = []
for rid, brow in base_rows.items():
    if rid == "A-H16":
        rows.append({"id": rid, "check": brow["check"], "location": "course/modules/M/M4/index.html:135", "status": "FAIL", "evidence": FRESH["A-H16"],
                     "fix": "In index.html:135 keep the Proposition 3.2 sentence and replace 'and rung 1 uses the rank \\(\\lceil 0.99\\, n \\rceil\\) of equally likely losses (Lesson 1, Proposition 3.4).' with 'Rung 1 takes the rank \\(\\lceil 0.99\\, n \\rceil\\) of its sorted losses (project.html, Rungs 1 and 2). Proposition 3.4 states that rank for distinct values, and the whole-cent losses of rung 1 can repeat.' Then rerun check_pages --unit M4, page_smoke --unit M4 --pages index, and a delta verification of this row."})
    elif rid == "CARDS-DUP":
        rows.append({"id": rid, "check": brow["check"], "location": "course/modules/M/M4/cards.json (M4-c028 and M4-c065 removed)", "status": "PASS", "evidence": FRESH["CARDS-DUP"]})
    elif rid in FRESH:
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS", "evidence": FRESH[rid]})
    elif rid in CARRY:
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS",
                     "evidence": PREFIX.format(files=CARRY[rid]) + brow["evidence"]})
    else:
        raise SystemExit("unassigned base row " + rid)

extra_ids = [k for k in FRESH if k not in base_rows]
for k in extra_ids:
    pass
for rid, loc, chk in [
    ("DELTA-L01-META", "course/modules/M/M4/L01.html:7", "delta: L01 meta description"),
    ("DELTA-HUB-LADDER-LINK", "course/modules/M/M4/index.html:70", "delta: hub link to the project ladder"),
    ("DELTA-CARD-C023", "course/modules/M/M4/cards.json (M4-c023)", "delta: card M4-c023 text"),
    ("DELTA-CARD-REMOVALS", "course/modules/M/M4/cards.json (M4-c028, M4-c065)", "delta: removed duplicate cards"),
]:
    rows.append({"id": rid, "check": chk, "location": loc, "status": "PASS", "evidence": FRESH[rid]})

for r in rows:
    if r["status"] != "PASS":
        assert r["fix"].strip()

mutants = []
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
from collections import Counter
c = Counter(r["status"] for r in rows)
frag = {
    "unit": "M4",
    "slice": "a",
    "round": 1,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyF21-M4-a)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "329c1d7feac5479403c351e64587c867278452cc",
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": "2026-11-09T12:00:00+00:00",
    "verdict": "PASS" if c["PASS"] == len(rows) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "Closing delta (rulings 30, 37) from the round-12 fragment (pin 329c1d7f, base ccaeeaf4). Delta in slice a: "
        "course/modules/M/M4/index.html:70 (ladder link) and :135 (rung-1 explanation); L01.html:7 (meta description); "
        "L02.html:151-158 and tests/labs/M4/lab-M4-L02-1.py docstring (exact-variance wording); cards.json (M4-c023 text, M4-c028 and "
        "M4-c065 removed). Rows whose cited subject changed or was a round-12 non-PASS row were re-verified from scratch; all other rows "
        "carry the round-12 evidence under the carry prefix because their cited lines and files are byte-identical. Outside slice a and "
        "not verified here: L05-L10 pages and twins (except cross-references), project.html content (only cross-references), L08-L10 card "
        "changes, curriculum/CURRICULUM.md/program.json M2 project brief, references.json regeneration (generated_at, FC2 used_by; the blitzstein record is identical). "
        "Mutants: none. Ruling 37 writes no new mutants; slice a has no grader, so the standing mutant set for slice a is empty. "
        "Judgment, not counted (same rule as round 12: same question and same answer only): M4-c051/M4-c052 both state the cell-by-cell "
        "independence test; M4-c022/M4-c029 restate the shortcut formula under different questions. Observation only, not a row. "
        "Stale constant in " + S + "recheck_slice_a.py (cards count 83): its MISMATCH line is the script's own expectation, not a page defect "
        "(true count 88). Blitzstein book not read; no locator claimed."
    ),
    "summary": (
        "Closing delta round 1 at 95f3f8cb (base 329c1d7f): " + str(len(rows)) + " rows; " + str(c["PASS"]) + " PASS, "
        + str(c["FAIL"]) + " FAIL, " + str(c["UNVERIFIABLE"]) + " UNVERIFIABLE. The round-12 FAIL A-H16 is fixed in its first clause but "
        "the replacement sentence cites Proposition 3.4 (distinct values) for rung 1, whose seeded losses repeat (616 and 680 repeated entries). "
        "CARDS-DUP is PASS (M4-c028 and M4-c065 removed). Every gate re-run, all rows re-verified or carried."
    ),
}
out = ROOT / "ledgers/M4/M4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), dict(c), "verdict", frag["verdict"])
