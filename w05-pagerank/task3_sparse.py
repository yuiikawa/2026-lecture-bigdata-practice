#!/usr/bin/env python3
"""Week 5 - Task 3: Efficient Sparse PageRank."""

import argparse


class DenseMatrix:
    """Original dense PageRank baseline. Do not modify."""

    def __init__(self, beta=0.85, tol=1e-10, max_iter=100):
        self.beta = beta
        self.tol = tol
        self.max_iter = max_iter

    def run(self, graph):
        nodes = list(graph)
        n = len(nodes)
        index = {v: i for i, v in enumerate(nodes)}

        M = [[0.0] * n for _ in range(n)]

        for v, outs in graph.items():
            if outs:
                share = 1.0 / len(outs)
                for w in outs:
                    M[index[w]][index[v]] = share
            else:
                for i in range(n):
                    M[i][index[v]] = 1.0 / n

        r = [1.0 / n] * n

        for self.iterations in range(1, self.max_iter + 1):
            nr = [0.0] * n

            for i in range(n):
                row = M[i]
                s = 0.0

                for j in range(n):
                    if row[j]:
                        s += row[j] * r[j]

                nr[i] = self.beta * s + (1 - self.beta) / n

            delta = sum(abs(a - b) for a, b in zip(nr, r))
            r = nr

            if delta < self.tol:
                break

        return {v: r[index[v]] for v in nodes}

    def memory_floats(self):
        return getattr(self, "_n", 0) ** 2


class YourPageRank:
    """Optimized sparse PageRank using adjacency lists.

    Time: O(iterations * (V + E))
    Rank storage: O(V)
    Sparse graph structure: O(V + E)
    """

    def __init__(self, beta=0.85, tol=1e-10, max_iter=100):
        self.beta = beta
        self.tol = tol
        self.max_iter = max_iter
        self.iterations = 0
        self._peak_floats = 0

    def run(self, graph):
        nodes = list(graph)
        n = len(nodes)

        if n == 0:
            self.iterations = 0
            self._peak_floats = 0
            return {}

        # Map node names to integer indices.
        index = {node: i for i, node in enumerate(nodes)}

        # Sparse adjacency list, created only once.
        adjacency = [
            [index[v] for v in graph[u]]
            for u in nodes
        ]

        # Precompute dangling nodes.
        dangling = [
            i for i, outs in enumerate(adjacency)
            if not outs
        ]

        # Initial uniform ranks.
        ranks = [1.0 / n] * n

        beta = self.beta
        teleport = (1.0 - beta) / n

        # Two rank vectors plus a small number of scalars.
        self._peak_floats = 2 * n + 8
        self.iterations = 0

        for iteration in range(1, self.max_iter + 1):

            # Total rank of dangling nodes.
            dangling_mass = sum(
                ranks[i] for i in dangling
            )

            # Teleportation and dangling redistribution.
            base = (
                teleport
                + beta * dangling_mass / n
            )

            new_ranks = [base] * n

            # Distribute rank only along existing edges.
            for i, outs in enumerate(adjacency):
                if not outs:
                    continue

                share = beta * ranks[i] / len(outs)

                for j in outs:
                    new_ranks[j] += share

            # L1 convergence test.
            delta = sum(
                abs(a - b)
                for a, b in zip(new_ranks, ranks)
            )

            ranks = new_ranks
            self.iterations = iteration

            if delta < self.tol:
                break

        return dict(zip(nodes, ranks))

    def memory_floats(self):
        return self._peak_floats
