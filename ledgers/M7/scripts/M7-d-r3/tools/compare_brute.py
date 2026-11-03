import json, sys
alt_dir, ref_dir = sys.argv[1], sys.argv[2]
sys.path.insert(0, ref_dir)
import reference as ref  # noqa: E402  (reference solution, copied as reference.py)
sys.path.insert(0, alt_dir)
import constrained_allocator as alt  # noqa: E402  (alternative under test)
from instance import make_instance  # noqa: E402
worst_w = 0.0; worst_cert = 0.0; bad = []
for s in range(50):
    case = json.loads(make_instance(s)["payload"])
    a = alt.allocate(json.loads(json.dumps(case)))
    r = ref.allocate(json.loads(json.dumps(case)))
    dw = max(abs(x - y) for x, y in zip(a["weights"], r["weights"]))
    cert = max(a["certificate"].values())
    worst_w = max(worst_w, dw); worst_cert = max(worst_cert, cert)
    if dw > 1e-9 or cert > 1e-8: bad.append((s, dw, cert))
print("seeds 0-49: max |w_alt - w_ref| =", f"{worst_w:.2e}", "; max alt certificate field =", f"{worst_cert:.2e}", "; seeds outside tolerance:", bad)
