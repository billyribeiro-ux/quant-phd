"""Build the FC1-b round-8 fragment from the round-7 rows, the delta at 4540351d, and this round's runs."""
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyS8-FC1-b")
OLD, NEW = "aa6597255304919b9c4e5e5ca07763ae3e13d45c", "4540351dc664559cdfd371b908f2b4e644cf4297"
R7 = json.load(open("/Users/billyribeiro/.fanout/frags/S-FC1-b.round7.json", encoding="utf-8"))
OUT = "ledgers/FC1/scripts/FC1-b-r8/out"

def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout

def files_unchanged(paths):
    for p in paths:
        if git("diff", "--name-only", OLD, NEW, "--", p).strip():
            raise SystemExit(f"carry refused: {p} changed between pins")

def cards_at(rev):
    return {c["id"]: c for c in json.loads(git("show", f"{rev}:course/modules/FC/FC1/cards.json"))}

OLD_CARDS, NEW_CARDS = cards_at(OLD), cards_at(NEW)
CHANGED_CARDS = sorted(i for i in set(OLD_CARDS) | set(NEW_CARDS) if OLD_CARDS.get(i) != NEW_CARDS.get(i))
assert CHANGED_CARDS == ["FC1-c016", "FC1-c103", "FC1-c105", "FC1-c125", "FC1-c153", "FC1-c174"], CHANGED_CARDS

def carry_ids(ids):
    for i in ids:
        if i in CHANGED_CARDS:
            raise SystemExit(f"carry refused: card {i} changed")
        assert OLD_CARDS[i] == NEW_CARDS[i]

# Carry map: round-7 row id -> (lesson/twin/reference files, card ids). Subjects must be byte-identical.
L04, L05 = "course/modules/FC/FC1/L04.html", "course/modules/FC/FC1/L05.html"
T04, T05 = "tests/labs/FC1/lab-FC1-L04-1.py", "tests/labs/FC1/lab-FC1-L05-1.py"
CARRY = {
    "FC1-b-r1-gate-page-code-equals-twin": ([L04, L05, T04, T05], []),
    "FC1-b-r1-gate-expected-equals-output": ([L04, L05, T04, T05], []),
    "FC1-b-r2-gate-verify-refs-live-unit": (["references/references.json"], []),
    "FC1-b-r1-num-L04-prose": ([L04], []),
    "FC1-b-r1-num-L04-lab-output": ([L04, T04], []),
    "FC1-b-r1-num-L05-prose": ([L05], []),
    "FC1-b-r1-num-L05-lab-output": ([L05, T05], []),
    "FC1-b-r1-lab05-parameter-claims": ([L05], ["FC1-c142"]),
    "FC1-b-r1-lab04-invariant-claim": ([L04, T04], []),
    "FC1-b-r1-math-L04-examples-problems": ([L04], []),
    "FC1-b-r1-math-L05-prop21-prop22": ([L05], []),
    "FC1-b-r1-math-L04-prop22-empty-side": ([L04], []),
    "FC1-b-r1-math-L04-prop23-assumptions": ([L04], ["FC1-c066"]),
    "FC1-b-r1-math-L04-remark-definitions": ([L04, T04], []),
    "FC1-b-r3-proof-P1-hypothesis": ([L04], []),
    "FC1-b-r4-key-result-NP-hypothesis": ([L05], ["FC1-c101"]),
    "FC1-b-r4-key-result-L04-503-hypothesis": ([L04], []),
    "FC1-b-r4-key-result-L05-541-hypothesis": ([L05], []),
    "FC1-b-r4-P1-empty-side-convention": ([L04], []),
    "FC1-b-r1-structure-L04": ([L04], []),
    "FC1-b-r1-structure-L05": ([L05], []),
    "FC1-b-r1-scope-words": ([L04, L05], []),
    "FC1-b-r1-attribution-harris": ([L04, L05, "references/references.json"], []),
    "FC1-b-r1-settlement-source-absence": ([L05], ["FC1-c090"]),
    "FC1-b-r1-references-L05": ([L05, "course/assets/js/refs.js"], []),
    "FC1-b-r1-references-L04-empty-list": ([L04, "course/assets/js/refs.js"], []),
    "FC1-b-r1-card-c066": ([L04], ["FC1-c066"]),
    "FC1-b-r4-card-c099-changed-text": ([L04], ["FC1-c099"]),
    "FC1-b-r2-cards-c154-c156": ([L04], ["FC1-c154", "FC1-c155", "FC1-c156"]),
    "FC1-b-r1-labs-runtime-seed-network": ([T04, T05], []),
    "FC1-b-r1-lab-prose-consistency": ([L04, L05], []),
    "FC1-b-r1-misconceptions-canon": ([L04, L05], []),
    "FC1-b-r1-inline-style": ([L04], []),
    "FC1-b-r2-math-L04-prop22-stop-arrival": ([L04], []),
    "FC1-b-r2-def12-order-entry-offset": ([L05, T05], []),
    "FC1-b-r2-canon-needs-empty-start": ([L04], []),
    "FC1-b-r2-A2-consistency": ([L04, L05], []),
    "FC1-b-r2-terms-before-definition": ([L04, L05], []),
    "FC1-b-r2-cross-reference-style": ([L04, L05], []),
    "FC1-b-r4-L05-why-market-claim": ([L05], []),
    "FC1-b-r4-L04-why-it-matters": ([L04], []),
    "FC1-b-r4-hours": ([L04, L05, "course/modules/FC/FC1/index.html"], []),
    "FC1-b-r3-lesson-links": ([L04, L05], []),
    "FC1-b-r5-delta-L05-hunks": ([L05], []),
    "FC1-b-r5-delta-L04-hunks": ([L04], []),
    "FC1-b-r5-quiz-L04-L05": ([L04, L05], []),
    "FC1-b-r5-lab05-printed-checks": ([T05, L05], []),
    "FC1-b-r6-card-c089-negative-consideration": ([], ["FC1-c089"]),
    "FC1-b-r7-delta-L04-line51": ([L04], []),
    "FC1-b-r7-delta-L05-line100": ([L05], []),
    "FC1-b-r7-delta-cards-c067-c100": ([], ["FC1-c067", "FC1-c100"]),
    "FC1-b-r7-delta-cards-c089": ([], ["FC1-c089"]),
}

