"""Round-13: exact random-instance checks of the L06 identities (Lemma 6.3, Lemma 6.4 V_U, Prop 6.7 clearing, Cor 6.8)."""
import random
from fractions import Fraction as F

rng = random.Random(13)
def rq():
    return F(rng.randint(1, 40), rng.randint(1, 40))

n_ok = 0
for trial in range(300):
    sv2, se2, su2, a = rq(), rq(), rq(), rq()
    lam = F(rng.randint(1, 19), 20)
    tv, te = 1 / sv2, 1 / se2
    kap = a / (lam * te)
    seta2 = se2 + kap * kap * su2
    teta = 1 / seta2
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    thu = kap * ths
    # Prop 6.7 clearing at random (s, u)
    s, u = rq() - 1, rq() - 1
    p = ths * s - thu * u
    vp = ths * ths * (sv2 + se2) + thu * thu * su2
    cvp = ths * sv2
    b = cvp / vp
    VU = sv2 - b * cvp
    VU_formula = sv2 * (ths * ths * se2 + thu * thu * su2) / vp
    assert VU == VU_formula, "V_U formula"
    omega = sv2 / (sv2 + se2)
    VI = sv2 * se2 / (sv2 + se2)
    assert omega / VI == te and 1 / VI == tv + te, "Lemma 6.3 identities"
    xi = (omega * s - p) / (a * VI)
    xu = (b * p - p) / (a * VU)
    assert lam * xi + (1 - lam) * xu == u, "A4 clearing at equilibrium"
    assert b == teta / (ths * (tv + teta)), "Cor 6.8 slope"
    assert VU == 1 / (tv + teta), "Cor 6.8 variance"
    n_ok += 1
print("random instances passing all identities:", n_ok, "of 300")
