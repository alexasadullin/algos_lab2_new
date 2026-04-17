from bisect import bisect_right

def cmp(v: list):
    s = sorted(set(v))
    d = {}
    # print(len(s))
    for k in range(len(s)):
        d[s[k]] = k
    return s, d

def prepare(rect: list):
    if len(rect) ==0:
        return [], [],[]
    xv = []
    yv = []
    for r in rect:
        xv.append(r[0]); xv.append(r[2])
        yv.append(r[1]); yv.append(r[3])
    # print(len(xv), len(yv))
    sx,ix = cmp(xv)
    sy, iy = cmp(yv)
    nx = len(sx) -1
    ny = len(sy)-1
    if nx <=0 or ny<=0:
        return sx, sy,[]
    g = []
    for i in range(nx):
        g.append([0] *ny)
    # cnt = 0
    for x1, y1,x2, y2 in rect:
        a = ix[x1]; b= ix[x2]
        c = iy[y1]; d = iy[y2]
        for i in range(a,b):
            for j in range(c, d):
                g[i][j] +=1
                # cnt += 1
    # print(cnt)
    return sx, sy,g

def query(pr: tuple, x: int, y: int):
    sx,sy, g = pr
    if len(g) ==0:
        return 0
    nx = len(sx) -1
    ny = len(sy)- 1
    i = bisect_right(sx, x) -1
    j = bisect_right(sy, y)- 1
    # print(x, y, i, j)
    if i<0 or j < 0:
        return 0
    if i >=nx or j>= ny:
        return 0
    res = g[i][j]
    return res
