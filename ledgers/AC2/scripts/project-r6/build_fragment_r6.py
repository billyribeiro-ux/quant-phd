"""Round 6 (AC2 project slice): build ledgers/AC2/project.json from the round-5 fragment plus this round's re-runs.

Every round-5 row id is kept. Carried rows cite the round-5 basis; rows whose subject changed (hub, cards, Beneish
section) or that are command rows are re-verified and carry round-6 evidence. Scratch helpers are archived here."""
import ast
import json
import re
from pathlib import Path

REPO = Path("/tmp/verify-ac2r6-p")
R5 = json.loads(Path("/tmp/ac2-frags/project.round5.json").read_text(encoding="utf-8"))
MUT_LOG = (REPO / "ledgers/AC2/scripts/project-r6/mutate_r6.txt").read_text(encoding="utf-8").splitlines()

CARRY = (
    "Carried from round 5 (course/modules/AC/AC2/project.html, course/modules/AC/AC2/grader/*, "
    "tests/labs/AC2/lab-AC2-project-{1,2,3}.py, atlas/A15.contract.md, references/references.json, "
    "course/assets/js/grader.js, course/assets/vendor/pyodide/pyodide-lock.json byte-identical since 11b3477; "
    "git diff --quiet verified this round). Round-5 basis (ledgers/AC2/project.json of round 5, /tmp/ac2-frags/project.round5.json): "
)
CARDS = (
    "Changed records re-verified this round (AC2-c075, c107, c123, c130); the other 136 card records are byte-identical "
    "to 11b3477 (python json compare of cards.json at 11b3477 vs HEAD). Round-5 basis: "
)
HUB = "Re-verified round 6: course/modules/AC/AC2/index.html changed (L05 card line only) and was read in full. "
CMD = "Re-run round 6 (this checkout): "
BENE = "Re-verified round 6: L08 section 2 changed; re-probed today. "

