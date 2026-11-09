"""Assemble ledgers/E3/E3-e.json (round 1) from the generated rows, the metadata and the notes."""
import json
from datetime import UTC, datetime

rows = json.load(open("/tmp/e3e_r1/rows_out.json", encoding="utf-8"))
notes = [
    "Closing delta (ruling 30) of slice e, round 1, pin 2a805c83 (detached checkout /Users/billyribeiro/.fanout/wt/verifyG1-E3-e) against the round-18 base fragment (pin 4540351d, base fragment ~/.fanout/frags/D-E3-e.round18.json, verdict FAIL with 3 non-PASS rows). Delta = git diff 4540351d..2a805c83 over course/modules/E/E3: L03.html (Proposition 1.2 and its proof: b renamed Lambda; interpretation paragraph L03.html:326), L05.html (Remark 3.4 grade-table row L05.html:499; footer :620), L06.html (footer :545), L07.html (legend :47; registry claim :80; table row :463 deleted; footer :570), L08.html (legend :47; Definition 1.2 :67; Example 2.5 :133; Section 4 bullet :479; two table rows deleted; footer :723), cards.json (E3-c037 Lambda; E3-c134, c157, c158 lose grade and cite). plans/FINAL-ARCHITECT-RULINGS.md rulings 37-39 added. project.html:648 changed (outside slice, see observation 1).",
    "Rulings applied: 30 (delta closes the slice: every non-PASS base row and every row whose subject changed was re-verified; the rest carry the carry prefix with 'Carried from round 18'); 37 (no mutant authored this round; mutants is empty); 38 (Xi and Omega stay: E3e-r18-notation-ruling33-letters PASS; the L03 exponent rename is judged in E3e-r19-notation-Lambda); 39 (registry-title claims ungraded and cards aligned: E3e-r15-footers-registry-claim PASS; the footer wording that ruling 39 quotes is FAIL in E3e-r18-footers-L05-L06 and E3e-r19-footers-L07-L08). Ruling 26 kinds only; no new-defect hunting outside the rows (observations below are notes).",
    "Footer evidence (commands run this round): grep -c data-cite on L05.html, L06.html, L07.html, L08.html = 0 each; grep 'site-footer' on L01-L08.html shows 'Each graded result carries a proof or a lab result labelled C.' on L01-L04 and 'Every substantive claim carries an evidence grade and at least one citation key from the verified registry.' on L05-L08. Ruling 39 (plans/FINAL-ARCHITECT-RULINGS.md line 141-144) requires the first sentence on L05-L08.",
    "Proof presence (script over L07 and L08 claim spans): L07 has 2 T claims (Remark 1.3 at :71, Proposition 2.2 at :123), each followed by a Proof block; L08 has 4 T claims (Proposition 1.3 :71, Theorem 2.2 :98, Proposition 2.4 :117, Proposition 3.2 :148), each followed by a Proof block; L07 has one C-graded result (:462, lab-backed).",
    "Observation 1 (outside slice e, not judged, for the project slice owner): project.html:648 now states 'the memo text of Exemplar B is 608 words'. Recount (ledgers/E3/scripts/E3-e-r1/count_exemplars.py, output out/count_exemplars.out): Exemplar B memo text = 459 words whether tags are read as word breaks or removed; Exemplar A = 117 (matches the page). The pre-delta value 459 was right; the delta's 608 is a wrong number. The added parenthetical '(reading the block tags as word breaks gives the same count)' is then also a claim the count supports, but the number is wrong.",
    "Observation 2 (pre-existing, not in the delta): L01.html:46 and L02.html:46 legend still read 'C single study', while L03-L08 read 'C single study or lab result' and the footers of L01-L04 say 'labelled C'. L01 and L02 have no C-graded result, so no row fails; the legend wording is inconsistent across the unit.",
    "Observation 3 (stale record, same class as the base note on KNOWN-ISSUES): plans/KNOWN-ISSUES.md lines 25-28 still list W, a, tau and eta as open collisions; in the pages they are resolved (tau is Xi in L01, the affine constant is tilde u with phi and varsigma in L03). Not in the slice; not edited.",
    "Observation 4 (plan vs ruling): plans/E3-build-plan.md:273-275 and :333 say the Ellsberg and Gilboa records are cited 'by key only'. Ruling 39 supersedes this: the pages now cite no key for them, as ungraded naming sentences. The plan text should be updated by the architect; not a row.",
    "Judgment (affine b): L04.html:153-154 writes L(s) = b_0 + b_1 s + ..., with b_1 the slope of the piecewise-linear L; this is the affine coefficient meaning of b used in L01, L02, L07 (u = a + b x). L03.html:90 'with b = 1' cites the affine slope of L02 Proposition 2.2. One meaning for b across E3 (E3e-r18-notation-b PASS).",
    "Judgment (Lambda): E3e-r19-notation-Lambda is FAIL under ruling 38's wording 'absent in E3 in either case'. If the architect accepts glyph-level distinctness for Lambda as ruling 38 does for Xi and Omega, that row is PASS and nothing else changes.",
    "Judgment (Remark 3.4 row): E3e-r19-L05-remark34-row is LOW (wording), graded T; the fix is a one-phrase qualifier. The Remark 3.4 proof itself (L05.html:157) is correct: r^gamma = r^(1/psi) for r = c1/c0 != 1 forces gamma = 1/psi; off that case the MRS differ at every plan with c1 != c0; on the diagonal both equal (1-beta)/beta.",
    "Not checked: run_graders and mutate_graders (slice e has no grader and no grader mutants; project slices only); ruff and mypy on the twins (twins byte-identical to 4540351d, carried from round 18 with its ruff and mypy output); live verify_refs and live Crossref (references byte-identical, not re-run online); the full pytest suite (relevant subset only, 474 passed); the page_smoke figure sweep (skipped, E3 has no live figure); project.html and the grader were not judged (outside slice e per the base fragment); the T-grade proofs not touched by the delta were not re-read (carried per row).",
    "Mutants: none authored (ruling 37). Slice e has no grader; the mutation rule does not apply to it.",
]
frag = {
    "unit": "E3",
    "slice": "e",
    "round": 1,
    "verifier": "Haiku independent verifier, E3-e round 1 closing delta (did not build E3)",
    "pin": "2a805c83 (detached checkout /Users/billyribeiro/.fanout/wt/verifyG1-E3-e)",
    "base": "4540351d (round-18 base fragment ~/.fanout/frags/D-E3-e.round18.json, verdict FAIL with 3 non-PASS rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-E3-e",
    "scratch": "/tmp/e3e_r1/",
    "verified_at": datetime.now(UTC).strftime("%Y-%m-%d"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
                "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0,
                "mutants": 0, "mutants_killed": 0},
}
json.dump(frag, open("ledgers/E3/E3-e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(frag["summary"])
