"""Verifier script: writes the FC1 slice b round-1 ledger fragment from the rows the verifier checked by hand and by command."""
import json
import sys

PASS, FAIL = "PASS", "FAIL"
L4 = "course/modules/FC/FC1/L04.html"
L5 = "course/modules/FC/FC1/L05.html"
T4 = "tests/labs/FC1/lab-FC1-L04-1.py"
T5 = "tests/labs/FC1/lab-FC1-L05-1.py"
SC = "ledgers/FC1/scripts/FC1-b-r1/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    rows.append(r)


row("FC1-b-cmd-pin", "2.9-structure", "repository", PASS,
    "git -C /tmp/verifyC1-FC1-b log --oneline -1 -> 55b5634 (detached); git status: only untracked .venv symlink before this round.")
row("FC1-b-cmd-run_labs", "2.5-lab", f"{T4}; {T5}", PASS,
    "tools/run_labs.py --unit FC1 --page L04 -> 'run_labs FC1: PASS (1/1)'; --page L05 -> 'run_labs FC1: PASS (1/1)'.")
row("FC1-b-cmd-twins-isolated", "2.5-lab", f"{T4}; {T5}", PASS,
    "python -I -W error tests/labs/FC1/lab-FC1-L04-1.py and ...L05-1.py: exit 0, 22 and 24 output lines (/tmp/fc1b-v/l04.out, l05.out). Second run identical (cmp). Wall time 0.04 s each.")
row("FC1-b-cmd-page_smoke", "2.5-lab", f"{L4}; {L5}", PASS,
    "tools/page_smoke.py --unit FC1 --pages L04 L05 -> 'page_smoke modules/FC/FC1/L04.html: PASS', 'L05.html: PASS', 'page_smoke FC1: PASS'.")
row("FC1-b-cmd-check_pages", "2.9-structure", f"{L4}; {L5}", PASS,
    "tools/check_pages.py --unit FC1 --page L04 -> PASS; --page L05 -> PASS. data-hours=10 on each lesson.")
row("FC1-b-cmd-check_dag", "DAG", "curriculum/02-economics-finance-core.yaml; course/modules/FC/FC1/L04.html; L05.html", PASS,
    "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS'. L04 links order-types, limit-order-book, bid-ask-spread (L03). L05 links financial-intermediary (L01, prerequisite), clearing-and-settlement, trade-lifecycle (defined in L05).")
row("FC1-b-cmd-lint-types", "2.5-lab", f"{T4}; {T5}", PASS,
    "ruff check and ruff format --check on both twins: 'All checks passed!', '2 files already formatted'. mypy on both: 'Success: no issues found in 2 source files'.")
row("FC1-b-cmd-refs", "2.1-citations", "references/references.json (harris2002trading)", PASS,
    "tools/verify_refs.py --unit FC1 -> 'live re-verification of FC1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'.")
row("FC1-b-reg-harris", "2.1-citations", f"{L4} section 8; {L5} section 4", PASS,
    "Registry record harris2002trading: year 2002, print_year 2002, years [2002, 2023], type edited-book. Both pages cite the registry year 2002 and no passage; L05 states the curriculum string (Harris 2003, curriculum/02-economics-finance-core.yaml line 385) differs from the registry. Consistent with architect ruling (b)/(c). No passage read (no locator claimed).")
row("FC1-b-reg-settlement-absent", "2.1-citations", f"{L5} section 4 and problem R1", PASS,
    "Registry scan (script check_embedded_and_arith is not used; inline json search of 560 entries for 'settle', 'clearing', 'depository'): hits bis2014basel, bis2024market, bis2025triennial, bisndbasel, bisndcpmi, duffie2011central. Titles read: none is a settlement-cycle source; duffie2011central is a CCP counterparty-risk paper that L05 says it does not read. Claim 'no settlement-cycle source admitted' holds.")
row("FC1-b-L04-lab-fixtures", "2.2-numbers", f"{L4} Example 1.3, 1.4, Lab 1 Fixtures", PASS,
    f"Lab output (/tmp/fc1b-v/l04.out) lines 'fills (price, shares): [(1000, 60), (1100, 90)]', 'total cost 159000 cents for 150 shares, average 1060 cents', 'shares still resting ... 1100: 10', 'all fills ... [(990, 100), (985, 100)]'. Recomputed: 60*1000+90*1100=159000, /150=1060; 10 shares left. Stop activates on trade 990 <= 990 (script run in twin).")
row("FC1-b-L04-lab-output-embedded", "2.5-lab", L4, PASS,
    f"ledgers/FC1/scripts/FC1-b-r1/check_embedded_and_arith.py /tmp/fc1b-v/l04.out /tmp/fc1b-v/L04.txt -> 'output lines 22 not found verbatim in page: 0'.")
