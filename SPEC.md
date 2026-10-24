# Experimental Specification Notes

## Data model

See `src/source_dependence/models.py`. Aligns with PROV-DM Entity (observations/claims), Activity (derivations), Agent (sources) without incompatible duplicates. Relationships labeled documented/declared/inferred/disputed/unknown/synthetic_ground_truth.

## Bundle format `reconciliation.bundle.v1`

JSON object with version, manifest (inputs), assumptions, analytical_version, report, integrity (content_sha256 of canonical form excluding integrity field, plus optional signature/timestamp under explicit policy).

Canonicalization: sorted keys, compact separators, UTF-8.

Verification reports separately:
- bytes match commitment
- signature under selected trust policy
- timestamp/transparency under documented assumptions
- analysis reproducible from available inputs and version
- lineage independently established (always false unless separate evidence)

## Analysis

`analyze()` returns SupportProfile. observations_counted is raw count. documented_origin_groups listed. Unknowns and unresolved preserved. Notes explicitly state root count ≠ independent observations.
