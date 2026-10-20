
#!/usr/bin/env python3
"""Week 5 · Task 1 — PageRank and the two ways it breaks.

Textbook §5.1, §5.1.3, §5.1.4.

Optimized using adjacency lists instead of dense matrices.
Time complexity: O(iterations * (V + E))
Space complexity: O(V + E)
"""

import argparse


# Example graphs
SIMPLE = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"]
}

DEAD_END = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": []
}

SPIDER_TRAP = {
    "A": ["B"],
    "B": ["C"],
    "C": ["D"],
    "D": ["C"]
}


def pagerank(graph, beta=0.85, iterations=100, tol=1e-10):
    """Calculate PageRank with teleportation and dangling-node handling.

    beta: probability of following a link
    iterations: maximum number of iterations
    tol: L1 convergence tolerance

    Returns:
        {node: rank}

    Also stores actual iteration count in pagerank.iterations.
    """

    nodes = list(graph)
    n = len(nodes)

    if n == 0:
        pagerank.iterations = 0
        return {}

    if not 0 <= beta <= 1:
        raise ValueError("beta must be between 0 and 1")

    # Map node labels to integer indices.
    index = {node: i for i, node in enumerate(nodes)}

    # Build adjacency lists once.
    adjacency = [
        [index[v] for v in graph[u] if v in index]
        for u in nodes
    ]

    # Initial uniform PageRank distribution.
    ranks = [1.0 / n] * n

    teleport = (1.0 - beta) / n
    pagerank.iterations = 0

    for step in range(iterations):

        # Collect rank from dangling nodes.
        dangling_mass = sum(
            ranks[i]
            for i, outs in enumerate(adjacency)
            if not outs
        )

        # Teleportation plus redistribution of dangling mass.
        base = teleport + beta * dangling_mass / n
        new_ranks = [base] * n

        # Distribute rank along outgoing edges.
        for i, outs in enumerate(adjacency):
            if not outs:
                continue

            share = beta * ranks[i] / len(outs)

            for j in outs:
                new_ranks[j] += share

        # L1 distance between consecutive iterations.
        change = sum(
            abs(new_ranks[i] - ranks[i])
            for i in range(n)
        )

        ranks = new_ranks
        pagerank.iterations = step + 1

        # Stop early when converged.
        if change < tol:
            break

    return dict(zip(nodes, ranks))


def pagerank_no_teleport(graph, iterations=100):
    """Broken PageRank without teleportation.

    Dead ends lose rank.
    Spider traps absorb rank.

    This function intentionally does NOT normalize rank.
    """

    nodes = list(graph)
    n = len(nodes)

    if n == 0:
        return {}

    index = {node: i for i, node in enumerate(nodes)}

    adjacency = [
        [index[v] for v in graph[u] if v in index]
        for u in nodes
    ]

    ranks = [1.0 / n] * n

    for _ in range(iterations):
        new_ranks = [0.0] * n

        for i, outs in enumerate(adjacency):

            # Dead ends lose their rank completely.
            if not outs:
                continue

            share = ranks[i] / len(outs)

            for j in outs:
                new_ranks[j] += share

        ranks = new_ranks

    return dict(zip(nodes, ranks))


# ------------------------------------------------------------
# Verification harness
# ------------------------------------------------------------

def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails

        print(
            f"  {'ok  ' if ok else 'FAIL'}  "
            f"{label:<48} {detail}"
        )

        fails += not ok

    try:
        r = pagerank(SIMPLE)
    except NotImplementedError:
        print("  pagerank is still a stub")
        return 1

    check(
        "ranks sum to 1",
        abs(sum(r.values()) - 1) < 1e-6,
        f"{sum(r.values()):.6f}"
    )

    check(
        "every node ranked",
        set(r) == set(SIMPLE),
        sorted(r)
    )

    check(
        "C outranks A and B",
        r["C"] > r["A"] and r["C"] > r["B"],
        {k: round(v, 4) for k, v in sorted(r.items())}
    )

    try:
        broken = pagerank_no_teleport(DEAD_END)
    except NotImplementedError:
        print("  pagerank_no_teleport is still a stub")
        return 1

    check(
        "without the fix, a dead end drains the graph",
        sum(broken.values()) < 0.5,
        f"total rank {sum(broken.values()):.4f}"
    )

    fixed = pagerank(DEAD_END)

    check(
        "with the fix, rank is conserved",
        abs(sum(fixed.values()) - 1) < 1e-6,
        f"{sum(fixed.values()):.6f}"
    )

    trapped = pagerank_no_teleport(SPIDER_TRAP)

    check(
        "without the fix, a spider trap takes everything",
        trapped["C"] + trapped["D"] > 0.95,
        f"C+D = {trapped['C'] + trapped['D']:.4f}"
    )

    untrapped = pagerank(SPIDER_TRAP)

    check(
        "with the fix, A and B keep some rank",
        untrapped["A"] > 0.01 and untrapped["B"] > 0.01,
        {k: round(v, 4) for k, v in sorted(untrapped.items())}
    )

    print(
        f"\n  {'all ok' if not fails else str(fails) + ' failed'}"
    )

    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")

    a = p.parse_args()

    raise SystemExit(
        verify() if a.verify else p.print_help()
    )
