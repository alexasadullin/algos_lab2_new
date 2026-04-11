# Lab 2

## Files

- algos/brute.py: linear scan over all rectangles per query
- algos/map_algo.py: coordinate compression and a precomputed 2D count grid
- algos/tree_algo.py: x-sweep line over a persistent segment tree on compressed y
- main.py: correctness check, generators, timing, memory, charts
- charts/: one PNG per algorithm, three subplots each

## Quick start

```
python3.13 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

## Generators

- `gen_nested(N)`: rectangles `(10i, 10i, 10(2N-i), 10(2N-i))` for i = 1..N. Every rectangle strictly contains the next one, all 4N coordinates are distinct, the common center (10N, 10N) lies inside N-1 rectangles
- `gen_random(N, seed)`: N rectangles with x1 < x2 and y1 < y2 sampled uniformly from [1, 10**9], coordinates almost always distinct and rectangles almost never nested
- `gen_distinct_coords(N, seed)`: N non-nested rectangles whose 2N x and 2N y endpoints are drawn without repetition, forcing the compressed grid to its maximum 2N by 2N shape
- `gen_same_x_range(N, seed)`: N rectangles sharing x-interval [1, 10**9] and differing only in y, collapsing the compressed x-axis to exactly two values
- `gen_points_hash(N, M)`: M deterministic points `((p_x * i) mod 20N, (p_y * i) mod 20N)` for i = 1..M using two large primes, spread across [0, 20N)**2 without aligning to any simple grid

## Algorithms complexity

### Brute force

Preprocessing O(1), query O(N). The worst case is a configuration in which the query point lies inside nearly every rectangle, for example N nested rectangles queried at their common center

### Map algo

Preprocessing O(N**3), query O(log N), memory O(N**2). Preprocessing compresses the 2N unique x values and 2N unique y values, allocates a (2N) by (2N) integer grid, then for every rectangle increments all cells in its compressed index range. The total number of cell increments equals the sum over all rectangles of `(x2_idx - x1_idx) * (y2_idx - y1_idx)`, which is maximised by nested rectangles because each outer rectangle covers a near-full slice of the grid

### Tree algo

Preprocessing O(N log N), query O(log N), memory O(N log N). The sweep line processes up to 2N distinct x-events and at each event updates the current persistent segment tree by path copying, allocating O(log N) new nodes per update. Memory is maximised when the update paths are deep, for example nested rectangles with all distinct coordinates. Query time is maximised when all N rectangles share the same x-interval, because the two-version history forces every query to descend a single fully loaded tree

### Brute force scenarios

| # | rectangles          | query points                                                                                 |
|---|---------------------|----------------------------------------------------------------------------------------------|
| 1 | `gen_nested(2000)`  | M = 2000 copies of the common center (20000, 20000), each contained by N - 1 = 1999 rectangles |
| 2 | `gen_random(3000)`  | M = 3000 copies of (10**9 + 13, 10**9 + 17), each contained by 0 rectangles                    |
| 3 | `gen_nested(3000)`  | M = 1 point at the common center (30000, 30000), contained by 2999 rectangles                |

### Map algo scenarios

| # | rectangles                 | query points                                                                    |
|---|----------------------------|---------------------------------------------------------------------------------|
| 1 | `gen_nested(200)`          | M = 1 point at the common center, maximum-density nested layout                 |
| 2 | `gen_distinct_coords(200)` | M = 1 point at (500000, 500000), same (2N) by (2N) grid size with sparser fills |
| 3 | `gen_nested(150)`          | M = 1000 hash-generated points spread across [0, 3000)**2                        |

### Tree algo scenarios

| # | rectangles                  | query points                                                                      |
|---|-----------------------------|-----------------------------------------------------------------------------------|
| 1 | `gen_distinct_coords(2000)` | M = 2000 hash-generated points, 2N distinct x-events producing 2N tree versions   |
| 2 | `gen_same_x_range(2000)`    | M = 2000 points inside the shared x-interval, exactly two tree versions retained  |
| 3 | `gen_nested(2000)`          | M = 2000 hash-generated points, nested layout produces maximum-depth rewrites     |

## Results

### Brute force

| # | scenario                                                                      | total time | total memory |
|---|-------------------------------------------------------------------------------|------------|--------------|
| 1 | N = 2000 nested, M = 2000 queries at center (every query inside 1999 rects)   | 0.3029 s   | 160 B        |
| 2 | N = 3000 random, M = 3000 queries outside every rectangle                     | 0.2706 s   | 96 B         |
| 3 | N = 3000 nested, M = 1 query at center (inside 2999 rects)                    | 0.0002 s   | 112 B        |

### Map algo

| # | scenario                                            | total time | total memory |
|---|-----------------------------------------------------|------------|--------------|
| 1 | N = 200 nested                                      | 0.2447 s   | 1 347 600 B  |
| 2 | N = 200 distinct non-nested coordinates             | 0.0910 s   | 1 354 060 B  |
| 3 | N = 150 nested, M = 1000 hash queries               | 0.0951 s   | 754 764 B    |

### Tree algo

| # | scenario                                              | total time | total memory |
|---|-------------------------------------------------------|------------|--------------|
| 1 | N = 2000 distinct coordinates, M = 2000 hash queries  | 0.0564 s   | 7 691 836 B  |
| 2 | N = 2000 same x-interval, M = 2000 queries            | 0.0343 s   | 1 121 580 B  |
| 3 | N = 2000 nested, M = 2000 hash queries                | 0.0554 s   | 8 283 032 B  |

## Conclusion

The brute force worst case is scenario 1: N = 2000 nested rectangles with M = 2000 queries at the common center, each query contained by N - 1 rectangles. Total time reaches 0.3029 s, memory = const 

The map algo worst case is scenario 1: N = 200 nested rectangles. At identical compressed grid size, as the experiment shown, the nested layout takes much less time than non-nested layout takes 0.0910 sec. The memory peak depends only on the size of the compressed grid, so scenarios 1 and 2 are quite similar by mem (tie) 

The tree algo worst case is scenario 3 (0.0554 s), because it generates 2N distinct x-events and therefore 2N persistent updates of cost O(log N). Worst memory is scenario 3 at 8.28 MB, slightly above scenario 1 (7.69 MB), because the monotonically shrinking y-ranges of nested rectangles rewrite deeper paths of the previous version on every update

Overall: brute force is bound by many full-evaluation iterations, map algo by its O(N**3) preprocessing on dense layouts, tree algo by its O(N log N) memory footprint from retained persistent nodes
