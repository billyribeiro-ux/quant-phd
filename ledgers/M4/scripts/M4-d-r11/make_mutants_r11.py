"""Write the three round-11 student-error mutants from grader/reference.py by exact string edits."""
import pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M4-d")
ref = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M4/mutants"

def edit(old, new, count=1):
    assert ref.count(old) == count, (ref.count(old), old)
    return ref.replace(old, new)

m1 = edit(
    '    matched = matched_scale(nu) if student and nu is not None else 1.0\n',
    '    matched = matched_scale(nu) if student and nu is not None else 1.0\n'
    '    if student and nu == 3:\n'
    '        print("debug: student_t draws at nu = 3")\n',
)
m1 = m1.replace(
    '"""Reference',
    '"""Reference', 1)
m1 = '"""Verifier round-11 student-error mutant: a leftover debug print in simulate_losses for the Student-t family at nu = 3.\n\nReference solution for the M4 project. All inputs are SIMULATED.\n"""\n' + m1.split('"""', 2)[2]

m2 = edit(
    '    index = (99 * len(losses_cents) + 99) // 100\n    return sorted(losses_cents)[index - 1]\n',
    '    index = (99 * len(losses_cents) + 99) // 100\n'
    '    if len(losses_cents) == 1:\n'
    '        print("debug: single loss")\n'
    '    return sorted(losses_cents)[index - 1]\n',
)
m2 = '"""Verifier round-11 student-error mutant: a leftover debug print in quantile_99 when the list holds one loss.\n\nReference solution for the M4 project. All inputs are SIMULATED.\n"""\n' + m2.split('"""', 2)[2]

m3 = edit(
    '    rng = random.Random(seed)\n    losses: list[int] = []\n',
    '    if n_draws % 100 == 0:\n'
    '        print("debug: round draw count", n_draws)\n'
    '    rng = random.Random(seed)\n    losses: list[int] = []\n',
)
m3 = '"""Verifier round-11 student-error mutant: a leftover debug print in simulate_losses when n_draws is a multiple of 100.\n\nReference solution for the M4 project. All inputs are SIMULATED.\n"""\n' + m3.split('"""', 2)[2]

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "r11_01_debug_print_student_t_nu_three_in_simulate.py").write_text(m1, encoding="utf-8")
(OUT / "r11_02_debug_print_quantile_single_loss.py").write_text(m2, encoding="utf-8")
(OUT / "r11_03_debug_print_draw_count_multiple_of_100.py").write_text(m3, encoding="utf-8")
print("written")
