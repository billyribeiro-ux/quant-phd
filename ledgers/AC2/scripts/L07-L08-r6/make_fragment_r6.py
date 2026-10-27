"""Build the round-6 fragment for slice L07-L08 (pin ff9284f).

Carried rows keep the round-5 evidence text with the required prefix; every other row
states what was re-run or re-read in round 6.
"""
import json
import sys

R5 = "/tmp/ac2-frags/L07-L08.round5.json"
OUT = sys.argv[1]
CARRY = ("Carried from round 5 (course/modules/AC/AC2/L07.html, tests/labs/AC2/lab-AC2-L07-1.py, "
         "atlas/A15.contract.md, references/references.json byte-identical since 11b3477): ")
CARD_CARRY = ("Carried from round 5 (course/modules/AC/AC2/cards.json entries named here, and "
              "course/modules/AC/AC2/L07.html, byte-identical since 11b3477): ")

d = json.load(open(R5, encoding="utf-8"))
r5 = {r["id"]: r for r in d["rows"]}

# carried rows: L07-only subjects, unchanged since 11b3477
CARRIED = {
    "L07-L08-cite-piotroski2000value", "L07-L08-cite-sloan1996stock", "L07-L08-math-signals-vs-contract", "L07-L08-loc-p1-p3-7.5-23",
    "L07-L08-loc-p12-1448-396", "L07-L08-loc-p7-n2-optimal", "L07-L08-loc-p7-ex-ante-quote",
    "L07-L08-loc-p7-distress-average", "L07-L08-loc-keyresults-2.3", "L07-L08-loc-signal-groups",
    "L07-L08-loc-scaling-p7-p8-p9", "L07-L08-loc-proxies-p7-p8-p9", "L07-L08-loc-p11-sample",
    "L07-L08-loc-p12-groups-bootstrap", "L07-L08-loc-sloan-p8", "L07-L08-math-proxies-stated",
    "L07-L08-math-P1", "L07-L08-math-P2", "L07-L08-math-P3", "L07-L08-math-worked-firm",
    "L07-L08-lab-L07-1", "L07-L08-num-L07-lab-distribution", "L07-L08-grade-L07",
    "L07-L08-r3-piotroski-fetch", "L07-L08-r3-quotes", "L07-L08-r3-recompute-L07",
    "L07-L08-r3-contract-departures", "L07-L08-r3-stock-funded-example", "L07-L08-r3-lab-checks-integer",
    "L07-L08-r3-lab-docstring-pages", "L07-L08-r3-period-7.5", "L07-L08-r4-eqoffer-p9",
    "L07-L08-r4-pdf-printed-pages", "L07-L08-r4-signals-match-claim", "L07-L08-loc-p9-n5-cutoff",
    "L07-L08-loc-p12-groups-bootstrap", "L07-L08-cards-L07-A", "L07-L08-r3-from-recall-L07",
}
CARD_CARRIED = {"L07-L08-loc-p9-n5-cutoff", "L07-L08-cards-L07-A", "L07-L08-r3-period-7.5"}

NEW = {}

def P(i, check, loc, ev):
    NEW[i] = dict(id=i, check=check, location=loc, status="PASS", evidence=ev)

def F(i, check, loc, ev, fix):
    NEW[i] = dict(id=i, check=check, location=loc, status="FAIL", evidence=ev, fix=fix)

def U(i, check, loc, ev, fix):
    NEW[i] = dict(id=i, check=check, location=loc, status="UNVERIFIABLE", evidence=ev, fix=fix)

# ---- command rows (re-run this round) ----
P("L07-L08-cmd-pin", "2.9-structure", "repository (checkout /tmp/verify-ac2r6-l78)",
  "Round 6: git rev-parse --short HEAD -> ff9284f; git status --short -> '?? .venv' only; "
  "git diff --quiet 11b3477 HEAD -- L07.html, both twins, references, atlas -> identical (exit 0).")
P("L07-L08-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC2",
  "Round 6 (ff9284f): 'run_labs AC2: PASS (11/11)', exit 0.")
P("L07-L08-cmd-twins", "2.5-lab", "tests/labs/AC2/lab-AC2-L07-1.py, lab-AC2-L08-1.py",
  "Round 6: each run as python -I -W error from a scratch dir (/tmp/ac2-v/L07-L08-r6/twin-L07, twin-L08): "
  "exit 0, stderr 0 bytes, stdout 533 and 1247 bytes.")
P("L07-L08-cmd-embed", "2.5-lab", "course/modules/AC/AC2/L07.html, L08.html (data-run and expected blocks) vs twins",
  "Round 6: scripts/embed_compare.py (archived) unescapes each page's data-run block and expected block: "
  "L07 code == twin True, expected == stdout True; L08 code == twin True, expected == stdout True. "
  "embed_labs.py was not run on the built pages (it rewrites marker-bearing pages; no check mode).")
P("L07-L08-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages L07 L08",
  "Round 6: exit 0; 'page_smoke modules/AC/AC2/L07.html: PASS', 'page_smoke modules/AC/AC2/L08.html: PASS', "
  "'page_smoke AC2: PASS' (log /tmp/ac2-v/L07-L08-r6/page_smoke.txt).")
