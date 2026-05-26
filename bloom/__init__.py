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

    def __init__(self, m: int, k: int = 1) -> None:
        """Construct a filter with at least m bits of capacity.

        Implementations should round m up to the nearest multiple of 8 so the
        underlying bytearray is fully addressable. Set self._m to the
        rounded-up size and self._k to the number of hash functions to use
        per probe. k defaults to 1 (stage 1); stage 2 passes a larger k via
        the Kirsch-Mitzenmacher two-hash construction.

        Stage 1: implement this for k=1.
        Stage 2: extend to support k>1.
        """
        # TODO(stage1/stage2): allocate the bit array; set self._m and self._k.
        self._m: int = 0
        self._k: int = k

    def add(self, key: bytes) -> None:
        """Insert a key into the filter.

        Stage 1: hash key, map to a bit position in [0, m), set the bit.
        Stage 2: extend to k bit positions via Kirsch-Mitzenmacher.
        """
        # TODO(stage1/stage2).
        raise NotImplementedError

    def test(self, key: bytes) -> bool:
        """Return True if the key may be in the filter, False if definitely not.

        Stage 1: hash key, map to a bit position in [0, m), check the bit.
        Stage 2: extend to k bit positions; ALL must be set.
        """
        # TODO(stage1/stage2).
        return False

    @property
    def m(self) -> int:
        """Actual bit capacity (after rounding up)."""
        return self._m

    @property
    def k(self) -> int:
        """Number of hash functions per probe."""
        return self._k
