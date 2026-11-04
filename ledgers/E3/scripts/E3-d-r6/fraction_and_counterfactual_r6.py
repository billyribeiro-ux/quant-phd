"""Check (1) the questionnaire regex against Fraction on zero-denominator text and (2) the grader docstring counterfactual."""
import re
from fractions import Fraction

JS_REGEX = re.compile(r"\d+(/\d+)?")  # the page's isProbability regex, /^\d+(\/\d+)?$/ (fullmatch = ^...$)
for text in ("1/0", "0/0", "0/5", "1", "0", "2"):
    accepted = bool(JS_REGEX.fullmatch(text))
    try:
        read = str(Fraction(text))
    except (ZeroDivisionError, ValueError) as err:
        read = f"raises {type(err).__name__}"
    print(f"probability text {text!r}: questionnaire accepts={accepted}; Fraction reads -> {read}")

# Counterfactuals for the prospect loss/gain branch in test_prospect_gain_branch_is_the_power_inverse_without_a_loss_weight
lam, gamma = 2.0, 0.5
v = [100 ** (1 - gamma), 400 ** (1 - gamma)]
value = (v[0] + v[1]) / 2
print("correct value", value, "-> sure amount", value ** (1 / (1 - gamma)))
print("loss weight applied to the value (value * lambda):", value * lam, "-> sure amount", (value * lam) ** 2)
print("value divided by lambda:", value / lam, "-> sure amount", (value / lam) ** 2)
print("sure amount divided by lambda (docstring's 225 / 2):", value ** 2 / lam)
