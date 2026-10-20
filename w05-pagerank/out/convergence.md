\# Task 2 — PageRank Convergence Analysis



\## A1–A3. Effect of Beta on Convergence



The experiment used a graph with 1,200 nodes and a convergence tolerance of 1e-10.



| Beta | Iterations | Time (seconds) |

|---|---:|---:|

| 0.50 | 14 | 0.0061 |

| 0.70 | 17 | 0.0089 |

| 0.85 | 20 | 0.0078 |

| 0.95 | 23 | 0.0097 |

| 0.99 | 24 | 0.0117 |



As beta increased from 0.50 to 0.99, the number of iterations increased from 14 to 24. A larger beta reduces the probability of teleportation, allowing the graph's link structure to have a stronger and longer-lasting influence on the rank distribution.



Consequently, PageRank generally converges more slowly as beta approaches 1. However, the relationship is not necessarily linear, and actual convergence depends on the graph structure.



\## A4. Effect of Graph Size



Before the experiment, I expected that a larger graph would increase total computation time substantially, while the number of iterations might remain relatively stable.



| Beta | Nodes | Iterations | Time (seconds) |

|---|---:|---:|---:|

| 0.85 | 1,200 | 20 | 0.0078 |

| 0.85 | 20,000 | 21 | 0.2041 |

| 0.95 | 1,200 | 23 | 0.0097 |

| 0.95 | 20,000 | 24 | 0.2247 |



Increasing the graph size by approximately 16.67 times increased the iteration count by only one for each beta.



However, execution time increased by approximately 26.3 times at beta = 0.85 and 23.2 times at beta = 0.95.



This demonstrates that the number of iterations depends primarily on convergence properties, while total execution time also depends on the amount of computation per iteration. The adjacency-list implementation processes nodes and edges, with approximately O(V + E) work per iteration.



\## A5. Effect of Convergence Tolerance



The experiment used beta = 0.85 and 1,200 nodes.



| Tolerance | Iterations | Time (seconds) |

|---|---:|---:|

| 1e-4 | 9 | 0.0044 |

| 1e-6 | 12 | 0.0064 |

| 1e-8 | 16 | 0.0078 |

| 1e-10 | 20 | 0.0078 |



Reducing tolerance from 1e-4 to 1e-6 required 3 additional iterations. Each further reduction by a factor of 100 required 4 additional iterations.



Overall, improving the tolerance by six decimal orders required 11 additional iterations, corresponding to approximately 1.83 extra iterations per decimal order.



A stricter tolerance produces a more stable rank estimate but increases computational work. Timing differences at this small scale may also reflect measurement noise.



\## A6. Effect of Beta on the Top-10 Ranking



The Top-10 ranking was compared using the 1,200-node graph and tolerance 1e-10.



At beta = 0.50:



1\. p00009

2\. p00001

3\. p00006

4\. p00005

5\. p00003

6\. p00002

7\. p00000

8\. p00004

9\. p00007

10\. p00008



At beta = 0.70, positions 7 and 8 were reversed: p00004 moved to 7th place and p00000 moved to 8th place.



The ranking remained identical from beta = 0.70 through beta = 0.99. All five beta values produced the same set of Top-10 pages, but their exact order was not completely stable.



Therefore, the first observed ranking change occurred at beta = 0.70.



This result shows that beta can affect the relative ordering of pages, even when the overall Top-10 membership remains unchanged. Published PageRank-based rankings may therefore depend on the choice of damping factor.



\## A7. Machine and Experimental Environment



\- CPU: 13th Gen Intel Core i5-1340P

\- RAM: 32 GB

\- Operating System: Windows 11

\- Python: 3.14.3

\- Execution environment: PowerShell terminal, using the course's synthetic graph generator

\- Other background applications: Not separately recorded



All measured convergence runs completed before the maximum limit of 500 iterations.



\## Conclusion



The results show that increasing beta generally requires more iterations, while increasing graph size primarily increases computation time per iteration. A stricter tolerance increases the iteration count, and even a small change in beta can change the relative ranking of pages. Therefore, beta, graph size, and tolerance must be considered separately when evaluating PageRank convergence.

