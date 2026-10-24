# Review Findings Disposition (updated)

Baseline after corrective: source-dependence @ 9ead1c22..., model-evidence-archive @ 2646fe55...

## Accepted prior fixes (preserved)
- R04: analysis_reproducible = NOT_RUN. Commit c5ec4e25.
- R13: explicit command names. Commit 9582dd8f.
- Partial R06: nonzero exit on envelope mismatch.

## R01 - PARTIAL
- Controller now loads prior state and preserves terminal statuses (FROZEN_* etc.). Fails closed if pyproject.toml missing.
- Still no full Day-3/7/30/90 machine, no artifact download/restore across runs, no budget reservation.
- Commit 8165ea49.

## R02 - PARTIAL
- OpenAIAdapter with injectable Transport and MockTransport added. Offline tests prove request construction, response parsing, hash of actual bytes, is_historical flag.
- Live workflow still dry-run; no secret wiring; no persistence of real records yet.
- Commit f930034e / cf62c882.

## R07-R11 - Partial progress
- Graph switched to MultiDiGraph; duplicate IDs rejected; multi-edges preserved; SCC-based cycle detection; order-invariant test added.
- Full sensitivity re-run, constraint reconciliation, baselines, public examples still incomplete.
- Commit 3d535ad8 / 8cac7823.

## R03 - Unresolved
- Runs 40060747386 and 40060747765 failed with runner ID 0, no steps. Cause not established from available metadata. New changes not yet re-dispatched.

## R12 - Open
- No GitHub Release created. Independent of PyPI.

R14 remains open for full gate enforcement.
