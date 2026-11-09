import json, sys, datetime
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b/ledgers/FC1/scripts/FC1-b-r9")
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/S-FC1-b.round8.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
OUT = "/tmp/fc1b_r9_rows.json"  # scratch, read by the final writer

CARRY = "Carried from round 8 ({g} byte-identical since the previous pin 4540351d; see out/guards.out): "
L04, L05, L01, L03 = "course/modules/FC/FC1/L04.html", "course/modules/FC/FC1/L05.html", "course/modules/FC/FC1/L01.html", "course/modules/FC/FC1/L03.html"
TW = "tests/labs/FC1"
# decision: id -> ("carry", guard_text, ([files], [cards])) | ("fresh", status, check, location, evidence, fix)
D = {}
def carry(i, files, cards=(), note=""):
    parts = []
    if files: parts.append(", ".join(files))
    if cards: parts.append("cards.json entries " + ", ".join(cards) + " (object-identical)")
    D[i] = ("carry", " and ".join(parts), (list(files), list(cards), note))
def fresh(i, status, check, location, evidence, fix=""):
    D[i] = ("fresh", status, check, location, evidence, fix)

# ---- gates re-run this round
fresh("FC1-b-r1-gate-check-pages", "PASS", "tools/check_pages.py --unit FC1; --page L04; --page L05",
      "course/modules/FC/FC1/L04.html, L05.html, cards.json, index.html",
      "Re-run at 95f3f8cb (cards.json changed): out/check_pages_unit.out 'check_pages FC1: PASS' rc=0; out/check_pages_L04.out 'check_pages FC1 L04: PASS' rc=0; out/check_pages_L05.out 'check_pages FC1 L05: PASS' rc=0.")
fresh("FC1-b-r1-gate-check-dag", "PASS", "tools/check_dag.py --unit FC1", "course/modules/FC/FC1/L04.html, L05.html",
      "Re-run at 95f3f8cb: out/check_dag.out 'check_dag FC1: PASS' rc=0.")
fresh("FC1-b-r1-gate-run-labs", "PASS", "tools/run_labs.py --unit FC1", "tests/labs/FC1/lab-FC1-L0[1-5]-1.py",
      "Re-run at 95f3f8cb: out/run_labs_unit.out 'run_labs FC1: PASS (8/8)' rc=0.")
fresh("FC1-b-r1-gate-twin-alone", "PASS", "each lab twin alone: python -I -W error, cwd /tmp",
      "tests/labs/FC1/lab-FC1-L01-1.py .. L05-1.py",
      "Re-run for L01-L05: each rc=0 with empty stderr (out/twin_L0N.stderr, 0 bytes). L03, L04, L05 stdout byte-identical to the round-8 stdout (cmp against ledgers/FC1/scripts/FC1-b-r8/out/).")
fresh("FC1-b-r1-gate-page-smoke", "PASS", "tools/page_smoke.py --unit FC1 --pages L01 / --pages L04 L05 --skip-sweep (Chromium)",
      "course/modules/FC/FC1/L01.html, L04.html, L05.html",
      "Re-run at 95f3f8cb: out/page_smoke_L04_L05.out 'page_smoke FC1: PASS' rc=0 (L04 and L05 PASS); out/page_smoke_L01.out 'page_smoke FC1: PASS' rc=0. The quiz deck insertion (quiz.js addLessonCards) was not exercised in a browser this round; see notes.")
fresh("FC1-b-r1-gate-ruff", "PASS", "ruff check and ruff format --check on the FC1 twins", "tests/labs/FC1/",
      "Re-run: out/ruff_check_FC1_labs.out 'All checks passed!' rc=0; out/ruff_format_FC1_labs.out '8 files already formatted' rc=0.")
fresh("FC1-b-r1-gate-mypy", "PASS", "mypy --no-incremental on FC1 twins L01, L04, L05", "tests/labs/FC1/lab-FC1-L01-1.py, L04, L05",
      "Re-run: out/mypy_FC1_labs.out 'Success: no issues found in 3 source files' rc=0.")
