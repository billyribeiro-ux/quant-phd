"""Build ledgers/BK4/BK4-a.json (round 1, closing delta) from the round-13 base fragment.

Rows re-verified this round carry fresh evidence (FRESH). Every other base row is carried with the carry prefix,
because the files it cites are byte-identical between the base pin e919577b and the pin 95f3f8cb (checked with
git diff --quiet; see notes). Row ids are kept. New rows cover the cards changed by the delta.
"""
import datetime
import json
import sys

BASE_PATH = "/Users/billyribeiro/.fanout/frags/E-BK4-a.round13.json"
OUT = sys.argv[1]
base = json.load(open(BASE_PATH, encoding="utf-8"))
S = "ledgers/BK4/scripts/BK4-a-r1/"
PAGES = "course/modules/BK/BK4/index.html, L01.html, L02.html, L03.html and tests/labs/BK4/"

FRESH = {
    "BK4a-hub-placement-keys": "Re-verified this round. FC1 L05.html:63 (the one FC1 line the key depends on) read with sed -n 63p: six states in the order order entry, matching, trade capture, clearing, settlement, position update, so Clearing comes before Settlement (FC1 L05.html changed only after the lifecycle list in e919577..HEAD). index.html:80,85,90,95,99,108,117,122,131 byte-identical since e919577b (git diff empty). Arithmetic keys re-read on the page: 110/1.1=100; 1+1/2+1/4=1.75; lim 2x at 3 is 6; Bertrand price c; grade C; rung-1 answer 20; rung-2 first survivor.",
    "BK4a-hub-prereq-chain": "Re-verified this round with python -I: curriculum/curriculum.json module entries BK4 (prereqs ['FC1']) and FC1 (prereqs ['P0.1','E1']) are identical between e919577b and HEAD; the file changed only in the M3 project brief. index.html:35,61 byte-identical (git diff empty). FC1 index.html changed only in wording, and its prerequisite sentence still names P0.1 and E1.",
    "BK4a-hub-P0.1-link": "Re-verified this round: ls course/modules/P0 returns 'No such file or directory'; index.html:35 byte-identical since e919577b (git diff empty).",
    "BK4a-hub-bertrand-trade-fee": "Re-verified this round: grep -n -i -E 'bertrand|present value|geometric|\\blim' over L01.html, L02.html, L03.html, project.html and grader/*.py (project.html and grader changed in this delta, so re-run). Matches are only plain-prose 'limit' (L03.html:55; project.html:215; grader comments at test_project.py:12,464,603,899). No Bertrand, present value or geometric-series use. index.html:65 byte-identical.",
    "BK4a-hub-concept-anchors": "Re-verified this round: course/concepts.html (byte-identical since e919577b) has id=\"clearing-and-settlement\", id=\"trade-lifecycle\" and id=\"bank-money-creation\" (grep -o). index.html:63-66 byte-identical; L01.html:37, L02.html:37,275 and L03.html:37 byte-identical; check_pages and check_dag this round PASS (ledgers/BK4/scripts/BK4-a-r1/).",
    "BK4a-hub-ladder-vs-project": "Re-verified this round because project.html changed. index.html:150-156 is unchanged. project.html:45 (rung 1: 'one default on a four-member clearing house') and :54 ('Both labs use one illustrative clearing house with four members ... integer cents ... 40 scenarios') are unchanged apart from the link anchors (defined under Conventions). project.html:220 (layer order: margin, default fund, CCP capital, then survivors) is byte-identical (sed -n 220p diff). project.html:38 changed only the link to the rubric and conventions. Hub facts still agree.",
    "BK4a-hub-reading-list": "Re-verified this round because references/references.json changed (generated_at and the used_by of black1973pricing only). The two records cited by index.html:186-194 are JSON-identical between e919577b and HEAD: duffie2011central (title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', Duffie and Zhu, Review of Asset Pricing Studies 1(1) 74-95, 2011) and bisndbasel. index.html byte-identical. Crossref check in BK4a13-crossref-duffie.",
    "BK4a-L01-FC1-claim": "Re-verified this round because FC1 L05.html changed. course/modules/FC/FC1/L05.html:63 (sed -n 63p, current pin) lists the six lifecycle states from order entry to settlement (order entry, matching, trade capture, clearing, settlement, position update). L01.html:55 byte-identical.",
    "BK4a-L01-dag-defs": "Re-verified this round: check_dag BK4 PASS (ledgers/BK4/scripts/BK4-a-r1/check_dag_BK4.txt, exit 0) covers the concept links at L01.html:37,59,64 and the dfn ids; L01.html byte-identical.",
    "BK4a-L01-lab-twin": "Re-verified this round: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L01-1.py run from /tmp exits 0 (ledgers/BK4/scripts/BK4-a-r1/twin_L01.stdout, twin_L01.stderr empty); page code equals the twin up to the trailing newline (lab_code_compare_r1.txt); expected block equals a fresh run (lab_embeds_r1.txt); run_labs BK4 8/8 (run_labs_BK4.txt).",
    "BK4a-L02-lab-twin": "Re-verified this round: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L02-1.py exits 0 (twin_L02.stdout); code equal to the twin up to the trailing newline (lab_code_compare_r1.txt); expected block equals the fresh output (lab_embeds_r1.txt); run_labs BK4 8/8.",
    "BK4a-L02-attribution": "Re-verified this round: L02.html:277,285,425 byte-identical (attribute only the question that is the title of duffie2011central). duffie2011central JSON-identical to e919577b. Plain curl https://api.crossref.org/works/10.1093/rapstu/rar001 returns HTTP 200 with title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?' and container Review of Asset Pricing Studies, volume 1, issue 1, pages 74-95, 2011 (crossref_duffie_r1.json). Abstract not readable (BK4a10-duffie-abstract-access).",
    "BK4a7-hub-skip-rule-vs-project": "Re-verified this round: project.html:43 is byte-identical to e919577b (sed -n 43p diff empty), and index.html:71,150 are byte-identical. Both pages state the same rule: passing the placement bar with both skill checks skips rungs 1 and 2.",
    "BK4a7-L02-duffie-attribution-abstract": "Re-verified this round: L02.html:277,285,425 byte-identical; duffie2011central JSON-identical; Crossref HTTP 200 this round (crossref_duffie_r1.json) confirms title, authors, container, year and pages. Abstract not readable, and no finding is attributed to the paper.",
    "BK4a7-gate-check-projects": "Re-run this round: .venv/bin/python tools/check_projects.py --unit BK4 printed 'check_projects BK4: PASS' with exit 0 (check_projects_BK4.txt). project.html and the grader changed in this delta, so this was re-run.",
    "BK4a-gate-check-pages": "Re-run this round: .venv/bin/python tools/check_pages.py --unit BK4 printed 'check_pages BK4: PASS' with exit 0 (check_pages_BK4.txt). cards.json changed in this delta, and check_pages validates its ids, lessons and grades.",
    "BK4a-gate-check-dag": "Re-run this round: .venv/bin/python tools/check_dag.py --unit BK4 printed 'check_dag BK4: PASS' with exit 0 (check_dag_BK4.txt). FC1 pages changed in this delta, and the BK4 links into FC1 concepts are checked here.",
    "BK4a-gate-run-labs": "Re-run this round: .venv/bin/python tools/run_labs.py --unit BK4 printed 'run_labs BK4: PASS (8/8)' with exit 0 (run_labs_BK4.txt).",
    "BK4a-gate-page-smoke": "Re-run this round: .venv/bin/python tools/page_smoke.py --unit BK4 --pages index L01 L02 L03 printed 'page_smoke BK4: PASS' with exit 0 (page_smoke_BK4_index_L01-L03.txt).",
    "BK4a-gate-ruff-mypy": "Re-run this round: .venv/bin/python -m ruff check tests/labs/BK4 'All checks passed!' (ruff_check_twins.txt); ruff format --check '8 files already formatted' (ruff_format_twins.txt); mypy --no-incremental tests/labs/BK4 'Success: no issues found in 8 source files' (mypy_twins.txt). All exit 0.",
    "BK4a-gate-pytest-labs": "Re-run this round: .venv/bin/python -m pytest tests/test_labs.py -k BK4 -q exits 0, all dots (pytest_labs_BK4.txt); .venv/bin/python -m pytest tests/test_page_checks.py -q exits 0 (pytest_page_checks.txt).",
    "BK4a-gate-verify-refs": "Re-run this round: .venv/bin/python tools/verify_refs.py --offline printed 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs_offline.txt). The live run (verify_refs --unit BK4) was not repeated; no network step was requested for this delta.",
    "BK4a-gate-repo-ruff-mypy-r4": "Re-run this round on tests/labs/BK4: ruff check and ruff format --check and mypy --no-incremental all exit 0 (ruff_check_twins.txt, ruff_format_twins.txt, mypy_twins.txt).",
    "BK4a10-gates": "Re-run this round, all PASS: check_pages BK4, check_dag BK4, check_projects BK4, run_labs BK4 8/8, page_smoke BK4 (index, L01-L03), verify_refs --offline (560 entries, 0 problems), ruff, mypy, pytest test_labs -k BK4 and test_page_checks. run_graders is not in this slice (project slice). Outputs in ledgers/BK4/scripts/BK4-a-r1/.",
    "BK4a10-lab-run": "Re-run this round: each of the three twins run alone with .venv/bin/python -I -W error exits 0 (twin_L01/L02/L03.stdout, stderr files); run_labs BK4 8/8.",
    "BK4a10-lab-embed": "Re-run this round: check_lab_embeds.py over the current checkout with the fresh twin outputs (lab_embeds_r1.txt): expected blocks equal a fresh run for L01, L02 and L03 (True). Page code equals the twin up to the trailing newline (the embed step drops it, as before; lab_code_compare_r1.txt shows equal after the trailing-newline strip).",
    "BK4a9-lab-embed-r9": "Re-run this round (ledgers/BK4/scripts/BK4-a-r1/lab_embeds_r1.txt): expected blocks equal the fresh outputs for L01, L02, L03; code equal up to the trailing newline.",
    "BK4a-lab-block-equality-r4": "Re-run this round (lab_embeds_r1.txt): expected blocks for L01, L02, L03 equal the fresh twin outputs; code equal up to the trailing newline (lab_code_compare_r1.txt).",
    "BK4a5-twins-alone": "Re-run this round: the three twins lab-BK4-L01-1.py, lab-BK4-L02-1.py and lab-BK4-L03-1.py each exit 0 with .venv/bin/python -I -W error from /tmp (twin_L0x.stdout, stderr).",
    "BK4a5-links-anchors": "Re-run this round: check_pages BK4 PASS (check_pages_BK4.txt) covers internal links and anchors on index, L01-L03; those four pages are byte-identical to e919577b.",
    "BK4a5-hub-prereq-uses": "Re-run this round: check_dag BK4 PASS (check_dag_BK4.txt): no concept outside the prerequisite closure is linked from index.html:61-66. index.html is byte-identical.",
    "BK4a10-links": "Re-run this round: check_pages BK4 PASS (check_pages_BK4.txt), which checks the internal links of index, L01-L03; those pages are byte-identical.",
    "BK4a10-concept-closure": "Re-run this round: check_dag BK4 PASS (check_dag_BK4.txt). FC1 pages changed in this delta; the closure is the one check_dag computes from curriculum.json. Concept links in index.html and L01-L03 point only to FC1 concepts and earlier BK4 definitions.",
    "BK4a9-cards-L01-L03": "Re-verified this round because cards.json changed (by-id comparison with e919577b, ledgers/BK4/scripts/BK4-a-r1/cards_delta_r1.txt). Cards with lessons L01-L03 are now L01 18, L02 24, L03 25 (67 cards; the round-13 row said 17+25+24=56, which was a stale location string; the evidence count of 67 is the right one). Changed in range: BK4-c012, BK4-c013, BK4-c107 (checked on the rows below); BK4-c032 (L02, checked below); BK4-c103 removed (L02). Unchanged cards are JSON-identical to e919577b and carried. No duplicate id, front or back (cards_delta_r1.txt).",
    "BK4a10-cards-all": "Re-verified this round: cards.json has 100 cards (L01 18, L02 24, L03 25, L04 19, L05 14). Versus e919577b (101 cards): BK4-c100 (L05) and BK4-c103 (L02) removed, BK4-c107 (L03) added, and BK4-c012, c013, c032, c088, c089 changed (cards_delta_r1.txt). Duplicate id, front and back scans are clean. Content of the changed cards is checked in their own rows; BK4-c088 fails and is recorded as BK4a-r1-card-c088.",
    "BK4a12-cards-delta": "Re-verified this round: cards.json lines 349-377 are byte-identical to e919577b (diff of sed -n 349,377p is empty; the file has no line shifts above line 683, since the changed hunks before that keep their line counts). BK4-c044, c046 and c047 are JSON-identical and match L03.html:145-147 and L03.html:168-169 (carried line content).",
    "BK4a10-delta-hunks": "Re-verified this round: BK4-c094 and BK4-c106 are JSON-identical to e919577b (cards_delta_r1.txt lists neither as changed). BK4-c094 is an L05 card checked against L05.html:486 (4375/2 rounds to 2188; L05.html byte-identical). L03.html:563-567 is byte-identical (diff empty), so the Example 1.5 table at l565 is unchanged.",
    "BK4a9-registry-bisndbasel": "Re-verified this round: bisndbasel is JSON-identical between e919577b and HEAD (python -I comparison of references/references.json entries). Its used_by lists BK1 and BK4; the BK4 pages do not cite it (grep).",
    "BK4a9-duffie-access": "Re-verified this round: plain curl https://doi.org/10.1093/rapstu/rar001 (-L) returned HTTP 403 at https://academic.oup.com/raps/article-lookup/doi/10.1093/rapstu/rar001 (a bot-check page; not bypassed). Title confirmed via Crossref HTTP 200 (crossref_duffie_r1.json). No claim in slice a depends on the abstract.",
    "BK4a10-duffie-abstract-access": "Re-verified this round: plain curl to the DOI returns HTTP 403 at the recorded OUP URL (bot check; not bypassed). The title is read through Crossref (HTTP 200). The abstract is not read, and no abstract claim is made.",
    "BK4a10-bis-index": "Re-verified this round: plain curl https://www.bis.org/committees/cpmi/publications returns HTTP 200; the title is 'CPMI publications | Bank for International Settlements', matching the registry title (index-level only).",
    "BK4a10-registry-no-waterfall": "Re-verified this round: over references/references.json (560 entries, python -I scan), 'counterparty' matches only duffie2011central; no record mentions 'waterfall' or 'margin'. L03.html:417 and :651 state that the registry holds no CCP waterfall or margin-behaviour source, and L03.html is byte-identical.",
    "BK4a12-L03-canon-no-register": "Re-verified this round: L03.html:651 is byte-identical; the references scan (BK4a10-registry-no-waterfall) finds no CCP waterfall or margin record.",
    "BK4a12-checkout-hygiene": "Re-verified this round because several listed files changed in e919577..HEAD (outside BK4 content). git diff --quiet e919577b HEAD on the listed files: IDENTICAL for index.html, L01-L03.html, tests/labs/BK4, notation/notation.json, course/assets/data/market/MANIFEST.json, tools/data_sources.yaml, references/review_queue.json, course/concepts.html, course/index.html, tools/check_pages.py, check_dag.py, run_labs.py, page_smoke.py, verify_refs.py, ledger.py, check_projects.py. CHANGED but outside BK4 content: CURRICULUM.md and curriculum/curriculum.json (the M3 covariance-matrix brief line only; BK4 module entry identical), references/references.json (generated_at and black1973pricing used_by FC2; duffie2011central and bisndbasel identical). render_curriculum.py reproduces the committed CURRICULUM.md and curriculum.json.",
    "BK4a10-mutants-na": "Re-verified this round: slice a has no grader and no mutant set (the BK4 grader and project.html are slice b-d paths). The standing mutant set for slice a is empty, so ruling 37 has nothing to run here. The grader changed in this delta and is outside slice a.",
    "BK4a10-recheck-status": "Re-verified this round: the BK4 paths changed between e919577b and HEAD are cards.json, grader/test_project.py and project.html only (git diff --stat). index.html, L01-L03.html, the twins, notation, data and the registry files for this slice are byte-identical or changed only outside BK4 content (see BK4a12-checkout-hygiene).",
    "BK4a13-lab-twin-trailing-newline": "Re-verified this round: lab_code_compare_r1.txt shows that for L01, L02 and L03 the page code equals the twin after html-unescaping and stripping the trailing newline.",
}

