\# Week 06 — Apriori Lab Observations



\## Task 1 — Apriori and Association Rules



\- I implemented Apriori using two passes: the first counts frequent individual items, and the second counts pairs containing only frequent items.

\- This pruning reduces unnecessary candidate pairs because an infrequent item cannot belong to a frequent pair.

\- I also calculated confidence and lift. For the rule diaper → beer, confidence was 0.8, showing that 80% of baskets containing diapers also contained beer.



\## Task 2 — Support Threshold Explosion



\- As support decreased from 400 to 1, peak counters increased from 10,585 to 893,456 (84.4×), while frequent pairs increased from 249 to 893,456.

\- Candidate counters stopped increasing at support 25, but frequent pairs continued growing. This shows the difference between candidate storage and the actual number of answers.

\- At support 1, execution took 6.63 seconds and peak traced memory reached 334.3 MB. The machine's practical limit was not reached.



\## Task 3 — PCY Memory Optimization



\- I implemented PCY with 1,048,576 hash buckets. The bitmap filtered out candidate pairs whose buckets had support below the threshold.

\- Peak pair counters decreased from 820,259 to 11,359 (98.6% reduction), while all 6,397 frequent pairs were preserved exactly.

\- The bucket array itself required approximately 4 MiB, and the bitmap required 128 KiB. These costs are not included in the pair-counter score. PCY becomes beneficial in total memory when the memory saved by eliminating pair counters exceeds this fixed overhead. Smaller bucket arrays reduce fixed memory but cause more hash collisions and allow more candidate pairs through.

