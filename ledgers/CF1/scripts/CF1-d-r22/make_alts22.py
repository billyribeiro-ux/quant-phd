"""Round-22 correct alternative engines built from the reference (different cutoffs and valid algorithms)."""
import pathlib

CHK = pathlib.Path("/tmp/verify22-CF1-d")
REF = (CHK / "course/modules/CF/CF1/grader/reference.py").read_text()
ALT = CHK / "ledgers/CF1/scripts/CF1-d-r22/alts"
ALT.mkdir(parents=True, exist_ok=True)


def swap(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)


alts = {
    # a: finer grid (8001 points) and a 120-step bisection stopping rule instead of 1e-15 relative width
    "alt_r22d_a_fine_grid_and_fixed_bisection.py": [
        ("_GRID_POINTS = 4001", "_GRID_POINTS = 8001"),
        ("            for _ in range(200):", "            for _ in range(120):"),
        ("                if hi - lo <= 1e-15 * hi:\n                    break\n", ""),
    ],
    # b: NPV by Horner's rule on the discount factor v = 1 / (1 + rate), a valid algorithm
    "alt_r22d_b_npv_horner_on_discount_factor.py": [
        (
            "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
            "    v = 1.0 / (1.0 + rate)\n    acc = 0.0\n    for cf in reversed(list(flows)):\n        acc = acc * v + cf\n    return acc",
        ),
    ],
    # c: payback treats a cumulative within 1e-9 cents of zero as recovered (a numerical cutoff, not the exact test)
    "alt_r22d_c_payback_recovery_tolerance_1e9_cents.py": [
        ("        if cumulative + discounted[t] >= 0.0:", "        if cumulative + discounted[t] >= -1e-9:"),
    ],
}

for name, reps in alts.items():
    src = REF
    for old, new in reps:
        src = swap(src, old, new)
    (ALT / name).write_text(src)
    print("wrote", name)
