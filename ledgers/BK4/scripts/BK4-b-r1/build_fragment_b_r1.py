"""Build ledgers/BK4/BK4-b.json (round 1, delta from base round 11) from the base fragment.

Carries every base PASS row whose cited lines/objects are byte-identical since 11d7077a,
replaces the rows whose subject changed with fresh evidence, and adds the new delta rows.
Run from the checkout root: python3 -I ledgers/BK4/scripts/BK4-b-r1/build_fragment_b_r1.py
"""

import json

BASE = "/Users/billyribeiro/.fanout/frags/E-BK4-b.round11.json"
OUT = "ledgers/BK4/BK4-b.json"
S = "ledgers/BK4/scripts/BK4-b-r1/"
PREFIX = "Carried from round 11 (cited lines/objects byte-identical since the previous pin 11d7077a; {what}):"

base = json.load(open(BASE, encoding="utf-8"))

# Rows whose subject changed in 11d7077a..HEAD, or that are gate/command rows re-run this round.
fresh = {
    "BK4b-gate-check-pages": ("PASS", "Re-run on 95f3f8cb: .venv/bin/python tools/check_pages.py --unit BK4 -> 'check_pages BK4: PASS', exit 0 (" + S + "check_pages.txt). L05.html changed at line 486 only; the page structure gate covers it."),
    "BK4b-gate-check-dag": ("PASS", "Re-run: tools/check_dag.py --unit BK4 -> 'check_dag BK4: PASS', exit 0 (" + S + "check_dag.txt). L04 links L01.html#def-settlement-cycle; L01.html changed at lines 55, 71, 80 and others only, so the anchor (L01.html:64) and Definition 1.2 (L01.html:63) are unchanged; concepts.html:483 (bank-money-creation anchor) is in a file not changed since 11d7077a."),
    "BK4b-gate-check-projects": ("PASS", "Re-run: tools/check_projects.py --unit BK4 -> 'check_projects BK4: PASS', exit 0 (" + S + "check_projects.txt). project.html and grader are slice c; this row only confirms the gate still runs on the BK4 projects."),
    "BK4b-run-labs": ("PASS", "Re-run: tools/run_labs.py --unit BK4 -> 'run_labs BK4: PASS (8/8)', exit 0 (" + S + "run_labs.txt)."),
    "BK4b-twin-isolated-run": ("PASS", "Re-run: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L04-1.py and lab-BK4-L05-1.py both exit 0 with empty stderr (" + S + "L04_twin_exit.txt, L05_twin_exit.txt, L04_twin.err and L05_twin.err are 0 bytes). Both twins are byte-identical to 11d7077a."),
    "BK4b-twin-lint": ("PASS", "Re-run: repo-wide .venv/bin/ruff check . -> 'All checks passed!', exit 0 (" + S + "ruff_check.txt); ruff format --check . -> '555 files already formatted' (" + S + "ruff_format.txt); mypy --no-incremental on both slice twins -> 'Success: no issues found in 2 source files' (" + S + "mypy_labs.txt)."),
    "BK4b-pytest-labs": ("PASS", "Re-run: .venv/bin/python -m pytest tests/test_labs.py -k BK4 -q -> 8 tests passed (eight dots), exit 0 (" + S + "pytest_labs.txt)."),
    "BK4b-page-smoke": ("PASS", "Re-run alone: tools/page_smoke.py --unit BK4 --pages modules/BK/BK4/L04.html modules/BK/BK4/L05.html -> 'page_smoke BK4: PASS', exit 0 (" + S + "page_smoke_alone.txt)."),
    "BK4b-verify-refs": ("PASS", "Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline.txt). references.json changed only at line 3 (generated_at) and at the Black & Scholes used_by entry (hunk -2925); bisndbasel lines 2815-2842 are unchanged."),
    "BK4b-verify-refs-unit-scope": ("PASS", "Re-run: tools/verify_refs.py --unit BK4 -> 'live re-verification of BK4: 3 of 560 entries, 0 problems', exit 0 (" + S + "verify_refs_unit.txt). Entries at references/references.json:2815-2842 are unchanged since 11d7077a."),
    "BK4b-build-site-check": ("PASS", "Re-run: tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 (" + S + "build_site_check.txt). course/assets/data/program.json changed (two project briefs in other units); the check passes on 95f3f8cb."),
    "BK4b-render-curriculum": ("PASS", "Re-run: tools/render_curriculum.py -> 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)', exit 0; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json -> exit 0 (" + S + "render_curriculum.txt, render_curriculum_diff.txt). BK4 hours are unchanged."),
    "BK4b-cmd-recompute": ("PASS", "Re-run of ledgers/BK4/scripts/BK4-b-r11/recompute_r11.py with python -I on 95f3f8cb -> 60 checks, 'ALL OK' (" + S + "recompute_r11_rerun.txt). Plus a new exact-fraction script for the changed Example 2.8 and Propositions 2.1 to 2.6 (" + S + "recompute_b_r1.py, output " + S + "recompute_b_r1.txt): mean 4375/2 under both joint laws, variances 57421875/4 (A3) and 133984375/4 (A4), difference 19140625 = 2 kappa^2 p(1-p) sum_{i<j} l_i l_j, 1-(7/8)^3 = 169/512, 1/8 = 64/512, 3p = 192/512, 2188 cents = 21.88 dollars, equal delays 2 give 1875."),
    "BK4b-numbers-L05-prose": ("PASS", "L05.html:84-152 and :335-337, :384-386, :393, :429-436 are unchanged since 11d7077a (the one changed line in L05.html is :486). Line :486 (key-results row) and Example 2.8 (:153) were re-derived: 2187.5 = (1/8)(2500)(7) = 17500/8 = 4375/2; rounding half up gives 2188; 2188 cents = 21.88 dollars exactly (Example 2.8, E1 solution at :429). Lab 1 Part B prints '4375/2 cents' and '2188 cents' (" + S + "L05_twin_stdout.txt lines 15-18 and 28-29)."),
    "BK4b-key-results-L05": ("PASS", "Re-verified: the table at L05.html:474-491 changed only at row :486, now 'At p=1/8, kappa=2500 and ell=(1,2,4) (Example 2.8), the exact expected cost is 4375/2 cents, which rounds half up to 2188 cents', grade T, keys 'Example 2.8 (Proposition 2.1 at p = 1/8, kappa = 2500, ell = (1, 2, 4); the rounding rule of Lab 1, applied once to 2187.5); Lab 1 Part B prints 4375/2'. Example 2.8 (L05.html:152-153) is a numbered Example, derived on the page from Proposition 2.1, so T with Example 2.8 as basis is the Architect ruling 13 grade. Cards BK4-c086 and BK4-c094 carry the same grade (T) and the same basis (Example 2.8). Rows :480-484 and :487 re-read: T rows match Propositions 2.1, 2.2, 2.4, 2.5, 2.6 and Example 2.7 (L05.html:84-146, 147-148); :487 stays C naming Lab 1 Part D."),
    "BK4b-cards-L04-L05-scan": ("FAIL", "cards_r1.py (" + S + "cards_r1.py, output " + S + "cards_r1.txt): 'cards in L04/L05: 33', 'numbers not found in own lesson text: none'. Changed L05 objects re-read against the page: BK4-c086 (Example 2.8, 4375/2, T), BK4-c089 (Example 2.7, T), BK4-c090 (Proposition 2.1 at ell=2, Problem M3 at L05.html:388-394, 1875, T), BK4-c094 (2188, T) all match. BK4-c088 FAILS: its front reads 'Assuming the finite probability space, A1 and A2, with A4 for comonotone failures, do dependent failures cost more on average than independent failures (Proposition 2.4)?' and its back and basis cite Proposition 2.2 ('the same as under A3 (Proposition 2.2)'), but Proposition 2.2's hypotheses include A3 (L05.html:95: 'the finite space of Assumption 1.3, and A1, A2 and A3'), and the front never assumes A3 (the round-11 front did: 'with A3 for independent failures and A4 for comonotone failures'). Card hypotheses must carry the hypotheses of the cited propositions (BUILDER_RULES; verifier rules class 10). The card removed the A3 hypothesis in this delta. c100 removed (its content is BK4-c080 and BK4-c088); L05 card count 15 -> 14, L04 unchanged at 19."),
    "BK4b-cards-duplicates": ("PASS", "cards_r1.py: 'total cards: 100 ids unique: True'; 'duplicate fronts across all cards: none'; 'duplicate backs across all cards: none' (" + S + "cards_r1.txt). Removed BK4-c100 and BK4-c103, added BK4-c106 and BK4-c107 (other slices); the total is still 100."),
    "BK4b-cards-grades-basis": ("PASS", "Re-read of every L05 card with a grade (" + "course/modules/BK/BK4/cards.json): T on c080, c081, c083, c084, c086, c088, c089, c090, c094 with bases naming Propositions 2.1, 2.2, 2.4, 2.5, 2.6, Example 2.7, Example 2.8 or Problem M3 (each on the page); C on c087 with basis 'Lab 1, Part D; SIMULATED parameters, one set'. Mirrors: key row :486 (T, Example 2.8) = c086 and c094 (T, Example 2.8); key row :482 (T) = c088; key row :485 (T) = c089; key row :487 (C) = c087. Grades and bases match up to the wording of the key-results cell (ruling 13 'same grade and basis' holds). Observation (not a FAIL): the key row :485 basis is 'Arithmetic on the page' while c089 cites 'Example 2.7'; unchanged since 11d7077a."),
    "BK4b-banned-and-process-words": ("PASS", "Re-run: tools/check_pages.py --unit BK4 PASS (its banned-word scan included). Changed text (L05.html:486, cards c086, c088, c089, c090, c094) read: no process words (no 'we', 'this section', 'the lab shows', 'paragraph'); card text uses 'Lab 1' and 'Example 2.8' as learner-facing locators."),
    "BK4b-notation": ("PASS", "Changed text uses p, kappa, ell with their Assumption 1.3 / Definition 2.1 meanings (L05.html:64, :68-70, :79-80) and no new symbol; notation/notation.json (no kappa or ell entry; unchanged since 11d7077a) gives no conflict."),
    "BK4b-hours": ("PASS", "course/modules/BK/BK4/L05.html:2 unchanged (the only L05 hunk is :486); index.html is unchanged since 11d7077a; BK4 curriculum hours unchanged (render_curriculum re-run, diff empty)."),
    "BK4b-dag-prose-terms": ("PASS", "Changed text (L05.html:486, cards c086, c088, c089, c090, c094) introduces no concept outside the closure: 'Example 2.8', 'Lab 1', 'rounding rule' are unit-local and defined before use (Example 2.8 at :152; the rule at Problem E1 :427-429 and Example 2.8). Unchanged L04/L05 prose verified at 11d7077a."),
    "BK4b-twin-page-exact": ("PASS", "Re-run: twin_vs_page_r1.py under python -I -W error -> L04 page code == twin True; L04 twin exit 0, stderr 0 bytes; L04 page expected == twin stdout True (38 lines); L05 page code == twin True; L05 twin exit 0, stderr 0 bytes; L05 page expected == twin stdout True (31 lines); RESULT: PASS (" + S + "twin_vs_page_r1.txt)."),
    "BK4b-slice-delta": ("PASS", "git diff --stat 11d7077a..95f3f8cb over slice b paths: course/modules/BK/BK4/L05.html (one line, :486); course/modules/BK/BK4/cards.json (BK4-c086, c088, c089, c090, c094 changed; BK4-c100 removed; c106 and c107 added (L01, L03); c012, c013, c032, c043, c044, c047 changed (other slices)); references/references.json (line 3 and one Black & Scholes used_by entry); curriculum/*.yaml, CURRICULUM.md, curriculum/curriculum.json and course/assets/data/program.json (M3 and FC2 project briefs only; no BK4 hours change). L04.html, lab-BK4-L04-1.py, lab-BK4-L05-1.py, index.html, notation/, tools/ and tests/test_labs.py are byte-identical to 11d7077a. Every changed hunk in the slice is re-verified above or noted as another slice's; the delta reads only the listed rows (ruling 30)."),
    "BK4b-r8-scope-words": ("PASS", "Scope words re-scanned on the changed text: L05.html:486 has no only/all/always/every/any/same/drives/exactly; changed cards: c088 'the same as under A3' (a comparison proved by Proposition 2.2 with A3, see BK4b-cards-L04-L05-scan), c090 'depends only' is a question answered 'No' with Proposition 2.1, 'every delay' is supported by pκℓ_i with p, κ > 0. Unchanged rest verified at 11d7077a."),
    "BK4b-r10-scope-no-T1": ("PASS", "grep for the symbol T1 in the changed text (L05.html:486, cards c086, c088, c089, c090, c094): none. Unchanged L04/L05/twin text verified at 11d7077a."),
    "BK4b-cards-c076": ("PASS", "BK4-c076 object identical in 11d7077a and 95f3f8cb (python compare of card objects; BK4 cards changed only at c012, c013, c032, c043, c044, c047, c086, c088, c089, c090, c094, c100 (removed), c103 (removed), c106, c107)."),
    "BK4b-r8-card-c074": ("PASS", "Carried from round 11 (BK4-c074 object identical since 11d7077a; cards.json changed only at the objects listed under BK4b-slice-delta): see the round-11 evidence, cards.json (BK4-c074); course/modules/BK/BK4/L04.html:85, :376, :391 unchanged."),
    "BK4b-r8-card-c075": ("PASS", "Carried from round 11 (BK4-c075 object identical since 11d7077a): cards.json (BK4-c075); course/modules/BK/BK4/L04.html:95, :152, :392 unchanged."),
    "BK4b-r9-card-c072": ("PASS", "Carried from round 11 (BK4-c072 object identical since 11d7077a): cards.json (BK4-c072); course/modules/BK/BK4/L04.html:152 unchanged."),
    "BK4b-citation-bisndbasel": ("PASS", "Carried from round 11 (course/modules/BK/BK4/L05.html:348, :580 and references/references.json:2815-2842 byte-identical since 11d7077a; the L05.html change is at :486 and the references.json changes are at lines 3 and 2925-2926): see round-11 evidence."),
    "BK4b-registry-citation-consistency": ("PASS", "Carried from round 11 (course/modules/BK/BK4/L05.html:348, :580 and references/references.json:2815-2842 and the BK4 entries byte-identical since 11d7077a): see round-11 evidence; re-checked by BK4b-verify-refs-unit-scope (3 of 560, 0 problems)."),
    "BK4b-L04-remark3.2-FC1-paraphrase": ("PASS", "Carried from round 11 (course/modules/BK/BK4/L04.html:368 byte-identical; course/modules/FC/FC1/L01.html lines 67, 70-74, 79-81 byte-identical since 11d7077a: its changed lines are 51, 55, 86, 90, 104, 117, 131-132, 156, 171, 310 onward): see round-11 evidence."),
    "BK4b-r11-pytest-refs": ("PASS", "Re-run: .venv/bin/python -m pytest tests/test_refs.py -q -> all passed, exit 0 (" + S + "pytest_refs.txt); tests/test_refs.py is byte-identical since 11d7077a."),
}

