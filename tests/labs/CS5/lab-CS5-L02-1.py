"""CS5 Lab L02: Value semantics, object lifecycle, and move semantics operational model.

Standard library only. Deterministic integer operation counter. Tracks default construction,
copy construction, move construction, copy assignment, move assignment, and destruction
across dynamic container reallocations and value transfers.
"""

from __future__ import annotations


class LifecycleTracker:
    def __init__(self) -> None:
        self.default_constructs = 0
        self.copy_constructs = 0
        self.move_constructs = 0
        self.copy_assigns = 0
        self.move_assigns = 0
        self.destructs = 0

    def reset(self) -> None:
        self.default_constructs = 0
        self.copy_constructs = 0
        self.move_constructs = 0
        self.copy_assigns = 0
        self.move_assigns = 0
        self.destructs = 0


GLOBAL_TRACKER = LifecycleTracker()


class TracedValue:
    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.is_moved_from = False
        GLOBAL_TRACKER.default_constructs += 1

    @classmethod
    def from_value(cls, value: int) -> TracedValue:
        return cls(value)

    def copy(self) -> TracedValue:
        GLOBAL_TRACKER.copy_constructs += 1
        return TracedValue(self.value)

    def move(self) -> TracedValue:
        GLOBAL_TRACKER.move_constructs += 1
        val = self.value
        self.is_moved_from = True
        self.value = 0
        return TracedValue(val)

    def destroy(self) -> None:
        GLOBAL_TRACKER.destructs += 1


class SimulatedVector:
    """Models std::vector dynamic reallocation behavior with geometric capacity doubling."""

    def __init__(self, use_noexcept_move: bool = True) -> None:
        self.capacity = 0
        self.data: list[TracedValue] = []
        self.use_noexcept_move = use_noexcept_move

    def push_back_lvalue(self, item: TracedValue) -> None:
        self._ensure_capacity()
        self.data.append(item.copy())

    def push_back_rvalue(self, item: TracedValue) -> None:
        self._ensure_capacity()
        self.data.append(item.move())

    def _ensure_capacity(self) -> None:
        if len(self.data) < self.capacity:
            return
        new_cap = 1 if self.capacity == 0 else self.capacity * 2
        new_data: list[TracedValue] = []
        for x in self.data:
            if self.use_noexcept_move:
                new_data.append(x.move())
            else:
                new_data.append(x.copy())
            x.destroy()
        self.data = new_data
        self.capacity = new_cap

    def clear(self) -> None:
        for x in self.data:
            x.destroy()
        self.data = []


def run_value_semantics_experiments() -> None:
    print("CS5 L02: Value Semantics and Move vs Copy Reallocation Tracker")

    # Sequence 1: push_back 8 rvalue items with noexcept move
    GLOBAL_TRACKER.reset()
    vec_move = SimulatedVector(use_noexcept_move=True)
    for i in range(8):
        v = TracedValue(i * 10)
        vec_move.push_back_rvalue(v)
        v.destroy()

    print(
        f"Push 8 rvalues (noexcept move): "
        f"moves={GLOBAL_TRACKER.move_constructs}, copies={GLOBAL_TRACKER.copy_constructs}, "
        f"destructs={GLOBAL_TRACKER.destructs}, capacity={vec_move.capacity}"
    )
    vec_move.clear()

    # Sequence 2: push_back 8 rvalue items without noexcept move (reallocations fall back to copy)
    GLOBAL_TRACKER.reset()
    vec_copy = SimulatedVector(use_noexcept_move=False)
    for i in range(8):
        v = TracedValue(i * 10)
        vec_copy.push_back_rvalue(v)
        v.destroy()

    print(
        f"Push 8 rvalues (copy on realloc): "
        f"moves={GLOBAL_TRACKER.move_constructs}, copies={GLOBAL_TRACKER.copy_constructs}, "
        f"destructs={GLOBAL_TRACKER.destructs}, capacity={vec_copy.capacity}"
    )
    vec_copy.clear()

    # Sequence 3: push_back 8 lvalue items (always deep copied at insertion)
    GLOBAL_TRACKER.reset()
    vec_lvalue = SimulatedVector(use_noexcept_move=True)
    for i in range(8):
        v = TracedValue(i * 10)
        vec_lvalue.push_back_lvalue(v)
        v.destroy()

    print(
        f"Push 8 lvalues (deep copies): "
        f"moves={GLOBAL_TRACKER.move_constructs}, copies={GLOBAL_TRACKER.copy_constructs}, "
        f"destructs={GLOBAL_TRACKER.destructs}, capacity={vec_lvalue.capacity}"
    )
    vec_lvalue.clear()


def main() -> None:
    run_value_semantics_experiments()


main()
