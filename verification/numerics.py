"""Descriptive numerical experiments (not used in any proof) for the qutrit paper.
Requires numpy and scipy. Seeds are fixed. Output: JSON on stdout."""
import json, itertools, sys
import numpy as np, scipy.optimize as so

def S(w):
    w = np.asarray(w); w = w[np.abs(w) > 1e-13]; return float(-np.sum(w*np.log(np.abs(w))))
def mutual(ks, rho):
    d = rho.shape[0]; m = ks[0].shape[0]
    J = sum(np.einsum('kj,li->ikjl', K, K.conj()).reshape(d*m, d*m) for K in ks)
    A = np.kron(rho, np.eye(m)); R = (A@J + J@A)/2
    return S(np.linalg.eigvalsh(rho)) + S(np.linalg.eigvalsh(sum(K@rho@K.conj().T for K in ks))) - S(np.linalg.eigvalsh(R))
def unpack(x, d, m, r):
    n = r*m*d
    V = (x[:n] + 1j*x[n:2*n]).reshape(r*m, d); Q, _ = np.linalg.qr(V)
    ks = [Q[a*m:(a+1)*m] for a in range(r)]
    G = (x[2*n:2*n+d*d] + 1j*x[2*n+d*d:2*n+2*d*d]).reshape(d, d)
    rho = G@G.conj().T; rho /= np.trace(rho).real
    return ks, rho
out = {}
# 1. unconstrained searches over complex channels and arbitrary states
searches = {}
for (m, r, seed) in [(3, 3, 3), (3, 9, 4), (2, 3, 1), (2, 6, 2)]:
    rng = np.random.default_rng(seed); best = np.inf
    for _ in range(25):
        res = so.minimize(lambda x: mutual(*unpack(x, 3, m, r)), rng.normal(size=2*r*m*3+18), method='L-BFGS-B')
        best = min(best, res.fun)
    searches[f"3->{m}, Kraus rank {r}, seed {seed}, 25 starts"] = best
out["unconstrained_minimum_found"] = searches
# 1b. structured 3->2 search: real Kraus rank 3, input diag(0, p, 1-p)
def unpack_r(x):
    V = x[:18].reshape(6, 3); Q, _ = np.linalg.qr(V)
    pv = 1/(1+np.exp(-x[-1])); return [Q[0:2], Q[2:4], Q[4:6]], np.diag([0, pv, 1-pv])
rng = np.random.default_rng(1); best = (np.inf, None)
for _ in range(40):
    res = so.minimize(lambda x: mutual(*unpack_r(x)), rng.normal(size=19), method='BFGS')
    if res.fun < best[0]: best = (res.fun, res.x)
ksb, rb = unpack_r(best[1])
out["structured_3to2_minimum_found"] = {"I": best[0], "input_diag": np.diag(rb).tolist()}
# 2. tensor powers of the coherent erasure family at t* = 0.1121973924
def base(t):
    s = np.sqrt(1-t); u = lambda i, j: np.outer(np.eye(3)[i], np.eye(3)[j])
    return [u(1,0)/np.sqrt(2) - s*u(0,1), u(2,0)/np.sqrt(2) - s*u(0,2), np.sqrt(t)*(u(2,1) - u(1,2))]
t = 0.1121973924; ks = base(t); rho = np.diag([0, .5, .5]); tens = {}
for k in (1, 2, 3):
    kk = [np.array([[1.0]])]; rk = np.array([[1.0]])
    for _ in range(k):
        kk = [np.kron(a, b) for a in kk for b in ks]; rk = np.kron(rk, rho)
    tens[str(k)] = mutual(kk, rk)
out["tensor_powers_at_t_star"] = tens
# 3. sanity: pure inputs never violate (Proposition 2), random channels
rng = np.random.default_rng(7); worst = np.inf
for _ in range(2000):
    d = int(rng.integers(2, 5)); m = int(rng.integers(2, 5)); r = int(rng.integers(1, 5)); r = max(r, -(-d//m))
    V = rng.normal(size=(r*m, d)) + 1j*rng.normal(size=(r*m, d)); Q, _ = np.linalg.qr(V)
    psi = rng.normal(size=d) + 1j*rng.normal(size=d); psi /= np.linalg.norm(psi)
    worst = min(worst, mutual([Q[a*m:(a+1)*m] for a in range(r)], np.outer(psi, psi.conj())))
out["pure_input_random_minimum"] = worst
# 4. random sampling of qutrit processes (rank-two inputs, Kraus rank 1-3)
rng = np.random.default_rng(11); neg = 0; N = 4000
for _ in range(N):
    r = int(rng.integers(1, 4))
    V = rng.normal(size=(3*r, 3)) + 1j*rng.normal(size=(3*r, 3)); Q, _ = np.linalg.qr(V)
    U, _ = np.linalg.qr(rng.normal(size=(3, 3)) + 1j*rng.normal(size=(3, 3)))
    pv = rng.uniform(); rho = U@np.diag([0, pv, 1-pv])@U.conj().T
    if mutual([Q[a*3:(a+1)*3] for a in range(r)], rho) < -1e-10: neg += 1
out["random_rank_two_qutrit_processes"] = {"samples": N, "negative": neg}
print(json.dumps(out, indent=2))
