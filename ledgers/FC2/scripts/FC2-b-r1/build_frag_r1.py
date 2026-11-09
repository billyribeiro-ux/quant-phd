import json, sys

BASE = "/Users/billyribeiro/.fanout/frags/S-FC2-b.round9.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyG1-FC2-b/ledgers/FC2/FC2-b.json"
base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

CARRY = ("Carried from round 9 (base fragment S-FC2-b.round9, pin 95f3f8cb; course/modules/FC/FC2/L04.html "
         "(only line 84 changed in 95f3f8cb..2a805c83, cited lines unchanged), cards.json (only c179, c192, c201 "
         "changed; cited card objects unchanged), L05.html, L06.html, tests/labs/FC2, notation/, references/, "
         "tools/, plans/FC2-build-plan.md, course/modules/FC/FC2/index.html byte-identical or unchanged in the "
         "subject): ")

# Rows re-verified from scratch this round: id -> (check, location, status, evidence)
fresh = {}
fresh["FC2b-cmd-check_pages"] = ("gate", "index, L01-L08, cards.json (unit gate)", "PASS",
  "Re-run r1 on pin 2a805c83: .venv/bin/python tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 "
  "(ledgers/FC2/scripts/FC2-b-r1/gates_r1.txt). cards.json and L04.html changed in this delta, so the gate is re-run.")
fresh["FC2b-cmd-check_dag"] = ("gate", "L04 link and dfn markup (L04.html:84 changed)", "PASS",
  "Re-run r1: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 (gates_r1.txt). The changed L04.html:84 "
  "and the three changed cards carry no concept-link markup (git diff 95f3f8cb..HEAD shows none).")
fresh["FC2b-cmd-check_projects"] = ("gate", "project.html (unit gate, outside slice)", "PASS",
  "Re-run r1: tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 (gates_r1.txt). "
  "git diff 95f3f8cb..2a805c83 shows no change to project.html or to FC2 grader files.")
fresh["FC2b-cmd-run_labs"] = ("gate", "tests/labs/FC2 (unit)", "PASS",
  "Re-run r1: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)', exit 0 (gates_r1.txt). The per-page "
  "run_labs results (L04, L05, L06 1/1 each) are carried from round 9 because tests/labs/FC2 is unchanged in the delta.")
fresh["FC2b-cmd-page_smoke"] = ("gate", "L04.html (changed line 84), L05.html, L06.html (each run alone)", "PASS",
  "Re-run r1: tools/page_smoke.py --unit FC2 --pages L04 -> 'page_smoke modules/FC/FC2/L04.html: PASS' and "
  "'page_smoke FC2: PASS'; then --pages L05 and --pages L06 each alone, same PASS lines (gates_r1.txt).")
fresh["FC2b-cmd-mutate-standing"] = ("mutation", "tools/mutate_graders.py --unit FC2 (standing set, ruling 37)", "PASS",
  "Re-run r1 (ruling 37, standing set only, no new mutants written): 'mutate_graders FC2: PASS (111/111 killed)' "
  "(gates_r1.txt). The FC2 grader is unchanged in the delta.")
fresh["FC2b-cards-near-duplicate"] = ("cards", "cards.json FC2-c051 (line 329) and FC2-c192 (line 1250)", "PASS",
  "Base FAIL resolved. FC2-c192 back is now 'The number K > 0 that the payoffs of Definition 1.1 are measured from "
  "(Definition 1.1).' Re-run r1 with ledgers/FC2/scripts/FC2-b-r1/dup_r1.py (difflib, threshold 0.6 on front or back, "
  "pairs with a slice card): c051/c192 is no longer listed; front ratio 0.37, back ratio 0.48 (dup_r1.txt). The pairs "
  "still listed that touch a slice card (c051/c202 back 0.63, c192/c193 and c192/c195 front 0.86 and 0.72, others) "
  "share a template but test different facts: c202 asks forward payoffs, c193 and c195 are premium and intrinsic "
  "value. Neither is a duplicate fact, and none is an exact duplicate.")
