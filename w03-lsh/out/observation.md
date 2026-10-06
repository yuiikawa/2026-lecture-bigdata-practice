\# Week 3 Observations



\## Task 1



MinHash signatures were constructed by scanning each row once and updating all

columns containing that row. This is preferable to scanning the matrix once per

column because a one-pass approach is more suitable for large datasets that may

not fit entirely in memory.



For LSH, I decided to raise a ValueError when the signature length is not evenly

divisible by the number of bands. This prevents leftover signature rows from

being silently ignored.



For S1 and S4, the true Jaccard similarity was 2/3, while two MinHash functions

estimated the similarity as 1.0 because both signature positions matched.

Increasing the number of hash functions would reduce the variance of the

estimate, at the cost of additional computation and memory.



\## Task 2



The experiment was performed on a Windows 11 machine with a 13th Gen Intel

Core i5-1340P and 32 GB RAM. No wall-time crossover was observed within the

available dataset. At n=2000, brute force took 11.73 seconds while LSH took

46.08 seconds, although LSH required only 106 similarity comparisons compared

with 1,999,000 for brute force.



The quadratic check approximately held. When n increased from 250 to 500,

500 to 1000, and 1000 to 2000, brute-force execution time increased by about

4.18x, 5.00x, and 3.98x respectively. This is consistent with O(n^2) behavior.



The supplied synthetic-data generator produced at most 2,120 documents, so a

requested n=4000 was actually capped at 2,120 documents. At this largest actual

size, brute force used about 28.8 KiB peak traced memory and LSH used about

10.34 MiB. The experiment therefore could not be extended far enough to reach

a one-minute runtime or observe the eventual wall-time crossover without

modifying the supplied data generator.



\## Task 3



I used 120 MinHash values divided into 30 bands, giving 4 rows per band.

The approximate S-curve step is



(1 / b)^(1 / r) = (1 / 30)^(1 / 4) ≈ 0.427.



This is below the target similarity threshold of 0.6, intentionally favoring

high recall. At similarity 0.6, the candidate probability is



1 - (1 - 0.6^4)^30 ≈ 0.984.



The measured result achieved 100% recall and 100% precision while making only

122 similarity comparisons instead of 2,246,140, avoiding 99.99% of the

baseline comparisons.



Moving the S-curve step upward would make LSH more selective and reduce the

number of candidate comparisons, but it would also increase the risk of

missing pairs near the 0.6 threshold and therefore reduce recall.



The benchmark does not charge for hashing, but this simplification becomes less

realistic as the number and size of documents grow. At sufficiently large

scale, computing many MinHash values and storing signatures and buckets consumes

significant CPU time and memory, so hashing can no longer be treated as free.

