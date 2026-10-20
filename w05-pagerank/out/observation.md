\# Week 05 — PageRank Lab Observations



\## Task 1 — PageRank, Dead Ends, and Spider Traps



\- Without teleportation, rank reaching a dead end disappears, causing the total rank to approach zero. I fixed this by redistributing dangling-node rank uniformly across all nodes.

\- Spider traps absorb rank because their outgoing links remain inside the trap. Teleportation prevents permanent trapping by allowing the surfer to jump to any page.

\- With beta = 0.85, the surfer follows an outgoing link with probability 85% and teleports with probability 15%. The corrected algorithm conserves total rank at 1.0.



\## Task 2 — PageRank Convergence



\- As beta increased from 0.50 to 0.99, convergence iterations increased from 14 to 24 because less frequent teleportation slows mixing.

\- Increasing the graph from 1,200 to 20,000 nodes increased iterations only from 20 to 21 at beta = 0.85, while runtime increased from 0.0078 to 0.2041 seconds due to greater computation per iteration.

\- The Top-10 membership remained unchanged, but p00000 and p00004 swapped positions for the first time at beta = 0.70. This shows that rankings can depend on the damping factor.



\## Task 3 — Efficient Sparse PageRank



\- Instead of storing a dense n × n transition matrix, I used adjacency lists and two rank vectors, holding 2n + 8 floating-point values during iteration. The adjacency structure additionally stores node and edge indices.

\- Teleportation and dead-end redistribution require only a shared base value added to each node, so no dense matrix is necessary.

\- The sparse implementation was 98.9 times faster and used 598 times fewer stored floats. Its worst per-node difference from the dense result was 1.18e-15, attributable to floating-point calculation order rather than a change in the algorithm.

## Task 4 — Optional Spark PageRank



\- Single-process PageRank completed 1,000, 5,000, and 50,000 nodes, with runtime increasing from 0.03 to 3.05 seconds and traced peak memory from 0.2 to 8.7 MB.

\- Spark failed with a Python worker error, so no valid Spark performance ratio could be measured. The single-process memory or time limit was not reached.

\- The provided Spark implementation may lose rank mass because dangling-node rank is not redistributed and some nodes may disappear from the RDD. A corrected version would preserve all nodes and redistribute dangling mass. Spark becomes useful when the workload is large enough to justify distributed-processing overhead.

