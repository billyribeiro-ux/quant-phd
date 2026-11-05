# Round 8: check the hub's prerequisite chain and module titles against curriculum/01-foundations.yaml and 03-markets.yaml
import sys, yaml, glob
mods = {}
for f in sorted(glob.glob("/Users/billyribeiro/.fanout/wt/verifyE8-SC1-a/curriculum/*.yaml")):
    d = yaml.safe_load(open(f, encoding="utf-8"))
    for part in d.get("parts", []):
        for m in part.get("modules", []):
            mods[m["id"]] = m
for mid in ["SC1", "M6", "M4", "M5", "M2", "M1", "P0.1"]:
    m = mods.get(mid)
    print(mid, "|", m.get("title"), "| prereqs:", m.get("prereqs"), "| hours:", m.get("hours"))