NEW_ROWS = {}
def row(rid, check, location, status, evidence, fix=""):
    NEW_ROWS[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}

GATE = "course/modules/FC/FC1"
row("FC1-b-r1-gate-check-pages", "tools/check_pages.py --unit FC1; --page L04; --page L05 (unit gate)",
    f"{GATE}/L04.html, L05.html, cards.json, index.html",
    "PASS", f"Re-run at {NEW[:8]}: {OUT}/check_pages_unit.out 'check_pages FC1: PASS' rc=0; check_pages_L04.out 'check_pages FC1 L04: PASS' rc=0; check_pages_L05.out 'check_pages FC1 L05: PASS' rc=0.")
row("FC1-b-r1-gate-check-dag", "tools/check_dag.py --unit FC1", f"{GATE}/L04.html, L05.html",
    "PASS", f"Re-run: {OUT}/check_dag.out 'check_dag FC1: PASS' rc=0.")
row("FC1-b-r1-gate-run-labs", "tools/run_labs.py --unit FC1", "tests/labs/FC1/lab-FC1-L0[1-5]-1.py",
    "PASS", f"Re-run: {OUT}/run_labs_unit.out 'run_labs FC1: PASS (8/8)' rc=0.")
row("FC1-b-r1-gate-twin-alone", "each lab twin alone: python -I -W error, cwd /tmp", "tests/labs/FC1/lab-FC1-L01-1.py .. L05-1.py",
    "PASS", f"Re-run: {OUT}/twin_L01..L05 .stdout/.stderr; rc=0 for all five, stderr 0 bytes each. L01 twin output lines 'cumulative reserves plus cumulative loans equal total deposits: True' (twin_L01.stdout) back card FC1-c103.")
row("FC1-b-r1-gate-page-smoke", "tools/page_smoke.py --unit FC1 --pages L01 / --pages L04 L05 --skip-sweep (Chromium)",
    f"{GATE}/L01.html, L04.html, L05.html", "PASS",
    f"Re-run: {OUT}/page_smoke_L01.out 'page_smoke FC1: PASS' rc=0; page_smoke_L04_L05.out 'page_smoke modules/FC/FC1/L04.html: PASS', '...L05.html: PASS', 'page_smoke FC1: PASS' rc=0. The figure-control sweep was skipped (--skip-sweep); no figure code changed in the delta.")
