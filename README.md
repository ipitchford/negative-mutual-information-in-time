# Negative mutual information in time in the smallest dimensions

*Three levels in, two out, a rank-two start: the exact point where a proposed quantum "mutual information in time" can
turn negative.*

Version 0.1.0-candidate. DOI [10.5281/zenodo.24269629](https://doi.org/10.5281/zenodo.24269629) (all versions:
[10.5281/zenodo.24269628](https://doi.org/10.5281/zenodo.24269628)). Evidence Press page:
https://evidencepress.org/releases/negative-mutual-information-in-time/. Creator: Anonymous. Status: unrefereed research
candidate.

## What this is about

**The question.** For two quantum systems at the same moment, the quantum mutual information measures how much they share,
and it is never negative. Physicists have proposed an analogue for *one* system at *two* times: before and after a
process (a quantum channel). There is no ordinary joint quantum state for two times, so the proposal uses a
"pseudo-density matrix" (a state over time). Unlike an ordinary quantum state it can have negative eigenvalues, so it
also needs an entropy that accepts negative eigenvalues, S(X) = -Tr X log|X|. Fullwood and Parzygnat defined the
resulting mutual information and conjectured that it is never negative either. A mutual information that can go negative
would be hard to read as "shared information".

**What was known.** Fullwood and Yang proved the conjecture whenever the input is a qubit (a preprint). The Omega
Institute published an explicit five-dimensional counterexample, so the conjecture is false in general, and listed the
smallest failing input dimension as open. This package is therefore not the first counterexample.

**What is new.** The exact threshold. A violation needs at least three input levels, at least two output levels, and a
starting state that is not pure (rank at least two). One explicit three-level-in, two-level-out process on a rank-two
state reaches all three bounds at once; its value, about -0.00139 nats, is certified exactly by root isolation and
interval arithmetic. A simple family, a "coherent" version of the textbook erasure channel, shows why: the channel must
keep quantum coherence between the occupied levels and an empty one. Without that coherence, for rank-two states, the
quantity is provably never negative. At the parameter value t = 5/21 the sign comes down to comparing two whole numbers,
2573571875 < 8707129344. Two processes that act identically on everything the system actually occupies can give
opposite signs.

**Limits.** The results concern one specific proposal (the anticommutator state over time with the entropy
-Tr X log|X|). The qubit-input lower bound comes from a preprint. Whether the quantity is unbounded below, and its most
negative value for qutrits, are open; the paper reports numerical evidence only. No operational meaning for negative
values and no replacement measure are offered. This is an unrefereed candidate: assurance is internal AI-assisted review
and computational checks, not peer review.

## For specialists

The paper ([manuscript.pdf](manuscript.pdf), source [manuscript.tex](manuscript.tex)) proves:

- **Thresholds** (Corollaries 4.2 and 5.2): every violation has input dimension d >= 3, output dimension m >= 2 and
  rank(rho) >= 2. The rank bound is a new proof for pure inputs (Proposition 3.2) from Fullwood and Yang's Lemma 4.4(iv);
  the dimension bound is their Theorem 4.1.
- **Qutrit-to-qubit witness** (Theorem 5.1): an explicit channel F: M_3 -> M_2 with rational data and input
  diag(0, 1/47, 46/47) has I in [-0.00139052762357144, -0.00139052762357143].
- **Mechanism** (Lemma 2.1, Proposition 2.2, Corollary 3.3): in an eigenbasis of rho the state over time is a weighted
  array of the images of matrix units; with no cross-coherence between supp(rho) and its complement, I equals that of the
  restricted channel, so a rank-two violation must be a coherent completion of a qubit-input channel.
- **Coherent erasure family** (Theorems 4.1 and 4.3): E_t on a qutrit with rho = diag(0, 1/2, 1/2) has an explicit
  spectrum; 42 I(5/21) = log(2573571875/8707129344); I(t) is strictly convex, negative exactly for
  0 < t < (sqrt(33) - 1)/16 (about 0.2965), with minimum about -0.0591 nats at t* about 0.112.
- **Robustness and support dependence** (Propositions 6.1 and 7.1): violations persist for full-rank states and
  positive-definite Choi matrices; coherent and incoherent completions that agree on the occupied subspace have opposite
  signs (the incoherent one gives t log 2).

## Technical: files and how to check them

| File | What it is |
|---|---|
| `manuscript.tex`, `manuscript.pdf` | The paper (11 pages); figure 1 is `qutrit_information.pdf` / `.png` |
| `verification/verify_qutrit.py` -> `verification/verification.json` | Exact checks (SymPy, mpmath interval arithmetic): spectra from assembled matrices, integer certificate, convexity formula, witness F with certified interval, Proposition 6.1 constants, support restriction. Every check raises SystemExit, so it also fails under `python -O` |
| `verification/numerics.py` -> `verification/numerics.json` | Descriptive numerics for Section 8 (fixed seeds); not used in any proof |
| `verification/make_figure.py` | Draws figure 1 |
| `requirements.txt`, `ENVIRONMENT.txt`, `REPLAY_RECEIPT.md` | Pinned versions and the release replay |
| `PRIOR_ART.md`, `RESEARCH_GATES.json`, `REVIEW_SUMMARY.md` | Dated prior-art record, research-gate record, internal review objections and dispositions |
| `AI_INDEX.md` | Machine-oriented map of claims, evidence and limits |
| `refs.bib`, `CITATION.cff`, `.zenodo.json`, `LICENSE.md`, `MANIFEST.sha256` | Bibliography, citation metadata, licences, SHA-256 of every file |
| `target.yaml` | Exact statement of the claim and its exclusions |

Replay (Python 3.12):

```sh
uv run --python 3.12 --with sympy==1.14.0 --with mpmath==1.3.0 python -O -I -B verification/verify_qutrit.py > v.json
cmp v.json verification/verification.json            # byte-identical, exit 0
uv run --python 3.12 --with numpy==2.3.5 --with scipy==1.17.0 python -I -B verification/numerics.py > n.json
cd verification && uv run --python 3.12 --with numpy==2.3.5 --with matplotlib==3.11.2 python -I make_figure.py
```

The verifier takes a few seconds and numerics.py about a minute. GitHub CI
([.github/workflows/replay.yml](.github/workflows/replay.yml)) checks the manifest, runs the verifier under `-O` and
compares its output byte for byte with `verification/verification.json` (every field is an exact string or boolean),
and checks two negative controls (a wrong integer certificate; a wrong interval bound), each of which must make the
verifier exit 1 (blocking). A separate non-blocking job reruns `numerics.py` and compares it with
`verification/numerics.json` within a declared tolerance (floats within 1e-6 relative or absolute; integers exactly),
because optimiser minima can differ in the last digits across platforms.

## Licence and credit

Text, figure and data CC0-1.0; code MIT (see [LICENSE.md](LICENSE.md)). The conjecture is due to Fullwood and
Parzygnat; the qubit-input theorem to Fullwood and Yang; the first counterexample to the Omega Institute; the name
"quantum mutual information in time" to Wu, Parzygnat, Vedral and Fullwood. AI-use statement: see the paper.
