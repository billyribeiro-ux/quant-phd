"""Round-7 numeric check of the hand-case comments in test_project.py (HAND_CASES, lines 227-255).
Usage: python -I hand_cases_r7.py <grader_dir>. Uses the reference solver on the same hand cases, with the upper bound
or the turnover limit varied to test the comment 'the unconstrained answer (0.35, 0.65)' of the upper-bound case.
"""
import copy
import sys

sys.path.insert(0, sys.argv[1])
import reference as ref  # noqa: E402


def hand_case(**fields):
    base = {
        "label": "SIMULATED hand case for the acceptance suite, not a real portfolio",
        "gamma": 1.0, "sector": [0, 0], "sector_caps": [2.0], "turnover_limit": 2.0,
        "sigma": [[1.0, 0.0], [0.0, 1.0]], "lower": [-1.0, -1.0], "upper": [2.0, 2.0],
    }
    base.update(fields)
    return base


def show(label, case):
    out = ref.allocate(copy.deepcopy(case))
    print(f"{label}: weights={[round(v, 6) for v in out['weights']]} turnover_mult={out['multipliers']['turnover_total']:.6f} upper={[round(v, 6) for v in out['multipliers']['upper']]}")


show("upper-bound case as written (mu=[0.2,0.5], upper=[1,0.3], tau=0.5)", hand_case(mu=[0.2, 0.5], w0=[0.8, 0.2], upper=[1.0, 0.3], turnover_limit=0.5))
show("same case with upper bounds removed (upper=[1,1]), tau=0.5", hand_case(mu=[0.2, 0.5], w0=[0.8, 0.2], upper=[1.0, 1.0], turnover_limit=0.5))
show("same case with turnover removed (tau=1e9), upper bounds removed", hand_case(mu=[0.2, 0.5], w0=[0.8, 0.2], upper=[1.0, 1.0], turnover_limit=1e9))
show("turnover-binding case as written (mu=[0.4,0], w0=[0.5,0.5], tau=0.2)", hand_case(mu=[0.4, 0.0], w0=[0.5, 0.5], turnover_limit=0.2))
show("same case with turnover removed (tau=1e9)", hand_case(mu=[0.4, 0.0], w0=[0.5, 0.5], turnover_limit=1e9))
show("budget-only case (mu=[0.3,0.1], w0=[0.5,0.5])", hand_case(mu=[0.3, 0.1], w0=[0.5, 0.5]))
