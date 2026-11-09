# Builds ledgers/E2/E2-d.json (round 1, closing delta on pin 95f3f8cb, base 33744e5 round-9 fragment).
# Base rows: re-verified rows get new evidence; all other base rows are carried with the carry prefix.
import json, datetime
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF11-E2-d"
base = json.load(open("/Users/billyribeiro/.fanout/frags/C-E2-d.round9.json"))
S = "ledgers/E2/scripts/E2-d-r1/"
P = "Carried from round 9 (course/modules/E/E2/project.html, course/modules/E/E2/grader/, tests/labs/E2/lab-E2-project-*.py and ledgers/E2/mutants/ byte-identical since the previous pin 33744e5; git diff 33744e5..HEAD over these paths shows only z01-z03 added): "
PC = "Carried from round 9 (course/modules/E/E2/project.html and course/modules/E/E2/grader/ byte-identical since the previous pin 33744e5; git diff 33744e5..HEAD shows no hunk there): "
PCARDS = "Carried from round 9 (cards.json entries {ids} byte-identical since the previous pin 33744e5; git diff 33744e5..HEAD -- course/modules/E/E2/cards.json has no hunk at these ids): "
CARD_CARRY_IDS = {
 "cards-sample-c010": "E2-c010", "cards-sample-c020": "E2-c020", "cards-sample-c030": "E2-c030",
 "cards-sample-c050": "E2-c050", "cards-sample-c070": "E2-c070", "cards-sample-c080": "E2-c080",
 "cards-sample-c100": "E2-c100", "cards-sample-c104": "E2-c104", "cards-sample-c110": "E2-c110",
 "cards-sample-c121": "E2-c121", "cards-changed-c022": "E2-c022", "cards-changed-c035-c037-c124": "E2-c035, E2-c037, E2-c124",
 "cards-changed-c051": "E2-c051", "cards-changed-c067": "E2-c067", "cards-changed-c080-c081": "E2-c080, E2-c081",
 "cards-changed-discrete-EM": "E2-c098, E2-c099, E2-c100, E2-c105", "cards-changed-c117": "E2-c117",
 "cards-changed-c016": "E2-c016", "cards-changed-c017": "E2-c017", "cards-changed-c027": "E2-c027",
 "cards-changed-c034": "E2-c034", "cards-changed-c061": "E2-c061", "cards-changed-c107": "E2-c107",
 "cards-changed-c002": "E2-c002", "cards-changed-c046": "E2-c046", "cards-changed-c114": "E2-c114",
 "cards-changed-c126": "E2-c126", "cards-changed-c127": "E2-c127",
}
PROJ_CARRY_IDS = [r["id"] for r in base["rows"] if r["id"].startswith("proj-") and r["id"] not in ("proj-process-words", "proj-grader-mutants-all")]
PROJ_CARRY_IDS += ["gate-run-graders", "gate-run-alternatives", "gate-labs-twins-isolated", "gate-page-smoke-project"]

