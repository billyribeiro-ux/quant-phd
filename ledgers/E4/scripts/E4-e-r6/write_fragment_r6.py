"""Write the round-6 fragment for E4 slice e from the evidence recorded under ledgers/E4/scripts/E4-e-r6/out/."""
import json
import sys
from datetime import datetime, timezone

OUT = "ledgers/E4/scripts/E4-e-r6/out"
S = "ledgers/E4/scripts/E4-e-r6"
CARD = "course/modules/E/E4/cards.json"

rows = [
    {"id": "E4-e-r4-scan", "check": "2.7-cards-scan", "location": CARD,
     "status": "PASS",
     "evidence": f"Command: .venv/bin/python -I {S}/dump_cards.py {CARD} -> {OUT}/dump_cards.out. TOTAL 220 keys [back, basis, cite, front, grade, id, lesson]; per lesson L01 17, L02 22, L03 15, L04 24, L05 27, L06 31, L07 21, L08 41, L09 22 (sum 220, same as round 5). Unique ids 220; no duplicate front or back text (python -I check, output in this round's transcript)."},
    {"id": "E4-e-r4-refs", "check": "2.7-cards-vs-lessons", "location": f"{CARD} (all 220 cards); scratch/txt/L01.txt to L09.txt rendered from course/modules/E/E4/L0*.html by {S}/html_to_text.py",
     "status": "PASS",
     "evidence": f"Every card read against the full current text of L01 to L09 (scratch/txt, 1707 lines, read in full, including Lab printed blocks, Problem sets, Key results and quiz). Card numbers vs lesson text: {S}/card_numbers_r6.py -> {OUT}/card_numbers_r6.out: only 1 token not literal in its own lesson (E4-c037 '3/32', which L02 writes as \\tfrac{{3}}{{32}} at line 0079); its value is correct."},
    {"id": "E4-e-r4-numbers", "check": "2.2-numbers", "location": f"{CARD}; L01-L09 prose and quiz numbers",
     "status": "PASS",
     "evidence": f"Command: .venv/bin/python -I {S}/rederive_r6.py > {OUT}/rederive_r6.out: 116 checks, every line OK, FAILS []. Covers 340/3, 56, 596/3, 235/4; prices (1/8,1/32,1/16); demands (9/4,9/2,9/4),(7/4,7/2,7/4); MRS 4,2,1/2 and price ratios; R2 derivatives 1/12, 1/4; L04 ranks and augmented ranks; L05 fixed points, error ratios -1/4, -1, -3/2, paths; L06 kappa 2, sigma_eta^2 2, theta 3/7 and 6/7, slope 7/9, posterior variance 2/3, x_I 1/7, x_U -1/7, alternative residual -9/85 (hand check: 1/2 * (-18/85) = -9/85); L07 rho^2 and Var(p) sweeps 4/9..1/66 and 729/1444..35937/4802; L08 G(0)=ln2/4, G(1)=ln(5/3)/4, bisection roots 0.965625410, 0.657828572, 0.231615819, Corr^2 0.088941, 0.013061, boundary gaps 7.71e-3 and -6.71e-3; L09 500 strict, 0 nonnegative on meet, 625 zero-posterior bets, 15625 bets."},
    {"id": "E4-e-r4-lab-output", "check": "2.5-labs", "location": "tests/labs/E4/lab-E4-L01-1.py to lab-E4-L09-1.py; <pre class=\"expected\"> block of each L0x.html",
     "status": "PASS",
     "evidence": f"Command: .venv/bin/python -I {S}/expected_vs_twin.py $PWD -> {OUT}/expected_vs_twin.out: for each of the nine twins, python -I -W error exit 0, empty stderr, stdout equals the lesson expected block, and the lesson's single <pre> code block equals the twin source. L05, L07 and L08 twins changed since round 5; all re-run."},
    {"id": "E4-e-r4-run-labs", "check": "2.5-run-labs", "location": "tools/run_labs.py --unit E4",
     "status": "PASS",
     "evidence": f"Command: .venv/bin/python tools/run_labs.py --unit E4 > {OUT}/run_labs_E4.out (exit 0): 'run_labs E4: PASS (12/12)'."},
    {"id": "E4-e-r4-delta", "check": "delta", "location": "git diff 7376a5e2 4bd8cb94 -- course/modules/E/E4 tests/labs/E4",
     "status": "PASS",
     "evidence": "git log 7376a5e2..4bd8cb94: 2d755599 and 4bd8cb94. Diff touches L01-L09.html (wording and prose), cards.json (14 insertions, 14 deletions on 12 cards: c052 back; c086, c107, c121, c123, c139, c199, c209, c210, c218 fronts; c123 and c218 backs; c179 and c184 basis), grader/project files (other slices), tests/labs/E4/lab-E4-L05, L07, L08 (docstring and comment wording only). Every hunk in cards.json and in the lesson pages was read; each changed card was re-verified against the current lesson text (rows E4-e-r4-cards-L01..L09). references/, notation/ and tools/ are unchanged in the delta."},
    {"id": "E4-e-r4-notation", "check": "2.4-notation", "location": "notation/notation.json vs course/modules/E/E4/L0*.html math and cards.json",
     "status": "PASS",
     "evidence": "Registry symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}: 0 occurrences in lesson math (\\( \\) and \\[ \\] spans, python scan this round). In cards.json, bare T occurs only as the transpose superscript in E4-c053, c055 and c218 (zeta^T A); the lessons write the same operator as \\top. It is not the registry count symbol T. Plain Q does not occur in cards."},
    {"id": "E4-e-r4-citations", "check": "2.1-attribution", "location": "cards.json E4-c099 (cite muth1961rational); L05.html data-cite muth1961rational; L09.html References (milgrom1982information)",
     "status": "PASS",
     "evidence": "references/references.json (unchanged in delta): muth1961rational title 'Rational Expectations and the Theory of Price Movements', container Econometrica, volume 29, issue 3, year 1961, DOI 10.2307/1909635, verified_by crossref. c099 and L05 data-locator 'title' use only that title. milgrom1982information: title 'Information, trade and common knowledge', Journal of Economic Theory 26(1) 17-27, 1982, matching L09 References (no card cites it)."},
    {"id": "E4-e-r4-verify-refs", "check": "2.1-registry", "location": "references/references.json",
     "status": "PASS",
     "evidence": f"Command: .venv/bin/python tools/verify_refs.py --offline > {OUT}/verify_refs_offline.out (exit 0): 'offline integrity: 560 entries, 0 problems'. The live --unit run is not performed here (see notes)."},
    {"id": "E4-e-r4-check-pages", "check": "2.9-structure", "location": "tools/check_pages.py --unit E4; tools/check_dag.py --unit E4; tools/page_smoke.py --unit E4 --skip-sweep",
     "status": "PASS",
     "evidence": f"Commands (exit 0 each): check_pages.py --unit E4 -> 'check_pages E4: PASS' ({OUT}/check_pages_E4.out, includes check_cards); check_dag.py --unit E4 -> 'check_dag E4: PASS'; page_smoke.py --unit E4 --skip-sweep -> 'page_smoke E4: PASS' ({OUT}/page_smoke_E4.out). The live figure sweep was skipped."},
    {"id": "E4-e-r4-banned", "check": "2.9-banned", "location": f"{CARD}; course/modules/E/E4/L0*.html",
     "status": "PASS",
     "evidence": "grep -n -i -E 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree' over cards.json and L01-L09.html: no hits."},
    {"id": "E4-e-r4-grades", "check": "2.3-grades", "location": f"{CARD} grade and basis fields; Key results tables of L01-L09",
     "status": "PASS",
     "evidence": f"Python count: T 147, C 19, absent 54 (definition, assumption and setup cards), same as round 5. Each C card names a finite check, exact-arithmetic finite grid, or SIMULATED seeded draw in basis ({S}/card_numbers_r6.py output). Each T card is proved on the page or reproduced exactly by a lab part with exact arithmetic or a closed form; the seeded values (E4-c124, c125, c146, c181, c223) are C."},
    {"id": "E4-e-r4-cards-L01", "check": "2.7-cards", "location": "cards.json E4-c001..c016, E4-c221 vs scratch/txt/L01.txt",
     "status": "PASS",
     "evidence": "Every card read against the full L01 text. Values 340/3, 56, 596/3, 235/4 and the Lab 1 printed block match (lab output in out/expected_vs_twin.out). Hypotheses: c004 and c007 assume A1, c010 assumes A1 and A2, matching the Propositions. c016 matches Lab 1 main() (check_probabilities runs before Part A)."},
    {"id": "E4-e-r4-cards-L02", "check": "2.7-cards", "location": "cards.json E4-c017..c038 vs scratch/txt/L02.txt",
     "status": "PASS",
     "evidence": "Every card read against L02 (Definitions 2.1-2.3, Lemma 2.4, Propositions 2.5, 2.8, 2.9, Corollary 2.7, Example 2.11, Lab 2 Parts B-E). Prices (1/8,1/32,1/16), demands, residuals 0, ratios 16/9 and 16/7 equal 1/w_i, v=(1,-1,0) value 3/32 and endowment cost 9/16 re-derived (E4-e-r4-numbers). E4-c031 and c036 use ebar = (4,8,4) correctly."},
    {"id": "E4-e-r4-cards-L03", "check": "2.7-cards", "location": "cards.json E4-c039..c052, E4-c214 vs scratch/txt/L03.txt",
     "status": "PASS",
     "evidence": "Every card read against L03. Changed card E4-c052 now reads 'the Arrow–Debreu security prices define' (see E4-e-r5-terms). E4-c049 derivatives 1/12 and 1/4 and the MRS values 4, 2, 1/2 for both agents re-derived. E4-c048 and c214 counts 0 and 2 with the 125-point grid match the lab output and my own enumeration (rederive_r6.py)."},
    {"id": "E4-e-r4-cards-L04", "check": "2.7-cards", "location": "cards.json E4-c053..c073, E4-c215, E4-c217, E4-c218 vs scratch/txt/L04.txt",
     "status": "PASS",
     "evidence": "Every card read against L04. Changed card E4-c218 (kernel dimension J - rank(A), nonzero when rank(A) < J) matches Remark 3.2 and rank-nullity in the lesson text. Ranks 2 and 3, augmented ranks 2, 3, 3, and the (1-t, 2-2t, 3-3t, t) family re-derived by Gaussian elimination (rederive_r6.py)."},
    {"id": "E4-e-r4-cards-L05", "check": "2.7-cards", "location": "cards.json E4-c074..c099, E4-c219 vs scratch/txt/L05.txt",
     "status": "PASS",
     "evidence": "Every card read against L05. Changed card E4-c086 now carries the hypotheses A1 to A3, matching Lemma 3.1. Fixed points (4, -3/10), (5/2, -3/16), (2, -3/20), paths 0,5,15/4,65/16; 0,5,0,5; 0,5,-5/2,35/4 and the error ratios -1/4, -1, -3/2 re-derived. E4-c099 is the muth1961rational title-only card."},
    {"id": "E4-e-r4-cards-L06", "check": "2.7-cards", "location": "cards.json E4-c100..c129, E4-c220 vs scratch/txt/L06.txt",
     "status": "PASS",
     "evidence": "Every card read against L06 (Definitions 6.1-6.6, Lemmas 6.2-6.4, Proposition 6.7, Corollary 6.8, Example 6.9, Lab 1 Parts A-E). Changed cards E4-c107 (A1 and A4 of L06) and E4-c121 (A1 to A4 and G, Proposition 6.7) now name their hypotheses; E4-c123 names the alternative theta_s = 1/2 with theta_u unchanged, matching the lab. Residual -9/85 and x_U = -1/7 re-derived by hand and in rederive_r6.py; Part E values 0.426617 and 0.761928 with tolerances match the lab output."},
    {"id": "E4-e-r4-cards-L07", "check": "2.7-cards", "location": "cards.json E4-c130..c150 vs scratch/txt/L07.txt",
     "status": "PASS",
     "evidence": "Every card read against L07. Changed card E4-c139 now names Proposition 7.6 as its hypothesis. Sweep values 4/9, 1/3, 1/6, 1/18, 1/66 (sigma_u), 1/6, 1/3, 9/22 (lambda), 4/9, 1/3, 1/6 (a), Var(p) 729/1444 and 35937/4802 re-derived exactly (rederive_r6.py). Seeded value 0.330625 matches the lab output."},
    {"id": "E4-e-r4-cards-L08", "check": "2.7-cards", "location": "cards.json E4-c151..c188, E4-c222..c224 vs scratch/txt/L08.txt",
     "status": "PASS",
     "evidence": "Every card read against L08 (Sections 1-5, Lab 1 printed block, Mech 1-3, Emp 1-3, Res 1-3, quiz). Changed card E4-c179 names A4 and Proposition 5.2(c), and E4-c184's basis now reads 999 interior fractions, matching Part D. G(0)=ln2/4, G(1)=ln(5/3)/4, bisection roots and Corr^2 values re-derived in double precision by rederive_r6.py; Part A residual 1.332e-15 and slope 0.1595 vs 0.1605 match the seeded lab output."},
    {"id": "E4-e-r4-cards-L09", "check": "2.7-cards", "location": "cards.json E4-c189..c211 (c202 absent) vs scratch/txt/L09.txt",
     "status": "PASS",
     "evidence": "Every card read against L09 (Definitions 1.1-1.2, Theorem 2.1, Corollary 2.3, Example 2.4, Lab 1 Parts A-C, Misconceptions 1-4, Problems Mech 1-3, Proof 1-3, Emp 1-3, Res 1-3). Changed card E4-c199 names B1 and B2; cards E4-c209 and c210 name B1 to B3. E4-c211 states the two-prior bet with p and r, where Problem Res 2 now writes nu_1 and nu_2; the statement agrees, and the letters are not registry symbols. Counts 500, 0, 625 and 15625 re-enumerated exactly (rederive_r6.py); c202 is absent by design (no reference in any file, see E4-e-r6-ids)."},
    {"id": "E4-e-r5-terms", "check": "2.4-terms", "location": f"{CARD} E4-c052 back (the round-5 failing row)",
     "status": "PASS",
     "evidence": "E4-c052 back now reads 'the Arrow–Debreu security prices define'. grep -n -i 'state.price' over course/modules/E/E4 (cards and L0*.html) returns nothing, so the term forbidden by plans/E4-build-plan.md section 4 D2 ('Do not use the term state price') is absent. Plural 'security prices' is the lesson's own term (L01 Definition 1.6 defines the Arrow–Debreu security price vector; Proposition 1.7 uses security prices)."},
    {"id": "E4-e-r5-tooling", "check": "2.5-tooling", "location": "tests/labs/E4/*.py; tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
     "status": "PASS",
     "evidence": "Commands: .venv/bin/ruff check tests/labs/E4 -> 'All checks passed!'; .venv/bin/ruff format --check tests/labs/E4 -> '12 files already formatted'; .venv/bin/mypy --no-incremental tests/labs/E4 -> 'Success: no issues found in 12 source files'; .venv/bin/python -m pytest -q -k 'E4 or lab' tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -> all dots, no failures."},
    {"id": "E4-e-r5-c212", "check": "2.7-removed-card", "location": f"{CARD} (E4-c212 removed since round 4)",
     "status": "PASS",
     "evidence": "git grep -c 'E4-c212' -- course tests tools notation references: 0 files. Card ids present: 220 unique; missing numbers in 1..224 are 202, 212, 213, 216, none referenced anywhere (see E4-e-r6-ids)."},
    {"id": "E4-e-r6-changed-cards", "check": "2.7-delta-cards", "location": f"{CARD}: E4-c052, c086, c107, c121, c123, c139, c180 (basis), c184 (basis), c199, c209, c210, c218",
     "status": "PASS",
     "evidence": "Each changed card's new text read against the current lesson text (scratch/txt, rendered this round). Every added hypothesis ('Assuming A1 to A3', 'Under the hypotheses of Proposition 7.6', 'Assuming B1 to B3', 'Assuming A1 and A4 of L06') is a hypothesis the cited result uses. E4-c123 matches the lab's alternative theta_s = 1/2 with theta_u = 6/7. E4-c052 now uses the security-prices term (E4-e-r5-terms)."},
    {"id": "E4-e-r6-ids", "check": "2.7-duplicates-and-ids", "location": f"{CARD} ids and fronts/backs",
     "status": "PASS",
     "evidence": "220 unique ids, no duplicate front or back text (python check). Gaps 202, 212, 213, 216 are referenced by no file (git grep -l 'E4-c202|E4-c213|E4-c216' over course, tests, tools, notation, references: 0 files; E4-c212 0 files). Ids need not be sequential (plan section 2.1, Architect ruling 2)."},
]

