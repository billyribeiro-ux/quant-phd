"""Build the CF1-c round-10 fragment from the round-9 fragment (read-only input) and this round's fresh evidence."""
import json
import sys

R9 = "/tmp/fanout-frags/CF1-c.round9.json"
OUT = "/tmp/verify10-CF1-c/ledgers/CF1/CF1-c.json"
PIN = "af08ad1e1458e56314bd70c2b82bd37b154e2beb"

PFX_LAB = ("Carried from round 9 (course/modules/CF/CF1/L05.html, course/modules/CF/CF1/L06.html, "
           "tests/labs/CF1/lab-CF1-L05-1.py and tests/labs/CF1/lab-CF1-L06-1.py byte-identical since the previous pin 96dd532; "
           "re-read in full in round 10):")
PFX_CARD = ("Carried from round 9 (the L05 and L06 card objects in course/modules/CF/CF1/cards.json byte-identical since the "
            "previous pin 96dd532; only card CF1-c012 of L01 changed):")
PFX_PROSE = ("Carried from round 9 (course/modules/CF/CF1/L05.html and L06.html byte-identical since the previous pin 96dd532; "
             "re-read in full in round 10):")

FRESH = {
 "CF1-c-lab-L05-hypothesis": (
  "Fresh in round 10: python -I -W error tests/labs/CF1/lab-CF1-L05-1.py exits 0 and its output equals the page pre.expected block "
  "(scripts/CF1-c-r10/l05.out, diffed). A simple 2.750 and discounted 3.469 for A; B simple 2.750, discounted none; D simple 2.000; "
  "NPV A 289367.40, B -96168.29, D -132231.40 (exact -132231.4050). Tails: 1 distinct simple and 1 distinct discounted payback in "
  "1000 draws. Hypothesis figures match. 'Proposition 3.1 gives a lower NPV for B' holds (B NPV below A NPV)."),
 "CF1-c-lab-L06-hypothesis": (
  "Fresh in round 10: python -I -W error tests/labs/CF1/lab-CF1-L06-1.py exits 0; output equals the page pre.expected block "
  "(scripts/CF1-c-r10/l06.out, diffed). Closed forms 79078.68 and 49379.84 recomputed (scripts/CF1-c-r10/recompute_r10.py). "
  "within_3se True at n = 100, 1000, 10000, 50000. Hypothesis figures match."),
 "CF1-c-num-L05-gap": (
  "Fresh in round 10 (scripts/CF1-c-r10/recompute_r10.py): 300000/1.1^4 + 200000/1.1^5 + 100000/1.1^6 = 385535.6942; lab npv gap "
  "385535.69; A and B NPVs 289367.3997 and -96168.2945. Gap/A = 1.332340, i.e. 133.2%. |gap|/|B| = 4.009, so the gap is larger "
  "than B's NPV in absolute value (line 219)."),
 "CF1-c-num-L05-E1-range": (
  "Fresh in round 10: 693692.91 - 121251.71 = 572441.20 cents = 5724.41 units. Undiscounted CUM for A: -1000000, -700000, -300000, "
  "+100000 at years 0-3, so tau_S = 3. Discounted cumulative for A: -96168.29 at year 3, +108735.74 at year 4, so tau_D = 4. "
  "Both paybacks read only years 0 to 4; the lab gives one value of each across the tails (1 distinct each)."),
 "CF1-c-num-L05-M2": (
  "Fresh in round 10: discounted terms 363.636, 330.579, 300.526, 273.205. Sum of the first three unrounded 994.7408, so the "
  "cumulative is -5.2592 (displayed terms 363.64 + 330.58 + 300.53 = 994.75, as the page says). After year 4: 267.946 (page 267.95). "
  "Payback 3 + 5.2592/273.2054 = 3.01925, i.e. 3.019. Without the fourth receipt the cumulative stays at -5.2592, so none."),
 "CF1-c-num-L05-M1-M3": (
  "Fresh in round 10: M1 CUM -1000, -600, -200, +200; payback 2 + 200/400 = 2.5. M3 CUM -500, -400, -200, +100; payback "
  "2 + 200/300 = 2.6667, i.e. 2.667 to three decimals (the exact value 2 + 2/3)."),
 "CF1-c-num-L06-closed-forms": (
  "Fresh in round 10 (scripts/CF1-c-r10/recompute_r10.py): m = 100001, Var(X) = (m^2-1)/12 = 833350000 (the round-9 fragment "
  "printed 8335000, a typo in that fragment; the page prints no variance). Expected NPV -300000 + 100000 x 3.7907868 = "
  "79078.677, printed 79078.68. sd = sqrt(833350000 x sum_t v_t^2) = 49379.8445, printed 49379.84. Matches Proposition 2.3 "
  "(line 96) and the hypothesis (line 111)."),
 "CF1-c-num-L06-E1-prob": (
  "Fresh in round 10: (84543.40 - 79078.68)/4400.22 = 1.241920, printed 1.2419 (lab +1.242). Two-sided normal tail "
  "2(1 - Phi(1.241920)) = 0.214266, printed 0.2143 (math.erf). The page labels the normal reading as untested (Remark 2.4, line 106)."),
 "CF1-c-num-L06-E2-band": (
  "Fresh in round 10: 0.0552 +/- 1.96 x 0.0010 = 0.05324 to 0.05716, printed 0.0532 to 0.0572 (line 320). The unrounded share is "
  "0.05522 and its se 0.00102, both printing as 0.0552 and 0.0010. The 1.96 multiplier is the normal reading of Remark 2.4, which the page says it does not test."),
 "CF1-c-num-L06-M2-M3": (
  "Fresh in round 10: 35/12 = 2.91667, printed 2.9167; sqrt(35/12) = 1.707825, printed 1.7078. M3: 1/1.1 + 1/1.21 = 1.735537; "
  "-100 + 50 x 1.735537 = -13.2231, printed -13.22."),
 "CF1-c-num-L06-19.9-22.4": (
  "Fresh in round 10: 4400.22/221.01 = 19.9096, printed 19.9; sqrt(500) = 22.3607, printed 22.4; sample sd 49419.62 / closed-form "
  "49379.84 = 1.000806, printed 1.0008. The lab does not compute the ratio from the closed-form sd, and the page says so (line 206)."),
 "CF1-c-num-L06-E3-width": (
  "Fresh in round 10: printed quantiles 143406.13 - 14896.62 = 128509.51 cents. Unrounded (lab code, scripts/CF1-c-r10/recompute_r10.py): "
  "143406.12657 - 14896.62306 = 128509.50351, printed 128509.50, as Section 3 (line 211) and misconception 2 state. 128509.51 / 100 = 1285.0951, "
  "printed 1285.10 units."),
 "CF1-c-cmd-pin": (
  "git rev-parse HEAD in /tmp/verify10-CF1-c = af08ad1e1458e56314bd70c2b82bd37b154e2beb (the round-10 pin)."),
 "CF1-c-cmd-check_pages": (
  "tools/check_pages.py --all: 'check_pages CF1: PASS' (and AC1, AC2, AC4, AP1 PASS); tools/check_pages.py --unit CF1 exit 0."),
 "CF1-c-cmd-check_dag": (
  "tools/check_dag.py --all: 'check_dag CF1: PASS' (AC1, AC2, AC4, AP1 PASS); tools/check_dag.py --unit CF1: 'check_dag CF1: PASS'."),
 "CF1-c-cmd-run_labs": (
  "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)'."),
 "CF1-c-cmd-page_smoke": (
  "tools/page_smoke.py --unit CF1 --pages L05 L06: rc 0; 'page_smoke modules/CF/CF1/L05.html: PASS', 'page_smoke modules/CF/CF1/L06.html: PASS', "
  "'page_smoke CF1: PASS'; lab runtimes 0.0 s and 0.3 s (scripts/CF1-c-r10/smoke.txt)."),
 "CF1-c-cmd-ruff-mypy-labs": (
  "ruff check and ruff format --check on the two twins: 'All checks passed!' and '2 files already formatted'; mypy --no-incremental on the twins: "
  "'Success: no issues found in 2 source files'."),
 "CF1-c-cmd-pytest-labs": (
  "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py: exit 0, 100% dots (scripts/CF1-c-r10/pytest.txt)."),
 "CF1-c-cmd-verify_refs": (
  "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', rc 0. tools/verify_refs.py --unit CF1: "
  "'live re-verification of CF1: 2 of 560 entries, 0 problems', rc 0 (scripts/CF1-c-r10/vr_offline.txt, vr_live.txt)."),
 "CF1-c-cmd-twin-vs-page": (
  "run_labs CF1 9/9 compares each page's data-run block to its twin; the diff of pre.expected against the fresh output is empty for "
  "L05 and L06 (scripts/CF1-c-r10/l05.out, l06.out). L05.html, L06.html and both twins are byte-identical to 96dd532 (git diff --quiet)."),
 "CF1-c-lab-L05-1-run": (
  "Fresh in round 10: python -I -W error tests/labs/CF1/lab-CF1-L05-1.py exits 0; output matches the page's expected block (diffed)."),
 "CF1-c-lab-L06-1-run": (
  "Fresh in round 10: python -I -W error tests/labs/CF1/lab-CF1-L06-1.py exits 0; output matches the page's expected block (diffed)."),
 "CF1-c-cards-duplicates": (
  "Fresh in round 10: cards.json holds 100 cards with 100 unique ids; no duplicate front and no duplicate back. Against 96dd532 the only "
  "changed card is CF1-c012 (L01), outside this slice."),
 "CF1-c-hours": (
  "Fresh in round 10: index.html data-hours-lessons=48 + data-hours-project=12 = 60 module hours; 12/60 = 20.0% (line 41). Six lessons x 8 h = 48; "
  "L05 and L06 data-hours=8 and eyebrows read 8 study hours. Consistent. Pace is not checked (architect ruling)."),
 "CF1-c-hub-L05-card-two-sided": (
  "FAIL, re-verified in round 10. The round-9 wording ('two-sided evidence on how firms use it') is gone. The hub card at "
  "course/modules/CF/CF1/index.html line 142 now promises that the card covers 'what the registered source on firm use does and does not establish'. "
  "The L05 page (course/modules/CF/CF1/L05.html) never says what that source establishes: the word 'establish' occurs only in the quiz prompt at line 444 "
  "('Does Lab 1 establish how often firms use payback?'). Section 4 (line 233) says only that Graham and Harvey (2001) is the registered source whose "
  "title names corporate finance practice, that the lesson states no finding from it, and that it quotes no passage. The card's 'does and does not' "
  "is therefore a claim the page does not make. The 'no finding stated' half is supported (L05 line 233; why-it-matters line 52)."),
}

