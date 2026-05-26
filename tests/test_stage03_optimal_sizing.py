"""Tests for Stage 3: optimal sizing math.

Read the stage on karnstack.com/build/bloom-filter/03-optimal-sizing-math
before debugging failures.
"""

import math

import pytest

from bloom import Filter, optimal_size


def test_stage03_optimal_size_at_10k_keys_one_percent():
    """optimal_size(10000, 0.01) yields m around 95850 and k around 7.

    5% slack on m, +-1 on k.
    """
    m, k = optimal_size(10000, 0.01)
    assert m > 0, "m = 0; check that the formula uses ln(p), not log10(p)"
    assert k > 0, "k = 0; round to nearest integer, not floor"
    expected_m = 95850
    m_delta = abs(m - expected_m) / expected_m
    assert m_delta <= 0.05, (
        f"m = {m}, want within 5% of {expected_m} (delta {m_delta * 100:.2f}%)"
    )
    assert 6 <= k <= 8, f"k = {k}, want 7 +- 1"


@pytest.mark.parametrize(
    "n,p,want_bits_per_key",
    [
        (1000, 0.01, 9.585),
        (1000, 0.001, 14.377),
        (1000, 0.0001, 19.170),
        (100000, 0.01, 9.585),
    ],
)
def test_stage03_optimal_size_at_varied_rates(n, p, want_bits_per_key):
    """Spot-check across a small grid; catches base-10 log substitutions."""
    m, _ = optimal_size(n, p)
    got = m / n
    delta = abs(got - want_bits_per_key) / want_bits_per_key
    assert delta <= 0.05, (
        f"bits/key = {got:.3f}, want {want_bits_per_key:.3f} "
        f"(delta {delta * 100:.2f}%)"
    )


def test_stage03_optimal_size_produces_usable_filter():
    """Wire the output back into Filter(m, k=k) and verify FP rate.

    Inserts n=10000 keys, queries 100000 unseen keys, expects observed
    FP <= 2x target p.
    """
    n, p, trials = 10000, 0.01, 100000
    m, k = optimal_size(n, p)
    f = Filter(m, k=k)
    for i in range(n):
        f.add(f"added-{i}".encode())
    fps = sum(1 for i in range(trials) if f.test(f"query-{i}".encode()))
    observed = fps / trials
    assert observed <= 2 * p, (
        f"FP rate {observed:.4f} exceeds 2x target {p:.4f}"
    )