fragment = {
    "unit": "E4",
    "slice": "e",
    "round": 6,
    "verifier": "independent verifier (Haiku 5.5), unit E4, slice e: all 220 cards in course/modules/E/E4/cards.json against lessons L01-L09",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin; frags/E-E4-e.round5.json used as context only; delta read in full)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-E4-e",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE6-E4-e/scratch/txt (L01.txt to L09.txt, rendered by ledgers/E4/scripts/E4-e-r6/html_to_text.py; not committed)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scope: all 220 cards read against the current text of L01 to L09 (full reads, scratch/txt). Round 5 failing row E4-e-r5-terms is fixed (E4-c052). "
        "Round-6 delta re-verified rather than carried: cards.json and the lesson pages changed, so every card was re-read. "
        "No card defect found. Non-blocking observations for the lesson owner (not card defects): (1) cards use 'Arrow–Debreu security prices' where D2 names the 'Arrow–Debreu security price vector'; both are the lesson's terms and 'state price' is absent. "
        "(2) Card basis labels 'Proposition 3.1 (a)' and '(b)' follow the proof's wording ('This proves (a)', then '(b)' by running it backwards); the lesson bullets themselves are unlabelled. "
        "(3) Card ids 202, 212, 213, 216 are unused; ids need not be sequential. "
        "(4) E4-c211 uses p and r for the two priors while Problem Res 2 now uses nu_1 and nu_2 (same statement; non-blocking notation difference). "
        "Not checked in this slice: project.html and grader (other slices); index.html hour split; the live verify_refs --unit E4 run (offline integrity run only); the live figure sweep of page_smoke (--skip-sweep); the Muth and Milgrom abstracts (registry fields only, no paper text read); the mutation gate (no grader in this slice); the rule of section 2.5 for lab runtime under 10 s (not timed here)."
    ),
    "summary": "cards 220; rows 26 (pass 26, fail 0, unverifiable 0); verdict PASS; numeric re-derivation rederive_r6.out (116 checks, FAILS []).",
}

json.dump(fragment, open("ledgers/E4/E4-e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows))
