# Builds ledgers/M2/M2-b.json for the closing delta (pin d9de2fe5, previous pin 2a805c83).
# Fresh rows cite this round's gate outputs; carried rows keep the base evidence under the carry prefix.
import datetime
import json
import re
import subprocess

ROOT = "/Users/billyribeiro/.fanout/wt/verifyH1-M2-b"
S = "ledgers/M2/scripts/M2-b-r1"
BASE_PIN = "2a805c831410ab77c38c227f7e121e8537193ce9"
PIN = "d9de2fe5eea982d14cd9f922a61676b847506fbc"
base = json.load(open("/Users/billyribeiro/.fanout/frags/G-M2-b.round1.json", encoding="utf-8"))
brows = {r["id"]: r for r in base["rows"]}

PAGES = "course/modules/M/M2/L07.html..L12.html, course/modules/M/M2/index.html, tests/labs/M2 twins, notation/notation.json, references/, ledgers/M2/mutants/"
CARRY = ("Carried from round 1 (" + PAGES + " byte-identical since the previous pin " + BASE_PIN[:8]
         + ", per git diff --name-only " + BASE_PIN[:8] + ".." + PIN[:8] + " over these paths: empty): ")
CARD_CARRY = ("Carried from round 1 (cards cited here byte-identical since the previous pin " + BASE_PIN[:8]
              + ", JSON object compare in " + S + "/closing_card_identity.out): ")

def strip_carry(ev):
    return re.sub(r"^Carried from round 1 \(.*?\): ", "", ev, flags=re.S)

def carry(rid, prefix=CARRY):
    r = brows[rid]
    return {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
            "evidence": prefix + strip_carry(r["evidence"])}

def fresh(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}

rows = []
rows.append(fresh("RUN-M2-CHECKS",
    brows["RUN-M2-CHECKS"]["check"],
    "tools/check_pages.py --unit M2; tools/check_dag.py --unit M2; tools/check_projects.py --unit M2; tools/run_labs.py --unit M2; tools/build_site.py --check",
    "Fresh at d9de2fe5: " + S + "/closing_check_pages_M2.out 'check_pages M2: PASS' exit 0; closing_check_dag_M2.out 'check_dag M2: PASS' exit 0; "
    "closing_check_projects_M2.out 'check_projects M2: PASS' exit 0; closing_run_labs_M2.out 'run_labs M2: PASS (27/27)' exit 0; "
    "closing_build_site_check.out 'site data current: 6 outputs' exit 0. Command record: " + S + "/closing_run_gates.sh. "
    "The --all variants of the base were not re-run (repo-wide; the delta touches no M2 gate input except cards.json, which check_pages --unit M2 covers)."))
rows.append(carry("LAB-GATES"))
rows.append(fresh("PAGE-SMOKE-L07-L12", brows["PAGE-SMOKE-L07-L12"]["check"],
    brows["PAGE-SMOKE-L07-L12"]["location"],
    "Fresh at d9de2fe5: " + S + "/closing_page_smoke_L07_L12.out 'page_smoke modules/M/M2/L12.html: PASS' and 'page_smoke M2: PASS' exit 0 (pages L07-L12)."))
rows.append(carry("TWIN-ISOLATED"))
rows.append(fresh("REFS-OFFLINE", brows["REFS-OFFLINE"]["check"], brows["REFS-OFFLINE"]["location"],
    "Fresh at d9de2fe5: " + S + "/closing_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' exit 0; "
    "closing_build_site_check.out 'site data current: 6 outputs' exit 0. The live unit check (tools/verify_refs.py --unit M2, base 'live re-verification of M2: 2 of 560 entries, 0 problems') is carried from round 1: " + PAGES.split(",")[2].strip() + " and references/ are byte-identical since " + BASE_PIN[:8] + "."))
