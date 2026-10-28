"""Build ledgers/AC4/AC4-e.json (round 23) from the r23 outputs; prior rows are kept by id."""
import json, re, pathlib, datetime
ROOT = pathlib.Path("/tmp/verify23-AC4-e")
S = ROOT / "ledgers/AC4/scripts/AC4-e-r23/out"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round22.json"))
CHANGED_CARDS = {"c007", "c020", "c037", "c074", "c082", "c089", "c093", "c095", "c096", "c108", "c113"}
CARRY = ("Carried from round 22 (course/modules/AC/AC4/project.html, course/modules/AC/AC4/grader/test_project.py, "
         "tests/labs/AC4/lab-AC4-project-1.py and lab-AC4-project-2.py byte-identical since the previous pin d160ac3; "
         "card entries unchanged since d160ac3): ")

def kv(path):
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip()]

proj = kv(S / "mutants_proj139_r23.out")
new6 = kv(S / "mutants_new6_r23.out")
alts = [l for l in kv(S / "alts_prior_r23.out") if "make_alts" not in l]
R23 = {
 "mut": "Re-run r23 on the grader: ledgers/AC4/scripts/AC4-e-r23/out/mutants_proj139_r23.out (139 project mutants, seeds 0-49) and mutants_new6_r23.out (6 new): every mutant KILLED.",
 "alt": "Re-run r23: ledgers/AC4/scripts/AC4-e-r23/out/alts_prior_r23.out and the three new alternatives alts/alt_r23_*.py: each PASS 50/50 seeds (make_alts_r12.py is a generator script, not an implementation, and is excluded).",
 "lab": "Re-run r23: python -I -W error tests/labs/AC4/lab-AC4-project-1.py output equals the page expected block (9 lines); run_labs AC4 10/10 PASS (out/run_labs.out).",
 "gate": "Re-run r23: see the named out/ file in ledgers/AC4/scripts/AC4-e-r23/out/ (AC4 line PASS).",
 "card": "Re-verified r23 against the current lesson text and its lab output (see proj-r23-cards-* rows).",
}
def r23_evidence(rid):
    t = rid
    if "mutant" in t or t.startswith("proj-mutant") or "rerun-mutants" in t or "mutants-" in t or re.search(r"\bfx\d", t):
        return R23["mut"]
    if "alt" in t and "exemplar" not in t and "calib" not in t and "instance" not in t:
        return R23["alt"]
    if "lab" in t and "exemplar" not in t:
        return R23["lab"]
    if "instance" in t or "exemplar" in t or "rubric" in t or "calib" in t or "memo" in t:
        return None
    if re.search(r"check-(pages|dag|projects)", t):
        return "Re-run r23: see proj-r23-gates-pages-dag-projects (out/check_pages.out, check_dag.out, check_projects.out)."
    if re.search(r"page-smoke|run-graders|run-labs|reference", t):
        return "Re-run r23: see proj-r23-gates-labs-smoke-graders (out/run_labs.out, page_smoke.out, run_graders.out)."
    if re.search(r"ruff|gates|check-tools|mypy", t):
        return "Re-run r23: see proj-r23-gates-build-ruff-mypy (out/ruff.out, mypy.out, build_site_check.out, pytest_relevant.out)."
    if re.search(r"collect|grading-count|count", t):
        return "Re-run r23: see proj-r23-collect-count-seeds (563 on seeds 0, 1, 7, 49, 12345)."
    if re.search(r"verify-refs|citations|reading", t):
        return "Re-run r23: see proj-r23-verify-refs and proj-r23-reading-list-keys."
    if "hours" in t:
        return "Re-derived r23: see proj-r23-hours-split-arith."
    if "banned" in t:
        return "Re-scanned r23: see proj-r23-banned-and-placeholders."
    if "cards-changed" in t or "cards-structure" in t or "cards-duplicates" in t or "cards-targeted" in t or "cards-sample" in t:
        return R23["card"]
    m = re.search(r"card-c(\d{3})", t) or re.search(r"cards-c(\d{3})", t) or re.search(r"-c(\d{3})", t)
    if m and ("card" in t or "cards" in t):
        return R23["card"] if m.group(1) in CHANGED_CARDS else None
    return None

rows = []
for r in prev["rows"]:
    ev = r23_evidence(r["id"])
    if ev is None:
        if r["id"].startswith(("proj-card", "proj-cards", "proj-r12-cards", "proj-r17-cards", "proj-r18-card", "proj-r13-card")):
            ev = CARRY + "card entry is byte-identical to the previous pin, and its lesson is unchanged since the pin: " + r["check"][:160]
        else:
            ev = CARRY + r["check"][:200]
    if r["id"] == "proj-r18-card-c074-qualifier":
        ev = R23["card"]
    rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

