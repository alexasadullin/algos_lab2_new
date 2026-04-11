from bisect import bisect_right


def prepare(rectangles: list) -> tuple:
    xs = sorted({r[0] for r in rectangles} | {r[2] for r in rectangles})
    ys = sorted({r[1] for r in rectangles} | {r[3] for r in rectangles})
    nx = len(xs) - 1
    ny = len(ys) - 1
    grid = [[0] * ny for _ in range(nx)]
    x_index = {v: i for i, v in enumerate(xs)}
    y_index = {v: i for i, v in enumerate(ys)}
    for x1, y1, x2, y2 in rectangles:
        i1 = x_index[x1]
        i2 = x_index[x2]
        j1 = y_index[y1]
        j2 = y_index[y2]
        for i in range(i1, i2):
            row = grid[i]
            for j in range(j1, j2):
                row[j] += 1
    return xs, ys, grid


def query(prepared: tuple, x: int, y: int) -> int:
    xs, ys, grid = prepared
    i = bisect_right(xs, x) - 1
    j = bisect_right(ys, y) - 1
    if i < 0 or i >= len(xs) - 1 or j < 0 or j >= len(ys) - 1:
        return 0
    return grid[i][j]