new_evidence = {
 "gate-check-pages": ("PASS", f"check_pages.py --unit E2: 'check_pages E2: PASS' (exit 0), {S}check_pages.out"),
 "gate-check-dag": ("PASS", f"check_dag.py --unit E2: 'check_dag E2: PASS' (exit 0), {S}check_dag.out; L04-L06 text changed, links unchanged"),
 "gate-check-projects": ("PASS", f"check_projects.py --unit E2: 'check_projects E2: PASS' (exit 0), {S}check_projects.out"),
 "gate-mutate-graders": ("PASS", f"tools/mutate_graders.py --unit E2 re-run in full: 'mutate_graders E2: PASS (64/64 killed)', exit 0, {S}mutate_graders_E2_full.out; z01-z03 also re-run one by one with a direct pytest control ({S}control_z.out)"),
 "gate-run-labs-unit": ("PASS", f"run_labs.py --unit E2: 'run_labs E2: PASS (12/12)', exit 0, {S}run_labs_unit.out (L04-L06 pages changed)"),
 "gate-ruff": ("PASS", f"ruff check . : 'All checks passed!' exit 0; ruff format --check . : '555 files already formatted' exit 0; {S}ruff.out (repo-wide; mutants excluded by pyproject)"),
 "gate-mypy": ("PASS", f"mypy --no-incremental: 'Success: no issues found in 386 source files' exit 0, {S}mypy.out"),
 "gate-pytest-labs-E2": ("PASS", f"pytest -q -k E2: 16 passed exit 0 ({S}pytest_k_E2.out); tests/test_labs.py collects 15 E2 tests and test_fetch_data.py 1 by name match ({S}collect_k_E2.out)"),
 "proj-grader-mutants-all": ("PASS", f"ledgers/E2/mutants/*.py: full mutate_graders re-run 64/64 killed ({S}mutate_graders_E2_full.out). The 61 non-z mutants are byte-identical since 33744e5; z01-z03 added in the delta and killed by named tests ({S}control_z.out)"),
 "proj-process-words": ("PASS", f"project.html unchanged (carried). Scan of the 26 changed or new cards for process words ({S}process_words_cards.out): 3 hits, all mathematical ('fixed at 6000', 'Delta'); no process words in cards.json changed text"),
 "cards-structure": ("PASS", f"cards.json re-read whole file ({S}cards_structure.out): 135 cards, ids unique and sequential E2-c001..c135, every lesson file exists, grade in {{T,C}} or absent (38 ungraded, the check_pages convention), every C has basis, every cite key is in references/references.json (560 entries), no duplicate fronts; check_pages.py PASS"),
 "cards-structure-r9": ("PASS", f"same re-run as cards-structure ({S}cards_structure.out) on the current cards.json, 135 entries; check_pages.py --unit E2 PASS"),
 "cards-numbers-in-lesson": ("PASS", f"every number token in every card (665 tokens, all 135 cards) found with token boundaries in the card's own lesson HTML, after removing {{,}} thousands separators ({S}cards_numbers_bounded.out)"),
 "cards-sample-c040": ("PASS", f"E2-c040 (L03, C, basis Lab 3) changed: back now 'One price, 6000 cents, for each share from 0 to 0.6' matches Lab 3 output lines 188-194 (alpha 0..3/5 all [6000]); 0.7-0.9 moved to E2-c131 (see cards-changed-c040-c131). cards.json line 265"),
 "cards-sample-c060": ("PASS", "E2-c060 (L05, C, basis changed to 'Title, year and venue only') matches L05 section 4 text (L05.html line 254) and the registry record rothschild1976equilibrium (title, QJE 90(4), 1976; references/references.json)"),
 "cards-sample-c090": ("PASS", "E2-c090 (L07, C, basis Lab 1, Part C) matches L07.html Lab 1 Part C output lines 336-343 (induced_revenue_cents 6000; tie_break_declines_for_L_revenue_cents 4200) and Proposition 2.2 (L07 line 100)"),
 "cards-changed-c058-c063-c125": ("PASS", "E2-c058 and E2-c125 (L05) re-verified: q_L=2000, q_H=6000 from Remark 1.5 (L05.html line 124) and Lab output line 223-224; m_L=theta_L q_L=6,000,000 and m_H=theta_H q_H-(theta_H-theta_L) q_L=36,000,000-6,000,000=30,000,000 by hand (theta_L=3000, theta_H=6000); E2-c063 byte-identical, carried"),
 "cards-changed-c088": ("FAIL", "E2-c088 (L07, T) changed in its second sentence; its first sentence is unchanged from round 9 and omits Proposition 3.2's hypotheses: L07.html line 139-141 states Prop 3.2 'with v_H > 0 and Delta = v_H - v_L > 0' and defines c = p_L v_L - p_H Delta; the card states 'With c < 0 the optimum excludes type L (Proposition 3.2)' without v_H > 0, Delta > 0 or the definition of c. The second sentence (rent at least Delta q_L from Lemma 3.1, L07.html line 149) is correct, since U_H >= U_L + Delta q_L and U_L >= 0 hold for any Delta"),
 "cards-changed-c120": ("PASS", f"E2-c120 (L09, T) brute force over all 256 profiles ({S}bruteforce_l09_r1.out): equal-revenue profiles by common top-three bid w are w=0:1, 1:5, 2:9, 3:13 (= 4w+1), total 28; Part B counts 228/28/0 match L09 output lines 235-238; R1 proof L09.html line 397"),
 "cards-changed-c125": ("PASS", "E2-c125 (L05, T) changed: m_L and m_H formulas and values re-derived by hand (see cards-changed-c058-c063-c125); Prop 1.4 transfers at L05.html line 112 match"),
 "proj-reading-list": ("PASS", "Carried from round 9 (project.html Reading section and the E2-cited registry records byte-identical since 33744e5; references/references.json differs from 33744e5 only in used_by for bisndbasel, black1973pricing and reinhart2009this, none of them cited by E2 (checked by script {S}registry_e2_check.out))"),
}
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in new_evidence:
        st, ev = new_evidence[rid]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev}
    elif rid in CARD_CARRY_IDS:
        row = dict(r); row["evidence"] = PCARDS.format(ids=CARD_CARRY_IDS[rid]) + r["evidence"]; row["status"] = r["status"]
        assert r["status"] == "PASS", rid
    elif rid in PROJ_CARRY_IDS:
        row = dict(r); row["evidence"] = P + r["evidence"]
        assert r["status"] == "PASS", rid
    else:
        raise SystemExit(f"unclassified base row {rid}")
    rows.append(row)