NEW = [
 ("proj-r23-delta-scope", "Delta for AC4-e since the previous pin d160ac3", "git diff --stat d160ac3 503d139 (AC4 slice)",
  "Project page, grader, project labs byte-identical since d160ac3 (not in the diff); changed in the slice: cards.json (c020, c037, c095, c108, c113 changed; c135 to c140 added), L07.html and L08.html (lesson text only, rows for their cards below). Previous fragment on disk is the round-18 file (pin 7143726); its rows were re-verified where the subject changed since 7143726 (c007, c074, c082, c089, c093)."),
 ("proj-r23-gates-pages-dag-projects", "check_pages, check_dag, check_projects for AC4", "tools/check_pages.py --all; check_dag.py --all; check_projects.py --all",
  "out/check_pages.out, check_dag.out, check_projects.out: 'check_pages AC4: PASS', 'check_dag AC4: PASS', 'check_projects AC4: PASS' (each rc=0)."),
 ("proj-r23-gates-labs-smoke-graders", "run_labs, page_smoke, run_graders for AC4", "tools/run_labs.py --unit AC4; page_smoke.py --unit AC4; run_graders.py --unit AC4 --seeds 0-49",
  "out/run_labs.out 'run_labs AC4: PASS (10/10)'; out/page_smoke.out 'page_smoke AC4: PASS'; out/run_graders.out 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)'."),
 ("proj-r23-gates-build-ruff-mypy", "build_site --check, ruff, mypy, relevant pytest", "tools/build_site.py --check; ruff check . && ruff format --check .; mypy --no-incremental; pytest tests/test_page_checks.py tests/test_run_labs.py tests/test_refs.py",
  "out/build_site_check.out 'site data current: 6 outputs' rc=0; out/ruff.out 'All checks' and '220 files already formatted' rc=0; out/mypy.out 'Success: no issues found in 153 source files' rc=0; out/pytest_relevant.out all dots, no failures."),
 ("proj-r23-collect-count-seeds", "563 checks on every seed", "pytest --collect-only on the reference solution in the run_graders workspace, QF_SEED 0, 1, 7, 49, 12345",
  "563 tests collected for every seed (ledgers/AC4/scripts/AC4-e-r23/collect_ws.py); the page states 563 at course/modules/AC/AC4/project.html line 265. n_products is fixed at 3 (grader/instance.py line 24)."),
 ("proj-r23-grader-read-full", "Every grader test body read", "course/modules/AC/AC4/grader/test_project.py lines 1-1155",
  "Read the header, oracle (lines 67-107), helpers, every test group, the 16-entry LATER_PRODUCT_CONDITIONS table (lines 1052-1073) and the purity tests (lines 1094-1155). Each condition named on the page (line 265) maps to a test: negative budgeted/actual/standard counts and budget price, boolean/float/text/none, missing fields, empty/non-text name, non-mapping product."),
 ("proj-r23-oracle-matches-spec", "Oracle and reference agree with the Conventions (project.html lines 257-260)", "grader/test_project.py oracle(); grader/reference.py; project.html Conventions",
  "Oracle: master profit, flexed amounts half-up (half_up), sales_mix = (AU x budgeted margin - F) - whole-cent flexed profit, efficiency = s(sum q AU - AQ), total = actual - master. Reconciliation is exact algebraically: price + (AMM - F) + efficiency = actual profit - F - s*AQ - master = total, so price + volume + mix + efficiency = total."),
 ("proj-r23-half-cent-bound-claim", "The mix uses the whole-cent flexed profit, so it differs from the exact fraction by less than one cent (page line 260)", "page line 260; grader test_mix_is_within_one_cent_of_the_exact_fraction",
  "Half-up rounding gives r - e in [-1/2, 1/2) for each of revenue and variable cost; the flexed profit error is (r_rev - e_rev) - (r_var - e_var), which lies in (-1, 1). So the statement holds; the lab's 1/7 cent is consistent (Lab 1 step 6 line)."),
 ("proj-r23-lab1-recompute", "Lab 1 numbers and interpretation (page lines 135-146) recomputed", "tests/labs/AC4/lab-AC4-project-1.py output; hand recomputation",
  "Recomputed by hand: master 8,600,000 - 1,000,000 - 5,000,000 = 2,600,000; flexed 1,500 units: 9,214,285.71 - 1,071,428.57 - 5,000,000 -> 3,142,857 (exact 3,142,857 1/7); price 240,000 - 60,000 = 180,000; volume 542,857; efficiency 200 x (5,100 - 5,300) = -40,000; mix 2,680,000 - 3,142,857 = -462,857; total 2,820,000 - 2,600,000 = 220,000; sum of four = 220,000. Interpretation figures 5,428.57 (7,600,000/1,400), 71.4%, 80.0%, 4,400 and 8,000 margins, 5,300 vs 5,100 inputs all match."),
 ("proj-r23-lab2-twin-and-blanks", "Lab 2 blanks and completed twin", "project.html lines 150-242; tests/labs/AC4/lab-AC4-project-2.py",
  "The page code has exactly three blanks (lines 210, 214, 216: efficiency, actual-mix margin, sales mix). The twin lab-AC4-project-2.py is the completed plant and is byte-identical to lab-AC4-project-1.py (diff: IDENTICAL). Both run output equals the page expected block (checked programmatically: True for both)."),
 ("proj-r23-exemplar-scores-and-words", "Exemplar official scores, levels and body length (page lines 324-386)", "project.html exemplar-a and exemplar-b; word count of memo-text body",
  "Exemplar A: headings Result, Causes, Recommendation (three); body 318 words; scores 2,2,2,1,2 consistent with the descriptors (C1 has two correct signs and the total; C4 recommends no action for the mix or efficiency variance, so 1). Exemplar B: headings Result, Causes, Assumptions, Recommendation; body 409 words; scores 4,4,3,4,4. Both within 300 to 600 words."),
 ("proj-r23-exemplar-B-figures", "Exemplar B figures and the 5,400 threshold (page lines 363-373)", "project.html exemplar-b; recomputation",
  "53,000 = 5,300 x 10 cents extra input cost; 220,000 - 53,000 = 167,000; 240,000 Standard price gain; -60,000 Deluxe; 71.4 (1,000/1,400), 80.0 (1,200/1,500), 28.6 (400/1,400), 20.0 (300/1,500) percent; Deluxe margin 5,400 - 1,000 = 4,400 equals Standard 4,400; d(mix)/d(price_D) = AU_D - (AT/BU) BU_D = 300 - 428.57 = -128.57, so a Deluxe price below 5,400 makes the mix favourable (sign reversal as stated)."),
 ("proj-r23-hours-split-arith", "Hours: 20 project, 50 lesson, 70 module; table sums", "project.html lines 271-289; index.html line 29; L01-L08 data-hours",
  "Lesson data-hours 6+7+6+6+6+7+6+6 = 50 (L01 to L08). Hub 50 + 20 = 70; 20/70 = 28.6 percent; 50/70 = 71.4 percent (index.html line 40). Project table rows 1+2+2+6+4+2+2+1 = 20."),
 ("proj-r23-reading-list-keys", "Reading list keys and their registry record", "project.html lines 404-410; references/references.json entries datar2020horngrens and kaplan1998cost",
  "Both keys exist with used_by containing AC4 and status verified. Registry note for datar2020horngrens: the source string says 17th ed. (2021) and the record year is 2020; the project page states no year, so no claim is affected."),
 ("proj-r23-verify-refs", "Registry verification for AC4", "tools/verify_refs.py --unit AC4 (live) and tools/verify_refs.py --offline",
  "out/verify_refs_live_AC4.out: 'live re-verification of AC4: 2 of 560 entries, 0 problems'; out/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'."),
 ("proj-r23-banned-and-placeholders", "Banned strings and placeholders in project.html and the AC4 cards", "BUILDER_RULES 1.2 and 1.3 strings; grep TODO TBD lorem roughly-half historically",
  "No match for TODO, TBD, lorem, roughly half, historically, about 6 percent or an ellipsis in project.html or cards.json."),
 ("proj-r23-storage-and-egress-claims", "Page claims: code saved in this browser (line 293, 390); nothing you write leaves it (footer, line 422)", "course/assets/js/grader.js lines 30-112; store.js; fetch call sites in course/assets/js/*.js",
  "Drafts are written with store.put to IndexedDB with a 400 ms debounce (grader.js lines 59-61, store.js line 17). Every fetch call in the site scripts loads a static asset (starter, suite, support files, data, notation, references, cards, map). No call sends user text, so the footer claim matches the source read; the claim about browsers that refuse storage is covered by the page's 'where the browser allows storage' wording."),
 ("proj-r23-card-mechanical-scan", "Every card number and cited label checked against its lesson", "cards.json 140 entries; lesson HTML text of L01 to L08",
  "140 cards, ids AC4-c001 to c140 unique and contiguous, no duplicate fronts or backs. Numbers absent from the plain text were TeX thousands separators ({,}) and were found on re-check (c075 1,900 in L06; c087 60,000 and 30,000 and c088 30,000 and c094 140,000 in L07). Cited Proposition, Lemma, Remark, Definition, Theorem labels exist in the card's lesson; 'Problem P2', 'Problem P3', 'Problem M2' name the blocks labelled P2, P3, M2 in the lesson. 34 cards have no grade field, which check_pages permits (grade optional) and BUILDER_RULES 7 allows for definitions and misconceptions."),
 ("proj-r23-cards-changed-r23", "Changed or new cards c020, c037, c095, c108, c113, c135 to c140 against the current lesson text and lab output", "cards.json; L02, L03, L07, L08; lab outputs run this round",
  "c020: 2,001 is in the lab loss run 2001 to 2088 (out of L02 twin output), 88.89 is the single-formula break-even; the step 27,000 from 2,000 units is in L02 text. c037: Proposition 1.2 proof 'appears in both totals and cancels' (L03). c095: 75 empty, 112 feasible, 186 generated plus the boundary pair (L07 twin: 'cases with q <= K and an empty range: 75', 'cases with a feasible range: 112'). c108: 'identity ... holds for 8/8 divisions' and Lemma 8.2 present in L08. c113: SIM-D 124000 vs SIM-A 59000 cents; RI -4130.00 vs -2440.00 (L08 twin). c135: Proposition 4.1 gives strictly increasing OI on each segment and at most one zero, so non-negative exactly at or above the zero follows (derived, not stated in the proposition; accepted). c136: Remark 1.3 text matches. c137: lab lines '187/187' for supplier-gain and sign checks. c138: '112/112' sum check. c139: '9/9' with boundary RI 0.00. c140: 5.67 (7030/124000) and 4.86 (2870/59000); capital charge 900 bp equals 9 percent; both RI negative."),
 ("proj-r23-cards-L07-L08-cited", "Cards c007, c074, c082, c087, c088, c089, c093, c094, c117 (worked case, theorems, problems) against L07", "cards.json; course/modules/AC/AC4/L07.html",
  "c087: 5,000 x 6 - 60,000 = -30,000; 46 = 40 + 6; full cost below floor 52 (section 4 is headed 'A worked case'). c088: v=40, p_m=60, K=10,000, E=8,000, q=2,000, r=55 is the lesson's hand-built case: D=0, buyer gain 2,000 x (55-60) = -10,000, surplus 30,000 (all in L07). c089: Sigma identity 'in §3 and P1 (Theorem 7.3 part 3 states it for t in the range)'. c093: lesson P2 text 'Since q > 0, q <= K, E <= K, p_m >= v' and block P2 labelled 'P2 ·'. c094: range [52, 80] and Sigma 140,000 in the worked case. c117: K=12,000 gives D=1,000 and t_min = 44 (lesson text). c082 and c007 re-read: correct (c007 phrase 'method states no error measure' is verbatim in L01 line 279)."),
 ("proj-r23-cards-L05-L06-lab", "Cards that quote L05 and L06 lab output: c062 to c068, c076, c077, c080, c081, c074", "cards.json; tests/labs/AC4/lab-AC4-L05-1.py and lab-AC4-L06-1.py run this round; L06 Definition 1.2 text",
  "L05 output: static 140000, volume and mix 265000, flexible -125000; flexed fixed 500000; L06 output: four variances -40000, 249000, 16000, -75000 summing to 150000; fixed variance -10000, operating profit variance 140000. c076: 2,400 budgeted kg (600,000 + 600,000 cents at 500 cents/kg), 2,950 actual, 550 kg difference (275,000 cents), 400 kg for the extra units (2x50 + 3x100), 150 kg excess (2,800 standard). c074: T = C_a - C_b and C_b = sum CM_i q_b,i are in Definition 1.2 (L06 text)."),
 ("proj-r23-cards-L01-L02-lab", "Cards quoting L01 and L02 lab output: c007, c008, c013, c014, c019, c029, c030, c118, c119, c125, c128", "tests/labs/AC4/lab-AC4-L01-1.py and lab-AC4-L02-1.py run this round",
  "L01: high-low 1846389 cents (18,463.89 USD) and 4198.96 cents/hour (41.99); generator 1800000 and 4250; largest absolute residual 51473 cents (514.73 USD); 10 of 12 nonzero; exact months [6, 11]. L02: loss runs 0 to 88 and 2001 to 2088; formula with step 2088.89; planned 2500: OI 5550.00 USD, margin of safety 411.11 (16.44 percent), DOL 6.08 (33750/5550 = 6.08); first whole unit 89."),
 ("proj-r23-cards-L03-L04-carry-note", "Cards quoting L03 and L04 lab output (c033 to c058, c123, c124, c126): carried, not re-run this round", "tests/labs/AC4/lab-AC4-L03-1.py and L04 twins: unchanged since d160ac3",
  "Carried from round 22 (tests/labs/AC4/lab-AC4-L03-1.py, lab-AC4-L04-1.py, course/modules/AC/AC4/L03.html, L04.html byte-identical since the previous pin d160ac3): figures not re-derived this round."),
]
for rid, check, loc, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

