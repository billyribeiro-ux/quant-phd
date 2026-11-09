import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyF11-E2-c")
BASE = json.load(open("/Users/billyribeiro/.fanout/frags/C-E2-c.round7.json", encoding="utf-8"))
base_rows = {r["id"]: r for r in BASE["rows"]}

PREFIX = ("Carried from round 7 (L07.html, L08.html, L09.html and the lab twins tests/labs/E2/lab-E2-L07/08/09-1.py "
          "byte-identical since the base pin 0d2d0f3f; sha256 in ledgers/E2/scripts/E2-c-r1/out/slice_pages_twins_hashes.out): ")

# Rows whose cited subject is unchanged since the base pin: carry the base evidence verbatim with the prefix.
CARRY = [
    "E2c-l07-numbers", "E2c-l08-numbers", "E2c-l07-prop2.2", "E2c-l07-lemma3.1", "E2c-l07-prop3.2",
    "E2c-l07-prop3.2-hypothesis", "E2c-l07-prop-3.1-example", "E2c-l07-remark2.4-signaling",
    "E2c-l07-quiz-items", "E2c-l07-problem-set", "E2c-l07-key-results", "E2c-l07-misconceptions",
    "E2c-l07-notation-xstar", "E2c-dag-outside-closure", "E2c-attributions", "E2c-hours",
    "E2c-lab-claims-match-output", "E2c-lab-docstring-claims", "E2c-delta-r5-hunks",
    "E2c-define-before-use-forward-ref", "E2c-l08-prop2.1", "E2c-l08-prop2.2", "E2c-l08-remark2.3-grade",
    "E2c-l08-continuous-analogue", "E2c-l08-remark3.2", "E2c-l08-quiz-items", "E2c-l08-problem-set",
    "E2c-l09-prop2.1", "E2c-l09-prop3.2-prop4.1", "E2c-l09-numbers", "E2c-l09-grades", "E2c-l09-quiz-items",
    "E2c-l09-problem-set", "E2c-l09-why-it-matters", "E2c-l08-why-it-matters-def1.2",
    "E2c-cards-l08-c091-c100", "E2c-cards-l08-c101-c103-c106", "E2c-cards-l08-c104", "E2c-cards-l08-c105", "E2c-l08-prop2.1",
]

FRESH = {}

FRESH["E2c-gate-check-pages"] = dict(
    check="2.9 structure (check_pages)",
    location="course/modules/E/E2/L07.html, L08.html, L09.html",
    status="PASS",
    evidence="Re-run at pin 95f3f8cb: `.venv/bin/python tools/check_pages.py --unit E2 --page L07|L08|L09` -> 'check_pages E2 L07: PASS', L08 PASS, L09 PASS, exit 0 each (out/check_pages_L07.out, L08, L09).")
FRESH["E2c-gate-check-dag"] = dict(
    check="2.9 DAG (check_dag)",
    location="course/modules/E/E2/L07-L09.html",
    status="PASS",
    evidence="Re-run at pin 95f3f8cb: `tools/check_dag.py --unit E2` -> 'check_dag E2: PASS', exit 0 (out/check_dag.out). Outside-closure reading in E2c-dag-outside-closure (carried).")
FRESH["E2c-gate-run-labs"] = dict(
    check="2.5 labs (run_labs)",
    location="tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py",
    status="PASS",
    evidence="Re-run at pin 95f3f8cb: `tools/run_labs.py --unit E2 --page L07|L08|L09` -> each 'run_labs E2: PASS (1/1)', exit 0 (out/run_labs_L07.out, L08, L09).")
FRESH["E2c-gate-page-smoke"] = dict(
    check="2.9 page_smoke (run alone)",
    location="course/modules/E/E2/L07.html, L08.html, L09.html",
    status="PASS",
    evidence="Re-run one page at a time at pin 95f3f8cb: `tools/page_smoke.py --unit E2 --pages L07` (then L08, then L09) -> 'page_smoke E2: PASS', exit 0 each (out/page_smoke_L07.out, L08, L09). Visual 360 px not inspected by eye. `timeout` is not installed on this Mac, so the runs were not time-limited by it.")