rows.append(fresh("DELTA-HUNKS", brows["DELTA-HUNKS"]["check"].replace("e896b7a4..95f3f8cb", "2a805c83..d9de2fe5"),
    "course/modules/M/M2/cards.json (only slice subject changed); course/modules/M/M2/L07-L12.html and six twins unchanged",
    "git diff --name-status 2a805c83..d9de2fe5 over course/modules/M/M2, tests/labs/M2, notation, references, tools, tests, ledgers/M2/mutants: only 'M course/modules/M/M2/cards.json' for M2 (command output recorded in " + S + "/closing_delta.out). "
    "Out-of-slice changes (not graded here, ruling 30): tests/labs/CS2/lab-CS2-project-3.py, tests/labs/E3/lab-E3-L02-1.py, tests/labs/E5/lab-E5-project-3.py; in cards.json, M2-c216 (L14). "
    "cards.json: 395 -> 397 cards; 0 removed; added M2-c431 (L08) and M2-c432 (L10); changed in slice: M2-c107 (L08), M2-c161 (L11). All re-verified in the rows below."))
rows.append(carry("CARD-L07", CARD_CARRY))
rows.append(fresh("CARD-L08", brows["CARD-L08"]["check"], "course/modules/M/M2/cards.json: M2-c107 (changed), M2-c431 (added); other L08 cards carried",
    "Fresh at d9de2fe5 for the changed and added cards. M2-c107 (grade C, basis 'Lab 1, part C (sample rows)'): L08.html:231 prints 'part C: 0.90 1 0.535841 8.10000000 8.10000000' (lab twin tests/labs/M2/lab-M2-L08-1.py unchanged); "
    "the card's point xi = 1 - (1 - 0.90)^(1/(n+2)) at n = 1 is 0.535841 (closing_c107_check.out: xi = 0.5358411166); R_1(0.9) = 0.81/0.1 = 8.10000000 and the Lagrange form at that xi is 8.10000000 (abs diff 1.8e-15). "
    "M2-c431 (no grade field, which is allowed for ungraded restatements): front and back match L08.html:76-82 (Theorem 1.2 under Assumption 1.1, p < q, continuity on [p,q], differentiability on (p,q), phi(p) = phi(q) gives phi'(c) = 0 with p < c < q; 'the special case of the mean value theorem (Theorem 2.3 of Lesson 6)'; 'Its proof is Theorem 2.2 of Lesson 6'; 'not proved on this page'); "
    "Assumption 1.1 is at L08.html:61-62; every card number (0.535841, 8.10000000, Theorem 1.2, Remark 1.3, Assumption 1.1) appears in L08. "
    "Carried from round 1 for the other L08 cards (M2-c099, c102, c104, c111-c114, removed c417/c428; byte-identical since " + BASE_PIN[:8] + "): " + strip_carry(brows["CARD-L08"]["evidence"])))
rows.append(carry("CARD-L09", CARD_CARRY))
rows.append(fresh("CARD-L10", brows["CARD-L10"]["check"], "course/modules/M/M2/cards.json: M2-c432 (added); M2-c134, c143, c145-c147 carried",
    "Fresh at d9de2fe5 for the added card M2-c432 (lesson L10, no grade field): its front '(mean value theorem, Theorem 2.3 of Lesson 6)' matches L10.html:62; its back 'Assuming Assumption 2.1 of Lesson 6, let p < q. If phi is continuous on [p, q] and differentiable on (p, q), then there is c with p < c < q and phi(q) - phi(p) = phi'(c)(q - p)' matches L10.html:62-63; "
    "'This lesson does not reprove it (Remark 1.3)' matches L10.html:67-68; Assumption 2.1 of Lesson 6 is cited at L10.html:52 and 77. "
    "Carried from round 1 for M2-c134, c143, c145, c146, c147 (byte-identical since " + BASE_PIN[:8] + "): " + strip_carry(brows["CARD-L10"]["evidence"])))
rows.append(fresh("CARD-L11", brows["CARD-L11"]["check"], "course/modules/M/M2/cards.json: M2-c161 (changed, fixes the base FAIL); M2-c152, c162, c163 carried",
    "Fresh at d9de2fe5: M2-c161 back now begins 'Under Assumption 2.1 of Lesson 6, dropping it gives the integral of x from 0 to 1 equal to minus itself, which forces that integral to be 0.' The qualifier now precedes the claim. "
    "Checked against L11.html:104 (Example 2.3: 'Under Assumption 2.1 of Lesson 6, Theorem 2.1 applies to them. Then int_0^1 x dx = [x^2]_0^1 - int_0^1 x dx = 1 - int_0^1 x dx ... = 1/2'), L11.html:237 (Misconception 1: 'Dropping it would give int_0^1 x dx = -int_0^1 x dx, which is false'), L11.html:97 (Example 2.2: v(1) = 0 and u(0) = 0). "
    "The card's remaining sentences ('The integral is 1/2, so the boundary term 1 is needed'; 'vanishes in Example 2.2 because v(1) = 0 and u(0) = 0 (Misconception 1)') match those lines. M2-c160 is absent at both pins. c152, c162, c163 are byte-identical since 2a805c83 (carried)."))