row("FC1-b-r1-gate-ruff", "ruff check and ruff format --check on the FC1 twins", "tests/labs/FC1/",
    "PASS", f"Re-run: {OUT}/ruff_check_FC1_labs.out rc=0; ruff_format_FC1_labs.out rc=0.")
row("FC1-b-r1-gate-mypy", "mypy --no-incremental on FC1 twins L01, L04, L05", "tests/labs/FC1/lab-FC1-L01-1.py, L04, L05",
    "PASS", f"Re-run: {OUT}/mypy_FC1_labs.out 'Success: no issues found in 3 source files' rc=0.")
row("FC1-b-r1-gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py",
    "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py", "PASS",
    f"Re-run: {OUT}/pytest_fc1_four.out, rc=0, all dots, no failures. The full suite was not run (the delta touches cards.json only).")
row("FC1-b-r3-gate-build-site-check", "tools/build_site.py --check", "course/assets/data, course/index.html, course/concepts.html",
    "PASS", f"Re-run: {OUT}/build_site_check.out 'site data current: 6 outputs' rc=0. build_site reads no cards.json (grep tools/build_site.py: no 'cards' match).")
row("FC1-b-r1-gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json",
    "PASS", f"Re-run: {OUT}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0.")
row("FC1-b-r4-gate-check-projects-unit", "tools/check_projects.py --unit FC1", f"{GATE}/project.html (unit gate)",
    "PASS", f"Re-run: {OUT}/check_projects_FC1.out 'check_projects FC1: PASS' rc=0. The project slices own the project verdict.")
row("FC1-b-r7-gate-fetch-data-check", "tools/fetch_data.py --check (offline)", "course/assets/data/market/",
    "PASS", f"Re-run: {OUT}/fetch_data_check.out 'fetch_data: 3 datasets, 0 problems' rc=0.")
row("FC1-b-r1-grades", "grade of each graded card matches its ground (T: proved on page; C: basis named), for the cards changed in the delta and the rest",
    f"cards.json FC1-c016, c103, c153 (changed); L01.html lines 89-95, 103-120, 131-140", "PASS",
    "Re-verified this round. FC1-c016 T: Proposition 3.1 (L01.html line 103, proof 110-117) and misconception 2 (line 334). FC1-c103 T: Proposition 2.2 (L01.html line 89, proof line 95). FC1-c153 T: Proposition 3.5 (L01.html line 131, proof 137-139). Each T card's result has a proof on the page. C cards in the file each carry a basis field (check_pages enforces cite or basis for non-T). Removed cards FC1-c125 (C) and FC1-c174 (C) no longer appear. Lesson-side grades in L04/L05 are carried (bytes identical).")
row("FC1-b-r1-notation", "every symbol in the changed cards against notation/notation.json",
    "cards.json FC1-c016, c103, c153 (and the rest); notation/notation.json symbols",
    "PASS", "Re-verified this round: registered symbols are T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} (notation/notation.json 'symbols'). The changed cards use rho, varphi, d, n, S_n, X_t, ell_t and the lesson-local letters only; none is a registered symbol with another meaning. Lesson-side inline math of L04 and L05 is carried (bytes identical).")
row("FC1-b-r1-prose-process-words", "no process words (builder, verifier, round, agent-as-process) in learner text",
    "cards.json (all 170 cards); L04.html, L05.html carried", "PASS",
    "Re-verified this round: case-insensitive scan of cards.json for builder, verifier, round N, we, our, my, TODO, TBD, etc. gives no process-word hit; the only matches are the symbols I and i (inventory, trade index) and the word 'agent' in the dealer definition (FC1-c035, 'An agent that posts a bid...'), which is a model term.")
row("FC1-b-r1-prose-banned-phrases", "banned phrases of BUILDER_RULES 1.3-1.4 absent (TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, obviously, clearly, it can be shown, roughly, historically, ellipsis)",
    "cards.json (all 170 cards)", "PASS",
    "Re-verified this round by regex over every front and back of cards.json: no hit. L04/L05 prose carried.")
