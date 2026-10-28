import json, re, sys
ROOT = "/tmp/verify21-M1-b"
prev = json.load(open("/tmp/fanout-frags/M1-b.round20.json"))
CARRY = ("Carried from round 20 (course/modules/M/M1/L04.html, L05.html and cards.json byte-identical "
         "since the previous pin fd9a9b7 at the cited lines; the round-21 delta changes only L04.html "
         "lines 79 and 112, L05.html line 127, cards.json lines 461, 597, 1133 and 1222, none cited here): ")
STRIP = re.compile(r"^Carried from round \d+ \(.*?\): ", re.S)
FRESH = {}
def fresh(i, loc, ev, status="PASS"):
    FRESH[i] = dict(check=None, location=loc, status=status, evidence=ev)

fresh("M1-b-cmd-pin", "repository HEAD; course/modules/M/M1/L04.html, L05.html, cards.json; tests/labs/M1; tools; references/references.json",
      "git rev-parse HEAD = f95243f240ec2e871508dc895c8cc960c00f7d5d (detached). git diff fd9a9b7 f95243f over course/modules/M/M1: L04.html 79 and 112, L05.html 127, cards.json 461, 597, 1133, 1222 (7 lines changed in total). git diff 51fa336 f95243f over tests/labs/M1, tools and references/references.json: empty.")
fresh("M1-b-cmd-run_labs", "tools/run_labs.py; course/modules/M/M1/L04.html; L05.html",
      "Command: .venv/bin/python tools/run_labs.py --unit M1 (exit 0): 'run_labs M1: PASS (11/11)'. Saved at ledgers/M1/scripts/M1-b-r21/out/run_labs.txt.")
fresh("M1-b-cmd-twins", "tests/labs/M1/lab-M1-L04-1.py; lab-M1-L05-1.py; course/modules/M/M1/L04.html expected block 191-217; L05.html expected block 223-235",
      "Each twin run as /tmp/verify21-M1-b/.venv/bin/python -I -W error from /tmp: exit 0, empty stderr; L04 prints 27 lines, L05 prints 13 lines (out/L04 and L05 outputs). ledgers/M1/scripts/M1-b-r21/embed_cmp.py compares the embedded <pre class=\"expected\"> block with the twin output: True for both (27 = 27 lines, 13 = 13 lines).")
fresh("M1-b-cmd-page_smoke", "tools/page_smoke.py --unit M1 --pages L04 L05",
      "Command exit 0; 'page_smoke modules/M/M1/L05.html: PASS' and 'page_smoke M1: PASS'. out/page_smoke.txt.")
fresh("M1-b-cmd-check_pages_dag", "tools/check_pages.py --unit M1; tools/check_dag.py --unit M1",
      "check_pages --unit M1: 'check_pages M1: PASS' (exit 0). check_dag --unit M1: 'check_dag M1: PASS' (exit 0). out/check_pages.txt, out/check_dag.txt.")
fresh("M1-b-cmd-lint-types", "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py",
      "ruff check on both twins: 'All checks passed!' (exit 0). ruff format --check: '2 files already formatted' (exit 0). mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' (exit 0). out/ruff_check.txt, out/ruff_format.txt, out/mypy.txt.")
fresh("M1-b-cmd-refs", "references/references.json; tools/verify_refs.py; L04.html and L05.html references (459-462, 472-475)",
      "verify_refs.py --offline (exit 0): 'offline integrity: 560 entries, 0 problems'. verify_refs.py --unit M1 (exit 0): 'live re-verification of M1: 1 of 560 entries, 0 problems'. Both pages cite no registry key (references paragraphs 460 and 473 unchanged).")
fresh("M1-b-cmd-pytest", "tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py",
      "pytest -q on the three files: exit 0 (out/pytest.txt).")
