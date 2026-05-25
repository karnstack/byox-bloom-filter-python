# karnstack/byox-bloom-filter-python

Starter template (Python) for the [Bloom Filter](https://karnstack.com/build/bloom-filter) primitive on karnstack.

Six stages. Paper-backed tests. You implement the interface; karnstack tells you what to read at each stage.

## Prerequisites

[mise](https://mise.jdx.dev/) is the only thing you need installed globally. It pins Python 3.14 for this repo, creates a virtual environment, and runs the stage tasks. If you do not want to install mise, the equivalent commands are documented under [Without mise](#without-mise) below.

Install mise:

```bash
curl https://mise.run | sh
```

## Quick start

```bash
mise trust              # allow this repo's .mise.toml (one time)
mise install            # installs Python 3.14 + creates .venv
mise run setup          # installs the bloom package + pytest into .venv
mise run stage 1        # runs the tests for stage 1 (they fail until you implement)
```

Open [stage 1 on karnstack](https://karnstack.com/build/bloom-filter/01-bit-array-and-hashing). Implement `bloom/__init__.py` until `mise run stage 1` passes. Then move on:

```bash
mise run stage 2
```

`mise run all` runs every stage at once.

## Layout

```
.
├── .mise.toml                          # toolchain + tasks
├── pyproject.toml
├── bloom/
│   └── __init__.py                     # you implement here
└── tests/
    ├── test_stage01_bit_array.py
    ├── test_stage02_multi_hash.py
    ├── test_stage03_sizing.py
    ├── test_stage04_blocked.py
    ├── test_stage05_concurrent.py
    └── test_stage06_serialize.py
```

## Stages

1. Bit array and single hash
2. Multiple hashes (Kirsch-Mitzenmacher)
3. Optimal sizing math
4. Cache-line-blocked layout
5. Concurrent-safe Add
6. Serialize and saturation

Each stage is described on karnstack. Read first, then implement.

## What you are building

A constant-size data structure that says "definitely not in the set" or "maybe in the set" in `O(k)` time, with a tunable false-positive rate. The structure inside every production LSM-tree (RocksDB, LevelDB, Cassandra) used to skip disk reads on missing keys.

## Papers cited

- Bloom, B. (1970). [Space/Time Trade-offs in Hash Coding with Allowable Errors](https://dl.acm.org/doi/10.1145/362686.362692). CACM 13(7).
- Kirsch, A.; Mitzenmacher, M. (2006). [Less Hashing, Same Performance: Building a Better Bloom Filter](https://www.eecs.harvard.edu/~michaelm/postscripts/rsa2008.pdf). ESA 2006.
- Putze, F.; Sanders, P.; Singler, J. (2007). [Cache-, Hash- and Space-Efficient Bloom Filters](https://doi.org/10.1007/978-3-540-72845-0_9). WEA 2007.

## Without mise

If you do not want to install mise, ensure you have Python 3.14+ installed and run:

```bash
python -m venv .venv
source .venv/bin/activate         # or .venv\Scripts\activate on Windows
pip install -e '.[test]'

# Stage 1
pytest -v -k stage01 tests/

# Stage N (replace 01 with the zero-padded stage number)
pytest -v -k stageNN tests/

# All stages
pytest -v tests/
```

## License

MIT. See [LICENSE](LICENSE). Your fork is yours.
