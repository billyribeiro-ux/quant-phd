# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Cross-check Lab 3's printed numbers against the reference and the three verifier candidates (AC2 project).

Usage (from the repository root): .venv/bin/python -I ledgers/AC2/scripts/project-r1/lab3_check.py

Runs the lab's own SAMPLE (read from tests/labs/AC2/lab-AC2-project-3.py, with its print calls disabled) through
modified_jones of the course reference and of impls/A, impls/B and impls/C, and prints the coefficients and the
discretionary accruals to six decimals, which are the page's printed precision.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    modules = {
        "reference": load("ref", ROOT / "course/modules/AC/AC2/grader/reference.py"),
        "impl A": load("impl_a", HERE / "impls/A/atlas/fundamentals.py"),
        "impl B": load("impl_b", HERE / "impls/B/atlas/fundamentals.py"),
        "impl C": load("impl_c", HERE / "impls/C/atlas/fundamentals.py"),
    }
    src = (ROOT / "tests/labs/AC2/lab-AC2-project-3.py").read_text(encoding="utf-8")
    ns: dict = {}
    exec(compile(src.replace("print(", "(lambda *a, **k: None)("), "lab3", "exec"), ns)
    sample = ns["SAMPLE"]
    for name, module in modules.items():
        out = module.modified_jones(sample)
        print(name, [round(c, 6) for c in out["coefficients"]], [round(d, 6) for d in out["discretionary"]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
