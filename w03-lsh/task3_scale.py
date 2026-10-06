#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything."""

import random


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()

        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))

        return out


class YourFinder:
    """Near-duplicate finder using MinHash + LSH."""

    def __init__(self, threshold):
        self.threshold = threshold

        # 120 hash functions, split into 30 bands.
        # Therefore each band contains 4 rows.
        self.num_hashes = 120
        self.bands = 30
        self.rows_per_band = self.num_hashes // self.bands

        # Large prime used for universal hashing.
        self.prime = 4294967311

        # Fixed seed makes the experiment reproducible.
        rng = random.Random(42)

        self.hash_params = []

        for _ in range(self.num_hashes):
            a = rng.randrange(1, self.prime)
            b = rng.randrange(0, self.prime)
            self.hash_params.append((a, b))

    def _signature(self, doc):
        """Create a MinHash signature for one document."""

        if not doc:
            return [self.prime] * self.num_hashes

        signature = [self.prime] * self.num_hashes

        for shingle in doc:
            # Convert the shingle to a deterministic integer.
            if isinstance(shingle, int):
                x = shingle
            else:
                # Deterministic hash independent of Python's randomized hash().
                data = str(shingle).encode("utf-8")

                x = 2166136261
                for byte in data:
                    x ^= byte
                    x = (x * 16777619) & 0xFFFFFFFF

            for h_idx, (a, b) in enumerate(self.hash_params):
                value = (a * x + b) % self.prime

                if value < signature[h_idx]:
                    signature[h_idx] = value

        return signature

    def find(self, docs, similarity):
        """Return near-duplicate pairs using LSH candidate generation."""

        if not docs:
            return set()

        # Step 1: build MinHash signatures.
        signatures = [
            self._signature(doc)
            for doc in docs
        ]

        candidates = set()

        # Step 2: split signatures into bands.
        for band in range(self.bands):
            buckets = {}

            start = band * self.rows_per_band
            end = start + self.rows_per_band

            for i, signature in enumerate(signatures):
                band_value = tuple(signature[start:end])

                if band_value not in buckets:
                    buckets[band_value] = []

                buckets[band_value].append(i)

            # Documents in the same bucket become candidates.
            for bucket in buckets.values():
                if len(bucket) < 2:
                    continue

                for x in range(len(bucket)):
                    for y in range(x + 1, len(bucket)):
                        i = bucket[x]
                        j = bucket[y]

                        candidates.add((i, j))

        # Step 3: expensive similarity comparison ONLY for candidates.
        result = set()

        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                result.add((i, j))

        return result