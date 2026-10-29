"""Build the round-12 M3 slice-a fragment from the round-11 rows: carry byte-identical rows, replace re-verified rows."""
import json
import sys

PREV = json.load(open("/Users/billyribeiro/.fanout/frags/B-M3-a.round11.json", encoding="utf-8"))
PIN_PREV = "f42f432"
CARRY_BASE = "Carried from round 11 (cited lines or files byte-identical since the previous pin " + PIN_PREV + "; " \
    "git diff " + PIN_PREV + "..ff38842 touches the slice only at course/modules/M/M3/L02.html:51, 368, 379 and " \
    "course/modules/M/M3/L03.html:261):"
CARRY = {
    "a6-hub-structure", "a6-hub-hours", "a6-hub-placement", "a6-hub-data-claims", "a6-hub-m1-refs", "a6-hub-cards",
    "a6-L01-defs-props-1", "a6-L01-span-prop", "a6-L01-indep-rank-thms", "a6-L01-prop312", "a6-L01-examples",
    "a6-L01-lab-twin-page", "a6-L01-lab-numbers", "a6-L01-lab-claims", "a6-L01-problems", "a6-L01-quiz",
    "a6-L01-key-results", "a6-L01-structure-prose", "a6-L01-misconceptions", "a6-L02-maps-matrices",
    "a6-L02-change-of-basis", "a6-L02-lab-twin-page", "a6-L02-lab-numbers", "a6-L02-lab-claims",
    "a6-L02-quiz-keyresults", "a6-L03-assumption-defs", "a6-L03-example-numbers", "a6-L03-decomp-props",
    "a6-L03-lab-twin-page", "a6-L03-lab-claims", "a6-L03-problems", "a6-L03-quiz-keyresults",
    "a6-L03-misconceptions", "a6-citations", "a6-L01-defuse-e-i", "a6-L01-dag-simple-return",
    "a6-L01-lab-docstring-claim-b", "a6-L02-notation-S", "a6-L03-ex25-independence",
    "a6-L01-lab-generated-inputs-label", "a7-L02-card-M3-c036", "a7-L02-meta-description-B", "a8-L01-card-c014",
    "a8-L01-notation-d", "a8-L01-thm38-math", "a8-L02-q9-option", "a8-cards-c005-c009-c019", "a8-card-c054",
    "a8-L03-fieldset-style", "a9-L01-example-3-10-lab-sentence", "a9-L01-R2-degree-letters",
    "a9-L01-prop312-letter-r", "a9-L02-product-letter-K", "a9-L02-M2-letters-s-t", "a11-L01-R3-float-pivot",
    "a11-L02-composition-sentence", "a11-L02-q7-explain", "a11-L02-R2-honest-gap",
    "a11-hub-curriculum-lab-entry", "a11-live-registry-keys", "a11-hub-M1-quantifier-theorem",
}
NEW = {}

