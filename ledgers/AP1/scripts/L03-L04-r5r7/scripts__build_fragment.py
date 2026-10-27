import json
from pathlib import Path

CK = "/tmp/verify-ap1-r5-b"
SCR = "/tmp/ap1-r5/L03-L04"
rows_old = json.load(open(f"{CK}/ledgers/AP1/L03-L04.json", encoding="utf-8"))["rows"]
old = {r["id"]: r for r in rows_old}

L03_CARRY = ("Carried from round 4 (course/modules/AP/AP1/L03.html changed since 9c8f3e4 only at line 477 "
             "(git diff -U0 9c8f3e4 33fd452: @@ -477 +477 @@), so the row's lines are byte-identical; "
             "round-4 evidence follows):")
L04_CARRY = ("Carried from round 4 (course/modules/AP/AP1/L04.html byte-identical since 9c8f3e4 "
             "(git diff --quiet): round-4 evidence follows):")

RUN_LABS = (f"run_labs: `.venv/bin/python tools/run_labs.py --unit AP1 --page L03` -> 'run_labs AP1: PASS (4/4)' and "
            f"`--page L04` -> 'run_labs AP1: PASS (4/4)' on Python 3.14.8, numpy 2.4.6, scipy 1.18.0; logs in {SCR}/logs/.")

NEW = {}
NEW["L03-L04-cmd-pin"] = dict(check="2.9-structure", location="repository; course/modules/AP/AP1/L03.html, L04.html, cards.json, tests/labs/AP1/*, references/references.json, tools/data_sources.yaml, tools/page_smoke.py",
    status="PASS", evidence=(
    "Pin 33fd452 (detached worktree /tmp/verify-ap1-r5-b). Slice delta since 9c8f3e4: L03.html is one line (`git diff -U0 9c8f3e4 33fd452 -- course/modules/AP/AP1/L03.html` -> `@@ -477 +477 @@`, the R3 'States' bullet); "
    "L04.html byte-identical (git diff --quiet); all 8 slice twins (lab-AP1-L03-1, lab-AP1-L03-2, sol-AP1-L03-E1, sol-AP1-L03-E2, lab-AP1-L04-1..4) byte-identical (git diff --quiet); "
    "cards.json changed only in AP1-c009 (lesson L01) and the 25 L03/L04 cards are equal as JSON objects before and after; references.json changed only in used_by lists (AP1 added to four entries) and generated_at; "
    "tools/data_sources.yaml changed only in the fx_daily/fx_monthly licence note text (licence and licence_url unchanged); tools/page_smoke.py changed (preload parsing), re-run below. Toolchain: Python 3.14.8, numpy 2.4.6, scipy 1.18.0 (`.venv/bin/python -c ...`)."))
NEW["L03-L04-cmd-run_labs"] = dict(check="2.5-lab", location="tools/run_labs.py; tests/labs/AP1/*; L03.html, L04.html", status="PASS", evidence=RUN_LABS + " Every lab's stdout matches the page's expected block under the page rule (run_labs compares against the page).")
NEW["L03-L04-cmd-page_smoke"] = dict(check="2.9-structure", location="tools/page_smoke.py", status="PASS", evidence=(
    f"`.venv/bin/python tools/page_smoke.py --unit AP1 --pages L03 L04` -> rc 0; 'page_smoke modules/AP/AP1/L03.html: PASS', 'page_smoke modules/AP/AP1/L04.html: PASS', 'page_smoke AP1: PASS'. "
    "Runtime boot 1.1 s; preload of numpy and scipy 1.9 s on L03 (0.3 s numpy-only on L04); each lab 0.0 s after preload. Log: " + SCR + "/logs/page_smoke.txt. The script's sweeps (console errors, strict KaTeX re-parse, external requests, 360 px and dark theme) are those in the tool; no page-level failure was printed."))
