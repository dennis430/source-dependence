# source-dependence

Source-dependence and evidential reconciliation methodology with reference implementation and portable bundle verifier.

This package provides:

- Structured models for claims, observations, sources, derivation relationships, assumptions, and acquisition metadata, aligned with W3C PROV concepts where useful.
- Local analysis that traces shared origins, circular support, unknown lineage, and constraint reconciliation. Outputs a support/dependence profile. Does not manufacture a universal truth score.
- Portable reconciliation bundles (experimental spec) with integrity verification that remains usable independently of the analytical engine.
- CLI and library for offline use. No accounts, no hosted upload service.

## Status

Experimental v0.1. Methodological validity and practical advantage gates are predeclared. See `LIMITATIONS.md`, `KILL_CRITERIA.md`, and `VALUE_CAPTURE.md`.

## Install

```bash
pip install source-dependence
```

(Once published; signed artifacts and checksums are also attached to GitHub releases.)

## Quick start

```bash
source-dependence analyze examples/duplicate.json
source-dependence verify-bundle examples/sample.bundle.json
```

See `examples/` and `docs/` for walkthroughs.

## What this does not do

- Does not claim a claim is true or assign calibrated real-world probabilities in v0.1 (probabilistic modules are isolated to synthetic fixtures with known generative processes).
- Successful bundle verification does not establish that lineage is independently authenticated or that a real-world claim is true.
- Not a substitute for qualified judgment.

License: MIT. Copyright 2026 Dennis Liu.
