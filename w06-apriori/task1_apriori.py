#!/usr/bin/env python3
"""Week 6 - Task 1: Optimized A-Priori and Association Rules."""

import argparse
from collections import Counter
from itertools import combinations


BASKETS = [
    {"bread", "milk"},
    {"bread", "diaper", "beer", "egg"},
    {"milk", "diaper", "beer", "cola"},
    {"bread", "milk", "diaper", "beer"},
    {"bread", "milk", "diaper", "cola"},
    {"bread", "milk", "beer"},
    {"diaper", "beer"},
]


def frequent_singletons(baskets, support):
    """Pass 1: Count individual items."""
    counts = Counter()

    for basket in baskets:
        counts.update(set(basket))

    return {
        item: count
        for item, count in counts.items()
        if count >= support
    }


def _apriori_counts(baskets, support):
    """Two passes with candidate pruning."""

    # Pass 1: Count all individual items.
    item_counts = Counter()

    for basket in baskets:
        item_counts.update(set(basket))

    frequent = {
        item
        for item, count in item_counts.items()
        if count >= support
    }

    # Pass 2: Count only pairs of frequent items.
    pair_counts = Counter()

    for basket in baskets:
        eligible = sorted(set(basket) & frequent)
        pair_counts.update(combinations(eligible, 2))

    pairs = {
        frozenset(pair): count
        for pair, count in pair_counts.items()
        if count >= support
    }

    return item_counts, pairs


def frequent_pairs(baskets, support):
    """Return frequent item pairs using A-Priori."""
    _, pairs = _apriori_counts(baskets, support)
    return pairs


def association_rules(baskets, support, min_confidence):
    """Generate association rules with confidence and lift."""

    item_counts, pairs = _apriori_counts(baskets, support)
    n = len(baskets)

    if n == 0:
        return []

    rules = []

    for pair, pair_count in pairs.items():
        a, b = tuple(pair)

        # Confidence is directional.
        for antecedent, consequent in ((a, b), (b, a)):

            confidence = (
                pair_count / item_counts[antecedent]
            )

            if confidence < min_confidence:
                continue

            consequent_support = (
                item_counts[consequent] / n
            )

            lift = confidence / consequent_support

            rules.append((
                antecedent,
                consequent,
                confidence,
                lift
            ))

    rules.sort(
        key=lambda r: (-r[2], str(r[0]), str(r[1]))
    )

    return rules


# ------------------------------------------------------------
# Verification
# ------------------------------------------------------------

def verify():
    fails = 0

    def check(label, got, want):
        nonlocal fails
        ok = got == want

        print(
            f"  {'ok  ' if ok else 'FAIL'}  "
            f"{label:<44} {got}"
            + (
                ""
                if ok
                else f"\n{'':>54}want {want}"
            )
        )

        fails += not ok

    try:
        singles = frequent_singletons(BASKETS, 3)
    except NotImplementedError:
        print("  frequent_singletons is still a stub")
        return 1

    check(
        "frequent singletons at support 3",
        dict(sorted(singles.items())),
        {
            "beer": 5,
            "bread": 5,
            "diaper": 5,
            "milk": 5
        }
    )

    try:
        pairs = frequent_pairs(BASKETS, 3)
    except NotImplementedError:
        print("  frequent_pairs is still a stub")
        return 1

    got = {
        tuple(sorted(k)): v
        for k, v in pairs.items()
    }

    check(
        "frequent pairs at support 3",
        dict(sorted(got.items())),
        {
            ("beer", "bread"): 3,
            ("beer", "diaper"): 4,
            ("beer", "milk"): 3,
            ("bread", "diaper"): 3,
            ("bread", "milk"): 4,
            ("diaper", "milk"): 3
        }
    )

    check(
        "infrequent items excluded from pairs",
        any(
            "cola" in k or "egg" in k
            for k in got
        ),
        False
    )

    try:
        rules = association_rules(
            BASKETS, 3, 0.75
        )
    except NotImplementedError:
        print("  association_rules is still a stub")
        return 1

    hit = [
        r for r in rules
        if r[0] == "diaper" and r[1] == "beer"
    ]

    check(
        "diaper -> beer confidence",
        round(hit[0][2], 3) if hit else None,
        0.8
    )

    check(
        "rules are sorted by confidence",
        all(
            rules[i][2] >= rules[i + 1][2]
            for i in range(len(rules) - 1)
        ),
        True
    )

    print(
        f"\n  {'all ok' if not fails else str(fails) + ' failed'}"
    )

    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()

    raise SystemExit(
        verify() if a.verify else p.print_help()
    )