FRESH["E2c-twins-isolated"] = dict(
    check="2.5 twins under python -I -W error",
    location="tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py",
    status="PASS",
    evidence="Re-run at pin 95f3f8cb from a fresh empty temp directory: `python -I -W error <twin>` -> exit 0, stderr 0 bytes for L07, L08, L09 (out/twin_compare.out; L08 stdout in out/twin_L08_stdout.txt).")
FRESH["E2c-page-code-equals-twin"] = dict(
    check="2.5 page code equals twin",
    location="L07.html line 164, L08.html line 141, L09.html line 95 (data-run block) vs the three twins",
    status="PASS",
    evidence="ledgers/E2/scripts/E2-c-r1/twin_compare.py: html.unescape of each data-run block equals the twin exactly except for one trailing newline that the embed strips (rstrip-equal True for L07, L08, L09; out/twin_compare.out).")
FRESH["E2c-expected-equals-output"] = dict(
    check="2.5 expected block equals output",
    location="L07.html:307, L08.html:252, L09.html:223 pre.expected",
    status="PASS",
    evidence="twin_compare.py: unescaped pre.expected equals stripped stdout of the isolated twin run for L07 (1540 chars), L08 (569) and L09 (647) (out/twin_compare.out: 'expected == stdout (strip): True' x3).")
FRESH["E2c-ruff-mypy-pytest"] = dict(
    check="gates (ruff, mypy, pytest)",
    location="tests/labs/E2/*.py; tests/test_labs.py",
    status="PASS",
    evidence="`.venv/bin/ruff check tests/labs/E2` -> 'All checks passed!'; `ruff format --check tests/labs/E2` -> '12 files already formatted'; `mypy --no-incremental` -> 'Success: no issues found in 386 source files' (repo has grown since the base's 229); `pytest tests/test_labs.py -k E2 -q` -> 15 passed (out/ruff_check.out, ruff_format.out, mypy.out, pytest_labs_E2.out).")
FRESH["E2c-verify-refs-offline"] = dict(
    check="2.1 registry integrity (verify_refs --offline)",
    location="references/references.json",
    status="PASS",
    evidence="references/references.json changed since the base pin (generated_at, and used_by lists for BK1/BK4, DV1/FC2, E9/LX1 only; git diff 0d2d0f3f..95f3f8cb -- references/references.json). `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out). The online run was not repeated: plain curl access to Crossref and the publisher pages was not attempted, and no bibliographic field of any L07-L09 citation changed.")
FRESH["E2c-cards-l07-c076-c085"] = dict(
    check="2.7 cards (L07 c076-c085)",
    location="course/modules/E/E2/cards.json E2-c076 to E2-c085 (c080, c081 changed since base pin)",
    status="PASS",
    evidence="c080 (changed): 'For one agent with finite type, message and outcome sets, every equilibrium outcome ... (Definition 2.1; Proposition 2.2)' matches L07 Assumption 3 (finite Theta, M, X; one agent), Definition 2.1 and Proposition 2.2; no grade (theorem statement, BUILDER_RULES section 7). c081 (changed): T, 'Not established ... nothing is proved for several agents' matches L07 Assumption 3 and section 4 ('not proved on this page'). c076-c079, c082-c085 byte-identical since 0d2d0f3f (cards_scan and per-card compare, out/slice_cards_delta.out).")
FRESH["E2c-cards-l07-c086-c090"] = dict(
    check="2.7 cards (L07 c086-c090)",
    location="cards.json E2-c086 to E2-c090 (c087, c088, c090 changed since base pin)",
    status="PASS",
    evidence="c087 (changed): 'In Lab 1 Part C ... low-price tie-break ... 6000 cents. The lab does not show that this menu is optimal.' C, basis 'Lab 1, Part C'; matches the L07 Part C output line 'induced_revenue_cents 6000' (lesson text line 370 and 'The lab does not show that either menu is optimal'). c088 (changed): T, 'With c < 0 the optimum excludes type L (Proposition 3.2). Any q_L > 0 gives type H a rent of at least Delta q_L (Lemma 3.1)': Lemma 3.1 gives U_H >= U_L + Delta q_L and U_L >= 0 by IR, so U_H >= Delta q_L; Proposition 3.2 with c < 0 gives the unique maximiser q_L = 0. c090 (changed): C, basis 'Lab 1, Part C', prints 6000 and 4200 (Part C output lines 'induced_revenue_cents 6000' and 'tie_break_declines_for_L_revenue_cents 4200'); 'No' follows from Proposition 2.2 (lesson section 2 and section 5 item 3). c086, c089 byte-identical since base pin.")
