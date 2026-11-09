"""Build ledgers/M4/M4-a.json for the closing delta of slice a (pin 85b109f8, base d9de2fe5).

Carried rows keep their base (d9de2fe5) evidence under the carry prefix; rows whose cited
subject changed in d9de2fe5..85b109f8 (L01.html lines 130 and 278) or that were non-PASS in the
base are re-verified and carry fresh evidence written here.
"""
import json
import sys

BASE = "/Users/billyribeiro/.fanout/frags/H-M4-a.round1.json"
OUT = "ledgers/M4/M4-a.json"
S = "ledgers/M4/scripts/M4-a-r1/"
PREFIX_ALL = "Carried from round 1 (course/modules/M/M4 files byte-identical since the previous pin d9de2fe5): "
PREFIX_L01 = ("Carried from round 1 (course/modules/M/M4/L01.html lines {rng} byte-identical since the previous pin "
              "d9de2fe5; the only L01 hunks are at lines 130 and 278): ")

base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

fresh = {
 "A-G01": ("check_pages.py --unit M4 at 85b109f8: exit 0, 'check_pages M4: PASS' (" + S + "v_check_pages.out).", "tools/check_pages.py --unit M4"),
 "A-G02": ("check_dag.py --unit M4 at 85b109f8: exit 0, 'check_dag M4: PASS' (" + S + "v_check_dag.out).", "tools/check_dag.py --unit M4"),
 "A-G03": ("check_projects.py --unit M4 at 85b109f8: exit 0, 'check_projects M4: PASS' (" + S + "v_check_projects.out). project.html has no diff since d9de2fe5.", "tools/check_projects.py --unit M4"),
 "A-G04": ("run_labs.py --unit M4 at 85b109f8: exit 0, 'run_labs M4: PASS (13/13)' (" + S + "v_run_labs.out). run_labs checks each page lab against its twin and the expected block against twin output.", "tools/run_labs.py --unit M4"),
 "A-G05": ("Each of the 13 twins run alone as `.venv/bin/python -I -W error tests/labs/M4/<file>`: exit 0 and empty stderr (lab-M4-L01-1 .. L10-1, lab-M4-project-1..3). The L01 lab block (L01.html:138-271) is outside the two changed hunks (lines 130 and 278); page-code-equals-twin and expected-equals-output are the run_labs checks of A-G04.", "tests/labs/M4/*.py vs course/modules/M/M4/L01..L04.html"),
 "A-G06": ("page_smoke.py --unit M4 --pages index L01 L02 L03 L04 at 85b109f8: exit 0, 'page_smoke M4: PASS' (" + S + "v_page_smoke.out); L01 was re-loaded in Chromium after the L01.html:130 and :278 edits.", "tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04"),
 "A-G07": ("`.venv/bin/ruff check tests/labs/M4 course/modules/M/M4` -> 'All checks passed!'; `ruff format --check tests/labs/M4` exit 0 (" + S + "v_ruff.out).", "ruff"),
 "A-G08": ("`.venv/bin/mypy --no-incremental` at 85b109f8: exit 0, 'Success: no issues found in 386 source files' (" + S + "v_mypy.out).", "mypy strict"),
 "A-G09": ("git status after all gate runs: no tracked source edit; the only tracked change is the verifier's own scratch output " + S + "v_page_smoke.out (overwritten by this round's run, prior content in git); untracked .venv symlink and this round's v_* outputs.", "repository state"),
 "A-G10": ("`.venv/bin/python -m pytest -q tests/test_page_checks.py tests/test_page_smoke.py tests/test_run_labs.py tests/test_docs_figures.py tests/test_curriculum.py tests/test_labs.py` at 85b109f8: exit 0, 443 dots, no F or E (" + S + "v_pytest.out).", "relevant pytest"),
 "A-G11": ("`.venv/bin/python tools/verify_refs.py --offline` at 85b109f8: exit 0, 'offline integrity: 560 entries, 0 problems' (" + S + "v_verify_refs_offline.out). The live Crossref half is not re-run; references/ is byte-identical since d9de2fe5, so it is carried from round 1.", "2.1 registry"),
 "A-G12": ("Fresh numeric check over the 219 cards in course/modules/M/M4/cards.json against the text of L01..L04.html: every number token in a card front or back occurs in its lesson text, 0 missing (command and output in " + S + "build_fragment_verifyI1.py run; the cards are byte-identical since d9de2fe5). No card id is dangling: the L01 hunks change prose only (no data-card attribute).", "course/modules/M/M4/cards.json vs L01..L04.html"),
 "A-G13": ("`.venv/bin/python tools/build_site.py --check` at 85b109f8: exit 0, 'site data current: 6 outputs' (" + S + "v_build_site_check.out).", "2.8 generated site data (not edited)"),
 "A-G14": ("`.venv/bin/python tools/fetch_data.py --check` at 85b109f8: exit 0, 'fetch_data: 3 datasets, 0 problems' (" + S + "v_fetch_data_check.out).", "2.8 data manifest"),
 "A-G15": ("`.venv/bin/python tools/render_curriculum.py` exit 0, then `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json` exit 0 (" + S + "v_render_curriculum.out, v_render_diff.out).", "generated curriculum current"),
 "L01-MATH": ("Re-verified from scratch at 85b109f8 (base FAIL withdrawn; the defect was Example 3.5 at L01.html:130 applying Proposition 3.4 without the distinct-values hypothesis, now fixed). Read L01.html:78-135 in full. Proposition 2.2 (a)-(d) and its proof: the sum over x_j <= x, F constant on [x_k, x_{k+1}), F_k - F_{k-1} = p_k > 0: correct. Definition 3.1 is well posed for 0 < p <= 1 (set nonempty by F_m = 1, bounded below by x_1). Proposition 3.2 and its minimality step (j >= k*, so x >= x_j >= x_{k*}): correct. Remark 3.3 (Q(F_k) = x_k needs p_k > 0; left-continuity via u_n in (F_{k-1}, p]): correct. Proposition 3.4 proof (F_j = j/n, least j with j/n >= p is the least integer >= pn): correct. Example 3.5 now opens 'Let X take n equally likely distinct values, as in Proposition 3.4' (L01.html:130): 200*0.99 = 198 (ceil 198), 150*0.99 = 148.5 (ceil 149, floor 148). Example 3.6 values F(-2)=1/10, F(-1)=3/10, F(0)=3/5, F(1)=4/5, F(2)=9/10, F(3)=1; Q(1/2)=0, Q(3/5)=0, Q(61/100)=1, and the Lab 1 predicted quantiles (L01.html:~140) re-derived in exact fractions (" + S + "v_math_check.py / v_math_check.out). All re-derived numbers agree with the page.", "L01.html:78-135 (Props 2.2, 3.2, Remark 3.3, Prop 3.4, Examples 3.5, 3.6); scripts " + S + "v_math_check.py"),
 "L01-P34-HYP": ("Re-verified from scratch over every use of Proposition 3.4 in the slice and its cards. Statement L01.html:119 (distinct y_1 < ... < y_n). Uses: L01.html:130 (Example 3.5, now 'Let X take n equally likely distinct values, as in Proposition 3.4'): hypothesis stated; :277 'applied to equally likely distinct values': stated; :278 canon-breaks bullet 2, now 'Example 3.5 gives 149 for n = 150 distinct equally likely values': stated (the delta fix); :280 'exact statement about n equally likely distinct values': stated; :297 misconception 3 'for 150 distinct equally likely values': stated; :326 M3 'forty distinct values': stated; :416 table 'For n distinct equally likely values': stated; :452 and :457 quiz prompts 'distinct losses': stated; :454 and :459 explanations rely on the prompts. Cards M4-c010 ('distinct values'), M4-c011 ('200 equally likely distinct losses'), M4-c015 ('equally likely distinct values', hypotheses carried) in cards.json lines 68-69, 75-76, 96-97: stated. No use omits the hypothesis.", "L01.html:119, :130, :277, :278, :280, :297, :326, :416, :452, :457; course/modules/M/M4/cards.json lines 68-69, 75-76, 96-97"),
 "DELTA-L01-P34-DISTINCT": ("Delta hunk at 85b109f8 re-verified: L01.html:278 now reads 'Example 3.5 gives 149 for n = 150 distinct equally likely values and p = 0.99' (the Example 3.5 numbers are the page's, 150*0.99 = 148.5, ceil 149), and :277 and :280 state 'distinct' (both read fresh). The 148th value's distribution function 148/150 = 74/75 = 0.98667 < 0.99 (" + S + "v_math_check.out).", "course/modules/M/M4/L01.html:277, :278, :280"),
 "NOTATION-A": ("Changed text at 85b109f8 read against notation/notation.json: new L01.html:130 uses X, n, p, pn, \\lceil pn \\rceil (notation/notation.json has the registered X, n, p, Q, F; no new symbol introduced); L01.html:278 adds no symbol. The \\lceil symbol has no notation.json entry at either pin (observation, unchanged from the base; see notes). The other changed lines (index.html:135, L01.html:296-297, :401, cards M4-c079) are byte-identical since d9de2fe5.", "course/modules/M/M4/L01.html:130, :278; notation/notation.json"),
 "NOTATION-MACRO": ("Changed text at L01.html:130 and :278 uses only existing macros (\\(X\\), \\(n\\), \\(p\\), \\(pn\\), \\(\\lceil\\,\\rceil\\), \\(\\tfrac\\)); no new macro. Macro definitions unchanged (no diff in course/assets since d9de2fe5).", "course/modules/M/M4/L01.html:130, :278"),
 "PROCESS-A": ("Changed text L01.html:130 and :278 read: no process words ('we', 'this page', 'Lesson', 'verifier', 'round', 'flagged', 'drafted'). Other changed lines byte-identical since d9de2fe5.", "course/modules/M/M4/L01.html:130, :278"),
 "SCOPE-A": ("Changed text L01.html:130 and :278 read: no scope word (only, all, always, every, any, same, exactly) without a computation or hypothesis. The new 'distinct' wording is the Prop 3.4 hypothesis itself. Example 3.5 numbers are computed on the page.", "course/modules/M/M4/L01.html:130, :278"),
 "NUM-A": ("Numbers in changed text re-derived (" + S + "v_math_check.out): L01.html:130 n = 200, p = 0.99, pn = 198, ceil 198; n = 150, pn = 148.5, ceil 149, floor 148; :278 n = 150, p = 0.99, 149, 148, pn = 148.5, 148/150 = 74/75 = 0.98667 (page: 0.987), below 0.99. All agree with the page.", "course/modules/M/M4/L01.html:130, :278"),
 "GRADE-A": ("Grade table (L01.html:413-418) and the grades of L01..L04 unchanged by the delta. The changed text (Example 3.5 at :130, bullet 2 at :278) is an example and a caveat, not a graded claim; Proposition 3.4 stays T with its hypothesis. Grades re-read on the whole of L01..L04 pages at 85b109f8; no grade attribute changed.", "course/modules/M/M4/index.html; L01..L04.html; cards.json (slice)"),
 "ASSUMP-A": ("Hypotheses of Proposition 3.4 at the point of use: Example 3.5 (L01.html:130) now states its hypothesis (n equally likely distinct values) before applying the index; canon-breaks bullet 2 (:278) states it; no new numbered Assumption was introduced by the delta. Hub index.html:138-140 byte-identical.", "course/modules/M/M4/L01.html:130, :278; index.html:138-140"),
 "DAG-A": ("check_dag.py --unit M4 at 85b109f8: PASS (" + S + "v_check_dag.out). The delta adds no dfn tag (diff of L01.html shows four changed lines, all prose, no id or class change); Proposition 3.4 is cited after its definition (:119 before :130). Lesson definitions unchanged.", "check_dag.py --unit M4; L01..L04.html dfn tags"),
 "STRUCT-A": ("check_pages.py --unit M4 at 85b109f8: PASS (A-G01); the delta changes two text nodes in L01.html, no tag, section or block added or removed (git diff d9de2fe5..85b109f8 -- course/modules/M/M4/L01.html: 2 insertions, 2 deletions, lines 130 and 278).", "course/modules/M/M4/L01..L04.html"),
}