fresh("FC1-b-r1-gate-pytest-labs", "PASS", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py",
      "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py",
      "Re-run (-q, -p no:cacheprovider): out/pytest_fc1_four.out, all dots, rc=0.")
fresh("FC1-b-r3-gate-build-site-check", "PASS", "tools/build_site.py --check", "course/assets/data, course/index.html, course/concepts.html",
      "Re-run: out/build_site_check.out 'site data current: 6 outputs' rc=0.")
fresh("FC1-b-r1-gate-verify-refs-offline", "PASS", "tools/verify_refs.py --offline", "references/references.json",
      "Re-run: out/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0.")
carry("FC1-b-r2-gate-verify-refs-live-unit", ["references/references.json"],
      note="The live run was not repeated this round; references/ is byte-identical and the row's subject is unchanged.")
fresh("FC1-b-r4-gate-check-projects-unit", "PASS", "tools/check_projects.py --unit FC1", "course/modules/FC/FC1/project.html (unit gate)",
      "Re-run: out/check_projects_FC1.out 'check_projects FC1: PASS' rc=0.")
fresh("FC1-b-r7-gate-fetch-data-check", "PASS", "tools/fetch_data.py --check (offline)", "course/assets/data/market/",
      "Re-run: out/fetch_data_check.out 'fetch_data: 3 datasets, 0 problems' rc=0.")

# ---- carried lesson and twin rows (subject unchanged)
carry("FC1-b-r1-gate-page-code-equals-twin", [L04, L05, TW], note="")
carry("FC1-b-r1-gate-expected-equals-output", [L04, L05, TW], note="Twin stdout re-run this round is byte-identical to the round-8 stdout.")
carry("FC1-b-r1-num-L04-prose", [L04])
carry("FC1-b-r1-num-L04-lab-output", [L04, TW])
carry("FC1-b-r1-num-L05-prose", [L05])
carry("FC1-b-r1-num-L05-lab-output", [L05, TW])
carry("FC1-b-r1-lab05-parameter-claims", [L05], ["FC1-c142"])
carry("FC1-b-r1-lab04-invariant-claim", [L04, TW])
carry("FC1-b-r1-math-L04-examples-problems", [L04])
carry("FC1-b-r1-math-L05-prop21-prop22", [L05])
carry("FC1-b-r1-math-L04-prop22-empty-side", [L04])
carry("FC1-b-r1-math-L04-prop23-assumptions", [L04], ["FC1-c066"])
carry("FC1-b-r1-math-L04-remark-definitions", [L04])
carry("FC1-b-r3-proof-P1-hypothesis", [L04])
carry("FC1-b-r4-key-result-NP-hypothesis", [L05], ["FC1-c101"])
carry("FC1-b-r4-key-result-L04-503-hypothesis", [L04])
carry("FC1-b-r4-key-result-L05-541-hypothesis", [L05])
carry("FC1-b-r4-P1-empty-side-convention", [L04])
carry("FC1-b-r1-structure-L04", [L04])
carry("FC1-b-r1-structure-L05", [L05])
carry("FC1-b-r1-scope-words", [L04, L05])
carry("FC1-b-r1-attribution-harris", [L04, L05, "references/references.json", "curriculum/02-economics-finance-core.yaml"])
carry("FC1-b-r1-settlement-source-absence", [L05, "references/references.json"], ["FC1-c090"])
carry("FC1-b-r1-references-L05", [L05, "course/assets/js/refs.js"])
carry("FC1-b-r1-references-L04-empty-list", [L04, "course/assets/js/refs.js"])
carry("FC1-b-r1-card-c066", [], ["FC1-c066"])
carry("FC1-b-r4-card-c099-changed-text", [L04], ["FC1-c099"])
carry("FC1-b-r2-cards-c154-c156", [L04], ["FC1-c154", "FC1-c155", "FC1-c156"])
carry("FC1-b-r1-labs-runtime-seed-network", [TW])
carry("FC1-b-r1-lab-prose-consistency", [L04, L05, TW])
carry("FC1-b-r1-misconceptions-canon", [L04, L05])
carry("FC1-b-r1-inline-style", [L04])
carry("FC1-b-r2-math-L04-prop22-stop-arrival", [L04])
carry("FC1-b-r2-def12-order-entry-offset", [L05, TW])
carry("FC1-b-r2-canon-needs-empty-start", [L04])
carry("FC1-b-r2-A2-consistency", [L04, L05])
carry("FC1-b-r2-terms-before-definition", [L04, L05])
carry("FC1-b-r2-cross-reference-style", [L04, L05])
carry("FC1-b-r4-L05-why-market-claim", [L05])
carry("FC1-b-r4-L04-why-it-matters", [L04])
carry("FC1-b-r4-hours", ["course/modules/FC/FC1/index.html", L04, L05])
carry("FC1-b-r3-lesson-links", [L04, L05])
carry("FC1-b-r5-delta-L05-hunks", [L05])
carry("FC1-b-r5-delta-L04-hunks", [L04])
carry("FC1-b-r5-delta-cards-hunks", [], ["FC1-c050", "FC1-c061", "FC1-c075", "FC1-c082", "FC1-c090", "FC1-c171", "FC1-c172"])
carry("FC1-b-r5-quiz-L04-L05", [L04, L05])
carry("FC1-b-r5-lab05-printed-checks", [L05, TW])
carry("FC1-b-r6-card-c089-negative-consideration", [], ["FC1-c089"])
carry("FC1-b-r7-delta-L04-line51", [L04])
carry("FC1-b-r7-delta-L05-line100", [L05])
carry("FC1-b-r7-delta-cards-c067-c100", [], ["FC1-c067", "FC1-c100"])
carry("FC1-b-r7-delta-cards-c089", [], ["FC1-c089"])
carry("FC1-b-r8-delta-cards-c016", [], ["FC1-c016"])
carry("FC1-b-r8-delta-cards-c103", [], ["FC1-c103"])
carry("FC1-b-r8-delta-cards-c105", [], ["FC1-c105"])
carry("FC1-b-r8-delta-cards-c153", [], ["FC1-c153"])
carry("FC1-b-r8-delta-numbers-rederived", [], ["FC1-c016", "FC1-c103", "FC1-c105", "FC1-c153"])
carry("FC1-b-r8-delta-L03-lab-numbers", [L03, TW], ["FC1-c052", "FC1-c053", "FC1-c054", "FC1-c097", "FC1-c098", "FC1-c170"])

