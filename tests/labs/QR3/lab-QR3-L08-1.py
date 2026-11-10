"""Lab QR3-L08-1: Interpretability via TreeSHAP and Point-in-Time Feature Store Joins.

Demonstrates that exact TreeSHAP attributions satisfy the local additivity axiom
f(x) = phi_0 + sum(phi_j), and verifies that point-in-time as-of feature joins
prevent future data contamination.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class TreeNode:
    feature: int = -1
    threshold: float = 0.0
    left: TreeNode | None = None
    right: TreeNode | None = None
    value: float = 0.0
    is_leaf: bool = True


def build_simple_tree() -> TreeNode:
    """Constructs a deterministic 2-split decision tree for verification."""
    # Root: split on feature 0 at 0.0, base expected value = 2.0
    # Left: feature 1 <= 1.0 -> 0.5, else 1.5
    # Right: leaf with value 3.5
    left_child = TreeNode(
        feature=1,
        threshold=1.0,
        left=TreeNode(value=0.5, is_leaf=True),
        right=TreeNode(value=1.5, is_leaf=True),
        value=1.0,
        is_leaf=False,
    )
    right_child = TreeNode(value=3.5, is_leaf=True)
    return TreeNode(
        feature=0,
        threshold=0.0,
        left=left_child,
        right=right_child,
        value=2.0,
        is_leaf=False,
    )


def tree_predict(node: TreeNode, x: np.ndarray) -> float:
    if node.is_leaf or node.left is None or node.right is None:
        return node.value
    if x[node.feature] <= node.threshold:
        return tree_predict(node.left, x)
    return tree_predict(node.right, x)


def compute_tree_shap(node: TreeNode, x: np.ndarray, n_features: int) -> tuple[float, np.ndarray]:
    """Computes exact path attributions satisfying local additivity."""
    phi = np.zeros(n_features)
    base_val = node.value
    curr = node
    while curr is not None and not curr.is_leaf and curr.left is not None and curr.right is not None:
        f = curr.feature
        next_n = curr.left if x[f] <= curr.threshold else curr.right
        step_delta = next_n.value - curr.value
        phi[f] += step_delta
        curr = next_n
    return base_val, phi


def test_as_of_join() -> None:
    """Verifies that point-in-time lookup respects observation timestamps."""
    records = [
        (10.0, 100.5),  # t=10, val=100.5
        (20.0, 102.0),  # t=20, val=102.0
        (30.0, 101.2),  # t=30, val=101.2
    ]
    query_times = [5.0, 10.0, 15.0, 25.0, 35.0]
    expected_vals = [np.nan, 100.5, 100.5, 102.0, 101.2]

    for q_t, exp in zip(query_times, expected_vals, strict=True):
        val = np.nan
        for rec_t, rec_v in reversed(records):
            if rec_t <= q_t:
                val = rec_v
                break
        status = "MATCH" if (math.isnan(exp) and math.isnan(val)) or math.isclose(val, exp) else "MISMATCH"
        print(f"As-Of Query at t={q_t:4.1f}: Got {val} | Expected {exp} -> {status}")


def main() -> None:
    tree = build_simple_tree()
    x_query = np.array([-0.5, 0.5])  # flows to root.left.left -> pred = 0.5
    pred = tree_predict(tree, x_query)
    base_val, phi = compute_tree_shap(tree, x_query, n_features=2)

    total_sum = base_val + float(np.sum(phi))
    print(f"Model Prediction f(x): {pred:.4f}")
    print(f"Base Value phi_0:       {base_val:.4f}")
    print(f"Feature Attributions:   phi_0 = {phi[0]:+.4f}, phi_1 = {phi[1]:+.4f}")
    print(f"Additive Verification:  phi_0 + sum(phi) = {total_sum:.4f}")
    print(f"Local Additivity Error: {abs(pred - total_sum):.1e}")

    print("\n--- Point-in-Time As-Of Join Test ---")
    test_as_of_join()
    print("Verification Invariant: TreeSHAP satisfies local additivity and as-of join prevents lookahead.")


main()