base_ids = {r["id"] for r in base["rows"]}
known_base_ids = set(new_evidence) | set(CARD_CARRY_IDS) | set(PROJ_CARRY_IDS)
missing = sorted(base_ids - known_base_ids)
assert not missing, missing
extra = [
 ("gate-page-smoke-L04-L06", "2.9-page-smoke", "tools/page_smoke.py --unit E2 --pages L04 L05 L06", "PASS", f"page_smoke E2: PASS, exit 0 (labs of L04-L06 run inside page_smoke), {S}page_smoke_L04-L06.out"),
 ("gate-verify-refs-offline", "2.1-registry", "tools/verify_refs.py --offline", "PASS", f"'offline integrity: 560 entries, 0 problems', exit 0, {S}verify_refs_offline.out (references.json changed in used_by and generated_at only)"),
 ("gate-build-site-check", "2.9-generated", "tools/build_site.py --check", "PASS", f"'site data current: 6 outputs', exit 0, {S}build_site_check.out"),
 ("lesson-L04-assumption4", "2.4-math", "course/modules/E/E2/L04.html line 80 (Assumption 4) and Proposition 1.3 proof lines 84-100", "PASS", "New text: 'The proof of Proposition 1.3 uses c_H > 0 and c_L > 0, and it does not divide by Delta.' The proof uses c_L > 0 (low-type bound) and c_H > 0 (high-type bound) and divides only by c_L and c_H; Delta is never divided by. Claim true"),
 ("lesson-L06-prop1.3-and-lemma1.2", "2.4-math", "course/modules/E/E2/L06.html lines 98-104 (Proposition 1.3 statement and new proof sentence), line 63 (E_a definition), line 95 (Lemma 1.2)", "PASS", "Statement now defines profit as expected output E_a minus expected payment: matches the definition at line 63 (E_H = 750,000, E_L = 250,000). New proof sentence cites Lemma 1.2 (affine contract alpha + beta x, line 95) correctly. Numbers 600,000 and 50,000 unchanged and re-derived: (1-1/5)*750,000 = 600,000; 1/5*750,000 - 100,000 = 50,000"),
 ("lesson-L06-remark1.4", "2.4-math", "course/modules/E/E2/L06.html line 236 (Remark 1.4); Assumption 2 outside option at line 71", "PASS", "New wording: 'the agent's utility is at least the outside option 0 of Assumption 2, then binds, the expected payment is c_H, profit E_H - c_H = 650,000'. Assumption 2 outside option is 0 (line 71); 750,000 - 100,000 = 650,000. Claim true"),
 ("lesson-L05-L06-citation-wording", "2.9-prose", "course/modules/E/E2/L05.html line 296 (L05-r2 solution), course/modules/E/E2/L06.html line 292 (L06-r3 solution)", "PASS", "'cited by its title, year and venue only' matches L05.html line 254 and L06.html line 248 and the registry records spence1973job, rothschild1976equilibrium, holmstrom1979moral (titles, years, QJE 87(3), QJE 90(4), Bell J. 10(1))"),
 ("cards-changed-c012-c013-c128-c129", "2.7-cards", "course/modules/E/E2/cards.json E2-c012, E2-c013, E2-c128, E2-c129 (L01)", "PASS", f"Split of old c012/c013. Lab 1 output L01.html lines 262-274: prisoner's dilemma [('D','D')]; coordination [('a','a'),('b','b'),('c','c')]; grid ties-allowed [(29,31),(30,30),(31,29)] over 8281 pairs; strict [(30,30)]. Example 2.3 (L01 line 106) gives (D,D) as unique pure equilibrium. Grades C with basis Lab 1 exhaustive enumeration; each claim matches its printed line"),
 ("cards-changed-c025", "2.2-numbers", "course/modules/E/E2/cards.json E2-c025 (L02); L02.html lines 91, 102, 127-134", "PASS", "Expected winning bid (n-1)/(n+1): proof at L02.html line 133 (beta n integral x^n = (n-1)/(n+1), beta=(n-1)/n). Graded T, Proposition 2.5 (line 127-128). The n >= 2 hypothesis is the auction model's standing assumption (L02.html line 91 'There are n bidders, n >= 2'), so the card's model context carries it"),
 ("cards-new-c130", "2.7-hypotheses", "course/modules/E/E2/cards.json E2-c130 (L02, T, line 889-895); L02.html Proposition 2.5 line 128 ('Let n >= 2')", "FAIL", "Card: 'What is the mean of the second-highest of n independent uniform values on [0, 1]?' answers (n-1)/(n+1). The value is correct (density n(n-1)x^(n-2)(1-x), L02.html line 134) but the second-highest of n values exists only for n >= 2, and the front omits Proposition 2.5's hypothesis n >= 2 (the auction model's n >= 2 at line 91 is not in this standalone question). Missing hypothesis, a ruling-26 FAIL kind"),
 ("cards-changed-c040-c131", "2.7-cards", "course/modules/E/E2/cards.json E2-c040 (C), E2-c131 (C) (L03)", "PASS", f"Lab 3 output L03.html lines 188-198: alpha 0..3/5 -> [6000]; 0.7 -> [6000, 10200]; 0.8 -> [6000, 10800]; 0.9 -> [6000, 11400]; 1 -> [12000]. Lab tests 15001 whole-cent prices (line 187). Both cards match"),
 ("cards-changed-c047-c132", "2.2-numbers", "course/modules/E/E2/cards.json E2-c047 (T), E2-c132 (T) (L04); L04.html Remark 2.1 line 219 and Lab 1 Part B/D lines 195-211", "PASS", "t=2 smallest separating threshold (set {2,3,4} from Proposition 1.3). Education cost 2 x 500,000 = 1,000,000; net utility 6,000,000 - 1,000,000 = 5,000,000 (Remark 2.1). Lab 1 output line 209-211: least-cost 2, cost 1000000, utility 5000000. T grade is arithmetic on page inputs (y_H, c_H, y_L given at L04.html line 56)"),
 ("cards-changed-c048-c049", "2.7-cards", "course/modules/E/E2/cards.json E2-c048 (C), E2-c049 (T) (L04); L04.html lines 229, 235", "PASS", "c048 basis 'Title, year and venue only; no result attributed' matches L04.html line 229 and the spence1973job record. c049: Lab 1 Part B lines 198-206: t=1 'low type mimics' (low utility at e=1 is 6,000,000-1,000,000 = 5,000,000 vs 4,000,000 at e=0); t=5,6 best high utility 4,000,000 at e=0 ('high type prefers another signal'); t=0 'same signal'. Statement 'reveals the type only when t >= 1 and both incentive constraints hold' is definitional for a separating threshold profile (L04 Assumption 3 line 75 and Prop 1.3 line 85-89). Pass"),
 ("cards-changed-c060-c072", "2.7-cards", "course/modules/E/E2/cards.json E2-c060 (C, L05), E2-c072 (C, L06)", "PASS", "Basis 'Title, year and venue only; no result attributed' matches L05.html line 254 and L06.html line 248; cited keys rothschild1976equilibrium and holmstrom1979moral exist (references.json, title/year/container/volume/issue checked against the card text)"),
 ("cards-changed-c064-c133", "2.2-numbers", "course/modules/E/E2/cards.json E2-c064 (C), E2-c133 (C) (L05); L05.html Lab 1 output lines 199-207 and code lines 199-207", "PASS", "Part B: 'profit maximizing low-type quantity on the grid: 2000' (L05 line 233). Part C: 'profit maximizing high-type quantity on the grid: 6000' (line 236) on the grid 0..12000 step 1000 with low fixed at 2000 (line 204). Both cards match the printed lines"),
 ("cards-changed-c074", "2.4-math", "course/modules/E/E2/cards.json E2-c074 (T, L06); L06.html Remark 1.4 line 236, Remark 2.1 line 243", "PASS", "Without limited liability the principal's profit is 650,000 = first best and the loss is 0 (Remark 1.4). With limited liability the agency cost 650,000 - 600,000 = 50,000 > 0 (Remark 2.1). Claims true and carried hypotheses are the base case"),
 ("cards-changed-c087-c134", "2.7-cards", "course/modules/E/E2/cards.json E2-c087 (C), E2-c134 (C) (L07); L07.html Lab 1 Part C output lines 336-343", "PASS", "induced_revenue_cents 6000 (low-price tie-break) and tie_break_declines_for_L_revenue_cents 4200 (decline); 0.7 x 6000 = 4200 by hand (L07.html line 449-460). Each card matches its printed line"),
 ("cards-changed-c119-c135", "2.2-numbers", "course/modules/E/E2/cards.json E2-c119 (T), E2-c135 (T) (L09); L09.html Lab 1 Part A output lines 223-234, E1/E3 lines 369-387", "PASS", "Part A: values (9000,5000,6000,7000), bids (8000,9500,6500,7000), uniform revenue 14000, discriminatory 17500, value of winners 14000, top values 16000, efficiency 7/8. Re-derived by brute-force script ({S}bruteforce_l09_r1.out): efficiency 0.875, uniform 14000, discriminatory 17500, gap 25.0%. The T grade rests on the page's stated profile"),
 ("cards-lesson-linked-unchanged", "2.9-cards", "course/modules/E/E2/cards.json E2-c044, c045, c051, c055-c059, c063, c067-c071, c073, c075 (L04-L06, byte-identical) against changed L04/L05/L06 passages", "PASS", "Each unchanged card that cites a passage whose wording changed (Assumption 4, Remark 1.4, Proposition 1.3, Lemma 1.2) was re-read; the numbers and claims (1/5, 600,000, 650,000, 50,000, 2000, 6000, 3000) still match the current lesson text"),
]
for rid, check, loc, st, ev in extra:
    rows.append({"id": rid, "check": check, "location": loc, "status": st, "evidence": ev})
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
for rid in base_ids:
    assert rid in ids, rid