FRESH["E2c-cards-l07-c134"] = dict(
    check="2.7 cards (new card E2-c134, L07)",
    location="cards.json E2-c134",
    status="PASS",
    evidence="New since the base pin. C, basis 'Lab 1, Part C (enumeration of the induced menu)'. Back '4200 cents ...' matches Part C output 'tie_break_declines_for_L_revenue_cents 4200' and the L07 text (Part C paragraph: 'a second induced menu ... earns 4200 cents, so the choice of equilibrium changes the direct mechanism'; 'The lab does not show that either menu is optimal'). No duplicate front or back (cards_scan_head.out).")
FRESH["E2c-cards-l09-c107-c121"] = dict(
    check="2.7 cards (L09 c107-c121)",
    location="cards.json E2-c107 to E2-c121 (c107, c114, c117, c119, c120 changed; c108-c113, c115, c116, c118, c121 identical); new E2-c135 is in row E2c-cards-l09-c135",
    status="PASS",
    evidence="c107 (changed): 'the k highest bids win and each winner pays the clearing bid b(k+1), not its own bid (Definition 1.1)' matches L09 Definition 1.1. c114 (changed): T, 'uniform-price winner pays b(2) ... discriminatory winner pays its own highest bid b(1) ... (Proposition 4.1, with k = 1)' matches Proposition 4.1 and its proof (L09 lines 273-282). c117 (changed): C, basis 'Lab 1, Part C (exhaustive enumeration of 256 profiles)', '256 of 256' matches output line 'uniform_winner_pays_second_highest 256 of 256' and text 'on all 256 profiles the uniform winner pays the second-highest bid'. c119 (changed): T, '7/8: 14000 against 16000 (Lab 1, Part A; Remark 3.3)' matches output 'value_of_winners_cents 14000', 'value_of_top_values_cents 16000', 'efficiency 7/8' and Remark 3.3. c120 (changed): T, '4w + 1 ... 1, 5, 9 and 13 for w = 0 to 3 (Research problem R1, using Proposition 2.1)' re-derived: fixed w, profiles with exactly three bids w and fourth x < w give 4w; all four equal to w adds 1; 1+5+9+13 = 28 = Part B 'discriminatory_equal_uniform 28'. Both numbers 4w+1 and 1,5,9,13 appear in the R1 solution (L09 line 397). Unchanged cards byte-identical (out/slice_cards_delta.out).")
FRESH["E2c-cards-l09-c135"] = dict(
    check="2.7 cards (new card E2-c135, L09)",
    location="cards.json E2-c135",
    status="PASS",
    evidence="New since the base pin. T: 'The gap is 3500 cents, which is 25% of the uniform revenue of 14000 cents (Lab 1, Part A)'. 17500 - 14000 = 3500; 3500 / 14000 = 0.25. The same numbers are in L09 E3 (Part A) and the key-results row 'discriminatory revenue exceeds the uniform revenue by 25%' (grade T). Card grade T agrees with the lesson's grade.")
FRESH["E2c-cards-duplicates"] = dict(
    check="2.7 cards (duplicate scan)",
    location="course/modules/E/E2/cards.json (135 cards now; L07-L09 = c076-c121 and c134, c135)",
    status="PASS",
    evidence="ledgers/E2/scripts/E2-c-r1/cards_scan.py on HEAD: 135 cards, 135 unique ids, sorted, ids E2-c001..E2-c135; dup fronts [], dup backs [] (out/cards_scan_head.out). Base had 125 cards (out/cards_scan_base.out). Key sets and grade values valid: C cards all have a basis, T and None cards have no basis.")
FRESH["E2c-cards-grades"] = dict(
    check="2.3 grades (card vs lesson)",
    location="cards.json E2-c076 to E2-c121, E2-c134, E2-c135 (L07-L09)",
    status="PASS",
    evidence="Every changed or new L07-L09 card compared with its lesson grade: c087, c090, c134 C (Lab 1 Part C prints); c117 C (enumeration, Part C); c081, c088, c114, c119, c120, c135 T (derivations or Propositions in the lesson, proved on the page; key rows T). Ungraded cards (c076-c080, c091-c093, c107-c110, c112) are unchanged since the base pin and carry no grade by design (definitions and the theorem statement c080). Unchanged cards carried from the base. No registered notation symbol (T, R*, R^e*, R_f, Phi, gamma_3, gamma_4, Q) appears in any L07-L09 card (scan in E2c-notation-registry).")
