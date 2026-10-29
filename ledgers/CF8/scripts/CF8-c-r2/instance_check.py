import sys, json, importlib.util
G = "/tmp/verifyC2-CF8-c/course/modules/CF/CF8/grader"
sys.path.insert(0, G)
spec = importlib.util.spec_from_file_location("ref", G + "/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
import instance
binds = []; lags_c=[]; lags_p=[]; pinch=set(); ok=0
for s in range(50):
    c = json.loads(instance.make_instance(s)["payload"])
    lags_c.append(c["collection_lag_days"]); lags_p.append(c["payment_lag_days"])
    plan = ref.revolver_plan(c)
    if plan["required_commitment_cents"] > c["revolver_commitment_cents"]:
        binds.append(s)
    pinch.add(ref.covenant_pinch(c)["week"])
    if c["minimum_cash_cents"] > 0 and c["revolver_commitment_cents"] >= c["opening_drawn_cents"]: ok += 1
print("collection lag range", min(lags_c), max(lags_c), "payment lag range", min(lags_p), max(lags_p))
print("binding seeds (required > commitment):", len(binds), binds)
print("valid cases:", ok, "/50; distinct pinch weeks:", sorted(pinch))
