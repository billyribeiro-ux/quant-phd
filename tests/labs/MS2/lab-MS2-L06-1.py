"""Lab MS2-L06-1: Kirilenko Flash Crash hot-potato simulation vs Frequent Batch Auction.

Simulates the May 6, 2010 inventory-churning cascade described by Kirilenko et al. (2017)
under continuous limit orders vs discrete Frequent Batch Auctions (Budish et al. 2015).
"""

from __future__ import annotations

import random


def simulate_flash_cascade(
    large_order_size: int,
    n_hfts: int,
    hft_max_inventory: int,
    batch_interval_steps: int,
    rng: random.Random,
) -> tuple[dict[str, float], dict[str, float]]:
    """Simulate inventory dumping cascade in CLOB vs batch netting in FBA.

    Returns:
        (clob_metrics, fba_metrics)
    """
    # 1. Continuous Trading (CLOB) with hot-potato trading
    clob_price = 100.0
    clob_volume = 0
    hft_inventories = [0] * n_hfts

    # Fundamental seller sells chunks of 5
    remaining_sell = large_order_size
    price_path_clob = [clob_price]

    while remaining_sell > 0:
        chunk = min(5, remaining_sell)
        remaining_sell -= chunk

        # Order hits best bid of an HFT
        buyer = rng.randint(0, n_hfts - 1)
        hft_inventories[buyer] += chunk
        clob_volume += chunk
        clob_price -= 0.02 * chunk  # price impact

        # Check if buyer exceeded inventory limit -> hot potato selling!
        if hft_inventories[buyer] > hft_max_inventory:
            # Panic dump to another HFT
            excess = hft_inventories[buyer] - hft_max_inventory
            hft_inventories[buyer] -= excess
            other = (buyer + rng.randint(1, n_hfts - 1)) % n_hfts
            hft_inventories[other] += excess
            clob_volume += excess
            clob_price -= 0.04 * excess  # aggressive dump impact

        price_path_clob.append(clob_price)

    clob_min_price = min(price_path_clob)
    clob_drawdown = (clob_min_price - 100.0) / 100.0

    # 2. Frequent Batch Auction (FBA)
    # Orders within batch_interval_steps are batched and cleared uniformly
    fba_price = 100.0
    fba_volume = 0
    remaining_sell_fba = large_order_size
    price_path_fba = [fba_price]

    batch_chunk = 5 * batch_interval_steps
    while remaining_sell_fba > 0:
        chunk = min(batch_chunk, remaining_sell_fba)
        remaining_sell_fba -= chunk

        # In batch auction, net supply meets aggregate demand uniformly
        # No intraday panic dumping among HFTs: inventory is shared pro-rata
        fba_volume += chunk  # strictly fundamental volume, zero hot-potato churn!
        fba_price -= 0.015 * chunk
        price_path_fba.append(fba_price)

    fba_min_price = min(price_path_fba)
    fba_drawdown = (fba_min_price - 100.0) / 100.0

    clob_metrics = {
        "volume": float(clob_volume),
        "min_price": round(clob_min_price, 2),
        "drawdown_pct": round(clob_drawdown * 100.0, 2),
        "hot_potato_volume": float(clob_volume - large_order_size),
    }
    fba_metrics = {
        "volume": float(fba_volume),
        "min_price": round(fba_min_price, 2),
        "drawdown_pct": round(fba_drawdown * 100.0, 2),
        "hot_potato_volume": float(fba_volume - large_order_size),
    }

    return clob_metrics, fba_metrics


def main() -> None:
    rng = random.Random(42)
    large_order = 400
    n_hfts = 6
    max_inv = 15
    batch_steps = 4

    print("Kirilenko et al. (2017) Flash Crash vs Frequent Batch Auction (Order Size=400):")
    print("Market Architecture | Total Vol | Hot-Potato Churn | Min Price ($) | Max Drawdown")
    print("----------------------------------------------------------------------------------")

    clob, fba = simulate_flash_cascade(large_order, n_hfts, max_inv, batch_steps, rng)

    print(
        f"Continuous (CLOB)   | {int(clob['volume']):9d} | {int(clob['hot_potato_volume']):16d} | "
        f"${clob['min_price']:12.2f} | {clob['drawdown_pct']:11.2f}%"
    )
    print(
        f"Frequent Batch (FBA)| {int(fba['volume']):9d} | {int(fba['hot_potato_volume']):16d} | "
        f"${fba['min_price']:12.2f} | {fba['drawdown_pct']:11.2f}%"
    )


main()