P("L07-L08-cmd-check_pages_dag_projects", "2.9-structure", "tools/check_pages.py, check_dag.py, check_projects.py --all",
  "Round 6: check_pages AC2 PASS, check_dag AC2 PASS, check_projects AC2 PASS (each --all).")
P("L07-L08-cmd-lint_mypy", "2.5-lab", "the two twins",
  "Round 6: .venv ruff check -> 'All checks passed!'; ruff format --check -> '2 files already formatted'; "
  "mypy on both twins -> 'Success: no issues found in 2 source files'.")
P("L07-L08-cmd-pytest", "2.5-lab", ".venv/bin/pytest -q -k 'AC2 or ac2 or L07 or L08'",
  "Round 6: exit 0, all selected tests passed (progress 100%, log /tmp/ac2-v/L07-L08-r6/pytest.txt).")
P("L07-L08-cmd-verify_refs", "2.1-citation", "tools/verify_refs.py --unit AC2 (live) and --offline",
  "Round 6: live 'live re-verification of AC2: 7 of 560 entries, 0 problems', exit 0; offline "
  "'offline integrity: 560 entries, 0 problems', exit 0.")

# ---- citation and locator rows carried from round 5 (L07 only) are below; these are re-verified ----
P("L07-L08-cite-beneish1999detection", "2.1-citation", "references/references.json key beneish1999detection; L08 data-cite (lines 56, 95)",
  "Round 6: registry entry: doi 10.2469/faj.v55.n5.2296, verified_by crossref, title 'The Detection of Earnings Manipulation', "
  "container Financial Analysts Journal, volume 55, issue 5, pages 24-36, year 1999. Plain curl to doi.org/10.2469/faj.v55.n5.2296 "
  "returned HTTP 302 to tandfonline.com and then 403 (see L07-L08-r6-access). Key-results row 568 states the model content is not verified: matches.")

P("L07-L08-r2-constants-provenance", "2.1-citation", "course/modules/AC/AC2/L08.html line 93 (and key-results row 566)",
  "Round 6: line 93 now says the page 'cites its coefficient formula to an undated Scribd document ... and cites that document "
  "and a ycharts.com page for its list of eight variables'. Plain curl to en.wikipedia.org/wiki/Beneish_M-score (HTTP 200, "
  "/tmp/ac2-v/L07-L08-r6/wiki.html): 'The formula to calculate the M-score is: [1]' with reference 1 = Messod D. Beneish, "
  "'The Detection of Earnings Manipulation', Scribd; 'The Beneish M-score is calculated using 8 variables ...: [1] [2]' with "
  "reference 2 = 'Beneish M Score Definition', ycharts.com. The line-93 provenance now matches the page. Row 566 names no "
  "locator, matching the page.")
P("L07-L08-r5-card-c107-jstor", "2.7-cards", "cards.json AC2-c107 (back field)",
  "Round 6: AC2-c107 back now reads 'its DOI resolver redirects to a publisher page that returns HTTP 403, and its ResearchGate "
  "page returned HTTP 403'; the JSTOR sentence is gone. Re-run: doi.org 302 then tandfonline 403 (verified); ResearchGate 403 "
  "on the verifier's URL (verified, status only). Card matches L08 line 93.")
P("L07-L08-cards-L07-B", "2.7-cards", "cards.json AC2-c130 (L07); c102, c103, c104, c105, c126, c127 read this round",
  "Round 6: AC2-c130 back now reads 'Eight conditions (s1 to s6, s8, s9)'; the list has eight members (s1, s2, s3, s4, s5, s6, s8, s9), "
  "matching L07 line 90 and key-results row line 428 ('eight'). c102 vector (1,1,1,0,1,1,1,1,1) sums to 8 with s4 failing (matches). "
  "c104 'unchanged for 400 of 400' matches lab output line 301 (400/400). c126 '1,448 and 396 ... (p. 12)' matches L07 line 106. "
  "c127 vector (0,1,0,1,1,1,1,1,1) sums to 7 (matches). c103 and c105 text consistent with L07 §3 and the 1976-1996 sample. "
  "Basis and grade fields: c130 grade C with cite piotroski2000value (unchanged).")
P("L07-L08-r5-used-only-scope", "2.3-grade", "L08.html line 95 ('used only ... in the lab, in the §3 worked M, in misconception 2 and in quiz item 5')",
  "Round 6 read of the whole page: the candidate constants also produce numbers in problem E1 (line 530: medians -2.4747 and -1.5067, "
  "difference 0.9680, 'under candidate weights'), which is not in the list. The sentence says the constants are used only in the four "
  "named places, and that is false. Other uses checked and correct: lab (107-383), §3 M (431-437), misconception 2 (488), quiz item 5 (608-609).")
F("L07-L08-r5-used-only-scope", "2.3-grade", "L08.html line 95 ('used only ... in the lab, in the §3 worked M, in misconception 2 and in quiz item 5')",
  "Round 6 read of the whole page: the candidate constants also produce numbers in problem E1 (line 530: medians -2.4747 and -1.5067, "
  "difference 0.9680, 'under candidate weights'), which is not in the list. The sentence says the constants are used only in the four "
  "named places, and that is false. Other uses checked and correct: lab (107-383), §3 M (431-437), misconception 2 (488), quiz item 5 (608-609).",
  "L08.html line 95: add 'in problem E1' to the list, or drop 'only' and say 'in, among others'. Make the card c107 scope consistent.")

