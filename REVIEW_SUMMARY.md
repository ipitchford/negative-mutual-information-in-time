# Review summary (internal, AI-assisted)

This candidate was checked inside Evidence Press before release. The checks were internal and AI-assisted: five
reviewer roles (editor, methodology, domain, perspective, devil's advocate), an adversarial review by a second AI
model, clean replays of every script, one revision round with extensions, a re-review of the changes, a proof audit
of the new proofs and a second-model audit of the new proofs. This is not peer review, independent reproduction or
formal verification. No reviewer found a mathematical error in the original claims.

## Main objections and how they were handled

| Objection | Disposition |
|---|---|
| A sentence saying real qutrit-to-qubit searches found no violation was false, and the minimal output dimension was answerable | Extension: exact rational qutrit-to-qubit witness (Theorem 5.1) with a certified interval; Corollary 5.2 shows input 3, output 2 and rank 2 are all minimal and attained at once; the false sentence was removed |
| No mechanism; the support comparison was only observational | Extension: block lemma (Lemma 2.1), no-cross-coherence proposition (Proposition 2.2), Corollary 3.3 (rank-two violations need cross-coherence); Proposition 7.1 now proved from them |
| Wu-Parzygnat-Vedral-Fullwood (New J. Phys. 2025) omitted; terminology drift | Cited; the quantity is named "mutual information in time" and identified with the dynamical mutual information |
| Fullwood-Yang's request for a simple, physically motivated example not mentioned | Quoted in the introduction; the erasure family is framed as an answer |
| Introduction hard to read for non-specialists | New introduction (question, what was known, what is new, roadmap); each section opens with a purpose sentence |
| Consequences unstated | Section 8 "Consequences" |
| Why random sampling missed violations | Section 8 paragraph with reproducible numerics (4000 random rank-two qutrit processes, none negative) |
| Pure-input padding implicit; basis independence of the Jamiolkowski matrix | Proof of Proposition 3.2 written out; basis independence stated in Section 2 |
| Minimality depends on a preprint | Stated in Corollary 4.2 and the introduction |
| Second-derivative derivation missing | Added to the proof of Theorem 4.3; the verifier checks the formula at six points to 40 digits |
| Interior perturbation bound loose | Tightened with derivation (Proposition 6.1) |
| Figure axis, units and range | Regenerated over [0, 1] in nats with t*, tau and 5/21 marked |
| Omega citation lacked a release identifier | Release 8f61e708e239, preregistration issue #14994 and access date added |
| Tensor powers and the global qutrit minimum | Reported as numerical observations and open questions only; no theorem claimed |
| The original verifier relied on `assert` and passed under `python -O` even when corrupted | Replaced by `verification/verify_qutrit.py` with explicit checks; negative controls fail under `-O` |
