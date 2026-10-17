# Greedy Huffman

A Huffman codec built on the `PriorityQueue` from Project 2.

## Files

- `structures.py` – PriorityQueue (with its own tests)
- `huffman.py` – Huffman codec
- `tests.py` – tests for the Huffman codec
- `canvas_tests.py` – Canvas tests for the Huffman codec

## Setup

```
pip install pytest
```

## Running the tests

Run everything:

```
pytest structures.py tests.py canvas_tests.py
```

Or run each file on its own:

```
pytest structures.py
pytest tests.py
pytest canvas_tests.py
```

Add `-v` to see each test by name, e.g. `pytest -v tests.py`.