# ---- the rows whose subject is cards.json or changed this round
fresh("FC1-b-r1-cards-L04", "FAIL", "every L04 card is atomic, correct against the current L04 text, not trivia; numbers appear in L04",
      "course/modules/FC/FC1/cards.json FC1-c056 (back)",
      "Re-verified all 31 L04 cards (out/cards_numbers_and_phrases.out, out/cards_L04_L05_numbers.out: no number missing from L04.html or the twin output). Every other L04 card was checked against L04.html text and matches (Definition 1.1 L04.html line 59; Remark 1.2 line 67; Definition 2.1 line 84; Proposition 2.2 line 99; Proposition 2.3 line 109; Example 1.3 line 72; Example 1.4 line 77; Problem R2 line 482; Problem R3 line 489). FC1-c056 back reads 'A market order trades at the best prices available on the opposite side at arrival, taking resting orders in price-time priority ... (Definition 1.1).' Definition 1.1 (line 59) says only 'the best prices available on the opposite side now, best price first'. The time rule 'earliest arrival first' and the term 'price-time priority' are defined in Definition 2.1 (line 84, <dfn>price-time priority</dfn>). The claim is correct, but the locator Definition 1.1 does not contain the clause it is cited for.",
      "In cards.json FC1-c056 back, cite '(Definition 1.1; the priority rule is Definition 2.1)', or replace 'taking resting orders in price-time priority' with 'taking resting orders best price first (Definition 1.1)'. Then re-run check_pages --unit FC1 and the closing delta for FC1-c056.")