def new(rid, check, location, status, evidence, fix=""):
    NEW[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        NEW[rid]["fix"] = fix

S = "ledgers/M3/scripts/M3-a-r12/"
new("a6-L02-misconceptions-problems", "2.4 math / 2.9 prose", "course/modules/M/M3/L02.html:372-497", "PASS",
    "Re-verified from scratch at ff38842. Misconception 1 (L02.html:379, now qualified): zero map is the zero matrix in every basis; identity is I when input and output bases coincide; with B standard and C=((1,0),(1,1)) the identity map has matrix [[1,-1],[0,1]] (" + S + "numeric_claims.out line 3; hand check: e2 = -1*(1,0) + 1*(1,1)). Misconception 2 (AN=[[2,1],[1,1]], NA=[[1,1],[1,2]]) and misconception 3 ((1,1) has coordinates (0,1) in C) re-derived by hand. Problems: M1 matrix [[2,-1],[1,0]] and M2 (2,1) re-derived; M3 kernel {(0,y)} and image {(x,0)} with Prop 1.4 (L02.html:76) and Prop 2.2 of Lesson 1 (L01.html:97) resolving; P1-P3 proofs checked step by step; E1 scope; E2 AP=[[1,2],[1,0]], P^-1(AP)=[[0,2],[1,0]] re-derived; E3 rejected-draw count 7 matches run_labs L02 output; R1 conversion matrix [id]_{C'<-C} correct; R2 scope correct; R3 matrix [[0,1,0,0],[0,0,2,0],[0,0,0,3],[0,0,0,0]] and action (c1,2c2,3c3,0) re-derived.")
new("a6-L02-structure-prose", "2.9 structure", "course/modules/M/M3/L02.html (whole page)", "PASS",
    "Re-verified at ff38842: check_pages --unit M3 --page L02 PASS; page_smoke --unit M3 --pages L02 PASS; section order s1-s10 at L02.html:53,90,134,152,364,375,393,498,516,601 matches BUILDER_RULES section 4; why-it-matters 116 words (" + S + "prose_scan.out; BUILDER_RULES 4.1 limit 120); banned-phrase and process-word scan clean (prose_scan.out).")
new("a6-L03-structure-prose", "2.9 structure", "course/modules/M/M3/L03.html (whole page)", "PASS",
    "Re-verified at ff38842: check_pages --unit M3 --page L03 PASS; page_smoke --unit M3 --pages L03 PASS; sections s1-s8 in order (L03.html:53,105,158 lab,256,267,285,390,409,490); why-it-matters 77 words; banned/process scan clean (" + S + "prose_scan.out).")
new("a6-dag-concepts", "2.9 DAG / 1.10", "course/modules/M/M3/index.html; L01.html; L02.html; L03.html", "PASS",
    "check_dag --all: 'check_dag M3: PASS' (" + S + "check_dag_all.out). The one new cross-reference, L02.html:51 'composition of maps (defined in Section 3)', is an explicit forward pointer to L02.html:135 (Section 3 defines composition as v -> S(Lv)); no concept is newly used outside the prerequisite closure.")
new("a6-notation-registry", "2.2 notation / BUILDER 3.1-3.2", "notation/notation.json; course/modules/M/M3/index.html, L01.html, L02.html, L03.html", "PASS",
    "notation/notation.json has 8 symbol entries and macro \\R at notation.json:25 (tex \\mathbb{R}). The slice pages use \\R (L02.html grep count 20) and no mbb{R} macro (grep count 0 in L02.html). Symbols B, C, I, e_j, [id] used in the round-12 hunks (L02.html:368, 379, 477) collide with no registered symbol (grep of Phi, gamma_3, R^\\ast, R_f, mathbb{Q} in the four slice pages: no hits). notation.json is byte-identical to the previous pin.")
new("a6-gates-lint-types", "gates", "tests/labs/M3/lab-M3-L01-1.py, lab-M3-L02-1.py, lab-M3-L03-1.py; tests/ -k M3", "PASS",
    "Rerun at ff38842: ruff check tests/labs/M3 -> 'All checks passed!' ; ruff format --check tests/labs/M3 -> '12 files already formatted' (" + S + "ruff_labs_M3.out); .venv/bin/mypy --no-incremental -> 'Success: no issues found in 255 source files' (" + S + "mypy.out); .venv/bin/pytest -q -k M3 tests/ -> 12 passed, exit 0 (" + S + "pytest_labs_M3.out).")
new("a6-render-page-smoke", "2.5 labs / 2.8 / 2.9", "tools/page_smoke.py --unit M3 --pages index L01 L02 L03", "PASS",
    "Rerun alone at ff38842: every page PASS (index, L01, L02, L03; lab-M3-L01-1, lab-M3-L02-1, lab-M3-L03-1 under 0.1 s each); 'page_smoke M3: PASS', exit 0 (" + S + "page_smoke_slice_a.out). Dark-mode and 360 px visual renders were not taken by this verifier beyond the page_smoke sweep.")
new("a8-process-words", "2.9 process words", "course/modules/M/M3/index.html, L01.html, L02.html, L03.html", "PASS",
    "Re-scanned at ff38842 (" + S + "prose_scan.py, prose_scan.out): no hits for round, verifier, builder, agent, draft, placeholder, grader, pending in the four slice pages. The only new phrase in the hunks, 'the lab shows' (L02.html:360, unchanged), describes lab output, not process.")
new("a8-run-labs-m3", "2.5 labs", "tools/run_labs.py --unit M3 (and --page L01, L02, L03); tests/labs/M3/lab-M3-L0{1,2,3}-1.py", "PASS",
    "Rerun at ff38842: 'run_labs M3: PASS (12/12)' (" + S + "run_labs_M3.out); per page 'run_labs M3: PASS (1/1)' for L01, L02, L03, exit 0 each (" + S + "run_labs_L0*.out). Each twin alone under python -I -W error exits 0 (" + S + "twin_alone_L0*.out).")
new("a8-gates-check-pages", "gates", "tools/check_pages.py --unit M3 (and --all); tools/check_dag.py --all", "PASS",
    "Rerun at ff38842: check_pages M3 PASS, L02 PASS, L03 PASS, --all lists 'check_pages M3: PASS' (" + S + "check_pages_*.out); check_dag --all 'check_dag M3: PASS' (" + S + "check_dag_all.out).")
new("a9-L02-basis-order-remark", "2.4 math / 2.9 prose", "course/modules/M/M3/L02.html:368", "PASS",
    "Re-verified on the changed hunk (old L02.html:367, now 368). Zero map: zero matrix in every order (exact). Projection (x,y)->(x,0) with B=C=(e1,e2): matrix [[1,0],[0,0]]; with B=C=(e2,e1): [[0,0],[0,1]] (" + S + "numeric_claims.out lines 4-5, hand check: L(e2)=0, L(e1)=e1 has coordinates (0,1) in (e2,e1)). The script's label 'output basis (e1,e2)' is a mislabel in the script; the value equals the B=C=(e2,e1) matrix. The statement that the matrix changes unless each column that moves equals the column it replaces is correct.")
new("a10-L02-mathbb-R-macro", "2.2 notation / BUILDER 3.1 (macros)", "course/modules/M/M3/L02.html:368; notation/notation.json:25", "PASS",
    "Re-verified on the changed hunk: the basis-order bullet now writes \\R^2 via the registered macro \\R (notation.json:25, tex \\mathbb{R}); grep of L02.html finds no \\mathbb{R}.")
new("a11-L02-misconception1-identity-scope", "2.4 prose / 2.9 structure", "course/modules/M/M3/L02.html:379", "PASS",
    "Fresh check of the round-11 FAIL. The rewritten sentences: zero map has the zero matrix for every choice of bases (true, Definition 2.3); identity map has I when input and output bases coincide (true: L b_j = b_j gives column e_j); with B standard and C=((1,0),(1,1)) the matrix is [[1,-1],[0,1]] (" + S + "numeric_claims.out line 3; hand check: e1=(1,0) has C-coordinates (1,0), e2=(0,1) = -1*(1,0)+1*(1,1) has (-1,1)). 'in general' is a weaker-than-true hedge (the matrix is never I when B and C differ as ordered bases), not a false statement. Example 4.3 and Example 2.6 matrices re-derived (see a6-L02-misconceptions-problems).")
new("a11-L03-eigenvector-only-scalar", "2.4 prose / scope words", "course/modules/M/M3/L03.html:261", "PASS",
    "Fresh check of the round-11 FAIL. The bullet now reads: when an eigenspace has dimension 2 or more, its eigenvectors are not all multiples of one another (true: two independent vectors in the eigenspace are not multiples of each other), and the order of eigenvalues is a labelling choice. Proposition 1.3 (L03.html:71-72, eigenspaces are subspaces) supports 'a nonzero multiple of an eigenvector is again an eigenvector'. Lab 1 sorts eigenvalues before printing (tests/labs/M3/lab-M3-L03-1.py:69-70, 77); lab output checked by run_labs L03.")
new("a11-twin-page-equality", "2.5 labs", ledgers_loc := "tests/labs/M3/lab-M3-L01-1.py; lab-M3-L02-1.py; lab-M3-L03-1.py; course/modules/M/M3/L01-L03.html", "PASS",
    "Rerun at ff38842: " + S + "twin_vs_page.py: L01, L02, L03 page code == twin (True), expected block == fresh run output (True), exit 0, stderr empty; 'ALL OK' (" + S + "twin_vs_page.out). Each twin run alone with python -I -W error exits 0 (" + S + "twin_alone_L0*.out).")
new("a11-cards-L01-L03-full-read", "2.7 cards", "course/modules/M/M3/cards.json (L01: c001-c022, c169-c170; L02: c023-c042, c184; L03: c043-c062, c171-c172)", "PASS",
    "The file changed since the previous pin. Per-card diff of cards.json at f42f432 and ff38842 (" + S + "cards_delta.py, cards_delta.out): changed among L01-L03 are M3-c038 and M3-c040 only; new is M3-c184 (L02). Changed/new cards re-verified: c038 front (3 x 3 integer matrices, coordinate check) matches lab docstring and output 'coordinates of A p_j equal P^-1 A P in 50 of 50 pairs'; c040 back matches L02.html:379 and the Example 2.6 matrix; c184 matches output 'composition matrix equals the product of matrices in 50 of 50 pairs'. Every other L01-L03 card is byte-identical to the round-11 read, and the keyword scan for statements on identity, zero map, basis and eigenvector scalars found no conflict with the new text (c042 consistent).")
new("a11-gates-pytest-dag-verify", "gates", "tests/ -k M3; tools/check_dag.py --all; tools/verify_refs.py --offline; tools/fetch_data.py --check; tools/build_site.py --check", "PASS",
    "Rerun at ff38842: pytest -k M3 12 passed exit 0; check_dag --all M3 PASS; verify_refs --offline 'offline integrity: 560 entries, 0 problems' exit 0 (" + S + "verify_refs_offline.out); fetch_data --check '3 datasets, 0 problems' exit 0 (" + S + "fetch_data_check.out); build_site --check 'site data current: 6 outputs' exit 0 (" + S + "build_site_check.out).")
new("a11-scope-words", "2.2 prose / scope words", "course/modules/M/M3/index.html; L01.html; L02.html; L03.html", "PASS",
    "Re-scanned the changed hunks: L02.html:51 'composition ... (defined in Section 3)'; L02.html:368 'The map has not changed ... unless each column that moves equals the column it replaces' (scope correct: 'unless' is an exact condition); L02.html:379 'for every choice of bases' (zero map, true), 'in general when they differ' (hedge, not false); L03.html:261 'not all multiples' (true for dimension >= 2, claims nothing for dimension 1). No unqualified 'only/all/always/every' claim without computation in the hunks.")
new("a11-banned-phrases-and-process", "2.9 banned phrases", "course/modules/M/M3/index.html; L01.html; L02.html; L03.html", "PASS",
    "Rerun " + S + "prose_scan.py at ff38842 (" + S + "prose_scan.out): no BUILDER_RULES 1.3 banned string (TODO, TBD, lorem, for brevity, beyond the scope, you can add more, filler phrases) in the four pages; the only ellipses are list notation 'e1, ..., e4' (L01.html:207, 339, 354).")
new("a12-L02-why-composition-defined-in-s3", "2.9 structure / 2.2 defined before use", "course/modules/M/M3/L02.html:51, 134-135", "PASS",
    "L02.html:51 now reads 'composition of maps (defined in Section 3)'. Section 3 heading at L02.html:134 ('Composition is matrix multiplication'); L02.html:135 defines composition, S o L = map v -> S(Lv). The forward pointer is explicit, so the term is not used undefined. Why-it-matters is 116 words, within the 120-word limit (" + S + "prose_scan.out).")
new("a12-cards-c038-c040-c184", "2.7 cards", "course/modules/M/M3/cards.json (M3-c038, M3-c040, M3-c184); course/modules/M/M3/L02.html:350-360, 379", "PASS",
    "c038 (grade C, lab result) and c184 (grade C) ask the coordinate and composition counts separately; each answer 'All 50' matches the lab output lines 'coordinates of A p_j equal P^-1 A P in 50 of 50 pairs' and 'composition matrix equals the product of matrices in 50 of 50 pairs' (run_labs L02 output; L02.html:353-354); both counts are finite-computation statements and say so. c040 (grade T) back matches the rewritten misconception L02.html:379 and the Example 2.6 matrix. Source: " + S + "cards_delta.py, cards_delta.out.")
new("a12-cards-duplicate-scan", "2.7 duplicates", "course/modules/M/M3/cards.json (all 184 M3 cards)", "PASS",
    "Full scan (" + S + "cards_delta.out): 184 unique ids; no duplicate fronts; one identical back text, 'All 50 (Lab 1 output). The count is a finite computation...', shared by M3-c038 and M3-c184. The two cards ask different facts (coordinate check; composition check) and are not duplicate cards, but the shared answer text is noted for the builder's awareness; no fix is required by BUILDER_RULES.")

rows = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid in NEW:
        rows.append(NEW.pop(rid))
    elif rid in CARRY:
        if r["status"] != "PASS":
            raise SystemExit("carry of non-PASS row " + rid)
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_BASE + " " + r["evidence"]})
    else:
        raise SystemExit("row not classified: " + rid)
