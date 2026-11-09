import json, subprocess
R = "/Users/billyribeiro/.fanout/wt/verifyF21-M4-b"
S = "ledgers/M4/scripts/M4-b-r1"
base = json.load(open("/Users/billyribeiro/.fanout/frags/D-M4-b.round12.json", encoding="utf-8"))
brows = {r["id"]: r for r in base["rows"]}
CARRY = ("Carried from round 12 (course/modules/M/M4/L05.html, L06.html, L07.html, tests/labs/M4/lab-M4-L05-1.py, "
         "lab-M4-L06-1.py, lab-M4-L07-1.py, notation/, tools/ and plans/M4-build-plan.md byte-identical since the "
         "previous pin 329c1d7f, see " + S + "/delta_evidence.txt):")
CARD_CARRY = ("Carried from round 12 (records M4-c088, c089, c092, c093, c097, c101, c105, c107, c108, c191 of "
              "course/modules/M/M4/cards.json byte-identical since the previous pin, checked by " + S + "/card_identity.py):")
carry_ids = ["B6-09", "B6-10", "B6-11", "B6-12", "B6-13", "B6-14", "B6-15", "B6-16", "B6-17", "B6-18", "B6-19",
             "B6-20", "B6-21", "B6-25", "B6-27", "B12-33", "B12-34", "B12-35", "B12-36", "B12-37", "B12-38",
             "B12-39", "B12-40", "B12-41", "B12-42"]
fresh = {}
fresh["B6-01"] = ("Delta from pin 329c1d7f to HEAD 95f3f8cb (ancestor check PASS). Slice files byte-identical "
  "(git diff --quiet over L05/L06/L07 pages, the three twins, notation/, tools/, plans/M4-build-plan.md): " + S + "/delta_evidence.txt, first block empty. "
  "M4 files changed outside slice: L01 (meta description), L02 (lines 149-155 only, hunk header @@ -149,10 +149,10 @@), L08, L09, L10, index.html, cards.json (7 records changed: c023, c122, c128, c140, c157, c158, c217; 12 added c246-c252, c256, c257; 26 removed incl. c241 of L05), 4 grader mutants added (ledgers/M4/mutants/r12_01..04). L05-L07 cards: 20 + 19 + 16 records, with c241 the only removal in the slice. Commands: git merge-base --is-ancestor; git diff --stat (" + S + "/delta_evidence.txt).")
