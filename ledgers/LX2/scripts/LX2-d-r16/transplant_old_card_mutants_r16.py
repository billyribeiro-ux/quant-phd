# Re-plants the planted change of each earlier-round card mutant (r13-r15) on the CURRENT cards.json, so that the
# automated checks are tested on the present baseline. usage: transplant_old_card_mutants_r16.py <cards.json> <outdir>
import copy, json, os, subprocess, sys
src, outdir = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as fh:
    base = json.load(fh)
PLANTS = [
    ("r13_card_mut2_c100_bias_41_12_to_41_13", "LX2-c100", "back", "41/12", "41/13"),
    ("r13_card_mut3_c016_300_to_250", "LX2-c016", "back", "less than 300 persons", "less than 250 persons"),
    ("r13_card_mut4_c053_3_104_to_3_105", "LX2-c053", "back", "3/104", "3/105"),
    ("r14_card_mut2_c010_ten_to_fifteen", "LX2-c010", "back", "not later than ten days", "not later than fifteen days"),
    ("r14_card_mut3_c096_no_to_yes", "LX2-c096", "back", "No. The third sentence", "Yes. The third sentence"),
    ("r14_card_mut4_c085_3_8_to_3_9", "LX2-c085", "back", "Hit rate 3/8 (9 hits", "Hit rate 3/9 (9 hits"),
    ("r15_card_mut1_c104_automatically_to_on_application", "LX2-c104", "back", "Automatically, if and so long", "Only on the issuer's application, if and so long"),
    ("r15_card_mut2_c027_15d_to_13a", "LX2-c027", "back", "comes from section 15(d)(1)", "comes from section 13(a)"),
    ("r15_card_mut3_c081_comply_to_optional", "LX2-c081", "back", "members must comply with any legally imposed one", "members may comply with any legally imposed one"),
    ("r15_card_mut4_c086_mae_3_to_2", "LX2-c086", "back", "is 3 index units", "is 2 index units"),
]
here = os.path.dirname(os.path.abspath(__file__))
lessons = [f"/Users/billyribeiro/.fanout/scratch-LX2-d-r16/L0{n}.txt" for n in (1, 2, 3, 4)]
for name, cid, field, old, new in PLANTS:
    cards = copy.deepcopy(base)
    hit = [c for c in cards if c["id"] == cid]
    assert len(hit) == 1 and old in hit[0][field], (name, old)
    hit[0][field] = hit[0][field].replace(old, new, 1)
    path = os.path.join(outdir, "transplant_" + name + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    num = subprocess.run([sys.executable, "-I", os.path.join(here, "card_numbers_r16.py"), path, *lessons], capture_output=True, text=True)
    cla = subprocess.run([sys.executable, "-I", os.path.join(here, "card_claims_r16.py"), path], capture_output=True, text=True)
    n_last = num.stdout.strip().splitlines()[-1]
    print(f"{name}: numbers={'KILLED' if not n_last.endswith(': 0') else 'survived'} claims={'KILLED' if cla.returncode else 'survived'}")
    for line in cla.stdout.splitlines():
        if "FAILED" in line:
            print("     ", line.strip())
print("r13_card_mut5_c003_2a8_to_2a5: moot (current LX2-c003 carries no locator; the planted text is absent)")
