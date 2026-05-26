"""Tests for Stage 4: cache-line-blocked layout.

Read the stage on karnstack.com/build/bloom-filter/04-cache-line-blocked
before debugging failures. Within the limits of CPython (interpreted,
not cache-tuned), the blocked layout is mostly informative; the FP-rate
property still holds.
"""

import math

from bloom import Filter


def test_stage04_blocked_allocates():
    """Filter.blocked(m, k) constructs and reports the rounded-up capacity."""
    f = Filter.blocked(95850, 7)
    assert f.m >= 95850, f"f.m = {f.m}, want >= 95850"
    assert f.k == 7, f"f.k = {f.k}, want 7"


def test_stage04_added_keys_are_present():
    """add/test round-trip on the blocked layout."""
    f = Filter.blocked(95850, 7)
    keys = [b"alice", b"bob", b"carol", b"dan", b"eve", b"frank"]
    for k in keys:
        f.add(k)
    for k in keys:
        assert f.test(k), f"test({k!r}) = False on blocked filter"


def test_stage04_fp_rate_below_theoretical_bound():
    """FP rate stays within 2x of (1 - e^-kn/m)^k for the blocked layout.

    A correctly implemented blocked Bloom (Putze-Sanders-Singler 2007)
    pays a small FP penalty (~1.3-1.5x) for the cache locality. 2x slack
    leaves room for hash quality variation.
    """
    m, k, n, trials = 95850, 7, 10000, 100000
    f = Filter.blocked(m, k)
    for i in range(n):
        f.add(f"added-{i}".encode())
    fps = sum(1 for i in range(trials) if f.test(f"query-{i}".encode()))
    observed = fps / trials
    theoretical = (1 - math.exp(-k * n / m)) ** k
    bound = 2 * theoretical
    assert observed <= bound, (
        f"blocked FP rate {observed:.4f} exceeds 2x theoretical "
        f"{theoretical:.4f} (bound {bound:.4f})"
    )
