"""CS2 lab L06: BFS hop counts against brute force, the DFS parenthesis property, and operation counts.

SIMULATED graphs: the random graphs of Parts A, B and D are seeded undirected graphs (seed 20261028 and offsets
from it); Part C uses one fixed weighted graph written out in the code. No market data, no network, standard
library only. Vertices are 0..n-1. Adjacency lists are sorted, so every run prints the same lines.

Part A: 40 seeded graphs with 3 to 7 vertices. For every source, the BFS hop counts equal the fewest edges over
all simple paths, found by exhaustive search. Mismatches are counted.
Part B: DFS discovery and finish times on 40 further graphs, drawn the same way. For every pair of vertices the two
intervals [discovery, finish] are nested or disjoint (the parenthesis property). Violations are counted.
Part C: a 4-vertex graph with edge weights. The BFS path is the fewest hops; the lightest path is found by
exhaustive search. The two paths differ for a and c; for b they coincide.
Part D: BFS operation counts on a seeded graph with 200 vertices: vertices enqueued, adjacency entries inspected,
and the cost of the same search on an adjacency matrix, which reads one full row per dequeued vertex.
"""

from __future__ import annotations

import itertools
import random
from collections import deque

SEED = 20261028
Graph = dict[int, list[int]]


def random_graph(rng: random.Random, n: int, p: float) -> Graph:
    """An undirected graph on 0..n-1: each pair is an edge with probability p. Adjacency lists are sorted."""
    adj: Graph = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    for v in adj:
        adj[v].sort()
    return adj


def bfs(adj: Graph, source: int) -> tuple[dict[int, int], dict[int, int], list[int], int, int]:
    """Breadth-first search from source. Returns hop distances, parents, the dequeue order, the number of
    adjacency entries inspected, and the number of enqueue operations. A FIFO queue holds the discovered
    vertices not yet dequeued."""
    dist: dict[int, int] = {source: 0}
    parent: dict[int, int] = {}
    order: list[int] = []
    queue: deque[int] = deque([source])
    inspections = 0
    enqueues = 1
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in adj[v]:
            inspections += 1
            if u not in dist:
                dist[u] = dist[v] + 1
                parent[u] = v
                queue.append(u)
                enqueues += 1
    return dist, parent, order, inspections, enqueues


def brute_min_hops(adj: Graph, source: int) -> dict[int, int]:
    """The fewest edges over all simple paths from source to each reachable vertex, by exhaustive search."""
    best: dict[int, int] = {source: 0}
    on_path = {source}

    def extend(v: int, length: int) -> None:
        for u in adj[v]:
            if u in on_path:
                continue
            if length + 1 < best.get(u, 10**9):
                best[u] = length + 1
            on_path.add(u)
            extend(u, length + 1)
            on_path.remove(u)

    extend(source, 0)
    return best


def dfs_times(adj: Graph) -> tuple[dict[int, int], dict[int, int]]:
    """Recursive depth-first search over all vertices. Returns discovery and finish times on one clock.

    The clock ticks once when a vertex is discovered and once when it finishes, so the times are 1..2n."""
    discover: dict[int, int] = {}
    finish: dict[int, int] = {}
    clock = [0]

    def visit(v: int) -> None:
        clock[0] += 1
        discover[v] = clock[0]
        for u in adj[v]:
            if u not in discover:
                visit(u)
        clock[0] += 1
        finish[v] = clock[0]

    for v in sorted(adj):
        if v not in discover:
            visit(v)
    return discover, finish


def nested_or_disjoint(d: dict[int, int], f: dict[int, int], u: int, v: int) -> bool:
    """True when the intervals [d[u], f[u]] and [d[v], f[v]] are disjoint or one contains the other."""
    if f[u] < d[v] or f[v] < d[u]:
        return True
    return (d[u] < d[v] and f[v] < f[u]) or (d[v] < d[u] and f[u] < f[v])


