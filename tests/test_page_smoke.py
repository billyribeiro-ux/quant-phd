"""page_smoke's lab preload: every package a page's labs declare or import is loaded before any lab is timed."""

from __future__ import annotations

from pathlib import Path

import pytest

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
    second = lab("import numpy as np\nimport math\ndef f():\n    import not_top_level\nprint('import x')\n", ("numpy",))
    imports, packages = lab_preload([first, second])
    assert imports.splitlines() == [
        "import numpy as np",
        "from scipy.optimize import linprog",
        "import math",
    ]
    assert packages == ["numpy", "scipy"]


def test_preload_of_a_page_without_imports_is_empty() -> None:
    assert lab_preload([lab("print(1)\n", ())]) == ("", [])


def test_preload_ignores_import_text_inside_a_string() -> None:
    docstring = lab('"""\nimport scipy.optimize as so\n"""\nimport numpy as np\n', ("numpy",))
    assert lab_preload([docstring])[0] == "import numpy as np"


def test_preload_keeps_only_the_import_statement_on_a_line_with_other_code() -> None:
    assert lab_preload([lab("import numpy as np; x = 1\n", ("numpy",))])[0] == "import numpy as np"


def test_preload_collects_a_parenthesized_multi_line_import_whole_and_it_compiles() -> None:
    imports = lab_preload([lab("from scipy.optimize import (\n    linprog,\n    minimize,\n)\n", ("scipy",))])[0]
    assert imports == "from scipy.optimize import linprog, minimize"
    compile(imports, "<preload>", "exec")


def test_preload_drops_a_future_import_even_after_another_labs_code() -> None:
    labs = [lab("import numpy as np\n", ("numpy",)), lab("from __future__ import annotations\nx = 1\n", ())]
    imports, _ = lab_preload(labs)
    assert imports == "import numpy as np"
    compile(imports, "<preload>", "exec")


def test_preload_ignores_a_docstring_line_that_starts_with_from() -> None:
    labs = [lab('"""\nfrom the training half of the sample\n"""\nx = 1\n', ())]
    assert lab_preload(labs) == ("", [])


def test_preload_names_the_lab_whose_code_is_not_valid_python() -> None:
    with pytest.raises(SyntaxError, match="lab-AP1-L02-1: not valid Python"):
        lab_preload([lab("import numpy as np\nx = (1,\n", ("numpy",))])