P("L07-L08-r2-jstor-statement", "2.1-citation", "course/modules/AC/AC2/L07.html line 104 ('The JSTOR record ... could not be read (bot check)')",
  "Round 6: plain curl to https://www.jstor.org/stable/2672906 returned HTTP 200 (status only). The body was not inspected: a further "
  "check of the response was refused by the sandbox as a bot-check circumvention, so the verifier did not look for or reproduce the "
  "challenge. The claim 'could not be read (bot check)' is therefore not reproduced this round.")
U("L07-L08-r2-jstor-statement", "2.1-citation", "course/modules/AC/AC2/L07.html line 104 ('The JSTOR record ... could not be read (bot check)')",
  "Round 6: plain curl to https://www.jstor.org/stable/2672906 returned HTTP 200 (status only). The body was not inspected: a further "
  "check of the response was refused by the sandbox as a bot-check circumvention, so the verifier did not look for or reproduce the "
  "challenge. The claim 'could not be read (bot check)' is therefore not reproduced this round.",
  "State only what was observed: the HTTP status and date (e.g. 'plain curl returned HTTP 200 on 2026-10-27 with no text extracted'), "
  "or keep the bot-check wording only with a recorded response artefact in the scratch folder.")
U("L07-L08-r6-jstor-challenge", "2.1-citation", "course/modules/AC/AC2/L08.html line 93 ('plain curl returned a JavaScript client challenge')",
  "Round 6: plain curl to https://www.jstor.org/stable/2672906 (the Piotroski record, DOI 10.2307/2672906 per registry) returned HTTP 200. "
  "The body was not inspected (the sandbox refused a further check as bot-check circumvention). The 'JavaScript client challenge' wording "
  "is not reproduced; the Ivey-hosted copy returned HTTP 200 on a HEAD request.",
  "Replace 'plain curl returned a JavaScript client challenge' with the observed status, or record the response body in the scratch folder "
  "and quote its marker. Keep the Ivey-hosted reading claim, which is separately reachable.")

P("L07-L08-loc-access-claims-L08", "2.1-citation", "L08.html line 93 (access sentence)",
  "Round 6 status checks (plain curl, 2026-10-27): doi.org/10.2469/faj.v55.n5.2296 -> HTTP 302 to www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, "
  "which returns 403; ResearchGate and SSRN URLs built by the verifier return 403 (status only; the page gives no URL for either, so "
  "the builder's exact URLs cannot be checked). The Ivey-hosted Piotroski copy returned 200. The page states the Beneish paper was not read, "
  "which is consistent with these statuses.")
P("L07-L08-r3-access", "2.1-citation", "L08.html line 93 access statuses",
  "Round 6: same statuses as L07-L08-loc-access-claims-L08 (doi.org 302 -> tandfonline 403; ResearchGate 403; SSRN 403; Ivey copy 200). "
  "The JSTOR challenge wording is a separate row (L07-L08-r6-jstor-challenge, UNVERIFIABLE).")
P("L07-L08-r6-wiki-recheck", "2.1-citation", "L08.html lines 93, 95, 97; lab docstring 114-118; constants 133-144",
  "Round 6: plain curl to https://en.wikipedia.org/wiki/Beneish_M-score (HTTP 200). Text: 'M-score = −4.84 + 0.92 × DSRI + 0.528 × GMI + "
  "0.404 × AQI + 0.892 × SGI + 0.115 × DEPI −0.172 × SGAI + 4.679 × TATA − 0.327 × LVGI'; 'The threshold value is -1.78 ... (see Beneish 1999, "
  "Beneish, Lee, and Nichols 2013, and Beneish and Vorst 2020)'. The lab constants (lines 134-143) and page values (line 93) equal these. "
  "The page's claims about the source (one secondary page, two other works cited, no page number) match.")
P("L07-L08-r2-wiki-constants", "2.1-citation", "L08.html lines 93, 95, 97; lab docstring lines 114-118; lab constants lines 133-144",
  "Round 6: values and citation text re-read (see L07-L08-r6-wiki-recheck). Lab constants: intercept -4.84; DSRI 0.920, GMI 0.528, AQI 0.404, "
  "SGI 0.892, DEPI 0.115, SGAI -0.172, LVGI -0.327, TATA 4.679 (matches). The labelling UNCONFIRMED appears in the docstring and the output.")
P("L07-L08-r4-wiki-threshold-cite", "2.1-citation", "course/modules/AC/AC2/L08.html line 97",
  "Round 6: L08 line 97 'citing \"Beneish 1999\" by name, with two other works, and no page' matches the Wikipedia text read this round.")
P("L07-L08-beneish-cutoffs", "2.1-citation", "course/modules/AC/AC2/L08.html line 97",
  "Round 6: line 97 states the -1.78 threshold as secondary-source, graded D, and 'the lesson states no cut-off as a rule'; "
  "no cut-off rule appears elsewhere in L08 (grep for 'cut-off', '-1.78'), and card c109 agrees.")