NEW["L03-L04-cmd-check_pages_dag"] = dict(check="2.9-structure", location="tools/check_pages.py, tools/check_dag.py, curriculum/curriculum.json", status="PASS", evidence=(
    "`.venv/bin/python tools/check_pages.py --unit AP1` -> 'check_pages AP1: PASS'; `.venv/bin/python tools/check_dag.py --unit AP1` -> 'check_dag AP1: PASS' (re-run this round; the DAG closure of AP1's prereqs is unchanged, curriculum.json changed only in the AP1 reading list of part 03)."))
NEW["L03-L04-cmd-lint"] = dict(check="2.5-lab", location="tests/labs/AP1/lab-AP1-L03-*.py, lab-AP1-L04-*.py, sol-AP1-L03-E1.py, sol-AP1-L03-E2.py", status="PASS", evidence=(
    "Re-run this round on the 8 slice twins: `.venv/bin/python -m ruff check` on them -> 'All checks passed!'; `ruff format --check tests/labs/AP1/` -> '22 files already formatted'; `.venv/bin/python -m mypy` on the 8 twins -> 'Success: no issues found in 8 source files'."))
NEW["L03-L04-cmd-verify_refs-offline"] = dict(check="2.1-citation", location="tools/verify_refs.py --offline", status="PASS", evidence=(
    "`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (re-run). `.venv/bin/python tools/fetch_data.py --check` -> 'fetch_data: 3 datasets, 0 problems'."))
NEW["L03-L04-cmd-verify_refs-live"] = dict(check="2.1-citation", location="tools/verify_refs.py --unit AP1", status="PASS", evidence=(
    "Round 4 was UNVERIFIABLE (proxy 403 to openlibrary.org and api.crossref.org). Re-run this round with the proxy working: `.venv/bin/python tools/verify_refs.py --unit AP1`, rc 0, final line exactly 'live re-verification of AP1: 9 of 560 entries, 0 problems' (log " + SCR + "/logs/verify_refs_live.txt). The 9 entries are the AP1 used_by set, which includes the four keys added this round (hansen1991, kalyuga, shleifer, tetzlaff) plus cochrane2005asset, duffie2001dynamic, delbaen1994general, harrison1979martingales, harrison1981martingales."))
NEW["L03-L04-data-fx_monthly"] = dict(check="2.8-figure", location="course/modules/AP/AP1/L04.html Lab 4 data-files=fx_monthly.csv; tools/data_sources.yaml fx_monthly note (changed this round); course/assets/data/market/MANIFEST.json", status="PASS", evidence=(
    "Re-checked because the licence note changed. (a) Snapshot: `git diff --quiet 9c8f3e4 33fd452 -- course/assets/data/market` -> identical; `shasum -a 256 course/assets/data/market/fx_monthly.csv` = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, matching MANIFEST sha256 of the snapshot; `fetch_data.py --check` -> '3 datasets, 0 problems'. "
    "(b) licence_url (MANIFEST and data_sources.yaml) = https://www.federalreserve.gov/disclaimer.htm, fetched this round with curl (saved to " + SCR + "/fx/disclaimer.htm): the text 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' is present, so the MANIFEST quote is on the page and grants redistribution. "
    "(c) The new note's quotes on https://www.federalreserve.gov/releases/h10/about.htm (fetched this round, " + SCR + "/fx/about.htm): 'The data are noon buying rates in New York for cable transfers payable in the listed currencies.' and 'The rates have been certified by the Federal Reserve Bank of New York for customs purposes as required by section 522 of the amended Tariff Act of 1930.' are present verbatim (the old ellipsis is gone and the words are contiguous in the source); 'Last Update: February 06, 2023' is present; the page contains no copyright, terms-of-use or 'public domain' text of its own (grep: none), so the note's statement that about.htm states no terms of its own is true."))