fresh("FC1-b-r1-cards-L05", "PASS", "every L05 card is atomic, correct against the current L05 text, not trivia; numbers appear in L05",
      "course/modules/FC/FC1/cards.json lesson L05 entries (34)",
      "Re-verified all 34 L05 cards this round against L05.html text (Definition 1.1 line 58; Definition 1.2 line 63; Remark 1.3 line 70; Section 2 line 75; Proposition 2.1 lines 79-85; Proposition 2.2 lines 90-95; Remark 2.3 line 100; Lab 1 lines 105-109, 390; misconceptions lines 410-423; Problem R2 lines 518-520; Section 4 line 397; Section 2 net-to-gross ratio NP/G at line 75) and the twin output (out/twin_L05.stdout). Numbers 216, 10060, 2172960, 14282414, 68398886, 0.209, 0.20881062 (= 14282414/68398886, computed), 10117, 2026-10-30 match. No card missing from L05.html; numbers check: out/cards_L04_L05_numbers.out.")
fresh("FC1-b-r1-grades", "PASS", "grade of each graded card matches its ground (T: proved on page; C: basis named), for the cards changed in the delta and the rest",
      "cards.json (42 T, 22 C); L01.html lines 89-95, 103-120, 131-140",
      "Subject is cards.json, changed by one deletion (FC1-c173, a T card). Guard out/guards.out: every remaining entry object-identical to 4540351d. Re-verified this round, from scratch: all 31 L04 and 34 L05 graded or ungraded entries that are T/C: T cards FC1-c061, c062, c066, c068, c099, c100, c169, c171 (L04) and c079, c080, c089, c101, c102 (L05) against their lesson statements (lines cited in the cards-L04 and cards-L05 rows); C cards FC1-c069 (L04) and c082-c086, c088, c172 (L05) against the twin output (out/twin_L04.stdout, out/twin_L05.stdout). Every C card has a basis; every basis-bearing card is C (out/cards_delta_identity.out: 'C without basis: []', 'basis on non-C: []'). T and C grades for L01-L03 entries are carried by entry identity (guard above) from round 8, where they were verified against L01-L03 text.")
fresh("FC1-b-r1-notation", "PASS", "every symbol in the changed cards against notation/notation.json",
      "cards.json (all 169 entries); notation/notation.json symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) and macros",
      "Scripted scan (out/cards_numbers_and_phrases.out and the grep in the transcript): no registered macro (\\E, \\Prob, \\R, ...) and no registered symbol (\\Phi, \\gamma, R^\\ast, R_f, \\mathbb{Q}) occurs in FC1 cards or lessons. Plain 'T' occurs only as the grade label (L04.html line 590 'T.'; L03.html line 564). Local letters G, R, X, C, V, W, I, P, q, p, c, x_j, NP are defined in their lessons (e.g. L04.html line 109 defines G, R, X, C; L05.html line 75 defines q_i, p_i, c_i, Rec_j, Pay_j, x_j, G, NP) and are not registered program-wide.")
fresh("FC1-b-r1-prose-process-words", "PASS", "no process words (builder, verifier, round, agent-as-process) in learner text",
      "cards.json (all 169 entries); L04.html, L05.html carried",
      "Scripted scan of all 169 entries for builder, verifier, round, agent, orchestrat, fixer, pass, ledger, delta (out/cards_numbers_and_phrases.out). Hits: 'round' inside 'rounded' (FC1-c010, c011, c012, c084) and 'agent' as the term of art 'An agent that posts a bid' (FC1-c035, a dealer definition, L03). No process word is used as learner text.")
fresh("FC1-b-r1-prose-banned-phrases", "PASS", "banned phrases of BUILDER_RULES 1.3-1.4 absent (TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, obviously, clearly, it can be shown, roughly, historically, ellipsis)",
      "cards.json (all 169 entries)",
      "Scripted case-insensitive scan of all 169 entries for TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, obviously, clearly, it can be shown, roughly, historically, '...', '…': no hit (out/cards_numbers_and_phrases.out prints 'BANNED' for any hit; none printed).")
