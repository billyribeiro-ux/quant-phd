"""Writes round-11 student-error mutants (into ledgers/FC2/mutants/) and two alternative correct scanners (into the
round-11 alts folder), each as a one-change edit of the reference solution. Every replacement must match exactly once.

Usage: python3 -I make_r11.py <repo_root>
"""

import os
import sys

root = os.path.abspath(sys.argv[1])
grader = os.path.join(root, "course", "modules", "FC", "FC2", "grader")
ref = open(os.path.join(grader, "reference.py"), encoding="utf-8").read()
REF_DOC_END = '"""\n\nfrom __future__ import annotations'
assert ref.count(REF_DOC_END) == 1, "reference docstring boundary"


def edit(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, f"expected exactly one match for {old[:60]!r}, found {src.count(old)}"
    return src.replace(old, new)


def with_doc(first_line: str, body: str, src: str) -> str:
    """Replace the module docstring with one whose first line describes the error, then the body."""
    rest = src.split(REF_DOC_END, 1)[1]
    return f'"""{first_line}\n\n{body}\n"""\n\nfrom __future__ import annotations' + rest


mutants = {
    "ledgers/FC2/mutants/a11_a_convexity_explanation_omits_P2.py": with_doc(
        "Student error: the convexity explanation omits the one-expiry label P2 that the convexity finding depends on.",
        "Reference solution with one change: _explain_convexity drops 'P2 one expiry' from its label list.",
        edit(ref, 'P1 European exercise, P2 one expiry, "\n        "P5 quotes',
             'P1 European exercise, "\n        "P5 quotes'),
    ),
    "ledgers/FC2/mutants/a11_b_parity_explanation_omits_P4.py": with_doc(
        "Student error: the parity explanation omits the supplied discount factor label P4 that a parity finding uses.",
        "Reference solution with one change: _explain_parity drops 'P4 the supplied discount factor' from its labels.",
        edit(ref, "P3 no income, P4 the supplied discount factor): ", "P3 no income): "),
    ),
    "ledgers/FC2/mutants/a11_c_parity_gap_returns_float.py": with_doc(
        "Student error: parity_gap_cents returns a float from true division, so the cents are not an integer.",
        "Reference solution with one change: parity_gap_cents returns float(_half_up(gap)).",
        edit(ref, "    return _half_up(gap)\n", "    return float(_half_up(gap))\n"),
    ),
    "ledgers/FC2/mutants/a11_d_scan_passes_puts_to_convexity.py": with_doc(
        "Student error: scan runs the convexity test on the put quotes instead of the call quotes.",
        "Reference solution with one change: scan calls convexity_violations on puts, not calls.",
        edit(ref, "    for j in convexity_violations(strikes, calls, df_ppm):",
             "    for j in convexity_violations(strikes, puts, df_ppm):"),
    ),
}

alt13 = edit(
    ref,
    "    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]\n"
    "    w_low = Fraction(high - mid, high - low)\n"
    "    w_high = Fraction(mid - low, high - low)\n"
    "    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]\n",
    "    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]\n"
    "    c0, c1, c2 = calls[j - 1], calls[j], calls[j + 1]\n"
    "    f012 = (Fraction(c2 - c1, k2 - k1) - Fraction(c1 - c0, k1 - k0)) / (k2 - k0)  # second divided difference\n"
    "    return (k1 - k0) * (k2 - k1) * f012  # equals the chord less the call\n",
)
alt14 = edit(
    ref,
    "        gross = _half_up(abs(gap))\n        net = gross - per_finding\n",
    "        gross = _half_up(abs(gap))\n        net = _half_up(abs(gap) - per_finding)\n",
)
alts = {
    "ledgers/FC2/scripts/FC2-d-r11/alts/alt13_divided_difference_convexity.py": alt13,
    "ledgers/FC2/scripts/FC2-d-r11/alts/alt14_net_rounded_once.py": alt14,
}
for rel, text in {**mutants, **alts}.items():
    path = os.path.join(root, rel)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote", rel)
