"""Tests for Stage 1: bit array and single hash.

Read the stage on karnstack.com/build/bloom-filter/01-bit-array-and-hashing
before debugging failures. Each test catches a specific failure mode listed
in the "Common Pitfalls" section.
"""

from bloom import Filter


def test_stage01_new_allocates_at_least_m_bits():
    """New(m) returns a filter whose actual bit capacity is at least m.

    Catches truncation of m rather than rounding up.
    """
    m = 95850
    f = Filter(m)
    assert f.m >= m, f"f.m = {f.m}, want >= {m}"


def test_stage01_added_key_is_present():
    """Test returns True after Add for any key.

    Catches a missing or broken Add implementation.
    """
    f = Filter(1024)
    keys = [b"alice", b"bob", b"carol", b"dan"]
    for k in keys:
        f.add(k)
    for k in keys:
        assert f.test(k), f"test({k!r}) = False, want True after add"


def test_stage01_empty_filter_returns_false():
    """Test on a fresh filter returns False for arbitrary keys.

    With a single hash and zero inserts, there is no false-positive path.
    Catches a bit array that initializes to non-zero values.
    """
    f = Filter(1024)
    for i in range(100):
        k = f"key-{i}".encode()
        assert not f.test(k), f"test({k!r}) = True on empty filter"


def test_stage01_bit_array_boundary():
    """New(1) does not crash; Add followed by Test works on a one-bit filter.

    Catches off-by-one errors in the modulo-into-bit-position math and
    division-by-zero on tiny filters.
    """
    f = Filter(1)
    assert f.m >= 1, f"f.m = {f.m} for Filter(1), want >= 1"
    key = b"anything"
    f.add(key)
    assert f.test(key), f"test({key!r}) = False after add on m=1 filter"


def test_stage01_hash_is_deterministic():
    """Two filters of identical capacity agree on test for the same key.

    Catches a hash function seeded from process randomness rather than a
    constant.
    """
    m = 1024
    f1 = Filter(m)
    f2 = Filter(m)
    key = b"deterministic"
    f1.add(key)
    f2.add(key)
    assert f1.test(key), "test(key) = False on filter 1 after add"
    assert f2.test(key), "test(key) = False on filter 2 after add"
