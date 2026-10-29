import importlib.util, json, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/quant-b2/course/modules/M/M7/grader")
import instance, reference as R
M = "/tmp/m7d_r14/removed/"
names = ["q04_dual_residual_without_zero_floor.py", "v11_01_dual_residual_sign_flipped_in_certificate.py",
         "r02_turnover_total_residual_dropped_from_primal.py", "r04_budget_left_out_of_primal_residual.py",
         "r05_turnover_total_slackness_term_zeroed.py", "v10_01_dual_residual_ignores_sector_and_turnover_multipliers.py",
         "v10_02_complementary_slackness_signed_not_absolute.py", "s12_03_turnover_total_multiplier_clipped_at_zero.py"]
def load(path, i):
    spec = importlib.util.spec_from_file_location(f"m{i}", path)
    mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod); return mod
for i, nm in enumerate(names):
    mod = load(M + nm, i)
    diff = []
    for seed in range(300):
        case = json.loads(instance.make_instance(seed)["payload"])
        a = R.allocate(json.loads(json.dumps(case)))
        b = mod.allocate(json.loads(json.dumps(case)))
        if a != b:
            diff.append(seed)
    print(nm, "differs on", len(diff), "of 300 seeds", diff[:5])
