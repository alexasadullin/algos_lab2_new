from bisect import bisect_right

class Nd:
    def __init__(s, l, r, v):
        s.l = l; s.r = r; s.v = v

def upd(n, lo, hi, l, r, d):
    if hi <= l or r <= lo:
        return n
    if l <= lo and hi <= r:
        if n is None:
            return Nd(None, None, d)
        return Nd(n.l, n.r, n.v + d)
    m = (lo + hi) // 2
    cl = n.l if n else None
    cr = n.r if n else None
    cv = n.v if n else 0
    nl = upd(cl, lo, m, l, r, d)
    nr = upd(cr, m, hi, l, r, d)
    return Nd(nl, nr, cv)

def qr(n, lo, hi, p):
    if n is None:
        return 0
    if hi - lo == 1:
        return n.v
    m = (lo + hi) // 2
    if p < m:
        return n.v + qr(n.l, lo, m, p)
    return n.v + qr(n.r, m, hi, p)

def mk_ev(rc, yi):
    ev = {}
    for x1, y1, x2, y2 in rc:
        a = yi[y1]; b = yi[y2]
        if x1 not in ev: ev[x1] = []
        ev[x1].append((a, b, +1))
        if x2 not in ev: ev[x2] = []
        ev[x2].append((a, b, -1))
    return ev

def prepare(rc):
    xv = []; yv = []
    for r in rc:
        xv.append(r[0]); xv.append(r[2])
        yv.append(r[1]); yv.append(r[3])
    sx = sorted(set(xv))
    sy = sorted(set(yv))
    yi = {}
    for i in range(len(sy)):
        yi[sy[i]] = i
    ny = len(sy) - 1
    if ny < 1: ny = 1
    ev = mk_ev(rc, yi)
    # print(len(ev))
    rs = []
    c = None
    for x in sx:
        if x in ev:
            for a, b, d in ev[x]:
                if a < b:
                    c = upd(c, 0, ny, a, b, d)
        rs.append(c)
    # print(len(rs))
    return sx, sy, ny, rs

def query(pr, x, y):
    sx, sy, ny, rs = pr
    i = bisect_right(sx, x) - 1
    if i < 0:
        return 0
    j = bisect_right(sy, y) - 1
    if j < 0 or j >= ny:
        return 0
    # print(i, j)
    return qr(rs[i], 0, ny, j)