P("L07-L08-loc-beneish-constants-label", "2.1-citation",
  "L08.html lines 56, 60, 93, 95, 97, 106, 439-443, 530, 566; lab docstring 114-118; constants 133-144",
  "Round 6 read of each listed line: each use of the constants carries the UNCONFIRMED label (56, 60, 93, 95, 97, 106, 437, 488, 530 'candidate weights', 566). "
  "Scope list at line 95 is the defect recorded in L07-L08-r5-used-only-scope (not a labelling defect).")
P("L07-L08-beneish-published-wording", "2.3-grade", "L08.html lines 56, 60, 95, 566",
  "Round 6: line 95 'Nothing in this lesson should be read as Beneish's own published number'; line 566 grades the constants C, UNCONFIRMED; "
  "no line presents the constants as Beneish's values.")
P("L07-L08-beneish-tata-disagreement", "2.1-citation", "L08.html R1 solution (line 545)",
  "Round 6: R1 says the intercept and all eight weights come from one secondary page and need checking against the paper. "
  "No number is asserted; the sentence is a directive.")
P("L07-L08-build-report-refs", "2.1-citation", "L08.html line 478 (pointer); L07.html line 344",
  "Round 6: L08 line 478 names 'plans/AC2-open-items.md' and the joint-use study item; open-items row 26 ('Joint use of the F-score and the M-score ... L08 sections 4-5 | OPEN') matches. "
  "The L07 line 344 pointer is in a page that did not change since 11b3477 (carried in substance; the L08 half re-verified).")
P("L07-L08-r3-open-items-content", "2.1-citation", "plans/AC2-open-items.md (rows 16, 19, 26)",
  "Round 6 grep: row 16 Beneish 'open or secondary reproduction of the intercept and eight-variable coefficient table'; row 19 "
  "'Beneish, Lee & Nichols (2013) ... (from recall) | L08 sections 4-5 | OPEN'; row 26 joint use | L08 sections 4-5 | OPEN. Matches the page pointers.")
P("L07-L08-r3-weights-only-source", "2.3-grade", "L08.html line 89 (features) and line 93",
  "Round 6: line 89 says the intercept and eight weights are the source-dependent numbers that cannot yet be confirmed; line 93 says they come from one secondary page. Matches.")
P("L07-L08-r3-used-in-lab-only", "2.3-grade", "L08.html line 95",
  "Round 6: the sentence lists lab, §3 worked M, misconception 2 and quiz item 5 as the only uses. Problem E1 (line 530) also uses the candidate "
  "M medians, so the 'only' list is incomplete. Same defect as L07-L08-r5-used-only-scope.")
F("L07-L08-r3-used-in-lab-only", "2.3-grade", "L08.html line 95",
  "Round 6: the sentence lists lab, §3 worked M, misconception 2 and quiz item 5 as the only uses. Problem E1 (line 530) also uses the candidate "
  "M medians (-2.4747, -1.5067, difference 0.9680), so the 'only' list is incomplete. Same defect as L07-L08-r5-used-only-scope.",
  "As for L07-L08-r5-used-only-scope: add problem E1 to the list (or drop 'only').")
P("L07-L08-r5-E1-label", "2.3-grade", "L08.html E1 solution (line 530)",
  "Round 6: E1 solution gives the candidate-weight medians and says 'the gap is in arithmetic units under candidate weights' and 'the constants are unconfirmed'. "
  "Difference -1.5067 - (-2.4747) = 0.9680 (checked). Label is correct; the scope defect is recorded at line 95.")

P("L07-L08-math-L08-indices", "2.4-math", "L08.html lines 78-85 (eight index list); atlas/A15.contract.md beneish_m_score (lines 145-156)",
  "Round 6: each of the eight formulas on lines 78-85 matches the contract's beneish_m_score definitions line by line (DSRI, GMI, AQI, SGI, DEPI, "
  "SGAI, LVGI, TATA). Seven indices are year-on-year ratios; TATA is not (checked by reading both).")
P("L07-L08-math-prop4.2", "2.4-math", "L08.html Proposition 4.2 and proof (lines 447-452), P1 (line 515)",
  "Round 6: the proof's steps (Bayes, total probability, substitution) give ps/(ps+(1-p)(1-sigma)); P1 derives the same.")
P("L07-L08-math-prop4.3", "2.4-math", "L08.html Proposition 4.3 and proof (lines 458-463), P2 (line 519)",
  "Round 6: AND = f1 f2, OR = 1-(1-f1)(1-f2) under independence; checked against P2.")
P("L07-L08-math-L08-P3", "2.4-math", "L08.html P3 (lines 520-523)",
  "Round 6: AND flag probability <= min(s1, s2) and OR >= max(s1, s2) hold for any joint law (union/intersection bounds); no independence used, as stated.")
P("L07-L08-math-worked-M", "2.2-numbers", "L08.html §3 display (lines 431-437), quiz item 5 explanation (line 609)",
  "Round 6 recomputation (scripts/recompute_l08.py): indices DSRI 1.5000, GMI 1.1429, AQI 1.0833, SGI 1.2000, DEPI 1.0909, SGAI 1.0000, "
  "LVGI 0.9792, TATA 0.0333. M with unrounded indices = -1.559271 -> -1.5593 (the displayed value). With the four-decimal indices M = -1.55943 "
  "-> -1.5594, which is the line-437 statement that the displayed terms sum to -1.5594. Quiz item 5 answer -1.5593 with tolerance 0.0005 holds.")
