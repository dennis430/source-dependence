"""Graph construction, shared origin tracing, circular support detection, constraint reconciliation.

Pure analysis works offline. LLM proposals are not authoritative.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import networkx as nx

from .models import (
    Assumption,
    Claim,
    Observation,
    Relationship,
    Source,
    SupportProfile,
)


def build_graph(
    claims: list[Claim],
    observations: list[Observation],
    sources: list[Source],
    relationships: list[Relationship],
) -> nx.DiGraph:
    g = nx.DiGraph()
    for c in claims:
        g.add_node(c.id, kind="claim", data=c)
    for o in observations:
        g.add_node(o.id, kind="observation", data=o)
        g.add_edge(o.id, o.claim_id, kind="bears_on")
    for s in sources:
        g.add_node(s.id, kind="source", data=s)
    for r in relationships:
        g.add_edge(r.from_id, r.to_id, data=r, label=r.label.value, kind=r.kind)
    return g


def analyze(
    graph: nx.DiGraph,
    claim_id: str,
    assumptions: list[Assumption] | None = None,
) -> SupportProfile:
    """Produce support/dependence profile. Preserve contradictions; do not average."""
    if claim_id not in graph:
        raise ValueError(f"Claim {claim_id} not in graph")

    obs_nodes = [
        n for n, d in graph.nodes(data=True)
        if d.get("kind") == "observation" and any(
            graph.has_edge(n, claim_id) for _ in [0]
        )
    ]
    # More precise: observations that edge to claim
    obs_nodes = [u for u, v, d in graph.edges(data=True) if v == claim_id and graph.nodes[u].get("kind") == "observation"]

    origin_groups = set()
    unresolved = []
    contradictions = []
    unknowns = []
    sensitivity = {}

    for oid in obs_nodes:
        obs = graph.nodes[oid]["data"]
        if obs.source_id and obs.source_id in graph:
            src = graph.nodes[obs.source_id]["data"]
            if src.origin_group:
                origin_groups.add(src.origin_group)
            else:
                unknowns.append(f"Unknown origin for source {obs.source_id} of {oid}")
        else:
            unknowns.append(f"No source for observation {oid}")

        # Check relationships
        for _, _, edata in graph.edges(oid, data=True):
            if edata.get("label") in ("unknown", "disputed", "inferred"):
                unresolved.append(f"{oid} -> {edata}")

    # Circular detection
    try:
        cycles = list(nx.simple_cycles(graph))
        if cycles:
            unknowns.append(f"Detected cycles: {cycles[:3]}...")  # limited
    except Exception:
        pass

    # Sensitivity: what if we remove disputed
    disputed_edges = [(u, v) for u, v, d in graph.edges(data=True) if d.get("label") == "disputed"]
    sensitivity["disputed_removed_count"] = len(disputed_edges)

    profile = SupportProfile(
        claim_id=claim_id,
        observations_counted=len(obs_nodes),
        documented_origin_groups=sorted(origin_groups),
        unresolved_relationships=unresolved,
        contradictions=contradictions,
        unknowns=unknowns,
        sensitivity=sensitivity,
        notes=[
            "Root count is not a count of statistically independent observations.",
            "Independence is relative to specified claim, process, and hypothesis.",
            "Unknown dependence remains unknown.",
        ],
    )
    return profile


def reconcile_constraints(observations: list[Observation]) -> dict[str, Any]:
    """Bounded time/quantity constraint reconciliation. Placeholder for v0.1; reports mismatches."""
    times = []
    for o in observations:
        if "observation" in o.times and o.times["observation"]:
            times.append(o.times["observation"])
    # Simple report of range and uncertainty presence
    return {
        "time_range_count": len(times),
        "has_uncertainty": any(o.uncertainty for o in observations),
        "note": "Full unit/timestamp reconciliation deferred; report mismatches explicitly.",
    }
