"""Round-13 sample of the autograder instances: seeds 0-49 (validity, interior root, distinctness) from the reference."""
import sys
sys.path.insert(0, "course/modules/E/E4/grader")
import instance as inst
import reference as ref

rows = []
for seed in range(50):
    i = inst.make_instance(seed)
    assert set(i) == {"noise_sd", "info_cost"}
    assert 0.5 <= i["noise_sd"] <= 0.75 and 0.12 <= i["info_cost"] <= 0.15, i
    assert i == inst.make_instance(seed)  # deterministic
    out = ref.solve_model(i["noise_sd"], i["info_cost"])
    rows.append((seed, i["noise_sd"], i["info_cost"], out["informed_fraction"], out["price_informativeness"]))
interior = sum(0.0 < r[3] < 1.0 for r in rows)
distinct_fracs = len({round(r[3], 9) for r in rows})
distinct_inst = len({(r[1], r[2]) for r in rows})
for r in rows[:20]:
    print("seed %2d noise %.3f cost %.3f informed %.8f informativeness %.8f" % r)
print(f"seeds 0-49: interior fraction in {interior}/50; distinct instances {distinct_inst}/50; distinct fractions {distinct_fracs}/50")