rows.extend(NEW.values())
print("rows", len(rows), "carried", sum(1 for r in rows if r["evidence"].startswith("Carried")))
out = {
    "unit": "M3",
    "slice": "a",
    "round": 12,
    "verifier": "independent Haiku verifier (round 12), not a builder of M3",
    "pin": "ff38842",
    "base": "f42f432 (round-11 pin). Delta f42f432..ff38842 for slice a: course/modules/M/M3/L02.html (lines 51, 368, 379), L03.html (line 261), cards.json (M3-c038, c040 changed; M3-c184 new; other changed cards are outside slice a). index.html, L01.html, lab twins L01-L03, notation/, references/, tools/ and curriculum/ are byte-identical to the previous pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB12-M3-a",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB12-M3-a/ledgers/M3/scripts/M3-a-r12",
    "verified_at": "2026-10-29T12:00:00+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": "Lesson slice: mutants not required (VERIFIER_RULES 2.6 applies to project graders; lab twins are demonstrations, per the rulings). Round-11 FAIL rows a11-L02-misconception1-identity-scope, a11-L03-eigenvector-only-scalar and a6-L02-misconceptions-problems are now PASS after fresh re-derivation. Not verified: project.html and project twins (outside slice a); L04-L09 cards and pages (outside slice a); dark-mode and 360 px visual renders by this verifier (page_smoke sweep only); the live Crossref / Open Library runs (offline registry check only; references unchanged since the previous pin); the Strang edition flag in registry_flags stands.",
    "summary": "Slice a round 12: verdict PASS. All round-11 FAIL rows re-derived and fixed in the text (L02.html:379 identity-matrix scope; L03.html:261 eigenspace bullet; L02 misconceptions/problems range). Round-12 delta read in full (three L02 hunks, one L03 hunk, cards c038/c040/c184). Every gate rerun on ff38842 passed.",
}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written", sys.argv[1])
