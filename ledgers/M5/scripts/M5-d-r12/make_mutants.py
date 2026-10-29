import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
muts = {
    "v12_01_stop_test_uses_beta_times_change.py": (
        "        if certified <= target:\n",
        "        if beta * change <= target:\n",
        "Student-error mutant (verifier-written, M5 slice d round 12): the stop test compares beta times the change with tol, dropping the 1/(1 - beta) factor of the certificate, so the solver stops before the certified error is within tol.",
    ),
    "v12_02_continuation_read_in_reverse_order.py": (
        "        for successor, continuation in zip(grid, values, strict=True):\n",
        "        for successor, continuation in zip(grid, values[::-1], strict=True):\n",
        "Student-error mutant (verifier-written, M5 slice d round 12): the continuation values are read in reverse grid order, so each successor k' is paired with the value of the mirror-image grid point.",
    ),
    "v12_03_value_returned_is_beta_times_the_iterate.py": (
        '        "value": values,\n',
        '        "value": [beta * x for x in values],\n',
        "Student-error mutant (verifier-written, M5 slice d round 12): solve returns beta times the iterate as value, confusing the value with its continuation term; the certified error still refers to the iterate.",
    ),
}
for name, (old, new, desc) in muts.items():
    assert src.count(old) == 1, (name, src.count(old))
    body = src.replace(old, new)
    lines = body.split("\n", 1)
    text = f"# {desc}\n" + body
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