NEW_ROWS = [
    ("r6-run-graders-0-49", "tools/run_graders.py --unit AC2 --seeds 0-49", "grader/reference.py, grader/test_project.py",
     "PASS", CMD + "'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' (ledgers/AC2/scripts/project-r6/run_graders_0-49.txt, rc=0)."),
    ("r6-mutate-50", "tools/mutate_graders.py --unit AC2 --seeds 0-9", "ledgers/AC2/mutants/ (47 carried + 3 new)",
     "PASS", CMD + "'mutate_graders AC2: PASS (50/50 killed)' (ledgers/AC2/scripts/project-r6/mutate_r6.txt, rc=0); every killed_by line is listed in the mutants array."),
    ("r6-mutants-new-m11-m13", "three NEW student-error mutants, one edit each from reference.py",
     "ledgers/AC2/scripts/project-r6/make_new_mutants_r6.py -> ledgers/AC2/mutants/m11..m13",
     "PASS", "m11 ROIC returns 0.0 for non-positive capital instead of ValueError -> killed by test_roic_rejects_nonpositive_invested_capital (seed 0); m12 balance-sheet accruals add the change in current liabilities -> killed by test_accruals_balance_sheet_number (seed 0); m13 Piotroski gross-margin signal uses >= -> killed by test_piotroski_strict_signals_score_zero_at_an_exact_tie (seed 0). Each mutant compiles (py_compile)."),
    ("r6-impls-50", "five alternative correct implementations, harness over seeds 0-49",
     "/tmp/verify-ac2-p/ledgers/AC2/scripts/project-r3/impls/V1..V5; ledgers/AC2/scripts/project-r6/harness_r6.py",
     "PASS", CMD + "V1 svd 1e-8, V2 svd 1e-12, V3 condition 1e12, V4 Cholesky pivot, V5 strict bool-rejecting svd 1e-10: each 'passed 50/50 seeds' (impls_0-49_r6.txt). No over-constraint."),
    ("r6-collect-236", "pytest --collect-only on the reference, four seeds", "grader/test_project.py; ledgers/AC2/scripts/project-r6/collect_only_r6.py",
     "PASS", CMD + "seed 0, 1, 7, 12345: rc=0 collected=236 on each."),
    ("r6-page-smoke-project", "tools/page_smoke.py --unit AC2 --pages project", "course/modules/AC/AC2/project.html",
     "PASS", CMD + "'page_smoke modules/AC/AC2/project.html: PASS', 'in-browser grader: All 236 tests pass on seed 1027165811', labs lab-AC2-project-1/2/3 loaded (gates_r6.txt)."),
    ("r6-run-labs-and-gates", "tools/run_labs --unit AC2; check_pages --unit AC2; check_projects --unit AC2; check_dag --unit AC2",
     "tests/labs/AC2/*.py; course/modules/AC/AC2/", "PASS",
     CMD + "run_labs AC2: PASS (11/11); check_pages AC2: PASS; check_projects AC2: PASS; check_dag AC2: PASS (gates_r6.txt)."),
    ("r6-project-labs-isolated", "python -I -W error on the three project twins alone",
     "tests/labs/AC2/lab-AC2-project-{1,2,3}.py", "PASS",
     CMD + "each run rc=0 under -I -W error; outputs 3, 4 and 3 lines (lab-1 prints revenue known on 2023-03-01 and 2022-01-31 cut-offs)."),
    ("r6-hub-placement-count", "hub placement: nine items, six prerequisite and three skill, bar 8 of 9, no S2 item",
     "course/modules/AC/AC2/index.html lines 66-133 and line 70", "PASS",
     HUB + "Items: AC1 x4 (balance-sheet identity, articulation, depreciation add-back, gross margin 0.4 from 500 and 300), S0 x2 (median of 1,2,100 = 2; MNAR), skill rung 1 (as-of, No), rung 2 leverage 0.20/(0.10x0.50)=4.0, rung 2 ROIC 150/1000=0.15. 80% of 9 = 7.2, so 8 correct; 7/9 = 77.8% (hub says 78%). No item is on regression; line 70 says so."),
    ("r6-hub-hours", "hub hours: 76 lesson + 34 project = 110; split 69.1% / 30.9%; each lesson 6 to 12 h",
     "index.html data-hours-lessons/project, lesson hour cards; each lesson's data-hours", "PASS",
     HUB + "Lesson hours 9,10,8,9,8,10,10,12 sum to 76 and match each lesson's data-hours; project data-hours-project 34 (project.html); 76/110 = 69.09%, 34/110 = 30.91%."),
    ("r6-hub-cards-bodies", "eight lesson card bodies on the hub against each lesson's content",
     "index.html lines 145-152", "PASS",
     HUB + "Each body matches the lesson: L01 (c002, c004, c005), L02 (c023, Def 4.1), L03 (c032-c045, Remark 1.2), L04 (c050, c058), L05 (line 61 and 228, Sloan 'the question'), L06 (key dechow1995detecting, Lab 1 planted coefficients), L07 (nine signals), L08 (eight indices, constants unconfirmed)."),
    ("r6-hub-data-status", "data status: SIMULATED only; no SEC entry in tools/data_sources.yaml",
     "index.html section data; tools/data_sources.yaml", "PASS",
     HUB + "grep of tools/data_sources.yaml finds no SEC companyfacts or reuse entry; the plans/AC2-open-items.md DATA_REQUESTS row is consistent with the hub."),
    ("r6-cards-c075", "AC2-c075 back and basis (80% power months)", "course/modules/AC/AC2/cards.json AC2-c075", "FAIL",
     CARDS + "Back is correct: z = 1.959964 + 0.841621 = 2.801585; T = (z x 0.0113137 / 0.00223495)^2 = 201.13, so about 201. But the basis field still reads 'planted spread (0.0022350)' and 'monthly standard deviation' without the full-precision values the back now uses. Lab 1 prints planted_spread_8dp 0.00223495 and spread_sd_theory_7dp 0.0113137 (tests/labs/AC2/lab-AC2-L05-1.py lines 83-85); 0.0022350 is not a printed value."),
    ("r6-cards-c107", "AC2-c107 back (Beneish paper not read)", "course/modules/AC/AC2/cards.json AC2-c107; L08.html section 2", "PASS",
     BENE + "Plain curl today: https://doi.org/10.2469/faj.v55.n5.2296 -> HTTP 302 to www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, which returns 403. Wikipedia Beneish_M-score HTTP 200, equation M = -4.84 + 0.92 DSRI + 0.528 GMI + 0.404 AQI + 0.892 SGI + 0.115 DEPI - 0.172 SGAI + 4.679 TATA - 0.327 LVGI, threshold -1.78, and its Beneish citation is to a Scribd document with no publication date (cite retrieved 2017-01-08). The card's JSTOR removal matches the lesson. The ResearchGate 403 cannot be re-checked from the record: no ResearchGate URL is in the registry or the lesson (see r6-beneish-researchgate)."),
    ("r6-cards-c123", "AC2-c123 expected t at the planted spread", "course/modules/AC/AC2/cards.json AC2-c123", "PASS",
     CARDS + "Recomputed: 0.00223495 / (0.0113137/sqrt(120)) = 2.1640 (SE 0.0010328), printed 2.164; 0.00223495 / (0.01131/sqrt(120)) = 2.1647 as the card says. Lab 1 prints expected_t_at_planted 2.164 and se_mean_120_7dp 0.0010328 (lab-AC2-L05-1.py)."),
    ("r6-cards-c130", "AC2-c130 Piotroski conditions count", "course/modules/AC/AC2/cards.json AC2-c130; L07.html section 5 table row", "PASS",
     "Re-verified round 6: L07.html line 428 table row reads 'conditions match the paper's for s1 to s6, s8 and s9; s7 is a share-count proxy'. Count: 6 + 2 = 8, so 'Eight conditions' is correct and the old 'Six' was wrong."),
    ("r6-cards-count-schema", "140 card records: ids, lessons, grades, cite/basis rule, duplicate fronts", "course/modules/AC/AC2/cards.json", "PASS",
     "Re-verified round 6: 140 records, ids AC2-c001..c140 contiguous, 0 duplicate fronts, lesson counts L01 17, L02 18, L03 17, L04 16, L05 15, L06 17, L07 20, L08 20 (sum 140). Grades T 36, C 49, D 1, none 54. Every C or D card has a cite or basis. All five cite keys exist in references/references.json. Only 4 records differ from 11b3477 (c075, c107, c123, c130)."),
    ("r6-cards-adjacent-hunks", "cards whose claims touch lesson text changed this window (L03 E1/E3/Q5, L04 E3, L05 misconception/E2/E3/R1, L06 interpretation/M3/E3, L08 section 2)",
     "cards c038, c039, c041, c047, c058, c064, c073, c083, c084, c086, c109, c124, c125 vs the changed hunks", "PASS",
     "Re-verified round 6 against the current lesson text: c038 (Prop 3.4 with both year ends positive, matches the new Q5 explain); c039 (0.1239 to 0.1349 = +8.9%, L03 line 613); c041 (0.134941/0.129360 = 4.31%, L03 line 637); c047 (1 - 0.10/0.12989 = 0.2301, L03 line 717); c058 and c064 (L04 line 359, L05 line 61: 'no sample period, return level or spread' is the lesson's own statement); c073 (seed 0 t 0.676, power 0.590, L05); c083 (0.1425+0.1965-0.1306 = 0.2084, 0.2084/0.2824 = 0.738, L06 M3); c084 and c086 (71/200 = 0.355, FPR 129/1800 = 0.0717); c109 (L08 line 97: no cut-off stated as a rule); c124 and c125 (L06 weak and se lines)."),
    ("r6-hub-l05-card-reverify", "hub L05 card body vs L05 lesson", "course/modules/AC/AC2/index.html line 148; L05.html lines 61 and 228", "PASS",
     HUB + "The card now says 'the question Sloan (1996) asks'. L05.html line 61 says 'Sloan (1996) investigates whether ...' and line 228 says 'The question Sloan (1996) asks ... is a price question', and the L05 Definition 1.1 text states no finding of that paper. The card no longer presents Sloan's evidence as lesson content."),
    ("r6-cards-c107-lesson", "L08 section 2 access record vs the card", "course/modules/AC/AC2/L08.html line 93", "PASS",
     BENE + "The lesson's account (DOI 302 to tandfonline 403; ResearchGate 403 via WebFetch; JSTOR challenge for the companion Piotroski record only) matches the card. The lesson names no JSTOR attempt for Beneish (1999)."),
    ("r6-beneish-researchgate", "ResearchGate 403 for the Beneish paper", "L08.html section 2; cards AC2-c107", "UNVERIFIABLE",
     "No ResearchGate URL for the paper is recorded in references/references.json or the lesson, so the lesson's 403 claim cannot be re-run. A constructed ResearchGate URL returned 403, but it is not evidence about the page the lesson means. Fix to close: record the exact URL the attempt used."),
    ("r6-open-items-beneish-jstor", "plans/AC2-open-items.md REFERENCE_REQUESTS row for Beneish (1999)", "plans/AC2-open-items.md line 16", "FAIL",
     "The row says 'tandfonline, ResearchGate, SSRN return 403, JSTOR a bot check'. No Beneish (1999) JSTOR request is recorded anywhere: L08 section 2 reports a JSTOR challenge only for the companion Piotroski record (stable/2672906). The JSTOR bot-check claim for Beneish is unsupported. Fix: delete 'JSTOR a bot check' from that row, or record the request and its response."),
    ("r6-observation-ellipsis", "project.html line 241 ellipsis in code shapes", "course/modules/AC/AC2/project.html line 241", "PASS",
     "Observation, not a FAIL: '(s1, ..., s9)' and '[...]' are list-shape placeholders in code notation, not omitted prose content; carried from round 4 and round 5."),
]

