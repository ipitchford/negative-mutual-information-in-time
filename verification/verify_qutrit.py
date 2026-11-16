"""Exact checks for 'Negative mutual information in time in the smallest dimensions'.

Every check raises SystemExit on failure (no `assert`, so the script also fails correctly
under `python -O`). Requires SymPy (mpmath is bundled with SymPy). Output: JSON on stdout.
Run:  python3 verify_qutrit.py > verification.json
"""
import json, sys
import sympy as sp
import mpmath as mp

R_ = sp.Rational
FAIL = []
def check(cond, name):
    if not bool(cond):
        FAIL.append(name)
        print(f"CHECK FAILED: {name}", file=sys.stderr)
        raise SystemExit(1)
    return True

def unit(i, j, n=3, m=None):
    M = sp.zeros(n, m if m else n); M[i, j] = 1; return M

def pdm(chan, rho, d, m):
    """R = (1/2){rho (x) 1_m, J}, J = sum_ij |i><j| (x) chan(|j><i|) (input first)."""
    J = sp.zeros(d*m)
    for i in range(d):
        for j in range(d):
            J += sp.kronecker_product(unit(i, j, d), chan(unit(j, i, d)))
    A = sp.kronecker_product(rho, sp.eye(m))
    return ((A*J + J*A)/2).applyfunc(sp.nsimplify), J

def marginals(R, d, m):
    ra = sp.Matrix(d, d, lambda i, j: sum(R[m*i+k, m*j+k] for k in range(m)))
    rb = sp.Matrix(m, m, lambda i, j: sum(R[m*k+i, m*k+j] for k in range(d)))
    return ra, rb

x = sp.Symbol('x')
out = {}

# ---------- 1. Coherent erasure family E_t (3 -> 3), Theorems 4.1 and 4.3 ----------
def kraus_t(t):
    s = sp.sqrt(1-t)
    return [unit(1,0)/sp.sqrt(2) - s*unit(0,1), unit(2,0)/sp.sqrt(2) - s*unit(0,2),
            sp.sqrt(t)*(unit(2,1) - unit(1,2))]
rho3 = sp.diag(0, R_(1,2), R_(1,2))
fam = []
for t in [R_(5,21), R_(7,40), R_(11,96)]:
    ks = kraus_t(t)
    chan = lambda X, ks=ks: sum((k*X*k.H for k in ks), sp.zeros(3)).applyfunc(sp.simplify)
    check(sum((k.H*k for k in ks), sp.zeros(3)).applyfunc(sp.simplify) == sp.eye(3), f"TP t={t}")
    Eout = chan(rho3)
    check(Eout == sp.diag(1-t, t/2, t/2), f"output t={t}")
    R, J = pdm(chan, rho3, 3, 3)
    ra, rb = marginals(R, 3, 3)
    check(ra == rho3 and rb == Eout, f"marginals t={t}")
    r = sp.sqrt(t*t - t + 1)
    expected = x**2*(x-t/2)**3*(x-(1-t)/2)**2*(x-(-t+r)/4)*(x-(-t-r)/4)
    check(sp.expand(R.charpoly(x).as_expr() - expected) == 0, f"spectrum t={t}")
    # closed form I(t) vs direct evaluation from the spectrum
    def H(v): return 0 if v == 0 else -v*sp.log(abs(v))
    spec = [0,0] + [t/2]*3 + [(1-t)/2]*2 + [(-t+r)/4, (-t-r)/4]
    Idirect = H(R_(1,2))*2 + sum(H(v) for v in Eout.diagonal()) - sum(H(v) for v in spec)
    Iform = t/2*sp.log(2*t) + (-t+r)/4*sp.log((-t+r)/4) + (-t-r)/4*sp.log((t+r)/4)
    check(abs(sp.N(Idirect - Iform, 50)) < 1e-45, f"I(t) formula t={t}")
    fam.append({"t": str(t), "spectrum_charpoly": str(sp.factor(R.charpoly(x).as_expr())),
                "I_nats": str(sp.N(Iform, 25))})
