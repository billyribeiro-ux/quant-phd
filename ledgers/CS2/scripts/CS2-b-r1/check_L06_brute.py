"""Verifier round 1 (CS2-b): L06 Part A brute force uses a pruned search. Compare it with an unpruned
exhaustive enumeration of all simple paths on the same seeded graphs, and recount BFS mismatches.
Run: <checkout>/.venv/bin/python -I <checkout>/ledgers/CS2/scripts/CS2-b-r1/check_L06_brute.py
"""
import random
from collections import deque

SEED = 20261028


def random_graph(rng, n, p):
    adj = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    for v in adj:
        adj[v].sort()
    return adj


def bfs_dist(adj, s):
    dist = {s: 0}
    q = deque([s])
    while q:
        v = q.popleft()
        for u in adj[v]:
            if u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist


def unpruned_min_hops(adj, s):
    """Enumerate every simple path from s (no pruning) and record the fewest edges per endpoint."""
    best = {s: 0}
    stack = [(s, [s])]
    while stack:
        v, path = stack.pop()
        for u in adj[v]:
            if u in path:
                continue
            L = len(path)  # edges of the path extended by (v, u)
            if u not in best or L < best[u]:
                best[u] = L
            stack.append((u, path + [u]))
    return best


def pruned_min_hops(adj, source):
    """Copy of the lab's brute_min_hops (pruned)."""
    best = {source: 0}
    on_path = {source}

    def extend(v, length):
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


rng = random.Random(SEED)
graphs = []
for k in range(40):
    n = 3 + k % 5
    p = 0.2 + 0.1 * (k % 4)
    graphs.append(random_graph(rng, n, p))

mis_unpruned = mis_pruned = pruned_vs_unpruned_diff = 0
for adj in graphs:
    for s in adj:
        b = bfs_dist(adj, s)
        u = unpruned_min_hops(adj, s)
        p = pruned_min_hops(adj, s)
        mis_unpruned += b != u
        mis_pruned += b != p
        pruned_vs_unpruned_diff += p != u
print("graphs", len(graphs), "sources", sum(len(a) for a in graphs))
print("bfs_vs_unpruned_exhaustive_mismatches", mis_unpruned)
print("bfs_vs_lab_pruned_mismatches", mis_pruned)
print("lab_pruned_vs_unpruned_differences", pruned_vs_unpruned_diff)
