
#!/usr/bin/env python3
"""Week 6 - Task 3: Optimized PCY Algorithm.

Reduce pair counters using hash buckets and a bitmap.
"""

from collections import Counter
from itertools import combinations
from array import array


class PlainApriori:
    """Original baseline. Do not modify."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()

        for basket in baskets:
            counts.update(basket)

        frequent = {
            i for i, c in counts.items()
            if c >= self.support
        }

        pair_counts = Counter()

        for basket in baskets:
            items = sorted(basket & frequent)

            for pair in combinations(items, 2):
                pair_counts[pair] += 1

            self.peak_counters = max(
                self.peak_counters, len(pair_counts)
            )

        return {
            frozenset(p): c
            for p, c in pair_counts.items()
            if c >= self.support
        }


class YourAlgorithm:
    """Memory-efficient PCY frequent-pair finder.

    Pass 1: Count singletons and hashed pair buckets.
    Pass 2: Count only pairs passing both filters.
    """

    def __init__(self, support, bucket_count=1 << 20):
        self.support = support
        self.bucket_count = bucket_count
        self.peak_counters = 0

        if bucket_count <= 0 or bucket_count & (bucket_count - 1):
            raise ValueError("bucket_count must be a power of two")

    def run(self, baskets):
        support = self.support
        bucket_count = self.bucket_count
        mask = bucket_count - 1

        self.peak_counters = 0

        # PASS 1: Count individual items and hash buckets.
        item_counts = Counter()

        # 4 bytes per bucket, instead of Python integer objects.
        buckets = array("I", [0]) * bucket_count

        for basket in baskets:
            item_counts.update(basket)

            for pair in combinations(sorted(basket), 2):
                bucket_index = hash(pair) & mask
                buckets[bucket_index] += 1

        # Keep only frequent individual items.
        frequent = {
            item
            for item, count in item_counts.items()
            if count >= support
        }

        # Convert bucket counts to a compact bitmap.
        bitmap = bytearray((bucket_count + 7) // 8)

        for i, count in enumerate(buckets):
            if count >= support:
                bitmap[i >> 3] |= 1 << (i & 7)

        # Release integer bucket counts before pass 2.
        del buckets

        # PASS 2: Count only candidate pairs.
        pair_counts = Counter()

        for basket in baskets:
            items = sorted(basket & frequent)

            for pair in combinations(items, 2):
                bucket_index = hash(pair) & mask

                # Skip pairs whose bucket is not frequent.
                if not (
                    bitmap[bucket_index >> 3]
                    & (1 << (bucket_index & 7))
                ):
                    continue

                pair_counts[pair] += 1

        # The number of pair counters grows monotonically.
        self.peak_counters = len(pair_counts)

        return {
            frozenset(pair): count
            for pair, count in pair_counts.items()
            if count >= support
        }