fresh("M1-b-2.7-cards", "course/modules/M/M1/cards.json: L04 cards M1-c064..c076, c144, c163, c176; L05 cards M1-c077..c092, c145, c152, c160, c177, c181; M1-c068 at cards.json:461",
      "Round-20 FAIL resolved for M1-c068: cards.json:461 now reads '(1 + r/m)^(mt) when mt is a whole number, because mt is then the number of periods (Remark 1.3).' That matches L04.html:70 ('with mt a whole number ... the number of periods'). Full scan of all 180 entries (out/cards_scan.txt, Counter-based): no duplicate id, no duplicate front. The L04/L05 cards were re-read against their lesson lines this round where the lesson text changed or the card states a scope: c068, c070, c075, c084, c085, c086, c087, c088, c089, c160, c163, c177, c181. The other L04/L05 card texts are byte-identical since fd9a9b7 and cite lesson lines that are unchanged; they are carried from round 20, where each was checked against its lesson line. Card M1-c088 and M1-c163 and M1-c177 are rows M1-b-r20-cards-c088, M1-b-r17-2.7-cards-c163-scope and M1-b-r21-cards-c177.")
fresh("M1-b-r20-cards-c088", "cards.json:597; L05.html:131-133",
      "cards.json:597 now reads 'No. Under Assumption E, the semiannual factor is strictly smaller (Proposition 2.4), so the two conventions give different discount factors at t = 5.' Proposition 2.4 (L05.html:132) is stated 'Assume E'. Round-20 FAIL resolved.")
fresh("M1-b-r20-E-scope-remarks", "L04.html:79, 112; L05.html:127",
      "Round-20 defects fixed: L04.html:79 list now includes 'Remark 2.3'; L04.html:112 (Remark 2.3) now reads 'Under Assumption E, Proposition 2.2 says ...'; L05.html:127 (Remark 2.3) now reads 'Under Assumption E, Proposition 2.2 says ...'. A residual omission in the L04.html:79 list is recorded as M1-b-r21-E-list-complete (FAIL).")
fresh("M1-b-2.5-lab-L04", "course/modules/M/M1/L04.html: Lab 1 hypothesis (117), Remark 2.3 (112), interpretation (218), misconceptions (253-261); tests/labs/M1/lab-M1-L04-1.py",
      "Line 117 names Propositions 2.1 and 2.2 and the ten values of m; tests/labs/M1/lab-M1-L04-1.py:22 PERIODS has ten entries (1, 2, 4, 12, 52, 365, 1000, 10000, 100000, 1000000); the twin prints Part B for those ten values (out/L04 output). Remark 2.3 (112) 'Part B of Lab 1 prints that gap for ten values of m' matches.")
fresh("M1-b-2.5-lab-L05", "course/modules/M/M1/L05.html: Lab 1 hypothesis (142), Remark 2.3 (127), interpretation (236), misconceptions 1-3 (266-274); tests/labs/M1/lab-M1-L05-1.py",
      "Line 142 names five t values; tests/labs/M1/lab-M1-L05-1.py:25 YEARS has five entries (0.5, 1, 2, 5, 10). The twin's output rows (out/L05 output) carry annual and continuous_at_5pct columns at those five t. Remark 2.3 (127) 'Lab 1 prints the annual factor and the continuous factor at 0.05 at five times' matches. Interpretation line 236 is byte-identical since fd9a9b7 (checked against the same rows).")
fresh("M1-b-2.9-DAG", "tools/check_dag.py --unit M1 (re-run); L04.html meta-rows (38) and definitions (59, 65, 67); L05.html meta-rows (38, 39) and definitions (64, 65, 69)",
      "check_dag --unit M1: PASS (re-run this round). None of the meta-rows or definition lines listed is in the delta (the delta lines are 79, 112, 127).")
fresh("M1-b-2.9-structure-prose", "course/modules/M/M1/L04.html and L05.html (delta lines 79, 112, 127 re-read in full; banned-phrase and process-word grep over both pages)",
      "grep -i over both pages for roughly, historically, typically, generally, usually, about 6%, builder, verifier, 'round N', ellipsis, 'unit report', REQUEST: no matches. Delta sentences read in full (L04.html:79, 112; L05.html:127): no banned phrase, no process word, no ellipsis. The unchanged lines are carried from round 20 (byte-identical since fd9a9b7); the full line-by-line re-read of unchanged lines was not repeated this round (see notes).")
