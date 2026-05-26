"""Tests for Stage 6: serialize, deserialize, and saturation estimation.

Read the stage on karnstack.com/build/bloom-filter/06-serialize-and-saturation
before debugging failures.
"""

import math

from bloom import Filter


def test_stage06_round_trip_preserves_membership():
    """to_bytes followed by from_bytes preserves Test for every key."""
    src = Filter(95850, k=7)
    n = 5000
    for i in range(n):
        src.add(f"key-{i}".encode())

    data = src.to_bytes()
    assert isinstance(data, (bytes, bytearray)), "to_bytes must return bytes"
    assert len(data) > 0, "to_bytes returned empty bytes"

    dst = Filter.from_bytes(data)
    assert dst.m == src.m, f"M mismatch after round-trip: {dst.m} vs {src.m}"
    assert dst.k == src.k, f"K mismatch after round-trip: {dst.k} vs {src.k}"

    for i in range(n):
        key = f"key-{i}".encode()
        assert src.test(key) == dst.test(key), (
            f"test({key!r}) differs after round-trip"
        )


def test_stage06_serialization_is_deterministic():
    """Same state -> byte-equal output across two MarshalBinary calls."""
    f = Filter(1024, k=4)
    for k in (b"a", b"b", b"c"):
        f.add(k)
    a = bytes(f.to_bytes())
    b = bytes(f.to_bytes())
    assert a == b, "to_bytes is not deterministic"


def test_stage06_saturation_tracks_theoretical():
    """saturation within 5% of 1 - e^(-k*n/m)."""
    m, k, n = 95850, 7, 10000
    f = Filter(m, k=k)
    for i in range(n):
        f.add(f"key-{i}".encode())
    observed = f.saturation()
    theoretical = 1 - math.exp(-k * n / m)
    delta = abs(observed - theoretical) / theoretical
    assert delta <= 0.05, (
        f"saturation = {observed:.4f}, theoretical {theoretical:.4f} "
        f"(delta {delta * 100:.2f}%, want <= 5%)"
    )