fresh["B6-02"] = ("tools/check_pages.py --unit M4 re-run on pin 95f3f8cb: '" + "check_pages M4: PASS', exit 0. Output " + S + "/check_pages.out.")
fresh["B6-03"] = ("tools/check_dag.py --unit M4 re-run: 'check_dag M4: PASS', exit 0 (" + S + "/check_dag.out). Grep of L05/L06/L07 for links to M3 unit pages or M3 concept ids: 0 hits (the only 'M3' strings are problem labels 'M3 · ...' at L05.html:326-327, L06.html:326-327, L07.html:324-325, and 'Problem M3' at L05.html:497). No link to M5 or M6 in the slice.")
fresh["B6-04"] = ("tools/check_projects.py --unit M4 re-run: 'check_projects M4: PASS', exit 0 (" + S + "/check_projects.out). The project pages belong to slice d.")
fresh["B6-05"] = ("tools/run_labs.py --unit M4 re-run: 'run_labs M4: PASS (13/13)', exit 0 (" + S + "/run_labs.out).")
fresh["B6-06"] = ("tools/page_smoke.py --unit M4 --pages L05 L06 L07 run alone: 'page_smoke modules/M/M4/L05.html: PASS', L06 PASS, L07 PASS, 'page_smoke M4: PASS', exit 0 (" + S + "/page_smoke.out).")
fresh["B6-07"] = ("Twins run under python -I -W error (" + S + "/twin_vs_page.py, output " + S + "/twin_vs_page.out): L05, L06, L07 'page code == twin: True', 'twin exit 0 stderr bytes 0', 'output == expected block: True'. Separately, /tmp twin stdout (L05 3865 bytes twin, L06 3246, L07 3627) exit 0 with stderr 0 bytes. Pages and twins byte-identical to base, so the page-to-twin equality is unchanged.")
fresh["B6-08"] = ("ruff check tests/labs/M4 course/modules/M/M4 re-run: 'All checks passed!', exit 0 (" + S + "/ruff_check.out). ruff format --check on the same paths: '17 files already formatted', exit 0 (" + S + "/ruff_format.out).")
fresh["B6-22"] = ("Cards read from course/modules/M/M4/cards.json (dump by " + S + "/dump_cards.py). L05 set changed: c241 removed, 20 remain (c067-c083, c191, c210, c242). All 20 read against current L05.html: c067 Remark 1.3 and L02 Def 2.1; c068 Def 1.4; c069 Prop 1.1(i); c070 Prop 1.2; c071 Prop 1.5; c072 Prop 1.6; c073 Example 1.7; c074 Remark 1.8 (E[Y]=2/3, E[Y^2]=2/3, Var=2/9, arithmetic checked); c075 Def 2.1; c076 Def 2.2; c077 Prop 2.3; c078 Prop 2.4 (finitely many values stated); c079 Remark 1.8; c080 Prop 1.2 with a=c=100 and Prop 1.6; c081 Prop 2.4 gives 4 <= 1, false; c082 value 0.00002223 at L05.html:275 and twin output 'max_entry_error 0.00002223' (" + S + "/twin_vs_page.out); c083 0.592936 and -0.007064 at L05.html:275 and twin output 'sample_correlation 0.592936 ... error -0.007064'; c191 matches Example 2.5 (L05.html:160-161, Assumption 1 stated, not proved); c210 Prop 1.1(iii); c242 Prop 1.1(iv). Every decimal on the L05-L07 cards appears in its lesson page: " + S + "/cards_numbers_L05_07.out, 'numbers checked 70 not found in lesson []'. L06 (19) and L07 (16) card records byte-identical to base (" + S + "/card_identity.py).")
fresh["B6-23"] = ("L02.html lines 98-104 re-read: Definition 2.1 (variance and standard deviation) defines sigma = sqrt(Var X) (L02.html:100-101), so L05 Remark 1.3 (L05.html:78-81) cites a correct definition. L02 changed only at lines 149-155 (" + S + "/delta_evidence.txt; git diff hunk header @@ -149,10 +149,10 @@). L04 and L05/L06/L07 cross-reference lines unchanged (byte-identical files; L04.html not in the M4 diff list).")
fresh["B6-24"] = ("L10 cross-lesson claims re-read at HEAD: L10.html:65-66 (Assumption 1: V = Z/sqrt(W/3) with W independent of Z, citing L06 Definition 2.5); L06.html:153-155 Definition 2.5 says W is chi-square 'independent of Z' (claim correct). L10.html:150-152 Proposition 2.3 (E[V^4] = infinity under Assumption 1) matches L06.html:284. L10.html:169 says Theorem 1.3, Proposition 1.2 and Proposition 2.3 of Lesson 9 are proved for finitely valued laws: L09.html:55, 68-69 (Proposition 1.2 'identically distributed and finitely valued'), 82-83 (Theorem 1.3), 131-132 (Proposition 2.3 'with the variables finitely valued') confirm it. L07.html:99 Proposition 1.4 gives domain (-inf, 1/2), matching the L07.html:112 remark (L06.html:281-284 cross-refs also re-read). No DOI or registry citation involved.")
fresh["B6-28"] = ("tools/verify_refs.py --offline re-run: 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "/verify_refs.out). Live Crossref resolution not run: the slice cites no registry key.")
fresh["B6-29"] = ("Standing mutant set (ruling 37, no new mutants): tools/mutate_graders.py --unit M4 --seeds 0-9 re-run: 'mutate_graders M4: PASS (163/163 killed)', exit 0 (" + S + "/mutate_M4.out). Set is 163 files, 159 at base plus 4 round-12 slice-d mutants r12_01..04 (" + S + "/delta_evidence.txt). Mutants are project-grader mutants; the slice is lessons, so this row is continuity only.")
fresh["B7-30"] = ("pytest tests/test_labs.py -k M4 re-run: 13 passed, exit 0 (" + S + "/pytest_labs_M4.out). mypy --no-incremental re-run: 'Success: no issues found in 386 source files', exit 0 (" + S + "/mypy.out).")
fresh["B9-31"] = ("tools/run_graders.py --unit M4 --seeds 0-49 re-run: 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.8 s)', exit 0 (" + S + "/run_graders.out). Grader unchanged since base (course/modules/M/M4/grader not in the M4 diff list).")
fresh["B12-32"] = ("L05.html:78-81 is the class 'remark' block titled Remark 1.3 (notation for the standard deviation), pointing to L02 Definition 2.1; L02.html:98-104 re-read and confirmed (see B6-23). Lines L05.html:78-81 byte-identical since the base pin.")
rows = []
for rid in [r["id"] for r in base["rows"]]:
    b = brows[rid]
    if rid in fresh:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS", "evidence": fresh[rid]})
    elif rid == "B6-26":
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                     "evidence": CARD_CARRY + " " + b["evidence"]})
    elif rid in carry_ids:
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                     "evidence": CARRY + " " + b["evidence"]})
    else:
        raise SystemExit("unassigned row " + rid)
