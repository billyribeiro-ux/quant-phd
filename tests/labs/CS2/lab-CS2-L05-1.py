"""CS2 lab L05: AVL insertion on seeded keys, the balance invariant, and the height bound.

SIMULATED keys: 500 distinct integers drawn from a seeded generator (seed 20261028). No market data, no
network, standard library only. Height is the number of nodes on the longest root-to-leaf path, so an empty
tree has height 0 and a single node has height 1. Every count is a count of nodes or rotations; no time is
measured, so every run prints the same lines.

Part A: insert 500 seeded keys into an AVL tree. After every insert the code checks the balance invariant
(every balance factor is -1, 0 or 1, and every stored height is correct), the in-order sequence, and the
height bound h <= log_phi(n + 1) with phi = (1 + sqrt 5) / 2. It counts single and double rotations.
Part B: the same kind of tree on the sorted keys 1..64, with a plain binary search tree beside it.
Part C: the recurrence values N(h) = 1 + N(h-1) + N(h-2) for h = 1 to 12, beside phi^h.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

SEED = 20261028
PHI = (1 + math.sqrt(5)) / 2


@dataclass
class Node:
    """A tree node. height counts the nodes on the longest path from this node down to a leaf."""

    key: int
    left: Node | None = None
    right: Node | None = None
    height: int = 1


@dataclass
class Counts:
    """Rotation calls by kind: a single rotation is one call, a double rotation is two calls."""

    single_left_left: int = 0
    single_right_right: int = 0
    double_left_right: int = 0
    double_right_left: int = 0
    rotation_calls: int = 0
    rebalances_that_rotated: int = 0


def node_height(node: Node | None) -> int:
    """The height of a subtree; the empty tree has height 0."""
    return 0 if node is None else node.height


def balance_factor(node: Node) -> int:
    """Left height minus right height. An AVL tree keeps it in {-1, 0, 1}."""
    return node_height(node.left) - node_height(node.right)


def update_height(node: Node) -> None:
    """Recompute the stored height of node from its children."""
    node.height = 1 + max(node_height(node.left), node_height(node.right))


def rotate_right(y: Node, counts: Counts) -> Node:
    """Single right rotation around y, whose left child x becomes the subtree root. Returns the new root."""
    x = y.left
    if x is None:
        raise ValueError("rotate_right needs a left child")
    y.left = x.right
    x.right = y
    update_height(y)
    update_height(x)
    counts.rotation_calls += 1
    return x


def rotate_left(x: Node, counts: Counts) -> Node:
    """Single left rotation around x, whose right child y becomes the subtree root. Returns the new root."""
    y = x.right
    if y is None:
        raise ValueError("rotate_left needs a right child")
    x.right = y.left
    y.left = x
    update_height(x)
    update_height(y)
    counts.rotation_calls += 1
    return y


def rebalance(node: Node, counts: Counts) -> Node:
    """Restore the balance factor of node to {-1, 0, 1}, using one single rotation or one double rotation."""
    update_height(node)
    factor = balance_factor(node)
    if factor > 1:
        left = node.left
        if left is None:
            raise ValueError("a left-heavy node has a left child")
        if balance_factor(left) < 0:
            node.left = rotate_left(left, counts)
            counts.double_left_right += 1
        else:
            counts.single_left_left += 1
        counts.rebalances_that_rotated += 1
        return rotate_right(node, counts)
    if factor < -1:
        right = node.right
        if right is None:
            raise ValueError("a right-heavy node has a right child")
        if balance_factor(right) > 0:
            node.right = rotate_right(right, counts)
            counts.double_right_left += 1
        else:
            counts.single_right_right += 1
        counts.rebalances_that_rotated += 1
        return rotate_left(node, counts)
    return node


def avl_insert(node: Node | None, key: int, counts: Counts) -> Node:
    """Insert a key that is not yet present, and rebalance on the way up. Raises ValueError on a duplicate."""
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = avl_insert(node.left, key, counts)
    elif key > node.key:
        node.right = avl_insert(node.right, key, counts)
    else:
        raise ValueError(f"key {key} is already present")
    return rebalance(node, counts)


def check_invariant(node: Node | None) -> tuple[bool, int]:
    """Return (ok, height). ok is True when every balance factor is in {-1, 0, 1} and every stored height is right."""
    if node is None:
        return True, 0
    ok_left, height_left = check_invariant(node.left)
    ok_right, height_right = check_invariant(node.right)
    height = 1 + max(height_left, height_right)
    factor = height_left - height_right
    ok = ok_left and ok_right and factor in (-1, 0, 1) and node.height == height
    return ok, height


def in_order(node: Node | None, out: list[int]) -> list[int]:
    """Append the keys of the subtree in increasing order and return the list."""
    if node is not None:
        in_order(node.left, out)
        out.append(node.key)
        in_order(node.right, out)
    return out


def plain_insert(node: Node | None, key: int) -> Node:
    """Insert key into an unbalanced binary search tree. No rotations are made."""
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = plain_insert(node.left, key)
    elif key > node.key:
        node.right = plain_insert(node.right, key)
    return node


def plain_height(node: Node | None) -> int:
    """The height of an unbalanced binary search tree, by a full traversal."""
    if node is None:
        return 0
    return 1 + max(plain_height(node.left), plain_height(node.right))


def height_bound(size: int) -> float:
    """log_phi(size + 1): an AVL tree with size nodes has height at most this value."""
    return math.log(size + 1) / math.log(PHI)


def min_nodes(max_height: int) -> list[int]:
    """N(h), the recurrence values N(h) = 1 + N(h-1) + N(h-2) for h = 0 to max_height."""
    values = [0, 1]
    for h in range(2, max_height + 1):
        values.append(1 + values[h - 1] + values[h - 2])
    return values[: max_height + 1]


def part_a() -> None:
    print("Part A: AVL insertion of 500 seeded distinct keys")
    rng = random.Random(SEED)
    keys = rng.sample(range(1, 1_000_000), 500)
    root: Node | None = None
    counts = Counts()
    inserts_without_rotation = 0
    max_rotations_in_one_insert = 0
    invariant_every_insert = True
    bound_every_insert = True
    order_every_insert = True
    inserted: list[int] = []
    for key in keys:
        calls_before = counts.rotation_calls
        root = avl_insert(root, key, counts)
        inserted.append(key)
        this_insert = counts.rotation_calls - calls_before
        if this_insert == 0:
            inserts_without_rotation += 1
        max_rotations_in_one_insert = max(max_rotations_in_one_insert, this_insert)
        ok, height = check_invariant(root)
        invariant_every_insert = invariant_every_insert and ok
        bound_every_insert = bound_every_insert and height <= height_bound(len(inserted))
        order_every_insert = order_every_insert and in_order(root, []) == sorted(inserted)
    print(f"invariant_after_every_insert {invariant_every_insert}")
    print(f"height_within_log_phi_n_plus_1_after_every_insert {bound_every_insert}")
    print(f"in_order_sorted_and_complete_after_every_insert {order_every_insert}")
    print(f"final_size {len(inserted)} final_height {node_height(root)}")
    print(f"log_phi_501 {height_bound(len(inserted)):.4f}")
    print(f"rotation_calls_total {counts.rotation_calls}")
    print(
        f"rotation_kinds single_left_left {counts.single_left_left} "
        f"single_right_right {counts.single_right_right} "
        f"double_left_right {counts.double_left_right} double_right_left {counts.double_right_left}"
    )
    print(f"inserts_without_rotation {inserts_without_rotation} of {len(keys)}")
    print(f"max_rotation_calls_in_one_insert {max_rotations_in_one_insert}")


def part_b() -> None:
    print("Part B: sorted keys 1..64 in a plain binary search tree and in an AVL tree")
    plain: Node | None = None
    avl: Node | None = None
    counts = Counts()
    for key in range(1, 65):
        plain = plain_insert(plain, key)
        avl = avl_insert(avl, key, counts)
    print(f"plain_bst_height {plain_height(plain)} for 64 keys inserted in increasing order")
    print(f"avl_height {node_height(avl)} for the same keys")
    print(f"avl_bound_log_phi_65 {height_bound(64):.4f}")
    ok, _ = check_invariant(avl)
    print(f"avl_invariant_holds {ok}")


def part_c() -> None:
    print("Part C: recurrence values N(h) = 1 + N(h-1) + N(h-2), beside phi^h")
    values = min_nodes(12)
    all_hold = True
    for h in range(1, 13):
        n_h = values[h]
        all_hold = all_hold and n_h + 1 >= PHI**h
        print(f"h {h} N_h {n_h} N_h_plus_1 {n_h + 1} phi_h {PHI**h:.4f}")
    print(f"N_h_plus_1_at_least_phi_h_for_h_1_to_12 {all_hold}")
    two: Node | None = None
    two_counts = Counts()
    two = avl_insert(two, 2, two_counts)
    two = avl_insert(two, 1, two_counts)
    print(f"two_node_avl_height {node_height(two)} nodes {len(in_order(two, []))} log2_2 {math.log2(2):.4f}")
    print(f"bound_constant_1_over_log2_phi {1 / math.log2(PHI):.6f}")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