rows.append(carry("CARD-L12", CARD_CARRY))
rows.append(fresh("CARD-DUP", brows["CARD-DUP"]["check"], "course/modules/M/M2/cards.json (all 397 cards at d9de2fe5)",
    "closing_card_dupes.out: 397 cards, 0 duplicate ids (check_pages M2 PASS, closing_check_pages_M2.out). Normalized duplicate fronts: only M2-c342/M2-c343 (L23, P'(y0) vs P''(y0) collapsed by normalization; out of slice, not a duplicate). "
    "Normalized duplicate backs: none. The new M2-c431 (L08 Rolle restatement) and M2-c432 (L10 MVT restatement) differ in front and back from L06 M2-c065 and M2-c066 (lesson-specific restatements, observation only)."))
rows.append(fresh("XREF-L07-L12", brows["XREF-L07-L12"]["check"], brows["XREF-L07-L12"]["location"],
    "Fresh at d9de2fe5 for the changed and added cards: M2-c107 (L08.html:52-82 for Remark 1.3 and Example 2.3 references; the Lab 1 part C reference resolves at L08.html:128-233); M2-c161 (L11.html:104 Example 2.3, L11.html:237 Misconception 1, L11.html:97 Example 2.2 all resolve); "
    "M2-c431 cites Assumption 1.1, Remark 1.3, Theorem 2.2 and Theorem 2.3 of Lesson 6 (all present: L08.html:61, 81-82; L06.html:77, 87); M2-c432 cites Assumption 2.1 and Theorem 2.3 of Lesson 6 and Remark 1.3 (L10.html:52, 62, 67; L06.html:72, 87). "
    "Other cross-references are carried (byte-identical cards, slice pages unchanged)."))
rows.append(carry("DAG-L07-L12", CARD_CARRY))
rows[-1]["evidence"] = ("Fresh check at d9de2fe5: " + S + "/closing_check_dag_M2.out 'check_dag M2: PASS' exit 0. Added cards M2-c431 and M2-c432 name only lesson-local or Lesson 6 results in prose and introduce no registered concept or concept link. "
    "Carried from round 1 for M2-c423 and M2-c425 (byte-identical since " + BASE_PIN[:8] + "): " + strip_carry(brows["DAG-L07-L12"]["evidence"]))
rows.append(fresh("PROSE-PROCESS", brows["PROSE-PROCESS"]["check"], "course/modules/M/M2/cards.json: M2-c107, M2-c161, M2-c431, M2-c432 (changed or added in this delta); other changed cards carried",
    "Regex scan (closing_prose_scan.out) of the front and back of M2-c107, M2-c161, M2-c431, M2-c432 for process words (now, previous, earlier, changed, revised, corrected, verifier, builder, round, draft, we, I, my, our, fixed, stale, ruling): no hits. "
    "The other 24 changed or added cards of the base delta are carried (byte-identical since 2a805c83)."))
rows.append(fresh("PROSE-BANNED", brows["PROSE-BANNED"]["check"], "course/modules/M/M2/cards.json: M2-c107, M2-c161, M2-c431, M2-c432; other cards carried",
    "Same closing_prose_scan.out scan for the BUILDER_RULES banned strings (TODO, TBD, lorem, ellipsis, for brevity, omitted, beyond the scope, left as an exercise, you can add, important to note, studies show, experts agree, well known, obviously, clearly, historically, roughly): no hits; no non-ASCII characters in the four cards."))
rows.append(carry("NOT-L09-R"))
rows.append(fresh("NOT-GLOBAL", brows["NOT-GLOBAL"]["check"], brows["NOT-GLOBAL"]["location"],
    "Fresh for the four changed or added cards: no notation.json symbol is used with a new meaning. notation/notation.json has no entry for xi, varphi, phi, c, p, q, x_0 or R_1 (grep over the symbols array; the registry's about text says local letters are defined per lesson), and none of the four cards uses T, Phi, gamma, R^*, R_f or Q. The slice pages and notation/notation.json are byte-identical since 2a805c83 (carried for the page-level symbols)."))
