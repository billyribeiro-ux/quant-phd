"""Write the verifier's round-5 student-error mutants of the M2 reference into ledgers/M2/mutants/.

Each mutant is the reference module with one change; the module docstring's first line describes the error.
"""

import pathlib
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M2-e")
REF = ROOT / "course/modules/M/M2/grader/reference.py"
OUT = ROOT / "ledgers/M2/mutants"

SPECS = [
    (
        "r5_01_central_difference_sign_swapped.py",
        "The central estimate is written with its endpoints swapped, so it returns minus the derivative.",
        "    if scheme == \"central\":\n        return (f(x + step) - f(x - step)) / (2 * step)\n",
        "    if scheme == \"central\":\n        return (f(x - step) - f(x + step)) / (2 * step)\n",
    ),
    (
        "r5_02_convexity_not_divided_by_the_price.py",
        "Convexity is returned as the second sensitivity in cents, without dividing by the unrounded price.",
        "\"convexity_analytic\": second / price,",
        "\"convexity_analytic\": second,",
    ),
    (
        "r5_03_hessian_mixed_entries_left_at_zero.py",
        "The mixed second partials are never filled in, so every off-diagonal Hessian entry stays at zero.",
        "            hessian[i][j] = mixed / (4 * step * step)\n",
        "            hessian[i][j] = 0.0 * mixed\n",
    ),
    (
        "r5_04_bond_price_uses_simple_interest.py",
        "The bond price discounts each cash flow with simple interest, 1 / (1 + rate * t), not compound discounting.",
        "    price = sum(cash * v**t for t, cash in flows)\n    return round(price)",
        "    price = sum(cash / (1 + rate * t) for t, cash in flows)\n    return round(price)",
    ),
]

def main() -> int:
    text = REF.read_text(encoding="utf-8")
    head, _, rest = text.partition('"""')
    _, _, rest_after_doc = rest.partition('"""')
    ref_doc_first = rest.splitlines()[0]
    for name, description, old, new in SPECS:
        if text.count(old) != 1:
            print(f"FAIL {name}: anchor found {text.count(old)} times")
            return 1
        body = text.replace(old, new, 1)
        doc_old = '"""' + rest.split('"""')[0]
        doc_new = '"""' + description + "\n\n" + rest.split('"""')[0][len(ref_doc_first) + 1:]
        if not doc_old.startswith('"""'):
            print("FAIL: unexpected docstring layout")
            return 1
        body = body.replace(doc_old, doc_new, 1)
        (OUT / name).write_text(body, encoding="utf-8")
        print(f"wrote {name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