assert len(rows) == 42 and all(r["status"] == "PASS" for r in rows)
frag = {
    "unit": "M4", "slice": "b", "round": 1,
    "verifier": "Haiku verifier, independent of the builders (verifyF21-M4-b), closing delta per ruling 30",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "round-12 fragment /Users/billyribeiro/.fanout/frags/D-M4-b.round12.json at pin 329c1d7feac5479403c351e64587c867278452cc (ancestor of this pin, checked with git merge-base --is-ancestor)",
    "checkout": R,
    "scratch": S,
    "verified_at": "2026-11-09",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [{
        "id": "M4-standing-set",
        "description": "No new mutants written (ruling 37). The standing M4 grader mutant set (ledgers/M4/mutants, 163 files) was re-run with tools/mutate_graders.py --unit M4 --seeds 0-9: 163/163 killed.",
        "killed_by": S + "/mutate_M4.out"}],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Closing delta of slice b (L05, L06, L07 and their three lab twins). Pages and twins are byte-identical to base pin 329c1d7f, so every row whose subject is those files is carried with the carry prefix; every gate was re-run on pin 95f3f8cb. Re-verified from scratch: B6-01 (delta), B6-22 (L05 card set changed: c241 removed; all 20 remaining L05 cards read against L05 text), B6-23 and B12-32 (L02 Definition 2.1, L02 changed at lines 149-155 only), B6-24 (L10 cross-lesson claims, changed at L10 lines 65-66 and 150-152 and 169; L09 hypotheses confirmed), B6-26 (record identity). Observations, not row failures: (1) L10.html changed at several lines outside the cited ones (Def 1.2, the Cauchy heavy-tail statements at lines 117-120, Lab 1 interpretation, E1-E3 and quiz notes); those lines belong to the L10 slice and were not re-verified here. (2) The L05 card c241 was removed; no L05 card or page refers to it (card_identity.py, check_pages PASS). (3) The base fragment's count of 159 mutants is now 163 after four slice-d mutants were added.",
    "summary": "Slice b (L05-L07 and their lab twins), closing delta round 1 from base pin 329c1d7f to 95f3f8cb: 42 rows, all PASS. Ids B6-01..B6-29, B7-30, B9-31 and B12-32..B12-42 kept. Re-verified from scratch: B6-01, B6-02..B6-08 (gates re-run), B6-22, B6-23, B6-24, B6-28, B6-29, B7-30, B9-31, B12-32. Carried with the carry prefix: the rest (pages, twins, notation and tools byte-identical). Gates re-run: check_pages, check_dag, check_projects, run_labs 13/13, page_smoke L05-L07, twins under python -I -W error, ruff check and format, mypy strict (386 files), pytest -k M4 (13), verify_refs offline (560, 0 problems), run_graders 50/50, mutate_graders 163/163. No new mutants (ruling 37).",
}
json.dump(frag, open(R + "/ledgers/M4/M4-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows))