fresh("FC1-b-r1-cards-duplicates", "PASS", "no two cards test the same fact (ids unique, fronts unique, no restatement)",
      "cards.json (169 entries) against the previous FC1-c173 (deleted) and FC1-c067",
      "Ids unique and fronts unique (out/cards_delta_identity.out: 'ids unique: True', 'fronts unique: True'; no exact duplicate back, out/dup_scan_r9.out). The round-8 duplicate FC1-c173 is deleted (out/cards_delta_identity.out: removed ['FC1-c173']). Full string-similarity scan re-run over all 169 entries (out/dup_scan_r9.out, 458 pairs above a 0.45 mean-similarity threshold): every pair in the top 40 was read in full: FC1-c058/c121 (buy stop vs sell stop); c132/c133 (best bid vs best ask); c036/c137 (spread s = a-b vs mid m = (a+b)/2); c152/c153 (bound d/rho vs equality condition phi = 1 or rho = 1); c013/c122 (equity after loss vs its sign condition); c061/c171/c169 (cost vs average vs remaining shares of one example); c165/c166 (clearing offset vs settlement lag); c158/c161, c159/c160 (exposure, venue, form values); c108/c113, c107, c105, c106 (distinct Assumptions B2-B4, A2-A3); c095/c096 (cash/derivative vs exchange/OTC counts); c118/c142 (what the offset check checks vs when it prints False). JUDGEMENT (not a defect in the scan): FC1-c064 defines price-time priority and FC1-c072 asks whether size enters priority and answers no with a worked case; FC1-c059 and FC1-c070 both mention the resting price. Each pair asks a different question (definition vs misconception with a worked case), so each is treated as distinct, as in rounds 5-8. A reviewer who reads c072 as a restatement of c064 would make this row a FAIL with fix: delete FC1-c072 or reword it to the misconception's worked case only.")
fresh("FC1-b-r7-delta-cards-c125-c173", "PASS", "round-7 delta: cards FC1-c125 (removed), FC1-c173 (added in round 7)",
      "cards.json (c173 removed; c125 absent)",
      "Round-8 FAIL resolved: FC1-c173 is deleted at 95f3f8cb (out/cards_delta_identity.out: 'removed ids [FC1-c173]', 'added ids []', 'c173/c174/c125 present: []'). The duplicate-of-c067 finding no longer applies. Delta text: git diff 4540351d 95f3f8cb -- course/modules/FC/FC1/cards.json is one hunk '@@ -1098,12 +1098,5 @@' removing the FC1-c173 object.")
fresh("FC1-b-r7-delta-cards-c174", "PASS", "round-7 FAIL: FC1-c174 restates FC1-c103 (cumulative identity); removal",
      "cards.json (c174 absent)", "Absent: out/cards_delta_identity.out 'c173/c174/c125 present: []'. No FC1-c174 in any FC1 file outside ledgers (grep: no hit).")
fresh("FC1-b-r7-twins-unchanged", "PASS", "tests/labs/FC1 has no diff since the previous pin", "tests/labs/FC1/*.py",
      "git diff --name-only 4540351d 95f3f8cb -- tests/labs/FC1 is empty (guards.out: 'changed tests/labs/FC1 -> []').")
fresh("FC1-b-r8-delta-cards-c125-removal", "PASS", "round-8 delta: card FC1-c125 removed",
      "cards.json (c125 absent)", "Absent at 95f3f8cb (out/cards_delta_identity.out: 'c173/c174/c125 present: []'); the 4540351d-to-95f3f8cb hunk does not re-add it.")
fresh("FC1-b-r8-delta-L04-lab-numbers", "PASS", "cards FC1-c061, c062, c069, c169, c171 against the L04 twin output",
      "tests/labs/FC1/lab-FC1-L04-1.py output (out/twin_L04.stdout)",
      "Re-checked this round: Fixture A 'fills (price, shares): [(1000, 60), (1100, 90)]', 'total cost 159000 cents', 'average 1060', '10 shares still resting at 1100' against FC1-c061, c169, c171; Fixture B 'all fills [(990, 100), (985, 100)]' and 'stop sell filled at 985' against FC1-c062; 'events with a crossed book: 0' and 'events where submitted != resting + 2 * traded + cancelled: 0' against FC1-c069. All identical to the round-8 twin output.")