NEW_ROWS = [
    {"id": "BK4a-r1-card-c012", "check": "cards delta: BK4-c012 (L01, grade C)",
     "location": "course/modules/BK/BK4/cards.json BK4-c012 (basis changed); L01.html:409 (E3), :286 (Part C text), :275-279 (printed amounts)",
     "status": "PASS",
     "evidence": "Basis now reads 'Lab 1, Part C (the two amounts printed); the share is computed on the page (Problem E3)'. L01.html:286 says Part C prints the amount moved (1533900) and gross (2841600) and that the lab does not print the ratio; L01.html:409 (E3 solution) computes 1533900/2841600 = 0.5398 from 0.53980152. The card back (0.5398, base is the gross value) matches. The label 'Problem E3' is the lesson's own problem id (E3 · The settled share of gross value, L01.html:406); the lesson's problem headings use the id form (L01.html:341-405). Grade C names the lab, as required for a printed-number result."},
    {"id": "BK4a-r1-card-c013", "check": "cards delta: BK4-c013 (L01, grade T)",
     "location": "course/modules/BK/BK4/cards.json BK4-c013; L01.html:322, :104-111 (Prop 2.4), :71 (A2), :59",
     "status": "PASS",
     "evidence": "New back: 'Not for a net payer ... Net settlement can lower the funds a bank must find at settlement, but it does not remove the settlement funding of a bank that is a net payer.' L01.html:322 says the same (RTGS need 112500 for Bank A with DNS debit 0; net settlement does not remove funding for a net payer). Basis cites Definition 2.1, A2 (L01.html:71) and Proposition 2.4 (L01.html:104), which is the RTGS-need-versus-net-debit comparison. Grade T is backed by the Proposition 2.4 statement at L01.html:104 and its proof at L01.html:110 (k = m in the minimum; unchanged). No scope word beyond 'not'."},
    {"id": "BK4a-r1-card-c032", "check": "cards delta: BK4-c032 (L02, grade C, cites duffie2011central)",
     "location": "course/modules/BK/BK4/cards.json BK4-c032; L02.html:277,285,425; references/references.json duffie2011central",
     "status": "PASS",
     "evidence": "New back: 'The question is whether a CCP reduces counterparty risk, which is the title of the paper. This lesson states no answer to it.' L02.html:277 says the question is their title and uses the same abbreviated wording. Registry title (Crossref HTTP 200, crossref_duffie_r1.json): 'Does a Central Clearing Counterparty Reduce Counterparty Risk?'. The card paraphrases the title with the defined abbreviation CCP (L02.html:64, Definition 1.2); it does not add a finding or a second source. Not verbatim, but the same question, and the lesson uses the same wording."},
    {"id": "BK4a-r1-card-c088", "check": "cards delta: BK4-c088 (L05, grade T): hypotheses carried by front and back",
     "location": "course/modules/BK/BK4/cards.json BK4-c088 (front and back changed); L05.html:68-73 (A3, A4), :85 (Prop 2.1 hypotheses), :94-95 (Prop 2.2 hypotheses: A1, A2, A3), :113-114 (Prop 2.4 hypotheses: A1, A2, A4)",
     "status": "FAIL",
     "summary": "Missing hypothesis (ruling 26 kind): the front drops A3 while the back's comparison relies on Proposition 2.2, which needs A3.",
     "evidence": "New front: 'Assuming the finite probability space, A1 and A2, with A4 for comonotone failures, do dependent failures cost more on average than independent failures (Proposition 2.4)?' The previous front named 'A3 for independent failures and A4 for comonotone failures'; the delta deleted the A3 clause. The new back says 'the same as under A3 (Proposition 2.2)'. L05.html:94-95 gives Proposition 2.2 the hypotheses 'the finite space of Assumption 1.3, and A1, A2 and A3'. So the card's answer uses A3 and Proposition 2.2 without stating A3 as a hypothesis, and the term 'independent failures' is not defined in the card (its name in L05.html:72 is the only link). Math is right (L05.html:114: E[C] = p kappa sum l_i under A1, A2, A4; L05.html:94-95 gives the A3 value); the defect is the hypothesis list. Basis 'Proposition 2.4 (proof in Section 2); Proposition 2.2 and Proposition 2.1' is consistent with the lesson (L05.html:119).",
     "fix": "Restore the A3 clause in the front: 'Assuming the finite probability space, A1 and A2, with A3 for independent failures and A4 for comonotone failures, do dependent failures cost more on average than independent failures (Proposition 2.4)?' Keep the back. Then re-run check_pages BK4 and this row's check."},
    {"id": "BK4a-r1-card-c089", "check": "cards delta: BK4-c089 (L05, grade T)",
     "location": "course/modules/BK/BK4/cards.json BK4-c089; L05.html:148 (Example 2.7), :360",
     "status": "PASS",
     "evidence": "New clause 'Under A1 and A4 it is p, which is 64/512 for p = 1/8': L05.html:148 (Example 2.7) says 'Under A4 it is p=64/512'; 1/8 = 64/512 (exact, arithmetic). 169/512 = 1-(7/8)^3 and 192/512 = 3/8 match L05.html:148. Hypotheses A1 and A3/A4 are stated in the front. cards_delta_r1.txt: labels Example 2.7 found in L05; numbers found in lesson text."},
    {"id": "BK4a-r1-card-c107", "check": "cards delta: BK4-c107 (new, L03, grade T)",
     "location": "course/modules/BK/BK4/cards.json BK4-c107; L03.html:133-134 (Definition 2.1), :139 (loss covered in full iff L <= M), :183-184 (Remark 2.6)",
     "status": "PASS",
     "evidence": "Back: 'No. The cover counts only the scenarios whose loss the margin pays in full. A scenario with a loss above the margin is not counted, even when the waterfall pays all of it.' Definition 2.1 counts c(M) = #{s : L_s <= M} (L03.html:134); Remark 2.6 (L03.html:183-184) says the cover does not count scenarios the default fund or the CCP capital pays, and a scenario with loss above the margin is uncovered in this sense even when the waterfall pays all of it. Basis 'Remark 2.6 (what the cover does not count)' matches the Remark's title (L03.html:183). The scope word 'only' is backed by Definition 2.1. Labels Definition 2.1 and Remark 2.6 found in L03 (cards_delta_r1.txt)."},
    {"id": "BK4a-r1-cards-removed-c100-c103", "check": "cards delta: removed cards BK4-c100 (L05) and BK4-c103 (L02) leave no dangling reference",
     "location": "course/modules/BK/BK4/cards.json (ids absent); L05.html:113-119 (Prop 2.4), L02 Problem P3",
     "status": "PASS",
     "evidence": "cards_delta_r1.txt: removed ['BK4-c100', 'BK4-c103'], no other card cites them by id (grep over cards.json for the two ids: none). check_pages BK4 PASS (ids, lessons and grades valid after removal). Proposition 2.4 still has a card (BK4-c088, see BK4a-r1-card-c088). Problem P3 is still a problem on L02; removing its card leaves the lesson unchanged."},
]

