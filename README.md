# Lab 2

## Files

- algos/brute.py: linear scan
- algos/map_algo.py: coordinate compression plus 2D count grid
- algos/tree_algo.py: sweep line plus persistent segment tree
- main.py: correctness check, generators, timing, memory, charts
- charts/: one PNG per algorithm

## Run

```
python3.13 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

## Generators

- `gen_nested(N)`: N rectangles nested around a common center, `(10*i, 10*i, 10*(2N-i), 10*(2N-i))`. All 4N coordinates distinct, every rectangle contains the next
- `gen_points_hash(N, M)`: M deterministic query points `((p_x*i) % 20N, (p_y*i) % 20N)` with large primes, spread across the intersection region
- `gen_random(N, seed)`: N rectangles with x1 < x2, y1 < y2 sampled uniformly from [1, 10**9]. Used with queries beyond 10**9 to force every query to miss
- `gen_distinct_coords(N, seed)`: N non-nested rectangles with 2N distinct x and 2N distinct y values, forces the compressed grid to its maximum 2N by 2N size
- `gen_same_x_range(N, seed)`: N rectangles sharing `x = [1, 10**9]` and differing only in y, collapses x to two unique values

