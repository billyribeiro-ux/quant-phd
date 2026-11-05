"""Write two round-10 alternative correct implementations (valid under the spec) derived from reference.py by one edit each."""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/FC2/scripts/FC2-d-r10/alts"

EDITS = {
    # validation order changed: lengths and cost checked before df and strikes (each condition still raised)
    "alt11_validation_order_lengths_first.py": [
        (
            "    _check_df(df_ppm)\n    _check_strikes(strikes)\n    _check_lengths(strikes, calls, puts)\n    _check_cost(fee, spread)\n",
            "    _check_lengths(strikes, calls, puts)\n    _check_cost(fee, spread)\n    _check_strikes(strikes)\n    _check_df(df_ppm)\n",
        ),
    ],
    # explanations reworded with the same labels, and the cost and the convexity rule stated in other words
    "alt12_reworded_explanations.py": [
        (
            '        f"put-call parity (P1 European exercise, P2 one expiry, P3 no income, P4 the supplied discount factor): "\n'
            '        f"{direction}, so {action}; net {net} cents after {LEGS_PER_FINDING} legs at fee {fee} plus half-spread "\n'
            '        f"{spread} (P6)."',
            '        f"Parity (P1, P2, P3, P4, P6): {direction}; {action}. Net {net} cents after {LEGS_PER_FINDING} legs, "\n'
            '        f"fee {fee} and half-spread {spread}."',
        ),
    ],
}

for name, edits in EDITS.items():
    text = ref
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