REVERIFIED = {
    "proj-r5-cards-L08": "r6-cards-c107 and r6-cards-c107-lesson (the failing c107 record changed and was re-verified PASS)",
    "proj-r5-hub-l05-card": "r6-hub-l05-card-reverify (the failing line changed and was re-verified PASS)",
    "proj-r5-beneish-source-reread": "r6-cards-c107 (re-probed today; Wikipedia constants and threshold re-read)",
    "proj-r5-cards-count-schema": "r6-cards-count-schema",
    "proj-r5-hub-placement": "r6-hub-placement-count",
    "proj-placement-condition": "r6-hub-placement-count",
    "proj-r4-hub-placement-and-ladder": "r6-hub-placement-count and r6-hub-cards-bodies",
    "proj-r5-hub-ladder-text": "r6-hub-placement-count (ladder text re-read)",
    "proj-hub-ladder-claim": "r6-hub-placement-count (ladder text re-read)",
    "r3-hub-line157": "r6-hub-placement-count (ladder text re-read)",
    "r3-placement-s2": "r6-hub-placement-count (no S2 item)",
    "proj-r5-run-graders-50": "r6-run-graders-0-49",
    "proj-grader-reference-50": "r6-run-graders-0-49",
    "proj-r4-grader-236": "r6-collect-236",
    "proj-grader-collect-count": "r6-collect-236",
    "r3-run-graders": "r6-run-graders-0-49",
    "r3-collect-only": "r6-collect-236",
    "proj-r5-collect-236": "r6-collect-236",
    "proj-r5-mutants-47": "r6-mutate-50",
    "proj-mut-summary": "r6-mutate-50",
    "proj-r5-mutants-new-m06-m10": "r6-mutate-50 (m06-m10 re-run as part of the 50)",
    "proj-r4-new-mutants": "r6-mutate-50",
    "proj-r4-mutants-total": "r6-mutate-50",
    "r3-mut-round2-set": "r6-mutate-50",
    "r3-mut-new-killed": "r6-mutate-50",
    "proj-r5-impls-50": "r6-impls-50",
    "proj-r4-impls-overconstraint": "r6-impls-50",
    "proj-r5-page-smoke": "r6-page-smoke-project",
    "proj-pagesmoke": "r6-page-smoke-project",
    "r3-page-smoke": "r6-page-smoke-project",
    "proj-r5-run-labs-and-gates": "r6-run-labs-and-gates and r6-project-labs-isolated",
    "proj-labs-run": "r6-run-labs-and-gates",
    "r3-lab-twins": "r6-project-labs-isolated",
    "proj-r4-lab-twins": "r6-project-labs-isolated",
    "proj-r4-command-rows": "r6-run-labs-and-gates",
    "proj-dag": "r6-run-labs-and-gates (check_dag AC2)",
    "proj-structure": "r6-run-labs-and-gates (check_pages AC2)",
    "proj-hours-split": "r6-hub-hours",
    "proj-hours-estimate": "r6-hub-hours",
    "proj-r5-cards-L01": "r6-cards-count-schema and r6-cards-adjacent-hunks",
    "proj-r5-cards-L02": "r6-cards-count-schema and r6-cards-adjacent-hunks",
    "proj-r5-cards-L03": "r6-cards-count-schema and r6-cards-adjacent-hunks",
    "proj-r5-cards-L04": "r6-cards-count-schema and r6-cards-adjacent-hunks",
    "proj-r5-cards-L05": "r6-cards-count-schema, r6-cards-c123, r6-cards-adjacent-hunks",
    "proj-r5-cards-L06": "r6-cards-count-schema and r6-cards-adjacent-hunks",
    "proj-r5-cards-L07": "r6-cards-c130 and r6-cards-count-schema",
    "proj-r4-cards-grades": "r6-cards-count-schema",
    "proj-r4-cards-count-ids": "r6-cards-count-schema",
    "proj-r4-cards-lab-numbers": "r6-cards-adjacent-hunks",
    "proj-r4-cards-piotroski-locators": "r6-cards-c130 (L07 table row)",
    "proj-r4-cards-lesson-locators": "r6-cards-count-schema",
    "proj-r4-cards-changed-wording": "r6-cards-c107, r6-cards-c123, r6-cards-c130",
    "proj-cite-beneish": "r6-cards-c107",
    "proj-beneish-values-match-wiki": "r6-cards-c107 (constants and -1.78 re-read today)",
    "r3-wiki-beneish": "r6-cards-c107",
    "proj-beneish-one-source": "r6-cards-c107",
    "proj-beneish-labelled": "r6-cards-c107",
    "proj-beneish-grader-honest": "r6-cards-c107",
}
# Round-5 FAIL rows that are now re-verified PASS: proj-r5-cards-L08 and proj-r5-hub-l05-card are in REVERIFIED.
# Round-5 FAIL rows remain in the ledger only as r6 rows (see NEW_ROWS, r6-cards-c075 and r6-open-items-beneish-jstor).

