import json, sys
SRC = "/Users/billyribeiro/.fanout/frags/B-M5-a.round9.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyB10-M5-a/ledgers/M5/M5-a.json"
d = json.load(open(SRC, encoding="utf-8"))
PIN = "e8b10b8110923bd88c3b4bd0e36e1571be3e6725"
CARRY = ("Carried from round 9 (cited subject lines byte-identical between pins b6865c7 and e8b10b8; "
         "round-10 delta hunks are index.html:168; L02.html:51; L03.html:62; L04.html:456; cards.json "
         "M5-c051, M5-c117, M5-c180, M5-c191, appended M5-c213..M5-c215; none inside the cited lines; "
         "tests/labs/M5 L01-L04 twins unchanged): ")
FRESH = {
 "M5a-hub-theorems-proved-L1-4": "Fresh: index.html:168 now reads 'Every theorem stated in Lessons 1 to 4 is proved on its page, except that the irrationality of the square root of 2 is cited, not reproved, from M1, Lesson 2, Corollary 2.6, which Lessons 1 and 2 use.' Proof markers follow each theorem-type block: L01 lines 76,91,105,122,137,241 (Thm 1.2, Thm 1.3, Cor 1.4, Lemma 1.5, Thm 1.6, Prop 1.7); L02 lines 72,92,107,121,135,165,178,192,206 (Prop 1.2, Prop 2.2, Lemma 2.3, Lemma 2.4, Thm 2.5, Cor 3.2, Prop 3.3, Lemma 3.4, Prop 3.5); L03 lines 74,87,101,179,193,210 (Lemma 1.3, Prop 1.4, Prop 1.5, Prop 2.1, Prop 2.2, Prop 3.1); L04 lines 83,226,247,274,284,311 (Prop 1.4, Prop 1.7, Prop 2.1, Prop 3.3, Prop 3.4, Prop 4.2), by grep -n 'Proof' on each page. The irrationality citation is used at L01.html:254, :370 and L02.html:300, and the cited statement exists at M1/L02.html:132-133 ('Corollary 2.6 (no rational number has square 2)'). Gap: proof bodies were read in round 9 and carried; this round re-checked markers and the sentence, not each proof body line by line.",
 "M5a-L02-why-it-matters": "Fresh: L02.html:51 now reads 'the harmonic series, whose partial sums fail the Cauchy condition of Corollary 3.2 (§3)'. Corollary 3.2 is the block at L02.html:157, under the Section 3 heading at L02.html:149 ('Series and the harmonic and geometric examples'). Proposition 3.3 (L02.html:171) supplies the harmonic failure.",
 "M5a-L03-line-62-after-definition": "Fresh: L03.html:62 now reads 'Proposition 3.1 (§3) shows that for x^2 on R and epsilon = 1, no single delta serves every point.' Proposition 3.1 is at L03.html:203, under the Section 3 heading at L03.html:198. Its statement (L03.html:203-208) is: for every delta > 0 there are x, y with |x-y| < delta and |f(x)-f(y)| >= 1. Proof (L03.html:210-214) takes x = 1/delta, y = x + delta/2, and f(y)-f(x) = x*delta + delta^2/4 >= 1. The sentence is a valid reading: for each delta, the point x0 = 1/delta has a y within delta with |f(y)-f(x0)| >= 1 = epsilon, so delta fails at x0. Checked by hand: (x+delta/2)^2 - x^2 = x*delta + delta^2/4.",
 "M5a-L04-quiz-q9-closed-set": "Fresh: L04.html:454 prompt 'A set \\(K\\) is closed when:'; L04.html:456 first option now reads 'every point of \\(K\\) is the centre of a ball inside \\(K\\)' (F removed, grep -F '(F' finds no closed-set F in L04); L04.html:457 correct option 'its complement is open'; L04.html:460 explain 'That is the definition of a closed set in §2' with §2 definition at L04.html:240 ('A set \\(K\\subseteq X\\) is closed when its complement \\(X\\setminus K\\) is open'). The first option is the open-set ball condition at L04.html:239, so the distractor is correct as an open-set description.",
 "M5a-cards-L04-c051-closed-set-symbol": "Fresh: cards.json card M5-c051 back now reads 'B(x, r) = {y : d(x, y) < r}. A set U is open when every x in U has some r > 0 with B(x, r) inside U.' The closed-set sentence is removed; its replacement is card M5-c215 (cards.json, lesson L04, 'When its complement X \\u2216 K is open'), which matches L04.html:240. No F remains in M5-c051.",
 "M5a-notation-registry": "Fresh: notation/notation.json holds 8 symbols (T, \\Phi, \\Phi^{-1}, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}). The round-10 delta adds the letters K (L04.html:240, :456), D (L02.html:121) and C (L02.html:97, :137); none is a registry symbol, so no registry meaning is reused. Other notation rows carried.",
}
NEW_ROWS = [
 {"id": "M5a-cards-L02-c213-c214", "check": "New cards M5-c213 and M5-c214 agree with the current L02 text and are not duplicates", "location": "course/modules/M/M5/cards.json (M5-c213, M5-c214, lesson L02); L02.html:97-98", "status": "PASS", "evidence": "Fresh: M5-c213 back 'When some real number C satisfies |s_n| <= C for every n' matches L02.html:97 ('there is a real number C with |s_n| <= C for every n'). M5-c214 back 'When some real number m satisfies m <= b for every member b of the set. Such an m is a lower bound of the set.' matches L02.html:97 ('some real number m satisfies m <= b for every member b of the set; such an m is a lower bound of the set'). Both labelled Section 2, where L02.html:97 sits (Section 2 heading at L02.html:77). Duplicate check (python json load of cards.json, 211 cards): 0 duplicate ids, 0 duplicate fronts; no other L02 card covers bounded sequences or bounded-below sets."},
 {"id": "M5a-cards-L04-c215", "check": "New card M5-c215 (closed set) agrees with L04 Section 2", "location": "course/modules/M/M5/cards.json (M5-c215, lesson L04); L04.html:240", "status": "PASS", "evidence": "Fresh: M5-c215 front 'When is a subset K of a metric space X closed (Section 2)?' back 'When its complement X \\u2216 K is open.' L04.html:240 reads 'A set \\(K\\subseteq X\\) is closed when its complement \\(X\\setminus K\\) is open.' Section 2 heading at L04.html:238. Duplicate fronts: 0 (python check)."},
 {"id": "M5a-cards-L01-c191", "check": "Card M5-c191 (maximum) agrees with L01 Section 1", "location": "course/modules/M/M5/cards.json (M5-c191, lesson L01); L01.html:55", "status": "PASS", "evidence": "Fresh: M5-c191 back now reads 'An element of A that is also an upper bound of A.' L01.html:55 defines a maximum in Section 1 as an element of A that is an upper bound of A. The removed 'Misconception 1' pointer is still valid text (L01.html:255, L01.html:261 Misconceptions); the card now states only the definition, so no card-to-lesson mismatch."},
 {"id": "M5a-cards-cross-L07-L10-c117-c180", "check": "Cross-slice check of cards M5-c117 (L07) and M5-c180 (L10) added grade C with basis, touched by the delta", "location": "course/modules/M/M5/cards.json (M5-c117, M5-c180); L07.html:329,394; L10.html:177,349,402", "status": "PASS", "evidence": "Cross-reference only (slices c/d own L07 and L10). M5-c117 'about 48.9 times the error' matches L07.html:394 (ratio 2.661258 / 0.05439523 ~ 48.92, recomputed: 2.661258/0.05439523 = 48.92); basis 'Lab 1 Part A' is the lab named at L07.html:197. M5-c180 'tagged sums are 0 and 1 ... meshes 0.1 and 0.01' matches L10.html:402 and the output line L10.html:349 ('n 100 mesh 0.010000 jumps 1 left_tag_sum 0 right_tag_sum 1'); the lab is SIMULATED (L10.html:177), so grade C naming the lab is the rule-9 form. Every one of the 143 graded cards has a grade of T or C and every C card has a basis (python check)."},
]
ids_fresh = set(FRESH)
rows = []
for r in d["rows"]:
    r = dict(r)
    if r["id"] in FRESH:
        r["evidence"] = FRESH[r["id"]]
        r["status"] = "PASS"
    elif r["id"] in ("M5a-gate-check-pages",):
        r["evidence"] = "Run this round: 'check_pages M5: PASS' (exit 0, ledgers/M5/scripts/M5-a-r10/check_pages_M5.out)."
    elif r["id"] in ("M5a-gate-check-dag",):
        r["evidence"] = "Run this round: 'check_dag M5: PASS' (exit 0, ledgers/M5/scripts/M5-a-r10/check_dag_M5.out)."
    elif r["id"] in ("M5a-gate-check-projects",):
        r["evidence"] = "Run this round: 'check_projects M5: PASS' (exit 0, ledgers/M5/scripts/M5-a-r10/check_projects_M5.out)."
    elif r["id"] in ("M5a-gate-run-labs",):
        r["evidence"] = "Run this round: 'run_labs M5: PASS (13/13)' (exit 0, ledgers/M5/scripts/M5-a-r10/run_labs_M5.out)."
    elif r["id"] in ("M5a-gate-page-smoke",):
        r["evidence"] = "Run this round: 'page_smoke M5: PASS' (exit 0, ledgers/M5/scripts/M5-a-r10/page_smoke_M5.out)."
    elif r["id"] in ("M5a-gate-ruff-mypy-pytest",):
        r["evidence"] = "Run this round: ruff check and ruff format --check '362 files already formatted' (ruff.out); mypy --no-incremental 'Success: no issues found in 255 source files' (mypy.out); pytest tests/test_labs.py -k M5 exit 0 (pytest_labs_M5.out); pytest test_docs_figures, test_curriculum, test_page_checks exit 0 (pytest_docs_curriculum.out). Note: pytest tests/test_labs.py without -k fails on missing E3 twins (tests/labs/E3 absent in this checkout), outside M5 (pytest_targeted.out)."
    elif r["id"] in ("M5a-gate-verify-refs-offline",):
        r["evidence"] = "Run this round: 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs.out). Live Crossref run not performed."
    elif r["id"] in ("M5a-gate-build-site-check",):
        r["evidence"] = "Run this round: 'site data current: 6 outputs', exit 0 (build_site_check.out). render_curriculum.py then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (render_diff.out)."
    elif r["id"] in ("M5a-data-fetch-check",):
        r["evidence"] = "Run this round: 'fetch_data: 3 datasets, 0 problems', exit 0 (fetch_data_check.out)."
    elif r["id"] in ("M5a-twins-isolated",):
        r["evidence"] = "Run this round: env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 .venv/bin/python -I -W error on lab-M5-L01-1.py..L04-1.py: exit 0 each, stderr 0 bytes (L0n.err); stdout ends with 'exit 0' in L0n.out (ledgers/M5/scripts/M5-a-r10/)."
    elif r["status"] == "PASS":
        r["evidence"] = CARRY + r["evidence"]
    rows.append(r)
