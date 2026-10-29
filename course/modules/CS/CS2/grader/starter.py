"""Starter for streamstats.py: the interface of the specification, with every method unimplemented.

Copy this file to streamstats.py and replace each NotImplementedError with your code. Until you do, the suite fails
on every test that calls a method you have not written, which is the intended checklist. Standard library only.
"""

from __future__ import annotations


class WelfordAccumulator:
    """Online mean and sample variance. Specification: project page, Rung 3."""

    def update(self, x: float) -> None:
        raise NotImplementedError("WelfordAccumulator.update is not written yet")

    @property
    def count(self) -> int:
        raise NotImplementedError("WelfordAccumulator.count is not written yet")

    def mean(self) -> float:
        raise NotImplementedError("WelfordAccumulator.mean is not written yet")

    def variance(self, ddof: int = 1) -> float:
        raise NotImplementedError("WelfordAccumulator.variance is not written yet")


class RollingMinMax:
    """Minimum and maximum of the last `window` values. Specification: project page, Rung 3."""

    def __init__(self, window: int) -> None:
        raise NotImplementedError("RollingMinMax.__init__ is not written yet")

    def push(self, x: float) -> None:
        raise NotImplementedError("RollingMinMax.push is not written yet")

    def minimum(self) -> float:
        raise NotImplementedError("RollingMinMax.minimum is not written yet")

    def maximum(self) -> float:
        raise NotImplementedError("RollingMinMax.maximum is not written yet")


class QuantileSketch:
    """Approximate quantiles with the rank guarantee of the specification. Specification: project page, Rung 3."""

    def __init__(self, epsilon: float) -> None:
        raise NotImplementedError("QuantileSketch.__init__ is not written yet")

    def add(self, x: float) -> None:
        raise NotImplementedError("QuantileSketch.add is not written yet")

    def quantile(self, q: float) -> float:
        raise NotImplementedError("QuantileSketch.quantile is not written yet")
