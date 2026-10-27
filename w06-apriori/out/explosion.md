\# Task 2 — Apriori Support Threshold Experiment



\## A1–A3. Experimental Results



The minimum support threshold was reduced from 400 to 1 to investigate the growth of candidate counters, frequent pairs, runtime, and memory consumption.



| Support | Frequent Pairs | Peak Counters | Time (s) | Peak Memory (MB) |

|---|---:|---:|---:|---:|

| 400 | 249 | 10,585 | 0.79 | 1.1 |

| 200 | 776 | 58,626 | 1.24 | 6.7 |

| 100 | 2,244 | 273,701 | 2.22 | 28.6 |

| 50 | 6,397 | 820,259 | 4.00 | 107.9 |

| 25 | 17,045 | 893,456 | 4.37 | 107.9 |

| 12 | 43,116 | 893,456 | 4.73 | 110.0 |

| 6 | 101,938 | 893,456 | 4.95 | 126.5 |

| 3 | 250,054 | 893,456 | 5.75 | 163.9 |

| 1 | 893,456 | 893,456 | 6.63 | 334.3 |



Nine support values were tested, spanning a 400-fold range.



\## A2. Practical Limit



At support 1, the algorithm processed 893,456 frequent pairs in 6.63 seconds, with 334.3 MB of peak traced memory.



The implementation completed successfully without memory exhaustion or excessive execution time. Therefore, the practical limit was not reached in this experiment. Support 1 was the lowest meaningful positive support threshold for this dataset.



\## A4. Growth of Candidate Counters



Reducing support from 400 to 200 increased candidate counters by 5.54 times. Further reductions from 200 to 100 and 100 to 50 increased them by 4.67 and 3.00 times, respectively.



However, after support reached 25, the counter count stopped increasing at 893,456.



Overall, the number of counters increased approximately 84.41 times from support 400 to support 1.



The growth was nonlinear, with rapid initial expansion followed by saturation of the candidate-pair space.



\## A5. Candidate Counters vs. Frequent Pairs



The number of frequent pairs increased from 249 at support 400 to 893,456 at support 1, approximately 3,588 times.



Unlike candidate counters, the frequent-pair count continued increasing even after the counters reached their maximum.



At support 25, only 17,045 of the 893,456 candidate pairs were frequent. At support 1, all 893,456 observed candidate pairs qualified as frequent.



This demonstrates that Apriori may need to maintain many candidate counters even when relatively few pairs satisfy the minimum support threshold.



The gap between candidate counters and actual frequent pairs motivates memory-efficient algorithms such as PCY, which uses hash buckets and a bitmap to reduce unnecessary pair counting.



\## A6. Machine and Environment



\- CPU: Intel Core i5-1340P

\- RAM: 32 GB

\- Operating system: Windows 11

\- Python: 3.14.3

\- Execution: PowerShell

\- Other running applications: Not systematically recorded



\## Conclusion



Lowering minimum support allows more frequent itemsets to be discovered, but it also increases candidate counting and memory usage.



In this experiment, candidate counters eventually saturated, while the number of frequent pairs continued growing. Although the system did not reach a practical processing limit, the measurements demonstrate why controlling candidate growth is important for scalable Apriori implementations.

