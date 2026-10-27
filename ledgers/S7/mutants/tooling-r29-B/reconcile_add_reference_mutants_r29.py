"""Round 29: reconcile the add_reference mutant counts (summary row r20-mut-summary says 49; part A's mutant list has 66).
Reads the release and history ledgers, part A and part B fragments at the checkout (git show for history). Prints every count.
Usage: python -I reconcile_add_reference_mutants_r29.py <checkout>"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1])

def git_json(rev_path):
    return json.loads(subprocess.run(["git", "show", rev_path], cwd=ROOT, capture_output=True, text=True, check=True).stdout)

def ar_ids(mutants):
    ids = []
    for m in mutants:
        desc = str(m.get("description", ""))
        if "add_reference" in desc[:200]:
            mm = re.search(r"mutant (\w+)", desc)
            if mm:
                ids.append(mm.group(1))
    return ids

print("== 1. cumulative counts of add_reference mutants in the ledgers (unique ids)")
cum = {}
for label, rev in [("round20", "ledgers/S7/history/round20/data-tooling.json"), ("round21", "ledgers/S7/history/round21/data-tooling.json"),
                   ("round22", "ledgers/S7/history/round22/data-tooling.json"), ("round23", "ledgers/S7/history/round23/data-tooling.json"),
                   ("round24", "ledgers/S7/history/round24/data-tooling.json"), ("release", "ledgers/S7/history/release/data-tooling.json")]:
    ids = ar_ids(git_json(f"c9beb92:{rev}")["mutants"])
    cum[label] = set(ids)
    print(f"{label:8s} rows={len(ids):3d} unique={len(set(ids)):3d}")
order = ["round20", "round21", "round22", "round23"]
prev = set()
print("per-round additions (new ids vs previous round):")
for r in order:
    new = cum[r] - prev
    print(f"  {r}: +{len(new)}  {sorted(new)}")
    prev = cum[r]
print("unique ids in release = round23 = round24 = release:", cum["release"] == cum["round23"] == cum["round24"], len(cum["release"]))

print("== 2. part A fragment (ledgers/S7/data-tooling-A.json at c9beb92)")
A = git_json("c9beb92:ledgers/S7/data-tooling-A.json")["mutants"]
a_ids = ar_ids(A)
print("part A add_reference mutants:", len(a_ids), "unique:", len(set(a_ids)), "equal to release set:", set(a_ids) == cum["release"])

print("== 3. part B fragment: mutant claims in rows (own rows and cited rows)")
B = json.loads((ROOT / "ledgers/S7/data-tooling-B.json").read_text(encoding="utf-8"))
own_rows = {r["id"]: re.findall(r"\b([RDACMU][A-Z]?\d{2})\b", r["id"]) for r in B["rows"] if "-mut-" in r["id"] and "add" not in r["id"]}
claims = {}
for r in B["rows"]:
    ids = set(re.findall(r"\b((?:R|D|A|C|MU)\d{2})\b", r["evidence"]))
    if ids:
        claims[r["id"]] = sorted(ids)
own = {}
for rid in ["r20-mut-R03", "r20-mut-R04", "r20-mut-R05", "r20-mut-R06", "r20-mut-R07", "r20-mut-R11", "r20-mut-R12", "r20-mut-D07", "r20-mut-D09",
            "r21-mut-D11", "r21-mut-A07", "r21-mut-R16", "r21-mut-R20", "r21-mut-C01", "r21-mut-C02", "r21-mut-C03", "r21-mut-A06"]:
    own[rid] = rid.split("-")[-1]
print("own per-id rows in part B:", len(own), sorted(own.values()))
print("row ids that cite mutant ids in their evidence (part B):")
for k, v in claims.items():
    print(f"  {k}: {v}")
allclaimed = set()
for v in claims.values():
    allclaimed |= set(v)
print("distinct add_reference-style ids claimed anywhere in part B evidence:", len(allclaimed))
print("ids claimed in part B that are NOT in the release set (R08, R09, R13, R15, R18, R19 are not mutants):",
      sorted(i for i in allclaimed if i not in cum["release"]))

print("== 4. the summary row")
summ = [r for r in B["rows"] if r["id"] == "r20-mut-summary"][0]
print("location says:", re.findall(r"\((\d+) mutants\)", summ["location"]), "| ledger cumulative values: 25, 36, 47, 66")
print("49 equals a cumulative round total?", 49 in [len(cum[r]) for r in order] or 49 in [25, 36, 47, 66])
print("49 - 47 (round 22 release-era total) =", 49 - 47, "; 66 - 49 =", 66 - 49)
print("RESULT: 49 is not the sum of the per-round additions (25 + 11 + 11 + 19 = 66) and not any cumulative total (25, 36, 47, 66). The harness that produced 49 is not archived, so its two-mutant difference from 47 cannot be named.")
