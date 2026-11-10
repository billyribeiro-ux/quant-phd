"""Lab X1-L01-1: Covered Interest Parity (CIP) no-arbitrage bounds simulator.

Calculates synthetic forward rates and tests no-arbitrage boundaries given
bid-ask spreads in spot FX, forward FX, and money market deposit rates.
"""

from __future__ import annotations


def check_cip_arbitrage(
    spot_bid: float,
    spot_ask: float,
    forward_bid: float,
    forward_ask: float,
    rate_usd_lend: float,
    rate_usd_borrow: float,
    rate_eur_lend: float,
    rate_eur_borrow: float,
    tenor_years: float = 1.0,
) -> dict[str, float | bool]:
    """Calculate synthetic forward bounds and test CIP arbitrage profitability.

    Rates are simple annualized money-market rates for tenor tau.
    Quotes are EUR/USD (USD per 1 EUR).
    """
    # Strategy 1: Synthetic Forward Borrowing (Borrow EUR, Lend USD)
    # Borrow 1 EUR at rate_eur_borrow, convert to USD at spot_bid -> spot_bid USD.
    # Lend USD at rate_usd_lend -> spot_bid * (1 + rate_usd_lend * tau) USD at maturity.
    # Repay EUR debt: (1 + rate_eur_borrow * tau) EUR.
    # Implied synthetic forward rate to buy EUR forward:
    f_synth_upper = (spot_bid * (1.0 + rate_usd_lend * tenor_years)) / (1.0 + rate_eur_borrow * tenor_years)

    # Strategy 2: Synthetic Forward Lending (Borrow USD, Lend EUR)
    # Borrow USD at rate_usd_borrow to buy 1 EUR at spot_ask -> spot_ask USD debt.
    # Lend 1 EUR at rate_eur_lend -> (1 + rate_eur_lend * tau) EUR at maturity.
    # Debt repayment at maturity: spot_ask * (1 + rate_usd_borrow * tau) USD.
    # Implied synthetic forward rate to sell EUR forward:
    f_synth_lower = (spot_ask * (1.0 + rate_usd_borrow * tenor_years)) / (1.0 + rate_eur_lend * tenor_years)

    # Arbitrage tests:
    # 1. Borrow Synthetic, Sell Forward: profitable if forward_bid > f_synth_lower
    # 2. Lend Synthetic, Buy Forward: profitable if forward_ask < f_synth_upper
    arb_borrow = forward_bid > f_synth_lower
    arb_lend = forward_ask < f_synth_upper
    arbitrage_exists = arb_borrow or arb_lend

    return {
        "f_synth_lower": round(f_synth_lower, 5),
        "f_synth_upper": round(f_synth_upper, 5),
        "forward_bid": forward_bid,
        "forward_ask": forward_ask,
        "arbitrage_exists": arbitrage_exists,
    }


def main() -> None:
    print("Lab X1-L01-1 | Covered Interest Parity Arbitrage Bounds Simulator")
    print("------------------------------------------------------------------")

    # Scenario 1: Normal market conditions (tight spreads, no arbitrage)
    # Spot EUR/USD = 1.0850 / 1.0852, USD rate = 5.00% / 5.05%, EUR rate = 3.50% / 3.55%
    res1 = check_cip_arbitrage(
        spot_bid=1.0850,
        spot_ask=1.0852,
        forward_bid=1.1005,
        forward_ask=1.1009,
        rate_usd_lend=0.0500,
        rate_usd_borrow=0.0505,
        rate_eur_lend=0.0350,
        rate_eur_borrow=0.0355,
        tenor_years=1.0,
    )
    print("Scenario 1 (Normal Markets):")
    print(f"  Synthetic No-Arb Band: [{res1['f_synth_upper']:.5f}, {res1['f_synth_lower']:.5f}]")
    print(f"  Quoted Forward Market: [{res1['forward_bid']:.5f}, {res1['forward_ask']:.5f}]")
    print(f"  Arbitrage Profitable:  {res1['arbitrage_exists']}")

    # Scenario 2: Severe funding dislocation (CIP deviation / basis dislocation)
    # Forward bid rises to 1.1050, breaking upper boundary
    res2 = check_cip_arbitrage(
        spot_bid=1.0850,
        spot_ask=1.0852,
        forward_bid=1.1050,
        forward_ask=1.1054,
        rate_usd_lend=0.0500,
        rate_usd_borrow=0.0505,
        rate_eur_lend=0.0350,
        rate_eur_borrow=0.0355,
        tenor_years=1.0,
    )
    print("Scenario 2 (Dislocated Markets):")
    print(f"  Synthetic No-Arb Band: [{res2['f_synth_upper']:.5f}, {res2['f_synth_lower']:.5f}]")
    print(f"  Quoted Forward Market: [{res2['forward_bid']:.5f}, {res2['forward_ask']:.5f}]")
    print(f"  Arbitrage Profitable:  {res2['arbitrage_exists']}")


main()
