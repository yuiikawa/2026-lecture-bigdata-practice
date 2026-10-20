#!/usr/bin/env python3
"""Week 5 · Task 4 (optional) — PageRank until one machine is not enough.

Textbook §5.2, and §2.3 for why iterative jobs look the way they do in MapReduce.

Task 3 made PageRank sparse, and sparse is enough for a very long time. This task
finds where "a very long time" ends on your machine, and checks whether the thing
that was slower at small scale is still running when yours has stopped.

    python3 task4_spark.py --nodes 50000            # your task 3 version
    python3 task4_spark.py --nodes 50000 --spark    # and Spark, side by side
    python3 task4_spark.py --nodes 2000000 --spark  # keep going

Optional. Not part of the assignment.
"""
import argparse, random, time, tracemalloc


def build(nodes, avg_out=8, seed=246):
    """A graph as an edge list. Deliberately not a dict - Spark cannot take one."""
    rng = random.Random(seed)
    edges = []
    hot = list(range(min(nodes, 200)))
    for v in range(nodes):
        for _ in range(max(1, int(rng.gauss(avg_out, 3)))):
            edges.append((v, rng.choice(hot) if rng.random() < 0.3
                          else rng.randrange(nodes)))
    return edges



def local_pagerank(edges, nodes, beta=0.85, iterations=10):
    """Sparse PageRank directly using the edge list.

    Time complexity: O(iterations * (V + E))
    Additional working memory: O(V)

    Includes teleportation and dangling-node redistribution.
    """
    from array import array
    import tracemalloc

    if nodes <= 0:
        local_pagerank.peak_bytes = 0
        return {}

    # Count outgoing edges without building another graph.
    degree = array("I", [0]) * nodes

    for src, _ in edges:
        degree[src] += 1

    # Initial uniform PageRank.
    ranks = [1.0 / nodes] * nodes
    weights = [0.0] * nodes

    for _ in range(iterations):
        dangling_mass = 0.0

        # Compute rank contribution per outgoing edge.
        for i, d in enumerate(degree):
            if d:
                weights[i] = beta * ranks[i] / d
            else:
                weights[i] = 0.0
                dangling_mass += ranks[i]

        # Teleportation + dangling-node redistribution.
        base = ((1.0 - beta) + beta * dangling_mass) / nodes
        new_ranks = [base] * nodes

        # Process existing edges only.
        for src, dst in edges:
            new_ranks[dst] += weights[src]

        ranks = new_ranks

    # Return the complete rank dictionary.
    result = dict(enumerate(ranks))

    # Record measured peak traced memory, when enabled.
    if tracemalloc.is_tracing():
        local_pagerank.peak_bytes = (
            tracemalloc.get_traced_memory()[1]
        )
    else:
        local_pagerank.peak_bytes = 0

    return result




def spark_pagerank(edges, nodes, beta=0.85, iterations=10):
    """Spark PageRank using reduced local parallelism.

    The original ranking algorithm is preserved.
    """

    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("w05")
        .config("spark.ui.enabled", "false")
        .config("spark.default.parallelism", "2")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    try:
        links = (
            sc.parallelize(edges, 2)
            .groupByKey()
            .mapValues(list)
            .cache()
        )

        ranks = links.mapValues(lambda _: 1.0 / nodes)

        for _ in range(iterations):
            contribs = links.join(ranks).flatMap(
                lambda kv: [
                    (dst, kv[1][1] / len(kv[1][0]))
                    for dst in kv[1][0]
                ]
            )

            ranks = (
                contribs
                .reduceByKey(lambda a, b: a + b)
                .mapValues(
                    lambda r: beta * r + (1 - beta) / nodes
                )
            )

        top = ranks.takeOrdered(
            10,
            key=lambda kv: -kv[1]
        )

        total = ranks.map(lambda kv: kv[1]).sum()

        return dict(top), total

    finally:
        spark.stop()



def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nodes", type=int, default=50_000)
    p.add_argument("--spark", action="store_true")
    p.add_argument("--iterations", type=int, default=10)
    a = p.parse_args()

    t0 = time.perf_counter()
    edges = build(a.nodes)
    print(f"\n  {a.nodes:,} nodes, {len(edges):,} edges, built in "
          f"{time.perf_counter() - t0:.1f}s\n")

    try:
        tracemalloc.start()
        t0 = time.perf_counter()
        ranks = local_pagerank(edges, a.nodes, iterations=a.iterations)
        t_local = time.perf_counter() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        top_local = sorted(ranks.items(), key=lambda kv: -kv[1])[:3]
        print(f"  single process   {t_local:8.2f}s   peak {peak / 1e6:8.1f} MB   "
              f"top={top_local[0][0]}")
    except NotImplementedError:
        print("  single process   TASK 4a not implemented")
        t_local = None
    except MemoryError:
        tracemalloc.stop()
        print("  single process   MemoryError - that is the finding. Record it.")
        t_local = None

    if a.spark:
        try:
            t0 = time.perf_counter()
            top, total = spark_pagerank(edges, a.nodes, iterations=a.iterations)
            t_spark = time.perf_counter() - t0
            first = sorted(top.items(), key=lambda kv: -kv[1])[0]
            print(f"  spark            {t_spark:8.2f}s   {'':16} "
                  f"top={first[0]}   sum={total:.4f}")
            if t_local:
                print(f"\n  spark is {t_spark / t_local:.1f}x the single process here")
        except Exception as e:
            print(f"  spark            did not run: {type(e).__name__}")
            print("  Record it in observation.md - this task is optional for exactly this reason.")
    print()


if __name__ == "__main__":
    main()