row("FC1-b-L04-trace-claims", "2.5-lab", f"{L4} E2, Lab 1 prose", PASS,
    "Run trace: event 0 and 1 best ask none; event 2 best ask 10015; best bid none printed after event 7 (trace line 'event 7: market sell, best bid none'). E2 solution agrees. Lab prose 'best bid 9984 from event 0 until event 7' agrees with trace lines 0-6.")
row("FC1-b-L04-E1-E3", "2.2-numbers", f"{L4} E1, E3", PASS,
    "E1: 24 activated + 18 pending = 42 = printed stop arrivals. E3: 5600/173 exact fraction (python Fraction) = 32.37 (not printed; exact fraction is what is claimed).")
row("FC1-b-L04-R1-cascade", "2.4-math", f"{L4} Problem R1", PASS,
    f"ledgers/FC1/scripts/FC1-b-r1/check_L04_R1_cascade.py {T4}: 'R1 activations 2 fills [(990, 100), (985, 100), (980, 100)] pending 0'. Matches R1 solution; claim 'twin's activation loop produces exactly this sequence' verified.")
row("FC1-b-L04-prop2.2", "2.4-math", f"{L4} Proposition 2.2 and proof, P1, R2", PASS,
    "Induction over arrival and activation: market arrival keeps best bid, lifts best ask; buy limit residual rests at p with no ask <= p left, new best bid max(beta,p) < alpha'. Symmetric for sells. Gap checked: empty side and fully filled residual handled in text. Counterexample R2 (crossed start) recomputed: bid 1005 >= ask 1000 remains crossed.")
row("FC1-b-L04-prop2.3", "2.4-math", f"{L4} Proposition 2.3, Remark 2.4, P2, R3", PASS,
    "P2: G=250, X=100, C=50, R=0: 0+200+50=250. R3: 2*60=120. Lab counts 0 conservation failures over 300 events (l04.out line 'events where submitted != ... : 0'). Stops not yet activated are excluded from G in both the proof and lab code (submitted only increments in match()).")
row("FC1-b-L04-solutions", "2.4-math", f"{L4} Problems M1-M3, P1, E1-E3, R1-R3", PASS,
    "M1: 60*995+40*990=99300, avg 993, 60 left at 990. M2: fills 30@1000, 20@1001; left 10@1001, 40@1003. M3: thresholds 1005, 1001 no, 1000 yes. All recomputed by hand and in python.")
row("FC1-b-L04-misconceptions-quiz", "2.4-math", f"{L4} section 4 and section 7", PASS,
    "Misconception 3 and card c072 example (10-share sell first, market buy of 10 fills it) agree with Definition 2.1. Quiz answers: 1060 cents, 10 shares remaining, 24+18=42, the 2X term (Problem R3) and A1 (empty start) all match the lesson text.")
row("FC1-b-L04-grade-keyrow5", "2.3-grades", f"{L4} section 6 key results, row 'Zero crossed events and zero conservation failures across 300 SIMULATED events'", FAIL,
    "Row graded T with source 'Lab 1 counts, consistent with Propositions 2.2 and 2.3'. Brief rule (e) and BLUEPRINT grading: results read off a SIMULATED lab are grade C with a basis naming the lab. The row is a count read off Lab 1 output (l04.out: 'events with a crossed book: 0', 'events where submitted != ...: 0'), not a proof on the page.",
    "Grade the row C, basis 'Lab 1 (SIMULATED, seed 2026)'. Keep the T rows for Propositions 2.2 and 2.3.")
row("FC1-b-L04-no-claim-below-T", "2.3-grades", f"{L4} section 8 final sentence", FAIL,
    "Sentence reads: 'Every result on this page is proved in the lesson or checked by Lab 1, and no claim is graded below T.' The page grades results C (row 5 as built) and the Lab 1 results are C under rule (e); the sentence contradicts the page's own legend (C = single study) once row 5 is regraded.",
    "Delete 'and no claim is graded below T' or make it true after the row-5 regrade (e.g. 'proved results are graded T; results read off Lab 1 are graded C').")
row("FC1-b-L04-scope-words", "2.4-math", f"{L4} lines with only, every, always, any, same", PASS,
    "Scope words checked with witnesses: 'Only the first 60 shares fill at the screen price' (fills 60 at 1000, then 90 at 1100); 'every event' (lab loop checks every event, lab line 'events with a crossed book'); 'every run' (Propositions are general proofs); 'every run prints the same numbers' (rerun identical, cmp); 'the book only lost asks' (proof of 2.2). No unsupported scope word found.")
