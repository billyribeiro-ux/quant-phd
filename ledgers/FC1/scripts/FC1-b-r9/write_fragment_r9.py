import json, datetime
from collections import Counter
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
rows = json.load(open("/tmp/fc1b_r9_rows.json", encoding="utf-8"))
counts = Counter(r["status"] for r in rows)
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
notes = [
 "Closing delta (ruling 30) from the round-8 pin 4540351d to 95f3f8cb. git diff --stat over course/modules/FC/FC1, tests/labs/FC1, notation, references, tools, curriculum: only course/modules/FC/FC1/cards.json changed (7 deletions: FC1-c173). out/guards.out records that L01, L03, L04, L05, index.html, project.html, tests/labs/FC1, references, notation, course/assets/js, course/assets/data, tools and curriculum are byte-identical between the two pins.",
 "Round-8 non-PASS rows re-verified from scratch: FC1-b-r1-cards-duplicates (now PASS: c173 is deleted; full re-scan of 169 entries, out/dup_scan_r9.out) and FC1-b-r7-delta-cards-c125-c173 (now PASS: c173 deleted, c125 absent). The round-8 judgement that FC1-c173 restated FC1-c067 is moot once the card is deleted.",
 "Rows whose subject is the whole cards.json file were re-verified as aggregate scans this round (ids and fronts unique, banned phrases, process words, numbers against the lesson and twin output, parenthetical citations, notation against notation.json, and the L04 and L05 card semantics read in full against the lesson text). Entry-level semantics of the L01-L03 cards were NOT re-read this round: they are carried from round 8 by object identity (out/guards.out: every remaining entry is object-identical to 4540351d; only FC1-c173 is removed). Carried rows carry the prefix 'Carried from round 8 (...)'.",
 "Row FC1-b-r1-cards-L04 is FAIL (LOW, locator only). FC1-c056 back cites Definition 1.1 for 'taking resting orders in price-time priority'. Definition 1.1 (L04.html line 59) says 'best price first' only; the time rule and the term are defined in Definition 2.1 (L04.html line 84). The claim is correct; the citation is incomplete. Fix: cite both definitions, or drop the priority clause from the back. The verdict flips to PASS after that one-card edit and a delta check of FC1-c056 (check_pages --unit FC1 plus this row).",
 "Judgement recorded in FC1-b-r1-cards-duplicates: FC1-c064 (definition of price-time priority) and FC1-c072 (misconception: size does not enter priority, with a worked case) are treated as distinct questions. If the orchestrator reads them as one fact, the row becomes FAIL with fix 'delete FC1-c072 or reword it to the worked case only'.",
 "Observation, not a finding: FC1-c011 writes '1,818.18' while L01.html line 142 writes '1818.18' (no thousands separator). The value is correct: 1000/(1-0.45) = 1818.18 rounded half up.",
 "Ruling 37: a closing round writes no new mutants. FC1-b has no mutant set (lessons, twins and cards); the mutants under ledgers/FC1/mutants/ belong to the project slice FC1-c. registry_flags carry the Harris year note from round 8 (curriculum/02-economics-finance-core.yaml line 385 reads 2003; the registry record reads 2002); the curriculum file is unchanged in this delta.",
 "Not run or not checked this round: (a) verify_refs --unit FC1 live (carried; references/ unchanged); (b) a browser run of the quiz deck insertion (quiz.js addLessonCards reads cards.json at runtime; page_smoke L01, L04 and L05 PASS, but the deck insertion itself was not exercised); (c) the full pytest suite (only the four FC1-related files, as in round 8); (d) run_graders and mutate_graders (project slices, outside this slice); (e) the L01-L03 card semantics (carried, see above).",
 "Gates run at 95f3f8cb: check_pages FC1 (unit, L04, L05), check_dag FC1, check_projects FC1, run_labs FC1 (8/8), each twin L01-L05 alone under python -I -W error (rc=0, empty stderr), page_smoke L01, L04, L05 (--skip-sweep), ruff check and format on tests/labs/FC1, mypy --no-incremental on L01/L04/L05 twins, pytest on the four files (rc=0), build_site --check, verify_refs --offline (560 entries, 0 problems), fetch_data --check, render_curriculum.py followed by git diff --exit-code on CURRICULUM.md and curriculum/curriculum.json (no change). No tracked file changed in the checkout; the only new untracked path is ledgers/FC1/scripts/FC1-b-r9/.",
 "No git commit or push was made. tools/ledger.py merge was not run.",
]
frag = {
 "unit": "FC1",
 "slice": "FC1-b",
 "round": 9,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 9 (closing delta; did not build FC1; read verifier-rules.md, CLAUDE.md, BUILDER_RULES.md, VERIFIER_RULES.md; round-8 fragment as context only; ruling 30 and 37 applied)",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "4540351dc664559cdfd371b908f2b4e644cf4297 (round-8 pin; round-8 fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round8.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b",
 "scratch": "ledgers/FC1/scripts/FC1-b-r9/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": ["harris2002trading: curriculum/02-economics-finance-core.yaml line 385 reads 'Harris, Trading and Exchanges (2003)'; the registry record (Crossref) reads 2002. Pages cite the key with the registry's own fields only. The curriculum string should be corrected by its owner; no registry edit is requested. Carried from round 8; the curriculum file is unchanged in this delta."],
 "freshness_flags": [],
 "notes": notes,
 "summary": f"FC1-b round 9 at 95f3f8cb (closing delta from 4540351d): {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL, 0 UNVERIFIABLE; no new mutants (ruling 37). The round-8 FAILs FC1-b-r1-cards-duplicates and FC1-b-r7-delta-cards-c125-c173 are resolved by the deletion of FC1-c173. One new FAIL (LOW, locator only): FC1-b-r1-cards-L04 on FC1-c056 (Definition 1.1 cited for the price-time priority clause, which is defined in Definition 2.1). The slice is not closed until that one card is corrected and delta-checked.",
}
probs = []
import sys
sys.path.insert(0, W + "/tools")
import ledger
probs = ledger.validate(frag, "FC1-b")
print("validate:", probs)
json.dump(frag, open(W + "/ledgers/FC1/FC1-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("verdict", verdict, dict(counts))
