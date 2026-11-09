"""Round-16 sample of the BK4 seeded instances (slice c): 20 seeds plus the two cases of the suite, checked against
the page's Inputs rules (:200) and the three-scenario separation the suite demands. Imports the grader's instance.py
from the checkout (read-only use). Run: python -I instance_sample_r16.py <checkout-root>
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "course/modules/BK/BK4/grader"))
from instance import make_instance  # noqa: E402

TARGETS = (9_000, 9_500, 9_750)
answers = {}
for seed in list(range(20)) + [7_919, 7_919 + 1]:
    c = make_instance(seed)
    ids = c["member_ids"]
    n = len(ids)
    ok = (
        4 <= n <= 6
        and ids == list(range(1, n + 1))
        and 1 <= c["defaulter_id"] <= n
        and all(f >= 1 for f in c["default_fund_cents"])
        and all(m >= 0 for m in c["initial_margin_cents"])
        and c["ccp_capital_cents"] >= 0
        and 40 <= len(c["losses_cents"]) <= 80
        and all(isinstance(x, int) and x >= 0 for x in c["losses_cents"])
        and c["target_bps"] in TARGETS
    )
    d = c["defaulter_id"] - 1
    m_d, f_d = c["initial_margin_cents"][d], c["default_fund_cents"][d]
    L = c["losses_cents"]
    inside_margin = any(x <= m_d for x in L)
    inside_fund = any(m_d < x <= m_d + f_d for x in L)
    past_all = any(x > m_d + f_d + c["ccp_capital_cents"] for x in L)
    S = len(L)
    k = math.ceil(Fraction(c["target_bps"] * S, 10_000))
    margin = sorted(L)[k - 1]
    answers[seed] = margin
    print(f"seed {seed}: valid {ok} | N {n} defaulter {c['defaulter_id']} S {S} target {c['target_bps']} "
          f"margin_d {m_d} fund_d {f_d} capital {c['ccp_capital_cents']} | regions {inside_margin} {inside_fund} {past_all} | "
          f"k {k} sized margin {margin}")
print("distinct sized margins over the 22 cases:", len(set(answers.values())))
