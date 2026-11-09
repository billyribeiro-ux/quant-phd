"""Round-12 verifier (M3 slice d): three mutants in ledgers/M3/mutants/ (r12d_m02, r12d_m03, r12d_m04) fail with
'SyntaxError: from __future__ imports must occur at the beginning of the file', so their kill is a collection error,
not a test assertion. This probe makes a scratch copy of each with the second (reference) docstring removed, so the
intended student error is the only change, and writes the copies under scripts/M3-d-r12/broken_mutant_repairs/. The
copies are then run by run_one_mutant_r12.sh. Run from the checkout root with python -I."""

import os
import re

NAMES = ["r12d_m02_min_eigenvalue_first_jacobi_value", "r12d_m03_projection_keeps_negatives_down_to_minus_0p01",
         "r12d_m04_weights_scale_row_by_first_volatility"]
OUT = "ledgers/M3/scripts/M3-d-r12/broken_mutant_repairs"
for name in NAMES:
    src = open(f"ledgers/M3/mutants/{name}.py", encoding="utf-8").read()
    # The file starts with the mutant's one-line docstring, then the reference docstring (a second string statement).
    fixed = re.sub(r'\A("""[^\n]*\n)"""Reference solution.*?"""\n', r"\1", src, count=1, flags=re.S)
    assert fixed != src, name
    compile(fixed, name, "exec")
    open(os.path.join(OUT, f"{name}.py"), "w", encoding="utf-8").write(fixed)
    print("repaired copy written:", name)