NEW["L03-L04-math-L03-ex2-3"] = dict(check="2.4-math", location="course/modules/AP/AP1/L03.html lines 79-82 (Example 2.3)", status="PASS", evidence=(
    "Recomputed this round (" + SCR + "/scripts/recompute_examples.py; logs/recompute_examples.txt): bond (1,1,1) at 0.96, stock (1.4,1.1,0.6) at 0.976, fund (2.4,2.1,1.6) at 1.95 as the page states; theta=(141,140,-140): payoff (1.0, 1.0, 1.0), today's cash flow 1.0, objective 4.0 = S+1 (S=3); violation (1,1,-1) costs 0.96+0.976-1.95 = -0.014, so 140 copies paying 0.014 today; cost of the trade -1.0. All as printed."))
NEW["L03-L04-math-L03-problems-M"] = dict(check="2.4-math", location="course/modules/AP/AP1/L03.html Problems M1-M3 (lines 301-321)", status="PASS", evidence=(
    "Recomputed this round (recompute_examples.py output): M1 payoff 4(1,1)-(10/3)(1.2,0.9) = (0,1); cost -0.0667 so cash 0.0667; objective 1.0667. M2 segment ends 0.46x0.4=0.184 and 0.16x0.4=0.064; parity 0.976-0.96=0.016; shifted (0.064, 0.184). M3 upper bounds 0.5+0.8+0.46 = 1.76 > 0.96. All match the page."))
NEW["L03-L04-math-L03-E3"] = dict(check="2.4-math", location="course/modules/AP/AP1/L03.html Problem E3 (line 394)", status="PASS", evidence=(
    "Recomputed this round (recompute_examples.py): det of the 3x3 payoff matrix [[1,1.4,0.4],[1,1.1,0.1],[1,0.6,0]] = -0.12 (rank 3); the family psi(t) = (0.5-0.5t, 0.8t, 0.46-0.3t) at t=1/2 gives (0.25, 0.4, 0.31), summing to 0.96 and pricing the stock at 0.976; the put paying (0,0,0.4) is 0.4 x 0.31 = 0.124 = 0.14 - 0.016 (parity). All match the page."))
NEW["L03-L04-math-L03-R2-R3"] = dict(check="2.4-math", location="course/modules/AP/AP1/L03.html Problems R2 (lines 465-470) and R3 'States' bullet (line 477)", status="PASS", evidence=(
    "R2 arithmetic (unchanged, recomputed): 100 x 0.014 = 1.4, fees 3 x 0.05 = 0.15, net 1.25; fees 0.5 per lot give 1.5 > 1.4, so the arbitrage disappears. "
    "R3, the changed bullet, recomputed from scratch with an LP (scripts: " + SCR + "/scripts/r3_lp.py, r3_lp2.py, r3_ray.py, r3_tail.py; logs r3_lp.txt, r3_lp2.txt, r3_ray.txt, r3_tail.txt). "
    "Setup: market prices from a discrete measure mu* with atoms 70,85,97,103,115,125 (weights 0.10,0.20,0.15,0.15,0.20,0.10; bond 0.9, underlying 89.5, calls at K=80,90,100,110,120 priced from mu*), so the market is off-grid. Bounds on E[g] for g = 1{S>=k} and 1{S>k} (k=95, 97.3, 100) over (a) measures on the recipe's node set plus a far atom at M=1e4 (1e6 also tried), (b) the page's own ray-state model (state-price LP, node states plus one ray row = slope; r3_ray.py), and (c) a truth set: measures on a dense grid 0..200 step 0.01 plus the ray atom plus k-1e-6, k, k+1e-6 (r3_tail.py shows the truth is unchanged when the grid is extended to 0..1000 step 0.05 and M changes from 1e4 to 1e6). "
    "Results (lower, upper): k=95, 1{S>=k}: truth (0.410000058, 0.7); page recipe {k-d,k,k+d}: d=0.1 (0.41568, 0.7), d=0.01 (0.41058, 0.7), d=0.001 (0.41006, 0.7), d=1e-5 (0.4100006, 0.7): converges to truth as d->0. "
    "k=95, 1{S>k}: truth (0.41, 0.7); page recipe d=0.1 (0.41, 0.7), d=0.001 (0.41, 0.7): converged. "
    "k=97.3: truth 1{S>=k} (0.345, 0.6326712), 1{S>k} (0.345, 0.6326712); page recipe at d=1e-5 gives (0.345, 0.6326708) and (0.345, 0.6326708), converging with error O(d). "
    "k=100 (a strike): truth (0.345, 0.555) for both conventions; page recipe reaches it. "
    "Narrow recipes (same grid, same markets): {k} alone is too narrow for both conventions (k=95 >=: (0.555, 0.7) vs truth lower 0.410; k=95 >: (0.41, 0.555) vs truth upper 0.7; k=97.3 >=: (0.555, 0.6327) vs truth lower 0.345). {k-d} alone is too narrow on the upper bound (k=95: 0.555 vs 0.7, both conventions); {k+d} alone is too narrow on the lower bound (k=95: 0.555 vs 0.41, both conventions). {k-d,k} is too narrow for 1{S>k} (k=95: upper 0.555 vs 0.7; k=97.3: 0.555 vs 0.6327) and converges for 1{S>=k}. {k,k+d} is too narrow for 1{S>=k} (k=95: lower 0.555) and converges for 1{S>k}. "
    "So the page's statements hold: the three-node recipe at k-d, k, k+d converges for both conventions; with only k, or with one side only, the interval can be far too narrow. The round-4 FAIL (the {k-d,k} recipe for 1{S>k}, upper bound 0.555 vs 0.70) is no longer in the text: the current bullet adds nodes on both sides. The rest of the R3 bullet (kinks, power payoffs) is unchanged and is covered by the carried rows."))
