# SIMULATED statements for one filer, in the A15 item names (USD thousands). Not a real company.
ST = {
    "2021-12-31": {
        "revenue": 1000.0,
        "net_income": 80.0,
        "total_assets": 900.0,
        "equity": 400.0,
        "operating_income": 120.0,
        "long_term_debt": 150.0,
        "cash": 60.0,
        "cfo": 95.0,
    },
    "2022-12-31": {
        "revenue": 1200.0,
        "net_income": 110.0,
        "total_assets": 1100.0,
        "equity": 460.0,
        "operating_income": 160.0,
        "long_term_debt": 180.0,
        "cash": 90.0,
        "cfo": 130.0,
    },
}
PREV, END = "2021-12-31", "2022-12-31"
TAX = 0.25  # a stated tax rate, not a filed one

avg_assets = (ST[END]["total_assets"] + ST[PREV]["total_assets"]) / 2
avg_equity = (ST[END]["equity"] + ST[PREV]["equity"]) / 2
roe = ST[END]["net_income"] / avg_equity
net_margin = ST[END]["net_income"] / ST[END]["revenue"]
asset_turnover = ST[END]["revenue"] / avg_assets
leverage = avg_assets / avg_equity
print("DuPont identity holds:", abs(roe - net_margin * asset_turnover * leverage) < 1e-12)
print("roe", round(roe, 6), "net margin", round(net_margin, 6))


def invested_capital(end: str) -> float:
    return ST[end]["equity"] + ST[end]["long_term_debt"] - ST[end]["cash"]


nopat = ST[END]["operating_income"] * (1 - TAX)
avg_capital = (invested_capital(END) + invested_capital(PREV)) / 2
roic = nopat / avg_capital
print("nopat", nopat, "roic", round(roic, 6))

accruals = (ST[END]["net_income"] - ST[END]["cfo"]) / avg_assets
print("cash-flow accruals", round(accruals, 6))
