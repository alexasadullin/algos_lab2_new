def query(rectangles: list, x: int, y: int) -> int:
    count = 0
    for x1, y1, x2, y2 in rectangles:
        if x1 <= x < x2 and y1 <= y < y2:
            count += 1
    return count