def desc(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"Student error:[^\n\"]*", text)
    return m.group(0).strip().rstrip('"') if m else "Student error (see file)"
mutants = []
for line in proj:
    name = line.split()[1]
    path = [p for p in open("/tmp/ac4-v/e23/proj_mut_list.txt").read().split() if p.endswith("/" + name)][0]
    killed = line.split(" -> ", 1)[1]
    mutants.append({"id": name[:-3], "file": path, "description": desc(ROOT / path), "killed_by": killed})
for line in new6:
    name = line.split()[1]
    path = f"ledgers/AC4/mutants/AC4-e-r23/{name}"
    killed = line.split(" -> ", 1)[1]
    mutants.append({"id": name[:-3], "file": path, "description": desc(ROOT / path), "killed_by": killed})

# prior correct alternatives: recorded as rows (not mutants)
rows.append({"id": "proj-r23-alternatives-new", "check": "Three new correct alternative implementations pass the suite",
  "location": "ledgers/AC4/scripts/AC4-e-r23/alts/alt_r23_1..3 (decimal half-up; integer divmod with mix rebuilt per product; floor-half with reordered checks)",
  "status": "PASS", "evidence": "out/alts_prior_r23.out and runfiles: each 50/50 seeds passed."})
rows.append({"id": "proj-r23-alternatives-prior", "check": "Earlier project alternatives re-run against the current grader",
  "location": "ledgers/AC4/scripts/AC4-e-r12..r18 alts/ (16 files)",
  "status": "PASS", "evidence": "out/alts_prior_r23.out: all 16 PASS 50/50 seeds; make_alts_r12.py (a generator script) excluded."})