rows = []
carried_prefix_files = {
    "BK4a-hub-data-status": "course/modules/BK/BK4/index.html, tools/data_sources.yaml, course/assets/data/market/MANIFEST.json (byte-identical since e919577b; the two tool and data files were checked with git diff --quiet)",
    "BK4a10-data-manifest": "course/assets/data/market/MANIFEST.json (byte-identical since e919577b)",
    "BK4a-L01-notation": "course/modules/BK/BK4/L01.html, L02.html, L03.html, notation/notation.json (byte-identical since e919577b)",
    "BK4a10-notation": "notation/notation.json and course/modules/BK/BK4/L01.html, L02.html, L03.html (byte-identical since e919577b)",
    "BK4a9-notation-local-symbols": "course/modules/BK/BK4/L01.html, L02.html, L03.html and notation/notation.json (byte-identical since e919577b)",
    "BK4a12-registry-sec-t1": "course/modules/BK/BK4/L01.html, index.html and references/review_queue.json (byte-identical since e919577b)",
    "BK4a12-grade-legend-template": "course/modules/BK/BK4/L01.html and BLUEPRINT.md (byte-identical since e919577b)",
    "BK4a-hub-P0.1-grade-source": "course/modules/BK/BK4/index.html and BLUEPRINT.md (byte-identical since e919577b)",
    "BK4a-hub-financial-intermediary": "course/modules/BK/BK4/index.html and course/concepts.html (byte-identical since e919577b)",
    "BK4a-hub-settlement-framing": "course/modules/BK/BK4/index.html (byte-identical since e919577b)",
    "BK4a7-L01-legend-B-template": "course/modules/BK/BK4/L01.html (byte-identical since e919577b)",
}
for r in base["rows"]:
    rid = r["id"]
    if rid in FRESH:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": FRESH[rid]})
    else:
        files = carried_prefix_files.get(rid, PAGES + " (byte-identical since e919577b)")
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": f"Carried from round 13 ({files}): " + r["evidence"]})
rows += NEW_ROWS

