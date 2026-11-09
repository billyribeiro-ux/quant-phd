"""Build the SC1-c round-1 closing-delta fragment from the round-13 base fragment (ruling 30)."""
import json
import sys

BASE = "/Users/billyribeiro/.fanout/frags/E-SC1-c.round13.json"
OUT = sys.argv[1]
base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}
S = "ledgers/SC1/scripts/SC1-c-r1/out/"
LAB = "course/modules/SC/SC1/L07.html, course/modules/SC/SC1/L08.html, tests/labs/SC1/lab-SC1-L07-1.py, tests/labs/SC1/lab-SC1-L08-1.py"
PAGE_PREFIX = f"Carried from round 13 ({LAB} byte-identical since e919577b): "
CARDS_PREFIX = "Carried from round 13 (cards.json entries {ids} byte-identical card-level since e919577b; L07.html and L08.html byte-identical): "

CHANGED = {"SC1-c157", "SC1-c159", "SC1-c171", "SC1-c174", "SC1-c201", "SC1-c241", "SC1-c242"}
_cards = json.load(open("/Users/billyribeiro/.fanout/wt/verifyF31-SC1-c/course/modules/SC/SC1/cards.json", encoding="utf-8"))
OTHER46 = ", ".join(c["id"] for c in _cards if c["lesson"] in ("L07", "L08") and c["id"] not in CHANGED)
fresh = {
    "gate-check-pages": (
        "course/modules/SC/SC1/L07.html, course/modules/SC/SC1/L08.html",
        f"Re-run this round: `.venv/bin/python tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS', exit 0 ({S}check_pages.txt).",
    ),
    "gate-check-dag": (
        "course/modules/SC/SC1/L07.html, course/modules/SC/SC1/L08.html",
        f"Re-run this round: `.venv/bin/python tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS', exit 0 ({S}check_dag.txt). The anchor linked from L07 and L08 (`<h2 id=\"s2\">` at course/modules/SC/SC1/L06.html:100) is still present.",
    ),
    "gate-run-labs": (
        "tests/labs/SC1/lab-SC1-L07-1.py, tests/labs/SC1/lab-SC1-L08-1.py",
        f"Re-run this round: `.venv/bin/python tools/run_labs.py --unit SC1` -> 'run_labs SC1: PASS (11/11)', exit 0 ({S}run_labs.txt).",
    ),
    "lab-L07-twin-isolated": (
        "tests/labs/SC1/lab-SC1-L07-1.py",
        f"Re-run this round: the twin executed alone as `python -I -W error` with cwd /tmp by ledgers/SC1/scripts/SC1-c-r1/sc1c_page_twin_r1.py: exit 0, stderr 0 bytes ({S}page_twin_r1.txt).",
    ),
    "lab-L08-twin-isolated": (
        "tests/labs/SC1/lab-SC1-L08-1.py",
        f"Re-run this round: same method as lab-L07-twin-isolated: exit 0, stderr 0 bytes ({S}page_twin_r1.txt).",
    ),
    "lab-L07-page-equals-twin": (
        "course/modules/SC/SC1/L07.html (code block, HTML-unescaped) vs tests/labs/SC1/lab-SC1-L07-1.py",
        f"Re-run this round: page code equals the twin after trailing-newline strip: True ({S}page_twin_r1.txt). L07.html and the twin are byte-identical to e919577b (git diff empty).",
    ),
    "lab-L08-page-equals-twin": (
        "course/modules/SC/SC1/L08.html (code block, HTML-unescaped) vs tests/labs/SC1/lab-SC1-L08-1.py",
        f"Re-run this round: page code equals the twin after trailing-newline strip: True ({S}page_twin_r1.txt). L08.html and the twin are byte-identical to e919577b.",
    ),
    "lab-L07-expected-equals-output": (
        "course/modules/SC/SC1/L07.html:357-379 (pre.expected)",
        f"Re-run this round: the expected block equals the twin's stdout (23 lines each after trailing-newline strip): True ({S}page_twin_r1.txt; stdout {S}L07_stdout.txt).",
    ),
    "lab-L08-expected-equals-output": (
        "course/modules/SC/SC1/L08.html:344-363 (pre.expected)",
        f"Re-run this round: expected block equals the twin's stdout: True ({S}page_twin_r1.txt; stdout {S}L08_stdout.txt).",
    ),
    "lint-mypy-twins": (
        "tests/labs/SC1/lab-SC1-L07-1.py, tests/labs/SC1/lab-SC1-L08-1.py",
        f"Re-run this round: `ruff check` 'All checks passed!' exit 0; `ruff format --check` '2 files already formatted' exit 0; `mypy --no-incremental` 'Success: no issues found in 2 source files' exit 0 ({S}ruff_check.txt, {S}ruff_format.txt, {S}mypy.txt). pyproject.toml changed since the base (ruff extend-exclude only), so re-run.",
    ),
    "page-smoke-L07-L08": (
        "course/modules/SC/SC1/L07.html, course/modules/SC/SC1/L08.html",
        f"Re-run alone: `.venv/bin/python tools/page_smoke.py --unit SC1 --pages L07 L08` -> 'page_smoke modules/SC/SC1/L07.html: PASS', 'page_smoke modules/SC/SC1/L08.html: PASS', 'page_smoke SC1: PASS', exit 0 ({S}page_smoke_L07_L08.txt).",
    ),
    "pytest-lab-tools": (
        "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
        f"Re-run this round: `.venv/bin/python -m pytest -q` on the three files: all dots, 100%, exit 0 ({S}pytest.txt). None of the three is in the e919577..HEAD change list.",
    ),
    "verify-refs-offline": (
        "references/references.json",
        f"Re-run this round: `.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.txt). references.json changed since e919577b in two places only: generated_at, and the used_by list of the Black & Scholes (1973) entry near line 2922 (adds FC2). The shreve2004stochastic entry is unchanged.",
    ),
    "verify-refs-live-SC1": (
        "references/references.json entry shreve2004stochastic",
        f"Re-run this round: `.venv/bin/python tools/verify_refs.py --unit SC1` -> 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 ({S}verify_refs_live_SC1.txt).",
    ),
    "xref-L01-L05-L06": (
        "course/modules/SC/SC1/L07.html, course/modules/SC/SC1/L08.html; L01.html:58-64, 211-235; L05.html:59-71, 271-289; L06.html:87-94, 102, 105-115, 153-181",
        "Re-read this round because L01.html:211-235 changed text (hunks at 215, 217, 234). L01 Def 1.1 (D1-D3) at L01.html:58-64 is unchanged. L01 Section 4 item 1 now cites 'Assumption 2.1(a)-(c)'; the claim (B~ has the same finite-dimensional laws and discontinuous paths on every outcome; L01.html:215-216, 234) is unchanged in substance. Assumption 2.1 has parts (a)-(c) (course/modules/SC/SC1/L02.html:93-99), so the new reference resolves. L05.html:59-71 and 271-289 are unchanged (L05 hunks at 332, 334 only). L06: Cor 1.4 (87-94), Lemma 2.1 (105-115), Theorem 2.5 (153-166), Cor 2.6 (174-181) unchanged; the tau_a definition at L06.html:102 is still `tau_a=inf{s>=0 : B_s=a}`, with the paragraph now naming Proposition 2.7. The new Proposition 2.7 (L06.html:184-208) is cited by neither L07 nor L08 (grep).",
    ),
    "cards-dup-and-numbers": (
        "course/modules/SC/SC1/cards.json",
        f"Re-run this round on the full file (227 cards, was 217): no duplicate id, front or back; every numeric token of the 53 L07/L08 cards occurs in its lesson page ({S}cards_r1.txt; script ledgers/SC1/scripts/SC1-c-r1/sc1c_cards_r1.py).",
    ),
    "cards-L07-L08-full-read": (
        "course/modules/SC/SC1/cards.json (L07: 28 cards; L08: 25 cards)",
        "Re-read this round against the current lesson text. Changed or new cards (7): SC1-c157 (L07 Problem R2; L07.html:499-502: {M_H>=b} increase to {M_H>a} as b down to a, continuity from below plus Theorem 1.3; matches). SC1-c159 (L07 Problem E3; L07.html:481-484: sqrt(x(n-x)/(n^2(n-1))), x=121, n=400 gives sqrt(33759/63840000)=0.0230; the wording now says x as the lesson does, which resolves the round-13 observation). SC1-c171 (L08 Part A: counts 512,0,384,0,288,0,224,0,180,0 for steps 3 to 12, sum 1588; matches the expected block at L08.html:344-363 and the interpretation at L08.html:364). SC1-c174 (L08 Part D: P(tau_1<=1)=0.317311 and P(tau_1<=2)=0.479500; both printed in the expected block; 0.479500 = erfc(0.5) = 0.4795001). SC1-c201 (L08 misconception at L08.html:384-385: factor 2 from Corollary 1.3, which runs through Theorem 2.5 of Lesson 6, as L08.html:83 states; matches). SC1-c241 (L08 Part A: 1588/4096=0.387695 and 794/4096=0.193848, both printed in the expected block). SC1-c242 (L08 Part D densities 0.241971 and 0.109848, printed with 'agree to 1e-8: True'; recomputed as f_1(1)=0.241971, f_1(2)=0.109848). Grades: c157, c159, c201 T with proof on the page; c171, c174, c241, c242 C with the lab named; all match. " + CARDS_PREFIX.format(ids=OTHER46) + "carried (the lessons are byte-identical).",
    ),
    "cards-no-A5-L05-lesson-scope": (
        "cards.json SC1-c149, c150, c174, c215, c137, c139, c140",
        "Re-run this round: a scan of all 227 cards finds A5 only in SC1-c140 and SC1-c215 (cards.json, out/cards_r1.txt). The changed card SC1-c174 no longer mentions A5; its basis names Corollaries 1.3 and 1.5 under A3 and A4 only. c137, c139, c149, c150 do not mention A5. Assumption A5 is labelled in L07 only (Corollary 1.5(b) at L07.html:88-92 and Problem text at L07.html:96-99), and c140 and c215 say so.",
    ),
    "cards-changed-r11-L07-L08": (
        "cards.json SC1-c149, c150, c162, c165, c171, c201, c229, c230",
        "Mixed. Re-read this round: SC1-c171 and SC1-c201 (changed since the round-13 pin; both match the current lessons, see cards-L07-L08-full-read). Carried from round 13 (cards SC1-c149, c150, c162, c165, c229, c230 byte-identical card-level since e919577b): c149 gives 0.2275 and 0.3025 with SE 0.0210 and 0.0230 (matches L07 Part B), c150 gives 0.7586 with SE 0.0317, c162 gives Proposition 1.2, c165 gives the density f_a, c229 and c230 match the L07 expected block and interpretation.",
    ),
}