fresh["FC2b-cards-c201"] = ("cards", "cards.json FC2-c201 (line 1286; L05, grade T) vs L05.html:63-67 (Theorem 1.2, proof) and L04.html:60-62, 76-78 (A1, A3, Lemma 1.2)", "PASS",
  "Base FAIL (missing hypothesis) resolved. Current front 'Under A1 to A5, why is C − P − S + DK = 0 (Theorem 1.2)?'; "
  "Theorem 1.2 (L05.html:63-64) is stated under A1, A2, A3, A4 and A5, so the front carries the hypotheses. Back 'The "
  "portfolio has zero payoff in every state, by A1, A2, A4, A5 and Lemma 1.2 of Lesson 4. A3 then excludes a negative "
  "initial value, and a positive one through the portfolio −X, so the value is zero (Theorem 1.2).' Checked against the "
  "proof at L05.html:67: lent cash returns K by A4 and A2; the short share costs S_τ by A1 and A2; payoffs by Definition "
  "1.1 of L04; zero sum by Lemma 1.2 of L04 (L04.html:76-78). A3 at L04.html:62 (V0 ≤ 0 with non-negative payoff implies "
  "V0 = 0): applied to X when V0 < 0 and to −X when V0 > 0, as the back says. Grade T matches the Theorem's data-grade "
  "T at L05.html:63 with its proof on the page. Its only numerals are the labels A1 to A5, Lemma 1.2 and Theorem 1.2, all present in the lesson. Unique "
  "front and back (cards_r1.txt). No duplicate: front/back ratios against c197 are 0.25 and 0.23 (dup_r1.txt scan).")
fresh["FC2b-cards-c192"] = ("card-vs-lesson", "cards.json FC2-c192 (line 1250, ungraded) vs L04.html:69-71 (Definition 1.1)", "PASS",
  "Card changed in this delta (back only). New back 'The number K > 0 that the payoffs of Definition 1.1 are measured "
  "from (Definition 1.1).' Definition 1.1 (L04.html:70) sets K > 0 as the strike and defines the payoffs in terms of K, "
  "so the card states the lesson's definition and nothing more. Definitional, ungraded, one fact. Unique id and "
  "text (cards_r1.txt).")
fresh["FC2b-cards-c197"] = ("cards", "cards.json FC2-c197 (line 1280, ungraded) vs L05.html:59 (Definition 1.1 text)", "PASS",
  "FC2-c197 is not in the delta (git diff 95f3f8cb..2a805c83 shows c179, c192, c201 only). Re-read: back 'C − P − S + "
  "DK, the initial cost of the parity portfolio in the proof of Theorem 1.2 (Definition 1.1).' L05.html:59 says 'The "
  "difference C − P − S + DK is the initial cost of the parity portfolio in the proof of Theorem 1.2, and Lab 1 calls it "
  "the parity cost.' No theorem result is stated, so no hypothesis is owed. The earlier pointer to c201 is obsolete; "
  "c201 now passes (row FC2b-cards-c201).")
fresh["FC2b-cards-c179-scope"] = ("card-grade-scope", "cards.json FC2-c179 (line 1166, grade T) vs L04.html:84 (Remark 1.3) and L04.html:76-78 (Lemma 1.2)", "PASS",
  "Card and lesson both changed in this delta. New front 'Does a long call combined with a short put, with the same "
  "strike and expiry, pay the same as buying the underlying at the strike at expiry?' New back 'Yes. At expiry they pay "
  "(S_τ − K)^+ − (K − S_τ)^+ = S_τ − K, the payoff of buying the underlying at the strike at expiry (Lemma 1.2; Remark "
  "1.3). The identity concerns payoffs and says nothing about what the two options cost.' L04.html:84 now reads 'A long "
  "call and a short put ... pay S_τ − K at expiry, which is the payoff of buying the underlying at the strike K at "
  "expiry ... The identity concerns payoffs. It does not say what the two options cost.' The payoff identity is Lemma "
  "1.2 (T, L04.html:76). Net convention: buying at K and receiving S_τ nets S_τ − K, the same net payoff as the lemma. "
  "The grade T and the card's scope match the lemma's data-grade T.")
fresh["FC2b-delta-L04-remark-1.3"] = ("prose", "L04.html:83-85 (Remark 1.3; text at line 84), changed in 95f3f8cb..2a805c83", "PASS",
  "Re-read the changed text (git diff 95f3f8cb..2a805c83, one line). Old: '...which is the payoff of a long forward on the "
  "underlying.' New: '...which is the payoff of buying the underlying at the strike K at expiry.' The claim is the same "
  "payoff identity as Lemma 1.2, net of the strike. The old word 'forward' is removed from the remark, but it survives "
  "in the quiz explanation (see FC2b-quiz-L04-L06). Remark 1.3 is not a graded claim (no data-grade on L04.html:83-85). "
  "No scope word added.")
fresh["FC2b-math-L04-s1-s2"] = ("math", "L04.html:57-112 (A1-A5, Def 1.1, Lemma 1.2, Def 2.1, Prop 2.2, Prop 2.3, Remark 2.4); Remark 1.3 at line 84 re-read", "PASS",
  "Subject lines 84 (Remark 1.3, changed this delta) and 99, 120, 248, 250, 317, 421 (changed in earlier deltas) are "
  "re-read. Lemma 1.2 proof (L04.html:76-80) is unchanged and correct by case split. Remark 1.3 at line 84 claims only "
  "the identity and its reading as a net payoff, which Lemma 1.2 gives. A1-A5 (L04.html:59-64), Def 1.1, Def 2.1, Prop "
  "2.2, Prop 2.3 and Remark 2.4 are carried from round 9, byte-identical in the cited lines.")
