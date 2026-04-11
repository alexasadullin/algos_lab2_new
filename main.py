import random
import time
import tracemalloc
import matplotlib.pyplot as plt

from algos.brute import query as brute_query
from algos.map_algo import prepare as map_prepare, query as map_query
from algos.tree_algo import prepare as tree_prepare, query as tree_query


def measure_time(fn, *args) -> float:
    start = time.perf_counter()
    for _ in range(100):
        fn(*args)
    return (time.perf_counter() - start) / 100


def measure_memory(fn, *args) -> int:
    tracemalloc.start()
    fn(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def gen_nested(N: int) -> list:
    return [(10 * i, 10 * i, 10 * (2 * N - i), 10 * (2 * N - i)) for i in range(1, N + 1)]


def gen_points_hash(N: int, M: int) -> list:
    p_x, p_y = 1000000007, 998244353
    return [((p_x * i) % (20 * N), (p_y * i) % (20 * N)) for i in range(1, M + 1)]


def gen_random(N: int, seed: int = 42) -> list:
    rng = random.Random(seed)
    rects = []
    for _ in range(N):
        x1 = rng.randint(1, 10 ** 9 - 2)
        x2 = rng.randint(x1 + 1, 10 ** 9)
        y1 = rng.randint(1, 10 ** 9 - 2)
        y2 = rng.randint(y1 + 1, 10 ** 9)
        rects.append((x1, y1, x2, y2))
    return rects


def gen_distinct_coords(N: int, seed: int = 7) -> list:
    rng = random.Random(seed)
    xs = rng.sample(range(1, 10 ** 6), 2 * N)
    ys = rng.sample(range(1, 10 ** 6), 2 * N)
    rects = []
    for i in range(N):
        x1, x2 = sorted((xs[2 * i], xs[2 * i + 1]))
        y1, y2 = sorted((ys[2 * i], ys[2 * i + 1]))
        rects.append((x1, y1, x2, y2))
    return rects


def gen_same_x_range(N: int, seed: int = 11) -> list:
    rng = random.Random(seed)
    x1, x2 = 1, 10 ** 9
    rects = []
    ys = rng.sample(range(1, 10 ** 6), 2 * N)
    for i in range(N):
        y1, y2 = sorted((ys[2 * i], ys[2 * i + 1]))
        rects.append((x1, y1, x2, y2))
    return rects


def identity(rectangles: list) -> list:
    return rectangles


def run_many_queries(query_fn, prepared, points: list) -> None:
    for x, y in points:
        query_fn(prepared, x, y)


def collect_scenario(prepare_fn, query_fn, rects: list, points: list) -> tuple:
    prepared = prepare_fn(rects)
    prep_time = measure_time(prepare_fn, rects)
    prep_mem = measure_memory(prepare_fn, rects)
    if len(points) == 1:
        x, y = points[0]
        query_time = measure_time(query_fn, prepared, x, y)
        query_mem = measure_memory(query_fn, prepared, x, y)
    else:
        query_time = measure_time(run_many_queries, query_fn, prepared, points)
        query_mem = measure_memory(run_many_queries, query_fn, prepared, points)
    return prep_time, query_time, prep_mem, query_mem


def build_brute_scenarios() -> list:
    N1, M1 = 2000, 2000
    N2, M2 = 3000, 3000
    N3 = 3000
    return [
        ("1. N=2000 nested, M=2000 at center", gen_nested(N1), [(10 * N1, 10 * N1)] * M1),
        ("2. N=3000 random, M=3000 miss all", gen_random(N2, seed=77), [(10 ** 9 + 13, 10 ** 9 + 17)] * M2),
        ("3. N=3000 nested, M=1 at center", gen_nested(N3), [(10 * N3, 10 * N3)]),
    ]


def build_map_scenarios() -> list:
    N1 = 200
    N2 = 200
    N3, M3 = 150, 1000
    return [
        ("1. N=200 nested", gen_nested(N1), [(10 * N1, 10 * N1)]),
        ("2. N=200 distinct non-nested coords", gen_distinct_coords(N2, seed=23), [(500_000, 500_000)]),
        ("3. N=150 nested, M=1000 hash queries", gen_nested(N3), gen_points_hash(N3, M3)),
    ]


def build_tree_scenarios() -> list:
    N, M = 2000, 2000
    s2_points = [(500_000_000, (i * 998244353) % 1_000_000) for i in range(M)]
    return [
        ("1. N=2000 distinct coords, M=2000 hash queries", gen_distinct_coords(N, seed=31), gen_points_hash(N, M)),
        ("2. N=2000 same x-interval, M=2000 queries", gen_same_x_range(N, seed=41), s2_points),
        ("3. N=2000 nested, M=2000 hash queries", gen_nested(N), gen_points_hash(N, M)),
    ]


def draw_chart(algo_name: str, results: list):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), gridspec_kw={"wspace": 0.9})
    for ax, (label, prep_time, query_time, prep_mem, query_mem) in zip(axes, results):
        ax2 = ax.twinx()
        bar_time = ax.bar([0], [prep_time + query_time], color="blue", width=0.6)
        bar_mem = ax2.bar([1], [prep_mem + query_mem], color="orange", width=0.6)
        ax.set_yscale("log")
        ax2.set_yscale("log")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["time", "memory"])
        ax.set_ylabel("time (s)")
        ax2.set_ylabel("memory (bytes)")
        ax.set_title(label)
        ax.legend([bar_time, bar_mem], ["time", "memory"], loc="upper left")
    fig.suptitle(algo_name)
    plt.savefig(f"charts/{algo_name}.png", bbox_inches="tight")
    plt.close()


def run_algo(name: str, prepare_fn, query_fn, scenarios: list):
    print(f"\n=== {name} ===")
    results = []
    for label, rects, points in scenarios:
        pt, qt, pm, qm = collect_scenario(prepare_fn, query_fn, rects, points)
        print(f"{label}: prep_time={pt:.6f}s query_time={qt:.6f}s prep_mem={pm}B query_mem={qm}B")
        results.append((label, pt, qt, pm, qm))
    draw_chart(name, results)


def main():
    run_algo("brute", identity, brute_query, build_brute_scenarios())
    run_algo("map_algo", map_prepare, map_query, build_map_scenarios())
    run_algo("tree_algo", tree_prepare, tree_query, build_tree_scenarios())


if __name__ == "__main__":
    main()
