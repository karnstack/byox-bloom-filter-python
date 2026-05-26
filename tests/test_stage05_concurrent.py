"""Tests for Stage 5: concurrent-safe add.

Read the stage on karnstack.com/build/bloom-filter/05-concurrent-add
before debugging failures. CPython's GIL serializes bytecode, so this
test is more informative than strict: it verifies the API holds up
under concurrent calls, not that the underlying ops are atomic. Free-
threaded (no-GIL) Pythons that ship in the future will rely on the
underlying primitive being atomic.
"""

import threading

from bloom import Filter


def test_stage05_concurrent_add_all_keys_present():
    """100 threads x 100 keys: every added key tests True after join."""
    workers, keys_per_worker = 100, 100
    f = Filter(95850, k=7)

    def insert(w: int) -> None:
        for i in range(keys_per_worker):
            f.add(f"w{w}-k{i}".encode())

    threads = [
        threading.Thread(target=insert, args=(w,)) for w in range(workers)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for w in range(workers):
        for i in range(keys_per_worker):
            key = f"w{w}-k{i}".encode()
            assert f.test(key), f"test({key!r}) = False after concurrent add"


def test_stage05_concurrent_add_on_blocked_filter():
    """Same property on the blocked layout."""
    workers = 50
    f = Filter.blocked(95850, 7)

    def insert(w: int) -> None:
        for i in range(100):
            f.add(f"blocked-w{w}-k{i}".encode())

    threads = [threading.Thread(target=insert, args=(w,)) for w in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for w in range(workers):
        for i in range(100):
            key = f"blocked-w{w}-k{i}".encode()
            assert f.test(key), f"test({key!r}) = False after concurrent add on blocked"
