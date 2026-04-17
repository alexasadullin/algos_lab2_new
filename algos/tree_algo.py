from bisect import bisect_right

class Nd:
    def __init__(s, l, r, v):
        s.l = l; s.r = r; s.v = v

def upd(n: Nd, lo: int, hi: int, l: int, r: int, d: int):
    if hi<=l or r <=lo:
        return n
    if l<= lo and hi <=r:
        if n is None:
            return Nd(None, None, d)
        return Nd(n.l, n.r, n.v +d)
    m = (lo +hi)//2
    if n is not None:
        cl = n.l
        cr = n.r
        cv = n.v
    else:
        cl, cr, cv = None, None, 0
    # print(lo, hi, m)
    nl = upd(cl, lo, m, l, r, d)
    nr = upd(cr, m, hi, l,r, d)
    return Nd(nl, nr, cv)

def qr(n: Nd, lo: int, hi: int, p: int):
    if n is None:
        return 0
    if hi - lo ==1:
        return n.v
    m = (lo+hi) //2
    # print(lo, hi, p)
    res = n.v
    if p <m:
        res = res + qr(n.l, lo, m, p)
    else:
        res = res + qr(n.r, m, hi, p)
    return res

def mk_ev(rc: list, yi: dict):
    ev = {}
    for k in range(len(rc)):
        x1 = rc[k][0]; y1 = rc[k][1]
        x2 = rc[k][2]; y2 = rc[k][3]
        a = yi[y1]; b = yi[y2]
        if x1 not in ev:
            ev[x1] = []
        ev[x1].append((a, b,+1))
        if x2 not in ev:
            ev[x2] = []
        ev[x2].append((a, b, -1))
    # print(len(ev))
    return ev

def prepare(rc: list):
    xv = []
    yv = []
    for k in range(len(rc)):
        xv.append(rc[k][0])
        xv.append(rc[k][2])
        yv.append(rc[k][1])
        yv.append(rc[k][3])
    sx = sorted(set(xv))
    sy = sorted(set(yv))
    # print(len(sx), len(sy))
    yi = {}
    for i in range(len(sy)):
        yi[sy[i]] = i
    ny = len(sy) -1
    if ny< 1:
        ny = 1
    ev = mk_ev(rc, yi)
    rs = []
    c = None
    for i in range(len(sx)):
        x = sx[i]
        if x in ev:
            lst = ev[x]
            for j in range(len(lst)):
                a = lst[j][0]; b = lst[j][1]; d = lst[j][2]
                if a< b:
                    c = upd(c, 0, ny, a,b, d)
        rs.append(c)
    # print(len(rs))
    return sx,sy, ny, rs

def query(pr: tuple, x: int, y: int):
    sx, sy,ny, rs = pr
    i = bisect_right(sx, x) -1
    if i <0:
        return 0
    j = bisect_right(sy, y)- 1
    # print(i, j)
    if j<0 or j >= ny:
        return 0
    ans = qr(rs[i], 0,ny, j)
    return ans
