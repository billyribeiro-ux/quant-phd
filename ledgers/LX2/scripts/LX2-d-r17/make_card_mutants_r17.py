# Writes planted card mutants (complete cards.json copies, one change each) into ledgers/LX2/mutants/ and reports which
# round-17 check kills each one. usage: make_card_mutants_r17.py <cards.json> <outdir> <scriptdir>
import copy, json, os, subprocess, sys
src, outdir, sdir = sys.argv[1], sys.argv[2], sys.argv[3]
base = json.load(open(src, encoding="utf-8"))
MUTANTS = [
    ("r17_card_mut1_c106_roles_swapped", "LX2-c106", "back", "The insider who gives it is the tipper.", "The insider who gives it is the tippee.", "Tipper role swapped; card claims assertion c106"),
    ("r17_card_mut2_c105_footnote_24", "LX2-c105", "back", "Footnote 23 of Dirks (p. 663 n. 23)", "Footnote 23 of Dirks (p. 663 n. 24)", "Scienter footnote locator changed; card claims assertion c105"),
    ("r17_card_mut3_c099_need_not_state", "LX2-c099", "back", "must state that the person is one", "need not state that the person is one", "A3 requirement inverted; card claims assertion c099"),
    ("r17_card_mut4_c030_knowledge_dropped", "LX2-c030", "back", " and the tippee knows or should know that there has been a breach", "", "Tippee knowledge condition dropped; card claims assertion c030"),
    ("r17_card_mut5_c101_restored", None, None, None, None, "Removed Dodd-Frank card restored; absence assertion (plan section 9)"),
    ("r17_card_mut6_c094_one_disagreement", "LX2-c094", "back", "in 0 trader counts", "in 1 trader counts", "Printed tally count changed; card claims assertion c094"),
    ("r17_card_mut7_c053_inequality_flipped", "LX2-c053", "back", "3 × 97 = 291 is less than 6 × 104 = 624", "3 × 97 = 291 is greater than 6 × 104 = 624", "Exact comparison reversed; card claims assertion c053"),
    ("r17_card_mut8_c100_bias_41_13", "LX2-c100", "back", "Bias 41/12 (errors summing to 82 over 24 periods)", "Bias 41/13 (errors summing to 82 over 24 periods)", "Wrong exact fraction; card numbers check (41/13 absent from lesson) and claims assertion"),
    ("r17_card_mut9_c059_threshold_three", "LX2-c059", "back", "The largest ratio, 21/37, is below 2.", "The largest ratio, 21/37, is below 3.", "Threshold restated; card claims assertion c059 (21/37 below 2)"),
    ("r17_card_mut10_c085_hit_rate_3_9", "LX2-c085", "back", "Hit rate 3/8 (9 hits in 24 periods), rounded 0.3750.", "Hit rate 3/9 (9 hits in 24 periods), rounded 0.3333.", "Wrong hit rate; card numbers check (3/9 absent) and claims assertion c085"),
]
os.makedirs(outdir, exist_ok=True)
report = []
for name, cid, field, old, new, desc in MUTANTS:
    cards = copy.deepcopy(base)
    if cid is None:
        cards.append({"id": "LX2-c101", "lesson": "L03", "front": "What does Definition 3.1 say about the Dodd–Frank Act?",
                      "back": "It names the Act as one of this unit's concepts. The lesson does not state its provisions, its scope or its duties.",
                      "basis": "Definition 3.1 (named, content not stated)"})
    else:
        hit = [c for c in cards if c["id"] == cid]
        assert len(hit) == 1, cid
        assert old in hit[0][field], (name, old)
        hit[0][field] = hit[0][field].replace(old, new)
    path = os.path.join(outdir, name + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=2)
    killers = []
    r = subprocess.run([sys.executable, "-I", os.path.join(sdir, "card_claims_r17.py"), path], capture_output=True, text=True)
    if r.returncode != 0: killers.append("card_claims_r17.py: " + r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "card_claims_r17.py")
    r = subprocess.run([sys.executable, "-I", os.path.join(sdir, "card_numbers_r17.py"), path] + [os.path.join(sdir, f) for f in ("L01.txt", "L02.txt", "L03.txt", "L04.txt")], capture_output=True, text=True)
    if "absent from own lesson: 0" not in r.stdout: killers.append("card_numbers_r17.py: " + r.stdout.strip().splitlines()[-1])
    report.append(f"{name}: {'KILLED' if killers else 'SURVIVED'} by {killers if killers else '-'} | {desc}")
print("\n".join(report))
