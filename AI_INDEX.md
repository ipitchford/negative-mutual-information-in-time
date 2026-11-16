# AI index: Negative mutual information in time in the smallest dimensions (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What this
is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is a plain
introduction with the question, what was known, what is new and a roadmap). DOI 10.5281/zenodo.24269629 (concept
10.5281/zenodo.24269628). Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

Channel E: M_d -> M_m (completely positive, trace preserving); state rho in M_d. Input-first Jamiolkowski matrix
J[E] = sum_ij |i><j| (x) E(|j><i|) (the partial transpose of the Choi matrix); anticommutator state over time
R(E, rho) = {rho (x) 1_m, J[E]}/2, Hermitian, unit trace, marginals rho and E(rho). Signed entropy
S(X) = -sum_lambda lambda log|lambda| (natural log, nats). Mutual information in time
I(E, rho) = S(rho) + S(E(rho)) - S(R(E, rho)) (Fullwood-Parzygnat dynamical mutual information; Wu-Parzygnat-Vedral-
Fullwood quantum mutual information in time). FP = Fullwood and Parzygnat, Entropy 27 (2025) 331; FY = Fullwood and
Yang, arXiv:2608.28946v1 (preprint); Omega = The Omega Institute dossier, release 8f61e708e239.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A | Block form: for diagonal rho, R = sum_ij (rho_i + rho_j)/2 |i><j| (x) E(|j><i|); with no cross-coherence across supp(rho), R ~ R(E|_P, rho|_P) (+) 0 and I(E, rho) = I(E|_P, rho|_P) | Lemma 2.1, Proposition 2.2 | written proof |
| B | I >= 0 for d = 2 (any m), for m = 1, and for pure rho (any channel) | Proposition 3.1, Proposition 3.2 | d = 2 is FY Theorem 4.1 (preprint); pure inputs: written proof from FY Lemma 4.4(iv) |
| C | Rank at most two and no cross-coherence imply I >= 0 | Corollary 3.3 | written proof |
| D | Coherent erasure family E_t (3 -> 3), rho = diag(0, 1/2, 1/2): explicit spectrum; I(5/21) = (1/42) log(2573571875/8707129344) < 0 | Theorem 4.1 | written proof; spectra checked exactly (characteristic polynomials of the assembled matrices) at t = 5/21, 7/40, 11/96; integer certificate checked |
| E | Smallest input dimension over all outputs with a violation is 3; smallest rank is 2 | Corollary 4.2 | depends on FY Theorem 4.1 (preprint) |
| F | I(t) strictly convex on (0,1), I(0) = 0, I(1) = log 2, negative exactly for 0 < t < tau = (sqrt(33) - 1)/16 (about 0.2965); minimiser t* about 0.1122 with I(t*) about -0.0590860; I(11/96) about -0.0590721 in closed form | Theorem 4.3 | written proof; I'' formula and rational lower bound checked symbolically and to 40 digits |
| G | Qutrit-to-qubit witness F with rational data, rho_F = diag(0, 1/47, 46/47): I(F, rho_F) in [-0.00139052762357144, -0.00139052762357143] | Theorem 5.1 | exact root isolation (SymPy, width < 1e-45) and mpmath interval arithmetic (60 digits), outward-rounded enclosure |
| H | (d, m, rank) = (3, 2, 2) are all minimal and attained simultaneously | Corollary 5.2 | written proof from B, E, G |
| I | Violations persist for full-rank states and positive-definite Choi matrices (eps = eta = 1e-6 at t = 5/21; perturbed value about -0.0290183) | Proposition 6.1 | written proof with explicit continuity modulus; constants checked |
| J | Coherent and incoherent completions agreeing on the occupied subspace give I = I(5/21) < 0 and I = t log 2 > 0 | Proposition 7.1 | written proof; completions checked to differ only on the cross blocks |
| K | Numerical observations: searches over qutrit processes reach about -0.0590860 and nothing lower; structured qutrit-to-qubit search -0.0013918; tensor powers -0.05909, -0.11912, -0.18016 (k = 1, 2, 3); 4000 random rank-two qutrit processes, none negative | Section 8 | descriptive numerics only; not claims |

Not claimed: that the quantity is unbounded below; the minimum over qutrit processes; any result for other states over
time or other entropies; an operational meaning of negative values; being the first counterexample (Omega's
five-dimensional Werner-Holevo example is earlier).

## Evidence files

- [verification/verify_qutrit.py](verification/verify_qutrit.py) -> [verification/verification.json](verification/verification.json):
  exact checks for D, F, G, I, J (all fields exact strings; `all_checks_passed: true`).
- [verification/numerics.py](verification/numerics.py) -> [verification/numerics.json](verification/numerics.json): K.
- [verification/make_figure.py](verification/make_figure.py) -> `qutrit_information.pdf`, `qutrit_information.png` (figure 1).
- [requirements.txt](requirements.txt), [ENVIRONMENT.txt](ENVIRONMENT.txt), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md):
  environment and the release replay (normal and `python -O`, negative controls).
- [PRIOR_ART.md](PRIOR_ART.md): dated prior-art record. [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md): internal review
  objections and dispositions. [RESEARCH_GATES.json](RESEARCH_GATES.json): contribution map, sources read in full,
  searches and limitation triage. [target.yaml](target.yaml): exact claim and exclusions.
- [refs.bib](refs.bib): bibliography from Crossref and arXiv records. [LICENSE.md](LICENSE.md): CC0-1.0 text and data,
  MIT code. [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json): citation metadata. CI:
  [.github/workflows/replay.yml](.github/workflows/replay.yml). [MANIFEST.sha256](MANIFEST.sha256): SHA-256 of every file.

## Limits

No human peer review, independent human reproduction or formal verification. The general statements rest on written
proofs; the computations check the stated spectra, certificate, witness and constants. The dimension threshold relies on
a preprint (FY Theorem 4.1). Unboundedness below and the qutrit minimum are open. Priority rests on a bounded search.