fresh("M1-b-2.4-math-L04", "course/modules/M/M1/L04.html: Prop 2.1 block (83-90), Prop 2.2 (101-109), R2 (358), R3 (361-367), key results (378-380), references (460)",
      "Re-read this round: Prop 2.2 statement and proof (101-109): proof at 107 is Assumption E with x = r/m, raised to the m-th power (valid since 0 < a < b gives a^m < b^m for whole m >= 1), then (e^(r/m))^m = e^r by A2. R3 (365): (1 + r_m/m)^m = e^r; the positive root is e^(r/m) by strict monotonicity of x^m on the positive reals; for even m, (-e^(r/m))^m = e^r, so the hypothesis 1 + r_m/m > 0 is needed as witnessed (algebra). Line 112 is Remark 2.3, verified in M1-b-r21-L04-112. No proof line changed.")
fresh("M1-b-2.4-math-L05", "course/modules/M/M1/L05.html: Assumption E block (79-84), Prop 1.4 proof (88-93), Prop 2.1 (106-110), Prop 2.2 proof (117-123), Prop 2.4 (131-137)",
      "Re-read this round. Prop 1.4 proof (93): b = 1 + r > 1, b^(-t) = 1/b^t, b^t > 1 for t > 0, and for 0 <= s < t, b^(-s) > b^(-t) (A2 gives b^(-s) = b^(t-s) b^(-t) with b^(t-s) > 1). This proves the statement for t >= 0 as written in L05.html:88. Prop 2.1 (106-110) and Prop 2.2 (117-123): proofs valid, E used at x = r. Prop 2.4 (137): A = (1 + r/2)^2 = 1 + r + r^2/4 > B = 1 + r > 0, and x -> x^t is strictly increasing for t > 0. Line 127 is Remark 2.3, verified in M1-b-r21-L05-127.")
fresh("M1-b-r17-2.7-cards-c163-scope", "course/modules/M/M1/cards.json M1-c163 (line 1133); L04.html:365 (R3)",
      "cards.json:1133 (changed this delta) reads 'The condition 1 + r_m/m > 0 is needed, since for even m, 1 + r_m/m = −e^(r/m) also satisfies the equation.' L04.html:365 says 'for even m, 1 + r_m/m = -e^(r/m) also satisfies the condition'. Algebra: (-e^(r/m))^m = e^r for even m. Scope: the card says 'is needed' and the lesson says 'The hypothesis is needed'; the witness is for even m, which is what both state. PASS.")
fresh("M1-b-r4-term-before-def-L04", "course/modules/M/M1/L04.html:52 (why-it-matters), 54-56 (s1), 59 (Def 1.1), 78-80 (Assumption E)",
      "Re-read this round, including the changed line 79. The new list adds the label 'Remark 2.3', which is defined later at line 111; a cross-reference to a later block, not a term used in a computation before its definition. Proposition 2.2 is named at line 79 before its statement at line 101; this is the same cross-reference as in round 20 and is accepted as a pointer to a stated result. PASS.")
fresh("M1-b-r18-cards-scan", "course/modules/M/M1/cards.json",
      "Scan re-run this round: 180 entries; no duplicate id, no duplicate front (out/cards_scan.txt).")
fresh("M1-b-r19-cards-scan", "course/modules/M/M1/cards.json",
      "Scan re-run this round (same as M1-b-r18-cards-scan): 180 entries, L04 16 and L05 21 cards; no duplicates.")
fresh("M1-b-r18-cards-unchanged-L04-L05", "cards.json: M1-c067, c072, c083, c176, c177; L04.html:64 (Def 1.2), 361-367 (R3); L05.html:87-89 (Prop 1.4)",
      "c067, c072, c083, c176 byte-identical since fd9a9b7 and their lesson lines unchanged. c177 changed (cards.json:1222) and is checked in M1-b-r21-cards-c177.")
fresh("M1-b-r18-embed-twins", "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py; course/modules/M/M1/L04.html:116-190 and 191-217 expected block; L05.html:141-222 and 223-235 expected block",
      "Re-run this round: ledgers/M1/scripts/M1-b-r21/embed_cmp.py: L04 expected block equals twin output (27 lines), L05 equals twin output (13 lines).")

