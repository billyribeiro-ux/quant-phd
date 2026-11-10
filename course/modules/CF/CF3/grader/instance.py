"""Instance generator for the CF3 Governance Scorecard project.

Deterministic from seed. Exposes make_instance(seed: int) -> dict[str, Any].
Standard library only.
"""

from __future__ import annotations

import random
from typing import Any

CORE_ENTRENCHMENT_PROVISIONS = [
    "staggered_board",
    "poison_pill",
    "golden_parachute",
    "limit_bylaw_amendment",
    "limit_charter_amendment",
    "supermajority_merger",
]

ADDITIONAL_GOVERNANCE_PROVISIONS = [
    "unequal_voting",
    "blank_check_preferred",
    "fair_price",
    "written_consent_prohibited",
]

ALL_PROVISIONS = CORE_ENTRENCHMENT_PROVISIONS + ADDITIONAL_GOVERNANCE_PROVISIONS

FIRM_NAMES = [
    "Apex Dynamics",
    "Beacon Capital",
    "Crestline Energy",
    "Delta Semiconductor",
    "Echo Logistics",
    "Falcon Healthcare",
    "Global Maritime",
    "Horizon Technologies",
    "Ironclad Materials",
    "Jupiter Media",
]


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid project instance for the given seed.

    Returns a panel of 10 corporate issuers with proxy-statement governance provisions,
    financial fundamentals in integer cents, and market valuations.
    """
    rng = random.Random(seed)
    firms: list[dict[str, Any]] = []

    # Latent cross-sectional parameters for Tobin's Q:
    # Q_i = true_alpha + true_beta * E_index_i + noise_i
    # Entrenchment (Bebchuk et al. 2008) implies true_beta < 0
    true_alpha = round(rng.uniform(2.10, 2.60), 4)
    true_beta = round(rng.uniform(-0.16, -0.08), 4)

    for i in range(10):
        firm_id = f"F{i + 1:02d}"
        name = FIRM_NAMES[i]

        # Draw binary governance provisions
        # Each provision has a calibrated empirical prevalence between 30% and 75%
        provisions: dict[str, int] = {}
        for prov in ALL_PROVISIONS:
            prob = rng.uniform(0.35, 0.70)
            provisions[prov] = 1 if rng.random() < prob else 0

        # Calculate latent E-index for data generation
        e_index = sum(provisions[p] for p in CORE_ENTRENCHMENT_PROVISIONS)
        g_index = sum(provisions[p] for p in ALL_PROVISIONS)

        # Draw financial fundamentals in integer cents
        # Assets between $500M and $5,000M
        assets_cents = int(rng.uniform(50_000_000_00, 500_000_000_00))
        # Debt leverage D/A between 15% and 55%
        debt_share = rng.uniform(0.15, 0.55)
        debt_cents = int(assets_cents * debt_share)

        # Book equity = Assets - Debt (simplified clean balance sheet)
        book_equity_cents = assets_cents - debt_cents

        # Tobin's Q = true_alpha + true_beta * e_index + epsilon
        # Stdev of residual noise ~0.35 to 0.50, creating realistic R^2 ~ 0.05 to 0.30
        noise = rng.gauss(0.0, 0.40)
        q_target = max(0.95, true_alpha + true_beta * e_index + noise)

        # Market equity derived from Q: Q = (Assets - Book Equity + Market Equity) / Assets
        # Thus Market Equity = Q * Assets - Assets + Book Equity = Q * Assets - Debt
        market_equity_cents = int(max(assets_cents * 0.40, q_target * assets_cents - debt_cents))

        # Realized empirical Tobin's Q matching the integer cents
        realized_q = round((assets_cents - book_equity_cents + market_equity_cents) / assets_cents, 4)

        sales_cents = int(assets_cents * rng.uniform(0.70, 1.40))
        capex_cents = int(assets_cents * rng.uniform(0.03, 0.09))

        firms.append(
            {
                "firm_id": firm_id,
                "name": name,
                "provisions": provisions,
                "assets_cents": assets_cents,
                "debt_cents": debt_cents,
                "book_equity_cents": book_equity_cents,
                "market_equity_cents": market_equity_cents,
                "sales_cents": sales_cents,
                "capex_cents": capex_cents,
                "target_q": realized_q,
                "latent_e_index": e_index,
                "latent_g_index": g_index,
            }
        )

    return {
        "seed": seed,
        "firms": firms,
        "core_provisions": list(CORE_ENTRENCHMENT_PROVISIONS),
        "all_provisions": list(ALL_PROVISIONS),
        "true_alpha": true_alpha,
        "true_beta": true_beta,
        "alpha_sig": 0.05,
    }
