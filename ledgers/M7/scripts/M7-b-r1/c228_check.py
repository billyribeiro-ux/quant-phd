# Verifier script (M7-b round 1): recomputes the turnover numbers of card M7-c228 and of L06.html E3 from the printed lines.
from fractions import Fraction as F

printed_weights = [F("0.389219"), F("0.220570"), F("0.390211"), F("0.000000")]  # twin_L06.out, nonneg row, gamma 4
w0 = F(1, 4)
six_place = sum(abs(w - w0) for w in printed_weights)
print("turnover from six-place printed weights =", float(six_place), "rounded 6 places:", f"{float(six_place):.6f}")
print("deviations:", [str(w - w0) for w in printed_weights])
print("printed exact value 0.5588607333 rounds to 6 places:", f"{0.5588607333:.6f}")
print("difference in sixth place:", round((float(six_place) - 0.5588607333) * 1e6, 3), "units of 1e-6")