carry_special = {
    "canon-breaks-L07-L08": "Carried from round 13 (course/modules/SC/SC1/L07.html, L08.html; and L05.html:59-71, 271-281 and L06.html:105-115 in the cited ranges byte-identical since e919577b; L06 hunks at 52, 102, 119, 148-149 and 183+ and L05 hunks at 332, 334 leave them in place): ",
    "math-L07-thm-1.3": "Carried from round 13 (course/modules/SC/SC1/L07.html:67-80 byte-identical; L01.html:58-64 and L06.html:153-181 unchanged in the cited ranges since e919577b): ",
    "math-L08-prop-1.2-cor-1.3-1.4": "Carried from round 13 (course/modules/SC/SC1/L08.html:62-94 byte-identical; L06.html:174-181 (Cor 2.6) unchanged since e919577b; L07.html:67-80 unchanged): ",
    "term-walk-identity-L07": "Carried from round 13 (course/modules/SC/SC1/L07.html, tests/labs/SC1/lab-SC1-L07-1.py byte-identical; L06.html:87 (Cor 1.4) unchanged since e919577b): ",
    "dag-reflection-link-L07-L08": "Carried from round 13 (L07.html, L08.html byte-identical since e919577b); re-checked this round: check_dag PASS and the L06 anchor `id=\"s2\"` at L06.html:100 is present. ",
    "dag-defined-once-L07-L08": "Carried from round 13 (L07.html, L08.html byte-identical since e919577b); re-checked this round: check_dag PASS. ",
    "structure-L07": "Carried from round 13 (L07.html byte-identical since e919577b); re-checked this round: check_pages PASS. ",
    "structure-L08": "Carried from round 13 (L08.html byte-identical since e919577b); re-checked this round: check_pages PASS. ",
    "notation-macros": "Carried from round 13 (L07.html, L08.html byte-identical; notation/notation.json not in the e919577..HEAD change list): ",
    "notation-T-first-passage-index": "Carried from round 13 (L07.html, L08.html byte-identical; notation/notation.json unchanged since e919577b): ",
    "notation-kappa-redefined": "Carried from round 13 (L07.html, L08.html byte-identical; notation/notation.json unchanged since e919577b): ",
    "notation-star-superscript-L08": "Carried from round 13 (L08.html byte-identical; notation/notation.json unchanged since e919577b): ",
    "notation-horizon-H": "Carried from round 13 (L07.html, L08.html byte-identical; notation/notation.json unchanged since e919577b): ",
    "notation-n-steps-L08": "Carried from round 13 (L08.html and tests/labs/SC1/lab-SC1-L08-1.py byte-identical; notation/notation.json unchanged since e919577b): ",
    "grader-and-mutants-not-applicable": "Carried from round 13 (slice c has no grader; the course/modules/SC/SC1/grader files changed in the project slice, not in this slice): ",
}
cards_carry = {
    "cards-c140-substitution": "SC1-c140",
    "cards-c150-gap": "SC1-c150",
    "cards-basis-A3-dependence": "SC1-c137, c139, c140, c145, c149, c150, c164, c165",
    "cards-c205-new": "SC1-c205",
    "cards-c215-A5-card": "SC1-c215",
    "cards-c218-new": "SC1-c218",
    "cards-c151-removed-coverage": "SC1-c143-c146, c152-c154 (c151 absent in both)",
    "cards-c150-c170-changed-text": "SC1-c150, c170",
    "cards-c229-c230-new": "SC1-c229, c230",
    "cards-L07-misconception-same-law": "SC1-c191",
    "num-L08-z-values": "SC1-c173",
    "delta-round9-carried-fail-fixed": "SC1-c140",
    "cards-L07-misconception-same-law": "SC1-c191",
}

