"""Fixer round 17: evidence for the equivalence proof of mutant_v17_02 (ledgers/E4/equivalent/README.md).

Compares the reference solver (course/modules/E/E4/grader/reference.py) with mutant_v17_02 on a grid, and checks the
two identities the README proof uses:

  (I1) For any price slope beta (= b_s) with b_u = -a beta / (lam tau_e), the variance Omega(beta) = Var(v - p) is the
       same whether it is computed from the informed side or the uninformed side. Hence both F_U and F_I of the
       mutant are (V / Omega(beta))^(1/2), and the mutant's gap has the sign of V_U - exp(2ac) V_I, as the reference's.
  (I2) The reported gap of the mutant at its own fraction agrees with the Proposition 3 gap at that fraction.

Run: .venv/bin/python -I ledgers/E4/scripts/E4-d-fix-r17/equiv_v17_02_probe.py
"""

import importlib.util
import random
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ref = load(ROOT / "course/modules/E/E4/grader/reference.py", "ref_solution")
mut = load(ROOT / "ledgers/E4/equivalent/mutant_v17_02_price_slope_drops_uninformed_term.py", "mut_v17_02")

A, TAU_V, TAU_E = 2.0, 1.0, 1.0


def omega_closed(beta: float, lam: float, sd: float) -> float:
    """Var(v - p) for p = beta s + b_u u, b_u = -a beta / (lam tau_e): 1/tau_v + beta^2 (1/tau_v + 1/tau_e)
    - 2 beta / tau_v + b_u^2 sd^2 (the variance of v - beta s - b_u u with v, s, u as in the model)."""
    b_u = -A * beta / (lam * TAU_E)
    return 1.0 / TAU_V + beta * beta * (1.0 / TAU_V + 1.0 / TAU_E) - 2.0 * beta / TAU_V + b_u * b_u * sd * sd


def main() -> None:
    n = 120
    sds = [0.30 + i * (2.70 - 0.30) / (n - 1) for i in range(n)]
    costs = [0.10 + j * (0.20 - 0.10) / (n - 1) for j in range(n)]
    cases = n * n
    differ_fraction = 0
    boundary_mismatch = 0
    max_abs_lam_diff = 0.0
    max_rel_lam_diff = 0.0
    max_mut_gap_vs_prop3 = 0.0
    max_ref_gap_vs_prop3 = 0.0
    for sd in sds:
        for cost in costs:
            r = ref.solve_model(sd, cost)
            m = mut.solve_model(sd, cost)
            lr, lm = r["informed_fraction"], m["informed_fraction"]
            if (lr == 0.0 or lr == 1.0) != (lm == 0.0 or lm == 1.0):
                boundary_mismatch += 1
            if lr != lm:
                differ_fraction += 1
            if 0.0 < lr < 1.0 and 0.0 < lm < 1.0:
                max_abs_lam_diff = max(max_abs_lam_diff, abs(lr - lm))
                max_rel_lam_diff = max(max_rel_lam_diff, abs(lr - lm) / lr)
            prop3_m = ref.gap_at_zero(sd, cost) if lm == 0.0 else ref.indifference_gap(lm, sd, cost)
            if lm not in (0.0, 1.0):
                max_mut_gap_vs_prop3 = max(
                    max_mut_gap_vs_prop3, abs(m["indifference_gap"] - prop3_m) / max(1.0, abs(prop3_m))
                )
            prop3_r = ref.gap_at_zero(sd, cost) if lr == 0.0 else ref.indifference_gap(lr, sd, cost)
            if lr not in (0.0, 1.0):
                max_ref_gap_vs_prop3 = max(
                    max_ref_gap_vs_prop3, abs(r["indifference_gap"] - prop3_r) / max(1.0, abs(prop3_r))
                )
    print(f"grid cases {cases} (sd {sds[0]:.2f}..{sds[-1]:.2f} x cost {costs[0]:.2f}..{costs[-1]:.2f})")
    print(f"cases with a different informed fraction (exact float): {differ_fraction}")
    print(f"cases where the boundary decision (0 or 1 vs interior) differs: {boundary_mismatch}")
    print(f"max |lam_ref - lam_mut| over interior cases: {max_abs_lam_diff:.3e}")
    print(f"max relative |lam_ref - lam_mut| / lam_ref over interior cases: {max_rel_lam_diff:.3e}")
    print(
        "max |reported gap - Prop 3 gap at the reported fraction| / max(1,|gap|), mutant: "
        f"{max_mut_gap_vs_prop3:.3e}; reference: {max_ref_gap_vs_prop3:.3e}"
    )

    # (I1) identity and sign agreement on random interior points
    rng = random.Random(17)
    worst_identity = 0.0
    sign_mismatch = 0
    checked = 0
    for _ in range(20000):
        lam = rng.uniform(1e-3, 1.0)
        sd = rng.uniform(0.3, 2.7)
        cost = rng.uniform(0.0, 0.4)
        ty = ref.price_precision(lam, sd)
        b_s_mut = mut.price_coefficients(lam, sd)[0]
        omega_mut_true = omega_closed(b_s_mut, lam, sd)
        # Omega from the mutant's uninformed and informed terms: Omega = V / F^2
        f_u = mut.uninformed_term(lam, sd)
        f_i = mut.informed_term(lam, sd)
        omega_u = (1.0 / (TAU_V + ty)) / (f_u * f_u)
        omega_i = (1.0 / (TAU_V + TAU_E)) / (f_i * f_i)
        worst_identity = max(worst_identity, abs(omega_u - omega_mut_true) / omega_mut_true)
        worst_identity = max(worst_identity, abs(omega_i - omega_mut_true) / omega_mut_true)
        g_ref = ref.indifference_gap(lam, sd, cost)
        g_mut = mut.indifference_gap(lam, sd, cost)
        if abs(g_ref) > 1e-13 and abs(g_mut) > 1e-13:
            checked += 1
            if (g_ref > 0.0) != (g_mut > 0.0):
                sign_mismatch += 1
    print(f"(I1) random interior points checked: {checked}")
    print(f"(I1) worst relative |Omega_from_terms - Omega(beta)| for the mutant: {worst_identity:.3e}")
    print(f"(I1) sign mismatches between reference and mutant gaps (|gap| > 1e-13): {sign_mismatch}")


if __name__ == "__main__":
    main()
