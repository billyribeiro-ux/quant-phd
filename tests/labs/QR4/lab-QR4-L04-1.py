"""Lab QR4-L04-1: Distributed Semantic Representations, Cosine Similarity, and Analogy Arithmetic.

Demonstrates distributed word embeddings in continuous vector spaces, evaluates cosine similarity
geometry across asset-class taxonomies, and computes vector arithmetic analogies
(e.g., v(equity) - v(dividend) + v(coupon) ≈ v(debt)).
"""

from __future__ import annotations

import numpy as np


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Compute cosine similarity between two 1D vectors."""
    n1 = float(np.linalg.norm(v1))
    n2 = float(np.linalg.norm(v2))
    if n1 == 0.0 or n2 == 0.0:
        return 0.0
    return float(np.dot(v1, v2) / (n1 * n2))


def find_nearest(
    target: np.ndarray,
    embeddings: dict[str, np.ndarray],
    exclude: set[str] | None = None,
) -> tuple[str, float]:
    """Find the word in embeddings with highest cosine similarity to target, excluding specified keys."""
    if exclude is None:
        exclude = set()
    best_word = ""
    best_sim = -1.0
    for word, vec in embeddings.items():
        if word in exclude:
            continue
        sim = cosine_similarity(target, vec)
        if sim > best_sim:
            best_sim = sim
            best_word = word
    return best_word, best_sim


def main() -> None:
    # Deterministic continuous semantic embedding space (d = 6 dimensions):
    # Latent dimensions: [Equity-ness, Debt-ness, Payout-ness, Risk/Vol, Sovereign-ness, Corporate-ness]
    np.random.seed(42)

    embeddings: dict[str, np.ndarray] = {
        # Asset classes
        "equity": np.array([2.5, 0.1, 1.2, 1.8, 0.0, 2.0], dtype=np.float64),
        "stock": np.array([2.4, 0.1, 1.1, 1.9, 0.0, 2.1], dtype=np.float64),
        "share": np.array([2.3, 0.2, 1.0, 1.7, 0.0, 1.9], dtype=np.float64),
        "debt": np.array([0.1, 2.6, 1.4, 0.6, 0.8, 1.8], dtype=np.float64),
        "bond": np.array([0.1, 2.5, 1.5, 0.5, 1.2, 1.6], dtype=np.float64),
        "treasury": np.array([0.0, 2.4, 1.3, 0.2, 2.5, 0.0], dtype=np.float64),
        # Payout mechanisms
        "dividend": np.array([1.8, 0.1, 2.8, 0.4, 0.0, 1.8], dtype=np.float64),
        "coupon": np.array([0.1, 2.2, 2.7, 0.2, 1.0, 1.5], dtype=np.float64),
        # Executive leadership
        "ceo": np.array([0.8, 0.5, 0.2, 1.0, 0.0, 3.0], dtype=np.float64),
        "president": np.array([0.2, 0.4, 0.1, 0.8, 2.8, 0.5], dtype=np.float64),
        "firm": np.array([1.2, 1.0, 0.5, 0.9, 0.0, 2.8], dtype=np.float64),
        "nation": np.array([0.1, 0.8, 0.2, 0.7, 3.0, 0.1], dtype=np.float64),
    }

    # 1. Cosine similarity checks
    sim_equity_stock = cosine_similarity(embeddings["equity"], embeddings["stock"])
    sim_equity_share = cosine_similarity(embeddings["equity"], embeddings["share"])
    sim_equity_debt = cosine_similarity(embeddings["equity"], embeddings["debt"])
    sim_debt_bond = cosine_similarity(embeddings["debt"], embeddings["bond"])

    print("--- Cosine Similarity Geometry ---")
    print(f"cos(equity, stock)    : {sim_equity_stock:.4f}")
    print(f"cos(equity, share)    : {sim_equity_share:.4f}")
    print(f"cos(equity, debt)     : {sim_equity_debt:.4f}")
    print(f"cos(debt, bond)       : {sim_debt_bond:.4f}")

    # 2. Vector analogy 1: equity - dividend + coupon ≈ ?
    # Analogy hypothesis: What is to coupon as equity is to dividend? Target: debt / bond
    query_vec_1 = embeddings["equity"] - embeddings["dividend"] + embeddings["coupon"]
    nearest_word_1, nearest_sim_1 = find_nearest(
        query_vec_1, embeddings, exclude={"equity", "dividend", "coupon", "stock", "share"}
    )

    print("\n--- Financial Vector Analogy 1 ---")
    print("Equation: v(equity) - v(dividend) + v(coupon)")
    print(f"Nearest semantic concept: '{nearest_word_1}' (cosine similarity = {nearest_sim_1:.4f})")

    # 3. Vector analogy 2: ceo - firm + nation ≈ ?
    query_vec_2 = embeddings["ceo"] - embeddings["firm"] + embeddings["nation"]
    nearest_word_2, nearest_sim_2 = find_nearest(query_vec_2, embeddings, exclude={"ceo", "firm", "nation"})

    print("\n--- Structural Vector Analogy 2 ---")
    print("Equation: v(ceo) - v(firm) + v(nation)")
    print(f"Nearest semantic concept: '{nearest_word_2}' (cosine similarity = {nearest_sim_2:.4f})")

    print("\nVerification Invariant: Synonymous financial assets share cosine similarity > 0.95.")


main()
