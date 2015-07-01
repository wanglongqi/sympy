from sympy.polys.domains import QQ
from sympy.polys.rings import ring
from sympy.polys.ring_series import (_invert_monoms, rs_integrate,
  rs_trunc, rs_mul, rs_square, rs_pow, _has_constant_term, rs_series_inversion,
  rs_series_from_list, rs_exp, rs_log, rs_newton, rs_hadamard_exp,
  rs_compose_add, rs_atan, rs_atanh, rs_tan, rs_sin, rs_cos, rs_cos_sin,
  rs_sinh, rs_cosh, rs_tanh, _tan1, fun, rs_series_reversion)
from sympy.utilities.pytest import raises
from sympy.core.compatibility import range

def test_ring_series1():
    R, x = ring('x', QQ)
    p = x**4 + 2*x**3 + 3*x + 4
    assert _invert_monoms(p) == 4*x**4 + 3*x**3 + 2*x + 1
    assert rs_hadamard_exp(p) == x**4/24 + x**3/3 + 3*x + 4
    R, x = ring('x', QQ)
    p = x**4 + 2*x**3 + 3*x + 4
    assert rs_integrate(p, x) == x**5/5 + x**4/2 + 3*x**2/2 + 4*x
    R, x, y = ring('x, y', QQ)
    p = x**2*y**2 + x + 1
    assert rs_integrate(p, x) == x**3*y**2/3 + x**2/2 + x
    assert rs_integrate(p, y) == x**2*y**3/3 + x*y + y

def test_trunc():
    R, x, y, t = ring('x, y, t', QQ)
    p = (y + t*x)**4
    p1 = rs_trunc(p, x, 3)
    assert p1 == y**4 + 4*y**3*t*x + 6*y**2*t**2*x**2

def test_mul_trunc():
    R, x, y, t = ring('x, y, t', QQ)
    p = 1 + t*x + t*y
    for i in range(2):
        p = rs_mul(p, p, t, 3)

    assert p == 6*x**2*t**2 + 12*x*y*t**2 + 6*y**2*t**2 + 4*x*t + 4*y*t + 1
    p = 1 + t*x + t*y + t**2*x*y
    p1 = rs_mul(p, p, t, 2)
    assert p1 == 1 + 2*t*x + 2*t*y
    R1, z = ring('z', QQ)
    def test1(p):
        p2 = rs_mul(p, z, x, 2)
    raises(ValueError, lambda: test1(p))

    p1 = 2 + 2*x + 3*x**2
    p2 = 3 + x**2
    assert rs_mul(p1, p2, x, 4) == 2*x**3 + 11*x**2 + 6*x + 6

def test_square_trunc():
    R, x, y, t = ring('x, y, t', QQ)
    p = (1 + t*x + t*y)*2
    p1 = rs_mul(p, p, x, 3)
    p2 = rs_square(p, x, 3)
    assert p1 == p2
    p = 1 + x + x**2 + x**3
    assert rs_square(p, x, 4) == 4*x**3 + 3*x**2 + 2*x + 1

def test_pow_trunc():
    R, x, y, z = ring('x, y, z', QQ)
    p0 = y + x*z
    p = p0**16
    for xx in (x, y, z):
        p1 = rs_trunc(p, xx, 8)
        p2 = rs_pow(p0, 16, xx, 8)
        assert p1 == p2

    p = 1 + x
    p1 = rs_pow(p, 3, x, 2)
    assert p1 == 1 + 3*x
    assert rs_pow(p, 0, x, 2) == 1
    assert rs_pow(p, -2, x, 2) == 1 - 2*x
    p = x + y
    assert rs_pow(p, 3, y, 3) == x**3 + 3*x**2*y + 3*x*y**2

def test_has_constant_term():
    R, x, y, z = ring('x, y, z', QQ)
    p = y + x*z
    assert _has_constant_term(p, x)
    p = x + x**4
    assert not _has_constant_term(p, x)
    p = 1 + x + x**4
    assert _has_constant_term(p, x)
    p = x + y + x*z

def test_inversion():
    R, x = ring('x', QQ)
    p = 2 + x + 2*x**2
    n = 5
    p1 = rs_series_inversion(p, x, n)
    assert rs_trunc(p*p1, x, n) == 1
    R, x, y = ring('x, y', QQ)
    p = 2 + x + 2*x**2 + y*x + x**2*y
    p1 = rs_series_inversion(p, x, n)
    assert rs_trunc(p*p1, x, n) == 1

    R, x, y = ring('x, y', QQ)
    p = 1 + x + y
    def test2(p):
        p1 = rs_series_inversion(p, x, 4)
    raises(NotImplementedError, lambda: test2(p))

