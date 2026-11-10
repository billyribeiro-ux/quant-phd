"""CS1 lab L04: Modules, packages, and structured exception handling.

Standard library only. Tests namespace isolation, exception hierarchies, and the
try-except-else-finally control flow.
SIMULATED risk limits and portfolio bounds.
"""

from __future__ import annotations

import types


def create_synthetic_package() -> tuple[types.ModuleType, types.ModuleType]:
    """Create a synthetic package and submodule to demonstrate namespace isolation."""
    pkg = types.ModuleType("atlas_risk")
    pkg.__doc__ = "Synthetic risk package"

    submod = types.ModuleType("atlas_risk.limits")
    submod.__doc__ = "Synthetic risk limits submodule"

    def check_notional_limit(notional: float, max_notional: float) -> bool:
        if notional < 0:
            raise ValueError(f"notional cannot be negative, got {notional}")
        if notional > max_notional:
            raise ValueError(f"notional {notional} exceeds max limit {max_notional}")
        return True

    submod.check_notional_limit = check_notional_limit  # type: ignore[attr-defined]
    return pkg, submod


def execute_trade_risk_check(notional: float, max_limit: float) -> tuple[str, list[str]]:
    """Demonstrate try-except-else-finally execution order."""
    events: list[str] = []
    status: str = "unknown"
    try:
        events.append("try_start")
        if notional < 0:
            raise ValueError("negative notional")
        if notional > max_limit:
            raise ValueError("limit exceeded")
        events.append("try_passed")
    except ValueError as exc:
        events.append(f"caught_{type(exc).__name__}")
        status = f"rejected: {exc}"
    else:
        events.append("else_block")
        status = "approved"
    finally:
        events.append("finally_cleanup")

    return status, events


def main() -> None:
    # 1. Package and module namespaces
    pkg, submod = create_synthetic_package()
    print(f"package name: {pkg.__name__}")
    print(f"submodule name: {submod.__name__}")
    print(f"submodule doc: {submod.__doc__}")

    # 2. Exception inheritance hierarchy
    val_err = ValueError("test error")
    print(f"ValueError is instance of Exception: {isinstance(val_err, Exception)}")
    print(f"ValueError is instance of BaseException: {isinstance(val_err, BaseException)}")
    print(f"Exception is instance of ValueError: {isinstance(Exception(), ValueError)}")

    # 3. Successful flow (try -> else -> finally)
    status_ok, events_ok = execute_trade_risk_check(50_000.0, 100_000.0)
    print(f"trade 1 status: {status_ok}")
    print(f"trade 1 events: {','.join(events_ok)}")

    # 4. Exception flow (try -> except -> finally)
    status_fail, events_fail = execute_trade_risk_check(150_000.0, 100_000.0)
    print(f"trade 2 status: {status_fail}")
    print(f"trade 2 events: {','.join(events_fail)}")


main()
