
#!/usr/bin/env python3
"""Week 4 - Task 1: Bloom Filter, Flajolet-Martin, Reservoir Sampling."""

import argparse
import random
import hashlib
import statistics


def stable_hash(item, seed, index):
    """Generate a deterministic 64-bit hash."""
    data = f"{seed}:{index}:{item}".encode("utf-8")
    digest = hashlib.blake2b(data, digest_size=8).digest()
    return int.from_bytes(digest, "big")


class BloomFilter:
    def __init__(self, m, k, seed=246):
        if m <= 0 or k <= 0:
            raise ValueError("m and k must be positive")

        self.m = m
        self.k = k
        self.seed = seed
        self.bits = bytearray((m + 7) // 8)

    def _positions(self, item):
        for i in range(self.k):
            yield stable_hash(item, self.seed, i) % self.m

    def add(self, item):
        for pos in self._positions(item):
            self.bits[pos // 8] |= 1 << (pos % 8)

    def __contains__(self, item):
        for pos in self._positions(item):
            if not (self.bits[pos // 8] & (1 << (pos % 8))):
                return False
        return True

    def expected_fp_rate(self, n_inserted):
        return (1 - (1 - 1 / self.m) ** (self.k * n_inserted)) ** self.k




def flajolet_martin(stream, n_hashes=64, seed=246):
    import hashlib

    if n_hashes <= 0:
        raise ValueError("n_hashes must be positive")

    # Number of groups (power of 2)
    m = 1 << (n_hashes - 1).bit_length()
    bucket_bits = m.bit_length() - 1
    mask = m - 1

    max_zeros = [0] * m
    seed_bytes = seed.to_bytes(8, "little")
    has_items = False

    for item in stream:
        has_items = True

        # Only ONE hash calculation per item
        digest = hashlib.blake2b(
            str(item).encode("utf-8"),
            digest_size=8,
            person=seed_bytes
        ).digest()

        h = int.from_bytes(digest, "little")

        # Assign item to one of m groups
        bucket = h & mask
        value = h >> bucket_bits

        # Count trailing zeros
        if value == 0:
            zeros = 64 - bucket_bits
        else:
            zeros = (value & -value).bit_length() - 1

        if zeros > max_zeros[bucket]:
            max_zeros[bucket] = zeros

    if not has_items:
        return 0.0

    # FM stochastic averaging: combine in log space
    avg_r = sum(max_zeros) / m
    return float(m * (2 ** avg_r) / 0.77351)

def reservoir_sample(stream, k, seed=246):
    if k < 0:
        raise ValueError("k must be non-negative")

    rng = random.Random(seed)
    sample = []

    for i, item in enumerate(stream):
        if i < k:
            sample.append(item)
        elif k > 0:
            j = rng.randrange(i + 1)

            if j < k:
                sample[j] = item

    return sample


# -------------------------------------------------- Verification
def verify():
    fails = 0
    rng = random.Random(246)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<46} {detail}")
        fails += not ok

    bf = BloomFilter(m=8192, k=5)
    inserted = [f"item-{i}" for i in range(800)]

    for x in inserted:
        bf.add(x)

    check("no false negatives", all(x in bf for x in inserted))

    absent = [f"other-{i}" for i in range(20_000)]
    fp = sum(1 for x in absent if x in bf) / len(absent)
    predicted = bf.expected_fp_rate(len(inserted))

    close = abs(fp - predicted) < max(0.02, predicted * 0.5)
    check(
        "measured false-positive rate matches theory",
        close,
        f"measured {fp:.3%}, predicted {predicted:.3%}"
    )

    distinct = 20_000
    stream = [f"k{rng.randrange(distinct)}" for _ in range(120_000)]

    est = flajolet_martin(stream)
    true_distinct = len(set(stream))
    ratio = est / true_distinct

    check(
        "distinct estimate within a factor of 2",
        0.5 <= ratio <= 2.0,
        f"estimated {est:,.0f}, true {true_distinct:,} ({ratio:.2f}x)"
    )

    counts = [0] * 20
    trials = 4000

    for t in range(trials):
        s = reservoir_sample(range(20), 5, seed=t)
        for i in s:
            counts[i] += 1

    expected = trials * 5 / 20
    spread = (max(counts) - min(counts)) / expected

    check(
        "reservoir is uniform across items",
        spread < 0.15,
        f"spread {spread:.1%} around {expected:.0f}"
    )

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