seen=set(); dedup=[]
for r in rows:
    if r['id'] in seen: continue
    seen.add(r['id']); dedup.append(r)
rows = dedup + NEW_ROWS
frag = {
 "unit": "M5", "slice": "a", "round": 10,
 "verifier": "verifier-B10 (Haiku 5.5, independent)",
 "pin": PIN, "base": d["base"],
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB10-M5-a",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyB10-M5-a/ledgers/M5/scripts/M5-a-r10",
 "verified_at": "2026-10-29T00:00:00Z",
 "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Round-10 delta (b6865c7..e8b10b8) restricted to slice a: index.html:168; L02.html:51; L03.html:62; L04.html:456; cards.json M5-c051, M5-c117, M5-c180, M5-c191, appended M5-c213..M5-c215. tests/labs/M5 L01-L04 twins and their HTML lab blocks are unchanged in the delta.",
  "Lab-only slice: no project grader, so no student-error mutants and no alternative implementations apply (mutants list empty by design).",
  "Not checked this round: full line-by-line re-read of unchanged L01-L04 prose (carried from round 9 by the byte-identical rule); run_graders/mutate_graders (project slice only); 360px visual render and screenshots; live verify_refs; L05-L10 and project.html except as cross-references.",
 ],
 "summary": "Round 10: %d rows (round-9 duplicate id M5a-twins-isolated collapsed to one row). All PASS. Round-9 FAIL rows M5a-L04-quiz-q9-closed-set and M5a-cards-L04-c051-closed-set-symbol re-verified PASS (L04.html:456 now names K; card M5-c051 no longer says F). Round-10 changed subjects re-verified: index.html:168 (irrationality citation), L02.html:51 (Corollary 3.2 (§3)), L03.html:62 (Proposition 3.1 (§3)). New cards M5-c213..M5-c215 and changed M5-c191 checked against lesson text. All mechanical gates for M5 PASS on this pin." % len(rows),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "verdict", frag["verdict"], "ids", len({r["id"] for r in rows}))