def test_series_reversion():
    R, x, y = ring('x, y', QQ)

    p = rs_tan(x, x, 10)
    assert rs_series_reversion(p, x, 8, y) == rs_atan(y, y, 8)

    p = rs_sin(x, x, 10)
    assert rs_series_reversion(p, x, 8, y) == 5*y**7/112 + 3*y**5/40 + \
        y**3/6 + y

def test_series_from_list():
    R, x = ring('x', QQ)
    p = 1 + 2*x + x**2 + 3*x**3
    c = [1, 2, 0, 4, 4]
    r = rs_series_from_list(p, c, x, 5)
    pc = R.from_list(list(reversed(c)))
    r1 = rs_trunc(pc.compose(x, p), x, 5)
    assert r == r1
    R, x, y = ring('x, y', QQ)
    c = [1, 3, 5, 7]
    p1 = rs_series_from_list(x + y, c, x, 3, concur=0)
    p2 = rs_trunc((1 + 3*(x+y) + 5*(x+y)**2 + 7*(x+y)**3), x, 3)
    assert p1 == p2

    R, x = ring('x', QQ)
    h = 25
    p = rs_exp(x, x, h) - 1
    p1 = rs_series_from_list(p, c, x, h)
    p2 = 0
    for i, cx in enumerate(c):
        p2 += cx*rs_pow(p, i, x, h)
    assert p1 == p2

def test_log():
    R, x = ring('x', QQ)
    p = 1 + x
    p1 = rs_log(p, x, 4)
    assert p1 == x - x**2/2 + x**3/3
    p = 1 + x +2*x**2/3
    p1 = rs_log(p, x, 9)
    assert p1 == -17*x**8/648 + 13*x**7/189 - 11*x**6/162 - x**5/45 + \
      7*x**4/36 - x**3/3 + x**2/6 + x
    p2 = rs_series_inversion(p, x, 9)
    p3 = rs_log(p2, x, 9)
    assert p3 == -p1

    R, x, y = ring('x, y', QQ)
    p = 1 + x + 2*y*x**2
    p1 = rs_log(p, x, 6)
    assert p1 == (4*x**5*y**2 - 2*x**5*y - 2*x**4*y**2 + x**5/5 + 2*x**4*y -
                  x**4/4 - 2*x**3*y + x**3/3 + 2*x**2*y - x**2/2 + x)

def test_exp():
    R, x = ring('x', QQ)
    p = x + x**4
    for h in [10, 30]:
        q = rs_series_inversion(1 + p, x, h) - 1
        p1 = rs_exp(q, x, h)
        q1 = rs_log(p1, x, h)
        assert q1 == q
    p1 = rs_exp(p, x, 30)
    assert p1.coeff(x**29) == QQ(74274246775059676726972369, 353670479749588078181744640000)
    prec = 21
    p = rs_log(1 + x, x, prec)
    p1 = rs_exp(p, x, prec)
    assert p1 == x + 1

def test_newton():
    R, x = ring('x', QQ)
    p = x**2 - 2
    r = rs_newton(p, x, 4)
    f = [1, 0, -2]
    assert r == 8*x**4 + 4*x**2 + 2

def test_compose_add():
    R, x = ring('x', QQ)
    p1 = x**3 - 1
    p2 = x**2 - 2
    assert rs_compose_add(p1, p2) == x**6 - 6*x**4 - 2*x**3 + 12*x**2 - 12*x - 7

def test_fun():
    R, x, y = ring('x, y', QQ)
    p = x*y + x**2*y**3 + x**5*y
    assert fun(p, rs_tan, x, 10) == rs_tan(p, x, 10)
    assert fun(p, _tan1, x, 10) == _tan1(p, x, 10)

def test_atan():
    R, x, y = ring('x, y', QQ)
    assert rs_atan(x, x, 9) == -1/7*x**7 + 1/5*x**5 - 1/3*x**3 + x
    assert rs_atan(x*y + x**2*y**3, x, 9) == 2*x**8*y**11 - x**8*y**9 + \
        2*x**7*y**9 - 1/7*x**7*y**7 - 1/3*x**6*y**9 + x**6*y**7 - x**5*y**7 + \
        1/5*x**5*y**5 - x**4*y**5 - 1/3*x**3*y**3 + x**2*y**3 + x*y

def test_tan():
    R, x, y = ring('x, y', QQ)
    assert rs_tan(x, x, 9) == \
        x + x**3/3 + 2*x**5/15 + 17*x**7/315
    assert rs_tan(x*y + x**2*y**3, x, 9) == 4/3*x**8*y**11 + 17/45*x**8*y**9 + \
        4/3*x**7*y**9 + 17/315*x**7*y**7 + 1/3*x**6*y**9 + 2/3*x**6*y**7 + \
        x**5*y**7 + 2/15*x**5*y**5 + x**4*y**5 + 1/3*x**3*y**3 + x**2*y**3 + x*y

