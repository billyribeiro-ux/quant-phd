"""page_smoke's lab preload: every package a page's labs declare or import is loaded before any lab is timed."""

from __future__ import annotations

from pathlib import Path

from coursekit import Lab
from page_smoke import lab_preload


def lab(code: str, packages: tuple[str, ...]) -> Lab:
    return Lab(
        page=Path("L02.html"),
        id="lab-AP1-L02-1",
        runtime="python",
        code=code,
        expected=None,
        tolerance=0.0,
        packages=packages,
    )


def test_preload_collects_top_level_imports_and_declared_packages_once() -> None:
    first = lab("import numpy as np\nfrom scipy.optimize import linprog  # LP\n\nx = 1\n", ("numpy", "scipy"))
    second = lab("import numpy as np\nimport math\n    import not_top_level\nprint('import x')\n", ("numpy",))
    imports, packages = lab_preload([first, second])
    assert imports.splitlines() == [
        "import numpy as np",
        "from scipy.optimize import linprog  # LP",
        "import math",
    ]
    assert packages == ["numpy", "scipy"]


def test_preload_of_a_page_without_imports_is_empty() -> None:
    assert lab_preload([lab("print(1)\n", ())]) == ("", [])
