
#!/usr/bin/env python3
"""Week 4 - Task 3: Same Memory, Fewer Mistakes."""

import hashlib


class NaiveFilter:
    """Original baseline filter - unchanged."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed
        self.bits = bytearray(n_bits)

    def _index(self, item):
        d = hashlib.blake2b(
            str(item).encode(),
            digest_size=8,
            key=str(self.seed).encode()
        ).digest()
        return int.from_bytes(d, "big") % self.n_bits

    def add(self, item):
        self.bits[self._index(item)] = 1

    def __contains__(self, item):
        return bool(self.bits[self._index(item)])

    def memory_bits(self):
        return self.n_bits


class YourFilter:
    """Optimized Bloom Filter using 7 hash positions."""

    def __init__(self, n_bits, seed=246):
        if n_bits < 8:
            raise ValueError("At least 8 bits are required")

        self.n_bits = (n_bits // 8) * 8
        self.seed = seed

        # Optimal k for m=80000, n=8000
        self.k = 7

        # Compact bit array: 80000 bits = 10000 bytes
        self.bits = bytearray(self.n_bits // 8)

    def _hashes(self, item):
        # Calculate two base hashes in one operation
        digest = hashlib.blake2b(
            str(item).encode("utf-8"),
            digest_size=16,
            key=str(self.seed).encode()
        ).digest()

        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:], "big") | 1

        # Double hashing creates 7 positions
        for i in range(self.k):
            yield (h1 + i * h2) % self.n_bits

    def add(self, item):
        # Set all 7 bit positions to 1
        for pos in self._hashes(item):
            byte_index = pos // 8
            bit_index = pos % 8

            self.bits[byte_index] |= (1 << bit_index)

    def __contains__(self, item):
        # If any required bit is 0, item was not inserted
        for pos in self._hashes(item):
            byte_index = pos // 8
            bit_index = pos % 8

            if not (
                self.bits[byte_index] & (1 << bit_index)
            ):
                return False

        return True

    def memory_bits(self):
        # Report all allocated bitmap bits
        return len(self.bits) * 8