rows.append(carry("HOURS-L07-L12"))
rows.append(carry("GRADE-L07-L12"))
for rid in ["STRUCT-L07","NUM-L07","MATH-L07","LAB-L07","STRUCT-L08","NUM-L08","MATH-L08","LAB-L08","STRUCT-L09","NUM-L09","MATH-L09","LAB-L09",
            "STRUCT-L10","NUM-L10","MATH-L10","LAB-L10","STRUCT-L11","NUM-L11","MATH-L11","LAB-L11","STRUCT-L12","NUM-L12","MATH-L12","LAB-L12",
            "LAB-L07-DOC","LINK-L11-chain","PROOF-L11-hyp","PROOF-L12-integrability","QUIZ-L07-L12","MUTANTS-NA","KR-L10"]:
    rows.append(carry(rid))

ids = [r["id"] for r in rows]
assert sorted(ids) == sorted(brows.keys()), (set(brows) ^ set(ids))
assert all(r["status"] == "PASS" for r in rows)

frag = {
    "unit": "M2", "slice": "b", "round": 1,
    "verifier": "independent Haiku verifier, M2 slice b, closing delta round 1 (rulings 30, 37); fresh context, no builder context",
    "pin": PIN,
    "base": BASE_PIN + " (base fragment ~/.fanout/frags/G-M2-b.round1.json, verdict FAIL, 52 rows, FAIL CARD-L11); delta " + BASE_PIN[:8] + ".." + PIN[:8],
    "checkout": ROOT, "scratch": ROOT + "/" + S,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta (ruling 30): git diff 2a805c83..d9de2fe5 over the slice paths changes only course/modules/M/M2/cards.json for M2 (+15/-3 lines). Pages L07-L12, index.html, the six twins, notation/, references/, tools/, tests/labs/M2/ and ledgers/M2/mutants/ are byte-identical.",
        "Out-of-slice changes (not graded here): tests/labs/CS2/lab-CS2-project-3.py, tests/labs/E3/lab-E3-L02-1.py, tests/labs/E5/lab-E5-project-3.py; cards.json M2-c216 (L14) changed. Commits 2ec5d481 (rulings 38a, 40) and d9de2fe5 touch no M2 page, twin, notation, reference or tool file.",
        "Card delta: 395 -> 397 cards; changed M2-c107 (L08, lab number text), M2-c161 (L11, the base FAIL, now fixed), added M2-c431 (L08) and M2-c432 (L10); none removed.",
        "Observation (not a FAIL; ruling 26 kinds not met): M2-c107 defines xi by its closed form; with the printed 6-digit xi 0.535841 substituted, the Lagrange form gives 8.09999389 (closing_c107_check.out). The card's 'to eight decimal places' refers to the exact point, which is how the lab computes it (L08.html:231 prints 8.10000000 at the same settings).",
        "Observation (not a FAIL): M2-c431 and M2-c432 restate Rolle's and the mean value theorem of Lesson 6 (M2-c065, M2-c066) in the L08 and L10 notation; the fronts and backs differ, so they are not duplicates in the CARD-DUP sense.",
        "Observation: M2-c431 and M2-c432 carry no grade field (allowed by check_pages: 86 cards have none); the L08 and L10 Theorem 1.2 blocks are data-grade T on the pages, so the cards state the result without a grade, not with a higher one.",
        "Not re-run in this round: ruff and mypy (no Python file of the slice changed; the labs and twins are byte-identical), page_smoke --all, check_pages --all, check_dag --all, verify_refs --unit M2 (live). Their base outputs are carried.",
    ],
    "summary": "M2-b closing delta round 1 (pin d9de2fe5, previous pin 2a805c83): 52 rows; PASS 52, FAIL 0. The base FAIL CARD-L11 is fixed (M2-c161 now qualifies the first clause under Assumption 2.1). Changed or added cards M2-c107, c161, c431, c432 re-verified from scratch against their lessons and the lab output; the other rows carry under the carry prefix with byte-identical subjects.",
}
json.dump(frag, open(ROOT + "/ledgers/M2/M2-b.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(ROOT + "/ledgers/M2/M2-b.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "PASS", sum(r["status"] == "PASS" for r in rows))
