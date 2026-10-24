# Review Findings Disposition

Reviewed baseline: source-dependence @ 295232f5..., model-evidence-archive @ 84b7a68b...

## R04 (critical) - Fixed
- Finding: analysis_reproducible set from hash match.
- Fix: explicit NOT_RUN until re-execution. Envelope consistency reported separately.
- Commit: c5ec4e25bc4ed0007a75dfd1d19620153b6cd018
- Verification: import verify_bundle; assert result['analysis_reproducible'] == 'NOT_RUN'

## R01, R02 - Addressed
- Daily and collect workflows now invoke real controller/collector code that persists state or reports PAUSED_ACCESS.
- Commits: 2b6b8428..., 2646fe55...

## R13 - Fixed
- Explicit name= on Click commands.
- Commit: 9582dd8f...

## R03 - Diagnosed as incomplete runner start (logs 404, runner 0). New workflows include setup-python and real scripts; re-dispatch required for fresh evidence.

## Remaining open (implementation depth)
- R07-R11: graph MultiDiGraph, relationship tracing, sensitivity re-execution, constraint reconciliation, expanded tests, baselines, public examples still require further commits. Current analysis remains conservative profile only.
- R12: GitHub release with wheel/sdist to be created after packaging check.
- R14: Gate controller skeleton in daily_controller; full Day-3/7/30/90 enforcement and injectable clock tests pending.

Original publication dates preserved. Functional deployment date is the first successful controller run after these fixes.
