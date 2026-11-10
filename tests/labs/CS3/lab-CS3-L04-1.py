"""CS3 Lesson 4 Inline Lab 1: Pure-Python ASOF join of trades to quotes.

Demonstrates matching trade executions to the prevailing quote with non-strict
timestamp ordering (quote_t <= trade_t) and deterministic tie-breaking on insertion sequence.
Tick size: 0.01.
Data: SIMULATED trades and quotes for equity instruments.
"""

from __future__ import annotations

from decimal import Decimal
from typing import NamedTuple


class Quote(NamedTuple):
    timestamp_ms: int
    symbol: str
    bid: Decimal
    ask: Decimal
    seq: int  # Insertion order tie-breaker


class Trade(NamedTuple):
    trade_id: int
    timestamp_ms: int
    symbol: str
    price: Decimal
    quantity: int


class EnrichedTrade(NamedTuple):
    trade_id: int
    timestamp_ms: int
    symbol: str
    price: Decimal
    quantity: int
    prevailing_bid: Decimal | None
    prevailing_ask: Decimal | None
    quote_timestamp_ms: int | None
    spread_cents: int | None


def asof_join(trades: list[Trade], quotes: list[Quote]) -> list[EnrichedTrade]:
    """Execute ASOF join matching each trade to the latest quote where quote_t <= trade_t.

    Tie rule: when multiple quotes have identical timestamp, greatest seq wins.
    """
    enriched: list[EnrichedTrade] = []

    for t in trades:
        # Filter candidate quotes: matching symbol and timestamp <= trade.timestamp
        candidates = [q for q in quotes if q.symbol == t.symbol and q.timestamp_ms <= t.timestamp_ms]

        if not candidates:
            enriched.append(
                EnrichedTrade(
                    trade_id=t.trade_id,
                    timestamp_ms=t.timestamp_ms,
                    symbol=t.symbol,
                    price=t.price,
                    quantity=t.quantity,
                    prevailing_bid=None,
                    prevailing_ask=None,
                    quote_timestamp_ms=None,
                    spread_cents=None,
                )
            )
            continue

        # Sort candidate quotes by (timestamp_ms DESC, seq DESC)
        best_quote = max(candidates, key=lambda q: (q.timestamp_ms, q.seq))
        spread = round((best_quote.ask - best_quote.bid) * 100)

        enriched.append(
            EnrichedTrade(
                trade_id=t.trade_id,
                timestamp_ms=t.timestamp_ms,
                symbol=t.symbol,
                price=t.price,
                quantity=t.quantity,
                prevailing_bid=best_quote.bid,
                prevailing_ask=best_quote.ask,
                quote_timestamp_ms=best_quote.timestamp_ms,
                spread_cents=spread,
            )
        )

    return enriched


def main() -> None:
    # SIMULATED Quotes (tick size 0.01)
    quotes = [
        Quote(1000, "AAPL", Decimal("150.00"), Decimal("150.02"), seq=1),
        Quote(1050, "AAPL", Decimal("150.01"), Decimal("150.03"), seq=2),
        Quote(1050, "AAPL", Decimal("150.02"), Decimal("150.04"), seq=3),  # Tie at t=1050: seq 3 wins
        Quote(1200, "AAPL", Decimal("150.05"), Decimal("150.07"), seq=4),
        Quote(1020, "MSFT", Decimal("305.50"), Decimal("305.55"), seq=5),
    ]

    # SIMULATED Trades
    trades = [
        Trade(1, 950, "AAPL", Decimal("149.99"), 100),  # Before first AAPL quote -> None
        Trade(2, 1000, "AAPL", Decimal("150.01"), 200),  # Exact match t=1000
        Trade(3, 1075, "AAPL", Decimal("150.03"), 150),  # Follows tied quotes at 1050
        Trade(4, 1205, "AAPL", Decimal("150.06"), 300),  # Follows quote at 1200
        Trade(5, 1100, "MSFT", Decimal("305.52"), 50),  # MSFT quote at 1020
    ]

    results = asof_join(trades, quotes)

    print(f"Total trades: {len(trades)}")
    print(f"Total quotes: {len(quotes)}")
    for r in results:
        q_time = r.quote_timestamp_ms if r.quote_timestamp_ms is not None else "None"
        q_bid = f"{r.prevailing_bid:.2f}" if r.prevailing_bid is not None else "None"
        q_ask = f"{r.prevailing_ask:.2f}" if r.prevailing_ask is not None else "None"
        print(
            f"Trade {r.trade_id} [{r.symbol} t={r.timestamp_ms} px={r.price:.2f}]: "
            f"Quote t={q_time} Bid={q_bid} Ask={q_ask} Spread={r.spread_cents}c"
        )

    # Invariants verification
    # 1. Trade 1 has no prior quote
    assert results[0].prevailing_bid is None
    # 2. Trade 2 at t=1000 matches quote at t=1000
    assert results[1].quote_timestamp_ms == 1000
    # 3. Trade 3 matches tied quote with seq=3 (Bid 150.02)
    assert results[2].prevailing_bid == Decimal("150.02")
    # 4. Strict no look-ahead condition: for all matched, quote_t <= trade_t
    no_lookahead = all(r.quote_timestamp_ms is None or r.quote_timestamp_ms <= r.timestamp_ms for r in results)
    print(f"No look-ahead invariant verified: {no_lookahead}")
    print(f"Tie-breaking rule on seq verified: {results[2].prevailing_bid == Decimal('150.02')}")


if __name__ == "__main__":
    main()
