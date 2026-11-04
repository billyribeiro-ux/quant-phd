"""Print the registry fields for the four keys the LX1 hub and slice pages cite, and the MANIFEST dataset ids."""
import json
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-LX1-a"
d = json.load(open(f"{ROOT}/references/references.json", encoding="utf-8"))
items = d if isinstance(d, list) else list(d.get("references", d.get("entries", d)).values()) if isinstance(d.get("references", d.get("entries", d)), dict) else d.get("references", d.get("entries", d))
keys = ["friedman1963monetary", "eichengreen1992golden", "garber2000famous", "reinhart2009this"]
for it in items:
    if isinstance(it, dict) and it.get("key") in keys:
        print(it["key"], "|", it["title"], "|", [a["family"] for a in it["authors"]], "|", it["year"], "|", it["status"], "|", it["used_by"])
man = json.load(open(f"{ROOT}/course/assets/data/market/MANIFEST.json", encoding="utf-8"))
print("MANIFEST ids:", [x["id"] for x in man["datasets"]])
