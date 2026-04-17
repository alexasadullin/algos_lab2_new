from bisect import bisect_right


def prepare(rectangles):
    x_values = []
    y_values = []
    for r in rectangles:
        x_values.append(r[0])
        x_values.append(r[2])
        y_values.append(r[1])
        y_values.append(r[3])

    xs = sorted(list(set(x_values)))
    ys = sorted(list(set(y_values)))

    nx = len(xs) - 1
    ny = len(ys) - 1

    grid = [[0] * ny for _ in range(nx)]

    x_index = {}
    for i in range(len(xs)):
        x_index[xs[i]] = i

    y_index = {}
    for i in range(len(ys)):
        y_index[ys[i]] = i

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


def query(prepared, x, y):
    xs, ys, grid = prepared
    i = bisect_right(xs, x) - 1
    j = bisect_right(ys, y) - 1
    if i < 0 or i >= len(xs) - 1 or j < 0 or j >= len(ys) - 1:
        return 0
    return grid[i][j]