def weighted_paths(adj: Graph, weight: dict[tuple[int, int], int], source: int) -> dict[int, tuple[int, list[int]]]:
    """For each reachable vertex, the lightest simple path from source: (total weight, path), by exhaustive search."""
    best: dict[int, tuple[int, list[int]]] = {source: (0, [source])}
    on_path = [source]

    def extend(v: int, total: int) -> None:
        for u in adj[v]:
            if u in on_path:
                continue
            step = total + weight[(min(v, u), max(v, u))]
            if u not in best or step < best[u][0]:
                best[u] = (step, [*on_path, u])
            on_path.append(u)
            extend(u, step)
            on_path.pop()

    extend(source, 0)
    return best


def part_a(rng: random.Random) -> None:
    print("Part A: BFS hop counts against exhaustive search over simple paths")
    graphs = 0
    pairs = 0
    mismatches = 0
    unreachable = 0
    sources = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = random_graph(rng, n, p)
        graphs += 1
        for source in range(n):
            sources += 1
            dist, _, _, _, _ = bfs(adj, source)
            brute = brute_min_hops(adj, source)
            pairs += len(dist)
            unreachable += n - len(dist)
            if dist != brute:
                mismatches += 1
    print(f"graphs {graphs} sources_checked {sources}")
    print(f"reachable_pairs_checked {pairs} unreachable_pairs {unreachable}")
    print(f"bfs_mismatches_against_brute_force {mismatches}")


def part_b(rng: random.Random) -> None:
    print("Part B: DFS parenthesis property on the same kind of graphs")
    graphs = 0
    pairs = 0
    violations = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = random_graph(rng, n, p)
        graphs += 1
        d, f = dfs_times(adj)
        for u in range(n):
            for v in range(u + 1, n):
                pairs += 1
                if not nested_or_disjoint(d, f, u, v):
                    violations += 1
    print(f"graphs {graphs} vertex_pairs_checked {pairs}")
    print(f"parenthesis_violations {violations}")


def part_c() -> None:
    print("Part C: fewest hops against lightest path on a weighted 4-vertex graph")
    names = ["s", "a", "b", "c"]
    adj: Graph = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    weight = {(0, 1): 10, (0, 2): 1, (1, 2): 1, (1, 3): 1}
    dist, parent, _, _, _ = bfs(adj, 0)
    light = weighted_paths(adj, weight, 0)
    for v in (1, 2, 3):
        path: list[int] = [v]
        while path[-1] != 0:
            path.append(parent[path[-1]])
        hop_path = "-".join(names[x] for x in reversed(path))
        weight_hop = sum(weight[(min(a, b), max(a, b))] for a, b in itertools.pairwise(path))
        total, light_path = light[v]
        light_text = "-".join(names[x] for x in light_path)
        print(
            f"to {names[v]}: bfs_path {hop_path} hops {dist[v]} weight {weight_hop} | "
            f"lightest_path {light_text} hops {len(light_path) - 1} weight {total}"
        )


def part_d() -> None:
    print("Part D: BFS operation counts on a seeded graph with 200 vertices")
    rng = random.Random(SEED + 1000)
    n = 200
    adj = random_graph(rng, n, 0.03)
    edges = sum(len(adj[v]) for v in adj) // 2
    dist, _, order, inspections, enqueues = bfs(adj, 0)
    reached = len(dist)
    degree_sum = sum(len(adj[v]) for v in order)
    print(f"vertices {n} edges {edges} reached_from_0 {reached}")
    once = enqueues == reached and len(set(order)) == len(order)
    print(f"enqueues {enqueues} dequeues {len(order)} each_vertex_enqueued_once {once}")
    print(f"adjacency_entries_inspected {inspections} equals_sum_of_degrees_of_reached {inspections == degree_sum}")
    print(f"matrix_row_reads_for_same_search {len(order) * n}")
    print(f"list_work_enqueues_plus_inspections {enqueues + inspections}")


def main() -> None:
    rng = random.Random(SEED)
    part_a(rng)
    part_b(rng)
    part_c()
    part_d()


main()