P("L07-L08-r3-recompute-L08", "2.2-numbers", "L08.html Lab 1 output, §3 worked M, base-rate table, E1-E3, AND/OR",
  "Round 6: lab output re-run (embed_compare: 'expected == stdout True'); worked M recomputed (see L07-L08-math-worked-M); E2 ratio 0.3448/0.0099 = 34.8 (page: 34.8); "
  "E3 1000 x 0.99 x 0.05 = 49.5 (page: 49.50); AND 0.10 x 0.05 = 0.0050 and OR 0.1450 match the lab.")
P("L07-L08-math-base-rate-table", "2.2-numbers", "L08.html lab output (lines 400-409) and base-rate table",
  "Round 6: lab output lines 400-409 equal the twin run (embed_compare True); the table formula is in the lab docstring (PPV = p s/(p s + (1-p)(1-spec))). "
  "Spot check: p=0.01, spec=0.95, s=0.5: 0.005/0.0545 = 0.0917.")
P("L07-L08-math-E2-E3-E1", "2.4-math", "L08.html E1 (lines 530), E2 (534), E3 (536-538)",
  "Round 6: E1 difference 0.9680 (checked); E2 ratio 34.8 and 'about 35' (checked); E3 49.5 and 50 per 1,000 clean (checked).")
P("L07-L08-math-dependence-sign", "2.4-math", "L08.html §4 paragraph (line 466), misconception 3 (line 490), quiz item 10 (line 653)",
  "Round 6: positive correlation raises the AND rate above f1 f2 and lowers the OR rate; the joint law with disjoint flags gives AND 0 and OR 0.1500 (= 0.10 + 0.05), "
  "matching line 466. Misconception 3 and quiz item 10 state the same sign.")
P("L07-L08-math-growth-claim", "2.4-math", "L08.html §5 bullet 'Growth is a confound' (line 476); card AC2-c118",
  "Round 6 recomputation: revenue 1000 to 1500, receivables 100 to 150, SG&A 150 to 225: DSRI = (150/1500)/(100/1000) = 1.0000; SGAI = (225/1500)/(150/1000) = 1.0000; "
  "SGI = 1500/1000 = 1.5000 (matches). c118 agrees.")
P("L07-L08-misconception-score-zero", "2.4-math", "L07.html misconception 1 (line 352) and L08.html line 443; card AC2-c103",
  "Round 6: L07 line 352 ('Signal 1 tests only that ROA is positive ... So a firm with a high ROA that is falling can score low') read; "
  "L08 line 443 signal taxonomy (s1, s2 sign tests at zero; s4 same-year; s3, s5-s9 change tests, conditioned on distress, L07 §3, which is the "
  "'The sample, the conditioning' section) read; c103 example is consistent.")
P("L07-L08-r3-signs-of-improvement", "2.4-math", "L08.html §4 paragraph (line 443)",
  "Round 6: line 443 taxonomy matches L07 line 86 and L07 §3 (heading 'The sample, the conditioning and what the paper reports'; line 340 'conditioned on distress').")
P("L07-L08-r3-margin-overlap", "2.4-math", "L08.html §4 paragraph (line 466)",
  "Round 6: F-score ROA and CFO scaled by beginning-of-year total assets (contract piotroski_f_score line 137); TATA, AQI, LVGI by each year's total assets (contract lines 146-154); "
  "accrual test s4 and TATA both compare NI with cash flow. Matches.")
P("L07-L08-r3-as-much-as", "2.4-math", "L08.html §4 paragraph (lines 466-468)",
  "Round 6: no 'as much as' phrase in L08 (grep); line 468 states the AND rule's sensitivity is at most that of either screen (P3), with no comparative sized beyond that.")
P("L07-L08-r3-prop-4.2-page-locator", "2.4-math", "L08.html lines 54-56 and §3 'Two things' (line 439)",
  "Round 6: lines 54-56 state the Beneish paper's registry locator (pages 24-36, title, DOI key) and the unconfirmed intercept/weights; line 439 'DSRI, at 1.5000' matches the worked M.")
P("L07-L08-r3-R2-track-growth", "2.4-math", "L08.html R2 solution (line 549)",
  "Round 6: R2 answer proposes growth terciles and the independence test of Proposition 4.3; no numeric claim is made.")
P("L07-L08-r3-lab-docstring-follows-beneish", "2.1-citation", "lab-AC2-L08-1 docstring lines 110-112",
  "Round 6: docstring says the index definitions are the contract's (atlas/A15.contract.md, beneish_m_score), and the paper's definitions were not read. Matches §1.")
P("L07-L08-r3-PPV-before-defined", "2.9-structure", "L08.html lab hypothesis (line 106) and table header (line 373); Proposition 4.2 (line 447)",
  "Round 6: PPV is defined in Definition 4.1 (line 101) before the hypothesis (line 106) and the table (line 373); its formula is Proposition 4.2 (line 447), stated as 'below' in line 106.")
P("L07-L08-r2-def41-before-use", "2.9-structure", "L08.html Definition 4.1 (lines 99-102) vs lab hypothesis (line 106) and first use",
  "Round 6: Definition 4.1 precedes its first use (line 106, 'PPV is defined in Definition 4.1 above'). Verified by reading.")
