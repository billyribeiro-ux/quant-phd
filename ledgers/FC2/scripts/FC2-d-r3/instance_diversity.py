"""Round-3: instance validity and diversity over seeds 0-49 (reference scanner, grader instance.py)."""
import collections
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "course/modules/FC/FC2/grader"))
import instance  # noqa: E402
import reference  # noqa: E402

kinds = collections.Counter()
chains = set()
findings_sig = collections.Counter()
rows = []
for seed in range(50):
    inst = instance.make_instance(seed)
    chain = {k: inst[k] for k in ("spot_cents", "df_ppm", "strikes_cents", "call_cents", "put_cents")}
    chain["cost"] = {"fee_cents_per_contract": inst["fee_cents_per_contract"], "half_spread_cents": inst["half_spread_cents"]}
    f = reference.scan(chain)
    kinds[inst["planted_kind"]] += 1
    chains.add(tuple(inst["call_cents"]) + tuple(inst["put_cents"]) + tuple(inst["strikes_cents"]))
    sig = tuple((r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in f)
    findings_sig[sig] += 1
    rows.append((seed, inst["planted_kind"], len(f), inst["spot_cents"], inst["df_ppm"], inst["strikes_cents"][0], inst["strikes_cents"][-1]))
print("planted kinds over 50 seeds:", dict(kinds))
print("distinct chains:", len(chains), "distinct findings lists:", len(findings_sig))
print("findings count distribution:", dict(collections.Counter(r[2] for r in rows)))
print("seed, planted, #findings, spot, df, K0, K5 (first 12):")
for r in rows[:12]:
    print("  ", r)