FRESH["E2c-banned-and-process-words"] = dict(
    check="2.9 banned phrases and process words",
    location="cards.json L07-L09 cards (fresh); L07.html, L08.html, L09.html text (carried, byte-identical)",
    status="PASS",
    evidence="Regex scan of all L07-L09 card front/back/basis for round, revise, correct, now, changed, fixed, verifier, builder, previous, earlier, updated, delta, ruling, finding: only 'Delta' (the mathematical symbol) and 'fixed' (fixed bid, fixed offset, fixed shading) match; no process words (ledgers/E2/scripts/E2-c-r1, inline scan).")
FRESH["E2c-notation-registry"] = dict(
    check="2.4 notation",
    location="L07.html, L08.html, L09.html math spans (carried); cards.json L07-L09 (fresh)",
    status="PASS",
    evidence="Symbol scan of all L07-L09 card text: no use of T, Q, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f (notation/notation.json, 8 registered symbols). New card symbols k, w, b(k+1), c, q_L, U_H, Delta, p_H have no registry entry, so no conflict. Page math carried from base (pages byte-identical).")
FRESH["E2c-html-structure"] = dict(
    check="2.9 structure",
    location="L07.html, L08.html, L09.html",
    status="PASS",
    evidence="Re-run at pin 95f3f8cb: check_pages PASS for L07, L08, L09 and page_smoke PASS for each page alone (out/check_pages_L0*.out; out/page_smoke_L0*.out). Heading order, grade legend and key-results table are byte-identical since 0d2d0f3f.")
FRESH["E2c-l08-simulation-reproduction"] = dict(
    check="2.5 lab / SIMULATED",
    location="tests/labs/E2/lab-E2-L08-1.py (seed 20261028)",
    status="PASS",
    evidence="Re-run of the twin under python -I -W error at pin 95f3f8cb (out/twin_L08_stdout.txt): naive winner profit total -26620718, naive SE 79810, exact -26673331, shaded 59282, shaded SE 79810 (not repeated), exact shaded 6669; equal to the L08 expected block (twin_compare.out 'expected == stdout: True'). The SIMULATED labelling is in the module docstring and page, both byte-identical since the base pin.")
FRESH["E2c-delta-r6-hunks"] = dict(
    check="2.9 delta (round-6 hunks, re-read)",
    location="L08.html lines 57, 289; L09.html lines 243, 397; cards.json E2-c080, c081, c088, c117, c120 (changed again in this delta)",
    status="PASS",
    evidence="The L07 line 359 and L08 line 289 hunks of the earlier delta are byte-identical since 0d2d0f3f (git diff --stat empty for the L07-L09 pages and twins). The cards named here changed again in the current delta and are re-read in E2c-cards-l07-c076-c085, E2c-cards-l07-c086-c090 and E2c-cards-l09-c107-c121. Cards c098, c100, c105 are byte-identical to the base pin.")
FRESH["E2c-delta-r7-hunks"] = dict(
    check="2.9 delta (current delta 0d2d0f3f..95f3f8cb, slice paths)",
    location="course/modules/E/E2/cards.json only (pages and twins: no change); new E2-c134 (L07), E2-c135 (L09)",
    status="PASS",
    evidence="`git diff --stat 0d2d0f3f..95f3f8cb -- course/modules/E/E2/L07.html L08.html L09.html tests/labs/E2/lab-E2-L0{7,8,9}-1.py` is empty. `git diff` on cards.json: 170 lines changed. Slice cards changed: c080, c081, c087, c088, c090, c107, c114, c117, c119, c120; new: c134, c135 (out/slice_cards_delta.out; ledgers/E2/scripts/E2-c-r1/cards_scan.py). Other changed cards (c002-c074, c125, c126-c133) belong to slices L01-L06 and are outside this slice.")

