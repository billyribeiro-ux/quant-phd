"""Round 11 witnesses for AC1-a: recompute the printed figures that the changed sentences cite.

Run as: <checkout>/.venv/bin/python -I ledgers/AC1/scripts/AC1-a-r11/witness_r11.py
Cents are integers; percentages are computed from the unrounded quotient.
"""
from fractions import Fraction as F

def c(x: str) -> int:
    """Parse a USD string like '1,234.56' into integer cents (exact)."""
    neg = x.startswith("-")
    x = x.lstrip("-").replace(",", "")
    d, _, r = x.partition(".")
    v = int(d) * 100 + int((r + "00")[:2])
    return -v if neg else v

def usd(v: int) -> str:
    s = "-" if v < 0 else ""
    d, r = divmod(abs(v), 100)
    return f"{s}{d:,}.{r:02d}"

ok = True
def check(label: str, cond: bool, detail: str = "") -> None:
    global ok
    ok &= cond
    print(("PASS " if cond else "FAIL ") + label + ((" | " + detail) if detail else ""))

# L01 Example 3.3 and E1 / E3 / Lab 1 arithmetic
credit_sales, cash_sales, collections = c("192,834.97"), c("21,046.51"), c("154,267.97")
revenue = credit_sales + cash_sales
cash_in = cash_sales + collections
ar_end = credit_sales - collections
check("L01 Example 3.3 revenue 213,881.48", usd(revenue) == "213,881.48")
check("L01 Example 3.3 cash from customers 175,314.48", usd(cash_in) == "175,314.48")
check("L01 Example 3.3 difference equals closing receivable 38,567.00", revenue - cash_in == ar_end == c("38,567.00"))
share = F(c("38,567.00"), c("213,881.48"))
check("L01 E1 share 0.18032 to five dp and 18.0% to one dp", f"{float(share):.5f}" == "0.18032" and f"{float(share)*100:.1f}" == "18.0", f"{float(share):.10f}")
check("L01 E2 gap 19,237.23 equals payable", c("49,831.40") - c("30,594.17") == c("19,237.23") == c("19,237.23"))
debit_side = c("224,720.31") + c("38,567.00") + c("49,831.40")
credit_side = c("19,237.23") + c("80,000.00") + c("213,881.48")
check("L01 E3 both sides 313,118.71", usd(debit_side) == usd(credit_side) == "313,118.71")
check("L01 quiz 1,000 - 800 receivable rise 200", 1000 - 800 == 200)

# L02 margins (E1), E2, M2, M3, E3, P-check
S = [c("9,168,896.75"), c("10,002,754.93"), c("9,110,215.12")]
K = [c("5,427,054.02"), c("5,906,265.33"), c("5,634,913.13")]
N = [c("1,003,421.14"), c("945,769.70"), c("419,730.32")]
gm = [round(F(s - k, s) * 10000) / 100 for s, k in zip(S, K)]
nm = [round(F(n, s) * 10000) / 100 for n, s in zip(N, S)]
check("L02 E1 gross margins 40.81 40.95 38.15", gm == [40.81, 40.95, 38.15], str(gm))
check("L02 E1 net margins 10.94 9.46 4.61", nm == [10.94, 9.46, 4.61], str(nm))
cash_sales25, coll25 = c("1,029,222.06"), c("7,624,353.82")
share25 = F(cash_sales25 + coll25, S[0])
check("L02 E2 share 94.38%", round(share25 * 10000) / 100 == 94.38, f"{float(share25)*100:.4f}")
check("L02 E2 remainder 515,320.87", usd(S[0] - (cash_sales25 + coll25)) == "515,320.87")
check("L02 M2 2026 net income 945,769.70", usd(S[1] - (c("5,906,265.33") + c("1,850,719.90") + c("1,300,000.00"))) == "945,769.70")
check("L02 M3 2026 retained earnings 1,549,190.84", usd(c("803,421.14") + c("945,769.70") - c("200,000.00")) == "1,549,190.84")
check("L02 E3 2026 subtotals sum 1,491,615.64", usd(c("2,191,615.64") - c("1,500,000.00") + c("800,000.00")) == "1,491,615.64")
check("L02 E3 cash 4,454,305.29 to 5,945,920.93 is 1,491,615.64", usd(c("5,945,920.93") - c("4,454,305.29")) == "1,491,615.64")
check("L02 Def 2.1 / Prop 2.2 2025: 1,003,421.14 + 1,000,000 - 515,320.87 + 166,205.02 = 1,654,305.29",
      usd(c("1,003,421.14") + c("1,000,000.00") - c("515,320.87") + c("166,205.02")) == "1,654,305.29")

# L03 M1, M2, M3, E1, E3 and the Check 6 gaps
check("L03 M1 2026 indirect 2,191,615.64", usd(c("945,769.70") + c("1,300,000.00") - c("65,302.46") + c("11,148.40")) == "2,191,615.64")
check("L03 M2 net equipment 2026 4,200,000.00", c("4,000,000.00") + c("1,500,000.00") - c("1,300,000.00") == c("4,200,000.00"))
check("L03 M3 quarterly 120,000.00 and six quarters 720,000.00", c("2,400,000.00") / 20 == c("120,000.00") and 6 * c("120,000.00") == c("720,000.00"))
a_q = c("5,000,000.00") // 20
b_q = c("1,500,000.00") // 20
check("L03 E3 schedule 2027: A 12 quarters, B 8 quarters, total 3,600,000.00",
      a_q * 12 + b_q * 8 == c("3,600,000.00"), f"A {usd(a_q*12)} B {usd(b_q*8)}")
check("L03 R2 ten-year life: A annual charge 1,000,000.00 to 500,000.00",
      c("5,000,000.00") // 5 == c("1,000,000.00") and c("5,000,000.00") // 10 == c("500,000.00"))
check("L03 R3 amortization 1,200,000 over four years is 300,000 per year", c("1,200,000.00") // 4 == c("300,000.00"))
check("L03 Check 6 add-back gap 2026 equals depreciation 1,300,000.00 (2,191,615.64 - 1,300,000.00 = 891,615.64)",
      c("2,191,615.64") - c("1,300,000.00") == c("891,615.64"))
check("L03 Check 6 dividend gap 2026: 1,749,190.84 - 1,549,190.84 = 200,000.00",
      c("1,749,190.84") - c("1,549,190.84") == c("200,000.00"))
check("L03 Check 4 2026 cash identity 4,454,305.29 + 1,491,615.64 = 5,945,920.93",
      c("4,454,305.29") + c("1,491,615.64") == c("5,945,920.93"))

# Hub skill check (rung 2): Proposition 3.2 with only the no-write-off condition stated.
# Witness: no write-offs, returns or allowances hold, yet revenue includes 100.00 of interest received in cash,
# so revenue less cash from customers (2,500.00 - 1,900.00 = 600.00) differs from the change in receivables.
credit = c("2,400.00")
interest_cash = c("100.00")
collections_w = c("1,900.00")          # cash from customers excludes the interest
revenue_w = credit + interest_cash      # revenue is not credit sales plus cash sales (hypothesis (ii))
cash_from_customers_w = collections_w   # cash from customers is 1,900.00 (hypothesis (iii) not used)
delta_ar = credit - collections_w       # the only AR debits are credit sales and the only credits are collections
check("hub rung 2 witness: no write-offs holds, yet R - K != change in AR",
      revenue_w - cash_from_customers_w != delta_ar,
      f"R-K={usd(revenue_w - cash_from_customers_w)} dAR={usd(delta_ar)}")

print("ALL PASS" if ok else "SOME FAIL")
