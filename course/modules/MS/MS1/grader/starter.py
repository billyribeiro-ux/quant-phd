"""Starter template for the MS1 project: Spread decomposition.

Students must implement decompose_trades to satisfy the specification on project.html.
"""

from __future__ import annotations


def decompose_trades(prices: list[float], signs: list[int]) -> dict[str, float]:
    """Decompose transaction prices and trade signs into microstructure components.

    Parameters
    ----------
    prices : list[float]
        Sequential transaction prices (length >= 3).
    signs : list[int]
        Sequential trade directions, each in {-1, +1}.

    Returns
    -------
    dict[str, float]
        Dictionary with keys:
        - "roll_spread"
        - "half_spread"
        - "order_processing"
        - "adverse_selection"
        - "adverse_share"
    """
    raise NotImplementedError("Complete decompose_trades implementation.")
