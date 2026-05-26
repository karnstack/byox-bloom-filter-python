"""Tests for Stage 2: multiple hashes via the Kirsch-Mitzenmacher construction.

Read the stage on karnstack.com/build/bloom-filter/02-multiple-hashes before
debugging failures. Each test catches a specific failure mode listed in the
"Common Pitfalls" section.
"""

import math

from bloom import Filter


def test_stage02_filter_accepts_k():
    """Filter(m, k=k) constructs and reports rounded-up capacity.

    Catches a missing k parameter or one that is silently ignored.
    """
    f = Filter(1024, k=3)
    assert f.m >= 1024, f"f.m = {f.m}, want >= 1024"


def test_stage02_added_keys_are_present():
    """add/test still work end to end once add is using k hashes.

    Failure here means the multi-hash construction is mis-indexing
    (off-by-one on i, wrong modulo, etc.).
    """
    f = Filter(95850, k=7)
    keys = [b"alice", b"bob", b"carol", b"dan", b"eve"]
    for k in keys:
        f.add(k)
    for k in keys:
        assert f.test(k), f"test({k!r}) = False, want True after add"


def test_stage02_fp_rate_below_theoretical_bound():
    """FP rate must stay within 2x of (1 - e^-kn/m)^k.

    Inserts n=10000 keys into an m=95850 / k=7 filter, queries 100k unseen
    keys, and verifies the observed false-positive rate is at most twice
    the theoretical Bloom bound. A broken Kirsch-Mitzenmacher derivation
    blows well past 2x.
    """
    m, k, n, trials = 95850, 7, 10000, 100000
    f = Filter(m, k=k)
    for i in range(n):
        f.add(f"added-{i}".encode())
    fps = sum(1 for i in range(trials) if f.test(f"query-{i}".encode()))
    observed = fps / trials
    theoretical = (1 - math.exp(-k * n / m)) ** k
    bound = 2 * theoretical
    assert observed <= bound, (
        f"FP rate {observed:.4f} exceeds 2x theoretical "
        f"{theoretical:.4f} (bound {bound:.4f})"
    )
