import random
import time
import tracemalloc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from algos.brute import query as brute_query
from algos.map_algo import prepare as mp_prep, query as mp_qr
from algos.tree_algo import prepare as tr_prep, query as tr_qr

def mtime(f, *a):
    t = time.perf_counter()
    for _ in range(100):
        f(*a)
    return (time.perf_counter() -t) / 100

def mmem(f, *a):
    tracemalloc.start()
    f(*a)
    _,pk = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pk

def gn(N):
    r = []
    for i in range(1, N +1):
        c = 10*i; c2 = 10 *(2*N - i)
        r.append((c, c, c2,c2))
    return r

def gph(N, M):
    px = 1000000007; py = 998244353
    p = []
    for i in range(1,M+1):
        p.append(( (px *i) % (20*N), (py*i) % (20 *N) ))
    return p

def grnd(N, sd=42):
    rng = random.Random(sd)
    r = []
    for _ in range(N):
        x1 = rng.randint(1, 10**9 -2)
        x2 = rng.randint(x1 +1, 10**9)
        y1 = rng.randint(1, 10**9- 2)
        y2 = rng.randint(y1+1, 10**9)
        r.append((x1, y1, x2,y2))
    return r

def gdc(N, sd=7):
    rng = random.Random(sd)
    xx = rng.sample(range(1, 10**6), 2 *N)
    yy = rng.sample(range(1, 10**6), 2*N)
    r = []
    for i in range(N):
        a, b = xx[2*i], xx[2*i +1]
        if a >b: a,b = b, a
        c,d = yy[2*i], yy[2 *i+1]
        if c> d: c, d = d,c
        r.append((a, c, b, d))
    return r

# same x range for all rects
def gsx(N, sd=11):
    rng = random.Random(sd)
    lx = 1; rx = 10**9
    yy = rng.sample(range(1, 10**6), 2*N)
    r = []
    for i in range(N):
        a,b = yy[2*i], yy[2*i +1]
        if a> b: a, b = b, a
        r.append((lx,a, rx, b))
    return r

def ident(rc):
    return rc

def rq(qf, pr, pp):
    for x,y in pp:
        qf(pr, x, y)

# print(rc, pp)
def coll(pfn, qf, rc, pp):
    d = pfn(rc)
    pt = mtime(pfn, rc)
    pm = mmem(pfn, rc)
    # print(pt, pm)
    if len(pp) ==1:
        x,y = pp[0]
        qt = mtime(qf, d, x, y)
        qm = mmem(qf, d, x,y)
    else:
        qt = mtime(rq, qf,d, pp)
        qm = mmem(rq, qf, d,pp)
    return pt, qt, pm,qm

def bsc():
    n1 = 2000; m1 = 2000
    n2 = 3000; m2 = 3000
    n3 = 3000
    return [
        ("1. N=2000 nested, M=2000 at center", gn(n1), [(10*n1, 10*n1)] *m1),
        ("2. N=3000 random, M=3000 miss all", grnd(n2, sd=77), [(10**9 +13, 10**9+17)] *m2),
        ("3. N=3000 nested, M=1 at center", gn(n3), [(10 *n3, 10*n3)]),
    ]

def msc():
    n1 = 200; n2 = 200
    n3 = 150; m3 = 1000
    return [
        ("1. N=200 nested", gn(n1), [(10 *n1, 10*n1)]),
        ("2. N=200 distinct non-nested coords", gdc(n2, sd=23), [(500_000,500_000)]),
        ("3. N=150 nested, M=1000 hash queries", gn(n3), gph(n3,m3)),
    ]

def tsc():
    n = 2000; m = 2000
    sp = []
    for i in range(m):
        sp.append((500_000_000, (i *998244353) % 1_000_000))
    return [
        ("1. N=2000 distinct coords, M=2000 hash queries", gdc(n, sd=31), gph(n,m)),
        ("2. N=2000 same x-interval, M=2000 queries", gsx(n, sd=41), sp),
        ("3. N=2000 nested, M=2000 hash queries", gn(n), gph(n, m)),
    ]

def chart(nm, res):
    fig, ax = plt.subplots(1, 3, figsize=(18, 5), gridspec_kw={"wspace": 0.9})
    for k in range(3):
        a = ax[k]
        lb, pt,qt, pm,qm = res[k]
        a2 = a.twinx()
        # print(lb)
        b1 = a.bar([0], [pt +qt], color='blue', width=0.6)
        b2 = a2.bar([1], [pm+ qm], color='orange', width=0.6)
        a.set_yscale('log'); a2.set_yscale('log')
        a.set_xticks([0, 1])
        a.set_xticklabels(['time', 'memory'])
        a.set_ylabel('time (s)')
        a2.set_ylabel('memory (bytes)')
        a.set_title(lb)
        a.legend([b1,b2], ['time', 'memory'], loc='upper left')
    fig.suptitle(nm)
    plt.savefig('charts/%s.png' % nm, bbox_inches='tight')
    plt.close()

def run(nm, pfn, qf, sc):
    print("\n=== %s ===" % nm)
    res = []
    for lb,rc, pp in sc:
        pt, qt, pm,qm = coll(pfn, qf, rc, pp)
        print("%s: prep_time=%.6fs query_time=%.6fs prep_mem=%dB query_mem=%dB" % (lb, pt, qt, pm, qm))
        res.append((lb, pt, qt, pm, qm))
    chart(nm, res)

if __name__ == "__main__":
    # print(time.time())
    run("brute", ident, brute_query, bsc())
    run("map_algo", mp_prep, mp_qr, msc())
    run("tree_algo", tr_prep, tr_qr, tsc())
    # print(time.time())
