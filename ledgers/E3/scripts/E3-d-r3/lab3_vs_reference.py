"""Round-3 cross-check: the Lab 3 reference case (twelve SIMULATED answers, copied from the page's data block) through the
reference engine's estimate(), compared with the numbers Lab 3 prints. Usage (from the checkout):
.venv/bin/python -I ledgers/E3/scripts/E3-d-r3/lab3_vs_reference.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
import reference as ref  # noqa: E402

data_src = (ROOT / "tests/labs/E3/lab-E3-project-3.py").read_text(encoding="utf-8")
ns: dict = {}
exec(compile(data_src.split("def value(")[0], "lab3data", "exec"), {"Fraction": __import__("fractions").Fraction, "math": __import__("math")}, ns)
responses = []
for pid, choice, pa, qa, pb, qb in ns["ANSWERS"]:
    responses.append({"pair_id": pid, "choice": choice, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb})
r = ref.estimate(responses)
for k in ("gamma_hat", "lambda_hat", "kappa_hat", "se_gamma", "se_lambda", "se_kappa", "log_likelihood"):
    print(k, repr(r[k]))
