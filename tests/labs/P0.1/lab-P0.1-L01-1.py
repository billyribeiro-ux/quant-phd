"""Lab 1 (L01): Navigating an inline prerequisite DAG and computing topological ordering.

Standard library only. This lab defines an inline curriculum subgraph (a declared subset of program
modules and their prerequisite edges), performs cycle detection via Kahn's algorithm, computes a
deterministic topological sort order, calculates the transitive prerequisite closure for downstream
modules, and identifies the unlock set (all reachable downstream modules) of an entry node.
"""

from __future__ import annotations

# Declarative inline prerequisite DAG: child module -> list of direct prerequisite parents.
GRAPH: dict[str, list[str]] = {
    "P0.1": [],
    "P0.2": ["P0.1"],
    "M1": ["P0.1"],
    "M2": ["M1"],
    "M3": ["M2"],
    "CS1": ["P0.1"],
    "M4": ["M2"],
    "S0": ["CS1", "M4"],
    "AC1": ["P0.1"],
    "AC2": ["AC1", "S0"],
}


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm with deterministic alphabetical tie-breaking."""
    in_degree: dict[str, int] = {u: len(graph[u]) for u in graph}
    adj: dict[str, list[str]] = {u: [] for u in graph}
    for u, prereqs in graph.items():
        for p in prereqs:
            adj[p].append(u)

    ready: list[str] = sorted([u for u in graph if in_degree[u] == 0])
    order: list[str] = []
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in sorted(adj[u]):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                ready.append(v)
                ready.sort()

    if len(order) != len(graph):
        raise ValueError("Cycle detected in prerequisite graph")
    return order


def prerequisite_closure(graph: dict[str, list[str]], target: str) -> set[str]:
    """Transitive closure of all antecedents required before target can be studied."""
    visited: set[str] = set()
    stack: list[str] = list(graph.get(target, []))
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph.get(node, []))
    return visited


def unlock_set(graph: dict[str, list[str]], source: str) -> set[str]:
    """Transitive set of all downstream nodes reachable from source."""
    adj: dict[str, list[str]] = {u: [] for u in graph}
    for u, prereqs in graph.items():
        for p in prereqs:
            adj[p].append(u)

    visited: set[str] = set()
    stack: list[str] = list(adj.get(source, []))
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(adj.get(node, []))
    return visited


def verify_topological_invariants(graph: dict[str, list[str]], order: list[str]) -> bool:
    """Verify that every prerequisite appears before its dependent module in order."""
    pos: dict[str, int] = {node: i for i, node in enumerate(order)}
    for node, prereqs in graph.items():
        for p in prereqs:
            if pos[p] >= pos[node]:
                return False
    return True


def main() -> None:
    print("Prerequisite DAG Analysis (inline curriculum subset)")
    print(f"Total modules: {len(GRAPH)}")

    order = topological_sort(GRAPH)
    valid = verify_topological_invariants(GRAPH, order)
    print("Cycles detected: 0")
    print(f"Topological order ({len(order)} nodes): {' -> '.join(order)}")
    print(f"Topological ordering invariant satisfied: {valid}")

    p02_closure = prerequisite_closure(GRAPH, "P0.2")
    print(f"Prerequisite closure for P0.2 ({len(p02_closure)} modules): {sorted(p02_closure)}")

    ac2_closure = prerequisite_closure(GRAPH, "AC2")
    print(f"Prerequisite closure for AC2 ({len(ac2_closure)} modules): {sorted(ac2_closure)}")

    p01_unlocks = unlock_set(GRAPH, "P0.1")
    print(f"Downstream modules unlocked by P0.1 ({len(p01_unlocks)} modules): {sorted(p01_unlocks)}")


main()
