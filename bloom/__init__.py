"""Karnstack BYOX: Bloom filter, Python variant.

The interface below is the contract karnstack tests target. Do not rename
the public methods. Implementation lives in this module across six stages:

    Stage 1: bit array storage and a single hash function.
    Stage 2: multiple hash functions via the Kirsch-Mitzenmacher construction.
    Stage 3: optimal sizing helpers (m and k from a target false-positive rate).
    Stage 4: cache-line-blocked layout (within the limits of CPython).
    Stage 5: concurrent-safe Add.
    Stage 6: serialize, deserialize, and saturation estimation.

Read the stage on karnstack.com/build/bloom-filter before implementing.
"""

from __future__ import annotations


class Filter:
    """A Bloom filter.

    Stage 1 uses a single hash function. Stage 2 switches to the
    Kirsch-Mitzenmacher two-hash construction.
    """

    def __init__(self, m: int) -> None:
        """Construct a filter with at least m bits of capacity.

        Implementations should round m up to the nearest multiple of 8 so the
        underlying bytearray is fully addressable. Set self._m to the
        rounded-up size.

        Stage 1: implement this.
        """
        # TODO(stage1): allocate the bit array; set self._m.
        self._m: int = 0

    def add(self, key: bytes) -> None:
        """Insert a key into the filter.

        Stage 1: hash key, map to a bit position in [0, m), set the bit.
        """
        # TODO(stage1).
        raise NotImplementedError

    def test(self, key: bytes) -> bool:
        """Return True if the key may be in the filter, False if definitely not.

        Stage 1: hash key, map to a bit position in [0, m), check the bit.
        """
        # TODO(stage1).
        return False

    @property
    def m(self) -> int:
        """Actual bit capacity (after rounding up)."""
        return self._m
