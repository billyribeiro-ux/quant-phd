import json, datetime, copy
SRC = "/tmp/ap1-r5/L05-L06/round4_L05-L06.json.bak"
OUT = "/tmp/verify-ap1-r5-b/ledgers/AP1/L05-L06.json"
r4 = json.load(open(SRC, encoding="utf-8"))
old = {r["id"]: r for r in r4["rows"]}
HTML = "course/modules/AP/AP1/L05.html and L06.html"
CARRY = "Carried from round 4 ({files} byte-identical since 9c8f3e4, re-proved this round by git diff --quiet 9c8f3e4 33fd452): "
def carry(rid, files=HTML, status=None):
    r = copy.deepcopy(old[rid])
    r["evidence"] = CARRY.format(files=files) + r["evidence"]
    if status: r["status"] = status
    return r
def fresh(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS": r["fix"] = fix
    return r

LABS_RUN = ("run this round: `.venv/bin/python tools/run_labs.py --unit AP1 --page L05` -> 'run_labs AP1: PASS (3/3)', exit 0; "
            "`--page L06` -> 'run_labs AP1: PASS (2/2)', exit 0.")
TWIN_RUN = "each twin also run directly this round: `.venv/bin/python -I -W error tests/labs/AP1/<twin>` (Python 3.14.8, numpy 2.4.6, scipy 1.18.0), output below."
PAGE_RUN = "tools/page_smoke.py --unit AP1 --pages L05 L06 (this round, exit 0): 'page_smoke modules/AP/AP1/L05.html: PASS', 'L06.html: PASS', 'page_smoke AP1: PASS'; lab timings 0.0-0.2 s; log /tmp/ap1-r5/L05-L06/smoke.txt."

rows = []
# ---- commands
rows.append(fresh("L05-L06-cmd-pin", "2.9-structure", "repository", "PASS",
  "Pin is 33fd452 (HEAD of /tmp/verify-ap1-r5-b, detached). `git diff --quiet 9c8f3e4 33fd452 -- <file>` exit 0 (byte-identical since round 4) for: course/modules/AP/AP1/L05.html, course/modules/AP/AP1/L06.html, tests/labs/AP1/lab-AP1-L05-1..3.py, lab-AP1-L06-1..2.py, notation/notation.json, course/modules/S/S7, course/modules/AP/AP1/L04.html, tools/run_labs.py, tools/verify_refs.py, tools/refs, tools/ledger.py, tools/katex_strict.js, course/assets/vendor/katex. Files that changed in 9c8f3e4..33fd452 and reach this slice's runtime or registry: course/assets/js/lab.js, data.js, theme.js (page runtime; covered by the re-run page_smoke and run_labs rows); tools/page_smoke.py (covered by its row); references/references.json (AP1 added to used_by of hansen1991implications, see cite row); course/modules/AP/AP1/cards.json (only AP1-c009, lesson L01, changed; see the card rows); curriculum/curriculum.json; L03.html and project.html (outside this slice). Pyodide/KaTeX lock: course/assets/vendor/LOCK.json changed; the vendored KaTeX reports version 0.19.1."))
rows.append(fresh("L05-L06-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AP1 --page L05 / --page L06", "PASS",
  LABS_RUN + " Log: /tmp/ap1-r5/L05-L06/run_labs.txt. " + TWIN_RUN + " (Their printed output is the source for the numbers in the lab rows.)"))
rows.append(fresh("L05-L06-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AP1 --pages L05 L06", "PASS", PAGE_RUN))
rows.append(fresh("L05-L06-cmd-check_pages-dag-projects", "2.9-structure", "tools/check_pages.py, check_dag.py, check_projects.py --unit AP1 (and check_dag --all)", "PASS",
  "Run this round, exit 0 each: 'check_pages AP1: PASS'; 'check_dag AP1: PASS'; check_dag --all 'check_dag S7: PASS', 'check_dag AP1: PASS'; 'check_projects AP1: PASS'. Log: /tmp/ap1-r5/L05-L06/cmds.txt."))
rows.append(fresh("L05-L06-cmd-verify_refs-live", "2.1-citation", "tools/verify_refs.py --unit AP1", "PASS",
  "Run this round (live, network reachable this time): `.venv/bin/python tools/verify_refs.py --unit AP1`, exit 0, final line exactly: 'live re-verification of AP1: 9 of 560 entries, 0 problems'. Scope = the 9 registry keys whose used_by lists AP1 (references/references.json read this round): cochrane2005asset, delbaen1994general, duffie2001dynamic, hansen1991implications, harrison1979martingales, harrison1981martingales, kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone. Round 4's 403 Tunnel errors did not recur. Output: /tmp/ap1-r5/L05-L06/verify_refs_live.txt. Offline: 'offline integrity: 560 entries, 0 problems' (verify_refs --offline, exit 0)."))
rows.append(fresh("L05-L06-cmd-katex-strict-parse", "2.9-structure",
  "every \\( \\) and \\[ \\] in course/modules/AP/AP1/*.html, course/modules/S/S7/*.html, and cards.json (AP1 and S7)", "PASS",
  "Verifier-written strict re-parse this round: /tmp/ap1-r5/L05-L06/parse_all.cjs (text nodes, skipping script/noscript/style/textarea/pre/code/option; every \\( \\) and \\[ \\] rendered with the vendored KaTeX 0.19.1 at course/assets/vendor/katex/katex.min.js, macros from notation/notation.json, throwOnError true, strict 'error', trust false). Result (/tmp/ap1-r5/L05-L06/parse_all.json): AP1 html 2869 expressions, S7 html 5136, AP1+S7 cards 811 (335 cards): 8816 total, 0 errors. Round 4 counted 3075 (AP1 incl. cards) + 5741 (S7) = 8816, the same total; the AP1 split differs by one (3076 by this extractor), not a parse error. Lesson-level parse of L05.html 434, L06.html 372, L05/L06 cards 51: 0 errors (/tmp/ap1-r5/L05-L06/parse_L05_L06.json). Detection control: the same pipeline reports 'Undefined control sequence' when the macro table is wrong (run during this round). `node --test tests/js/katex_strict.test.mjs`: 3 pass, 0 fail (the real vendored KaTeX flags \\Sigmab)."))

# ---- citations
rows.append(carry("L05-L06-cite-hansen1991implications-attribution", "course/modules/AP/AP1/L05.html (lines 145, 361, 506)"))
rows.append(carry("L05-L06-cite-hansen1991implications-grade", "course/modules/AP/AP1/L05.html (lines 145, 361, 506)"))
rows.append(fresh("L05-L06-cite-hansen1991implications-used_by", "2.1-citation", "references/references.json key hansen1991implications", "PASS",
  "references/references.json read this round: hansen1991implications used_by == ['AP1', 'AP3'] (the AP1 entry was added through the registry in 33fd452; hunk at references.json line 11489 of `git diff 9c8f3e4 33fd452`). verified_by crossref, doi 10.1086/261749, volume 99, issue 2, pages 225-262. Live verify_refs --unit AP1 now includes this key and reports 0 problems (row cmd-verify_refs-live)."))
rows.append(carry("L05-L06-cite-harrison1979martingales-Th2", "course/modules/AP/AP1/L06.html (lines 237, 396)"))
rows.append(fresh("L05-L06-cite-harrison1981martingales-Th2.7", "2.1-citation",
  "course/modules/AP/AP1/L06.html line 117, line 238, line 393 (key-results row 2)", "UNVERIFIABLE",
  "Locator still not established from the original. Registry (references.json, read this round): harrison1981martingales doi 10.1016/0304-4149(81)90026-0, volume 11, issue 3, pages 215-260, verified_by crossref. Crossref record (curl https://api.crossref.org/works/10.1016/0304-4149(81)90026-0, HTTP 200, saved /tmp/ap1-r5/L05-L06/https___api_crossref_org_works_10_1016_0304_4149_81_90026_0_.bin): volume '11', issue '3', page '215-260', title 'Martingales and stochastic integrals in the theory of continuous trading', container 'Stochastic Processes and their Applications'. That matches the registry, but Crossref carries no theorem numbers. Attempts to read the article for 'Theorem 2.7' this round: sciencedirect.com/science/article/pii/0304414981900260 (curl HTTP 403, a bot-check page of 1.2 MB with no article text, no 'Theorem' string); the /pdfft variant (403); zbmath.org queries (403); kellogg.northwestern.edu/research/math/papers/454.pdf (404) and www.kellogg.northwestern.edu/... (404). Round 4's Schachermayer survey reading (secondary: prpr0141a.pdf, 'Theorem 1 ([15, Th. 2.7.])') was not repeated and is not a primary source. The disclosure at L06 line 242 remains accurate but does not verify the number.",
  "Read HP81 (SPA 11(3) 215-260, or Kellogg CMS-EMS DP 454) and confirm the printed number and page of the finite-model theorem; set data-locator='Theorem 2.7, p. N' and delete the disclosure sentence. If the original stays unreadable, admit Schachermayer's survey through tools/add_reference.py and cite it alongside (data-cite='<survey key> harrison1981martingales', data-locator='survey Theorem 1, quoting HP81 Th. 2.7')."))
rows.append(fresh("L05-L06-cite-delbaen1994general-Cor1.2", "2.1-citation",
  "course/modules/AP/AP1/L06.html line 239, line 397; misconception 4; quiz item 8; card AP1-c067", "UNVERIFIABLE",
  "Locator still not established from the original. Attempts this round: link.springer.com/article/10.1007/BF01450498 (curl HTTP 200 but a 3038-byte 'Client Challenge' JavaScript page, no article text); link.springer.com/content/pdf/10.1007/BF01450498.pdf (same stub); doi.org/10.1007/BF01450498 (same stub); eudml.org/doc/165264 (metadata only, no text); digizeitschriften GDZPPN00234002X (HTTP 404) and gdz.sub.uni-goettingen.de/id/GDZPPN00234002X (HTTP 404). Crossref record for the DOI (this round, see the issue row) gives title, authors, volume, pages, not theorem numbers. Round 4's survey reading was not repeated.",
  "Read Math. Ann. 300 Corollary 1.2 (Springer or GDZ) and add the printed page: data-locator='Corollary 1.2, p. N', then delete the disclosure sentence. Otherwise admit the survey via tools/add_reference.py and cite it alongside ('survey Theorem 6, quoting DS94 Corr. 1.2')."))
rows.append(carry("L05-L06-cite-survey-unregistered", "course/modules/AP/AP1/L06.html (line 242)"))
rows.append(fresh("L05-L06-cite-delbaen1994general-issue", "2.1-citation", "references/references.json delbaen1994general; rendered reference list on L06", "UNVERIFIABLE",
  "Registry (references.json, read this round): volume '300', issue '1', pages '463-520', doi 10.1007/bf01450498, verified_by crossref. Crossref record fetched this round (curl https://api.crossref.org/works/10.1007/bf01450498, HTTP 200, saved /tmp/ap1-r5/L05-L06/crossref_delbaen.json): volume '300', issue '1', page '463-520', journal-issue {issue: '1', published-print: 1994-09}, container 'Mathematische Annalen', ISSN 0025-5831 / 1432-1807, type journal-article, authors Delbaen, Freddy; Schachermayer, Walter, title 'A general version of the fundamental theorem of asset pricing'. So the registry agrees with the Crossref record. EuDML doc 165264 (fetched this round, https://eudml.org/doc/165264): 'Mathematische Annalen (1994) Volume: 300, Issue: 3, page 463-520', BibTeX '300.3'. The two sources disagree on the issue. The publisher page (Springer, see row cite-delbaen1994general-Cor1.2) is unreachable (JavaScript challenge), so it cannot settle the conflict. Left UNVERIFIABLE; registry is consistent with Crossref.",
  "Resolve issue 1 vs 3 against the Springer issue page (or the printed volume) from a host that can render it. If 3 is confirmed, record the correction through the registry's corrections mechanism (never hand-edit references.json) so the rendered citation reads 300(3); if 1 is confirmed, record that in the evidence and close the row."))
rows.append(carry("L05-L06-cite-cochrane2005asset-3.2", "course/modules/AP/AP1/L06.html (line 75)"))
rows.append(carry("L05-L06-cite-freshness", "course/modules/AP/AP1/L05.html and L06.html (all data-cite keys)"))

# ---- grades
for rid in ["L05-L06-grade-L05-Prop1.2","L05-L06-grade-L05-Thm1.3","L05-L06-grade-L05-Prop2.2","L05-L06-grade-L05-Prop2.3",
            "L05-L06-grade-L05-Thm2.4","L05-L06-grade-L05-Cor2.5","L05-L06-grade-L05-Thm4.1","L05-L06-grade-L06-Thm3.2",
            "L05-L06-grade-L06-Cor3.3","L05-L06-grade-L06-Prop5.1","L05-L06-grade-L05-Thm2.1","L05-L06-grade-L05-Thm3.2",
            "L05-L06-grade-L06-Thm1.2","L05-L06-grade-cochrane-span","L05-L06-grade-HK-span","L05-L06-grade-L06-uncited-claims",
            "L05-L06-grade-L05-misconception4"]:
    rows.append(carry(rid))
rows.append(carry("L05-L06-grade-HP-spans", "course/modules/AP/AP1/L06.html (lines 117, 238, 393)", status="UNVERIFIABLE"))
rows[-1]["evidence"] = old["L05-L06-grade-HP-spans"]["evidence"] + " Round 5: the cited 'Theorem 2.7' is still not established from the original (row cite-harrison1981martingales-Th2.7); the grade is unchanged."
rows[-1]["fix"] = old["L05-L06-grade-HP-spans"]["fix"]
rows[-1]["evidence"] = "Not carried. " + rows[-1]["evidence"]
rows.append(carry("L05-L06-grade-DS-span", "course/modules/AP/AP1/L06.html (lines 239, 397)", status="UNVERIFIABLE"))
rows[-1]["evidence"] = "Not carried. Round 5: 'Corollary 1.2' still not established from the original (row cite-delbaen1994general-Cor1.2). " + old["L05-L06-grade-DS-span"]["evidence"]
rows[-1]["fix"] = old["L05-L06-grade-DS-span"]["fix"]

# ---- numbers (all re-derived this round)
rows.append(fresh("L05-L06-num-L05-misconception2-twice", "2.2-number", "course/modules/AP/AP1/L05.html line 377", "PASS",
  "(a) computed live: lab-AP1-L05-1 prints 'true SDF: mean 0.970000, s.d. 0.422254 >= sigma_min at its mean 0.174605' (run this round). Recomputed: 0.422254 / 0.174605 = 2.41834 -> 'about 2.4' correct (/tmp/ap1-r5/L05-L06/recompute.py)."))
rows.append(fresh("L05-L06-num-L05-E1-annualized", "2.2-number", "course/modules/AP/AP1/L05.html line 452", "FAIL",
  "Inputs: lab-AP1-L04-4 prints 'x*: mean 0.9996, s.d. 0.1410' (rounded). Re-run this round with the lab's own code at full precision (scratch copy, not the repo twin; data from course/assets/data/market/fx_monthly.csv): mean 0.999564503212, s.d. 0.141005868564 (np.std, ddof 0, as the lab uses). Page chain: 0.1410/0.9996 = 0.141056 -> 0.1411, OK. Annualised, page states 0.1411 x sqrt(12) = 0.4888: that is arithmetic on the rounded intermediate (0.1411 x 3.4641016 = 0.488785). From the unrounded values: 0.141006/0.999565 = 0.141067; x sqrt(12) = 0.48867 -> 0.4887 to four decimals. From the displayed inputs without rounding the intermediate: 0.1410/0.9996 x sqrt(12) = 0.48863 -> 0.4886. So 0.4888 is reproduced only by rounding the intermediate; it is not the value of the quantity it names (0.4887). Log: /tmp/ap1-r5/L05-L06/l04_4/exact.py output.",
  "Change '0.1411 x sqrt(12) = 0.4888' to the exact chain: 'sigma_min/mean = 0.141006/0.999565 = 0.14107, times sqrt(12) = 0.4887 annualized' (or drop the fourth decimal: 'about 0.49'). Re-run this row."))
rows.append(fresh("L05-L06-num-L05-Ex3.3", "2.2-number", "course/modules/AP/AP1/L05.html line 227 (Example 3.3)", "PASS",
  "(c) derived on the page; recomputed this round from the L04.html Example 4.2 market (payoffs bond (1,1,1) at 0.96, stock (1.4,1.1,0.6) at 0.976, pi (0.25,0.5,0.25), /tmp/ap1-r5/L05-L06/recompute.py): b = (1.367273, -0.387879), x* = (0.824242, 0.940606, 1.134545), E[x*] = 0.96, E[x*^2] = 0.934012, R* = (0.882475, 1.007060, 1.214701), E[R*] = 1.027824, R_f = 1/0.96 = 1.041667, sigma(x*) = 0.111410, bound sigma/E = 0.116052 (0.1160518), stock mean 1.05/0.976 = 1.075820, stock Sharpe 0.116052 (= bound, as stated). All to the page's six decimals."))
rows.append(fresh("L05-L06-num-L05-Lab1-text", "2.2-number", "course/modules/AP/AP1/L05.html lines 149, 198, 381", "PASS",
  "(a) lab-AP1-L05-1 run this round prints: 'the mean with the smallest bound: v = 0.959009, sigma_min = 0.140481'; 'true SDF: mean 0.970000, s.d. 0.422254 >= sigma_min at its mean 0.174605'; the five-row table has sigma_min(v)/v equal to max Sharpe at R_f=1/v in every row. Twin design (tests/labs/AP1/lab-AP1-L05-1.py): 10 states (line 6), 4 risky payoffs (line 9), mean 0.97 (line 8), 2000 random portfolios (line 24), seed 653. The page's numbers match the printed output."))
rows.append(fresh("L05-L06-num-L05-Lab2-Lab3-text", "2.2-number", "course/modules/AP/AP1/L05.html lines 232, 291, 312, 355, 373, 466", "PASS",
  "(a) lab-AP1-L05-2 and -3 run this round print: E[x*] = 0.980000 = 1/R_f with R_f = 1.020408; E[R*^2] = 1.014480; E[R*] = 0.994190 <= R_f; maximum Sharpe 0.162392; w = -2, 0, +2 with |SR| 0.162392 and s.d. 0.477889, 0.161449, 0.154991; true m sigma/E = 0.208325; x* sigma/E = 0.162392; lab-3's four columns agree. Twins: 8 states, a riskless payoff, 3 risky payoffs, seed 606 (lab-AP1-L05-2.py lines 4-5, 8, 27). Line 466: (0.162392/0.208325)^2 = 0.607640 -> 61%, and 1 - 0.607640 = 0.392360 -> 39%: correct."))
rows.append(fresh("L05-L06-num-L05-M1-M2-M3-R1", "2.2-number", "course/modules/AP/AP1/L05.html lines 400, 407, 414, 477; quiz items 2 and 6 (lines 528, 560)", "PASS",
  "Recomputed this round: M1 (1/1.01)(0.005/0.04) = 0.123762 (page 0.123762, quiz 0.123762 with six decimals); M2 |1 - 1.05 x 0.95|/0.2 = 0.0125 at v = 0.95, zero at v = 1/1.05 = 0.952381 (quiz 0.952381); M3 with the page's displayed inputs: (1.075820 - 1.041667)/(1.027824 - 1.041667) = -2.46725 and from unrounded values -2.467213 -> -2.4672 to four decimals (the page's value is the correctly rounded exact result); R1 0.15/0.02 = 7.5. Script output in /tmp/ap1-r5/L05-L06/recompute.py."))
rows.append(fresh("L05-L06-num-L06-Ex1.3-M1-M3", "2.2-number", "course/modules/AP/AP1/L06.html lines 79, 286, 300; misconception 3 line 267", "PASS",
  "Recomputed this round: Example 1.3 Q = R_f pi x* = (0.214646, 0.489899, 0.295455), sum 1.0000000; density R_f x* = (0.858586, 0.979798, 1.181818); stock check 0.96 x E^Q[x_stock] = 0.976; boundary Q (0.520833, 0, 0.479167) and (0, 0.833333, 0.166667), each pricing (0.96, 0.976). M1 (line 286): R_f = 1/0.97, Q = (0.461856, 0.538144), density (0.769759, 1.345361), P-mean 1.0, m = density/R_f = (0.746667, 1.305). Line 300: (0.25,0.4,0.35) gives stock 1.0 and (0.2,0.5,0.3) gives 1.01, both != 1.016667; midpoint (0.260417, 0.416667, 0.322917) gives 1.016668 (sum 1.000001, rounding). Misconception 3's two non-EMM measures sum to one and give zero mass on one state."))
rows.append(fresh("L05-L06-num-L06-M2-quiz", "2.2-number", "course/modules/AP/AP1/L06.html line 293 (Problem M2), quiz items 3 and 5 (lines 425, 439)", "PASS",
  "Recomputed: q = (1.01 - 0.95)/(1.1 - 0.95) = 0.4; terminal 121, 104.5, 90.25; put payoffs 0, 0, 9.75; value 0.36 x 9.75 / 1.01^2 = 3.440839 (page and quiz 3.440839). Quiz item 3 (q = 0.4) matches."))
rows.append(fresh("L05-L06-num-L06-Lab1-text", "2.2-number", "course/modules/AP/AP1/L06.html lines 131, 181, 247", "PASS",
  "(a) lab-AP1-L06-1 run this round prints: q = 0.400000; dQ/dP on paths [0.444444, 1.0, 1.0, 2.25]; call value 10.457516; q(up) = 1.1667 at 25%; short-stock date-2 gains [12.25, 48.25, 48.25, 75.25]. Recomputed independently: q = 0.4; Q(dd) = 0.36, P(dd) = 0.16 (line 247); call = (0.16 x 44 + 0.48 x 8)/1.02^2 = 10.457516; (1.25 - 0.9)/(1.2 - 0.9) = 1.166667; gains 156.25 - {144, 108, 81} = 12.25, 48.25, 75.25."))
rows.append(fresh("L05-L06-num-L06-Lab2-Prop5.1", "2.2-number", "course/modules/AP/AP1/L06.html lines 194, 206, 229", "PASS",
  "Recomputed exactly for n = 1..14 (win = 1 - 2^-n, mean gain 0, expected deepest loss n/2; asserted in /tmp/ap1-r5/L05-L06/recompute.py): n = 4, 8, 12 give win 0.9375, 0.996094, 0.999756 and deepest 2, 4, 6. 2^12 - 1 = 4095 and 1/4096 'one path in 4,096' correct. Lab-AP1-L06-2 run this round prints the table (sim within Monte Carlo error of exact; mean gains +0.0099, -0.0470, +0.0477)."))
rows.append(fresh("L05-L06-num-L06-E1", "2.2-number", "course/modules/AP/AP1/L06.html line 336 (Problem E1)", "PASS",
  "Recomputed: 100 x 1.02^2 = 104.04 (4.04%); 0.6 x 1.2 + 0.4 x 0.9 = 1.08; 100 x 1.08^2 = 116.64 (16.64%)."))
rows.append(fresh("L05-L06-num-L06-E2", "2.2-number", "course/modules/AP/AP1/L06.html line 343 (Lab 2 mean-gain noise)", "PASS",
  "Recomputed this round: E[G^2] = (1 - 2^-n) + 2^-n (2^n - 1)^2 = 15, 255, 4095 for n = 4, 8, 12; sigma = 3.872983, 15.968719, 63.992187; se over 400,000 paths = 0.006124, 0.025249, 0.101181. Printed mean +0.0099 -> z = +1.62 (page: 1.6); -0.0470 -> z = -1.8615 (page: 1.9); +0.0477 -> z = +0.47 (page: half a standard error). Two-sided p at n = 8: 0.06268, 1/p = 15.95 (page: 'about one run in sixteen (two-sided p = 0.063)'). E[G^2] = 0.999756 + 4094.000244 = 4095 (page)."))
rows.append(fresh("L05-L06-math-L05-Thm2.1", "2.4-math", "L05 lines 87-99; quiz q3 explanation line 539", "PASS",
  "Proof steps (feasibility, orthogonality, minimality) carried in substance from round 4 (L05.html byte-identical since 9c8f3e4). Numeric re-derivation this round (/tmp/ap1-r5/L05-L06/cards_check.py, 200 seeded random markets, S in 4..8 states, N in 1..3 payoffs): the minimum-variance SDF formula m_v = v + (x - mu)' Sigma^-1 (p - v mu) prices every payoff, and its variance equals (p - v mu)' Sigma^-1 (p - v mu) to 2.2e-13 max error. Quiz q3 explanation 'm_v = v + (x - mu)^T b_v' matches. Round 4's 0.893482 came from round 4's own seed and is not re-used."))
rows.append(carry("L05-L06-math-L05-Def1.1-Prop1.2", "course/modules/AP/AP1/L05.html (lines 58-71)"))
rows.append(carry("L05-L06-math-L05-Thm1.3", "course/modules/AP/AP1/L05.html (lines 73-81)"))
rows.append(carry("L05-L06-math-L05-Prop2.2-Prop2.3", "course/modules/AP/AP1/L05.html (lines 103-121)"))
rows.append(carry("L05-L06-math-L05-Thm2.4", "course/modules/AP/AP1/L05.html (lines 123-133)"))
rows.append(carry("L05-L06-math-L05-Cor2.5", "course/modules/AP/AP1/L05.html (lines 135-143)"))
rows.append(carry("L05-L06-math-L05-Thm4.1", "course/modules/AP/AP1/L05.html (lines 296-306)"))
rows.append(carry("L05-L06-math-L05-Def3.1-Thm3.2", "course/modules/AP/AP1/L05.html (lines 205-221)"))
rows.append(carry("L05-L06-math-L05-P1-P2-P3", "course/modules/AP/AP1/L05.html (lines 421-443)"))
rows.append(carry("L05-L06-math-L05-R3-E2-M2", "course/modules/AP/AP1/L05.html (lines 405-408, 457-460, 488-492)"))
rows.append(carry("L05-L06-math-L06-Def1.1-Ex1.3", "course/modules/AP/AP1/L06.html (lines 58-80)"))
rows.append(carry("L05-L06-math-L06-Thm3.2", "course/modules/AP/AP1/L06.html (lines 102-115)"))
rows.append(carry("L05-L06-math-L06-Cor3.3-P1-P3", "course/modules/AP/AP1/L06.html (lines 119-127, 307-327)"))
rows.append(carry("L05-L06-math-L06-P2-Bayes", "course/modules/AP/AP1/L06.html (lines 314-319)"))
rows.append(carry("L05-L06-math-L06-Prop5.1", "course/modules/AP/AP1/L06.html (lines 192-200)"))
rows.append(carry("L05-L06-math-L06-s5-s6-R2-R3-E3", "course/modules/AP/AP1/L06.html (lines 202, 234-242, 350, 371-381)"))
rows.append(carry("L05-L06-math-L05-keyresults-row4", "course/modules/AP/AP1/L05.html (line 506)"))
rows.append(carry("L05-L06-math-L06-Thm1.2", "course/modules/AP/AP1/L06.html (lines 66-73, 392)"))
rows.append(carry("L05-L06-math-L06-s4-deflator", "course/modules/AP/AP1/L06.html (line 186)"))
rows.append(carry("L05-L06-math-L06-R1-minimal-martingale", "course/modules/AP/AP1/L06.html (line 362)"))
rows.append(fresh("L05-L06-math-L06-R1-interval", "2.4-math", "L06 line 366 (Problem R1 solution, last paragraph)", "PASS",
  "Re-derived this round on L04.html Example 5.1 (lines 276-283: pi (0.25, 0.5, 0.25), payoff z = (3, 1, -1), SDF m = (1.2, 0.9, 0.8), price 1.15): E[m z] = 1.15; x* = c z with c = 1.15/E[z^2] = 1.15/3 = 0.383333, so x* = (1.15, 0.383333, -0.383333); Arrow-3 price pi_3 x*_3 = -0.095833. scipy linprog over state prices psi >= 0 with sum psi_s z_s = 1.15: minimum psi_3 = 0 (status 0), so no nonnegative state-price vector prices state 3 below 0; x* does, so the claim 'it can price a payoff outside the interval' is right. Strictly positive EMM or SDF give prices inside the interval (L02 Prop 4.1 / L03 Cor 4.2 cited on page)."))
rows.append(carry("L05-L06-math-L06-R1-minimal-martingale", "course/modules/AP/AP1/L06.html (line 362)") if False else None)
rows = [r for r in rows if r is not None]
# ---- drop the messy carried UNVERIFIABLE stubs (rebuilt below as fresh rows)
rows = [r for r in rows if r["id"] not in ("L05-L06-grade-HP-spans", "L05-L06-grade-DS-span")]
rows.append(fresh("L05-L06-grade-HP-spans", "2.3-grade", "L06 lines 117, 238, 393", "UNVERIFIABLE",
  "Grade T is right for a cited theorem with a precise locator (on-page Theorem 3.2 proof establishes the finite-tree statement). The cited 'Theorem 2.7' of Harrison-Pliska is still not established from the original (row cite-harrison1981martingales-Th2.7), so the T on a cited proof rests on an unverified locator. Not carried: this row depends on a numeric/citation check re-done this round.",
  old["L05-L06-grade-HP-spans"]["fix"]))
rows.append(fresh("L05-L06-grade-DS-span", "2.3-grade", "L06 lines 239, 397", "UNVERIFIABLE",
  "Grade T is right for a cited theorem; 'Corollary 1.2' is still not established from the original (row cite-delbaen1994general-Cor1.2), and this module does not prove the result, so the T rests on that unverified locator.",
  old["L05-L06-grade-DS-span"]["fix"]))

# ---- notation
rows.append(fresh("L05-L06-notation-macros", "2.4-math", "L05, L06 all math; whole unit", "PASS",
  "Re-run this round over the whole AP1 unit and the cards (strict KaTeX parse, row cmd-katex-strict-parse, 0 errors): every backslash command resolves to a KaTeX built-in or a macro registered in notation/notation.json (notation.json byte-identical since 9c8f3e4). Raw-spelling grep for registered macros (\\mathbb{E|P|R}, \\operatorname{Var|Cov|Corr|tr|diag}) over AP1 and S7 html: one hit, course/modules/AP/AP1/index.html line 183 '\\operatorname{diag}(1, 10^{-6})' (same meaning as registered \\diag; index.html not in this slice; advisory, see open_questions 1)."))
rows.append(carry("L05-L06-notation-xstar-S7-collision", "notation/notation.json, course/modules/S/S7 (byte-identical since 9c8f3e4), course/modules/AP/AP1/L05.html, L06.html"))
rows.append(carry("L05-L06-notation-Q-meaning", "notation/notation.json, course/modules/AP/AP1/L06.html"))
rows.append(carry("L05-L06-notation-T-card", "course/modules/AP/AP1/cards.json (entry AP1-c064 identical; the only changed card is AP1-c009)"))
rows.append(carry("L05-L06-notation-Rstar-Restar", "course/modules/AP/AP1/L05.html, cards.json (entries c048, c054 identical)"))
rows.append(carry("L05-L06-notation-Rf", "course/modules/AP/AP1/L05.html, L06.html, notation/notation.json"))
rows.append(carry("L05-L06-notation-local-collisions", "course/modules/AP/AP1/L05.html, L06.html"))
rows.append(carry("L05-L06-notation-xstar-unit", "course/modules/AP/AP1/L05.html, L06.html, L04.html (identical since 9c8f3e4)"))
rows.append(fresh("L05-L06-notation-unit-registry-sweep", "2.4-math", "notation/notation.json vs all AP1 math", "PASS",
  "Recount this round over the AP1 html and AP1 cards (/tmp/ap1-r5/L05-L06/recompute.py-style extraction, verifier-written): R_f 177, R^\\ast 112, \\mathbb Q 104, T (sample size) 89, R^{e\\ast} 46, \\Phi 0, \\gamma_{3,4} 0; 3076 AP1 expressions. These equal round 4's per-symbol counts exactly (R_f 177, R^\\ast 112, Q 104, T 89, R^{e\\ast} 46, Phi 0, gamma 0; round 4 total 3075). The only changes in AP1 since 9c8f3e4 are L03.html (a bullet in the Programs/States text), project.html (the grading-check count) and cards.json AP1-c009 (lesson L01); the counts show no registered symbol was added or removed in the unit."))

# ---- labs (twins run directly this round)
rows.append(fresh("L05-L06-lab-L05-1", "2.5-lab", "lab-AP1-L05-1 / tests/labs/AP1/lab-AP1-L05-1.py", "PASS",
  "run_labs PASS (run this round); twin run directly with `python -I -W error`: prints the 5-row table (sigma_min(v) 0.574181, 0.164195, 0.174605, 0.411455, 0.869880; sigma_min/v equal to the max Sharpe at R_f = 1/v in every row), 'true SDF: mean 0.970000, s.d. 0.422254 >= 0.174605', 'v = 0.959009, sigma_min = 0.140481'. Seeded (default_rng 653), numpy only; page_smoke 0.1 s. SIMULATED labelled. Page code equals twin (run_labs compares them). Interpretation ('below the curve is rejected; above is not thereby confirmed') does not overreach."))
rows.append(fresh("L05-L06-lab-L05-2", "2.5-lab", "lab-AP1-L05-2 / interpretation line 291", "PASS",
  "run_labs PASS; twin run directly: 'R_f = 1.020408, E[x*] = 0.980000 = 1/R_f: True', 'E[R*^2] = 1.014480; 1/E[x*^2] = 1.014480', 'maximum Sharpe ratio of the excess returns: 0.162392', 'w = +2.0: E[R] = 1.045578, s.d. 0.154991 ... |SR| = 0.162392', 'true m: sigma/E = 0.208325'. Interpretation line 291 ('second-moment-minimizing return of Theorem 1.3 ... lower branch') consistent with R* mean 0.994190 < R_f. Seeded (606), numpy only, SIMULATED labelled."))
rows.append(fresh("L05-L06-lab-L05-3", "2.5-lab", "lab-AP1-L05-3 / tests/labs/AP1/lab-AP1-L05-3.py line 4", "PASS",
  "run_labs PASS; twin run directly: asset rows E[R]-R_f = -0.027202, -0.003622, -0.020422 with -R_f Cov(m,R), -R_f Cov(x*,R) and beta_R* (E[R*]-R_f) identical to six decimals; 'E[R*] = 0.994190 < R_f = 1.020408: True'. Twin comment (line 4) reads 'Lab 2's SIMULATED market, rebuilt: 8 states, a riskless payoff and 3 risky payoffs' (seed 606, as lab 2)."))
rows.append(fresh("L05-L06-lab-L06-1", "2.5-lab", "lab-AP1-L06-1", "PASS",
  "run_labs PASS; twin run directly (deterministic, no RNG): 'one-step q(up) = 0.400000', Q of paths [0.16, 0.24, 0.24, 0.36], dQ/dP [0.444444, 1.0, 1.0, 2.25], E_P[dQ/dP] = 1.0, node discounted prices equal E_Q[next] (100, 117.647059, 88.235294), call 10.457516, q(25%) = 1.1667, gains [12.25, 48.25, 48.25, 75.25]. Matches the page (row num-L06-Lab1-text). Interpretation's 'price of the replicating strategy' rests on Corollary 3.3 for this complete tree, not on the lab; acceptable. SIMULATED labelled."))
rows.append(fresh("L05-L06-lab-L06-2", "2.5-lab", "lab-AP1-L06-2", "PASS",
  "run_labs PASS; twin run directly (seed 404, 400,000 paths, horizons 4, 8, 12): sim vs exact P(win) 0.938120/0.937500, 0.995910/0.996094, 0.999768/0.999756; mean gain +0.0099, -0.0470, +0.0477 vs exact 0; E[worst loss] 1.9911, 4.0675, 6.0230 vs exact 2.0, 4.0, 6.0. All within Monte Carlo error (row num-L06-E2 gives the z-scores). Interpretation declines to claim the infinite-horizon exclusion. SIMULATED labelled."))

# ---- figures
rows.append(fresh("L05-L06-fig-none", "2.8-figure", "course/modules/AP/AP1/L05.html, course/modules/AP/AP1/L06.html", "PASS",
  "`ls course/modules/AP/AP1 | grep -i figures` returns nothing (no figures-L05.js / figures-L06.js); no data-figures or data-files attribute to check on L05/L06; labs are SIMULATED and labelled. No dataset licence applies to this slice (the L04 lab 4 FX data belongs to L04, not to this slice)."))

# ---- structure / prose
rows.append(carry("L05-L06-struct-L05-order", "course/modules/AP/AP1/L05.html"))
rows.append(carry("L05-L06-struct-L05-counts", "course/modules/AP/AP1/L05.html"))
rows.append(carry("L05-L06-struct-L06-order", "course/modules/AP/AP1/L06.html"))
rows.append(carry("L05-L06-struct-L06-counts", "course/modules/AP/AP1/L06.html"))
rows.append(fresh("L05-L06-struct-hours", "2.9-structure", "course/modules/AP/AP1/index.html; L01-L07 data-hours; project.html; curriculum.json", "PASS",
  "Re-checked this round: data-hours = 12 on each of L01.html..L07.html (sum 84); index.html data-hours-lessons 84 and data-hours-project 36; project.html data-hours-project 36 (project.html changed since 9c8f3e4 only in the grading-check count, not its hours); 84 + 36 = 120 = curriculum.json AP1 hours 120 (read this round); project share 36/120 = 30%."))
rows.append(fresh("L05-L06-banned-L06-rhetorical-question", "2.9-banned", "L06 line 190", "PASS",
  "L06.html line 190 reads 'The catch is the horizon.' (no question). Scan of both pages' teaching text this round (grep for '?'): the only '?' characters are in problem and quiz prompts and headings (L05 lines 398, 412, 450, 463, 475, 481, 528, 560; L06 lines 297, 298, 334, 340, 341, 377, 426, 431, 440), none in teaching paragraphs."))
rows.append(fresh("L05-L06-banned-scan-other", "2.9-banned", "L05.html, L06.html", "PASS",
  "grep -i -n -E 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|important to note|studies show|experts agree|well known|obviously|clearly' on both pages (run this round): 0 hits."))
rows.append(carry("L05-L06-dag-L05-L06", "course/modules/AP/AP1/L05.html (line 38), L06.html (line 38), curriculum/curriculum.json (AP1 prereqs) ; check_dag --unit AP1 and --all re-run this round: PASS"))
rows.append(carry("L05-L06-quiz-L05", "course/modules/AP/AP1/L05.html (lines 519-591)"))
rows.append(carry("L05-L06-quiz-L06", "course/modules/AP/AP1/L06.html (lines 407-479)"))
rows.append(carry("L05-L06-keyresults-L05-other-rows", "course/modules/AP/AP1/L05.html (lines 503-509)"))
rows.append(carry("L05-L06-keyresults-L06-other-rows", "course/modules/AP/AP1/L06.html (lines 392-397)"))
rows.append(carry("L05-L06-misconceptions-L05-1-3", "course/modules/AP/AP1/L05.html (lines 371-382)"))
rows.append(carry("L05-L06-misconceptions-L06", "course/modules/AP/AP1/L06.html (lines 257-272)"))
rows.append(carry("L05-L06-struct-L06-s6-flow", "course/modules/AP/AP1/L06.html (line 242), L05.html (line 506), L06.html (line 75)"))

# ---- cards (round 4 had no card rows; all 27 lesson L05/L06 cards read this round)
CARDS_NOTE = "All 27 cards of lessons L05 and L06 in course/modules/AP/AP1/cards.json read this round (AP1-c048..c059, c060..c070, c080, c083, c088, c089); cards.json differs from 9c8f3e4 only in AP1-c009 (lesson L01). "
rows.append(fresh("L05-L06-cards-c048-c059", "2.7-cards", "course/modules/AP/AP1/cards.json, cards AP1-c048..c059 (L05, 12 cards)", "PASS",
  CARDS_NOTE + "Checked against the lesson text and numerically: c048 (R* = x*/E[x*^2], second moment 1/E[x*^2]), c049 (m_v formula and variance; 200 random markets, error 2.2e-13), c050 (Prop 2.2), c051 (Thm 2.4), c052 (Cor 2.5), c053 (Hansen-Jagannathan, positivity; cite hansen1991implications is registered and live-verified), c054 (R^e* = (R_f - R*)/R_f, Problem P3), c055 (E[R*] < R_f, 200 random markets with 0 violations), c056 (E[R]-R_f = -R_f Cov(m,R), max error 8.8e-14), c057-c059 (misconceptions, consistent with L05 lines 371-382). Each card atomic; no trivia."))
rows.append(fresh("L05-L06-cards-c060-c070", "2.7-cards", "course/modules/AP/AP1/cards.json, cards AP1-c060..c070 (L06, 11 cards)", "PASS",
  CARDS_NOTE + "Checked against L06 lines 60-127 and 257-272: c060 (EMM definition, Def 1.1), c061 (Theorem 1.2 and its uniqueness claim), c062 (Theorem 3.2; cite harrison1981martingales, whose theorem number is itself UNVERIFIABLE, row cite-harrison1981martingales-Th2.7; the card states no number), c063 (node-by-node construction), c064 (Cor 3.3), c065 (Prop 5.1, 1-2^-n, 0, n/2 re-computed), c066 (admissibility), c067 (DS94 statement; cite delbaen1994general; the statement matches the survey quotation, but attribution to DS94 rests on the UNVERIFIABLE row cite-delbaen1994general-Cor1.2), c068-c070 (misconceptions 1, 3, 4). No card claims a locator."))
rows.append(fresh("L05-L06-cards-c080-c089", "2.7-cards", "course/modules/AP/AP1/cards.json, cards AP1-c080, c083, c088, c089", "PASS",
  CARDS_NOTE + "c080 (Prop 2.3: x* = m_v* with v* = E[x*]; 200 random markets, max error 2.4e-10, numerical tolerance), c083 (Definition 2.1 of a predictable strategy and discounted gain), c088 (misconception 4 of L05: any frontier return prices every return exactly), c089 (doubling: loss 2^n - 1 with probability 2^-n, mean gain 0, checked in recompute.py)."))
rows.append(fresh("L05-L06-cards-duplicates", "2.7-cards", "course/modules/AP/AP1/cards.json (all 92 cards, for duplicates)", "PASS",
  "Full scan this round over all 92 cards in AP1 (L01 16, L02 12, L03 12, L04 13, L05 14, L06 13, L07 12): no duplicate id, no duplicate front (case-insensitive, stripped), no duplicate back."))

# ---- finish
assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"
fails = [r["id"] for r in rows if r["status"] == "FAIL"]
unv = [r["id"] for r in rows if r["status"] == "UNVERIFIABLE"]
passes = [r["id"] for r in rows if r["status"] == "PASS"]
verdict = "PASS" if len(passes) == len(rows) else "FAIL"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
frag = {
 "unit": "AP1", "slice": "L05-L06", "round": 5,
 "verifier": "independent round-5 verifier for slice L05-L06 (did not build AP1; no shared context with its builder or earlier verifiers beyond the round-4 ledger and VERIFIER_RULES.md)",
 "pin": "33fd452", "base": "9c8f3e4",
 "previous_ledger": "round 4 fragment ledgers/AP1/L05-L06.json (pin 9c8f3e4, 98 rows: 91 PASS, 1 FAIL, 6 UNVERIFIABLE; read in full)",
 "checkout": "/tmp/verify-ap1-r5-b, detached at 33fd452 (pin); the only file written is ledgers/AP1/L05-L06.json; the previous verifier's ledgers/AP1/L03-L04.json was not touched",
 "scratch": "/tmp/ap1-r5/L05-L06/",
 "verified_at": now,
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [
  "hansen1991implications: used_by now includes AP1 (fixed in 33fd452; verified this round). Resolved.",
  "delbaen1994general: registry issue '1' matches Crossref (doi 10.1007/bf01450498, issue '1', published-print 1994-09); EuDML doc 165264 says Issue 3. Unresolved: Springer page unreachable; correction only through the corrections mechanism.",
  "harrison1981martingales 'Theorem 2.7' and delbaen1994general 'Corollary 1.2': still not established from the originals this round (sciencedirect 403, Springer JS challenge, GDZ/Kellogg 404, zbMATH 403); the round-4 survey reading is secondary only.",
  "REFERENCE_REQUEST candidate if the originals stay unreadable: Schachermayer, 'The Fundamental Theorem of Asset Pricing' survey, to carry the HP81 and DS94 theorem numbers (identity to be resolved through tools/add_reference.py)."
 ],
 "freshness_flags": ["None required: no working paper is cited on L05 or L06, and AP1 has no debate tag (unchanged since round 4)."],
 "open_questions": [
  "1. Advisory: index.html line 183 writes \\operatorname{diag}(1, 10^{-6}); notation.json registers \\diag with the same meaning; prefer \\diag (index.html is outside this slice).",
  "2. Advisory (carried): L05 line 145 has two consecutive sentences opening 'Theorem 2.1 and Theorem 2.4 ...' that say nearly the same thing; merge them.",
  "3. Advisory (carried): L06 misconception 3 says the boundary measures 'correspond to an arbitrage-boundary price, not to no arbitrage'.",
  "4. Advisory (carried): \\kappa is lesson-local in L01 (cost function) and L06 E3 (strike)."
 ],
 "notes": "Round 5 re-verification at 33fd452. Round-4 non-PASS rows re-checked from scratch: cmd-verify_refs-live now PASS (live run, 9 keys, 0 problems); cite-hansen1991implications-used_by now PASS (registry); cite-harrison1981martingales-Th2.7, cite-delbaen1994general-Cor1.2 and grade-HP-spans, grade-DS-span stay UNVERIFIABLE after the attempts listed; cite-delbaen1994general-issue stays UNVERIFIABLE with the Crossref fields (issue 1, registry-consistent) and EuDML's conflicting issue 3. New FAIL: num-L05-E1-annualized (0.4888 vs exact 0.4887; rounding chain). All commands re-run on the 33fd452 toolchain (run_labs, page_smoke, check_pages, check_dag --unit/--all, check_projects, verify_refs live and offline, node katex test) and a verifier-written strict KaTeX parse over all AP1 and S7 html and cards. Every numeric row re-derived (recompute.py, cards_check.py, lab twins run with -I -W error). Byte-identity proved per subject with git diff --quiet 9c8f3e4 33fd452. Rows carried from round 4 carry the required prefix. Round 4 had no retrieval-card rows for L05-L06 although the slice includes them; this round reads all 27 cards and adds card rows. Mutants: none (no grader in this slice).",
 "summary": {
  "rows": len(rows), "pass": len(passes), "fail": len(fails), "unverifiable": len(unv),
  "mutants": 0, "fail_ids": fails + unv,
  "verdict_rule": "PASS only if every row is PASS; UNVERIFIABLE counts as FAIL."
 }
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows", len(rows), "pass", len(passes), "fail", fails, "unverifiable", unv, "verdict", verdict)
