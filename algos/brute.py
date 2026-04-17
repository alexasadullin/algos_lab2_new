def query(rectangles: list, x: int, y: int):
    cnt = 0
    for k in range(len(rectangles)):
        r = rectangles[k]
        x1 = r[0]; y1 = r[1]
        x2 = r[2]; y2 = r[3]
        # print(x1, y1, x2, y2)
        if x1 <=x and x< x2 and y1 <=y and y <y2:
            cnt +=1
    return cnt