out["family"] = fam

# ---------- 2. Integer certificate ----------
num, den = 5**5*7**7, 2**14*3**12
check(num == 2573571875 and den == 8707129344 and num < den and 3*num < den, "integer certificate")
t = R_(5,21); r = sp.sqrt(t*t-t+1)
check(sp.simplify(r - R_(19,21)) == 0, "r(5/21)=19/21")
I521 = t/2*sp.log(2*t) + R_(1,6)*sp.log(R_(1,6)) + R_(-2,7)*sp.log(R_(2,7))
check(sp.simplify(42*I521 - sp.log(sp.Rational(num, den))) == 0 or abs(sp.N(42*I521 - sp.log(sp.Rational(num,den)), 60)) < 1e-55, "42 I(5/21) = log(num/den)")
out["certificate"] = {"inequality": f"{num} < {den}", "also": f"3*{num} = {3*num} < {den}",
                      "I(5/21)_nats": str(sp.N(I521, 30))}

# ---------- 3. Convexity: I'' formula and its rational lower bound ----------
T = sp.Symbol('t', positive=True)
rT = sp.sqrt(T*T - T + 1)
IT = T/2*sp.log(2*T) + (rT-T)/4*sp.log((rT-T)/4) - (rT+T)/4*sp.log((rT+T)/4)
d2 = sp.diff(IT, T, 2)
claimed = 1/(2*T) + (4*T**2-7*T+4)/(8*(1-T)*rT**2) - 3/(8*rT**3)*sp.atanh(T/rT)
for tv in [R_(1,100), R_(1,10), R_(3,10), R_(1,2), R_(9,10), R_(99,100)]:
    check(abs(sp.N((d2-claimed).subs(T, tv), 50)) < 1e-40, f"I'' formula at {tv}")
r2 = T*T - T + 1
lower = R_(1,2)/T + (4*T*T-7*T+4)/(8*(1-T)*r2) - 3*T/(8*r2*r2) - T**3/(8*r2*r2*(1-T))
check(sp.factor(lower - (T*T-2*T+2)/(4*T*r2*r2)) == 0, "rational lower bound identity")
check(sp.limit(IT, T, 0, '+') == 0 and sp.simplify(sp.limit(IT, T, 1, '-') - sp.log(2)) == 0, "endpoint values")
mp.mp.dps = 40
f = sp.lambdify(T, IT, 'mpmath'); fp = sp.lambdify(T, sp.diff(IT, T), 'mpmath')
tstar = mp.findroot(fp, 0.11); tau = mp.findroot(f, 0.3)
tau_exact = (sp.sqrt(33) - 1)/16
check(sp.simplify(sp.sqrt(tau_exact**2 - tau_exact + 1) - 3*tau_exact) == 0, "r(tau) = 3 tau")
check(abs(sp.N(IT.subs(T, tau_exact), 60)) < 1e-55 and abs(tau - mp.mpf(str(sp.N(tau_exact, 45)))) < mp.mpf(10)**-30, "tau = (sqrt33-1)/16 is the zero")
I1196 = sp.Rational(1,192)*sp.log(sp.Integer(2)**142*sp.Integer(5)**40*sp.Integer(11)**11/sp.Integer(51)**51)
check(abs(sp.N(I1196 - IT.subs(T, R_(11,96)), 50)) < 1e-45, "I(11/96) closed form")
out["family_numbers"] = {"t_star": mp.nstr(tstar, 15), "I_t_star": mp.nstr(f(tstar), 15),
                         "tau": mp.nstr(tau, 15), "tau_exact": "(sqrt(33)-1)/16", "I(11/96)": str(sp.N(I1196, 15)),
                         "max_I_on_[0,1]_is_log2": "endpoint value; convexity gives max at an endpoint"}

