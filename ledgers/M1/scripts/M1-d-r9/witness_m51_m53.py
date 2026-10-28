"""Round-9 witnesses for the two survivors: m51 (annual cutoff below 1e-8) and m53 (term capped at 360 months).

Run with python -I. Loads the reference and the mutants by file path."""
import importlib.util
import sys


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ref = load("ref", "/tmp/verify9-M1-d/course/modules/M/M1/grader/reference.py")
ROOT = "/tmp/verify9-M1-d/ledgers/M1/mutants/"
m51 = load("m51", ROOT + "m51_tiny_rate_cutoff_1e-8_treated_as_zero.py")
m53 = load("m53", ROOT + "m53_term_capped_at_360_months.py")
print("m51 level payment, L=13296419 cents, annual 5e-9, 360 months: reference", ref.level_payment_cents(13296419, 5e-9, 360), "mutant", m51.level_payment_cents(13296419, 5e-9, 360))
print("m51 month-1 payment via schedule: reference", ref.amortization_schedule(13296419, 5e-9, 360)[0].payment_cents, "mutant", m51.amortization_schedule(13296419, 5e-9, 360)[0].payment_cents)
print("reference level payment, 100000 cents, 5 %, 480 months:", ref.level_payment_cents(100000, 0.05, 480))
try:
    print("m53 mutant:", m53.level_payment_cents(100000, 0.05, 480))
except ValueError as exc:
    print("m53 mutant raises ValueError:", exc)
