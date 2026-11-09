"""Independent 50-digit (decimal) re-derivation of the numbers the project page prints (VERIFIER round 15).

Uses only the closed forms of Propositions 1 to 4 written from the page's own formulas, not the lab code.
Prints each quantity next to the value the page states, so the reader can compare them.
Usage: python -I numbers_r15.py
"""

from decimal import Decimal as D, getcontext

getcontext().prec = 60
A = D(2)
TV = D(1)
TE = D(1)


def tau_bar(c: D) -> D:
    return (TV + TE) * (-2 * A * c).exp() - TV


def lam_star(sd: D, c: D) -> D:
    t = tau_bar(c)
    return A * sd * (t / (TE * (TE - t))).sqrt()


def gap_zero(sd: D, c: D) -> D:
    a2 = A * A * sd * sd
    uninformed = (1 + a2 / TV) ** D("-0.5")
    informed = (1 + TE / TV + (TV + TE) * a2 / (TV * TV)) ** D("-0.5")
    return uninformed - (A * c).exp() * informed


def gap_at(lam: D, sd: D, c: D) -> D:
    ty = lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)
    denom = lam * (TV + TE) + (1 - lam) * (TV + ty)
    bs = (lam * TE + (1 - lam) * ty) / denom
    bu = -A * bs / (lam * TE)
    r = ty / (TV + ty) - bs
    fu = (1 + r * r * (TV + ty) * (1 / TV + 1 / ty)) ** D("-0.5")
    prec = TV + TE
    slope = TE / prec - bs
    var_gap = slope * slope * (1 / TV + 1 / TE) + bu * bu * sd * sd
    fi = (1 + prec * var_gap) ** D("-0.5")
    return fu - (A * c).exp() * fi


def informativeness_at(lam: D, sd: D) -> D:
    ty = lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)
    return ty / (TV + ty)


def report(name: str, sd: str, c: str) -> None:
    sd_d, c_d = D(sd), D(c)
    lam = lam_star(sd_d, c_d)
    t = tau_bar(c_d)
    ty_at = lam * lam * TE * TE / (lam * lam * TE + A * A * sd_d * sd_d)
    print(f"--- {name}: noise {sd}, cost {c}")
    print(f"tau_bar = {float(t):.8f}")
    print(f"gap at 0 = {float(gap_zero(sd_d, c_d)):+.6f}")
    print(f"gap at 1 = {float(gap_at(D(1), sd_d, c_d)):+.6f}")
    print(f"lambda* (closed form) = {float(lam):.8f}  [{lam:.12f}]")
    print(f"gap at lambda* = {float(gap_at(lam, sd_d, c_d)):+.3e}")
    bs_over = -A / (lam * TE)
    print(f"b_u/b_s = -a/(lambda* tau_e) = {float(bs_over):.8f}")
    print(f"tau_y(lambda*) = {float(ty_at):.8f}")
    print(f"informativeness tau_bar/(tau_v+tau_bar) = {float(t / (TV + t)):.8f}")
    print(f"1 - e^(2ac) tau_v/(tau_v+tau_e) = {float(1 - (2 * A * c_d).exp() * TV / (TV + TE)):.8f}")
    print(f"informativeness via lambda* = {float(informativeness_at(lam, sd_d)):.8f}")


if __name__ == "__main__":
    report("Lab 1", "0.60", "0.13")
    report("Lab 2", "0.70", "0.14")
    print("--- spec box")
    print(f"tau_bar(0.150) = {float(tau_bar(D('0.150'))):.10f}")
    print(f"tau_bar(0.120) = {float(tau_bar(D('0.120'))):.10f}")
    print(f"tau_y(1) at sd 0.75 = 1/(1+4 sd^2) = {float(1 / (1 + 4 * D('0.75') ** 2)):.8f}")
