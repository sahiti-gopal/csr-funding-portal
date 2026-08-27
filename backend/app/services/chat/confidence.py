"""Confidence scorer — takes the preprocessor's (question, entities) output
plus the cache-check result and decides which path the pipeline takes:
fast_path (highest confidence, no LLM), cache (high confidence, no LLM),
or llm (fall through to the SQL generator).

Entities feed into the score itself, not just the routing: a question with
recognized region/status/financial-year entities is less ambiguous for the
SQL generator than a bare-bones one, so a higher entity_confidence is passed
through and surfaced in the audit trail / response meta, and the entities
themselves are forwarded to the SQL generator's prompt as hints.
"""

from dataclasses import dataclass, field

# How much each recognized entity type is worth toward entity_confidence,
# capped at 1.0. Fast path is always 1.0 (a fixed template, no ambiguity to
# resolve); cache reuses whatever confidence produced the cached SQL originally
# isn't recomputed here — a cache hit is scored on its own entity match instead.
_ENTITY_WEIGHT = 0.3
_BASE_CONFIDENCE = 0.3


@dataclass
class RoutingDecision:
    source: str  # "fast_path" | "cache" | "llm"
    sql: str | None  # pre-resolved SQL for fast_path/cache; None for llm
    entity_confidence: float = 0.0
    entities: dict = field(default_factory=dict)


def score_entities(entities: dict) -> float:
    """More recognized entities => less ambiguity => higher confidence that
    the SQL generator has enough to work with without guessing."""
    if not entities:
        return _BASE_CONFIDENCE
    return min(1.0, _BASE_CONFIDENCE + _ENTITY_WEIGHT * len(entities))


def decide_route(preprocessed, cached_sql: str | None) -> RoutingDecision:
    if preprocessed.fast_path_rule is not None:
        return RoutingDecision(
            source="fast_path",
            sql=preprocessed.fast_path_rule.sql_template,
            entity_confidence=1.0,
            entities=preprocessed.entities,
        )

    if cached_sql is not None:
        return RoutingDecision(
            source="cache",
            sql=cached_sql,
            entity_confidence=score_entities(preprocessed.entities),
            entities=preprocessed.entities,
        )

    return RoutingDecision(
        source="llm",
        sql=None,
        entity_confidence=score_entities(preprocessed.entities),
        entities=preprocessed.entities,
    )
