import random
import time
import tracemalloc
import matplotlib.pyplot as plt

from algos import brute, map_algo, tree_algo


def measure_time(fn, *args):
    start = time.perf_counter()
    for _ in range(100):
        fn(*args)
    return (time.perf_counter() - start) / 100


def measure_memory(fn, *args):
    tracemalloc.start()
    fn(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def gen_nested(N):
    return [(10 * i, 10 * i, 10 * (2 * N - i), 10 * (2 * N - i)) for i in range(1, N + 1)]


def gen_points_hash(N, M):
    p_x, p_y = 1000000007, 998244353
    return [((p_x * i) % (20 * N), (p_y * i) % (20 * N)) for i in range(1, M + 1)]


def gen_random(N, seed=42):
    rng = random.Random(seed)
    rects = []
    for _ in range(N):
        x1 = rng.randint(1, 10 ** 9 - 2)
        x2 = rng.randint(x1 + 1, 10 ** 9)
        y1 = rng.randint(1, 10 ** 9 - 2)
        y2 = rng.randint(y1 + 1, 10 ** 9)
        rects.append((x1, y1, x2, y2))
    return rects


def gen_distinct_coords(N, seed=7):
    rng = random.Random(seed)
    xs = rng.sample(range(1, 10 ** 6), 2 * N)
    ys = rng.sample(range(1, 10 ** 6), 2 * N)
    rects = []
    for i in range(N):
        x1, x2 = sorted((xs[2 * i], xs[2 * i + 1]))
        y1, y2 = sorted((ys[2 * i], ys[2 * i + 1]))
        rects.append((x1, y1, x2, y2))
    return rects


def gen_same_x_range(N, seed=11):
    rng = random.Random(seed)
    x1, x2 = 1, 10 ** 9
    rects = []
    ys = rng.sample(range(1, 10 ** 6), 2 * N)
    for i in range(N):
        y1, y2 = sorted((ys[2 * i], ys[2 * i + 1]))
        rects.append((x1, y1, x2, y2))
    return rects


def run_many_queries(mod, prepared, points):
    for x, y in points:
        mod.query(prepared, x, y)


def collect_scenario(mod, rects, query_points):
    prepared = mod.prepare(rects)
    prep_time = measure_time(mod.prepare, rects)
    if len(query_points) == 1:
        qx, qy = query_points[0]
        query_time = measure_time(mod.query, prepared, qx, qy)
        query_mem = measure_memory(mod.query, prepared, qx, qy)
    else:
        query_time = measure_time(run_many_queries, mod, prepared, query_points)
        query_mem = measure_memory(run_many_queries, mod, prepared, query_points)
    prep_mem = measure_memory(mod.prepare, rects)
    return prep_time, query_time, prep_mem, query_mem


def build_brute_scenarios():
    N1, M1 = 2000, 2000
    s1_rects = gen_nested(N1)
    s1_points = [(10 * N1, 10 * N1) for _ in range(M1)]

    N2, M2 = 3000, 3000
    s2_rects = gen_random(N2, seed=77)
    s2_points = [(10 ** 9 + 13, 10 ** 9 + 17) for _ in range(M2)]

    N3 = 3000
    s3_rects = gen_nested(N3)
    s3_points = [(10 * N3, 10 * N3)]

    return [
        ("nested, all-hit, many queries", s1_rects, s1_points),
        ("large N x M, all miss", s2_rects, s2_points),
        ("large N nested, single hit", s3_rects, s3_points),
    ]


def build_map_scenarios():
    N1 = 200
    s1_rects = gen_nested(N1)
    s1_points = [(10 * N1, 10 * N1)]

    N2 = 200
    s2_rects = gen_distinct_coords(N2, seed=23)
    s2_points = [(500_000, 500_000)]

    N3, M3 = 150, 1000
    s3_rects = gen_nested(N3)
    s3_points = gen_points_hash(N3, M3)

    return [
        ("nested N=200, max grid fill", s1_rects, s1_points),
        ("distinct random coords N=200", s2_rects, s2_points),
        ("nested N=150, many queries", s3_rects, s3_points),
    ]


def build_tree_scenarios():
    N1, M1 = 2000, 2000
    s1_rects = gen_distinct_coords(N1, seed=31)
    s1_points = gen_points_hash(N1, M1)

    N2, M2 = 2000, 2000
    s2_rects = gen_same_x_range(N2, seed=41)
    s2_points = [(500_000_000, (i * 998244353) % 1_000_000) for i in range(M2)]

    N3, M3 = 2000, 2000
    s3_rects = gen_nested(N3)
    s3_points = gen_points_hash(N3, M3)

    return [
        ("distinct coords, max versions", s1_rects, s1_points),
        ("same x-range, heavy queries", s2_rects, s2_points),
        ("nested N=2000, many queries", s3_rects, s3_points),
    ]


def draw_chart(algo_name, file_name, results):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), gridspec_kw={"wspace": 0.9})
    for ax, (label, prep_time, query_time, prep_mem, query_mem) in zip(axes, results):
        total_time = prep_time + query_time
        total_mem = prep_mem + query_mem
        ax2 = ax.twinx()
        x_time = 0
        x_mem = 1
        bar_time = ax.bar([x_time], [total_time], color="blue", width=0.6, label="time")
        bar_mem = ax2.bar([x_mem], [total_mem], color="orange", width=0.6, label="memory")
        ax.set_yscale("log")
        ax2.set_yscale("log")
        ax.set_xticks([x_time, x_mem])
        ax.set_xticklabels(["time", "memory"])
        ax.set_ylabel("time (s)")
        ax2.set_ylabel("memory (bytes)")
        ax.set_title(label)
        ax.legend([bar_time, bar_mem], ["time", "memory"], loc="upper left")
    fig.suptitle(algo_name)
    plt.savefig(f"charts/{file_name}.png", bbox_inches="tight")
    plt.close()


def run_algo(name, file_name, mod, scenarios):
    print(f"\n=== {name} ===")
    results = []
    for label, rects, points in scenarios:
        pt, qt, pm, qm = collect_scenario(mod, rects, points)
        print(f"{label}: prep_time={pt:.6f}s query_time={qt:.6f}s prep_mem={pm}B query_mem={qm}B")
        results.append((label, pt, qt, pm, qm))
    draw_chart(name, file_name, results)


def main():
    run_algo("brute", "brute", brute, build_brute_scenarios())
    run_algo("map_algo", "map_algo", map_algo, build_map_scenarios())
    run_algo("tree_algo", "tree_algo", tree_algo, build_tree_scenarios())


if __name__ == "__main__":
    main()
