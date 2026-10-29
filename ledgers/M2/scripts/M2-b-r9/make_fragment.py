import json, pathlib
R9 = "ledgers/M2/scripts/M2-b-r9"
def carry(files):
    return f"Carried from round 8 ({files} byte-identical since the previous pin ce7b382): "
RERUN = "Re-run round 9 at pin b6865c7: "
rows = []
def add(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

labs_cmd = ("tools/run_labs.py --unit M2 --page Lnn -> 'run_labs M2: PASS (1/1)'; "
            "isolated twin .venv/bin/python -I -W error tests/labs/M2/lab-M2-Lnn-1.py exit 0, stderr 0 bytes, stdout lines 43/17/22/26/10/21 for L07..L12 "
            f"({R9}/cmds.out); run_labs PASS also certifies page code equals twin and expected block equals output")
for n in ["07", "08", "09", "10", "11", "12"]:
    add(f"LAB-L{n}", "2.5 labs", f"course/modules/M/M2/L{n}.html lab section; tests/labs/M2/lab-M2-L{n}-1.py", "PASS",
        RERUN + labs_cmd.replace("Lnn", f"L{n}") + ". Lab twin unchanged since pin ce7b382 (no diff in tests/labs/M2)")

num = {
 "NUM-L07": ("course/modules/M/M2/L07.html lines 204-205, 271-279, 282-288, 157 (POINTS_A), 46", "L07.html byte-identical since ce7b382 (no diff)"),
 "NUM-L08": ("course/modules/M/M2/L08.html lines 165-169, 185-195, 208, lab part C table", "L08.html byte-identical since ce7b382"),
 "NUM-L09": ("course/modules/M/M2/L09.html lines 166-169, 202-210, 215-221, 88-93 (Remark 1.4)", "L09.html byte-identical since ce7b382"),
 "NUM-L10": ("course/modules/M/M2/L10.html line ~347 (Problem L10-E3 solution), lines 370-372", "L10.html byte-identical since ce7b382"),
 "NUM-L11": ("course/modules/M/M2/L11.html lines 300-330 (E1, E2, E3), Lab part A/B expected blocks", "L11.html changed since ce7b382 only at line 245 (git diff ce7b382 HEAD); cited lines byte-identical"),
 "NUM-L12": ("course/modules/M/M2/L12.html lines 164, 186, 190, 192-194, 296-330 (P1, E1-E3)", "L12.html byte-identical since ce7b382"),
}
for k, (loc, why) in num.items():
    old = [r for r in []]
    add(k, "numbers in prose vs unrounded values", loc, "PASS", carry(why) + "numbers re-derived in round 8 (ledgers/M2/scripts/M2-b-r8); labs re-run this round print the cited digits (" + R9 + "/cmds.out)")

math = {
 "MATH-L07": "course/modules/M/M2/L07.html Prop 1.4, Lemma 1.6, Prop 2.3, Lemma 3.1, Thm 3.2, ...",
 "MATH-L08": "course/modules/M/M2/L08.html Lemma 1.1, Thm 1.2, Thm 2.1 proof, Cor 2.2, Ex 2.3, ...",
 "MATH-L09": "course/modules/M/M2/L09.html Lemmas 1.1-1.2, Def 1.3, Thm 2.2 proof, Cor 2.3, Ex ...",
 "MATH-L10": "course/modules/M/M2/L10.html Thm 2.1 proof, Ex 2.2, Cor 3.1 (lines ~80-100), Pro...",
 "MATH-L11": "course/modules/M/M2/L11.html Example 3.3 integrability (line 134), Lemma 1.1, Cor 1.2, Thm 2.1 proof (lines 84-99)",
 "MATH-L12": "course/modules/M/M2/L12.html Lemma 2.1 proof (lines ~140-146), Problem L12-P1 solution, E1-E3",
}
for k, loc in math.items():
    n = k[-3:]
    why = "L11.html changed only at line 245 (outside the cited proof lines 84-134)" if n == "L11" else f"{n}.html byte-identical since ce7b382"
    add(k, "proofs and grades", loc, "PASS", carry(why) + "proof text re-read in round 8 and cited lines unchanged this round (git diff ce7b382 HEAD)")

add("PROSE-L09-monotone", "prose claims", "course/modules/M/M2/L09.html Remark 1.4 (lines ~45-47, 88-93)", "PASS",
    carry("L09.html") + "Remark 1.4 text unchanged; Theorem 2.2 is the monotone-integrability result it cites (L09.html line 99)")
add("ASSUME-L12-monotone-convergence", "named assumptions", "course/modules/M/M2/L12.html why-it-matters (line ~27), Problem L12-R3", "PASS",
    carry("L12.html") + "Assumption 2.2 wording unchanged")
add("SCOPE-L12-integer-exponents", "scope words", "course/modules/M/M2/L12.html Section 4 bullet 2 (~line 242), Remark 3.4 (~line 2xx)", "PASS",
    carry("L12.html") + "scope sentences unchanged")
add("NOTATION-L07-L12", "notation vs notation/notation.json", "course/modules/M/M2/L07-L12.html math spans; notation/notation.json", "PASS",
    carry("notation/notation.json and L07-L10, L12 html") + "the only changed line in L11 (line 245) introduces no new symbol; its symbols u', v, a, b, [0,b] already appear in the lesson")
add("DAG-L07-L12", "DAG and concept links", "tools/check_dag.py --unit M2; concept links in L07-L12", "PASS",
    RERUN + "tools/check_dag.py --unit M2 -> 'check_dag M2: PASS' (" + R9 + "/cmds.out)")
add("SMOKE-L07-L12", "page_smoke", "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12 (run alone)", "PASS",
    RERUN + "'page_smoke M2: PASS' and per-page PASS lines for L07..L12 (" + R9 + "/cmds.out)")
add("STRUCT-L07-L12", "headers, misconceptions, problem tiers", "L07-L12 html headers and sections", "PASS",
    carry("L07-L10, L12 html") + "L11 change is inside an existing <li> (line 245); no section/heading/tier markup altered (git diff ce7b382 HEAD)")
add("GRADE-L07-L12", "data-grade markers", "data-grade markers in L07-L12 bodies", "PASS",
    carry("L07-L10, L12 html") + "L11 diff contains no data-grade attribute change (git diff ce7b382 HEAD)")
add("CROSSREF-L07-L12", "lesson and theorem citations", "lesson-number and theorem-number citations in L07-L12", "PASS",
    RERUN + "L11 line 245 now cites only Corollary 1.2 (L11.html line 72) and Lesson 9 Theorem 2.2 (L09.html line 99); both exist. cards_check.py found no card number absent from its lesson (" + R9 + "/cards_check.out)")
add("BANNED-L07-L12", "BUILDER_RULES 1.3-1.4 phrase list and filler", "L07-L12 bodies", "PASS",
    carry("L07-L10, L12 html") + "the changed L11 sentence (line 245) was read in full and contains no phrase from the list or filler words")
add("CARDS-L07-L12", "cards.json for L07-L12", "course/modules/M/M2/cards.json: 105 cards with lesson L07..L12 (L07 22, L08 18, L09 18, L10 15, L11 16, L12 16)", "FAIL",
    RERUN + "cards_check.py: 105 slice cards, no duplicate ids or fronts, every cited Theorem/Lemma/Corollary/Proposition/Example/Remark/Problem/Definition/Assumption number appears in its lesson html. "
    "FAIL: card M2-c163 (L11, grade T, cards.json line ~1165) back still says 'The worked examples check it: polynomials on [0, b] with b > 0 (Corollary 1.2) and monotone functions (Lesson 9, Theorem 2.2) (Misconception 3).' "
    "Round 9 removed only the Lemma 1.1 clause. The integration-by-parts examples of Theorem 2.1 are Example 2.2 (u=x^2, v'=(1-x)^3) and Example 2.3 (u=x, v=x) at L11.html lines 96-104; both integrands are polynomials. The only monotone integrand in L11 is f=x in Example 3.3 (line 133-134), which checks Theorem 3.1 (substitution), not Theorem 2.1. "
    "Fix: delete 'and monotone functions (Lesson 9, Theorem 2.2)' from c163 back text. Duplicate-check also: c388 and c389 were removed in this delta with no duplicate front left behind.")
add("CLAIM-L11-each-application-checks", "claims about what the worked examples check", "course/modules/M/M2/L11.html line 245 (Misconception 3); quiz L11q7 (line 418-424) is consistent", "FAIL",
    "L11.html line 245 reads: 'The worked examples check it, using polynomials on [0, b] with b > 0 (Corollary 1.2), and monotone functions (Lesson 9, Theorem 2.2).' The sentence is about the integrability of u'v and uv' for Theorem 2.1. Only Examples 2.2 and 2.3 (lines 96-104) apply Theorem 2.1; both use polynomials. The monotone clause is false for integration by parts (it is Example 3.3, a substitution example, lines 133-134). "
    "The round-9 delta removed the Lemma 1.1 clause (git diff ce7b382 HEAD, L11.html line 245) but kept the false monotone clause that round 8 also failed on. "
    "Fix: remove ', and monotone functions (Lesson 9, Theorem 2.2)' from line 245 and the same clause from card M2-c163, or move the monotone reference to the substitution examples with the right theorem (Theorem 3.1).")

frag = {
 "unit": "M2", "slice": "b", "round": 9,
 "verifier": "independent Haiku verifier, M2 slice b (L07-L12 and lab twins), round 9; fresh context",
 "pin": "b6865c7d10020e31b9858a49edf751f4b814c031",
 "base": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089 (round-8 pin, fragment B-M2-b.round8.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB9-M2-b",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyB9-M2-b/ledgers/M2/scripts/M2-b-r9",
 "verified_at": "2026-10-28T00:00:00Z",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
   "Delta since round 8 touches M2 files: L11.html (line 245 only), cards.json (c163 changed; c388, c389 removed; c379 is lesson L05, outside slice). L13, L14, L16-L20, L24 changed too but are outside slice b.",
   "Lab twins L07-L12 and their expected blocks unchanged since ce7b382 (no diff under tests/labs/M2); lab twins are demonstrations, so no grader mutation is applied (ruling).",
   "62 cards in cards.json have no 'grade' key (e.g. M2-c075, M2-c165, M2-c180, in-slice M2-c075/076/081/082/097/115/116/120/133/165/180); not treated as a finding because the schema is not stated in this slice's contract; not checked further.",
   "Not checked: full line-by-line re-read of unchanged L07-L10 and L12 bodies (carried from round 8 on byte-identical subjects); banned-phrase scan rerun in full (only the changed L11 sentence was re-read)."
 ],
 "summary": "M2-b round 9 on pin b6865c7: 30 rows, 28 PASS, 2 FAIL (CLAIM-L11-each-application-checks and CARDS-L07-L12, same false monotone-integrability clause in L11 line 245 and card M2-c163). Round-9 delta fixed only the Lemma 1.1 clause; verdict FAIL."
}
out = pathlib.Path("ledgers/M2/M2-b.json")
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print(len(rows), sum(r["status"] == "PASS" for r in rows))