row("FC1-b-r1-cards-L04", "every L04 card is atomic, correct against the current L04 text, not trivia; numbers appear in L04",
    "cards.json lesson L04 entries (32)", "PASS",
    "Re-read this round: all 32 L04 cards read in full. All 32 L04 entries are object-identical to the previous pin (none is in CHANGED_CARDS: c016, c103, c105, c125, c153, c174). FC1-c173 is an L04 card; its duplication with FC1-c067 is recorded in FC1-b-r1-cards-duplicates.")
row("FC1-b-r1-cards-L05", "every L05 card is atomic, correct against the current L05 text, not trivia; numbers appear in L05",
    "cards.json lesson L05 entries (34)", "PASS",
    "Re-read this round: all 34 L05 cards read in full; no L05 card changed in the delta (CHANGED_CARDS list). Numbers checked by rerunning T05 (twin_L05.stdout): 2172960, 14282414, 68398886, 2026-10-28 Wednesday and 2026-10-30 Friday, 10117/10060.")
row("FC1-b-r1-cards-duplicates", "no two cards test the same fact (ids unique, fronts unique, no restatement)",
    "cards.json FC1-c173 (line 1103-1109) against FC1-c067 (line 437-441) and L04.html lines 120-122 (Remark 2.4) and 486-489 (Problem R3)",
    "FAIL",
    "Re-verified from scratch: 170 ids unique, 170 fronts unique (python check). The round-7 duplicate FC1-c174 (restating FC1-c103) is removed; FC1-c103 is now the only cumulative-identity card. A pairwise similarity scan (dup_scan.py, out/dup_scan.out) flagged 459 pairs above threshold; the top 60 by similarity were read, and none other than the pair below is a restatement. The top pairs (c058/c121 buy vs sell stop, c132/c133 bid vs ask, c152/c153 bound vs equality) test different facts. Pairs below the top 60 were not read individually. One restatement remains: FC1-c173 'What does a single fill of 60 shares add to the filled sum...? 120' tests the same fact as FC1-c067 'Why does the traded term carry a factor of two? Each fill of q shares adds q to the filled quantity of both ... orders' (Remark 2.4), and its back is the worked answer to Problem R3 (L04.html line 489). Judgement: this is a near-duplicate with a number, not a distinct fact, so it is reported as a PLAUSIBLE LOW finding; the round-7 verifier judged it distinct.",
    "Delete FC1-c173, or merge its numeric check into FC1-c067 (for example, 'a fill of 60 shares: the filled sum is 120') and remove the separate card. Then rerun tools/check_pages.py --unit FC1.")
row("FC1-b-r5-cards-full-scan", "full scan of cards.json for duplicates, lesson-text agreement and trivia",
    "cards.json (170 cards, 1109 lines)", "PASS",
    "Re-done this round: all 170 cards read in full (lines 1-1109). Round 7 had 172; minus FC1-c125 and FC1-c174 (the two removals). The changed cards were checked against the current L01 text (see FC1-b-r8-delta rows). The only non-PASS scan item is FC1-c173 (row FC1-b-r1-cards-duplicates).")
row("FC1-b-r5-delta-cards-hunks", "cards.json hunks of the round-5 delta (c050, c061, c075, c082, c090, c171, c17x) unchanged since the previous pin",
    "cards.json entries of the round-5 hunks", "PASS",
    "Re-verified by object comparison: at aa659725 and at 4540351d, every card id except FC1-c016, c103, c105, c125, c153, c174 is object-identical (script: ledgers/FC1/scripts/FC1-b-r8/build_fragment.py, CHANGED_CARDS assertion). The round-5 hunk entries are therefore unchanged; their content was re-read in the full scan.")
row("FC1-b-r7-delta-cards-c125-c173", "round-7 delta: cards FC1-c125 (removed), FC1-c173 (added in round 7)", "cards.json FC1-c173 (1103-1109); FC1-c125 removal (old line 822-829)",
    "FAIL",
    "c125 removal: correct, the card (C, 'Does each stage of Lab 1, Part B balance?') overlapped FC1-c006 and is gone. c173 arithmetic is correct (2 x 60 = 120, L04 Problem R3 line 489), but c173 restates FC1-c067 (see FC1-b-r1-cards-duplicates). Status FAIL on the c173 point only.",
    "See FC1-b-r1-cards-duplicates: delete or merge FC1-c173.")
