# Replay receipt (release 0.1.0-candidate)

Replayed by the Evidence Press publisher on 16 November 2026 from fresh copies of the approved candidate, working
directory the package copy, CPython 3.12.11 (uv; `sys.version` printed inside the run), `PYTHONDONTWRITEBYTECODE=1`.

| Run | Command | Result |
|---|---|---|
| Exact verifier | `python -I -B verification/verify_qutrit.py` (sympy 1.14.0, mpmath 1.3.0) | exit 0; stdout byte-identical to `verification/verification.json`; about 2 s |
| Exact verifier, optimised | `python -O -I -B verification/verify_qutrit.py` | exit 0; byte-identical |
| Negative control 1 | integer certificate `5**5*7**7` changed to `5**6*7**7`, under `-O` | exit 1, "CHECK FAILED: integer certificate" |
| Negative control 2 | Theorem 5.1 upper bound `-0.00139052762357143` changed to `-0.00139052762357150`, under `-O` | exit 1, "CHECK FAILED: enclosure lies inside the interval stated in Theorem 5.1" |
| Numerics | `python -I -B verification/numerics.py` (numpy 2.3.5, scipy 1.17.0) | exit 0; byte-identical to `verification/numerics.json`; about 59 s |
| Figure | `python -I -B make_figure.py` in `verification/` (numpy 2.3.5, matplotlib 3.11.2) | exit 0; `qutrit_information.png` byte-identical |

Values confirmed: all_checks_passed true; tau_exact (sqrt(33)-1)/16; I(5/21) = -0.0290201758642584671...;
"2573571875 < 8707129344"; witness interval [-0.0013905276235714364018479043331292731364,
-0.0013905276235714364018479043331292731363] (outward, 40 digits); t* 0.112197392433428, I(t*) -0.0590859989390897.

After the replay only the title-page version/DOI line of the manuscript (and the rebuilt PDF), README and metadata
files were added or changed; the scripts and recorded outputs are byte-identical to the replayed candidate.

Cross-platform policy (also in CI, README.md and ENVIRONMENT.txt): verification.json byte for byte (blocking; identical
on GitHub's Linux runner). numerics.json in a non-blocking job: quoted Section 8 values within 1e-6, counts exactly; the
unquoted best values of other random-start searches only checked not to go below the family minimum (on Linux they land in
different local minima: -0.058633 and -0.001028 instead of -0.058742 and -0.001092; no quoted value is affected).
