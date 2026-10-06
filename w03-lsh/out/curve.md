\# Task 2 - Crossover Measurement



\## Machine



\- CPU: 13th Gen Intel(R) Core(TM) i5-1340P

\- RAM: 32 GB

\- OS: Windows 11

\- Python: 3.14.3

\- Other programs: PowerShell and normal background applications were running during the experiment.



\## Timing Results



| Requested n | Actual documents | Brute force time (s) | Brute comparisons | LSH time (s) | LSH comparisons |

|---:|---:|---:|---:|---:|---:|

| 250 | 250 | 0.14 | 31,125 | 4.43 | 1 |

| 500 | 500 | 0.59 | 124,750 | 10.25 | 7 |

| 1000 | 1000 | 2.95 | 499,500 | 20.28 | 27 |

| 2000 | 2000 | 11.73 | 1,999,000 | 46.08 | 106 |

| 4000 | 2120\* | 13.06 | 2,246,140 | 52.79 | 122 |



\*The supplied bench.build() generates at most 2,120 documents. Therefore, the

4000 request was capped at 2,120 actual documents. This is also confirmed by

the brute-force comparison count: 2120 \* 2119 / 2 = 2,246,140.



\## A3 - Time versus n



Brute force was faster for all tested sizes, while LSH performed dramatically

fewer similarity comparisons. For example, at 2,000 documents brute force took

11.73 s with 1,999,000 comparisons, whereas LSH took 46.08 s but required only

106 similarity comparisons.



The result shows that reducing the number of similarity comparisons does not

automatically make the complete program faster at small data sizes because LSH

also has preprocessing costs.



\## A4 - Quadratic Check



The brute-force comparison count follows n(n-1)/2, so its theoretical

complexity is O(n^2). The measured times also approximately show quadratic

growth.



\- 250 -> 500: 0.14 s -> 0.59 s, approximately 4.18x

\- 500 -> 1000: 0.59 s -> 2.95 s, approximately 5.00x

\- 1000 -> 2000: 2.95 s -> 11.73 s, approximately 3.98x



Thus, doubling n generally increased brute-force time by approximately four

times. The measurements are consistent with quadratic behavior, allowing for

normal timing variation.



The requested 4000 point was excluded from this doubling check because the

provided synthetic-data generator contains only 2,120 documents.



\## A5 - Peak Memory



At the largest actual dataset of 2,120 documents:



\- Brute force peak traced memory: 29,480 bytes (about 28.8 KiB)

\- LSH peak traced memory: 10,836,688 bytes (about 10.34 MiB)



LSH used substantially more memory because it stores MinHash signatures and

LSH buckets, while brute force compares pairs directly without maintaining

these additional structures.



\## A6 - Machine Information



The experiment was performed on Windows 11 with a 13th Gen Intel Core i5-1340P

and 32 GB of RAM using Python 3.14.3. PowerShell and normal background

applications were running during the measurements.



\## A7 - Crossover



No wall-time crossover was observed within the available dataset.



At every tested actual size, brute force was faster than LSH. At 2,000

documents, brute force took 11.73 s while LSH took 46.08 s. The supplied

generator limits the dataset to 2,120 documents, so a larger experiment could

not be performed without modifying the provided benchmark data generator.



Although there was no wall-time crossover in this range, LSH already reduced

the number of expensive similarity comparisons dramatically: 106 comparisons

instead of 1,999,000 at n=2,000.



\## A8 - Why LSH Loses at Small n



LSH performs additional work before making similarity comparisons. It must

compute a 120-value MinHash signature for every document, divide the signatures

into 30 bands, construct buckets, and generate candidate pairs.



These preprocessing operations are approximately linear with the number of

documents, but their constant cost is significant. For small datasets,

brute-force comparison is still cheap enough that this preprocessing overhead

costs more than simply comparing every pair. As n becomes much larger, the

quadratic number of brute-force comparisons should eventually dominate, while

LSH can restrict expensive similarity comparisons to a small candidate set.