carry_what = {
    "L05": "course/modules/BK/BK4/L05.html lines cited are unchanged; the file's only changed line is :486",
    "L01": "cited lines of course/modules/BK/BK4/L01.html unchanged",
    "cards": "cited card objects and lines unchanged",
}

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in fresh:
        status, ev = fresh[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        continue
    loc = r["location"]
    ev = r["evidence"]
    if "L05.html" in loc or "cards.json" in loc or "L01.html" in loc:
        if "L05.html" in loc and "cards.json" not in loc:
            what = carry_what["L05"]
        elif "cards.json" in loc:
            what = carry_what["cards"]
        else:
            what = carry_what["L01"]
    else:
        what = "every cited file is byte-identical to 11d7077a"
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": r["status"],
                 "evidence": PREFIX.format(what=what) + " " + ev})

# New rows for the delta (ruling 13 and ruling 30).
rows.append({"id": "BK4b-r1-ruling13-regrade-L05-486", "check": "9-terms", "location": "course/modules/BK/BK4/L05.html:152-153, :486; course/modules/BK/BK4/cards.json (BK4-c086, BK4-c094)", "status": "PASS",
             "evidence": "Ruling 13: a value derived on the page by hand in a numbered Example is T with the Example as basis even when a lab prints it. Example 2.8 (L05.html:152-153) derives 4375/2 = 2187.5 by Proposition 2.1 with p = 1/8, kappa = 2500, ell = (1, 2, 4), and states the half-up rounding to 2188. Key row :486 and cards c086 and c094 carry T with basis Example 2.8; Lab 1 Part B (L05 twin stdout) prints the same value as a check, not as the source."})
