# Week 04 — Task 2: When Exact Distinct Counting Becomes Expensive

## A3. Measurements

All results below were measured on my computer using the final, one-pass stochastic-averaging Flajolet–Martin implementation. Memory is peak memory reported by `tracemalloc`, not total system RAM usage; MB means 1,000,000 bytes.

| Stream items (n) | True distinct | Exact time (s) | Exact peak (bytes) | Exact peak (MB) | FM time (s) | FM peak (bytes) | FM estimate | FM / truth |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100,000 | 36,702 | 0.15 | 3,925,492 | 3.93 | 0.75 | 4,764 | 69,718.7 | 1.90× |
| 400,000 | 146,970 | 0.60 | 11,591,174 | 11.59 | 2.97 | 4,087 | 227,007.9 | 1.54× |
| 1,600,000 | 587,625 | 2.72 | 46,647,456 | 46.65 | 17.85 | 3,999 | 860,167.5 | 1.46× |
| 6,400,000 | 2,349,909 | 11.39 | 188,287,470 | 188.29 | 68.91 | 4,706 | 3,478,136.6 | 1.48× |

The four stream sizes span **64×** (100,000 to 6,400,000). FM's peak traced memory is roughly **4–5 KB** at every size; a `0.00 MB` display in the terminal is just rounding.

## A4. Memory growth rates

With each 4× rise in n, the exact set's measured peak memory changes by **2.95×, 4.02×, and 4.04×**, respectively. Across the complete 64× stream-size range, it rises from 3.93 MB to 188.29 MB, about **47.97×**. This is consistent with approximately **O(D)** space, where D is the number of distinct elements, including the effects of Python set allocation.

Over the same 64× range, FM's peak measured memory goes from **4,764 to 4,706 bytes (0.99×)**, with intermediate values of 4,087 and 3,999 bytes. Its storage depends on the fixed **64 registers**, not the number of stream items: approximately **O(64) = O(1)** space with respect to n. Small changes in measured bytes reflect temporary allocations and measurement noise.

## A5. Accuracy versus stream size

The FM estimate/truth ratios were **1.90×, 1.54×, 1.46×, and 1.48×** as n increased. The estimate was closest at n = 1,600,000, but became slightly worse at 6,400,000; it **does not improve monotonically** with stream size. This is the accuracy cost of approximate counting with fixed memory. All four observed ratios fell within the assignment's factor-of-two tolerance.

## A6. Machine and measurement environment

- CPU: **13th Gen Intel Core i5-1340P**
- Installed RAM: **32 GB** (approximately 31.7 GiB)
- OS: **Windows 11**
- Python: **3.14.3**
- Measurement: Python `time.perf_counter()` and `tracemalloc` in the supplied `task2_limits.py`
- Other applications: PowerShell / VS Code were in use; additional background workload was not separately logged.

## A2. Where exact counting became uncomfortable

**I did not reach the exact method's failure or genuinely uncomfortable point in the measured range.** At the largest completed input, 6,400,000 stream elements, exact counting still took only **11.39 s** and peaked at **188.29 MB**. It would be incorrect to claim a time or memory limit from these data. By contrast, FM processing took **68.91 s** at this size, so the approximate method's CPU cost was already noticeable; this is **not** evidence that the exact set had reached its limit.

A larger experiment would be needed to determine the exact crossover to an impractical set size on this machine, subject to available time and RAM. The submitted measurements document the growth trend and the largest completed size rather than inventing an unobserved limit.


## Additional Experiment — Exact Method Limit (A2)

An additional experiment was conducted with 40,000,000 stream elements.

- Actual distinct elements: 14,686,717
- Exact execution time: 139.75 seconds
- Peak traced memory: 1,331.93 MB

The exact method became impractical at 40 million elements because execution
time exceeded two minutes. Memory usage increased substantially, but memory
exhaustion did not occur.

Flajolet-Martin was not measured at this size because this additional
experiment focused on finding the practical limit of exact counting.