fresh["FC2b-cards-key-mirror"] = ("card-vs-table", "L04.html:386-390 key-results table vs cards c179, c062", "PASS",
  "Re-verified r1. The key-results table row 'For every real s, (s − K)^+ − (K − s)^+ = s − K (Lemma 1.2)' carries grade "
  "T. Card FC2-c179 (T), changed this delta, mirrors it with the same grade and the same basis (Lemma 1.2; Remark 1.3). "
  "The table is byte-identical in the delta. No other table row is mirrored by a changed card.")
fresh["FC2b-cards-L04-grades"] = ("cards", "cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c179, c205 (L04)", "PASS",
  "Re-verified r1 with cards_r1.txt. c179 (T, basis Lemma 1.2 T at L04.html:76) changed text only; its grade and basis are "
  "unchanged. c051 and c205 are ungraded definitional cards (c205 matches L04.html:70). Grade distribution now T 112, C "
  "13, ungraded 69, unchanged by the delta (no card added or removed).")
fresh["FC2b-cards-L04-rest"] = ("cards", "cards.json L04 cards without grade (c051, c053, c142, c143, c158, c159, c187, c192-c196, c205)", "PASS",
  "Re-verified r1: c192 (changed) is a definition restatement of Definition 1.1 (K > 0). The other ungraded L04 cards "
  "are definitional, assumption restatements or the in-the-money card, as in round 9. The c051/c192 overlap that round 9 "
  "flagged is resolved (row FC2b-cards-near-duplicate).")
fresh["FC2b-cards-duplicates"] = ("cards", "cards.json whole deck (194 cards)", "PASS",
  "Re-run r1 with ledgers/FC2/scripts/FC2-b-r1/cards_r1.py: total 194, ids unique, dup fronts [], dup backs [] after "
  "normalisation, keys consistent (cards_r1.txt). Ids have gaps (pre-existing); ruling 2 says gaps are not defects.")
fresh["FC2b-cards-coverage"] = ("cards", "cards.json lessons L01-L08", "PASS",
  "Re-run r1 (cards_r1.txt): per-lesson counts L01 22, L02 24, L03 23, L04 25, L05 27, L06 31, L07 24, L08 18 (total 194). "
  "Every lesson has at least one card. The delta changes text only (c179, c192, c201), so counts match round 9.")
fresh["FC2b-cards-grade-ruling9"] = ("cards", "cards.json grades for L04-L06", "PASS",
  "Re-run r1 (cards_r1.txt): C cards are FC2-c046, c049, c050, c058, c061, c072, c073, c074, c079, c095, c148, c155, c171; "
  "every C card has a basis (script prints no 'C without basis'). The T cards in L04-L06 include c179 (changed, T with "
  "Lemma 1.2 basis) and c201 (changed, T with Theorem 1.2 and its proof on the page). Ungraded definitional cards: c051, "
  "c192, c205, c206, c083. No derived result is left ungraded in L04-L06.")
fresh["FC2b-quiz-L04-L06"] = ("quiz", "L04.html:396-468 (9 items; explanation at line 463 for the Lemma 1.2 item), L05.html:464-535 (9 items), L06.html:412-482 (10 items)", "PASS",
  "Re-counted r1: grep -c 'class=\"item\"' on L04.html gives 9. The q9 explanation at L04.html:463 reads 'Their difference "
  "is the payoff of a forward (Remark 1.3).' Remark 1.3 (L04.html:84) no longer uses the word forward, so the citation "
  "points to a remark that describes the same payoff in other words. The term 'forward' is defined in Lesson 2 "
  "(prerequisite), so it is not undefined. The statement is correct, so no ruling-26 kind applies. Observation only (LOW "
  "wording; suggested: 'the payoff of buying the underlying at the strike (Remark 1.3)'). L05 and L06 quiz counts are carried.")
fresh["FC2b-banned-process"] = ("prose", "L04-L06 visible prose, twin docstrings, and the changed text", "PASS",
  "Re-run r1: grep -n -i -E 'clearly|obviously|important to note|well known|can be shown|experts|studies show|left as an exercise|TODO|TBD|lorem|brevity|beyond the scope' over the delta's + lines (git diff 95f3f8cb..2a805c83 for course/modules/FC/FC2) returns no hit. The changed text (L04.html:84, c179, c192, c201) contains no process word.")
fresh["FC2b-scope-words"] = ("scope-words", "L04-L06 and the delta text", "PASS",
  "Re-run r1: scope words (only, every, any, all, never, always, exactly, same) in the + lines of the delta: L04.html:84 "
  "'with the same strike and expiry' (pre-existing wording, identity restated); c201 back 'zero payoff in every state' "
  "(computed in the proof, L05.html:67: payoff = (S−K) − S + K = 0 in every state); no other hit. Each is computed or "
  "pre-existing, so no new unsupported scope.")