row("FC1-b-r7-delta-cards-c174", "round-7 FAIL: FC1-c174 restates FC1-c103 (cumulative identity); removal", "cards.json (c174 absent; c103 at lines 659-663)",
    "PASS",
    "Re-verified: FC1-c174 is absent from cards.json at 4540351d (git diff hunk -1116,8 +1107,0; grep 'FC1-c174' empty). FC1-c103 is the single cumulative-identity card and its back now cites Proposition 2.2 with 'Lab 1, Part B prints True', which matches twin_L01.stdout 'cumulative reserves plus cumulative loans equal total deposits: True'.")
row("FC1-b-r7-twins-unchanged", "tests/labs/FC1 has no diff since the previous pin", "tests/labs/FC1/*.py",
    "PASS", f"git diff --name-only {OLD[:8]} {NEW[:8]} -- tests/labs/FC1 : empty. Twins identical.")
row("FC1-b-r8-delta-cards-c016", "round-8 delta: card FC1-c016 back rewritten (numbers and 'reaches 10 only in the limit' removed)",
    "cards.json line 104-108 (c016 back at line 107); L01.html lines 103-120 (Proposition 3.1), 332-334 (misconception 2)", "PASS",
    "Claim 'at stage n it is (1 - (1-rho)^(n+1))/rho, which is smaller than 1/rho at every finite n when rho < 1' matches Proposition 3.1 (L01.html line 103-107: S_n/d = (1-(1-rho)^(n+1))/rho) and misconception 2 (L01.html line 334: 'For rho < 1 it is smaller than 1/rho at every finite n'). Hypothesis carried: Assumption 2.0 with d > 0 and 0 < rho <= 1 (Proposition 3.1 line 104; A1 line 74). Re-derived (rederive.py, out/rederive.out): strictly below 1/rho for rho<1 and equal at rho=1 for n<60 on a 5-value rho grid: True. Stage 10 value 6.8618940391 (out/rederive.out) matches misconception 2 in L01. The lesson still states both (L01.html line 334), so the card is a subset of the lesson text.")
row("FC1-b-r8-delta-cards-c103", "round-8 delta: card FC1-c103 back now adds 'Lab 1, Part B prints True'",
    "cards.json line 662; L01.html line 89-95 (Proposition 2.2); tests/labs/FC1/lab-FC1-L01-1.py (Part B)", "PASS",
    "Proposition 2.2 (L01.html line 89: 'Assuming Assumption 2.0 ... sum X_t + sum l_t = S_n', proof line 95) supports the T grade and the 'Under Assumption 2.0' hypothesis. Lab 1 Part B prints 'cumulative reserves plus cumulative loans equal total deposits: True' (out/twin_L01.stdout, rc 0, stderr 0 bytes), which agrees with L01.html line 460 ('Parts A and B print True for each exact comparison'). The lab corroboration is named, the grade is not raised. Random check of the identity over 300 (rho, d, n): True (out/rederive.out). No duplicate: FC1-c006 is the per-stage identity; c103 is the cumulative one.")
row("FC1-b-r8-delta-cards-c105", "round-8 delta: card FC1-c105 punctuation only (sentence split)",
    "cards.json line 676; L03.html line 81 (A2)", "PASS",
    "Text matches L03.html line 81 'The dealer has no fees, no interest on cash, no inventory cost and no information. Its cash and its shares are the only two quantities.' The change is a full stop and does not alter content.")
row("FC1-b-r8-delta-cards-c153", "round-8 delta: card FC1-c153 back now carries Proposition 3.5's hypotheses",
    "cards.json line 986; L01.html lines 131-139 (Proposition 3.5 and proof)", "PASS",
    "Proposition 3.5 (L01.html line 131): 'Assuming Assumption 2.0 with d > 0 and with A2 replaced by A2-prime ... Keep A1, with 0 < rho <= 1, and keep the no-withdrawal and no-repayment parts of A3 ... This limit is at most d/rho, with equality if and only if phi = 1 or rho = 1.' The card's hypotheses (A2-prime, d > 0, A1 with 0 < rho <= 1, no-withdrawal and no-repayment parts of A3) match. Proof line 137-139: equality iff (1-rho)(1-phi) = 0. Re-derived on a 12x13 grid of (rho, phi), d=1: equality iff phi=1 or rho=1: True (out/rederive.out). The 'exactly when' wording needs d > 0 (for d=0 both sides are 0), which the card states.")