NEW = {}
NEW["M1-b-r21-E-list-complete"] = dict(
    check="Scope of the L04.html:79 list of places that cite Proposition 2.2 (round-20 fix)",
    location="course/modules/M/M1/L04.html:79 (list), 75 and 460 (places that cite Proposition 2.2 but are not in the list)",
    status="FAIL",
    evidence=("L04.html:79 now reads 'It is used in Proposition 2.2, in the places that cite that proposition (Lab 1, Problem R2, Remark 2.3, "
              "the key-results table, quiz item 5 and the misconception in §5), and directly in Problem R3.' The round-20 fix added Remark 2.3, "
              "but two places that cite Proposition 2.2 are still omitted: L04.html:460 (References paragraph: 'Proposition 2.2 from Assumption E') "
              "and L04.html:75 (section 2 introduction: 'Proposition 2.2 uses an inequality, which is stated as Assumption E in the next block'). "
              "Found by grep -n 'Proposition 2.2' over L04.html (lines 75, 101, 107, 112, 261, 358, 365, 378, 380, 425, 460). The list is a closed "
              "parenthetical, so the completeness claim is false as written."),
    fix="Add 'the section 2 introduction (line 75) and the references paragraph (line 460)' to the list in L04.html:79, or replace 'the places that cite that proposition (...)' with 'Proposition 2.2 and the places that cite it, including Lab 1, ...'.")
NEW["M1-b-r21-L04-112"] = dict(check="Remark 2.3 rewrite (L04.html:112) against Propositions 2.1, 2.2 and Lab 1 Part B",
    location="course/modules/M/M1/L04.html:111-113; tests/labs/M1/lab-M1-L04-1.py:22",
    status="PASS",
    evidence="'Proposition 2.1 says that the factors rise with m' matches Prop 2.1 (L04.html:84-85: strictly increasing in m for r > 0). 'Under Assumption E, Proposition 2.2 says that they stay below e^r' matches Prop 2.2 (101-102). 'These two results do not say how close F_m(r) comes to e^r' is a scope statement that holds because both results are one-sided bounds. 'Part B of Lab 1 prints that gap for ten values of m' matches PERIODS (10 entries). No claim of convergence is made.")
NEW["M1-b-r21-L05-127"] = dict(check="Remark 2.3 rewrite (L05.html:127) against Proposition 2.2 (L05.html:116-118) and Lab 1",
    location="course/modules/M/M1/L05.html:126-128; tests/labs/M1/lab-M1-L05-1.py:25",
    status="PASS",
    evidence="'Under Assumption E, Proposition 2.2 says that treating r as a continuous rate discounts more than treating r as an annual effective rate' matches Prop 2.2 (L05.html:117: 'Assume E. Let r > 0 and t > 0. Then e^(-rt) < (1+r)^(-t)'). 'Lab 1 prints the annual factor and the continuous factor at 0.05 at five times' matches YEARS (five entries) and the twin's rows. The gap-as-difference-of-columns statement is arithmetic on the printed columns.")
NEW["M1-b-r21-cards-c068"] = dict(check="Card M1-c068 back against Remark 1.3 (L04.html:70)",
    location="course/modules/M/M1/cards.json:461; L04.html:70", status="PASS",
    evidence="Card back: '(1 + r/m)^(mt) when mt is a whole number, because mt is then the number of periods (Remark 1.3).' Remark 1.3: 'with mt a whole number, the factor is (1 + r/m)^(mt), because mt is then the number of periods.' Agree.")
NEW["M1-b-r21-cards-c075-credit"] = dict(check="Card M1-c075 term 'credit' against its definition in L04",
    location="cards.json (M1-c075); L04.html:60", status="PASS",
    evidence="Card: 'each extra credit adds value (Proposition 2.1)'. L04.html:60 defines 'Interest is credited m times a year', so 'credit' is defined before the card's use. Prop 2.1 (84-85) gives the increase in m; no defect.")
NEW["M1-b-r21-cards-c084-c089-scope"] = dict(check="Scope words of cards M1-c084, c085, c086, c087, c089 against Propositions 1.4, 2.1, 2.2, 2.4",
    location="cards.json M1-c084..c089; L05.html:88, 103-105 (Prop 2.1), 117, 132, 116", status="PASS",
    evidence="c084 'for every t >= 0' matches Prop 2.1 ('For every t >= 0'). c085 'Yes, under Assumption E' matches Prop 2.2. c086 'Yes, strictly, under Assumption E' matches Prop 2.4 (L05.html:132). c087 'Under Assumption E, for r > 0 and t > 0' matches Prop 1.4 (88). c089 'for every t > 0' matches Prop 2.2. No defect.")