fresh["FC2b-notation"] = ("notation", "L04-L06 math vs notation/notation.json (changed text only)", "PASS",
  "Re-verified r1 for the changed text: L04.html:84 uses S_τ, K; c179 uses S_τ, K, (·)^+; c201 uses C, P, S, D, K (with "
  "D = e^{−rτ} defined at L05.html:55 and used as DK); c192 uses K. Each symbol keeps its meaning. No new symbol, no reuse.")
fresh["FC2b-dag-links"] = ("dag", "L04-L06 concept links and definitions (changed text only)", "PASS",
  "Re-run r1: check_dag FC2 PASS (gates_r1.txt). The changed L04.html:84 and the changed cards c179, c192, c201 contain "
  "no concept-link markup (git diff inspection). c201 cites Lemma 1.2 of Lesson 4 by name, which is in the prerequisite "
  "closure (L05 requires L04).")

rows = []
for rid, r in base_rows.items():
    if rid in fresh:
        check, loc, status, ev = fresh[rid]
        rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
    else:
        ev = base_rows[rid]["evidence"]
        if base_rows[rid]["status"] != "PASS":
            raise SystemExit("non-PASS base row not re-verified: " + rid)
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + ev})

# every fresh id must exist in base (keep ids)
missing = [k for k in fresh if k not in base_rows]
assert not missing, missing

n_fresh = len(fresh)
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"

out = {
  "unit": "FC2",
  "slice": "b",
  "round": 1,
  "verifier": "Haiku independent verifier, FC2 slice b, round 1 (closing delta under ruling 30; did not build FC2)",
  "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
  "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (round-9 pin; base fragment S-FC2-b.round9.json, verdict FAIL with rows FC2b-cards-near-duplicate and FC2b-cards-c201). Delta 95f3f8cb..2a805c83 for the slice: course/modules/FC/FC2/L04.html line 84 (Remark 1.3 wording), cards.json c179, c192, c201. No change to tests/labs/FC2, notation/, references/, tools/, grader, project.html or plans/FC2-build-plan.md.",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-FC2-b",
  "scratch": "ledgers/FC2/scripts/FC2-b-r1/",
  "verified_at": "2026-11-09T17:03:45+00:00",
  "verdict": verdict,
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Scope (ruling 30): re-verified from scratch the two base non-PASS rows (FC2b-cards-c201 FAIL now PASS; FC2b-cards-near-duplicate FAIL now PASS) and every row whose subject changed in 95f3f8cb..2a805c83 (L04.html:84 and the rows citing it; cards c179, c192, c201; whole-deck card rows and gate rows touched by the cards edit). Every other row is carried with the carry prefix because its cited subject is byte-identical. No new defect was hunted outside those rows.",
    "Re-run gates (scripts in ledgers/FC2/scripts/FC2-b-r1/gates_r1.txt): check_pages FC2 PASS, check_dag FC2 PASS, check_projects FC2 PASS, run_labs FC2 11/11, page_smoke L04, L05, L06 each alone PASS, mutate_graders FC2 111/111 killed (standing set, no new mutants per ruling 37). Carried, not re-run: run_graders, run_labs per page, twins under python -I, ruff, mypy, pytest, verify_refs, because no FC2 twin, grader, tools/, references/ or notation/ file changed in the delta.",
    "Observation (not a FAIL under ruling 26, LOW wording): L04.html:463 quiz q9 explanation still reads 'the payoff of a forward (Remark 1.3)' while Remark 1.3 (L04.html:84) now says 'the payoff of buying the underlying at the strike K at expiry'. The statement is correct and 'forward' is a Lesson 2 term. Suggested later wording fix, to be listed in plans/KNOWN-ISSUES.md if deferred.",
    "Observation: the Remark 1.3 phrase 'buying the underlying at the strike K at expiry' is a net payoff (asset worth S_tau minus cash K), matching Lemma 1.2 and the card. It is not a gross payoff, and the page uses the net reading consistently.",
    "Not checked here: the cards outside the slice (c202, c203, c204, c207 and c016/c039 which the round-9 notes flagged) are not slice rows; the fixed-leg and floating-leg cards are not in this slice. Byte-level diff of the whole repo was not re-run; the slice diff was taken with git diff 95f3f8cb..2a805c83 over course/modules/FC/FC2, tests/labs/FC2, notation, references, tools, plans/FC2-build-plan.md, grader and project.html."
  ],
  "summary": {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "re_verified_this_round": n_fresh,
    "carried_rows": len(rows) - n_fresh,
    "mutants": 0
  }
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows", len(rows), counts, "fresh", n_fresh, "verdict", verdict)
