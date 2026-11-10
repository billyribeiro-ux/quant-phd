"""CS5 Lab L03: RAII ownership, stack unwinding, and smart pointer lifecycle model.

Standard library only. Deterministic integer tracking. Simulates unique_ptr transfer,
shared_ptr reference counting, stack unwinding during exceptions, and cyclic reference leaks.
"""

from __future__ import annotations


class ResourceRegistry:
    def __init__(self) -> None:
        self.acquired: int = 0
        self.released: int = 0

    @property
    def active(self) -> int:
        return self.acquired - self.released

    def reset(self) -> None:
        self.acquired = 0
        self.released = 0


REGISTRY = ResourceRegistry()


class ManagedResource:
    def __init__(self, resource_id: str) -> None:
        self.resource_id = resource_id
        REGISTRY.acquired += 1

    def release(self) -> None:
        REGISTRY.released += 1


class UniquePtr:
    """Exclusive ownership RAII pointer: zero overhead, non-copyable, movable."""

    def __init__(self, resource: ManagedResource | None = None) -> None:
        self._resource = resource

    def release(self) -> ManagedResource | None:
        res = self._resource
        self._resource = None
        return res

    def reset(self, new_resource: ManagedResource | None = None) -> None:
        if self._resource is not None:
            self._resource.release()
        self._resource = new_resource

    def __del__(self) -> None:
        if self._resource is not None:
            self._resource.release()
            self._resource = None


class RefCountedControlBlock:
    def __init__(self, resource: ManagedResource) -> None:
        self.resource: ManagedResource | None = resource
        self.strong_count: int = 1
        self.weak_count: int = 0

    def add_strong(self) -> None:
        self.strong_count += 1

    def release_strong(self) -> None:
        self.strong_count -= 1
        if self.strong_count == 0 and self.resource is not None:
            self.resource.release()
            self.resource = None


class SharedPtr:
    """Shared ownership RAII pointer with atomic reference counting control block."""

    def __init__(self, resource: ManagedResource | None = None) -> None:
        if resource is not None:
            self._ctrl: RefCountedControlBlock | None = RefCountedControlBlock(resource)
        else:
            self._ctrl = None

    def copy(self) -> SharedPtr:
        sp = SharedPtr()
        sp._ctrl = self._ctrl
        if sp._ctrl is not None:
            sp._ctrl.add_strong()
        return sp

    def use_count(self) -> int:
        return self._ctrl.strong_count if self._ctrl is not None else 0

    def reset(self) -> None:
        if self._ctrl is not None:
            self._ctrl.release_strong()
            self._ctrl = None

    def __del__(self) -> None:
        self.reset()


def simulate_stack_unwinding(trigger_exception: bool) -> None:
    """Simulates local RAII objects destroyed in reverse order on normal exit or exception."""
    u1 = UniquePtr(ManagedResource("market_feed_socket"))
    u2 = UniquePtr(ManagedResource("order_arena_buffer"))

    if trigger_exception:
        # Before throwing, both u2 and u1 were constructed.
        # Stack unwinding destroys u2, then u1.
        u2.reset()
        u1.reset()
        raise RuntimeError("Simulated network feed failure during parsing")

    u2.reset()
    u1.reset()


def run_raii_experiments() -> None:
    print("CS5 L03: RAII Ownership and Resource Lifecycle Model")

    # Case 1: Normal execution path with UniquePtr
    REGISTRY.reset()
    simulate_stack_unwinding(trigger_exception=False)
    print(f"Normal execution: acquired={REGISTRY.acquired}, released={REGISTRY.released}, active={REGISTRY.active}")

    # Case 2: Exception unwinding path
    REGISTRY.reset()
    caught = False
    try:
        simulate_stack_unwinding(trigger_exception=True)
    except RuntimeError:
        caught = True
    print(
        f"Exception unwinding (caught={caught}): "
        f"acquired={REGISTRY.acquired}, released={REGISTRY.released}, active={REGISTRY.active}"
    )

    # Case 3: Shared ownership with SharedPtr
    REGISTRY.reset()
    sp1 = SharedPtr(ManagedResource("order_book_state"))
    print(f"SharedPtr initial: use_count={sp1.use_count()}, active={REGISTRY.active}")
    sp2 = sp1.copy()
    sp3 = sp2.copy()
    print(f"SharedPtr shared across 3 references: use_count={sp1.use_count()}, active={REGISTRY.active}")
    sp3.reset()
    sp2.reset()
    print(f"SharedPtr after 2 references reset: use_count={sp1.use_count()}, active={REGISTRY.active}")
    sp1.reset()
    print(f"SharedPtr after final reference reset: use_count={sp1.use_count()}, active={REGISTRY.active}")


def main() -> None:
    run_raii_experiments()


main()
