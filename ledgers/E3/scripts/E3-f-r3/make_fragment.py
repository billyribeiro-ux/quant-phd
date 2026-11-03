"""Build ledgers/E3/E3-f.json (round 3) from the scripts and locator output of this round.

Every card row cites cards.json:<line> and the lesson locators found by locate_card_refs.py (file:line). Rows for the
numeric cards cite out/rederive.out (independent re-derivation), out/run_labs_*.out and out/twin-*.stdout (lab output).
Run with: .venv/bin/python -I ledgers/E3/scripts/E3-f-r3/make_fragment.py
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-E3-f")
CARDS = ROOT / "course/modules/E/E3/cards.json"
SCR = ROOT / "ledgers/E3/scripts/E3-f-r3"
OUT = SCR / "out"
LOC = json.loads((OUT / "card_locators.json").read_text(encoding="utf-8"))
cards = [c for c in json.loads(CARDS.read_text(encoding="utf-8")) if c["lesson"] in ("L01", "L02", "L03", "L04")]
lines = CARDS.read_text(encoding="utf-8").split("\n")

# Card-level findings that are not plain PASS. Key: card id. Value: (status, evidence, fix).
NOTES: dict[str, str] = {
    "E3-c013": "PASS with note: the front asks 'which one' and the back names one maximiser; R1 (L01.html:437) "
    "shows the maximisers are all lotteries on outcomes attaining m, so the card is correct but does not say the "
    "maximiser is not unique. Not a failure.",
    "E3-c015": "Round-2 locator defect fixed (now 'Definitions 1.2 and 3.2'; Definition 1.2 is L01.html:63, Definition "
    "3.2 is L01.html:142). The card's statement is correct. Duplicate of E3-c006 is recorded in E3f-dup-c006-c015.",
    "E3-c026": "Assuming F6 is stated (L02.html Example 2.3 'by F6'); r_A=1/(2w), r_R=1/2 re-derived in rederive.out.",
    "E3-c029": "Round-2 unit defect fixed on the card and in L02.html:395 (now '900 CU squared'); Var(X)=1800 CU^2 "
    "re-derived exactly (rederive.out).",
    "E3-c030": "Round-2 missing assumption fixed: 'Assuming F6' (Example 2.3 at L02.html:158 'by F6').",
    "E3-c039": "Round-2 missing A2 fixed ('Assuming A2 ... (Proposition 1.4)', L03.html:94). The card also repeats the "
    "limit that E3-c040 owns; see E3f-dup-c039-c040.",
    "E3-c051": "Round-2 missing F2 fixed ('Assuming F2', Proposition 1.7 at L03.html:116). The Proposition 1.7 values "
    "repeat E3-c041; see E3f-dup-c041-c051.",
    "E3-c052": "New card. Gamma = 0 is the affine member: u_0(w)=w-1 (L03.html Example 1.5 at line 106). Ranking "
    "claim follows from L01 Proposition 3.3 (L01.html:147). Checked: correct.",
    "E3-c054": "Lab values re-derived in rederive.out (CE at gamma 0, 1, 2, 4 = 11250, 10000, 8888.8889, 7337.6161); "
    "printed block at L03.html lab output and out/twin-L03-1.stdout. The gamma = 2 value repeats E3-c055; see "
    "E3f-dup-c054-c055.",
    "E3-c055": "80000/9 and M=9/80000 re-derived exactly (rederive.out). Problem E2 at L03.html:422 carries "
    "\\tfrac{9}{80000}; the token is present in LaTeX form (card_numbers.out).",
    "E3-c068": "Example 2.5 values re-derived (rederive.out: I_X, I_Y, F_X(2000)=1/2 > 1/4, F_Y(3000)=3/4 > 1/2).",
    "E3-c070": "Example 1.7 vectors F_X=(1/2,1/2,1), F_Y=(0,1/2,1) re-derived with a dict-based CDF (rederive.out).",
    "E3-c073": "Basis 'Lab 1 (SIMULATED)' matches the lab; pairs 16 and 19 re-derived by an independent generator "
    "(rederive.out, indices [16, 19]). The count also appears in E3-c076 as a supporting tally; not a duplicate "
    "(different question; see E3f-dup-c073-c076).",
    "E3-c074": "Round-2 duplicate fixed: the card no longer restates Example 2.5 (answer now cites section 4, third "
    "misconception, L04.html:500).",
    "E3-c075": "FOSD tally re-derived by an independent generator of the lab's documented draw (rederive.out): X 3, Y 10, "
    "identical 1, none 10; agreement 24 of 24 is the lab's own check (out/run_labs_L04.out).",
    "E3-c076": "SOSD tally re-derived (rederive.out): X 3, Y 2, identical 1, none 2 over 8 equal-mean pairs.",
    "E3-c071": "Problem R3 (L04.html:613) re-derived: I_X(s_m)=s_m - E X, so I_X(s_m)<=I_Y(s_m) gives E X >= E Y; the "
    "last-interval slope sigma_{m-1} >= 0 by monotonicity; the card's claim is correct.",
    "E3-c159": "Remark 1.4 (L02.html:130) states the hypotheses the proof uses (A2, F2, F1, A3); Proposition 1.3 is at L02.html:103 and its proof follows it. Agrees with the card.",
    "E3-c160": "The lab line 'certainty equivalent at gamma 1 +/- 1e-6 is within 0.01 cents of gamma 1: True' is printed "
    "by the twin (out/twin-L03-1.stdout, expected block at L03.html lab). The gamma = 1 value 10000 is independently "
    "re-derived (rederive.out, c054 checks). The +/- 1e-6 comparison itself was checked only by running the twin, not "
    "re-derived; the card claims only that it is a floating-point check, which the lab's own code shows.",
    "E3-c161": "Part B is a five-scale numerical check (L02.html Lab 1 at line 207 and Remark 3.2 at line 203). Card "
    "correct.",
    "E3-c162": "Remark 1.4 (L02.html:130): 'For a utility with u'' >= 0, Steps 1 to 3 hold with each inequality reversed.' "
    "Re-checked by hand: Step 1 reverses, Step 2 gives E u(X) >= u(m), Step 3 gives c >= m.",
    "E3-c168": "Remark 2.8 (L03.html:183). Bound |R(kv)-kR(v)| <= (k+1)/2 brute-forced over 200000 random draws "
    "(rederive.out: max excess 0).",
    "E3-c171": "Lab homogeneity line: k = 2, 3, 10 at the six gammas, unrounded relative error <= 1e-12 (out/twin-L03-1.stdout, "
    "'homogeneity ... True').",
    "E3-c173": "New card (L01 section 5 third misconception, L01.html:339). b = 0 gives E v(L) = a for every L (rederive.out).",
    "E3-c174": "New card. Assumption A5 at L02.html:167. The card paraphrases the lesson's own justification ('every "
    "small eps puts all of w + eps x_i in I' because I is open and X is finite).",
    "E3-c175": "New card. Assumptions A1 and A2 of L03 at L03.html:56: 'Module M1, Lesson 3 defines e as e^1 and does not "
    "derive this limit, so the lesson takes it as given.' Card correct.",
}

FAIL_CARDS: dict[str, tuple[str, str]] = {}  # none: every card row is PASS; duplicate defects are dup rows

DUP_FAIL = {
    "E3f-dup-c006-c015": (
        ["E3-c006", "E3-c015"],
        "Both cards assert the same result, E u(X) = b E X under a risk-neutral utility u(x)=bx: E3-c006 back "
        "'Its expected utility is b times the expected value (Definition 3.2)' (cards.json line of E3-c006), and "
        "E3-c015 back 'Under a risk-neutral utility the expected utility is b times the expected value ... "
        "(Definitions 1.2 and 3.2)'. Definition 3.2 is L01.html:142. The answer to E3-c015 is the answer to E3-c006.",
        "Rewrite E3-c015's back to the probability point only: 'No. The expected value in Definition 1.2 is a "
        "probability-weighted average of the outcomes, so the probabilities enter every expected utility (section 5, "
        "second misconception, L01.html:339).' Keep the b E X result only in E3-c006.",
    ),
    "E3f-dup-c039-c040": (
        ["E3-c039", "E3-c040"],
        "E3-c040 is the card whose answer is the Proposition 1.4 limit (ln w, L03.html:94). E3-c039's back restates "
        "that limit as 'Assuming A2, it gives a finite limit at gamma = 1 (Proposition 1.4)'. Its last clause also "
        "restates the Proposition 2.7 result that E3-c049 owns (changes no certainty equivalent). The question of "
        "E3-c039 ('why subtract 1') is answered by the constant and the derivatives alone.",
        "Delete from E3-c039's back the sentence 'Assuming A2, it gives a finite limit at gamma = 1 (Proposition 1.4).' "
        "and the clause 'and changes no certainty equivalent (Proposition 2.7)'. Keep the u_gamma(1)=0 reason and the "
        "unchanged derivatives and Arrow-Pratt measures.",
    ),
    "E3f-dup-c041-c051": (
        ["E3-c041", "E3-c051"],
        "E3-c041's back is the Proposition 1.7 result (r_A = gamma/w, r_R = gamma, L03.html:116). E3-c051's back "
        "restates the same two results ('what is constant is r_R = gamma (Proposition 1.7), and the absolute measure "
        "r_A = gamma/w falls ...') as the answer to a misconception.",
        "Replace E3-c051's back with: 'No. The utility changes with w, so the level of utility is not constant "
        "(section 4, first misconception, L03.html:341).' The Proposition 1.7 result stays on E3-c041 alone.",
    ),
    "E3f-dup-c054-c055": (
        ["E3-c054", "E3-c055"],
        "Both cards give the certainty equivalent of the Lab 1 lottery at gamma = 2. E3-c054 prints 8888.8889 among four "
        "values, and E3-c055 gives the same value exactly as 80000/9 (about 8888.89). The same number answers both "
        "questions.",
        "Remove the gamma = 2 entry from E3-c054's back and front (keep gamma = 0, 1 and 4: 11250, 10000, 7337.6161 "
        "cents). E3-c055 keeps the exact value.",
    ),
}

DUP_PASS = {
    "E3f-dup-c024-c042": "Round-2 FAIL resolved: E3-c042 is deleted from cards.json (no id E3-c042 in the slice; "
    "git diff c737272..a007712 shows the removal). Remaining E3-c024 is the definition only.",
    "E3f-dup-c040-c052": "Round-2 FAIL resolved: E3-c052 is rewritten to 'which member is affine in wealth' (gamma = 0). "
    "Its back no longer states the gamma -> 1 limit; the limit is owned by E3-c040 alone.",
    "E3f-dup-c068-c074": "Round-2 FAIL resolved: E3-c074's back now answers the misconception from the two tests' "
    "definitions (distribution functions vs integrals) and no longer restates Example 2.5; E3-c068 owns Example 2.5's "
    "first-order verdict.",
    "E3f-dup-c069-c072": "Round-2 FAIL resolved: E3-c069 is deleted from cards.json; E3-c072 owns the Example 2.6 "
    "misconception.",
    "E3f-dup-c026-c030": "Considered and passed: E3-c030 quotes the Example 2.3 values r_A=0.005, r_R=0.5 only as an "
    "example of the factor-w difference and of the unit difference; its question differs from E3-c026's. Noted, not a "
    "duplicate under the standard in notes.",
    "E3f-dup-c073-c076": "Considered and passed: the count 'no ranking 2 times' appears in E3-c073 as a supporting "
    "example and in E3-c076 as one entry of a tally; the questions differ (is SOSD a ranking of every pair vs do the "
    "verdicts agree). Noted, not a duplicate under the standard in notes.",
}

CMD_ROWS = [
    ("E3f-cmd-check-pages", "2.9-structure", "tools/check_pages.py --unit E3 (and --page L01): PASS",
     "ledgers/E3/scripts/E3-f-r3/out/check_pages.out, check_pages_L01.out"),
    ("E3f-cmd-check-dag", "2.9-dag", "tools/check_dag.py --unit E3: PASS (checks linked uses only; the unlinked out-of-closure name scan of L01-L04 and the cards was done by reading, and found only plain-prose uses such as 'convex utility' that the architect decision allows)",
     "ledgers/E3/scripts/E3-f-r3/out/check_dag.out"),
    ("E3f-cmd-run-labs-L01", "2.5-labs", "tools/run_labs.py --unit E3 --page L01: PASS (1/1); page code equals twin and expected block equals output",
     "ledgers/E3/scripts/E3-f-r3/out/run_labs_L01.out"),
    ("E3f-cmd-run-labs-L02", "2.5-labs", "tools/run_labs.py --unit E3 --page L02: PASS (1/1)", "ledgers/E3/scripts/E3-f-r3/out/run_labs_L02.out"),
    ("E3f-cmd-run-labs-L03", "2.5-labs", "tools/run_labs.py --unit E3 --page L03: PASS (1/1)", "ledgers/E3/scripts/E3-f-r3/out/run_labs_L03.out"),
    ("E3f-cmd-run-labs-L04", "2.5-labs", "tools/run_labs.py --unit E3 --page L04: PASS (1/1)", "ledgers/E3/scripts/E3-f-r3/out/run_labs_L04.out"),
    ("E3f-cmd-twins-python-I-W-error", "2.5-labs", "four twins (L01-1..L04-1) run as python -I -W error: exit 0 each, stderr 0 bytes",
     "ledgers/E3/scripts/E3-f-r3/out/twin-L01-1.exit .. twin-L04-1.exit, twin-*.stderr"),
    ("E3f-cmd-page-smoke", "2.9-structure", "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04: PASS (labs in Pyodide, 360 px, both themes)",
     "ledgers/E3/scripts/E3-f-r3/out/page_smoke.out"),
    ("E3f-cmd-rederive-cards", "2.7-cards", "independent re-derivation of every card number (48 checks, ALL CHECKS PASS), including the L04 seeded pairs regenerated from the lab's documented draw",
     "ledgers/E3/scripts/E3-f-r3/rederive_cards_L01_L04.py; out/rederive.out"),
    ("E3f-cmd-scan-cards", "2.7-duplicates", "duplicate scan of 85 slice cards (3570 pairs, no duplicate id) and card numeric tokens found in lesson (170 tokens; 1 present only as LaTeX)",
     "ledgers/E3/scripts/E3-f-r3/dup_scan.py; out/dup_scan.out; card_numbers_in_lesson.py; out/card_numbers.out"),
    ("E3f-cmd-locate-refs", "2.7-cards", "every lesson locator cited on a slice card resolved to L0x.html:line (4 cross-lesson or case-sensitive misses resolved by hand: L01.html:63, L01.html:147, L02.html:73, L02.html:167, L03.html:56)",
     "ledgers/E3/scripts/E3-f-r3/locate_card_refs.py; out/card_locators.out"),
    ("E3f-cmd-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline: 560 entries, 0 problems. The slice's cards cite no registry key (no cite field on any L01-L04 card)",
     "ledgers/E3/scripts/E3-f-r3/out/verify_refs_offline.out"),
    ("E3f-cmd-ruff-twins", "2.5-labs", "ruff check and ruff format --check on the four L01-L04 twins: All checks passed; 4 files already formatted",
     "ledgers/E3/scripts/E3-f-r3/out/ruff_check.out"),
    ("E3f-cmd-mypy-twins", "2.5-labs", "mypy --no-incremental on the four L01-L04 twins: Success, no issues in 4 source files",
     "ledgers/E3/scripts/E3-f-r3/out/mypy_twins.out"),
]


def card_line(cid: str) -> int:
    pat = re.compile(rf'"id": "{re.escape(cid)}"')
    for i, line in enumerate(lines, 1):
        if pat.search(line):
            return i
    raise SystemExit(f"card {cid} not found")


rows: list[dict[str, str]] = []
for c in cards:
    cid = c["id"]
    loc = LOC.get(cid, {"lesson": c["lesson"], "refs": []})
    refs = [f"{r['ref']} at {c['lesson']}.html:{r['line']}" for r in loc["refs"] if r.get("line")]
    ref_text = "; ".join(refs) if refs else "no lesson locator on the card; statement read against the whole lesson section"
    base = (
        f"cards.json:{card_line(cid)} ({cid}, {c['lesson']}) read in full. Front and back checked against "
        f"course/modules/E/E3/{c['lesson']}.html ({ref_text})."
    )
    extra = NOTES.get(cid, "Statement re-checked against the lesson text; no defect found.")
    rows.append(
        {
            "id": f"E3f-{cid}",
            "check": "2.7-cards",
            "location": f"cards.json:{card_line(cid)} ({cid}, {c['lesson']})",
            "status": "PASS",
            "evidence": f"{base} {extra}",
        }
    )

for rid, (ids, evidence, fix) in DUP_FAIL.items():
    rows.append(
        {
            "id": rid,
            "check": "2.7-duplicates",
            "location": f"cards.json ({', '.join(ids)})",
            "status": "FAIL",
            "evidence": evidence + " Duplicate standard applied: the same result asserted as the principal answer of two cards.",
            "fix": fix,
        }
    )
for rid, text in DUP_PASS.items():
    rows.append(
        {"id": rid, "check": "2.7-duplicates", "location": "cards.json (slice L01-L04)", "status": "PASS", "evidence": text}
    )
rows.append(
    {
        "id": "E3f-dup-scan-all",
        "check": "2.7-duplicates",
        "location": "cards.json (slice L01-L04, 85 cards)",
        "status": "PASS",
        "evidence": "dup_scan.py over all 3570 slice pairs: no duplicate id; the top-similarity pairs are templated 'What is assumption A..' "
        "fronts or the Example 2.5 / 2.6 pairs already passed above. Standard applied in every pair: a result asserted as the "
        "principal answer of two cards is a duplicate (E3f-dup-c006-c015, -c039-c040, -c041-c051, -c054-c055 FAIL).",
    }
)
rows.append(
    {
        "id": "E3f-coverage",
        "check": "2.7-cards",
        "location": "cards.json (slice L01-L04)",
        "status": "PASS",
        "evidence": "Slice = 85 cards (L01 18, L02 22, L03 23, L04 22 by lesson tag). Round 2 had 84: E3-c042 and E3-c069 are deleted; "
        "E3-c173, E3-c174, E3-c175 are new and all checked. No card of another lesson was checked against this slice.",
    }
)
rows.append(
    {
        "id": "E3f-grades",
        "check": "2.3-grades",
        "location": "cards.json (slice L01-L04; grade fields)",
        "status": "PASS",
        "evidence": "Every card with grade T is a proved result or a derivation on the page (Propositions, Lemmas, Theorems, "
        "Problem solutions, or hand computations). Every grade C card carries a basis that names the lab (E3-c016, c017, c032-c035, "
        "c054, c073, c075, c076, c160, c161, c171). No slice card states a graded result without a grade or basis (check_pages "
        "rule, check_pages.out).",
    }
)
rows.extend(
    {"id": cid, "check": chk, "location": "tools and ledgers/E3/scripts/E3-f-r3/", "status": "PASS", "evidence": f"{ev}; artefact {art}"}
    for cid, chk, ev, art in CMD_ROWS
)

# CMD_ROWS was already added above via the comprehension; de-duplicate ids defensively.
seen: set[str] = set()
unique_rows = []
for r in rows:
    if r["id"] in seen:
        raise SystemExit(f"duplicate row id {r['id']}")
    seen.add(r["id"])
    unique_rows.append(r)

verdict = "PASS" if all(r["status"] == "PASS" for r in unique_rows) else "FAIL"
counts = {s: sum(1 for r in unique_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}

fragment = {
    "unit": "E3",
    "slice": "f",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for E3 slice f, round 3 (did not build E3; retrieval cards of L01 to L04)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (a007712f, detached)",
    "base": "c737272f (round-2 pin, frags/D-E3-f.round2.json). Delta touching the slice, c737272f..a007712f (git diff --stat): course/modules/E/E3/cards.json (E3-c015, c024, c029, c030, c039, c051, c052, c074 edited; E3-c042 and E3-c069 deleted; E3-c173, c174, c175 added); L02.html (A4 wording, Step 1 to 3 notation, misconception 1, canon-break text); L03.html (why-it-matters, F1 wording); L04.html (A2 wording). L01.html unchanged. Every slice card was re-verified from scratch in this round; no round-2 PASS row is carried.",
    "checkout": str(ROOT),
    "scratch": "/Users/billyribeiro/.fanout/scratch/E3-f-r3",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": unique_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Duplicate standard (applied uniformly): a duplicate is a result asserted as the principal answer of two cards. Value overlap as a supporting example or a lab print of a worked example is not counted; those pairs are recorded as PASS rows with the reason.",
        "E3-c013 (which lottery maximizes EU): the back names one maximiser ('The lottery that pays, for certain...'). R1 shows the maximisers are all lotteries that put every unit of probability on outcomes attaining m. The card is correct; it does not say the maximiser is not unique. Optional wording fix for the builder, not a failure.",
        "E3-c039 (why subtract 1) carries the Proposition 2.7 result that E3-c049 owns; the fix in E3f-dup-c039-c040 removes it.",
        "E3-c174 and E3-c175 are assumption cards with no grade field; the lesson states no grade for an assumption, so this matches the page.",
    ],
    "summary": f"E3 slice f round 3: verdict {verdict}. {len(unique_rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
    "85 slice cards re-verified from scratch against L01-L04 text, the rederive script (48 numeric checks), the dup scan and the locator output. "
    "Non-PASS: four duplicate pairs (E3-c006/c015, c039/c040, c041/c051, c054/c055).",
}

path = SCR.parents[1] / "E3-f.json"  # ledgers/E3/E3-f.json
path.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {path} verdict={verdict} rows={len(unique_rows)} counts={counts}")
