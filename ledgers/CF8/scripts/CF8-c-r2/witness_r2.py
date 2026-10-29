"""Round 2 witnesses: rewrite the reference engine with one behaviour each, run targeted tests on seeds 0-2."""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path
GRADER = Path("/tmp/verifyC2-CF8-c/course/modules/CF/CF8/grader")
REF = (GRADER / "reference.py").read_text(encoding="utf-8")
PY = "/tmp/verifyC2-CF8-c/.venv/bin/python"
W = {
 "print_in_forecast": ("def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:\n    \"\"\"Thirteen weekly rows of the capped revolver forecast, in cents.\"\"\"\n",
    "def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:\n    \"\"\"Thirteen weekly rows of the capped revolver forecast, in cents.\"\"\"\n    print('forecast called')\n"),
 "warn_in_pinch": ("def covenant_pinch(case: Mapping[str, Any]) -> dict[str, int]:\n    \"\"\"The week (1 to 13) with the smallest covenant headroom, earliest on a tie, and that headroom in cents.\"\"\"\n",
    "def covenant_pinch(case: Mapping[str, Any]) -> dict[str, int]:\n    \"\"\"The week (1 to 13) with the smallest covenant headroom, earliest on a tie, and that headroom in cents.\"\"\"\n    import warnings\n    warnings.warn('pinch')\n"),
 "imports_instance": ("from typing import Any\n", "from typing import Any\nimport instance  # noqa\n"),
 "cached_rows": ("def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:\n    \"\"\"Thirteen weekly rows of the capped revolver forecast, in cents.\"\"\"\n    _check_case(case)\n    return _path(case, capped=True)\n",
    "_CACHE: dict[str, Any] = {}\n\ndef forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:\n    \"\"\"Thirteen weekly rows of the capped revolver forecast, in cents.\"\"\"\n    _check_case(case)\n    if 'rows' not in _CACHE:\n        _CACHE['rows'] = _path(case, capped=True)\n    return _CACHE['rows']\n"),
 "mutates_argument": ("def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:\n    \"\"\"Thirteen weekly rows of the capped revolver forecast, in cents.\"\"\"\n    _check_case(case)\n",
    "def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:\n    \"\"\"Thirteen weekly rows of the capped revolver forecast, in cents.\"\"\"\n    _check_case(case)\n    case['horizon_weeks'] = 13  # noqa\n    try:\n        case['covenant_threshold_cents'] = case['covenant_threshold_cents']  # noqa\n    except Exception:\n        pass\n    if 'opening_cash_cents' in case and False:\n        pass\n    import copy as _c\n    case_ = case\n    case_.update({'opening_drawn_cents': case_['opening_drawn_cents']})\n"),
}
EXTRA = {"mutates_argument": ("case_.update", "case_.update")}
def run(name, src, selector):
    work = Path(tempfile.mkdtemp(prefix="w-"))
    for n in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / n, work / n)
    (work / "treasury_forecast.py").write_text(src, encoding="utf-8")
    out = []
    for seed in (0, 1, 2):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "-k", selector, "test_project.py"], cwd=work, capture_output=True, text=True, env=env)
        out.append(f"seed{seed}:{'PASS' if r.returncode == 0 else 'FAIL'}")
    shutil.rmtree(work, ignore_errors=True)
    return out
if __name__ == "__main__":
    for name, (old, new) in W.items():
        if name == "mutates_argument":
            continue  # not run: superseded by test_functions_do_not_change_their_argument
        assert REF.count(old) == 1, (name, REF.count(old))
        src = REF.replace(old, new)
        if name == "imports_instance":
            sel = "does_not_import_instance or imports_only"
        elif name in ("print_in_forecast", "warn_in_pinch"):
            sel = "prints_or_warns or writes_to_stdout"
        elif name == "cached_rows":
            sel = "fresh_objects or fresh"
        else:
            sel = "fresh_objects or fresh"
        print(name, run(name, src, sel))