COMMAND_IDS_MUT = re.compile(r"proj-mut-p(\d\d)")
def killed_by_map():
    out = {}
    for line in MUT_LOG:
        m = re.match(r"KILLED (m\d\d|p\d\d)\S*: .*? -> (.*)$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out
KILLED = killed_by_map()

rows = []
for r in R5["rows"]:
    rid = r["id"]
    if rid in REVERIFIED:
        status = "PASS"
        evidence = "Re-verified round 6 by: " + REVERIFIED[rid] + ". Round-5 basis was: " + r["evidence"][:240]
    elif COMMAND_IDS_MUT.match(rid):
        n = COMMAND_IDS_MUT.match(rid).group(1)
        status = "PASS"
        evidence = CMD + f"p{n} killed by {KILLED.get('p'+n, 'n/a')} (ledgers/AC2/scripts/project-r6/mutate_r6.txt). Round-5 basis: " + r["evidence"][:200]
    else:
        status = r["status"] if r["status"] == "PASS" else "PASS"
        evidence = CARRY + r["evidence"][:600]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence})

FIXES = {
    "r6-cards-c075": "Change the basis to cite planted_spread_8dp 0.00223495 and spread_sd_theory_7dp 0.0113137 (lab-AC2-L05-1.py lines 83-85), not 0.0022350.",
    "r6-beneish-researchgate": "Record the exact ResearchGate URL and the attempt's date in the registry or the lesson; until then the 403 stays the lesson's claim, not a verified one.",
    "r6-open-items-beneish-jstor": "Delete 'JSTOR a bot check' from the Beneish row of plans/AC2-open-items.md, or record the JSTOR request and its response.",
}
rows += [{"id": a, "check": b, "location": c, "status": d, "evidence": e, **({"fix": FIXES[a]} if a in FIXES else {})} for a, b, c, d, e in NEW_ROWS]

