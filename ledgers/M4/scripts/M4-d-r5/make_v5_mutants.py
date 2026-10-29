"""Round-5 verifier student-error mutants for the M4 project, each one edit of the reference solution."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/M/M4/grader/reference.py"
OUT = ROOT / "ledgers/M4/mutants"

EDITS = {
    "v5_m01_matched_scale_applied_not_square_rooted": (
        "Verifier round-5 student-error mutant. (nu - 2) / nu multiplies the return, not its square root.",
        "            scale = math.sqrt(matched * nu / chi_square)",
        "            scale = matched * math.sqrt(nu / chi_square)",
    ),
    "v5_m02_positions_applied_in_reverse_order": (
        "Verifier round-5 student-error mutant. Each return is weighted by the mirrored asset's position.",
        "            total += position_cents[i] * ret",
        "            total += position_cents[n - 1 - i] * ret",
    ),
    "v5_m03_quantile_index_rounded_not_ceiled": (
        "Verifier round-5 student-error mutant. The 99% index is round(0.99 n), not its ceiling.",
        "    index = (99 * len(losses_cents) + 99) // 100",
        "    index = max(1, round(0.99 * len(losses_cents)))",
    ),
}

SRC = REF.read_text(encoding="utf-8")
for name, (doc, old, new) in EDITS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    body = SRC.replace(old, new)
    end = body.index('"""', 3) + 3  # drop the reference's module docstring, keep the code
    (OUT / f"{name}.py").write_text(f'"""{doc}"""' + body[end:], encoding="utf-8")
    print("wrote", name)