def test_sin():
    R, x, y = ring('x, y', QQ)
    assert rs_sin(x, x, 9) == \
        x - x**3/6 + x**5/120 - x**7/5040
    assert rs_sin(x*y + x**2*y**3, x, 9) == 1/12*x**8*y**11 - \
        1/720*x**8*y**9 + 1/12*x**7*y**9 - 1/5040*x**7*y**7 - 1/6*x**6*y**9 \
        + 1/24*x**6*y**7 - 1/2*x**5*y**7 + 1/120*x**5*y**5 - 1/2*x**4*y**5 \
        - 1/6*x**3*y**3 + x**2*y**3 + x*y

def test_cos():
    R, x, y = ring('x, y', QQ)
    assert rs_cos(x, x, 9) == \
        1/40320*x**8 - 1/720*x**6 + 1/24*x**4 - 1/2*x**2 + 1
    assert rs_cos(x*y + x**2*y**3, x, 9) == 1/24*x**8*y**12 - \
        1/48*x**8*y**10 + 1/40320*x**8*y**8 + 1/6*x**7*y**10 - \
        1/120*x**7*y**8 + 1/4*x**6*y**8 - 1/720*x**6*y**6 + 1/6*x**5*y**6 \
        - 1/2*x**4*y**6 + 1/24*x**4*y**4 - x**3*y**4 - 1/2*x**2*y**2 + 1

def test_cos_sin():
    R, x, y = ring('x, y', QQ)
    cos, sin = rs_cos_sin(x, x, 9)
    assert cos == rs_cos(x, x, 9)
    assert sin == rs_sin(x, x, 9)
    cos, sin = rs_cos_sin(x + x*y, x, 5)
    assert cos == rs_cos(x + x*y, x, 5)
    assert sin == rs_sin(x + x*y, x, 5)

def test_atanh():
    R, x, y = ring('x, y', QQ)
    assert rs_atanh(x, x, 9) == 1/7*x**7 + 1/5*x**5 + 1/3*x**3 + x
    assert rs_atanh(x*y + x**2*y**3, x, 9) == 2*x**8*y**11 + x**8*y**9 + \
        2*x**7*y**9 + 1/7*x**7*y**7 + 1/3*x**6*y**9 + x**6*y**7 + x**5*y**7 + \
        1/5*x**5*y**5 + x**4*y**5 + 1/3*x**3*y**3 + x**2*y**3 + x*y

def test_sinh():
    R, x, y = ring('x, y', QQ)
    assert rs_sinh(x, x, 9) == 1/5040*x**7 + 1/120*x**5 + 1/6*x**3 + x
    assert rs_sinh(x*y + x**2*y**3, x, 9) == 1/12*x**8*y**11 + \
        1/720*x**8*y**9 + 1/12*x**7*y**9 + 1/5040*x**7*y**7 + 1/6*x**6*y**9 + \
        1/24*x**6*y**7 + 1/2*x**5*y**7 + 1/120*x**5*y**5 + 1/2*x**4*y**5 + \
        1/6*x**3*y**3 + x**2*y**3 + x*y

def test_cosh():
    R, x, y = ring('x, y', QQ)
    assert rs_cosh(x, x, 9) == 1/40320*x**8 + 1/720*x**6 + 1/24*x**4 + \
        1/2*x**2 + 1
    assert rs_cosh(x*y + x**2*y**3, x, 9) == 1/24*x**8*y**12 + \
        1/48*x**8*y**10 + 1/40320*x**8*y**8 + 1/6*x**7*y**10 + \
        1/120*x**7*y**8 + 1/4*x**6*y**8 + 1/720*x**6*y**6 + 1/6*x**5*y**6 + \
        1/2*x**4*y**6 + 1/24*x**4*y**4 + x**3*y**4 + 1/2*x**2*y**2 + 1

def test_tanh():
    R, x, y = ring('x, y', QQ)
    assert rs_tanh(x, x, 9) == -17/315*x**7 + 2/15*x**5 - 1/3*x**3 + x
    assert rs_tanh(x*y + x**2*y**3 , x, 9) == 4/3*x**8*y**11 - \
        17/45*x**8*y**9 + 4/3*x**7*y**9 - 17/315*x**7*y**7 - 1/3*x**6*y**9 + \
        2/3*x**6*y**7 - x**5*y**7 + 2/15*x**5*y**5 - x**4*y**5 - \
        1/3*x**3*y**3 + x**2*y**3 + x*y