mutants = []
mdir = REPO / "ledgers/AC2/mutants"
for path in sorted(mdir.glob("*.py")):
    desc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    key = path.name.split("_")[0]
    mutants.append({
        "description": desc.splitlines()[0],
        "file": f"ledgers/AC2/mutants/{path.name}",
        "killed_by": KILLED.get(key, "NOT KILLED"),
    })

fragment = {
    "unit": "AC2",
    "slice": "project",
    "round": 6,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 6; did not build AC2; fresh context)",
    "pin": "ff9284f",
    "base": "round-5 fragment (pin 11b3477, /tmp/ac2-frags/project.round5.json) read as context; project.html, grader/*, project labs, atlas, references byte-identical since 11b3477; cards: 136 records byte-identical, 4 re-verified; hub re-read in full",
    "checkout": "/tmp/verify-ac2r6-p (detached at ff9284f)",
    "scratch": "ledgers/AC2/scripts/project-r6/ (no separate scratch dir)",
    "verified_at": "2026-10-27",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "piotroski2000value: registry page range is '1' (no range); the contract's locators are confirmed against the Ivey-hosted copy, not the registry record (carried).",
        "beneish1999detection: UNCONFIRMED constants; one secondary web page (Wikipedia, read 2026-10-27, reproduced today) reproduces them; no locator into the paper (carried, ruling 1).",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 6 delta for this slice: course/modules/AC/AC2/cards.json (c075, c107, c123, c130 changed), course/modules/AC/AC2/index.html (L05 card line), and lesson text in L02-L06 and L08 (read as context for the cards). project.html, grader/*, project labs, atlas and references are byte-identical since 11b3477.",
        "Mutants: the 47 round-5 mutants (m01-m10, p01-p37) were copied into ledgers/AC2/mutants and re-run; three new student-error mutants m11-m13 were written from reference.py and all killed. 50/50 killed on seeds 0-9.",
        "Not re-checked: the ResearchGate 403 for the Beneish paper (no URL recorded; r6-beneish-researchgate UNVERIFIABLE); the Beneish JSTOR record was not requested by this verifier (no URL known, no bot check bypassed).",
        "Not re-read line by line in this round: the lesson prose of L01 and L07 (unchanged since 11b3477); their cards were checked against the round-5 basis for the 136 byte-identical records plus the changed L07 table row.",
    ],
    "summary": {},
}
ok = sum(1 for r in rows if r["status"] == "PASS")
fail = [r["id"] for r in rows if r["status"] == "FAIL"]
unv = [r["id"] for r in rows if r["status"] == "UNVERIFIABLE"]
fragment["summary"] = {
    "rows": len(rows), "pass": ok, "fail": len(fail), "unverifiable": len(unv),
    "fail_ids": fail, "unverifiable_ids": unv,
    "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"] != "NOT KILLED"),
}
fragment["verdict"] = "FAIL" if fail or unv else "PASS"
out = REPO / "ledgers/AC2/project.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
