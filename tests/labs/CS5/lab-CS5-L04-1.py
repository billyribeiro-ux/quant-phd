"""CS5 Lab L04: Template instantiation, C++20 concept constraints, and compile-time dispatch.

Standard library only. Simulates compile-time type constraint checking, concept satisfaction,
SFINAE substitution failure, and static dispatch for generic pricing kernels.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ConceptViolationError(TypeError):
    """Represents a C++20 concept constraint dissatisfaction compiler error."""

    pass


def concept_floating_point(type_obj: type) -> bool:
    """Models std::floating_point<T> concept."""
    return issubclass(type_obj, float)


def concept_arithmetic(type_obj: type) -> bool:
    """Models std::is_arithmetic_v<T> concept."""
    return issubclass(type_obj, (int, float)) and not issubclass(type_obj, bool)


def concept_payoff_functor(fn: Any, arg_type: type) -> bool:
    """Models a C++20 Payoff<F, T> concept: requires F to be invocable with T returning T."""
    if not callable(fn):
        return False
    try:
        sample_input = arg_type(100.0)
        output = fn(sample_input)
        return isinstance(output, (int, float))
    except Exception:
        return False


class GenericPricerKernel:
    """Models a template class Pricer<T> with C++20 requires clauses."""

    @classmethod
    def instantiate(cls, value_type: type, payoff_fn: Callable[[Any], Any]) -> GenericPricerKernel:
        # Constraint 1: requires std::is_arithmetic_v<T>
        if not concept_arithmetic(value_type):
            raise ConceptViolationError(
                f"Compile error: type '{value_type.__name__}' does not satisfy concept 'std::is_arithmetic_v<T>'"
            )
        # Constraint 2: requires PayoffFunctor<F, T>
        if not concept_payoff_functor(payoff_fn, value_type):
            raise ConceptViolationError(
                f"Compile error: callable does not satisfy concept 'PayoffFunctor<F, {value_type.__name__}>'"
            )
        return cls(value_type, payoff_fn)

    def __init__(self, value_type: type, payoff_fn: Callable[[Any], Any]) -> None:
        self.value_type = value_type
        self.payoff_fn = payoff_fn

    def execute_batch(self, simulated_terminal_prices: list[Any]) -> list[Any]:
        results = []
        for st in simulated_terminal_prices:
            typed_st = self.value_type(st)
            results.append(self.payoff_fn(typed_st))
        return results


def run_template_concept_experiments() -> None:
    print("CS5 L04: C++ Template Instantiation and Concept Constraint Evaluation")

    def call_payoff(s: float) -> float:
        return max(s - 100.0, 0.0)

    # Valid instantiation 1: double (float)
    kernel_double = GenericPricerKernel.instantiate(float, call_payoff)
    out_double = kernel_double.execute_batch([90.0, 105.5, 120.0])
    print(f"Instantiation <double, CallPayoff>: satisfied, evaluated {len(out_double)} points -> {out_double}")

    # Valid instantiation 2: int64 (int)
    kernel_int = GenericPricerKernel.instantiate(int, lambda s: max(s - 100, 0))
    out_int = kernel_int.execute_batch([90, 105, 120])
    print(f"Instantiation <int64_t, CallPayoff>: satisfied, evaluated {len(out_int)} points -> {out_int}")

    # Invalid instantiation 1: string (rejected by arithmetic concept)
    try:
        GenericPricerKernel.instantiate(str, call_payoff)
        print("Template: Unexpected compilation success on str")
    except ConceptViolationError as err:
        print(f"Concept constraint rejection (non-arithmetic): {err}")

    # Invalid instantiation 2: non-callable payoff functor
    try:
        GenericPricerKernel.instantiate(float, "not_a_functor")  # type: ignore[arg-type]
        print("Template: Unexpected compilation success on non-callable")
    except ConceptViolationError as err:
        print(f"Concept constraint rejection (invalid functor): {err}")


def main() -> None:
    run_template_concept_experiments()


main()
