"""AC1 lab L01: post generated transactions to T-accounts and check that every entry balances.

SIMULATED: the firm's transaction amounts are drawn from a seeded random number generator for this lab. The
opening investment and the entry dates are fixed in the code. The firm is not a real company. Amounts are
integer cents; no floating-point money. Standard library only, no network. Every number printed below is
computed by this file.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 20261027

# Account -> (type, normal side). The normal side is the side that increases the balance.
CHART: dict[str, tuple[str, str]] = {
    "cash": ("asset", "debit"),
    "accounts_receivable": ("asset", "debit"),
    "accounts_payable": ("liability", "credit"),
    "common_stock": ("equity", "credit"),
    "sales": ("revenue", "credit"),
    "operating_expense": ("expense", "debit"),
}


@dataclass(frozen=True)
class Line:
    """One side of one account. Debit and credit are non-negative integer cents; one of them is zero."""

    account: str
    debit: int = 0
    credit: int = 0


@dataclass(frozen=True)
class Entry:
    """A journal entry: the day of the quarter, a memo, and its lines."""

    day: int
    memo: str
    lines: tuple[Line, ...]


def check_entry(entry: Entry) -> None:
    """Raise ValueError if the entry uses an unknown account, a bad amount, or does not balance."""
    debits = 0
    credits = 0
    for line in entry.lines:
        if line.account not in CHART:
            raise ValueError(f"{entry.memo!r}: unknown account {line.account!r}")
        for amount in (line.debit, line.credit):
            if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
                raise ValueError(f"{entry.memo!r}: amounts must be non-negative integer cents, got {amount!r}")
        if line.debit and line.credit:
            raise ValueError(f"{entry.memo!r}: one line carries both a debit and a credit on {line.account!r}")
        debits += line.debit
        credits += line.credit
    if debits != credits:
        raise ValueError(f"{entry.memo!r}: debits {debits} do not equal credits {credits}")


class Ledger:
    """Accepts only entries that pass check_entry. A rejected entry leaves the ledger unchanged."""

    def __init__(self) -> None:
        self.entries: list[Entry] = []

    def post(self, entry: Entry) -> None:
        check_entry(entry)
        self.entries.append(entry)

    def debit_total(self, account: str) -> int:
        return sum(line.debit for e in self.entries for line in e.lines if line.account == account)

    def credit_total(self, account: str) -> int:
        return sum(line.credit for e in self.entries for line in e.lines if line.account == account)

    def balance(self, account: str) -> int:
        """Balance on the account's normal side, in integer cents, never negative in this lab."""
        debit, credit = self.debit_total(account), self.credit_total(account)
        return debit - credit if CHART[account][1] == "debit" else credit - debit


def money(cents: int) -> str:
    """Format integer cents as dollars and cents, for example 1234567 -> 12,345.67."""
    sign = "-" if cents < 0 else ""
    dollars, rest = divmod(abs(cents), 100)
    return f"{sign}{dollars:,}.{rest:02d}"


def generate_quarter(rng: random.Random, ledger: Ledger) -> dict[str, int]:
    """Post one opening investment and six transactions of one quarter, drawing each amount from rng.

    Returns the amounts posted, so that the printed comparisons use the same integers as the entries.
    """
    ledger.post(Entry(1, "owner invests cash", (Line("cash", debit=8_000_000), Line("common_stock", credit=8_000_000))))
    amounts: dict[str, int] = {}
    amounts["credit_sale"] = rng.randrange(18_000_000, 24_000_000)
    ledger.post(
        Entry(
            5,
            "sale on credit",
            (Line("accounts_receivable", debit=amounts["credit_sale"]), Line("sales", credit=amounts["credit_sale"])),
        )
    )
    amounts["cash_sale"] = rng.randrange(2_000_000, 4_000_000)
    ledger.post(
        Entry(9, "cash sale", (Line("cash", debit=amounts["cash_sale"]), Line("sales", credit=amounts["cash_sale"])))
    )
    amounts["expense_on_account"] = rng.randrange(3_000_000, 4_000_000)
    ledger.post(
        Entry(
            14,
            "operating expense incurred on account",
            (
                Line("operating_expense", debit=amounts["expense_on_account"]),
                Line("accounts_payable", credit=amounts["expense_on_account"]),
            ),
        )
    )
    amounts["expense_paid"] = rng.randrange(1_000_000, 2_000_000)
    ledger.post(
        Entry(
            20,
            "operating expense paid in cash",
            (Line("operating_expense", debit=amounts["expense_paid"]), Line("cash", credit=amounts["expense_paid"])),
        )
    )
    amounts["collection"] = ledger.balance("accounts_receivable") * 4 // 5
    ledger.post(
        Entry(
            40,
            "collection of receivables",
            (Line("cash", debit=amounts["collection"]), Line("accounts_receivable", credit=amounts["collection"])),
        )
    )
    amounts["payment"] = ledger.balance("accounts_payable") // 2
    ledger.post(
        Entry(
            58,
            "payment of payables",
            (Line("accounts_payable", debit=amounts["payment"]), Line("cash", credit=amounts["payment"])),
        )
    )
    return amounts


