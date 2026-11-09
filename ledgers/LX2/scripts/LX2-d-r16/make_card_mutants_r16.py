# Writes seven planted card mutants (complete cards.json copies, one change each) into ledgers/LX2/mutants/ and reports
# which verifier check kills each one. usage: make_card_mutants_r16.py <cards.json> <outdir> <L01> <L02> <L03> <L04>
import copy, json, os, subprocess, sys
src, outdir = sys.argv[1], sys.argv[2]
lessons = sys.argv[3:7]
with open(src, encoding="utf-8") as fh:
    base = json.load(fh)
MUTANTS = [
    ("r16_card_mut1_c070_inclusive_to_exclusive", "LX2-c070", "|e_t| ≤ 2 (an inclusive band of 2 index units)", "|e_t| < 2 (an exclusive band of 2 index units)"),
    ("r16_card_mut2_c051_drop_2X", "LX2-c051", "G = R + 2X + C_m + C_t", "G = R + X + C_m + C_t"),
    ("r16_card_mut3_c063_reprice_adds_zero", "LX2-c063", "No. Each adds 1 to cancels", "Yes. A reprice adds 0 to cancels and a withdrawal adds 1"),
    ("r16_card_mut4_c018_R15_listed", "LX2-c018", "R15 requires it to be not_listed", "R15 requires it to be listed"),
    ("r16_card_mut5_c076_at_least", "LX2-c076", "is at most the number of hits at b2", "is at least the number of hits at b2"),
    ("r16_card_mut6_c099_need_not_state", "LX2-c099", "must state that the person is one", "need not state that the person is one"),
    ("r16_card_mut7_c079_45_117", "LX2-c079", "44/117, about 0.3761", "45/117, about 0.3846"),
]
here = os.path.dirname(os.path.abspath(__file__))
for name, cid, old, new in MUTANTS:
    cards = copy.deepcopy(base)
    hit = [c for c in cards if c["id"] == cid]
    assert len(hit) == 1 and old in hit[0]["back"], (name, old)
    hit[0]["back"] = hit[0]["back"].replace(old, new, 1)
    path = os.path.join(outdir, name + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    num = subprocess.run([sys.executable, "-I", os.path.join(here, "card_numbers_r16.py"), path, *lessons], capture_output=True, text=True)
    cla = subprocess.run([sys.executable, "-I", os.path.join(here, "card_claims_r16.py"), path], capture_output=True, text=True)
    numk = "KILLED" if num.stdout.strip().splitlines()[-1].endswith(": 0") is False else "survived"
    clak = "KILLED" if cla.returncode != 0 else "survived"
    print(f"{name}: card_numbers_r16={numk} card_claims_r16={clak}")
    for line in cla.stdout.splitlines():
        if "FAILED" in line:
            print("    ", line.strip())
