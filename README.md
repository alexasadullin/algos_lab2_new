# Lab 2

## Files

- algos/brute.py - just loops through all rectangles for each query
- algos/map_algo.py - compresses coordinates, builds a 2D grid with counts
- algos/tree_algo.py - sweep line + persistent segment tree
- main.py - runs everything: correctness check, timing, memory, charts
- charts/ - one PNG per algorithm

## How to run

```
python3.13 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

## Algorithms

Brute force: prep O(1), query O(N). Simple but slow when there are many rectangles and queries.

Map algo: prep O(N^3), query O(log N), memory O(N^2). Builds a grid after coordinate compression, then just looks up a cell. Prep is the bottleneck.

Tree algo: prep O(N log N), query O(log N), memory O(N log N). Uses a persistent segment tree with sweep line. Fast queries but uses more memory.

## Worst cases

### Brute force

| scenario | time | memory |
|----------|------|--------|
| N=2000 nested, M=2000 queries at center | biggest | lowest |
| N=3000 random, M=3000 queries that miss all rects | big | lowest |
| N=3000 nested, single query at center | lowest | lowest |

Worst case is scenario 1 - lots of nested rectangles and every query hits almost all of them, so each query does maximum work. Memory is tiny in all cases since brute force stores nothing extra.

### Map algo

| scenario | time | memory |
|----------|------|--------|
| N=200 nested | biggest | big |
| N=200 distinct non-nested coords | middle | big |
| N=150 nested, M=1000 hash queries | middle | middle |

Worst case is scenario 1 - nested rectangles make O(N^3) prep hurt the most because each outer rectangle covers nearly the whole grid. Memory is about the same for scenarios 1 and 2 since grid size depends on how many unique coordinates there are, not on nesting.

### Tree algo

| scenario | time | memory |
|----------|------|--------|
| N=2000 distinct coords, M=2000 hash queries | big | big |
| N=2000 same x-interval, M=2000 queries | lowest | lowest |
| N=2000 nested, M=2000 hash queries | big | biggest |

Worst case for memory is scenario 3 - nested rectangles cause the deepest path rewrites in the persistent tree, creating the most new nodes. Time is similar between scenarios 1 and 3 since both have many distinct x-events.

## Conclusion

Brute force is the simplest but gets slow fast when you have many rectangles and many queries that land inside them. Map algo preprocesses a grid which is great for queries (log N) but the O(N^3) prep kills it on large inputs. Tree algo is the best balance - O(N log N) prep and O(log N) query - but it eats the most memory because of persistent nodes. Pick brute for small N, map algo when N is small enough for cubic prep, tree algo for everything else.
