"""Round-3: size of the float gap that makes alternative 4 fail test_zero_probability_prize_contributes_nothing (exact ==).
Builds alternative 4 with run_alternatives.build, imports it from a scratch directory, and compares the likelihood with and
without a zero-probability prize on seeds 26, 29, 44, 45 (the seeds where the suite fails).
Usage (from the checkout): .venv/bin/python -I ledgers/E3/scripts/E3-d-r3/alt4_zero_prob_gap.py
"""
import importlib.util
import json
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "ledgers/E3/scripts"))
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
import run_alternatives as ra  # noqa: E402
from instance import make_instance  # noqa: E402

work = Path(tempfile.mkdtemp(prefix="e3-alt4-gap-"))
(work / "elicit_alt4.py").write_text(ra.build("alt4"), encoding="utf-8")
spec = importlib.util.spec_from_file_location("elicit_alt4", work / "elicit_alt4.py")
alt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alt)
import reference as ref  # noqa: E402

for seed in (26, 29, 44, 45):
    inst = make_instance(seed)
    true = {"gamma": float(inst["gamma"]), "lambda": float(inst["lambda"]), "kappa": float(inst["kappa"])}
    resp = json.loads(str(inst["responses_json"]))
    base = dict(resp[0])
    with_zero = [dict(base, prizes_a=base["prizes_a"][:1] + [base["prizes_a"][1] if len(base["prizes_a"]) > 1 else 0],
                      probs_a=["0", "1"])]
    # the test's construction: a loss with probability zero is added to A
    rr = [dict(RESP := {"pair_id": 0, "choice": "A", "prizes_a": [-100, 300], "probs_a": ["0", "1"], "prizes_b": [200], "probs_b": ["1"]})]
    without = [dict(rr[0], prizes_a=[300], probs_a=["1"])]
    a = alt.log_likelihood(rr, true)
    b = alt.log_likelihood(without, true)
    print("seed", seed, "alt4 zero-prob gap:", repr(a - b), "| reference gap:", repr(ref.log_likelihood(rr, true) - ref.log_likelihood(without, true)))