row("FC1-b-L04-banned-phrases", "2.9-structure", L4, PASS,
    "Scan of L04 text for roughly, about N, historically, ellipsis, build/builder/round/verifier/requests/unit report: no hits.")
row("FC1-b-L04-cards", "2.7-cards", "course/modules/FC/FC1/cards.json c056-c072 (L04)", PASS,
    "17 cards read against L04 text. Each card number appears in its lesson (150, 60, 1000, 1100, 159000, 1060, 990, 985, 120, 300, 10015 etc). Hypotheses A1 carried where the proposition needs it (c065, c066). No duplicate front or back in the 90-card unit set.")
row("FC1-b-L05-prop2.1", "2.4-math", f"{L5} Proposition 2.1 and proof", PASS,
    "(i) sum of x_j = sum c_i - sum c_i = 0; (ii) 0 <= NP <= G with -x_j <= Pay_j. Checked by lab output (sum_of_net_positions_cents 0, net_payments_at_most_gross True) and by recomputation: NP 14282414 <= G 68398886. R2 negative-consideration counterexample recomputed: 100 <= -100 false.")
row("FC1-b-L05-prop2.2-sign", "2.4-math", f"{L5} Proposition 2.2 statement and proof; Key results row for Prop 2.2; card FC1-c080", FAIL,
    "Statement: 'participant j's net obligation to the CCP is x_j', x_j = Rec_j - Pay_j. Under the leg structure of the proof, j receives Rec_j and pays Pay_j from the CCP, so j's net PAYMENT to the CCP is Pay_j - Rec_j = -x_j. With x_j > 0 (j is owed) the page calls it an obligation to the CCP. Internally consistent only if 'obligation' is redefined as the signed position. Problem P3 and card c080 repeat the same convention. Sign convention is undefined in the text.",
    "Define the signed quantity explicitly. Write: 'j's net position with the CCP is x_j (negative means j pays the CCP, which is -x_j in payments)', and use the same wording in the key-results row, P3 and card FC1-c080.")
row("FC1-b-L05-prop2.1-P2-P3", "2.4-math", f"{L5} proofs of P2, P3; Problem P1", PASS,
    "P1 (NP=G when no one nets) recomputed in general form. P2: f(x)=max(-x,0) is non-increasing and 1-Lipschitz, so brackets lie in [-c_t,0] and [0,c_t] (c_t >= 0 by A1). P3: buyer -c, seller +c. Each proof step checked.")
row("FC1-b-L05-lab-numbers", "2.2-numbers", f"{L5} section 3 before-run paragraph; Lab 1 output", PASS,
    "l05.out: resting P2 10060x263, P3 10257x362, P4 10331x152; incoming P1 10117x216; one fill; 216*10060=2172960 (recomputed). Batch gross 68398886, net 14282414 (lines reproduced verbatim in page: 0 missing of 24).")
row("FC1-b-L05-ratio", "2.2-numbers", f"{L5} Lab 1 prose, key results, card FC1-c084, quiz", PASS,
    "14282414/68398886 = 0.2088106... (python); floor(1000*NP/G + 1/2) = 209, so 0.209 half up; exact quotient 0.20881 to five decimals; basis = gross payments stated. Four-decimal rounding 0.2088 (quiz) correct.")
row("FC1-b-L05-E1-E2", "2.2-numbers", f"{L5} E1, E2", PASS,
    "E1: 11060360/68398886 = 0.161704 -> 16.17% of gross; 11060360/14282414 = 0.774404 -> 77.44% of net (both recomputed; basis stated). E2: 7411991+6656379+214044 = 14282414 = positives 3222054+11060360; net positions sum 0.")
row("FC1-b-L05-E3", "2.5-lab", f"{L5} E3 solution", FAIL,
    "E3 claims 'the last line still prints True'. Lab 1 with SETTLEMENT_LAG=3 (sed copy, python -I): diff vs run shows only the header line and the settlement and position_update lines change (their dates become Monday 2026-11-02 at offset 3). The line that stays True is 'offsets_nondecreasing True', which is the 14th-from-last line, not the last output line (the last line is 'net P5 cents 11060360'). The claim 'No other line changes' is true.",
    "Replace 'so the last line still prints True' with 'so the line offsets_nondecreasing still prints True'.")
row("FC1-b-L05-M2-dates", "2.2-numbers", f"{L5} M2, Lab 1 settlement date", PASS,
    "2026-10-28 is Wednesday, 2026-10-30 Friday, 2026-11-02 Monday (python datetime). Offsets: Thu 29 = 1, Fri 30 = 2; Mon 2 Nov = 1, Tue 3 Nov = 2 as in M2.")