fresh("FC1-b-r8-delta-L05-lab-numbers", "PASS", "cards FC1-c082, c083, c084, c085, c086, c088, c172 against the L05 twin output",
      "tests/labs/FC1/lab-FC1-L05-1.py output (out/twin_L05.stdout)",
      "Re-checked this round: 'fills 1', 'one trade of 216 shares at 10060 cents' (c082); settlement 'offset 2 date 2026-10-30 Friday' (c083); 'batch_trades 20 gross_payments_cents 68398886 net_payments_cents 14282414', net_to_gross_ratio 0.209 (c084; 14282414/68398886 = 0.20881062302681364 computed in Python); misconception numbers (c085, c086, c088: incoming limit 10117, trade 10060); consideration 2172960 (c172). All identical to the round-8 output.")
fresh("FC1-b-r8-mutants-none", "PASS", "mutation testing", "FC1-b slice: lessons and cards",
      "Not applicable: this slice has lessons, twins and cards (VERIFIER_RULES; ruling 37 says a closing round writes no new mutants). FC1-b has no standing mutant set; ledgers/FC1/mutants/r17n01-03 belong to the project slice FC1-c. No mutant was written this round.")
fresh("FC1-b-r9-delta-c173-deletion", "PASS", "round-9 delta: the only change in the slice is the deletion of card FC1-c173",
      "course/modules/FC/FC1/cards.json lines 1098-1102 at 4540351d (object removed)",
      "git diff --stat 4540351d 95f3f8cb -- course/modules/FC/FC1 tests/labs/FC1 notation references tools curriculum: only cards.json, 7 deletions. out/cards_delta_identity.out: 170 -> 169 entries, removed [FC1-c173], added [], no entry object modified, surviving order preserved, file ends with newline. check_pages (out/check_pages_unit.out) passes.")
fresh("FC1-b-r9-c173-no-references", "PASS", "no remaining reference to FC1-c173 in the repository outside ledgers/",
      "repository, excluding ledgers/, .git, .venv", "grep -rl 'FC1-c173' (excluding ledgers, .git, .venv): 0 files.")

fresh("FC1-b-r5-cards-full-scan", "PASS", "full scan of cards.json for duplicates, lesson-text agreement and trivia",
      "cards.json (169 entries, 1102 lines)",
      "Re-scanned all 169 entries this round: duplicates (out/cards_delta_identity.out ids and fronts unique; out/dup_scan_r9.out, read as in FC1-b-r1-cards-duplicates), numbers (out/cards_numbers_and_phrases.out: only FC1-c011 '1,818.18' differs from L01.html line 142 '1818.18' by a thousands separator; the value 1000/(1-0.45) = 1818.18 is correct), citations (out/cards_cites.out: 188 parenthetical citations; all resolve to a Definition, Proposition, Remark, Example, Problem, Assumption, Section or Lab label, or to a misconception list item numbered by position), and triviality (every card read; no trivia found in the L04/L05 cards read in full this round, see the cards-L04 and cards-L05 rows). L01-L03 entry-level lesson agreement is carried by entry identity from round 8.")

# ---- assemble
rows = []
for rid, r in prev_rows.items():
    pass
ids_in_order = [r["id"] for r in prev["rows"]]
new_extra = ["FC1-b-r9-delta-c173-deletion", "FC1-b-r9-c173-no-references"]
missing = [i for i in ids_in_order if i not in D]
extra_dec = [i for i in D if i not in ids_in_order and i not in new_extra]
print("missing decisions:", missing)
print("decisions not in round-8 rows:", extra_dec)
guard_ok = True
for rid in ids_in_order + new_extra:
    d = D[rid]
    if d[0] == "fresh":
        _, status, check, location, evidence, fix = d
        rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})
    else:
        _, gtext, (files, cards, note) = d
        ev = CARRY.format(g=gtext) + prev_rows[rid]["evidence"]
        if note: ev += " Note (round 9): " + note
        prow = prev_rows[rid]
        rows.append({"id": rid, "check": prow["check"], "location": prow["location"], "status": "PASS",
                     "evidence": ev, "fix": ""})
json.dump(rows, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print("rows", len(rows), Counter(r["status"] for r in rows))
