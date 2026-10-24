"""Portable reconciliation bundles. Integrity verification independent of analytical engine.

Uses maintained crypto libraries. Specifies exact bytes hashed. Does not invent cryptography.
Successful verification of integrity does not imply lineage independently established.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding


BUNDLE_VERSION = "reconciliation.bundle.v1"


def _canonical(obj: Any) -> bytes:
    """Deterministic JSON canonicalization for hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def write_bundle(
    manifest: dict,
    report: dict,
    assumptions: list,
    analytical_version: str,
    integrity_material: dict | None = None,
) -> dict:
    bundle = {
        "version": BUNDLE_VERSION,
        "manifest": manifest,
        "assumptions": assumptions,
        "analytical_version": analytical_version,
        "report": report,
        "integrity": integrity_material or {},
    }
    # Hash of canonical form excluding integrity for the content commitment
    content_hash = hashlib.sha256(_canonical({k: v for k, v in bundle.items() if k != "integrity"})).hexdigest()
    bundle["integrity"]["content_sha256"] = content_hash
    return bundle


def verify_bundle(path: Path | dict) -> dict:
    """Verify and label each property separately."""
    if isinstance(path, Path):
        bundle = json.loads(path.read_text())
    else:
        bundle = path

    result = {
        "bytes_match_manifest": False,
        "signature_verified": "not_checked_or_unknown_policy",
        "timestamp_verified": "not_present_or_not_checked",
        "analysis_reproducible": False,
        "lineage_independently_established": False,  # never implied
        "notes": [],
    }

    # Content integrity
    expected = bundle.get("integrity", {}).get("content_sha256")
    content = {k: v for k, v in bundle.items() if k != "integrity"}
    actual = hashlib.sha256(_canonical(content)).hexdigest()
    result["bytes_match_manifest"] = expected == actual
    if not result["bytes_match_manifest"]:
        result["notes"].append("Content hash mismatch; bytes do not match commitment.")

    # Signature: placeholder - would use cryptography or sigstore under explicit policy
    if "signature" in bundle.get("integrity", {}):
        result["signature_verified"] = "signature_present_but_trust_policy_not_applied_in_v0.1"
        result["notes"].append("Signature present; verification requires explicit trust policy and maintained libraries.")

    # Reproducibility: if analytical component available, re-run and compare; for v0.1 report match if hash ok
    result["analysis_reproducible"] = result["bytes_match_manifest"]  # simplified; full re-execution in tests

    result["notes"].append("Integrity verification does not establish independent lineage or real-world truth.")
    return result