now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
fails = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "BK4",
    "slice": "a",
    "round": 1,
    "round_note": "Closing delta verification (ruling 30) from base fragment round 13 (pin e919577b). Ruling 37: no new mutants.",
    "verifier": "independent verifier (Haiku 5.5), closing delta round 1",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 fragment E-BK4-a.round13.json, verdict PASS, 138 rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-BK4-a",
    "scratch": "ledgers/BK4/scripts/BK4-a-r1/ (scripts and outputs kept; /tmp used only for copies of twin stdout/stderr)",
    "verified_at": now,
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Delta e919577b..95f3f8cb for slice a: course/modules/BK/BK4/cards.json (BK4-c012, c013, c032, c088, c089 changed; c100 and c103 removed; c107 added), and project.html and grader/test_project.py (outside slice a; the hub row BK4a-hub-ladder-vs-project re-verified because it quotes project.html). index.html, L01-L03.html and tests/labs/BK4 are byte-identical to e919577b.",
        "Shared files that changed outside BK4 content: references/references.json (generated_at; black1973pricing used_by FC2), curriculum/curriculum.json and CURRICULUM.md (M3 brief line), course/modules/FC/FC1/* (FC1 wording, L05.html line 63 tail), course/assets/data/program.json. Each BK4 subject that depends on them was re-verified (rows with fresh evidence).",
        "Row BK4a-r1-card-c088 is FAIL: the front of BK4-c088 dropped the A3 hypothesis that its back uses through Proposition 2.2. Fix: restore 'with A3 for independent failures and A4 for comonotone failures' in the front. This is the only non-PASS row.",
        "Gates re-run on pin 95f3f8cb and all PASS: check_pages BK4, check_dag BK4, check_projects BK4, run_labs BK4 8/8, page_smoke BK4 (index, L01-L03), ruff check and format and mypy --no-incremental on tests/labs/BK4, pytest tests/test_labs.py -k BK4 and tests/test_page_checks.py, verify_refs --offline (560 entries, 0 problems).",
        "Observation (not a FAIL kind, ruling 26): BK4-c106 (L01) has no grade field and no basis; check_pages accepts it because it states no grade. Not changed in this delta.",
        "Observation (wording): BK4-c032 paraphrases the title with the defined abbreviation CCP; the lesson uses the same wording (L02.html:277).",
        "Not checked: verify_refs --unit BK4 (live network run; not requested for this delta); run_graders and mutate_graders (project slices, not in slice a); Duffie abstract (OUP bot check, HTTP 403 reproduced with plain curl, not bypassed); full pytest suite (targeted only, per the test-what-changed rule); the BK4 project.html and grader changes are not verified in this slice.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(fails),
        "carried": sum(1 for r in rows if r["evidence"].startswith("Carried from round 13")),
        "fresh_or_new": sum(1 for r in rows if not r["evidence"].startswith("Carried from round 13")),
        "mutants": 0,
    },
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows", len(rows), "fail", [r["id"] for r in fails], "verdict", frag["verdict"])
