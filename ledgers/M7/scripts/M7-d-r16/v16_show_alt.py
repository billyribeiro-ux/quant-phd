import importlib.util, json, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD16-M7-d/ledgers/M7/scripts/M7-d-r16")
import v16_probe as P
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("alt_show", path)
m = importlib.util.module_from_spec(spec); sys.modules["alt_show"] = m; spec.loader.exec_module(m)
case = P.case_of(mu=[1000.0, 0.0], turnover_limit=1e-9)
out = m.allocate(json.loads(json.dumps(case)))
print("weights", out["weights"]); print("multipliers", out["multipliers"]); print("certificate", out["certificate"])
ok, info = P.check(case, out); print("independent", ok, info)