FRESH["E2c-notes-no-row-cards-l07-c080"] = dict(
    check="2.7 cards (theorem card without grade)",
    location="cards.json E2-c080",
    status="PASS",
    evidence="E2-c080 is a theorem statement (revelation principle, one agent, finite sets) with no grade field; BUILDER_RULES section 7 requires a grade only for graded results other than a theorem. Its back matches Assumption 3, Definition 2.1 and Proposition 2.2 (see E2c-cards-l07-c076-c085). Not counted.")

rows = []
for rid in base_rows:
    if rid in FRESH:
        f = FRESH[rid]
        rows.append({"id": rid, "check": f["check"], "location": f["location"], "status": f["status"], "evidence": f["evidence"]})
    elif rid in CARRY:
        b = base_rows[rid]
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": b["status"],
                     "evidence": PREFIX + b["evidence"]})
    else:
        raise SystemExit("unhandled base row " + rid)
for rid in ("E2c-cards-l07-c134", "E2c-cards-l09-c135", "E2c-delta-r7-hunks"):
    pass
for rid in ("E2c-cards-l07-c134", "E2c-cards-l09-c135", "E2c-delta-r7-hunks"):
    f = FRESH[rid]
    rows.append({"id": rid, "check": f["check"], "location": f["location"], "status": f["status"], "evidence": f["evidence"]})

missing_from_base = [k for k in CARRY + list(FRESH) if k not in base_rows and k not in ("E2c-cards-l07-c134", "E2c-cards-l09-c135", "E2c-delta-r7-hunks")]
assert not missing_from_base, missing_from_base
unhandled = [k for k in base_rows if k not in FRESH and k not in CARRY]
assert not unhandled, unhandled

statuses = [r["status"] for r in rows]
verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"

fragment = {
    "unit": "E2",
    "slice": "c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for E2-c round 1 (did not build E2; no context shared with the builders)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "0d2d0f3f8ffb68fc54bb854cb1d7bf28e6483e78 (round-7 pin; base fragment /Users/billyribeiro/.fanout/frags/C-E2-c.round7.json used as the base: PASS rows carried only where the cited subject is byte-identical)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF11-E2-c",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyF11-E2-c/ledgers/E2/scripts/E2-c-r1",
    "verified_at": "2026-11-09T15:30:41+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lab-only slice (lessons L07-L09, their three twins, and the L07-L09 cards): mutation testing applies to project graders only, so mutants is empty by design; no mutants were written or run.",
        "Delta 0d2d0f3f..95f3f8cb inside the slice: cards.json only. L07.html, L08.html, L09.html and the three twins are byte-identical to the base pin (sha256 in out/slice_pages_twins_hashes.out).",
        "Changed slice cards: E2-c080, c081, c087, c088, c090, c107, c114, c117, c119, c120. New slice cards: E2-c134 (L07), E2-c135 (L09). All re-read against the unchanged lesson text.",
        "references/references.json changed (generated_at and used_by lists only). verify_refs --offline re-run; the online run was not repeated.",
        "Repo-wide changes outside the slice (tools/curriculum/hub/other units) were not verified here; the slice gates were re-run at the pin.",
        "Card-grade convention: T cards without basis (c081, c088, c114, c119, c120, c135) are derivations or propositions proved on the page, as accepted in the base round-7 resolution of c098/c100/c105; C cards carry basis.",
        "Not run: build_site --check, render_curriculum, check_projects and run_graders (not in this slice's gate list); the full pytest suite; the 360 px visual render by eye; the online verify_refs run.",
    ],
    "summary": "",
}
n_pass = sum(1 for s in statuses if s == "PASS")
fragment["summary"] = (
    f"Slice E2-c (L07-L09 pages, twins, L07-L09 cards) at 95f3f8cb, round 1: {verdict}. "
    f"{len(rows)} rows: {n_pass} PASS, {len(rows) - n_pass} non-PASS. Gates re-run at the pin: check_pages, check_dag, run_labs, page_smoke (one page at a time), "
    "twins under python -I -W error, page-code and expected-block equality, ruff, mypy, pytest test_labs -k E2, verify_refs --offline: all pass. "
    "Changed cards were re-derived against the unchanged lesson text; the two new cards were checked fresh."
)

out = ROOT / "ledgers/E2/E2-c.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "verdict", verdict, "pass", n_pass)