row("FC1-b-r8-delta-cards-c125-removal", "round-8 delta: card FC1-c125 removed", "cards.json (old lines 822-829 removed; hunk -822,8 +821,0)", "PASS",
    "FC1-c125 is absent at 4540351d. grep -rn 'FC1-c125|FC1-c174' over the repo, excluding ledgers/, .venv and .git, returns no match, so no lesson, test or tool cites either removed card. Its per-stage claim is covered by FC1-c006 and L01 line 460.")
row("FC1-b-r8-delta-numbers-rederived", "numbers in the changed and re-read cards re-derived in exact arithmetic (independent script)",
    "ledgers/FC1/scripts/FC1-b-r8/rederive.py; out/rederive.out", "PASS",
    "Output (rc 0): c010 686189 cents; c011 181818; c092 181790 (half share) and limit 181818; c084 net/gross 0.20881062302681364 -> 0.209; c082/c172 216 x 10060 = 2172960; c083 2026-10-28 is Wednesday, 2026-10-30 Friday; c016 multiplier below 1/rho for rho<1 and equal at rho=1 (n<60) True; c016 stage 10 at rho=1/10: 6.8618940391; c153 equality iff phi=1 or rho=1: True; c103 identity on 300 random cases: True; c050 (k-1)N > kN/2 iff k>2: True; c037 30/5000 = 0.006; c043 2 x 200 = 400; c139 -1000; c140 -600; c061 and c171 159000 and 1060; c152/c153 limit at phi=1/2, rho=1/10 = 1.818 (d=1), d/rho = 10.")
row("FC1-b-r8-delta-L03-lab-numbers", "cards FC1-c052, c053, c054, c097, c098, c170 against the L03 twin output",
    "tests/labs/FC1/lab-FC1-L03-1.py output (out/twin_L03.stdout)", "PASS",
    "twin_L03.stdout: Part A 4000 cents, zero inventory (c052); Part B spread capture 4000 cents, mid-move -545, mark-to-mid 3455, equals spread capture plus mid-move True (c053, c097, c098); Part C 121 pairs, equilibria (100,100),(101,101),(102,102), all symmetric True (c054, c170). Carried-in bytes of these cards are unchanged (CHANGED_CARDS).")
row("FC1-b-r8-delta-L04-lab-numbers", "cards FC1-c061, c062, c069, c169, c171 against the L04 twin output",
    "tests/labs/FC1/lab-FC1-L04-1.py output (out/twin_L04.stdout)", "PASS",
    "twin_L04.stdout: Fixture A fills (1000,60),(1100,90), total 159000 cents, average 1060, 10 shares resting at 1100 (c061, c169, c171); Fixture B sell stop fills at 985 after the market buy (c062); 300-event flow: 'events with a crossed book: 0', 'events where submitted != resting + 2*traded + cancelled: 0' (c069).")
row("FC1-b-r8-delta-L05-lab-numbers", "cards FC1-c082, c083, c084, c085, c086, c088, c172 against the L05 twin output",
    "tests/labs/FC1/lab-FC1-L05-1.py output (out/twin_L05.stdout)", "PASS",
    "twin_L05.stdout: one fill of 216 at 10060 (c082); matching offset 0, settlement offset 2, 2026-10-30 Friday (c083, c085); batch_trades 20, gross 68398886, net 14282414, ratio 0.209 (c084, c086); buy limit 10117 vs trade 10060 (c088); consideration 2172960 (c172). c142's 'offsets_nondecreasing' line is at tests/labs/FC1/lab-FC1-L05-1.py line 240 (carried).")
row("FC1-b-r8-mutants-none", "mutation testing", "FC1-b slice: lessons and cards", "PASS",
    "Not applicable: VERIFIER_RULES 2 and the ruling say mutation testing applies to project graders; this slice has lessons, twins and cards. No mutant was written. Lab twins are demonstrations (ruling).")

