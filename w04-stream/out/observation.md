# Week 04 — Observations

## Task 1 — Stream sketches
- **Bloom filter:** No false negatives occurred because inserted bits are set and never cleared. Predicted false-positive rate was **0.861%** versus **0.835%** measured; the slight gap is consistent with sampling variation.
- **Flajolet–Martin:** I used **64 registers and log-space (geometric) averaging**, yielding **31,966 / 19,953 = 1.60×**. Using the *same hash/register results*, direct averaging of `2^R` gave **102,845 (5.15×)**, the median of R gave **21,181 (1.06×)**, and taking the median of eight groups of eight mean-R values gave **32,666 (1.64×)**. Direct averaging is especially sensitive to outliers.
- **Reservoir sampling:** I keep only **k** slots; for the i-th arriving element I randomly choose a position from **1..i**, replacing a slot if the choice is at most **k**. This remains uniform without knowing the final stream length (observed spread: **8.9%**).

## Task 2 — Exact vs. approximate counting
- On Intel Core i5-1340P / 32 GB RAM / Windows 11, exact counting became impractical at **40,000,000** stream items, requiring **139.75 seconds** and **1,331.93 MB** of peak traced memory. Execution time became the main limitation, not memory exhaustion.
- Across the original measurements (100,000–6,400,000 items), exact memory increased from **3.93 MB to 188.29 MB**, while FM memory stayed around **4–5 KB**. The observed FM accuracy ratios ranged from **1.46x to 1.90x**.
- A factor-of-two estimate may be acceptable for rough daily traffic trends, but it is insufficient for billing, financial reporting, or applications requiring exact distinct-user counts.

## Task 3 — Same memory, fewer mistakes
- With **m = 80,000** bits and **n = 8,000** insertions, the theoretical optimum is **k = (m/n) ln 2 ≈ 6.93**, so I chose **7** hashes; the expected minimum false-positive rate is **(0.6185)^10 ≈ 0.819%**.
- Under the same **80,000-bit** budget, false positives fell from **19,023/200,000 = 9.511%** to **1,663/200,000 = 0.831%** (about **91.3%** fewer), with **zero false negatives**; measured error was about **0.012 percentage points** above the theoretical minimum.
- If n were unknown, I would use a **scalable Bloom filter** that adds layers as the stream grows. Underestimating n increases false positives; overestimating n wastes memory.