rows.append({"id": "BK4b-r1-card-count-L05", "check": "2.7-cards", "location": "course/modules/BK/BK4/cards.json (L05 objects)", "status": "PASS",
             "evidence": "python -I count over cards.json: L05 cards = 14 (BK4-c077, c078, c079, c080, c081, c083, c084, c086, c087, c088, c089, c090, c094, c098); L04 = 19; total 100 (cards_r1.txt). The round-11 count of 15 L05 cards included BK4-c100, which is removed; no key row or lesson sentence cites BK4-c100 (grep over course/modules/BK/BK4/*.html)."})
rows.append({"id": "BK4b-r1-delta-scope-ruling30", "check": "9-scope", "location": "git diff 11d7077a..95f3f8cb (slice b paths)", "status": "PASS",
             "evidence": "Ruling 30 delta: every non-PASS row of round 11 (none; the round-11 verdict was PASS) and every row whose cited subject changed was re-verified from scratch (rows listed above with fresh evidence); every other row is carried with the carry prefix. No new mutants written (ruling 37). The delta hunks outside slice b (L01-L03, project.html, grader, lab-BK4-project-1.py, other units' modules and labs, plans, pyproject.toml, tests/test_lx1_project_lab3.py) are not in slice b and were not verified here."})

for rr in rows:
    for k in ("id", "check", "location", "status", "evidence"):
        assert str(rr.get(k, "")).strip(), (rr.get("id"), k)