P("L07-L08-r2-lab-L08-table-claim", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 106)",
  "Round 6: the hypothesis's PPV check (0.0917 at prevalence 0.01, specificity 0.95, sensitivity 0.5) is printed as 'True' in the lab output line 398 (run this round).")
P("L07-L08-r2-threshold-row", "2.3-grade", "L08.html key-results row (line 567)",
  "Round 6: row 567 grades the -1.78 threshold D with source 'Not confirmed (§2)'; matches the page text at line 97.")
P("L07-L08-r2-paper-design-claim", "2.1-citation", "L08.html lines 97 and 474",
  "Round 6: line 97 'The paper's classification threshold and sample description are not stated here'; line 474 'The paper's sample design is not confirmed'. Both match the page's unread status.")
P("L07-L08-r2-uncited-assertions", "2.9-structure", "L08.html line 52 (why-it-matters lead)",
  "Round 6: line 52 claims: linear score from eight ratios, seven year-on-year (checked against the index list, lines 78-85); "
  "no uncited numeric claim.")
P("L07-L08-r2-balance-sheet-accrual", "2.4-math", "L08.html line 477 ('Accruals are measured twice' bullet)",
  "Round 6: contract accruals_cash_flow is (net_income - cfo) / average total_assets (atlas lines 111-112); TATA has the same numerator over year-end TA (contract "
  "beneish_m_score line 154). Line 477 states this correctly.")
P("L07-L08-r2-bayes-S1-and-total-probability", "DAG", "L08.html line 455 (Bayesian inference link), Proposition 4.2 proof (line 452)",
  "Round 6: line 455 links 'Bayesian inference' (concept exists in course/concepts.html, one match) and the proof uses Bayes' rule and total probability as stated.")
P("L07-L08-r2-process-words", "2.9-structure", "L07.html, L08.html (case-insensitive)",
  "Round 6: grep for 'builder', 'this build', 'REQUESTS', 'unit report', 'recall', 'Dechow', 'Lee', 'Mohanram': no hits in L07 or L08 learner text. "
  "Note (not a FAIL): L08 line 93 names a tool ('WebFetch') for one access attempt; it is a method note, and the rest of the page says 'plain curl'.")
P("L07-L08-r2-lab-numbering", "2.9-structure", "L08.html lab heading (line 105) and L07.html lab heading",
  "Round 6: L08 lab heading 'Lab 1 · ...' (line 105); no other lab on L08. L07 has its own 'Lab 1' (carried).")
P("L07-L08-r2-links", "2.9-structure", "L08.html internal and concept links",
  "Round 6: check_pages AC2 PASS; anchors exist: L07.html#def-piotroski-f-score (id present in L07), L04.html#def-accruals (present in L04), "
  "concepts.html anchors depreciation-and-amortization, bayesian-inference, robust-statistics (one match each in course/concepts.html).")
P("L07-L08-r2-quiz-keys", "2.4-math", "L08.html quiz (lines 575-655); L07.html quiz (carried)",
  "Round 6 L08 quiz keys checked: item 1 'about 0.09' (0.005/0.0545 = 0.0917); item 2 0.0917 (tolerance 0.0005); item 3 0.0050; item 4 'at most the smaller'; "
  "item 5 -1.5593; item 6 linear combination; item 7 DSRI; item 8 low prevalence; item 9 generated firms; item 10 higher. All keys correct.")
P("L07-L08-r3-from-recall-L08", "2.9-structure", "L08.html (no 'Dechow', 'Lee', or 'recall' in learner text)",
  "Round 6 grep: no 'Dechow', 'Lee' or 'recall' in L08.html (the 'Lee' of the Wikipedia citation is not in the learner text).")
P("L07-L08-r3-eight-year-on-year", "2.9-structure", "L08.html why-it-matters (line 52)",
  "Round 6: line 52 'eight ratios, seven of them year-on-year' matches the index list.")
P("L07-L08-r3-signal-taxonomy-placeholder", "2.9-structure", "L08.html", "placeholder")  # removed below
NEW.pop("L07-L08-r3-signal-taxonomy-placeholder")

P("L07-L08-struct-sections", "2.9-structure", "L08.html section list (§1-§10)",
  "Round 6: sections 1 indices, 2 constants, 3 worked firm, 4 combined rules, 5 canon breaks, 6 misconceptions, 7 problem set, 8 key results, 9 quiz, 10 references; "
  "L07 unchanged (carried).")
P("L07-L08-struct-counts", "2.9-structure", "L08.html (problem set, quiz, misconceptions); L07.html (carried)",
  "Round 6: L08 has 3 misconceptions, problems M1-M3, P1-P3, E1-E3, R1-R3 (12) and 10 quiz items (counted). L07 counts carried.")
P("L07-L08-struct-banned-phrases", "2.9-structure", "L08.html, L07.html (case-insensitive scan)",
  "Round 6 grep for 'roughly half', 'about 6%', 'historically', 'typically', 'U.S.', 'as much as', '...' and '…': none in L08. "
  "L07's two '...' occurrences are Python type hints (tuple[int, ...]) at lines 162 and 249, not omissions.")