NEW["L03-L04-math-L04-ex4-2"] = dict(check="2.4-math", location="course/modules/AP/AP1/L04.html Example 4.2 (lines 176-180) and Lab 1 hypothesis (line 184)", status="PASS", evidence=(
    "Recomputed this round (recompute_examples.py): pi=(0.25,0.5,0.25), E[xx']=[[1,1.05],[1.05,1.185]], b=(1.367273,-0.387879), x*=(0.824242,0.940606,1.134545), E[x*]=0.96, E[x*^2]=0.934012 (= b'p). pi*x* = (0.206061,0.470303,0.283636) = psi(0.587879) with psi(tau)=(1-tau)(0.5,0,0.46)+tau(0,0.8,0.16). Lab 1 printed values match (run_labs PASS)."))
NEW["L03-L04-math-L04-ex5-1-prop5-2"] = dict(check="2.4-math", location="course/modules/AP/AP1/L04.html lines 270-285 (Example 5.1, Proposition 5.2)", status="PASS", evidence=(
    "Recomputed this round (recompute_examples.py): E[mz]=0.9+0.45-0.2=1.15; E[z^2]=3; c=0.383333; x*=(1.15,0.383333,-0.383333); E[x* e_3]=-0.095833; E[x* z]=1.15 (check). Lab 3 twin (tests/labs/AP1/lab-AP1-L04-3.py) run by run_labs."))
NEW["L03-L04-math-L04-lab3-kkt"] = dict(check="2.4-math", location="course/modules/AP/AP1/L04.html Lab 3 hypothesis (line 289) and lab-AP1-L04-3.py", status="PASS", evidence=(
    "Recomputed this round from the twin's Example 5.1 market (z=(3,1,-1), pi=(0.25,0.5,0.25), price 1.15): floor 0: m=(3 lam, lam, 0) with E[mz]=2.75 lam=1.15, lam=0.418182, m=(1.254545,0.418182,0); E[m^2]=0.25*1.573864+0.5*0.174876=0.480913 (printed 0.4809 by Lab 3). " + RUN_LABS))