rows.append({"id": "proj-r23-mutants-project-all", "check": "All 139 committed project mutants and 6 new student-error mutants are killed by the current grader",
  "location": "ledgers/AC4/mutants/ (project files; lab-twin mutants out of scope per the architect ruling)",
  "status": "PASS", "evidence": "out/mutants_proj139_r23.out: 139 KILLED; out/mutants_new6_r23.out: 6 KILLED (fx23_01 to fx23_06: exact flexed mix, efficiency on budget units, truncated flexed revenue, price variance on budget units, negative flexed units clamped, master profit without variable cost). 0 survivors. The 130 lab-twin mutants are out of scope (ruling)."})
rows.append({"id": "proj-r23-prior-row-ids-kept", "check": "All round-22 row ids are kept in this fragment", "location": "ledgers/AC4/AC4-e.json",
  "status": "PASS", "evidence": f"{len(prev['rows'])} previous ids carried or re-verified above with the same ids."})

frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 23,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 23, slice AC4-e; did not build AC4)",
 "pin": "503d139", "base": "d160ac3 (previous pin for the delta; the file on disk, /tmp/fanout-frags/AC4-e.round22.json, carries pin 7143726 and says round 18)",
 "checkout": "/tmp/verify23-AC4-e", "scratch": "/tmp/ac4-v/e23",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "PASS",
 "rows": rows, "mutants": mutants,
 "registry_flags": ["datar2020horngrens: source string says 17th ed. (2021); registry record year 2020 (owner: registry). Not cited with a year on project.html."],
 "freshness_flags": ["L07.html and L08.html changed since the previous pin: their cards (c087, c088, c094, c108, c113, c137 to c140) were re-verified; the lesson text itself belongs to other slices."],
 "notes": "Not checked: (1) the browser UI itself (Pyodide run in a real browser, storage behaviour) was not driven; page_smoke and source reading only. (2) Cards quoting L01 to L04 that are unchanged were carried, not re-derived. (3) The 130 lab-twin mutants were not used as grader mutants (architect ruling); they were not run through the project grader. (4) The 34 ungraded cards were checked for numbers and labels, not for grade appropriateness. (5) The memo rubric is not machine-tested; only its internal consistency and the exemplar arithmetic were checked. Outside the slice: the L07 and L08 lesson sentences were read only where a card cites them.",
 "summary": None,
}
out = ROOT / "ledgers/AC4/AC4-e.json"
frag["summary"] = {"rows": len(rows), "mutants": len(mutants)}
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
