from bisect import bisect_right
from collections import defaultdict


class Node:
    __slots__ = ("left", "right", "value")

    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value


def _update(node, lo, hi, l, r, delta):
    if hi <= l or r <= lo:
        return node
    if l <= lo and hi <= r:
        if node is None:
            return Node(None, None, delta)
        return Node(node.left, node.right, node.value + delta)
    mid = (lo + hi) // 2
    left = node.left if node else None
    right = node.right if node else None
    value = node.value if node else 0
    new_left = _update(left, lo, mid, l, r, delta)
    new_right = _update(right, mid, hi, l, r, delta)
    return Node(new_left, new_right, value)


def _point_query(node, lo, hi, p):
    if node is None:
        return 0
    if hi - lo == 1:
        return node.value
    mid = (lo + hi) // 2
    if p < mid:
        return node.value + _point_query(node.left, lo, mid, p)
    return node.value + _point_query(node.right, mid, hi, p)


def prepare(rectangles):
    xs = sorted({r[0] for r in rectangles} | {r[2] for r in rectangles})
    ys = sorted({r[1] for r in rectangles} | {r[3] for r in rectangles})
    y_index = {v: i for i, v in enumerate(ys)}
    ny = max(len(ys) - 1, 1)
    events = defaultdict(list)
    for x1, y1, x2, y2 in rectangles:
        j1 = y_index[y1]
        j2 = y_index[y2]
        events[x1].append((j1, j2, 1))
        events[x2].append((j1, j2, -1))
    roots = []
    current = None
    for x in xs:
        for j1, j2, delta in events[x]:
            if j1 < j2:
                current = _update(current, 0, ny, j1, j2, delta)
        roots.append(current)
    return xs, ys, ny, roots


def query(prepared, x, y):
    xs, ys, ny, roots = prepared
    i = bisect_right(xs, x) - 1
    if i < 0:
        return 0
    j = bisect_right(ys, y) - 1
    if j < 0 or j >= ny:
        return 0
    return _point_query(roots[i], 0, ny, j)
