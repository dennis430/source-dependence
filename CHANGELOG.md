# Changelog

## 0.1.1 - 2026-10-24 (corrective)

- Removed false analysis_reproducible success assertion (R04). Status is now NOT_RUN until explicit re-execution.
- Explicit Click command names (analyze, verify-bundle) and non-zero exit on verification failure.
- Replaced echo-only daily workflow with controller that performs integrity check and persists state/ledger.
- Archive collector implemented with offline fixtures and PAUSED_ACCESS reporting; workflow invokes it.
- Findings ledger added at docs/review/findings.md.

Original 0.1.0 release remains the first public snapshot. These changes are prospective repairs, not backdated observations.

## 0.1.0 - 2026-10-23

- Initial experimental release (scaffolding).
