"""Starter for the AC2 project: atlas/fundamentals.py, the Atlas A15 fundamentals engine.

Implement every function to the A15 contract (project page, section "Rung 3 · Specification"), then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

The four tables below (ITEMS, TAG_PRIORITY, the Beneish constants) are given by the A15 contract. Do not import
any file from the grader: the module must run on its own. Every function must validate its inputs and raise
ValueError for the conditions the contract names. None may print or warn, or change its arguments. Use NumPy and
the standard library only.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

# The four tables below are given by the A15 contract; the functions are yours to write.
ITEMS: tuple[str, ...] = (
    "revenue",
    "cogs",
    "sga",
    "depreciation",
    "operating_income",
    "net_income",
    "cfo",
    "total_assets",
    "current_assets",
    "cash",
    "receivables",
    "ppe",
    "total_liabilities",
    "current_liabilities",
    "long_term_debt",
    "equity",
    "shares_outstanding",
)
TAG_PRIORITY: Mapping[str, tuple[str, ...]] = {
    "revenue": ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"),
    "cogs": ("CostOfRevenue", "CostOfGoodsAndServicesSold"),
    "sga": ("SellingGeneralAndAdministrativeExpense",),
    "depreciation": ("DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "Depreciation"),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss",),
    "cfo": ("NetCashProvidedByUsedInOperatingActivities",),
    "total_assets": ("Assets",),
    "current_assets": ("AssetsCurrent",),
    "cash": ("CashAndCashEquivalentsAtCarryingValue",),
    "receivables": ("AccountsReceivableNetCurrent",),
    "ppe": ("PropertyPlantAndEquipmentNet",),
    "total_liabilities": ("Liabilities",),
    "current_liabilities": ("LiabilitiesCurrent",),
    "long_term_debt": ("LongTermDebtNoncurrent",),
    "equity": ("StockholdersEquity",),
    "shares_outstanding": ("CommonStockSharesOutstanding",),
}
# The Beneish (1999) constants are UNCONFIRMED: reproduced by one secondary web source without a locator.
BENEISH_INTERCEPT: float = -4.84
BENEISH_COEFFICIENTS: Mapping[str, float] = {
    "DSRI": 0.920,
    "GMI": 0.528,
    "AQI": 0.404,
    "SGI": 0.892,
    "DEPI": 0.115,
    "SGAI": -0.172,
    "LVGI": -0.327,
    "TATA": 4.679,
}

__all__ = [
    "BENEISH_COEFFICIENTS",
    "BENEISH_INTERCEPT",
    "ITEMS",
    "TAG_PRIORITY",
    "accruals_balance_sheet",
    "accruals_cash_flow",
    "beneish_m_score",
    "current_ratio",
    "days_sales_outstanding",
    "debt_to_assets",
    "dupont",
    "gross_margin",
    "modified_jones",
    "piotroski_f_score",
    "roic",
    "standardize",
]

Facts = Mapping[str, Any]
Statements = Mapping[str, Mapping[str, float]]


def standardize(facts: Facts, as_of: str | None = None) -> dict[str, dict[str, float]]:
    """Standardized statements {period_end: {item: value}} from a company-facts mapping, as known on ``as_of``."""
    raise NotImplementedError("standardize")


def dupont(statements: Statements, period_end: str) -> dict[str, float]:
    """DuPont decomposition on average assets and equity; roe equals net_margin * asset_turnover * leverage."""
    raise NotImplementedError("dupont")


def roic(statements: Statements, period_end: str, tax_rate: float) -> float:
    """NOPAT over average invested capital, with invested capital = equity + long-term debt - cash."""
    raise NotImplementedError("roic")


def current_ratio(statements: Statements, period_end: str) -> float:
    """Current assets over current liabilities at the period end."""
    raise NotImplementedError("current_ratio")


def gross_margin(statements: Statements, period_end: str) -> float:
    """Gross margin: (revenue - cogs) / revenue."""
    raise NotImplementedError("gross_margin")


def debt_to_assets(statements: Statements, period_end: str) -> float:
    """Long-term debt over total assets at the period end."""
    raise NotImplementedError("debt_to_assets")


def days_sales_outstanding(statements: Statements, period_end: str) -> float:
    """Receivables over revenue, times 365."""
    raise NotImplementedError("days_sales_outstanding")


def accruals_cash_flow(statements: Statements, period_end: str) -> float:
    """Cash-flow accruals: (net income - cfo) over average total assets."""
    raise NotImplementedError("accruals_cash_flow")


def accruals_balance_sheet(statements: Statements, period_end: str) -> float:
    """Sloan (1996) balance-sheet accruals over average total assets."""
    raise NotImplementedError("accruals_balance_sheet")


def modified_jones(sample: Sequence[Mapping[str, float]]) -> dict[str, Any]:
    """Modified Jones model (Dechow, Sloan & Sweeney 1995), estimated by OLS without an intercept."""
    raise NotImplementedError("modified_jones")


def piotroski_f_score(statements: Statements, period_end: str) -> dict[str, Any]:
    """Piotroski (2000) F-score: nine binary signals on the period end and its two preceding year ends."""
    raise NotImplementedError("piotroski_f_score")


def beneish_m_score(statements: Statements, period_end: str) -> dict[str, float]:
    """Beneish (1999) eight-variable M-score on the period end and the previous year end."""
    raise NotImplementedError("beneish_m_score")