# ---------- 4. Qubit-output witness F (3 -> 2), Theorem 5.1 ----------
p, c1, c2, e, a, b = R_(1,47), R_(124,125), R_(1,47), R_(-1,232), R_(1,64), R_(1,841)
tab = {(0,0): unit(0,0,2), (0,1): c1*unit(0,1,2), (0,2): c2*unit(0,1,2),
       (1,1): sp.diag(a, 1-a), (2,2): sp.diag(b, 1-b), (1,2): e*sp.diag(1,-1)}
def Fmu(i, j): return tab[(i,j)] if (i,j) in tab else tab[(j,i)].T
def Fchan(X):
    return sum((X[i,j]*Fmu(i,j) for i in range(3) for j in range(3)), sp.zeros(2))
check(all(sp.trace(Fmu(i,j)) == (1 if i == j else 0) for i in range(3) for j in range(3)), "F trace preserving")
C = sp.zeros(6)
for i in range(3):
    for j in range(3):
        C[2*i:2*i+2, 2*j:2*j+2] = Fmu(i, j)
check(C == C.T, "Choi symmetric")
cpC = sp.Poly(C.charpoly(x).as_expr(), x)
# all roots real (symmetric); no negative root iff coefficients alternate in sign (Descartes)
coeffs = [c for c in cpC.all_coeffs()]
alt = all(coeffs[k] == 0 or coeffs[k]*(-1)**k > 0 for k in range(len(coeffs)))
check(alt, "Choi PSD (alternating characteristic coefficients)")
rhoF = sp.diag(0, p, 1-p)
RF, JF = pdm(Fchan, rhoF, 3, 2)
raF, rbF = marginals(RF, 3, 2)
outF = Fchan(rhoF)
check(raF == rhoF and rbF == outF, "F marginals")
PF = sp.Poly(RF.charpoly(x).as_expr(), x)
iv = mp.iv; iv.dps = 60; mp.mp.dps = 60
def mpq(q): q = sp.Rational(q); return iv.mpf(int(q.p))/iv.mpf(int(q.q))  # outward-rounded
roots = []
for fct, mult in sp.factor_list(PF.as_expr())[1]:
    for (lo, hi), k in sp.Poly(fct, x).intervals(eps=R_(1, 10**45)):
        roots += [(lo, hi)]*(k*mult)
check(len(roots) == 6, "six eigenvalues isolated")
def h_iv(lo, hi):
    if lo == 0 and hi == 0: return iv.mpf(0)
    X = iv.mpf([mpq(lo).a, mpq(hi).b])
    if lo > 0: return -X*iv.log(X)
    if hi < 0: return -X*iv.log(-X)
    raise SystemExit("root interval straddles zero")
def h_exact(v): return iv.mpf(0) if v == 0 else -mpq(v)*iv.log(mpq(v))
SR = sum((h_iv(lo, hi) for lo, hi in roots), iv.mpf(0))
SA = sum((h_exact(v) for v in rhoF.diagonal()), iv.mpf(0))
SB = sum((h_exact(v) for v in outF.diagonal()), iv.mpf(0))
check(outF.is_diagonal(), "F output diagonal")
IF = SA + SB - SR
check(IF.b < 0, "qubit-output witness negative (interval upper end < 0)")
def exact(raw):  # exact rational value of a raw binary endpoint (sign, mantissa, exponent, bitcount)
    sgn, man, ex, _ = raw
    return (-1)**sgn * sp.Rational(int(man)) * sp.Rational(2)**int(ex)
lo_x, hi_x = exact(IF._mpi_[0]), exact(IF._mpi_[1])
check(lo_x <= hi_x and hi_x - lo_x < sp.Rational(1, 10**40), "enclosure is tight")
check(sp.Rational("-0.00139052762357144") < lo_x and hi_x < sp.Rational("-0.00139052762357143"),
      "enclosure lies inside the interval stated in Theorem 5.1")
scale = sp.Integer(10)**40
lo_s = sp.floor(lo_x*scale)/scale; hi_s = sp.ceiling(hi_x*scale)/scale  # directed (outward) decimal rounding
out["qubit_output_witness"] = {
    "choi_charpoly": str(sp.factor(cpC.as_expr())),
    "output_state": [str(v) for v in outF.diagonal()],
    "pdm_charpoly_factors": [str(fct) for fct, _ in sp.factor_list(PF.as_expr())[1]],
    "I_interval_nats_outward_40_digits": [str(sp.N(lo_s, 45)), str(sp.N(hi_s, 45))]}