NEW["L03-L04-math-L04-problems-M"] = dict(check="2.4-math", location="course/modules/AP/AP1/L04.html Problems M1-M3 (lines 397-417)", status="PASS", evidence=(
    "Recomputed this round (recompute_examples.py): M1 m=(0.746667,1.305), E[m]=0.97, R_f=1.030928, E[mx]=1.00 for x=(1.3,0.8). M2 c=0.54, x*=(1.08,0.54,0), E[x*^2]=0.486. M3 E[x* x_stock]=0.976 and E[x*^2]=0.934012 (= b'p = 0.934012). All match the page."))
NEW["L03-L04-math-L04-E1-E2"] = dict(check="2.4-math", location="course/modules/AP/AP1/L04.html Problems E1 (line 451) and E2 (line 458)", status="PASS", evidence=(
    "Recomputed this round: E1 1.004012/1.133251 = 0.88596 (0.886), eps share 0.11404 (11.4%); E2 1/1.003 = 0.997009. The Lab 2 and Lab 4 numbers come from run_labs (PASS). " + RUN_LABS))
NEW["L03-L04-math-L04-E3"] = dict(check="2.4-math", location="course/modules/AP/AP1/L04.html Problem E3 solution (line 470)", status="PASS", evidence=(
    "Re-derived this round by hand from the page's solution: E[mz_k]=1.35-0.2k; E[z_k^2]=2.75+0.25k^2 > 0; c>0 for 0<k<6.75 gives x* of the sign of z_k (negative in state 3); k=6.75 gives x*=0; k>6.75 gives c<0 and x* negative in states 1 and 2. The page's claim 'negative for every k>0 except k=6.75' is right; k=0 gives x*>=0 (checked)."))
NEW["L03-L04-math-L03-ex4-3"] = dict(check="2.4-math", location="course/modules/AP/AP1/L03.html Example 4.3 (lines 207-210)", status="PASS", evidence=(
    "Recomputed this round (recompute_examples.py): segment ends psi(1)'z = 0.5x0.4 = 0.2 and psi(2)'z = 0.8x0.1 = 0.08; upper portfolio 0.5 stock - 0.3 bonds costs 0.488-0.288 = 0.2 and pays (0.4, 0.25, 0) >= z; lower portfolio 0.2 stock - 0.12 bonds costs 0.1952-0.1152 = 0.08 and pays (0.16, 0.10, 0) <= z. All match the page."))
for lab_id, lab_desc in [("L03-L04-num-L03-lab1", "Lab 1 numbers (0.7783, 0.2078, margins, LP value 6.201973) printed by lab-AP1-L03-1"),
                         ("L03-L04-num-L03-boundary-0.2078", "gap 0.2078 printed by lab-AP1-L03-1"),
                         ("L03-L04-num-L03-E2", "sol-AP1-L03-E2 snippet output (+1.419e-5, 3.987137, -3.7e-8, -3.7e-11, 0) printed"),
                         ("L03-L04-num-L03-lab2-ex", "Lab 2 printed values (0.2000, 0.0800, margins 0, 0.25, 0); M2, M3, E3, R2 recomputed in their rows"),
                         ("L03-L04-num-L03-lab-E1", "sol-AP1-L03-E1 printed values (0.1983, 0.3558, 0.2746, 0.6706, 0.2918, 0.5706, 0.7783)"),
                         ("L03-L04-num-L04-lab1-ex4-2", "Lab 1 printed values (0.587879, 0.934012, 0.9544, 0.206061, 0.470303, 0.283636); Example 4.2 entries recomputed in L03-L04-math-L04-ex4-2"),
                         ("L03-L04-num-L04-lab2-E1", "Lab 2 printed values (1.133251, 1.004012, 0.129239, 0.3926); 0.886 and 11.4% recomputed in L03-L04-math-L04-E1-E2"),
                         ("L03-L04-num-L04-ex5-1-lab3-E3", "Lab 3 printed values (0.440833, 0.925000, 0.4809, 0.5045, 0.6544); Example 5.1 and E3 recomputed"),
                         ("L03-L04-num-L04-M-quiz", "M1, M2 values and quiz answers 0.746667 and 0.486 recomputed in L03-L04-math-L04-problems-M"),
                         ("L03-L04-num-L04-lab4-E2", "Lab 4 printed values (T=332, max abs 8.9e-15, mean 0.9996, s.d. 0.1410, min 0.2078, max 1.5187) on the embedded snapshot; 1/1.003 recomputed")]:
    NEW[lab_id] = dict(check="2.2-number", location=old[lab_id]["location"], status="PASS", evidence=(
        lab_desc + ". " + RUN_LABS + " Hand-derived numbers in this row are recomputed in the rows named above; prose unchanged since 9c8f3e4 except L03 line 477, which has no number."))
