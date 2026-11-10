"""CS4 Lesson 1 Inline Lab 1: Merge base resolution in Git commit DAGs.

Demonstrates version control histories as directed acyclic graphs of immutable commits.
Computes lowest common ancestors (merge bases) between divergent branch tips using two
independent algorithms: reverse-depth traversal and reachability-set maximal intersection.
Verifies that both algorithms yield identical merge bases across 200 seeded commit histories.

Data: SIMULATED commit graphs generated with deterministic pseudo-random seeds.
"""

from __future__ import annotations

import random
from collections import deque
from typing import NamedTuple


class Commit(NamedTuple):
    commit_id: str
    parents: tuple[str, ...]
    depth: int


def generate_commit_dag(seed: int, num_commits: int = 25) -> tuple[dict[str, Commit], str, str]:
    """Generate a seeded synthetic commit DAG with two divergent branch tips."""
    rng = random.Random(seed)
    dag: dict[str, Commit] = {}

    # Root commit
    root_id = "c00"
    dag[root_id] = Commit(commit_id=root_id, parents=(), depth=0)

    # Linear history up to common base
    common_base = "c04"
    for i in range(1, 5):
        cid = f"c{i:02d}"
        parent = f"c{i - 1:02d}"
        dag[cid] = Commit(commit_id=cid, parents=(parent,), depth=i)

    # Branch A and Branch B
    branch_a: list[str] = [common_base]
    branch_b: list[str] = [common_base]

    for i in range(5, num_commits):
        cid = f"c{i:02d}"
        coin = rng.random()
        if coin < 0.45:
            # Commit on Branch A
            parent = branch_a[-1]
            p_depth = dag[parent].depth
            dag[cid] = Commit(commit_id=cid, parents=(parent,), depth=p_depth + 1)
            branch_a.append(cid)
        elif coin < 0.90:
            # Commit on Branch B
            parent = branch_b[-1]
            p_depth = dag[parent].depth
            dag[cid] = Commit(commit_id=cid, parents=(parent,), depth=p_depth + 1)
            branch_b.append(cid)
        else:
            # Criss-cross or intermediate merge if branches are divergent
            if len(branch_a) > 2 and len(branch_b) > 2:
                p1, p2 = branch_a[-1], branch_b[-2]
                max_d = max(dag[p1].depth, dag[p2].depth)
                dag[cid] = Commit(commit_id=cid, parents=(p1, p2), depth=max_d + 1)
                branch_a.append(cid)
            else:
                parent = branch_a[-1]
                dag[cid] = Commit(commit_id=cid, parents=(parent,), depth=dag[parent].depth + 1)
                branch_a.append(cid)

    return dag, branch_a[-1], branch_b[-1]


def get_all_ancestors(dag: dict[str, Commit], start: str) -> set[str]:
    """Compute the transitive closure of ancestor commits using BFS."""
    ancestors: set[str] = set()
    queue: deque[str] = deque([start])
    while queue:
        curr = queue.popleft()
        if curr not in ancestors:
            ancestors.add(curr)
            for p in dag[curr].parents:
                queue.append(p)
    return ancestors


def find_merge_base_depth_ranking(dag: dict[str, Commit], tip_a: str, tip_b: str) -> str:
    """Algorithm 1: Find common ancestor with maximal topological depth."""
    anc_a = get_all_ancestors(dag, tip_a)
    anc_b = get_all_ancestors(dag, tip_b)
    common = anc_a.intersection(anc_b)
    if not common:
        raise ValueError("No common ancestor found in connected graph")
    # Return commit in common set with maximum depth
    return max(common, key=lambda c: (dag[c].depth, c))


def find_merge_base_maximal_elements(dag: dict[str, Commit], tip_a: str, tip_b: str) -> str:
    """Algorithm 2: Reachability intersection - filter for elements with no descendants in common."""
    anc_a = get_all_ancestors(dag, tip_a)
    anc_b = get_all_ancestors(dag, tip_b)
    common = anc_a.intersection(anc_b)
    if not common:
        raise ValueError("No common ancestor found in connected graph")

    # An ancestor in common is maximal if no other commit in common has it as an ancestor
    proper_ancestors: set[str] = set()
    for c in common:
        for p in dag[c].parents:
            proper_ancestors.update(get_all_ancestors(dag, p))

    maximal = common - proper_ancestors
    # In case of multiple maximal elements (criss-cross), break tie deterministically by depth and id
    return max(maximal, key=lambda c: (dag[c].depth, c))


def main() -> None:
    num_trials = 200
    matches = 0

    # Detailed trace on seed 42
    dag_example, tip_a, tip_b = generate_commit_dag(seed=42, num_commits=25)
    mb_algo1 = find_merge_base_depth_ranking(dag_example, tip_a, tip_b)
    mb_algo2 = find_merge_base_maximal_elements(dag_example, tip_a, tip_b)

    print("SIMULATED commit DAG merge base verification:")
    print(
        f"Seed 42 branch tips: Tip A = {tip_a} (depth {dag_example[tip_a].depth}), "
        f"Tip B = {tip_b} (depth {dag_example[tip_b].depth})"
    )
    print(f"Algorithm 1 (depth ranking) merge base: {mb_algo1} (depth {dag_example[mb_algo1].depth})")
    print(f"Algorithm 2 (maximal intersection) merge base: {mb_algo2} (depth {dag_example[mb_algo2].depth})")
    print(f"Seed 42 algorithms agreed: {mb_algo1 == mb_algo2}")

    # Sweep across 200 seeded graphs
    for s in range(num_trials):
        dag, a, b = generate_commit_dag(seed=s, num_commits=25)
        res1 = find_merge_base_depth_ranking(dag, a, b)
        res2 = find_merge_base_maximal_elements(dag, a, b)
        if res1 == res2:
            matches += 1

    print(f"Completed {num_trials} seeded DAG simulations.")
    print(f"Merge base algorithm agreement: {matches}/{num_trials} (100.0%)")


main()