FIXES = {
 "cards-changed-c088": "In cards.json E2-c088 front/back, state Proposition 3.2's hypotheses and c: 'With v_H > 0, Delta = v_H - v_L > 0 and c = p_L v_L - p_H Delta < 0, the optimum excludes type L (Proposition 3.2).' Keep the second sentence.",
 "cards-new-c130": "In cards.json E2-c130 front, add the hypothesis: 'What is the mean of the second-highest of n independent uniform values on [0, 1], for n >= 2?' Back unchanged.",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIXES[r["id"]]
fails = [r for r in rows if r["status"] != "PASS"]
mutants = [
 {"id": "z01_symmetric_bid_ceils_instead_of_half_up", "description": "Symmetric discriminatory bid rounded up (ceil) instead of half up", "killed_by": "test_first_price_symmetric_bid_is_n_minus_1_over_n_times_value (seed 0)"},
 {"id": "z02_efficiency_best_takes_one_extra_value", "description": "Best attainable value sums units+1 highest values", "killed_by": "test_two_bidder_case_by_hand (seed 0)"},
 {"id": "z03_discriminatory_top_winner_pays_clearing", "description": "Discriminatory top-ranked winner pays the clearing bid", "killed_by": "test_two_bidder_case_by_hand (seed 0)"},
]
frag = {
 "unit": "E2", "slice": "d", "round": 1,
 "verifier": "Claude Haiku 5.5, independent verifier for E2-d, closing delta round 1 (did not build E2)",
 "pin": "95f3f8cb",
 "base": "33744e5 (round-9 fragment, verdict PASS; ~/.fanout/frags/C-E2-d.round9.json)",
 "checkout": ROOT,
 "scratch": "none outside the checkout; all runs in ledgers/E2/scripts/E2-d-r1/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "PASS" if not fails else "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": (
  "Closing delta (rulings 30, 37) from base 33744e5 to pin 95f3f8cb over the slice paths: course/modules/E/E2/cards.json (18 changed ids: c012, c013, c025, c040, c047, c048, c049, c058, c060, c064, c072, c074, c087, c088, c090, c119, c120, c125; 8 new ids c128-c135), L04.html, L05.html, L06.html (solution/wording only), references/references.json (used_by and generated_at only; no E2-cited record changed), ledgers/E2/mutants z01-z03 (added). project.html, grader/, tests/labs/E2/ and the alternatives are byte-identical since 33744e5. No new mutants were written (ruling 37). "
  "Carry prefix uses round 9, the base fragment's round; the fragment's own round field is 1 as instructed. "
  "Judgement: E2-c025 PASS because the n >= 2 hypothesis is the auction model's standing assumption (L02.html line 91). E2-c049 PASS because its only-when claim is definitional for a separating threshold profile. "
  "Run this round: check_pages, check_dag, check_projects, run_labs, page_smoke L04-L06, mutate_graders (full, 64/64), ruff, mypy, pytest -k E2, verify_refs --offline, build_site --check. Not run this round: the full pytest suite (only -k E2); run_alternatives and run_graders (carried: grader and alternatives unchanged); page_smoke for project.html and the twins under python -I -W error (carried: project.html and tests/labs/E2 unchanged); verify_refs live (offline only). "
  "Observations (not rows): the 38 ungraded cards follow the check_pages convention (grade optional). pyproject.toml changed in the delta (ruff extend-exclude adds ledgers/*/retired and ledgers/*/lab-mutants) and tests/labs changed for other units; both are outside this slice, and ruff and mypy were re-run repo-wide and pass. E2-c088 first sentence is unchanged from round 9 but is re-verified because the card changed (ruling 30). "
 ),
 "summary": (
  f"E2-d closing delta round 1 on pin 95f3f8cb (base 33744e5): {len(rows)} rows, {len(rows) - len(fails)} PASS, {len(fails)} FAIL. "
  "FAILs: cards-changed-c088 (Prop 3.2 hypotheses v_H > 0 and Delta > 0 omitted) and cards-new-c130 (n >= 2 omitted). "
  "Gates PASS: check_pages, check_dag, check_projects, run_labs 12/12, page_smoke L04-L06, mutate_graders 64/64 (z01-z03 killed by named tests), ruff, mypy (386 files), pytest -k E2 (15 test_labs), verify_refs offline 560/0, build_site --check."
 ),
}
json.dump(frag, open(f"{ROOT}/ledgers/E2/E2-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(f"{ROOT}/{S}fragment_summary.txt", "w").write(f"rows {len(rows)} fails {[r['id'] for r in fails]}\n")
print("rows", len(rows), "fails", [r["id"] for r in fails], "verdict", frag["verdict"])