NEW["L03-L04-fig-L03-none"] = dict(check="2.8-figure", location="course/modules/AP/AP1/ (no figures-L03.js or figures-L04.js)", status="PASS", evidence="`ls course/modules/AP/AP1/` lists no figures-L03.js or figures-L04.js (re-checked this round); L03 and L04 contain no chart figure, so the figure rules do not apply.")
NEW["L03-L04-banned-scan"] = dict(check="2.9-banned", location="course/modules/AP/AP1/L03.html, L04.html", status="PASS", evidence=(
    "Re-scanned this round (grep -i -E over both pages for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, can be shown, roughly, historically, '...', the ellipsis character, 'about N%'): the only hits are the six quiz stems ending in an ellipsis (L03 lines 537, 546, 569; L04 lines 524, 547, 556), which are unchanged. The new R3 line 477 has none of the strings."))
NEW["L03-L04-card-sample-c025"] = dict(check="2.7-card", location="course/modules/AP/AP1/cards.json AP1-c025 (sample 1 of 25)", status="PASS", evidence="Card back `sup_theta 1^T X theta - p^T theta s.t. 0 <= X theta <= 1, 0 <= -p^T theta <= 1` matches the program on L03.html lines 60-75 (the displayed sup-program with the same two constraint blocks). Atomic and correct.")
NEW["L03-L04-card-sample-c031"] = dict(check="2.7-card", location="course/modules/AP/AP1/cards.json AP1-c031 (sample 2 of 25)", status="PASS", evidence="Card back (0.08, 0.20) with ends psi=(0,0.8,0.16) and (0.5,0,0.46) matches Example 4.3 (L03.html lines 207-210) and the recomputation in L03-L04-math-L03-ex4-3 (0.2 and 0.08).")
NEW["L03-L04-card-sample-c042"] = dict(check="2.7-card", location="course/modules/AP/AP1/cards.json AP1-c042 (sample 3 of 25)", status="PASS", evidence="Card back x* = (1.15, 0.383, -0.383) and 'positive in a complete market' matches Example 5.1 and Proposition 5.2 (L04.html lines 270-285); recomputed in L03-L04-math-L04-ex5-1-prop5-2.")
NEW["L03-L04-card-dup-scan"] = dict(check="2.7-card", location="course/modules/AP/AP1/cards.json (25 cards with lesson L03 or L04)", status="PASS", evidence="Full scan of the 25 L03/L04 cards (AP1-c025..c047, c086, c087): ids unique; fronts unique case-insensitively across all 92 cards in the file; no two backs are identical; the misconception cards (c033, c034, c045, c046, c047, c086, c087) state different misconceptions. No duplicate found.")
NEW["L03-L04-card-identity"] = dict(check="2.7-card", location="course/modules/AP/AP1/cards.json", status="PASS", evidence="Compared the 25 L03/L04 cards as JSON objects at 9c8f3e4 and 33fd452: identical. The only changed card in the file is AP1-c009 (lesson L01), outside this slice.")

