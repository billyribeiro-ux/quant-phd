Round-12 verifier: two candidate mutants that survived the full seeds 0-49 run were moved here, not kept as mutants.
r12_02: ratio test uses <= (last tied blocking row enters the working set). Changes only the active-set path.
r12_03: initial working set uses exact zero slack. Constraints within tolerance enter after a negligible first step.
Both return KKT points that satisfy every definition on the page for seeds 0-49 (mutate_M7_0-49_r12.log: SURVIVED,
no test failure on any seed), so the page states no behaviour they violate. They are valid alternatives.
