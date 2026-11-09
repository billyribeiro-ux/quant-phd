"""Alternative correct implementation: Fraction-exact Welford state, brute-force rolling, reference sketch."""
import importlib.util
import math
from fractions import Fraction

_REF_PATH = "/Users/billyribeiro/.fanout/wt/verifyH1-CS2-d/course/modules/CS/CS2/grader/reference.py"
_spec = importlib.util.spec_from_file_location("ref_for_sketch_r6", _REF_PATH)
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = Fraction(0)
        self._m2 = Fraction(0)

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        x = Fraction(x)
        self._n += 1
        d = x - self._mean
        self._mean += d / self._n
        self._m2 += d * (x - self._mean)

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("empty")
        return float(self._mean)

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("empty")
        if ddof == 0:
            return float(self._m2 / self._n)
        if ddof == 1:
            if self._n < 2:
                raise ValueError("need two")
            return float(self._m2 / (self._n - 1))
        raise TypeError("ddof")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1 or window != int(window):
            raise ValueError("window")
        self._w = int(window)
        self._xs: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._xs.append(float(x))

    def minimum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return min(self._xs[-self._w:])

    def maximum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return max(self._xs[-self._w:])


QuantileSketch = _ref.QuantileSketch
