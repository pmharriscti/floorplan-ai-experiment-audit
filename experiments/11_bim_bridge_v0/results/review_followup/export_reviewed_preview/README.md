# Reviewed-preview export (2026-10-01)

Copies of the checks and records of the reviewed-preview IFC. The IFC itself is not committed; its path and SHA-256 are in `../../../provenance.json`.

`review_verification.json` is the first verification run. Its junction-contact rows are wrong: the verifier computed wall footprints from the wall start point instead of the body. All its other checks were unaffected. `review_verification_02.json` replaces it, computes footprints from the tessellated bodies, and is the result reported in the entry README.