rows = []
for rid, brow in base_rows.items():
    if rid in fresh:
        ev, loc = fresh[rid]
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"] if rid not in ("A-G01", "A-G02", "A-G03", "A-G04", "A-G05", "A-G06", "A-G07", "A-G08", "A-G09", "A-G10", "A-G11", "A-G12", "A-G13", "A-G14", "A-G15") else loc,
                     "status": "PASS", "evidence": ev, "fix": ""})
        continue
    if brow["status"] != "PASS":
        raise SystemExit(f"base non-PASS row {rid} is not in the fresh set")
    ev = brow["evidence"]
    if rid.startswith("L01-") or rid.startswith("DELTA-L01") or rid in ("CARDS-L01",):
        rng = "outside 130 and 278"
        pre = PREFIX_L01.format(rng=rng)
    else:
        pre = PREFIX_ALL
    rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS",
                 "evidence": pre + ev, "fix": ""})

# keep base id order
order = list(base_rows.keys())
rows.sort(key=lambda r: order.index(r["id"]))

fail = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "M4",
    "slice": "a",
    "round": 1,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyI1-M4-a), closing delta",
    "pin": "85b109f8ae3045085b52626f323f3c934e7718de",
    "base": "d9de2fe5eea982d14cd9f922a61676b847506fbc (base fragment ~/.fanout/frags/H-M4-a.round1.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyI1-M4-a",
    "scratch": "ledgers/M4/scripts/M4-a-r1/",
    "verified_at": "2026-11-09",
    "verdict": "PASS" if not fail else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"],
    "freshness_flags": base["freshness_flags"] + [
        "Closing delta round 1 (pin 85b109f8): the only M4 slice change since d9de2fe5 is L01.html lines 130 and 278 (git diff d9de2fe5..85b109f8 -- course/modules/M/M4 tests/labs/M4 notation references tools curriculum course/assets plans project.html tests). live Crossref verify_refs run not repeated; offline run 560 entries, 0 problems; live half carried (references/ byte-identical since d9de2fe5).",
    ],
    "notes": (
        "Closing delta (rulings 30, 37, 26 kinds only; no new mutants) of slice a from base H-M4-a.round1.json (pin d9de2fe5) to 85b109f8. "
        "git diff d9de2fe5..85b109f8 over the M4 slice paths touches one file: course/modules/M/M4/L01.html, two hunks: line 130 (Example 3.5 now opens 'Let X take n equally likely distinct values, as in Proposition 3.4.') and line 278 (canon-breaks bullet 2 now says 'n = 150 distinct equally likely values'). "
        "Both base FAIL rows (L01-MATH, L01-P34-HYP) were re-verified from scratch and are now PASS; their subject changed. Every other row citing a line range not touched by those hunks is carried under the carry prefix (its evidence is the base's). "
        "Rows whose subject changed or that cite a whole L01 file were re-verified: L01-MATH, L01-P34-HYP, DELTA-L01-P34-DISTINCT, NOTATION-A, NOTATION-MACRO, PROCESS-A, SCOPE-A, NUM-A, GRADE-A, ASSUMP-A, DAG-A, STRUCT-A, and the gate rows A-G01..A-G15. "
        "No new mutants (ruling 37); slice a has no grader and its standing mutant set is empty. "
        "Observations (notes, not rows; unrelated to this delta or outside slice a): (1) \\lceil and \\rceil have no entry in notation/notation.json at either pin (unchanged from the base). "
        "(2) project.html:190, :214, :441 use the ceiling index ceil(0.99 n) for n losses that may tie, and project.html:441 says tied losses fill consecutive positions; index.html:135 states that Proposition 3.4 proves the rank for distinct values only. "
        "Project content is outside slice a; the observation is recorded for the project slice's verifier, not counted here. "
        "Not checked this round: the live Crossref half of verify_refs; L05..L10 pages and cards except as carried; the carried byte-identical cards were not re-read line by line (they are carried under ruling 30, with the numeric check A-G12 and the Prop 3.4 card re-read in L01-P34-HYP). "
        "The tracked file " + S + "v_page_smoke.out was overwritten by this round's run."
    ),
    "summary": (
        f"Closing delta round 1 for M4-a at 85b109f8 (base d9de2fe5): {len(rows)} rows; {len(rows) - len(fail)} PASS, {len(fail)} FAIL, 0 UNVERIFIABLE. "
        "Both base FAIL rows (L01-MATH, L01-P34-HYP) are fixed by the L01.html:130 and :278 delta and re-verified PASS; no new defect of the ruling-26 kinds was found in the changed hunks."
    ),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "verdict", frag["verdict"], "fail", fail)