FAIL_FIX = ("Change the clause in course/modules/CF/CF1/index.html line 142 to 'and why this lesson states no finding from the registered source on "
            "firm use'. Or add a paragraph to L05 Section 4 that states what graham2001theory's record shows (title, journal, year) and what it "
            "does not show, then keep the card's wording.")

r9 = json.load(open(R9))
rows = []
for r in r9["rows"]:
    rid = r["id"]
    if rid in FRESH:
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "FAIL" if rid == "CF1-c-hub-L05-card-two-sided" else "PASS",
               "evidence": FRESH[rid]}
        if row["status"] != "PASS":
            row["fix"] = FAIL_FIX
    else:
        pfx = PFX_CARD if r["check"] == "2.7-cards" and "cards.json" in r["location"] else PFX_PROSE
        if "lab" in r["id"] or r["check"] == "2.5-labs":
            pfx = PFX_LAB
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
               "evidence": f"{pfx} {r['evidence']}"}
        if r["status"] != "PASS":
            row["fix"] = FAIL_FIX
    rows.append(row)

ids_r9 = [r["id"] for r in r9["rows"]]
assert [r["id"] for r in rows] == ids_r9, "row ids must be kept in order"
assert set(FRESH) <= set(ids_r9)

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1

frag = {
    "unit": "CF1",
    "slice": "CF1-c",
    "round": 10,
    "verifier": "independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 10; did not build CF1; no shared context with builders or earlier verifiers",
    "pin": PIN,
    "base": "96dd532fbddddd97b5b8b497f17a8159e9fa4104",
    "checkout": "/tmp/verify10-CF1-c (detached worktree at af08ad1; .venv symlinked)",
    "scratch": "/tmp/cf1-v/CF1-c-r10",
    "verified_at": "2026-10-28T08:00:00+00:00",
    "verdict": "FAIL",
    "verdict_basis": "FAIL: one row, CF1-c-hub-L05-card-two-sided. The round-9 FAIL is fixed in wording, but the new hub card clause promises 'what the registered source on firm use does and does not establish', which L05 never states. All other rows are PASS: L05.html, L06.html and both twins are byte-identical to 96dd532 and were re-read in full; every command row was re-run.",
    "mutants": [],
    "registry_flags": ["glasserman2003monte: registry used_by is ['M8'] but CF1 L06 cites this key; used_by not updated (generated registry, not edited by the verifier). Not a row failure."],
    "freshness_flags": [],
    "notes": (
        "Delta: git diff --stat 96dd532 af08ad1 touches course/modules/CF/CF1/index.html (line 142 L05 card only), cards.json (card CF1-c012 of L01 only), "
        "L01.html, L02.html, project.html and grader/test_project.py (not this slice), and AC1 labs (not this slice). L05.html, L06.html and both twins are byte-identical. "
        "Carried rows carry the prefix; re-verified rows carry fresh evidence. Re-run in round 10: check_pages, check_dag, run_labs, page_smoke (L05 L06), pytest on the three test modules, "
        "ruff and mypy on the twins, verify_refs offline and live, both twins under python -I -W error, and an independent recomputation (scripts/CF1-c-r10/recompute_r10.py). "
        "Mutants: not required, since this is a lesson and lab slice, not a project slice. Alternative implementations: not applicable. "
        "Not checked: the Graham and Harvey (2001) article and the Glasserman (2003) book were not read (no publisher access attempted), so no passage-level claim is verified; "
        "the pages make none beyond the registry record. Hours were not failed on pace (architect ruling)."
    ),
    "summary": (
        f"CF1-c round 10: {len(rows)} rows (pass {counts['PASS']}, fail {counts['FAIL']}, unverifiable {counts['UNVERIFIABLE']}). "
        "One FAIL: the hub card for L05 (index.html line 142) promises what the registered source does and does not establish; L05 states only that no finding is taken from it. "
        "The round-9 wording problem is gone and every L05/L06 page row, command row and recomputed number holds."
    ),
}
frag["rows"] = rows
json.dump(frag, open(OUT, "w"), indent=2, ensure_ascii=False)
open(OUT, "a").write("\n")
print("rows", len(rows), counts, "verdict", frag["verdict"])
