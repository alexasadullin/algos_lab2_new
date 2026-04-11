def prepare(rectangles):
    return rectangles


def query(prepared, x, y):
    count = 0
    for x1, y1, x2, y2 in prepared:
        if x1 <= x < x2 and y1 <= y < y2:
            count += 1
    return count