def main() -> None:
    ledger = Ledger()
    amounts = generate_quarter(random.Random(SEED), ledger)

    print("Journal (Dr = debit, Cr = credit; USD)")
    for entry in ledger.entries:
        for line in entry.lines:
            side, amount = ("Dr", line.debit) if line.debit else ("Cr", line.credit)
            print(f"day {entry.day:>2}  {entry.memo:<38} {side} {line.account:<20} {money(amount):>14}")
        debits = sum(x.debit for x in entry.lines)
        credits = sum(x.credit for x in entry.lines)
        print(f"        entry balances: debits {money(debits)} = credits {money(credits)}")

    print()
    print("T-accounts at the end of the quarter (USD)")
    print(f"{'account':<22}{'type':<10}{'debits':>16}{'credits':>16}{'balance':>16}")
    for account, (kind, _side) in CHART.items():
        print(
            f"{account:<22}{kind:<10}{money(ledger.debit_total(account)):>16}"
            f"{money(ledger.credit_total(account)):>16}{money(ledger.balance(account)):>16}"
        )
    total_debits = sum(ledger.debit_total(a) for a in CHART)
    total_credits = sum(ledger.credit_total(a) for a in CHART)
    print(
        f"trial balance: total debits {money(total_debits)}, total credits {money(total_credits)}, "
        f"equal: {total_debits == total_credits}"
    )

    accrual_revenue = ledger.credit_total("sales")
    cash_receipts = amounts["cash_sale"] + amounts["collection"]
    receivable_end = ledger.balance("accounts_receivable")
    print()
    print("Revenue on the accrual basis and cash received from customers (USD)")
    print(f"revenue earned (cash and credit sales)  {money(accrual_revenue):>16}")
    print(f"cash received from customers            {money(cash_receipts):>16}")
    print(f"difference                              {money(accrual_revenue - cash_receipts):>16}")
    print(f"accounts receivable at quarter end      {money(receivable_end):>16}")
    print(f"difference equals receivable: {accrual_revenue - cash_receipts == receivable_end}")

    expense_accrual = ledger.debit_total("operating_expense")
    cash_paid = amounts["expense_paid"] + amounts["payment"]
    payable_end = ledger.balance("accounts_payable")
    print()
    print("Operating expense on the accrual basis and cash paid out (USD)")
    print(f"expense recognized (accrual basis)      {money(expense_accrual):>16}")
    print(f"cash paid for operating costs           {money(cash_paid):>16}")
    print(f"difference                              {money(expense_accrual - cash_paid):>16}")
    print(f"accounts payable at quarter end         {money(payable_end):>16}")
    print(f"difference equals payable: {expense_accrual - cash_paid == payable_end}")

    print()
    print("Malformed entries are rejected and the ledger is unchanged")
    before = len(ledger.entries)
    rejected = [
        Entry(3, "unbalanced test", (Line("cash", debit=100), Line("sales", credit=99))),
        Entry(3, "unknown account test", (Line("inventory", debit=5), Line("cash", credit=5))),
        Entry(3, "fractional amount test", (Line("cash", debit=150), Line("sales", credit=1.5))),  # type: ignore[arg-type]
    ]
    for entry in rejected:
        try:
            ledger.post(entry)
        except ValueError as exc:
            print(f"ValueError: {exc}")
        else:
            print(f"accepted: {entry.memo}")
    print(f"entries before {before}, after {len(ledger.entries)}")


main()