P("L07-L08-struct-uses-metadata", "2.9-structure", "L08.html line 38 ('Uses') and L07.html line 38",
  "Round 6: L08 'Uses' lists piotroski-f-score (L07), accruals (L04), depreciation-and-amortization; each is used (TATA/accruals; DEPI; F-score in §4).")
P("L07-L08-dag-check_dag", "DAG", "tools/check_dag.py --all (AC2)",
  "Round 6: check_dag AC2 PASS.")
P("L07-L08-dag-order", "DAG", "L07.html, L08.html uses and concept links",
  "Round 6: L08 uses L07 (F-score, §4) and L04 (accruals, line 477); both precede L08 in the module order.")
P("L07-L08-hours", "2.9-structure", "L07.html data-hours=10; L08.html data-hours=12; index.html data-hours-lessons=76",
  "Round 6: data-hours L01 9, L02 10, L03 8, L04 9, L05 8, L06 10, L07 10, L08 12: sum 76 = index data-hours-lessons=76 (index.html changed only in card text).")
P("L07-L08-grade-L08", "2.3-grade", "L08.html key-results table (lines 562-568)",
  "Round 6: rows 562-568 grade T for the linear definition, PPV, AND/OR, and the sensitivity bounds; C for the unconfirmed constants and the registry row; "
  "D for the threshold. Each T row is a proof on the page; the C and D rows are secondary or unconfirmed.")
P("L07-L08-r3-stock-funded-example", "2.1-citation", "L07.html §2 item 2 (line 94)", "Round 6: carried text unchanged (see carried row).")  # overwritten below
NEW.pop("L07-L08-r3-stock-funded-example")
P("L07-L08-cards-L08-A", "2.7-cards", "cards.json AC2-c106 to AC2-c115 and AC2-c129 (lesson L08)",
  "Round 6 read all eleven entries: c106 (linear combination, screen), c107 (changed: DOI/ResearchGate 403; matches L08 line 93), c108 (registry fields "
  "match references.json), c109 (no cut-off rule; D), c110 (PPV = ps/(ps+(1-p)(1-sigma)), T), c111 (AND/OR, T), c112 (P3, T), c113 (0.0917, C, lab), "
  "c114 (PPVs below 0.1 at prevalence 0.001, C), c115 (probability: no), c129 (prevalence defined as in Definition 4.1). All agree with the page.")
P("L07-L08-cards-L08-B", "2.7-cards", "cards.json AC2-c116, AC2-c117, AC2-c118, AC2-c119",
  "Round 6 read: c116 (AND/OR and correlation), c117 (-2.4747 and -1.5067 match lab output; labelled C), c118 (growth witness recomputed: 1.0, 1.0, 1.5), "
  "c119 (accrual numerator from accruals_cash_flow; average vs year-end total assets, contract lines 111-112 and 154). All agree.")
P("L07-L08-cards-coverage", "2.7-cards", "cards.json (L08 cards) vs Definition 4.1 (lines 99-102)",
  "Round 6: Definition 4.1 terms (false-positive rate, specificity, sensitivity, prevalence, PPV, AND/OR) are each covered by c110-c112, c113, c129 and c116.")
P("L07-L08-cards-dupes", "2.7-cards", "cards.json all 140 AC2 cards (c001-c140)",
  "Round 6 (python -I): 140 entries; ids equal AC2-c001..AC2-c140 exactly; 140 unique ids; no duplicate 'front' text.")
P("L07-L08-rubric-or-project", "2.6-project", "not applicable (no project in this slice)", "Round 6: no project or rubric in L07-L08; N/A.")
P("L07-L08-r2-us-claim", "2.1-citation", "L07.html line 104 and whole page; L08.html", "Round 6 grep: no 'U.S.' in L07 or L08.")
P("L07-L08-r2-jstor-statement-unused", "2.1-citation", "placeholder", "placeholder")
NEW.pop("L07-L08-r2-jstor-statement-unused")

P("L07-L08-r2-process-words-note", "2.9-structure", "placeholder", "placeholder")
NEW.pop("L07-L08-r2-process-words-note")

P("L07-L08-r3-recompute-L07", "2.2-numbers", "L07.html Lab 1 output, §4, M1-M3, E1-E3, P3 (carried)", "placeholder")
NEW.pop("L07-L08-r3-recompute-L07")

P("L07-L08-r6-delta-coverage", "2.9-structure", "git diff 11b3477 HEAD for course/tests/atlas/plans/references/curriculum",
  "Round 6: diff stat: 11 files; for the slice, only L08.html (line 93) and cards.json (c075, c107, c123, c130) touch L07-L08. "
  "c075 and c123 are L05 cards (outside the slice; c123 'expected_t_at_planted' is L05). L07.html, both twins, atlas and references are byte-identical to 11b3477. "
  "Every hunk read.")
P("L07-L08-r6-worked-M-recompute-script", "2.2-numbers", "scripts/recompute_l08.py",
  "Round 6: exact M = -1.559271, four-decimal-index M = -1.55943, all eight indices recomputed from the §3 inputs (1000/1200 etc.) by python -I.")
P("L07-L08-r6-E1-count-recompute", "2.2-numbers", "L07.html E1 (line 396) and Lab 1 output (lines 289-300)",
  "Round 6: twin run output: scores 8: 24, 9: 7 -> 31 of 400 = 0.0775 (page: 31 of 400 = 0.0775).")


