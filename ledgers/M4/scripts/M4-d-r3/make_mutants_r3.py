"""Round-3 verifier D (M4 slice d): writes the student-error mutants v6_01..v6_05 from the checkout's reference.

Each replacement must match exactly once in the reference, so every mutant differs from the reference in one place.
The disclosed survivor (Student-t loss sign) is written under scripts/, not under mutants/, because the suite is
documented as not testing it (project.html, "What the suite does not test").
Usage: python -I ledgers/M4/scripts/M4-d-r3/make_mutants_r3.py <checkout_root>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/M/M4/grader/reference.py").read_text()
out = root / "ledgers/M4/mutants"
scripts = root / "ledgers/M4/scripts/M4-d-r3"

MUTANTS = {
    "v6_01_student_t_chi_square_has_two_nu_degrees_of_freedom.py": (
        "Student-t chi-square drawn with shape nu (2 nu degrees of freedom) instead of nu / 2 (nu degrees of freedom).",
        [("chi_square = rng.gammavariate(nu / 2, 2.0)", "chi_square = rng.gammavariate(nu, 2.0)")],
    ),
    "v6_02_one_chi_square_variable_for_the_whole_run.py": (
        "Student-t uses one chi-square variable for the whole run, drawn once before the first draw, not one per draw.",
        [
            ("    rng = random.Random(seed)\n    losses: list[int] = []",
             "    rng = random.Random(seed)\n"
             "    shared_chi = rng.gammavariate(nu / 2, 2.0) if student and nu is not None else 1.0\n"
             "    losses: list[int] = []"),
            ("            chi_square = rng.gammavariate(nu / 2, 2.0)\n            scale = math.sqrt(matched * nu / chi_square)",
             "            scale = math.sqrt(matched * nu / shared_chi)"),
        ],
    ),
    "v6_03_third_position_dropped_from_the_loss.py": (
        "The loss sums the first two positions only, so a three-position portfolio ignores its third position.",
        [("        for i in range(n):\n            ret = scale", "        for i in range(min(n, 2)):\n            ret = scale")],
    ),
    "v6_04_quantile_takes_the_order_statistic_of_absolute_losses.py": (
        "The 99% loss is the order statistic of the absolute losses, so a gain can set the quantile.",
        [("    return sorted(losses_cents)[index - 1]", "    return sorted(abs(x) for x in losses_cents)[index - 1]")],
    ),
    "v6_05_matched_ratio_inverted_in_the_chi_square_scale.py": (
        "The chi-square scale is sqrt(matched * W / nu), the inverse of sqrt(matched * nu / W), so the returns shrink.",
        [("scale = math.sqrt(matched * nu / chi_square)", "scale = math.sqrt(matched * chi_square / nu)")],
    ),
}

SURVIVOR = (
    "scripts/M4-d-r3/disclosed_survivor_student_t_loss_sign_flipped.py",
    "Student-t loss sign flipped: the Student-t loss is +sum w R, the Gaussian stays -sum w R. Disclosed as not tested.",
    [("            ) if False else None\n", "")],
)

for name, (doc, reps) in MUTANTS.items():
    src = ref
    for old, new in reps:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    body = f'"""Verifier round-3 student-error mutant (v6). {doc}\n\nMutant of the M4 reference (tail_risk.py). All inputs are SIMULATED.\n"""\n'
    body += src.split('"""', 2)[2].lstrip("\n")
    (out / name).write_text(body)
    print("wrote", out / name)

# Disclosed survivor: the Student-t losses take the opposite sign (documented, not counted as a mutant).
old = "        losses.append(round(-total))"
assert ref.count(old) == 1
surv = ref.replace(old, "        losses.append(round(-total) if not student else round(total))")
surv = '"""Verifier round-3 disclosed survivor. Student-t loss sign flipped (+sum w R); the page states the suite does not test it.\n\nNot a counted mutant: scripts/ only. All inputs are SIMULATED.\n"""\n' + surv.split('"""', 2)[2].lstrip("\n")
(scripts / "disclosed_survivor_student_t_loss_sign_flipped.py").write_text(surv)
print("wrote", scripts / "disclosed_survivor_student_t_loss_sign_flipped.py")
