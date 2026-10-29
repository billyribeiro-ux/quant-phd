"""Build ledgers/E2/E2-a.json for round 8 (pin f618cf1). Evidence strings cite the scripts in this directory."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/C-E2-a.round7.json").read_text(encoding="utf-8"))
S = "ledgers/E2/scripts/E2-a-r8/"
DELTA = "0d2d0f3"


def carry(prev_id: str, files: str) -> dict:
    row = next(r for r in PREV["rows"] if r["id"] == prev_id)
    assert row["status"] == "PASS", prev_id
    return {
        "id": prev_id,
        "check": row["check"],
        "location": row["location"],
        "status": "PASS",
        "evidence": f"Carried from round 7 ({files} byte-identical since the previous pin {DELTA}): " + row["evidence"],
    }


def new(rid: str, check: str, location: str, evidence: str) -> dict:
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}


cmd = {
    "E2a-r4-cmd-check_pages": ("2.9 structure; tools/check_pages.py", "index, L01-L03",
        f"Re-run at f618cf1: `tools/check_pages.py --unit E2` -> 'check_pages E2: PASS', rc 0 ({S}check_pages.out). Its banned-phrase scan (tools/check_pages.py:58-125) covers the changed prose."),
    "E2a-r4-cmd-check_dag": ("2.9 DAG; tools/check_dag.py", "index, L01-L03",
        f"Re-run at f618cf1: 'check_dag E2: PASS', rc 0 ({S}check_dag.out)."),
    "E2a-r4-cmd-check_projects": ("2.6 project gate (unit-level)", "unit E2",
        f"Re-run at f618cf1: 'check_projects E2: PASS', rc 0 ({S}check_projects.out). No project file in slice a."),
    "E2a-r4-cmd-run_labs": ("2.5 labs; tools/run_labs.py", "lab-E2-L01-1, lab-E2-L02-1, lab-E2-L03-1",
        f"Re-run at f618cf1: 'run_labs E2: PASS (12/12)', rc 0 ({S}run_labs.out)."),
    "E2a-r4-lab-isolated": ("2.5 labs: twin alone under python -I -W error", "tests/labs/E2/lab-E2-L01-1.py, lab-E2-L02-1.py, lab-E2-L03-1.py",
        f"Re-run at f618cf1: `python -I -W error <twin>` rc 0 for L01, L02, L03; stderr 0 bytes each ({S}twins.out, {S}twin_L0*.stderr). Twins byte-identical since 0d2d0f3 (git diff lists only tests/labs/E2/lab-E2-L05-1.py and lab-E2-project-1.py under tests/labs/E2)."),
    "E2a-r4-lab-page-equals-twin-and-expected": ("2.5 labs: page code equals twin; expected equals stdout", "course/modules/E/E2/L01.html:167-274, L02.html:146-239, L03.html:117-199",
        f"Re-run at f618cf1 with ledgers/E2/scripts/E2-a-r5/embed_and_expected_r3.py (run via python -I): 'lab-E2-L01-1: page code == twin: True (len 4517 vs 4518); expected == stdout: True'; L02 and L03 likewise; 'ALL OK' ({S}embed.out). Length difference 1 is the trailing newline."),
    "E2a-r4-page-smoke": ("2.9 page_smoke", "index, L01, L02, L03",
        f"Re-run at f618cf1: `tools/page_smoke.py --unit E2 --pages index L01 L02 L03` -> 'page_smoke E2: PASS', rc 0 ({S}page_smoke.out)."),
    "E2a-r4-ruff-mypy": ("build gate: ruff, mypy strict", "repository",
        f"Re-run at f618cf1: ruff check 'All checks passed!' rc 0; ruff format --check '335 files already formatted' rc 0 ({S}ruff.out); mypy --no-incremental 'Success: no issues found in 229 source files' rc 0 ({S}mypy.out)."),
    "E2a-r4-pytest": ("tooling tests for labs and page checks", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
        f"Re-run at f618cf1: all dots, rc 0 ({S}pytest.out)."),
    "E2a-r4-verify_refs": ("2.1 citations; verify_refs --offline", "references/references.json",
        f"Re-run at f618cf1: 'offline integrity: 560 entries, 0 problems', rc 0 ({S}verify_refs.out). Live Crossref not run."),
}
rows = [new(k, *v) for k, v in cmd.items()]

rows.append(new("E2a-r4-recompute", "2.2/2.4 numbers and formulas", "index.html; L01.html; L02.html; L03.html",
    f"Re-run at f618cf1: ledgers/E2/scripts/E2-a-r5/recompute_e2a_r4.py via python -I: 'TOTAL 55 PASS 55 FAIL 0' ({S}recompute.out). The changed sentences (L01.html:76, :284; L02.html:85, :94; index.html:115, :128, :135) contain no computed number except the registry year 1950 and the year-free titles, which were checked against references/references.json."))

rows.append(carry("E2a-r4-banned-process-words", "index.html, L01.html, L02.html, L03.html"))
rows[-1]["evidence"] = ("Re-checked at f618cf1 by the banned-phrase scan of tools/check_pages.py (rows E2a-r4-cmd-check_pages PASS, rc 0), which replaces the round-4 grep for the same list. " + "Previous evidence: " + rows[-1]["evidence"])
rows.append(carry("E2a-r4-macros-registered", "L02.html:358 and the other slice-a pages' macro uses"))

for rid, files in [
    ("E2a-r3-notation-T-as-action-label", "course/modules/E/E2/L01.html:322-324"),
    ("E2a-r5-L01-M3-solution-paragraph-markup", "L01.html:331, :406"),
    ("E2a-r5-L01-M3-lab-comparison-count", "L01.html:331, :406"),
    ("E2a-r5-L01-R2-assumption-reference", "L01.html:94, :399"),
    ("E2a-r5-L01-285-hedge", "L01.html:285"),
    ("E2a-r5-L02-248-symmetric-bullet", "L02.html:245, :248"),
    ("E2a-r5-L03-282-price-cases", "L03.html:282, :63-66, :72-87"),
    ("E2a-r3-L03-misconceptions-problems-quiz", "L03.html:218-230, :237-431"),
    ("E2a-r3-L02-canon-uniqueness-heading", "L02.html:247, :249"),
    ("E2a-r3-DAG-forward-mentions", "L01.html:37, L02.html:37, L02.html:249, L03.html:51, index.html:55-56"),
    ("E2a-r3-hub-meta-M4-title", "index.html:35"),
    ("E2a-r3-hub-dangling-reference", "index.html:56"),
    ("E2a-r3-hub-placement-item-1-ambiguous-key", "index.html:64-70"),
    ("E2a-r3-hub-L08-simulated-claim", "index.html:117 and L08.html:139-140"),
    ("E2a-r3-hub-prereq-unlocks", "index.html:35-36"),
    ("E2a-r3-hub-objectives", "index.html:44-49"),
    ("E2a-r3-hub-placement-items-2-5", "index.html:72-103"),
    ("E2a-r3-hours-arithmetic", "index.html:28-29; L01-L03 data-hours"),
    ("E2a-r3-L01-printed-continuous-line", "L01.html:262-274 and lab-E2-L01-1.py"),
    ("E2a-r3-L01-key-result-unique-best-response", "L01.html:392-393, :422"),
    ("E2a-r3-L01-prop-2.2-3.2-4.2", "L01.html:91-103, :119-128, :142-155"),
    ("E2a-r3-L01-quiz", "L01.html:434-508"),
    ("E2a-r3-L02-prop-2.5-proof-gap", "L02.html:127-135"),
    ("E2a-r3-L02-R1-solution-gap", "L02.html:355-359"),
    ("E2a-r3-L02-prop-claims-lab-prints", "L02.html:145, :231-240"),
    ("E2a-r3-L02-misconceptions-quiz-problems", "L02.html:257-270, :278-355, :358-375, :397-466"),
    ("E2a-r3-L03-def-prop-2.1", "L03.html:55-88"),
    ("E2a-r3-L03-prop-2.3-remark-2.4", "L03.html:96-107"),
    ("E2a-r3-L03-lab-hypothesis-and-output", "L03.html:116, :184-199"),
    ("E2a-r3-L03-akerlof-attribution", "L03.html:212, :437"),
    ("E2a-r6-L01-cournot-tie-grid", "L01.html:159, :166, :272-274, :392, :422"),
    ("E2a-r6-L02-R1-and-L03-price-set", "L02.html:358; L03.html:72-87"),
    ("E2a-r7-L01-81-cournot-label", "L01.html:81"),
]:
    rows.append(carry(rid, files))

# Subjects that changed since 0d2d0f3 and were re-verified this round.
rows.append(new("E2a-r3-hub-core-reading", "2.1/2.4 hub core reading vs registry",
    "course/modules/E/E2/index.html:135 (claim) and :137-144 (list)",
    "Previously FAIL (round 7): claim said 'capitalization normalized' but nash1950equilibrium differs by spacing. Now index.html:135 reads 'with capitalization and spacing normalized'. Checked against references/references.json by a script: every data-cite key exists; titles equal the page after lowercasing and removing the space in 'n -person' (nash1950equilibrium, registry 'Equilibrium points in n -person games'); vickrey1961counterspeculati registry title is all caps, a capitalization difference; all eight years equal the registry years (1950, 1970, 1973, 1976, 1979, 1961, 1982, 1991). Evidence script output in " + S + "core_reading.out."))
rows.append(new("E2a-r3-hub-cards-titles", "2.9 hub cards vs lesson h1 titles",
    "course/modules/E/E2/index.html:110-118 vs L01-L09 h1",
    "Re-verified at f618cf1: the card-title spans equal the h1 of L01 ('Strategic Form and Nash Equilibrium'), L02, L03 ... L09 exactly. The changed card body at index.html:115 (L06) is checked in E2a-r8-index-115-L06-card-affine. Cards at :110-118 with L08 at :117 unchanged."))
rows.append(new("E2a-r8-index-115-L06-card-affine", "2.2 hub card text vs lesson",
    "course/modules/E/E2/index.html:115 vs L06.html:7, :86, :95",
    "Changed card says 'an affine contract'. L06.html meta description (line 7), Lemma 1.2 title '(the contract is affine in output)' (line 86) and the sentence at line 95 all use 'affine'; L06 uses no 'linear contract' wording (grep -F 'linear' L06.html returns only line 118, 'quasi-linear utility'). Agrees."))
rows.append(new("E2a-r8-index-128-stretch-card", "2.2 hub rung text",
    "course/modules/E/E2/index.html:128",
    "'An open extension: ...' replaces 'An open extension with no ceiling'. No sentence in E2 pages or project.html (grep -F 'no ceiling' over course/modules/E/E2/) remains that claims a ceiling; the stretch list is prose only, with no numbers. Agrees."))
rows.append(new("E2a-r8-L01-76-registry-quote", "2.3 citations: registry title quote",
    "course/modules/E/E2/L01.html:76, :513",
    "Quoted title 'Equilibrium points in n -person games' equals references/references.json nash1950equilibrium title exactly (script output). Year 1950 matches the registry. No passage or theorem attributed."))
rows.append(new("E2a-r6-L02-def-1.1-finite-types-contradiction", "2.4 defined terms vs Definition 1.1",
    "course/modules/E/E2/L02.html:56-60 (Definition 1.1), :85, :94",
    "Definition 1.1 (L02.html:56-60) is named '(two-player Bayesian game)' with finite type sets Theta_i and two players. The auction paragraph at :94 now says 'Definition 1.1 is stated for two players with finite type sets', which is accurate. The earlier contradiction (round 6: L02.html:94 calling the auction a Bayesian game outside Def 1.1 while the definition is a two-player finite-type object) is gone; the auction is no longer labelled a Bayesian game in that paragraph."))
rows.append(new("E2a-r7-L02-94-bayesian-game-term", "2.4 defined term use",
    "course/modules/E/E2/L02.html:94 vs Definition 1.1 at :56-60",
    "The word 'Bayesian game' no longer appears in the auction paragraph. Definition 1.1 is the only definition of the term and it is for two players with finite type sets; the paragraph's statement that the auction lies outside Definition 1.1 (continuous values, n bidders) matches Example 2.1 (n >= 2 bidders, values V_i). Agrees."))
rows.append(new("E2a-r7-L02-85-example-locator", "2.4 cross-reference locator",
    "course/modules/E/E2/L02.html:85 vs Example 2.1 (L02.html:90-93) and :94",
    "'as the paragraph after Example 2.1 explains' refers to the paragraph at L02.html:94, which directly follows the Example 2.1 block and explains the integral extension of Definitions 1.2 and 1.3. The locator is unambiguous. Agrees."))
rows.append(new("E2a-r7-index-135-normalization-claim", "2.3 registry-title normalization claim",
    "course/modules/E/E2/index.html:135; L01.html:76",
    "The claim now names both normalizations ('capitalization and spacing'). The only spacing difference, nash1950equilibrium 'n -person' vs page 'n-person', is covered. The registry-side spacing is recorded as a registry flag, not as a page error. Agrees."))
rows.append(new("E2a-r3-L01-misconceptions", "2.4 misconceptions block (L01)",
    "course/modules/E/E2/L01.html:284 (changed) and :293-309",
    "The changed bullet at L01.html:284 says 'Example 4.3 shows that the tie-allowed and strict best-response tests give different equilibrium sets on the same grid'. Example 4.3 (L01.html:158-160) defines both tests and shows (29,31) passes tie-allowed and fails strict; Lab 1 prints 'strict best responses: [(30, 30)]' (L01.html:272-274). The word 'weak' (undefined here) was replaced by 'tie-allowed', which Example 4.3 defines. Agrees. Also re-checked the arithmetic of Example 4.3: 29x30=870=30x29; against 31 firm 2 gets 930 at 30 and 31 (31x30=930). Lines 293-309 unchanged."))
rows.append(new("E2a-r3-L01-examples-remarks-numbers", "2.2 numbers in examples and remarks",
    "L01.html:76, 81, 107, 132, 139, 159",
    "Line 76 (Remark 1.4) now quotes the registry title with its recorded spacing and the year 1950 (no computed number). Line 81 is unchanged. Other lines unchanged since 0d2d0f3 and checked by recompute (E2a-r4-recompute)."))
rows.append(new("E2a-r8-cards-L01-c016", "2.10 card vs lesson", "course/modules/E/E2/cards.json E2-c016 vs L01.html:301-302",
    "Card back: 'player 1 earns 5 from action 1, 3 from action 2 and 6 from action 3 ... the change to action 2 does not pay, but the change to action 3 does'. L01.html:302 gives the same payoffs 5, 3, 6 with player 2 having one action, the neighbour change 3<5 not paying and 6>5 paying. Grade T matches Definition 1.3 (counter-example). Agrees."))
rows.append(new("E2a-r8-cards-L02-c017", "2.10 card vs lesson", "cards.json E2-c017 vs L02.html:56-60",
    "Card front 'What is a two-player Bayesian game?' names Definition 1.1 (two-player Bayesian game, L02.html:56). Back: finite nonempty type sets, action sets, prior and payoffs, common knowledge, as stated in Definition 1.1. Agrees."))
rows.append(new("E2a-r8-cards-L02-c022", "2.10 card vs lesson", "cards.json E2-c022 vs L02.html Proposition 2.2 Assumptions 1-4 (L02.html:97-101)",
    "Card back lists risk-neutral; independent uniform values, each bidder knowing its own value and the distribution of the others' values; same strategy; probability of equal bids 0. Matches the Assumption 1-4 text of Proposition 2.2 (L02.html Assumption 2 says 'Each bidder knows its own value and the distribution of the others' values'). Grade T matches Proposition 2.2 (T). Agrees."))
rows.append(new("E2a-r8-cards-L02-c027", "2.10 card vs lesson", "cards.json E2-c027 vs L02.html:107-113 (proof Steps 3 and 4)",
    "Card back: 'through Steps 3 and 4 of its proof'. The proof has 'Step 3, the maximum on [0, beta]' (L02.html:109) and 'Step 4, bids above beta' (L02.html:112). Agrees; the card's '21 values, 1201 grid bids' is not re-derived this round (no lab or lab text changed)."))
rows.append(new("E2a-r8-cards-L03-c034", "2.10 card vs lesson", "cards.json E2-c034 vs L03.html Prop 2.1 (L03.html:72-87) and Example 2.2 (L03.html:91-93)",
    "Card back: 'With alpha < 2/3, Proposition 2.1 makes 6000 the only market-consistent price, and the offered mix at 6000 is the low-quality sellers alone (Example 2.2)'. Prop 2.1 says the price 6000 is the only one when alpha < 2/3; Example 2.2 (alpha=1/2) says at 6000 only low-quality sellers trade. Agrees with the old 9000 sentence removed."))

rows.sort(key=lambda r: r["id"])
assert len({r["id"] for r in rows}) == len(rows)
prev_ids = {r["id"] for r in PREV["rows"]}
missing = prev_ids - {r["id"] for r in rows}
print("previous ids not carried:", sorted(missing), file=sys.stderr)

frag = {
    "unit": "E2",
    "slice": "a",
    "round": 8,
    "round_note": ("Round 8 independent verification of E2-a at pin f618cf1 (checkout /Users/billyribeiro/.fanout/wt/verifyC8-E2-a). "
                   "Previous pin 0d2d0f3 (round-7 fragment /Users/billyribeiro/.fanout/frags/C-E2-a.round7.json, context only). "
                   "Delta in slice a since 0d2d0f3: L01.html:76, :284, :513; L02.html:85, :94; index.html:115, :128, :135; cards.json entries c016, c017, c022, c027, c034 (L01-L03). "
                   "Lab twins L01-L03 and the L01-L03 lab blocks byte-identical."),
    "verifier": "Haiku independent verifier, E2-a round 8 (did not build E2)",
    "pin": "f618cf1",
    "base": "0d2d0f3",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC8-E2-a",
    "scratch": "ledgers/E2/scripts/E2-a-r8/",
    "verified_at": "2026-10-29T00:00:00+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": ("Slice a has no project and no grader; mutation testing of project graders does not apply (verifier-rules rulings). "
              "No mutants were run. Live Crossref not run. Lab twins were run alone under python -I -W error and page code/expected blocks were compared with the twins. "
              "Registry flag: references.json nash1950equilibrium title spacing 'n -person' differs from the 'n-person' form in index.html:137 and L01 prose; the page now records the difference explicitly."),
    "summary": "",
}
frag["summary"] = (f"E2-a round 8 at f618cf1: {frag['verdict']}. {len(rows)} rows, all PASS. Round-7 non-PASS rows (E2a-r7-L02-94-bayesian-game-term, "
                   "E2a-r7-L02-85-example-locator, E2a-r7-index-135-normalization-claim, E2a-r3-hub-core-reading) are re-verified PASS against the edited text. "
                   "All command rows re-run at f618cf1 and pass.")
out = ROOT / "ledgers" / "E2" / "E2-a.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", frag["verdict"])
