"""Generates the round-2 student-error mutants from the reference solution by one textual change each."""
import sys
from pathlib import Path

REF = Path(sys.argv[1])
OUT = Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")
MUTANTS = {
    "x01_bond_price_rounds_half_up.py": (
        "    return round(price)\n",
        "    import math\n    return int(math.floor(price + 0.5))\n",
        "bond_price_cents rounds half up (floor of price plus one half) instead of half to even, so an exact half cent goes up.",
    ),
    "x02_hessian_mixed_entry_forward_difference.py": (
        "            mixed = (\n                f(_moved(base, {i: step, j: step}))\n                - f(_moved(base, {i: step, j: -step}))\n                - f(_moved(base, {i: -step, j: step}))\n                + f(_moved(base, {i: -step, j: -step}))\n            )\n            hessian[i][j] = mixed / (4 * step * step)\n",
        "            mixed = (\n                f(_moved(base, {i: step, j: step}))\n                - f(_moved(base, {i: step}))\n                - f(_moved(base, {j: step}))\n                + f0\n            )\n            hessian[i][j] = mixed / (step * step)\n",
        "The mixed Hessian entry is a forward mixed difference, (f(x+he_i+he_j) - f(x+he_i) - f(x+he_j) + f(x)) / h^2, which has error of order h.",
    ),
    "x03_central_scheme_skips_the_step_check.py": (
        "    step = _positive_step(h)\n    if scheme == \"forward\":\n        return (f(x + step) - f(x)) / step\n    if scheme == \"central\":\n        return (f(x + step) - f(x - step)) / (2 * step)\n",
        "    if scheme == \"forward\":\n        step = _positive_step(h)\n        return (f(x + step) - f(x)) / step\n    if scheme == \"central\":\n        step = float(h)\n        return (f(x + step) - f(x - step)) / (2 * step)\n",
        "The central scheme does not check its step, so a step of zero or a negative step is computed instead of raising ValueError.",
    ),
    "x04_dual_product_multiplies_the_derivatives.py": (
        "        return _Dual(self.value * o.value, self.value * o.dot + self.dot * o.value)\n",
        "        return _Dual(self.value * o.value, self.dot * o.dot)\n",
        "The dual product multiplies the two derivatives, self.dot * other.dot, instead of applying the product rule.",
    ),
}
for name, (old, new, desc) in MUTANTS.items():
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new, 1)
    # the mutant's docstring is replaced by its one-line description, as the other mutants do
    head_end = text.index('"""', text.index('"""') + 3) + 3
    text = f'"""{desc}"""' + text[head_end:]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