# ---------- 5. Proposition 6.1 (interior) constants ----------
mp.mp.dps = 30
delta = mp.mpf(3)*mp.mpf(10)**-6
omega = delta*mp.log(2*mp.e/delta)
check(15*omega < mp.mpf('0.00072'), "15 omega(3e-6) < 0.00072")
check(mp.mpf(5)/2 < mp.e and (mp.mpf(5)/2)**15 > 2/delta, "log(2e/delta) < 16 certificate")
check(-mp.mpf(1)/42 + mp.mpf('0.00072') < 0, "perturbed value negative")
# actual perturbed value, numerically (descriptive)
eps = eta = R_(1, 10**6); t = R_(5,21)
ks = kraus_t(t)
def chan_eta(X):
    base = sum((k*X*k.H for k in ks), sp.zeros(3))
    return ((1-eta)*base + eta*sp.trace(X)*sp.eye(3)/3)
rhoe = sp.diag(eps, (1-eps)/2, (1-eps)/2)
Re, _ = pdm(lambda X: chan_eta(X).applyfunc(sp.nsimplify), rhoe, 3, 3)
def Snum(M):
    w = [complex(v) for v in sp.Matrix(M).evalf(40).eigenvals(multiple=True)]
    return -sum(z.real*mp.log(abs(z.real)) for z in w if abs(z.real) > 1e-30)
Ie = Snum(rhoe) + Snum(chan_eta(rhoe)) - Snum(Re)
check(Ie < 0, "actual perturbed value negative")
out["interior"] = {"15*omega(3e-6)": mp.nstr(15*omega, 10), "I_perturbed_numeric": mp.nstr(Ie, 12)}

# ---------- 6. Support restriction (Proposition 7.1) ----------
t = R_(5,21); ks = kraus_t(t)
inc = [unit(1,0)/sp.sqrt(2), unit(2,0)/sp.sqrt(2), sp.sqrt(1-t)*unit(0,1), sp.sqrt(1-t)*unit(0,2), ks[2]]
check(sum((k.H*k for k in inc), sp.zeros(3)).applyfunc(sp.simplify) == sp.eye(3), "incoherent TP")
chE = lambda X: sum((k*X*k.H for k in ks), sp.zeros(3)).applyfunc(sp.simplify)
chI = lambda X: sum((k*X*k.H for k in inc), sp.zeros(3)).applyfunc(sp.simplify)
agree = all(chE(unit(i,j)) == chI(unit(i,j)) for i in range(3) for j in range(3) if (i == 0) == (j == 0))
differ = [(i,j) for i in range(3) for j in range(3) if chE(unit(i,j)) != chI(unit(i,j))]
check(agree and sorted(differ) == [(0,1),(0,2),(1,0),(2,0)], "completions differ only on cross blocks")
Rinc, _ = pdm(chI, rho3, 3, 3)
# restricted channel on span{|1>,|2>}: embed qubit input
def Fres(X2):
    X = sp.zeros(3); X[1:,1:] = X2; return chE(X)
Rres, _ = pdm(Fres, sp.eye(2)/2, 2, 3)
check(Rinc[3:, 3:] == Rres and Rinc[:3, :] == sp.zeros(3, 9) and Rinc[:, :3] == sp.zeros(9, 3), "incoherent PDM = restricted PDM (+) 0")
check(sp.expand(Rres.charpoly(x).as_expr() - (x-(1-t)/2)**2*(x-t/2)**3*(x+t/2)) == 0, "restricted spectrum")
out["support_restriction"] = {"I_incoherent(5/21)": str(sp.N(t*sp.log(2), 20)), "I_coherent(5/21)": str(sp.N(I521, 20))}

out["all_checks_passed"] = True
print(json.dumps(out, indent=2))