fail_rows = [r["id"] for r in rows if r["status"] != "PASS"]
for rr in rows:
    if rr["status"] != "PASS":
        rr["fix"] = ("Restore 'with A3 for independent failures' in the front of BK4-c088 (cards.json), as the round-11 card had it, "
                     "so that the hypotheses of the cited Proposition 2.2 are carried; or cite only Proposition 2.1 and Proposition 2.4 "
                     "in its basis and rewrite the back without 'as under A3 (Proposition 2.2)'. Then re-run cards_r1.py and the "
                     "card check against L05.html:95 and :113-114.")

frag = {
    "unit": "BK4",
    "slice": "b",
    "round": 1,
    "verifier": "Haiku independent verifier, BK4-b round 1 of the closing delta (did not build BK4; delta verification per rulings 30 and 37 from the round-11 base)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin; base fragment /Users/billyribeiro/.fanout/frags/E-BK4-b.round11.json, PASS, 87 rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-BK4-b",
    "scratch": "/tmp/bk4b_r1_scratch (copies of the twin stdout, the card scan and the recompute output are also in ledgers/BK4/scripts/BK4-b-r1/)",
    "verified_at": "2026-11-09T15:53:45+00:00",
    "verdict": "FAIL" if fail_rows else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"] + [
        "references/references.json changed since 11d7077a at line 3 (generated_at) and at the Black & Scholes used_by entry (hunk -2925: DV1 plus FC2). That is outside slice b; verify_refs offline 560/0 and unit BK4 3/0 re-run and PASS."
    ],
    "freshness_flags": base["freshness_flags"],
    "notes": [
        "Delta since round 11 (11d7077a..95f3f8cb) in slice b: L05.html line 486 (key-results row, C to T with Example 2.8); cards.json objects BK4-c086, c088, c089, c090, c094 changed and BK4-c100 removed.",
        "BK4-c088 regression: the round-11 front assumed A3; the delta removed it while the card still cites Proposition 2.2, which needs A3. This is the only non-PASS row (ruling 26, missing hypothesis).",
        "Observation (not a FAIL, unchanged since round 11): key row :485 basis 'Arithmetic on the page' versus card BK4-c089 basis 'Example 2.7'.",
        "Observation (not a FAIL): Example 2.8 (L05.html:153) states its values under the model of Assumption 1.3 and A1, A2 by name only in the cards, not in the Example text; the model is in force in Section 1-2, which is how Example 2.7 also reads.",
        "Observation (not a FAIL): key row :487 stays C although Proposition 2.5 (proved on the page) gives the sign for every parameter set; the C grade is conservative, and the row says 'for the SIMULATED parameters'.",
        "Round-11 registry flag resolved as before: bisndbasel used_by ['BK1', 'BK4'] at references/references.json:2838-2841 (unchanged), verify_refs --unit BK4 3 of 560, 0 problems.",
        "Mutants: none written (ruling 37; slice b has no grader and no project; lab twins are demonstrations)."
    ],
    "summary": (
        f"BK4-b round 1 (closing delta, rulings 30 and 37): verdict {'FAIL' if fail_rows else 'PASS'}. "
        f"{len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {len(fail_rows)} non-PASS ({', '.join(fail_rows)}). "
        "The non-PASS row is card BK4-c088 (cites Proposition 2.2, which needs A3; the front no longer assumes A3). "
        "Re-verified from scratch: L05.html:486 and Example 2.8 (exact fractions, recompute_b_r1.py), key-results table, cards c086/c088/c089/c090/c094, "
        "the card scan, and the gates (check_pages, check_dag, check_projects, run_labs, twins under python -I -W error, page_smoke alone, "
        "pytest test_labs -k BK4 and test_refs, ruff, mypy, verify_refs offline and unit, build_site --check, render_curriculum diff)."
    ),
}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "non-PASS", fail_rows, "verdict", frag["verdict"])