row("FC1-b-L05-M1-M3", "2.4-math", f"{L5} M1, M3", PASS,
    "M1: 100*10090=1009000 cents = 10090.00 units. M3: consideration 1000000 each, G=2000000, NP=1000000, ratio 0.500 on gross, positions -1e6, 0, +1e6 sum 0.")
row("FC1-b-L05-key-results-grades", "2.3-grades", f"{L5} section 7 key results", PASS,
    "Proved rows graded T (Prop 2.1(i),(ii); Prop 2.2 wording aside, see FC1-b-L05-prop2.2-sign). Lab rows graded C with 'Lab 1 (SIMULATED)' basis, as rule (e) requires.")
row("FC1-b-L05-cards", "2.7-cards", "course/modules/FC/FC1/cards.json c073-c090 (L05)", FAIL,
    "18 cards read against L05. All numbers appear in the lesson (2172960, 10060, 10117, 14282414, 68398886, 0.209, 0.20881, 2026-10-30). Card FC1-c080 repeats the Prop 2.2 sign convention (net obligation = x_j), which is defective (see FC1-b-L05-prop2.2-sign). Other cards agree with current text and keep hypotheses A1 and A4.",
    "Fix FC1-c080 with the same wording as the lesson fix in FC1-b-L05-prop2.2-sign.")
row("FC1-b-L05-section4-scope", "2.9-structure", f"{L5} section 4 and sections 5-6", PASS,
    "'The settlement lag is not a fact' and 'no settlement period for any market' are prose claims; the registry scan shows no settlement-cycle source (FC1-b-reg-settlement-absent). 'Settlement is due ...' lines state the lab parameter. Scope words: 'every amount is SIMULATED' and 'no holiday calendar is used' are checked against code (business_day_after counts weekdays only).")
row("FC1-b-L05-banned-phrases", "2.9-structure", L5, PASS,
    "Scan for roughly, about N, historically, ellipsis, process words: no hits. Quiz distractors 'always' and 'every market' are wrong answers, not claims.")
row("FC1-b-notation", "2.4-math", f"{L4}, {L5} (symbols G, R, X, C, alpha, beta, p, s, q, c, J, n, Rec, Pay, x, NP, CCP)", PASS,
    "notation/notation.json has 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). None of the symbols used on L04/L05 is in it, and none is used with a registry meaning (T is not used). Lesson-local reuse of G (total shares in L04, gross payments in L05) and of 'A1' (start empty in L04, positive integers in L05) is scoped per lesson; flagged as an observation, not a conflict.")
row("FC1-b-labels-P1", "2.9-structure", f"{L5} Problem P1-P3, lab participants P1-P5", PASS,
    "Problem labels P1-P3 and participant names P1-P5 share the prefix P. Readable (problems are cited with the middle dot), so not a defect. Observation only.")
row("FC1-b-hours", "2.10-hours", f"{L4} and {L5} data-hours=10; course/modules/FC/FC1/index.html data-hours-lessons=50", PASS,
    "L01-L05 data-hours 10 each (verified by regex), sum 50 = hub data-hours-lessons 50; project 20; total 70. Arithmetic consistent. Pace not judged (architect ruling).")
row("FC1-b-mutants", "2.6-grader", "project slice only", PASS,
    "Slice b is lessons L04-L05 and their twins; no grader is in this slice. Mutation testing applies to project graders only (architect ruling). No mutants written for this slice.")
row("FC1-b-not-run", "2.9-structure", "gates", PASS,
    "Not run here: pytest suite (tests/labs and test_refs), build_site --check, render_curriculum, fetch_data --check; they are repo-wide, owned by architect.")

fragment = {
    "unit": "FC1",
    "slice": "FC1-b",
    "round": 1,
    "verifier": "independent Haiku verifier, FC1 slice b (L04-L05 and twins); did not build FC1",
    "pin": "55b5634",
    "base": "none",
    "checkout": "/tmp/verifyC1-FC1-b (detached at 55b5634)",
    "scratch": "/tmp/fc1b-v",
    "verified_at": "2026-10-28",
    "verdict": "FAIL" if any(r["status"] == FAIL for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lab twins are demonstrations; mutation testing not applicable (architect ruling).",
        "Curriculum string for Harris reads 2003; registry year is 2002; both pages cite the registry year only (architect ruling).",
        "Duffie 2011 is in the registry and bears on CCP risk; L05 says it reads no evidence on that question, which is true for this slice.",
    ],
    "summary": {"rows": len(rows), "pass": sum(r["status"] == PASS for r in rows), "fail": sum(r["status"] == FAIL for r in rows)},
}
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, fragment["summary"], fragment["verdict"])