NEW["M1-b-r21-cards-c177"] = dict(check="Card M1-c177 (changed to 't > 0') against Proposition 1.4 (L05.html:88)",
    location="course/modules/M/M1/cards.json:1222; L05.html:88", status="PASS",
    evidence="Card now: 'It strictly decreases for t > 0, under Assumption E (Proposition 1.4).' Prop 1.4 states strict decrease for t >= 0 (L05.html:88, proof 93 covers 0 <= s < t). The card states a true subset of the proposition, so it does not contradict it. Noted, not a defect.")
NEW["M1-b-r21-mutants"] = dict(check="Mutants: project-slice requirement; slice b is lessons and twins only", location="ledgers/M1/mutants/ (slices a and c)", status="PASS",
    evidence="Architect ruling (lab twins are demonstrations; mutation testing applies to project graders only). No student-error mutants are written for slice b; the mutant directory is not part of this slice.")

rows = []
seen = set()
for r in prev["rows"]:
    i = r["id"]
    if i in FRESH:
        f = FRESH.pop(i)
        rows.append(dict(id=i, check=r["check"], location=f["location"], status=f["status"], evidence=f["evidence"]))
    elif i in ("M1-b-2.7-cards", "M1-b-r20-cards-c088", "M1-b-r20-E-scope-remarks"):
        raise SystemExit("missing fresh row for " + i)
    else:
        assert r["status"] == "PASS", i
        ev = STRIP.sub("", r["evidence"], count=1)
        rows.append(dict(id=i, check=r["check"], location=r["location"], status="PASS", evidence=CARRY + ev))
    seen.add(i)
assert not FRESH, FRESH.keys()
for k, v in NEW.items():
    rows.append(dict(id=k, **v))
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
miss = [i for i in (r["id"] for r in prev["rows"]) if i not in ids]
assert not miss, miss
statuses = [r["status"] for r in rows]
frag = dict(unit="M1", slice="M1-b", round=21,
    verifier="independent verifier (Haiku), round 21",
    pin="f95243f240ec2e871508dc895c8cc960c00f7d5d",
    base="fd9a9b7 (round 20 pin; delta lines: L04.html 79, 112; L05.html 127; cards.json 461, 597, 1133, 1222)",
    previous_fragment="/tmp/fanout-frags/M1-b.round20.json",
    checkout="/tmp/verify21-M1-b", scratch="/tmp/M1-v/M1-b-r21",
    verified_at="2026-10-28T12:00:00+00:00",
    verdict="FAIL" if "FAIL" in statuses else "PASS",
    mutants=[], registry_flags=[], freshness_flags=[],
    notes=[
        "Slice b is lessons L04 and L05 with their twins, not a project slice: no new student-error mutants or alternative implementations apply (same ruling as rounds 16-20). ledgers/M1/mutants/ holds the project mutants of slices a and c.",
        "Delta fd9a9b7..f95243f for slice b: L04.html lines 79 and 112; L05.html line 127; cards.json lines 461 (M1-c068), 597 (M1-c088), 1133 (M1-c163), 1222 (M1-c177). tests/labs/M1, tools and references are unchanged since 51fa336.",
        "Round-20 FAIL rows M1-b-2.7-cards (M1-c068) and M1-b-r20-cards-c088 are resolved. M1-b-r20-E-scope-remarks is resolved for the two defects it named; its residual omission is the new FAIL row M1-b-r21-E-list-complete.",
        "Not checked this round: a full line-by-line re-read of every unchanged line of L04.html and L05.html. Unchanged lines are carried from round 20 by byte-identity of the cited lines, as in rounds 16-20. Every command row was re-run this round.",
        "Not checked: no external source is cited or read in this slice; the registry check is a live sample (1 of 560 entries) plus the full offline integrity pass. Lab output is exact arithmetic (no SIMULATED data).",
        "Card M1-c181 (L05) and card M1-c180 (L07) status is carried from round 20; card M1-c180 belongs to lesson L07, outside this slice.",
    ],
    summary={"rows": len(rows), "pass": statuses.count("PASS"), "fail": statuses.count("FAIL"), "unverifiable": statuses.count("UNVERIFIABLE")})
frag["rows"] = rows
out = ROOT + "/ledgers/M1/M1-b.json"
json.dump(frag, open(out, "w"), ensure_ascii=False, indent=1)
print(out, frag["verdict"], frag["summary"])
