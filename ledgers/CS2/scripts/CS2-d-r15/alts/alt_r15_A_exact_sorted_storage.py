import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._count = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._count += 1
        delta = x - self._mean
        self._mean += delta / self._count
        self._m2 += delta * (x - self._mean)

    @property
    def count(self) -> int:
        return self._count

    def mean(self) -> float:
        if self._count == 0:
            raise ValueError("the mean is undefined before the first value")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._count == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 0:
            return self._m2 / self._count
        if ddof == 1:
            if self._count < 2:
                raise ValueError("the sample variance needs at least two values")
            return self._m2 / (self._count - 1)
        raise TypeError("ddof must be 0 or 1")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        if window != int(window):
            raise ValueError("the window must be a whole number of values")
        self._window = int(window)
        self._last: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._last.append(x)
        del self._last[: max(0, len(self._last) - self._window)]

    def minimum(self) -> float:
        if not self._last:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._last)

    def maximum(self) -> float:
        if not self._last:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._last)


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._exact_epsilon = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        lo, hi = 0, len(self._sorted)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._sorted[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        self._sorted.insert(lo, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        target = max(1, math.ceil(Fraction(q) * n - self._exact_epsilon * n))
        return self._sorted[min(target, n) - 1]