# Carried rows (subject spans unchanged). Prefix as required by the verifier rules.
CARRY_L03_IDS = [r["id"] for r in rows_old if r["id"].startswith("L03-L04-")]
out_rows = []
for r in rows_old:
    rid = r["id"]
    if rid in NEW:
        n = NEW[rid]
        out_rows.append(dict(id=rid, check=n["check"], location=n["location"], status=n["status"], evidence=n["evidence"]))
        continue
    loc = r["location"]
    if rid == "L03-L04-cmd-verify_refs-live":
        raise SystemExit("should be overridden")
    if "L04.html" in loc and "L03.html" not in loc:
        prefix = L04_CARRY
    else:
        prefix = L03_CARRY
    status = r["status"]
    assert status == "PASS", (rid, status)
    out_rows.append(dict(id=rid, check=r["check"], location=loc, status="PASS", evidence=prefix + " " + r["evidence"]))

for rid in NEW:
    assert rid in old or rid.startswith("L03-L04-card") or rid.startswith("L03-L04-cmd") or True

for rid, n in NEW.items():
    if rid not in old:
        out_rows.append(dict(id=rid, check=n["check"], location=n["location"], status=n["status"], evidence=n["evidence"]))
ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)), "dup ids"
pass_n = sum(r["status"] == "PASS" for r in out_rows)
fail_n = sum(r["status"] == "FAIL" for r in out_rows)
un_n = sum(r["status"] == "UNVERIFIABLE" for r in out_rows)

frag = {
    "unit": "AP1",
    "slice": "L03-L04",
    "round": 5,
    "verifier": "round-5 independent verifier for slice L03-L04 (did not build AP1; shares no context with the builders or earlier verifiers)",
    "pin": "33fd452",
    "base": "9c8f3e4",
    "previous_ledger": "ledgers/AP1/L03-L04.json as it was at 33fd452 before this overwrite (round 4, pin 9c8f3e4: 78 rows, 76 PASS, 1 FAIL (L03-L04-math-L03-R2-R3), 1 UNVERIFIABLE (L03-L04-cmd-verify_refs-live))",
    "checkout": "/tmp/verify-ap1-r5-b (detached worktree at 33fd452)",
    "scratch": SCR,
    "verified_at": "2026-10-26T00:00:00+00:00",
    "verdict": "PASS" if pass_n == len(out_rows) else "FAIL",
    "rows": out_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Toolchain changed (Python 3.14.8, numpy 2.4.6, scipy 1.18.0, Pyodide 314.0.7 via the vendored runtime): every command row was re-run; every number printed by a lab was re-checked by run_labs (expected-output comparison) on the new toolchain; hand-derived numbers were recomputed in " + SCR + "/scripts/recompute_examples.py.",
        "The only changed page text in this slice is L03.html line 477 (R3 'States' bullet). Rows whose spans lie outside that line are carried with the prefix; the R3 row and the rows that quote R3 were re-verified from scratch.",
        "cochrane2005asset: the live registry check, which was UNVERIFIABLE in round 4, now passes (verify_refs --unit AP1, 0 problems). The publisher-preview locators from round 4 are carried (the cited lines are unchanged).",
        "fx_monthly licence: the new note's quotes were checked against the live about.htm and disclaimer.htm pages (fetched this round), not only against the round-4 notes.",
        "The page's statements about the R3 digital recipe are not in the registry; the LP recomputation is the only evidence for them. The truth set is approximated on a dense grid plus a far atom; the approximation was tested for stability (r3_tail.py).",
        "Mutants: none. The L03/L04 slice has no grader; the AP1 project grader is outside this slice.",
        "Quiz stems with a trailing ellipsis (L03 quiz items 5, 6, 9; L04 quiz items 1, 4, 5) are fill-in prompts; the round-4 judgement (PASS, not omitted content) is carried because their text is unchanged. The verifier notes this as a judgement, not a machine check."
    ],
    "summary": {"rows": len(out_rows), "pass": pass_n, "fail": fail_n, "unverifiable": un_n, "mutants": 0, "fail_ids": [r["id"] for r in out_rows if r["status"] != "PASS"]},
}
Path(f"{CK}/ledgers/AP1/L03-L04.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(out_rows), "pass", pass_n, "fail", fail_n, "unv", un_n, frag["verdict"])
