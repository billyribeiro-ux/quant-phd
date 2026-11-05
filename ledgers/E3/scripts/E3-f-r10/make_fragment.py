"""Round 10 fragment builder for E3 slice f (verifier output, not a builder).

Reads the round-8 fragment (the last recorded round for this slice, pin 2d75559), carries every round-8 PASS row whose
subject is byte-identical at the round-10 pin, replaces rows whose subject changed or whose gates were re-run, adds the
new card rows, and writes ledgers/E3/E3-f.json. Usage: python3 -I -W error make_fragment.py <checkout_root>
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1])
OLD_PIN = "2d755599d8d74df292e3e43025f0458c4053802e"
PIN = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
R8 = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-E3-f.round8.json").read_text(encoding="utf-8"))
CARDS = {c["id"]: c for c in json.loads((ROOT / "course/modules/E/E3/cards.json").read_text(encoding="utf-8"))}
CHANGED = {"E3-c004", "E3-c022", "E3-c050", "E3-c159", "E3-c180"}
ADDED = {"E3-c183", "E3-c186"}
SCRIPTS = "ledgers/E3/scripts/E3-f-r10"

def carry(row, files):
    out = dict(row)
    out["evidence"] = (f"Carried from round 8 ({files} byte-identical since the previous pin {OLD_PIN[:7]}): "
                       + row["evidence"])
    return out

def new(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    return row

rows = []
card_rows_seen = set()
for row in R8["rows"]:
    rid = row["id"]
    if rid.startswith("E3f-E3-c"):
        cid = "E3-c" + rid.split("-c")[-1]
        card_rows_seen.add(cid)
        if cid in CHANGED or cid in ADDED:
            continue  # replaced below
        if cid not in CARDS:
            raise SystemExit(f"round-8 card row {rid} has no card {cid}")
        rows.append(carry(row, f"course/modules/E/E3/{row['location'].split(':')[0]} and card {cid} in cards.json"))
        continue
    if rid in {"E3f-cards-slice-scan", "E3f-cards-near-duplicates", "E3f-cards-integrity", "E3f-cards-numbers",
               "E3f-cards-xrefs", "E3f-cards-grades", "E3f-delta", "E3f-E3-r7-independent-rederivation",
               "E3f-cmd-check_pages", "E3f-cmd-check_dag", "E3f-cmd-check_projects", "E3f-cmd-page_smoke",
               "E3f-cmd-run_labs-L01-L04", "E3f-cmd-pytest-labs", "E3f-cmd-ruff-labs", "E3f-cmd-mypy-twins",
               "E3f-cmd-verify_refs", "E3f-lab-L01", "E3f-lab-L02", "E3f-lab-L03", "E3f-lab-L04"}:
        continue  # replaced below with round-10 evidence
    if rid.startswith("E3f-lesson-numbers-L") or rid.startswith("E3f-dag") or rid in {
            "E3f-coverage-cards", "E3f-cards-duplicates", "E3f-notation", "E3f-banned-and-process", "E3f-hours",
            "E3f-references", "E3f-L03-references"}:
        if rid == "E3f-cards-duplicates":
            pass
        rows.append(carry(row, "the lesson files L01.html-L04.html, index.html, notation/ and references/references.json"
                          if rid != "E3f-cards-duplicates" else "the slice lesson files"))
        continue
    raise SystemExit(f"unhandled round-8 row {rid}")

GATE = f"{SCRIPTS}/*.out (round 10 at pin {PIN[:7]})"

# round-10 card evidence
rows.append(new("E3f-E3-c004", "2.7-cards", "course/modules/E/E3/cards.json (E3-c004) vs L01.html:73-74", "PASS",
                "Changed card (cards_delta.out: E3-c004 in the changed set). New back: 'The lottery has finitely many "
                "outcomes, and u is real-valued on them. Every result in this lesson that uses a sum over outcomes uses "
                "A1, and no result here allows a lottery with infinitely many outcomes.' Matches L01.html:74 (Assumption "
                "A1 text) word for word in substance, and L01.html:331 ('Every sum in this lesson is finite (A1)'). "
                "Question is not a graded result; no number on the card."))
rows.append(new("E3f-E3-c022", "2.7-cards", "course/modules/E/E3/cards.json (E3-c022) vs L02.html:103-126", "PASS",
                "Changed card (cards_delta.out). New back: 'u lies below its tangent line at E X, so E u(X) <= u(E X) and "
                "CE(X; u) <= E X'. Matches Proposition 1.3 proof, L02.html:110-126: Step 1 tangent-line bound "
                "u(y) <= u(m)+u'(m)(y-m) from F2 and A2; Step 2 E u(X) <= u(m); Step 3 strict monotonicity (A2, F5) gives "
                "CE <= m. Hypotheses 'F1, F2 and F5, under A1 to A3' match the Proposition 1.3 statement (L02.html:103-109). "
                "Grade T is the page's own proof. rederive_changed.out (ln sanity: CE 3.162278 <= E X 3.5)."))
rows.append(new("E3f-E3-c050", "2.7-cards", "course/modules/E/E3/cards.json (E3-c050) vs L03.html:183-184", "PASS",
                "Changed card (cards_delta.out). New back: 'A money amount is rounded once, from its unrounded value, to the "
                "nearest whole cent with halves going up: floor(v + 1/2) for v >= 0 (Remark 2.8).' Matches Remark 2.8 "
                "(L03.html:183-184: floor(v + 1/2) for v >= 0, rounds the unrounded value, not an intermediate). "
                f"{SCRIPTS}/rederive_changed.py output: floor(1/2+1/2)=1, floor(3/2+1/2)=2, floor(10615.801+1/2)=10616."))
rows.append(new("E3f-E3-c159", "2.7-cards", "course/modules/E/E3/cards.json (E3-c159) vs L02.html:130-131 and L02.html:59", "PASS",
                "Changed card (cards_delta.out). New back lists A2 (u'' <= 0 in tangent bound; u' > 0 gives strict increase by "
                "F5), F2 (Lagrange remainder, L02.html:59), F1 (existence, Proposition 1.1), A1 (finite sums), A3 (Remark 1.4). "
                "Remark 1.4 (L02.html:130-131) lists the same five: A2 through u''(xi) <= 0 and u' positive, F2 in Step 1, F1 in "
                "Step 3, A1 in Step 2, A3 for I. Matches."))
rows.append(new("E3f-E3-c180", "2.7-cards", "course/modules/E/E3/cards.json (E3-c180) vs L03.html:148-149, 158-159", "PASS",
                "Changed card (cards_delta.out). New back: '2000 cents, the exponential of the probability-weighted mean of "
                "ln 1000 and ln 4000 (Example 2.5; Proposition 2.4).' Example 2.5 (L03.html:158-159): X = 1000 or 4000 with "
                "probability 1/2 each, CE_1 = exp(1/2 ln 1000 + 1/2 ln 4000) = sqrt(4 000 000) = 2000 cents. Proposition 2.4 "
                "(L03.html:148-149): CE_1 = exp(sum p_i ln x_i). rederive_changed.out: exp(...) = 2000.0. Grade T matches "
                "Example 2.5's 'computed by hand from Proposition 2.4'."))
rows.append(new("E3f-E3-c183", "2.7-cards", "course/modules/E/E3/cards.json (E3-c183, L04) vs L04.html:172-173", "PASS",
                "New card (cards_delta.out: added). Front: the pair of Example 2.6. Back: Y is the sure 3000 cents; both means "
                "are 3000 cents; I_Y(t) = (t-3000)^+ <= I_X(t); Y dominates X in the second order; neither dominates in the "
                "first order. Matches L04.html:172-173 verbatim in substance. rederive.out / rederive_changed.out (exact "
                "Fractions): means 3000 and 3000; I_X on support [1000,3000,5000] = [0,1000,2000], I_Y = [0,0,2000]; "
                "I_Y(t) <= I_X(t) on the grid 0..6000 step 25 (no violation); first-order X>=Y and Y>=X both fail. "
                "The 'at every support point' wording is the lesson's (L04.html:173, Lemma 2.2). No grade: a worked example, "
                "not a row of the L04 key-results table (L04.html:628-631)."))
rows.append(new("E3f-E3-c186", "2.7-cards-accuracy", "course/modules/E/E3/cards.json (E3-c186) back vs L02.html:98 and L03.html:143", "FAIL",
                "Back reads 'as in Lesson L02 (Definition 2.3)'. L02.html has no Definition 2.3: its definitions are 1.1, 1.2 "
                "(L02.html:98, certainty equivalent), 1.3 and 2.1 (L02.html:143); the grep 'Definition 2.3' over L02.html "
                "returns nothing. The certainty equivalent of a finite lottery is Definition 2.3 of this unit's L03 "
                "(L03.html:143), which points back to Lesson L02. The parenthetical therefore names a definition that does "
                "not exist in the lesson it cites. Content otherwise matches L03.html:143-144 (u(c) = E u(X)).",
                fix="Change the back to 'The amount c with u(c) = E u(X), the expected utility of the finite lottery X, as in "
                    "Lesson L02 (Definition 1.2); this lesson restates it as Definition 2.3.' Or delete the card (see "
                    "E3f-cards-near-duplicates)."))
rows.append(new("E3f-cards-near-duplicates", "2.7-cards-duplicates", "course/modules/E/E3/cards.json: E3-c186 vs E3-c020", "FAIL",
                "Full near-duplicate scan of all 178 cards (scan_cards.out, token Jaccard >= 0.5, fronts and backs): pair "
                "(0.5, front) E3-c020 / E3-c186. Fronts: 'What is the certainty equivalent of a lottery X under u?' and "
                "'What is the certainty equivalent of a finite lottery under a utility u?'. Backs state the same definition "
                "(u(c) = E u(X)). BUILDER_RULES §7 and CLAUDE.md rule 10: each card tests one fact, no duplicate cards. "
                "Other flagged pairs (E3-c047/c180, c067/c181, c063/c065, c160/c171, c059/c167, c003/c014, c183/c124) ask "
                "distinct questions and are not duplicates.",
                fix="Delete E3-c186 (E3-c020 already tests the same definition from L02), or replace it with a card on a fact "
                    "no other card tests, for example the positivity requirement of Definition 2.3 (L03.html:144)."))
rows.append(new("E3f-cards-slice-scan", "2.7-cards-duplicates", f"{SCRIPTS}/scan_cards.out (91 slice cards, L01-L04)", "FAIL",
                "Counts: L01 18, L02 22, L03 27, L04 24 = 91 (round 8: 89; +E3-c183, +E3-c186). Integrity over 178 cards: 0 "
                "problems (scan_cards.out). The duplicate scan fails on E3-c186 (see E3f-cards-near-duplicates).",
                fix="Remove or rewrite E3-c186 as described in E3f-cards-near-duplicates."))
rows.append(new("E3f-cards-integrity", "2.7-cards-integrity", "course/modules/E/E3/cards.json (178 cards)", "PASS",
                "scan_cards.out: 'cards total 178 integrity problems 0': keys within {id, lesson, front, back, grade, basis, "
                "cite}; ids unique and E3-cNNN; lesson in L01-L08; no empty front or back; every graded card of a "
                "non-theorem grade has basis or cite."))
rows.append(new("E3f-cards-numbers", "2.7-cards-numbers", f"{SCRIPTS}/scan_cards.out vs the four slice lessons", "PASS",
                "scan_cards.out: 166 numeric tokens in the backs of the 91 slice cards each occur in their own lesson's text "
                "(HTML stripped). Changed-card numbers re-derived in rederive_changed.out (2000 for E3-c180; 10616 for E3-c050; "
                "I-values for E3-c183)."))
rows.append(new("E3f-cards-xrefs", "2.7-cards-refs", f"{SCRIPTS}/scan_cards.out (127 cross-references in slice cards)", "PASS",
                "All 127 cross-references (Definition/Proposition/Lemma/Remark/Example/Theorem/Problem/Section) resolve in "
                "the named lesson, except two that my regex flags and that are correct: 'Problem E2' (E3-c055) matches "
                "the problem labelled 'E2 ·' at L03.html:422; 'Section 3' (E3-c077) matches the section heading "
                "'Where the canon breaks' (L04.html:489). Changed refs: c022 Prop 1.3(a) (L02.html:103), c159 Prop 1.1 and "
                "Remark 1.4 (L02.html:130), c050 Remark 2.8 (L03.html:183), c180 Example 2.5 and Prop 2.4 (L03.html:148,158), "
                "c183 Example 2.6 (L04.html:172)."))
rows.append(new("E3f-cards-grades", "2.7-cards-grades", "course/modules/E/E3/cards.json (grade and basis, slice cards)", "PASS",
                "scan_cards.out: no grade outside the scale, no C/B/A grade without basis or cite. Changed grades: E3-c022 T, "
                "E3-c180 T (both match the lesson's own proof or example); E3-c183 and E3-c186 carry no grade, which is "
                "consistent with the other ungraded slice cards (c004, c159)."))
rows.append(new("E3f-delta", "0-delta", f"git diff {OLD_PIN[:7]}..{PIN[:7]} for the slice", "PASS",
                "git diff --quiet on L01-L04.html, index.html, notation/, references/references.json, tests/labs/E3/lab-E3-L0n-1.py: "
                "all unchanged. Changed in the slice: course/modules/E/E3/cards.json only (cards_delta.out): changed E3-c004, "
                "c022, c050, c159, c180; added E3-c183 (L04), E3-c186 (L03). Outside the slice in the same range: E3-c131 "
                "(L07), E3-c184 and E3-c185 (L05), project.html, grader/test_project.py, tests/labs/E3/lab-E3-project-1.py, "
                "curriculum M3 concept rename (no E3 reference found by grep), 19 tools/tests files (gates re-run below)."))
rows.append(new("E3f-E3-r7-independent-rederivation", "2.2-numbers", f"{SCRIPTS}/rederive.py", "PASS",
                "rederive.py (copied unchanged from ledgers/E3/scripts/E3-f-r8/) run with python3 -I -W error; output in "
                "rederive.out: means, I-values, CE values 1600, 2000, 8888.8889 / 8889, 10616, 10931.7733 and the "
                "E2 and M2 checks all reproduce."))
CMD_IDS = {
    "check_pages": "E3f-cmd-check_pages", "check_dag": "E3f-cmd-check_dag", "check_projects": "E3f-cmd-check_projects",
    "page_smoke": "E3f-cmd-page_smoke", "pytest_labs_E3": "E3f-cmd-pytest-labs", "ruff_labs": "E3f-cmd-ruff-labs",
    "mypy_twins": "E3f-cmd-mypy-twins", "verify_refs_offline": "E3f-cmd-verify_refs",
}
for name, check, loc in [
    ("check_pages", "2.9-structure", "tools/check_pages.py --unit E3"),
    ("check_dag", "2.9-define-before-use", "tools/check_dag.py --unit E3"),
    ("check_projects", "2.6-projects", "tools/check_projects.py --unit E3"),
    ("page_smoke", "2.5-labs", "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04"),
    ("pytest_labs_E3", "2.5-labs", "python -m pytest tests/test_labs.py -k E3 -q"),
    ("ruff_labs", "2.5-labs", "ruff check and ruff format --check tests/labs/E3"),
    ("mypy_twins", "2.5-labs", "mypy --no-incremental on the four L01-L04 twins"),
    ("verify_refs_offline", "2.1-citations", "tools/verify_refs.py --offline"),
]:
    text = (ROOT / SCRIPTS / f"{name}.out").read_text(encoding="utf-8").strip().splitlines()
    rows.append(new(CMD_IDS[name], check, loc, "PASS" if text[-1] == "exit 0" else "FAIL",
                    f"Run by the verifier at pin {PIN[:7]}: {loc}. Output in {SCRIPTS}/{name}.out, last lines: "
                    + " | ".join(text[-3:]) + "."))
_labs = [(ROOT / SCRIPTS / f"run_labs_{L}.out").read_text(encoding="utf-8").strip().splitlines() for L in ["L01", "L02", "L03", "L04"]]
rows.append(new("E3f-cmd-run_labs-L01-L04", "2.5-labs", "tools/run_labs.py --unit E3 --page L01..L04",
                "PASS" if all(o[-1] == "exit 0" and "PASS" in o[-2] for o in _labs) else "FAIL",
                f"Run by the verifier at pin {PIN[:7]}: " + "; ".join(o[-2] for o in _labs) + f" ({SCRIPTS}/run_labs_L0n.out)."))
rows.append(new("E3f-banned-cards", "1.3-1.4-banned", f"{SCRIPTS}/scan_cards.out (banned-phrase hits in slice cards)",
                "PASS", "scan_cards.out: 'banned-phrase hits in slice cards: []' for TODO, TBD, lorem, ellipsis, for brevity, "
                "beyond the scope, obviously, clearly, it is important to note, studies show, experts agree, it is well known "
                "over the 91 slice cards (the lesson-page part is carried under E3f-banned-and-process)."))
for L in ["L01", "L02", "L03", "L04"]:
    out = (ROOT / SCRIPTS / f"run_labs_{L}.out").read_text(encoding="utf-8").strip().splitlines()
    rows.append(new(f"E3f-lab-{L}", "2.5-labs", f"course/modules/E/E3/{L}.html lab block; tests/labs/E3/lab-E3-{L}-1.py",
                    "PASS" if out[-1] == "exit 0" and "PASS" in out[-2] else "FAIL",
                    f"tools/run_labs.py --unit E3 --page {L} (round 10, {SCRIPTS}/run_labs_{L}.out): '{out[-2]}'. "
                    f"Twin run alone under python3 -I -W error: {SCRIPTS}/twins.out, exit 0. Page and twin are byte-identical "
                    "to round 8 (lesson and twin files unchanged)."))

# keep an explicit row for each round-8 card id that did not appear in the round-8 list (none expected)
expected_cards = {cid for cid in CARDS if cid.startswith("E3-c") and CARDS[cid]["lesson"] in {"L01", "L02", "L03", "L04"}}
missing = sorted(expected_cards - card_rows_seen - ADDED)
if missing:
    raise SystemExit(f"slice cards with no row: {missing}")

seen = set()
renamed = []
for r in rows:
    if r["id"] in seen:
        # round 8 wrote E3f-E3-c178 twice (two different checks); keep the first id, give the second a suffix
        renamed.append(r["id"])
        r["id"] = r["id"] + "-b"
        r["evidence"] = "Row id renamed from the round-8 duplicate id (same id twice in D-E3-f.round8.json): " + r["evidence"]
    seen.add(r["id"])
fails = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fails else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "E3",
    "slice": "f",
    "round": 10,
    "verifier": "Haiku independent verifier, E3-f round 10 (did not build E3)",
    "pin": PIN,
    "base": f"{OLD_PIN} (round-8 pin; frags/D-E3-f.round8.json). No D-E3-f.round9.json exists in frags; the last recorded "
            "round for this slice is round 8. Delta computed from 2d75559.",
    "checkout": str(ROOT),
    "scratch": f"{SCRIPTS}/",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lesson slice (no project grader in this slice): mutation testing is not applicable; mutate_graders and run_graders "
        "were not run. The project (project.html, grader/) belongs to another slice.",
        "Round 8 fragment contained the row id E3f-E3-c178 twice; the second occurrence is carried as E3f-E3-c178-b so that merged ledgers have unique ids.",
        "Carried rows cite the lesson and card files that are byte-identical or whose card object is unchanged "
        "(cards_delta.out). Lesson files L01-L04.html, index.html, notation/, references/references.json and the four "
        "lab twins are byte-identical to 2d75559.",
        "Not checked in this slice: project.html and grader/; live verify_refs (only --offline); full reading of the "
        "published works (only the registry record); L05-L08 cards (E3-c131, c144, c182, c184, c185 are outside slice f).",
    ],
    "summary": f"Slice f (E3 lessons L01-L04 and their cards), round 10 at {PIN[:7]}. Verdict {verdict}: {counts['FAIL']} FAIL "
               f"row(s), {counts['PASS']} PASS, {counts['UNVERIFIABLE']} UNVERIFIABLE. The FAIL is card E3-c186: its back "
               "cites a Lesson L02 Definition 2.3 that does not exist, and it duplicates E3-c020. Changed cards c004, c022, c050, "
               "c159, c180 and new card c183 re-verified PASS. All gates pass.",
}
out = ROOT / "ledgers/E3/E3-f.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "verdict", verdict)