rows = []
carried = 0
for r in R7["rows"]:
    rid = r["id"]
    if rid in NEW_ROWS:
        rows.append(NEW_ROWS.pop(rid))
        continue
    if rid in CARRY:
        files, ids = CARRY[rid]
        files_unchanged(files)
        carry_ids(ids)
        carried += 1
        prefix = f"Carried from round 7 ({', '.join(files + ['cards.json entries ' + ', '.join(ids)] if ids else files)} byte-identical since the previous pin {OLD[:8]}):"
        rows.append({**r, "evidence": prefix + " " + r["evidence"], "status": "PASS", "fix": ""})
        continue
    raise SystemExit(f"round-7 row {rid} has no decision")

rows = [r for r in rows] + list(NEW_ROWS.values())
assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"
for r in R7["rows"]:
    assert r["id"] in {x["id"] for x in rows}, f"row id dropped: {r['id']}"

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 8 (did not build FC1; read verifier-rules.md, CLAUDE.md, BUILDER_RULES.md, VERIFIER_RULES.md; round-7 fragment as context only)",
    "pin": NEW,
    "base": f"{OLD} (round-7 pin; round-7 fragment /Users/billyribeiro/.fanout/frags/S-FC1-b.round7.json)",
    "checkout": str(ROOT),
    "scratch": "ledgers/FC1/scripts/FC1-b-r8/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": R7["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Delta since round 7 in the slice (git diff -U0 aa659725 4540351d -- course/modules/FC/FC1/cards.json): hunks at lines 107 (c016), 662 (c103), 676 (c105), removal at old 822-829 (c125), 986 (c153), removal at old 1116-1123 (c174). The brief named only c174 and c103; the other three cards and the c125 removal also changed and are verified here.",
        "No other file in the slice changed: course/modules/FC/FC1 L01-L05, index.html and project.html (except cards.json), tests/labs/FC1, notation/, references/, course/assets/js/, course/assets/data/ are byte-identical between the two pins (git diff --name-only empty).",
        f"Changed card ids, computed by object comparison: {', '.join(CHANGED_CARDS)}. The other 166 cards present at 4540351d are object-identical to the previous pin, so every carried card row cites an unchanged entry.",
        "Carry rule applied: a round-7 PASS row is carried only when every file and card id it cites is identical between the two pins (checked by script in build_fragment.py); carried rows carry the 'Carried from round 7' prefix.",
        "Round-7 non-PASS rows re-verified from scratch: FC1-b-r1-cards-duplicates (now FAIL on c173 only, PLAUSIBLE LOW); FC1-b-r7-delta-cards-c174 (PASS, removed). FC1-b-r7-delta-cards-c125-c173 is FAIL on the c173 point.",
        "Judgement note: FC1-c173 was accepted in round 7 as a distinct question (why versus how much). This round it is reported as a restatement of FC1-c067 (same fact, same mechanism, one number, and the answer to Problem R3). The orchestrator may accept it as distinct, in which case FC1-b-r1-cards-duplicates and FC1-b-r7-delta-cards-c125-c173 become PASS.",
        "Not run: pytest on the full suite (only the four FC1-related files); run_graders and mutate_graders (project slices); check_projects for the other project rows; verify_refs live (carried: references.json unchanged); the figure sweep of page_smoke (--skip-sweep); a browser run of the quiz review-deck insertion (quiz.js addLessonCards), so the runtime use of the changed cards.json is validated only as JSON and by check_pages.",
        "No git commit or push was made. ledger.validate was run on this fragment only; tools/ledger.py merge was not run.",
    ],
    "summary": (f"FC1-b round 8 at {NEW[:8]}: {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
                f"{counts['UNVERIFIABLE']} UNVERIFIABLE; {carried} rows carried from round 7 with byte-identity checks. "
                "Non-PASS: FC1-b-r1-cards-duplicates and FC1-b-r7-delta-cards-c125-c173 (both on FC1-c173, a near-duplicate of FC1-c067; LOW, PLAUSIBLE). "
                "The round-7 FAIL FC1-b-r7-delta-cards-c174 is resolved (card removed)."),
}
out_path = ROOT / "ledgers/FC1/FC1-b.json"
out_path.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(rows), counts, "carried", carried)