rows = []
for rid, b in base_rows.items():
    if rid in fresh:
        loc, ev = fresh[rid]
        rows.append({"id": rid, "check": b["check"], "location": loc, "status": "PASS", "evidence": ev})
    elif rid in cards_carry:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                     "evidence": CARDS_PREFIX.format(ids=cards_carry[rid]) + b["evidence"]})
    elif rid in carry_special:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                     "evidence": carry_special[rid] + b["evidence"]})
    else:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                     "evidence": PAGE_PREFIX + b["evidence"]})

# cards-changed-r11 and full-read keep their fresh text; the carried-cards reference is embedded there.
assert all(r["status"] == "PASS" for r in rows)
assert [r["id"] for r in rows] == [r["id"] for r in base["rows"]]

summary = {"rows": len(rows), "pass": len(rows), "fail": 0, "unverifiable": 0, "mutants_killed": 0, "mutants": 0}
frag = {
    "unit": "SC1",
    "slice": "c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08, lab twins), closing delta round 1 (ruling 30); did not build SC1",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (detached, /Users/billyribeiro/.fanout/wt/verifyF31-SC1-c)",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin; round-13 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round13.json, 108 rows, all PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-SC1-c (detached at 95f3f8cb; .venv symlinked)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r1/out/",
    "verified_at": "2026-11-09T16:34:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta e919577b..95f3f8cb over the slice paths: course/modules/SC/SC1/L07.html, L08.html and tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py are byte-identical (git diff empty). Changed in the slice: course/modules/SC/SC1/cards.json only (card-level diff: changed SC1-c157, c159, c171, c174, c201; added SC1-c241, c242; c217 removed is an L06 card, another slice). Every changed or new L07/L08 card is re-verified in cards-L07-L08-full-read.",
        "Cross-slice subjects whose cited locators changed: L01.html:211-235 (text only; re-verified in xref-L01-L05-L06), L06.html (Proposition 2.7 inserted after line 183; cited L06 lines 87-181 unchanged; no L07/L08 text cites Remark 2.4 or Proposition 2.7 of Lesson 6), references/references.json (generated_at and one used_by list; re-run), plans/SC1-build-plan.md and SC1-open-items.md (project section 5.5 and 5.7(4) and the L06 open item only; no L07/L08 requirement changed), curriculum (M4 brief only; no SC1 line), pyproject.toml (ruff exclude only).",
        "Round-13 observation resolved: card SC1-c159 now says 'x successes', as L07.html:482 does.",
        "Observation, not a row (carried from round 13): the L08 twin docstrings (tests/labs/SC1/lab-SC1-L08-1.py lines 21-22 and the part_c docstring near line 147) say the exact truncated mean is 'from Part B'; part_c recomputes it. The printed values are right, so no printed claim is wrong.",
        "Observation, not a row (carried from round 13): the L08 lab twin uses n for the walk length (lines 6-15) while the prose uses N; neither letter is registered in notation/notation.json.",
        "No mutants were authored (ruling 37). The slice has no grader, so no mutant applies; the standing SC1 project mutant set belongs to the project slice.",
        "Ruling 26 kinds: no FAIL found in the delta. Each changed subject was re-derived from its own lesson text, the lab expected blocks and independent arithmetic (sqrt(33759/63840000), 1588/4096, 794/4096, erfc(0.5), f_1(1), f_1(2)).",
    ],
    "summary": summary,
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", OUT, summary)