P("L07-L08-math-E1-count", "2.2-numbers", "L07.html E1 (line 396) and Lab 1 output (lines 289-300)",
  "Round 6: twin run output: score 8 count 24 and score 9 count 7, total 31 of 400; 31/400 = 0.0775 (page matches). "
  "The page's statement about the paper's high group is not a numeric claim about the paper.")
P("L07-L08-lab-L08-1-overreach", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 106) and main() (lines 334-380)",
  "Round 6 read: hypothesis (line 106) is stated before running and names the footprints the generator plants; interpretation (line 413) says the "
  "medians' separation 'is a property of how the generator was built, so it says nothing about real firms'. No overreach found.")
P("L07-L08-lab-L08-1-run", "2.5-lab", "lab-AC2-L08-1 run and labels (lines 384-412)",
  "Round 6: run output equals the expected block (embed_compare True); labels read SIMULATED (lines 345, 354, 373); the output lines (DSRI 1.7052 etc.) equal the run.")
P("L07-L08-r3-wiki-fetch", "2.1-citation", "Wikipedia 'Beneish M-score' (https://en.wikipedia.org/wiki/Beneish_M-score), plain curl",
  "Round 6: plain curl returned HTTP 200 (scratch wiki.html); the formula, eight variables and -1.78 threshold read as in L07-L08-r6-wiki-recheck.")
P("L07-L08-r3-registry-no-fscore-study", "2.1-citation", "references/references.json (560 entries); L07.html line 344",
  "Round 6: offline integrity 560 entries, 0 problems; a scan of all 560 entries finds one F-score-related record (piotroski2000value). "
  "L07 line 344 ('The registry holds no verified study of the F-score outside the paper's sample') is correct on that scan.")

# ---- carried rows: keep round-5 evidence text with the carry prefix ----
out_rows = []
for rid, r in r5.items():
    if rid in NEW:
        out_rows.append(NEW[rid]); continue
    if rid in CARRIED:
        pref = CARD_CARRY if rid in CARD_CARRIED else CARRY
        row = dict(r)
        row["evidence"] = pref + r["evidence"]
        out_rows.append(row)
        continue
    raise SystemExit("no decision for " + rid)

# every new id must be in r5 or be r6 new
new_only = [k for k in NEW if k not in r5]
for k in new_only:
    out_rows.append(NEW[k])
ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)), "duplicate ids"
frag = {
    "unit": "AC2",
    "slice": "L07-L08",
    "round": 6,
    "verifier": "round-6 independent verifier for slice L07-L08 (did not build AC2; not the round-5 verifier)",
    "pin": "ff9284f",
    "base": None,
    "previous_ledger": "round 5, pin 11b3477: 115 rows, 112 PASS, 3 FAIL (overwritten by this round's fragment)",
    "checkout": "/tmp/verify-ac2r6-l78 (detached worktree at ff9284f; .venv symlinked)",
    "scratch": "/tmp/ac2-v/L07-L08-r6",
    "verified_at": "2026-10-27",
    "verdict": "FAIL",
    "mutants": [],
    "registry_flags": d["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "Round 6 (pin ff9284f). Delta: L08.html line 93 (provenance sentence) and cards.json c107 (Beneish access), c130 (L07 'Eight'), "
        "plus L05 cards c075/c123 outside the slice. L07.html, both twins, atlas and references are unchanged since 11b3477 and their rows are carried "
        "with the required prefix. Every L08 row was re-verified by reading the whole page (673 lines) and by recomputation. "
        "Round-5 FAIL rows: L07-L08-cards-L07-B and L07-L08-r2-constants-provenance now PASS; L07-L08-r5-card-c107-jstor now PASS. "
        "New FAIL: L07-L08-r5-used-only-scope and L07-L08-r3-used-in-lab-only (the line-95 'used only' list omits problem E1). "
        "UNVERIFIABLE: L07-L08-r2-jstor-statement (L07 line 104) and L07-L08-r6-jstor-challenge (L08 line 93): the JSTOR status returned HTTP 200 "
        "and the verifier was refused a further look at the body as a bot-check circumvention; the challenge wording is not reproduced. "
        "Command rows re-run: run_labs 11/11, twins exit 0 with empty stderr, embed compare True, page_smoke PASS, check_pages/dag/projects PASS, "
        "ruff/mypy/pytest PASS, verify_refs live 7/560 and offline 560/560 with 0 problems. Beneish (1999) table and constants: not readable "
        "(DOI 302 then tandfonline 403); the page labels them UNCONFIRMED (ruling 1: not failed). Wikipedia values and threshold reproduced this round. "
        "Not checked: the Ivey PDF content (carried from round 5; HEAD returned 200); Sloan (1996) passage (paper not read; the lesson says so)."
    ),
    "rows": out_rows,
    "summary": None,
}
statuses = [r["status"] for r in out_rows]
frag["summary"] = {
    "rows": len(out_rows),
    "pass": statuses.count("PASS"),
    "fail": statuses.count("FAIL"),
    "unverifiable": statuses.count("UNVERIFIABLE"),
}
frag["verdict"] = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(frag["summary"], "new:", new_only)
