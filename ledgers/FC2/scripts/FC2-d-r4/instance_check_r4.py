"""Round-4 checks on the FC2 generator (seeds 0-49): clean chains have no finding, planted amounts, bounds, distinctness."""
import collections
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "course/modules/FC/FC2/grader"))
sys.path.insert(0, str(ROOT / "ledgers/FC2/scripts/FC2-d-r3/alts"))
import instance  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", ROOT / "course/modules/FC/FC2/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

kinds = collections.Counter()
none_with_findings = []
planted_mismatch = []
distinct = set()
counts = collections.Counter()
for s in range(50):
    i = instance.make_instance(s)
    kinds[i["planted_kind"]] += 1
    chain = {k: i[k] for k in ("spot_cents", "df_ppm", "strikes_cents", "call_cents", "put_cents")}
    chain["cost"] = {"fee_cents_per_contract": i["fee_cents_per_contract"], "half_spread_cents": i["half_spread_cents"]}
    f = ref.scan(chain)
    counts[len(f)] += 1
    distinct.add(repr([(x["kind"], x["strike_cents"], x["net_cents"]) for x in f]))
    if i["planted_kind"] == "none" and f:
        none_with_findings.append(s)
    if i["planted_kind"] == "parity" and i["planted_amount_cents"] - (i["fee_cents_per_contract"] + i["half_spread_cents"]) * 3 > 0:
        if not any(x["kind"] == "parity" for x in f):
            planted_mismatch.append(s)
    if i["planted_kind"] == "convexity" and i["planted_amount_cents"] - (i["fee_cents_per_contract"] + i["half_spread_cents"]) * 3 > 0:
        if not any(x["kind"] == "convexity" for x in f):
            planted_mismatch.append(("cvx", s))
print("planted kinds:", dict(kinds))
print("findings count distribution:", dict(counts))
print("distinct finding lists:", len(distinct))
print("clean (none) chains with a finding:", none_with_findings)
print("planted violations above cost but not found:", planted_mismatch)
print("labels:", {i["label"] for i in (instance.make_instance(s) for s in range(50))})
