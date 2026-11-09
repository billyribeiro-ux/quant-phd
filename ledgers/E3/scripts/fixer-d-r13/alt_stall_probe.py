"""Probe: does an alternative return a non-stationary point on the STALL participant (generator seed 108)?"""
import importlib.util
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
spec = importlib.util.spec_from_file_location("run_alts", ROOT / "ledgers/E3/scripts/run_alternatives.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
name = sys.argv[1]
work = Path(tempfile.mkdtemp(prefix="stallprobe-"))
try:
    shutil.copy(ROOT / "course/modules/E/E3/grader/test_project.py", work / "test_project.py")
    shutil.copy(ROOT / "course/modules/E/E3/grader/instance.py", work / "instance.py")
    (work / "elicit.py").write_text(mod.build(name), encoding="utf-8")
    sys.path.insert(0, str(work))
    import elicit as sol  # noqa: E402
    import test_project as tp  # noqa: E402
    from instance import make_instance  # noqa: E402
    responses = json.loads(str(make_instance(108)["responses_json"]))
    try:
        fit = sol.estimate(responses)
        parsed = [tp.parse(r) for r in responses]
        print(name, "returned gamma", fit["gamma_hat"], "lambda", fit["lambda_hat"], "kappa", fit["kappa_hat"])
        print(name, "largest score at 1e-5", tp._largest_score_component(parsed, fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"], 1e-5))
        print(name, "largest score at 1e-6", tp._largest_score_component(parsed, fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"], 1e-6))
    except Exception as err:  # noqa: BLE001
        print(name, "raised", type(err).__name__, str(err)[:100])
finally:
    shutil.rmtree(work, ignore_errors=True)
