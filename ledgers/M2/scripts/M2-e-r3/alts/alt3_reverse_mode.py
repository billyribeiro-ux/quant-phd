"""Alternative 3 (reverse mode): ad_derivative records a tape of operations and back-propagates from the output."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from reference_core import bond_price_cents, fd_derivative, hessian_fd, sensitivities


class _Node:
    __slots__ = ("parents", "value")

    def __init__(self, value: float, parents: list[tuple[_Node, float]]) -> None:
        self.value = value
        self.parents = parents

    def __add__(self, other: Any) -> _Node:
        o = _lift(other)
        return _Node(self.value + o.value, [(self, 1.0), (o, 1.0)])

    __radd__ = __add__

    def __sub__(self, other: Any) -> _Node:
        o = _lift(other)
        return _Node(self.value - o.value, [(self, 1.0), (o, -1.0)])

    def __rsub__(self, other: Any) -> _Node:
        o = _lift(other)
        return _Node(o.value - self.value, [(o, 1.0), (self, -1.0)])

    def __mul__(self, other: Any) -> _Node:
        o = _lift(other)
        return _Node(self.value * o.value, [(self, o.value), (o, self.value)])

    __rmul__ = __mul__


def _lift(x: Any) -> _Node:
    return x if isinstance(x, _Node) else _Node(float(x), [])


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    root = _Node(float(x), [])
    out = _lift(f(root))
    adjoint: dict[int, float] = {id(root): 0.0}
    order: list[_Node] = []
    seen: set[int] = set()

    def visit(node: _Node) -> None:
        if id(node) in seen:
            return
        seen.add(id(node))
        for parent, _ in node.parents:
            visit(parent)
        order.append(node)

    visit(out)
    grads: dict[int, float] = {id(out): 1.0}
    for node in reversed(order):
        g = grads.get(id(node), 0.0)
        for parent, partial in node.parents:
            grads[id(parent)] = grads.get(id(parent), 0.0) + g * partial
    return float(grads.get(id(root), 0.0))
