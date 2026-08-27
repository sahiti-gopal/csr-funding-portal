"""Preprocessor stage — the first thing a question hits.

Does two things, matching the "Preprocessor (intent + entities)" box in the
target architecture:
  1. Extracts lightweight entities (region / financial year / status
     mentions) by matching against known schema values — no LLM.
  2. Checks the question against a small set of fixed regex rules; on a
     match it hands back a ready-to-run SQL template, letting the caller
     skip straight past the cache/confidence-scorer stages and the LLM
     entirely ("rule-based fast path (skips LLM)" in the diagram).
"""

import re
from dataclasses import dataclass, field


@dataclass
class FastPathRule:
    name: str
    patterns: list
    sql_template: str


FAST_PATH_RULES = [
    FastPathRule(
        name="highest_likelihood_donors",
        patterns=[
            r"highest likelihood",
            r"most likely donors?",
            r"top donors? by likelihood",
        ],
        sql_template=(
            "SELECT name, focus_area, likelihood, status FROM donors "
            "ORDER BY likelihood DESC LIMIT 10"
        ),
    ),
    FastPathRule(
        name="active_projects_by_region",
        patterns=[
            r"active projects.*by region",
            r"projects.*active.*region",
            r"region.*active projects",
        ],
        sql_template=(
            "SELECT region, COUNT(*) AS project_count FROM projects "
            "WHERE status = 'Active' GROUP BY region ORDER BY project_count DESC"
        ),
    ),
    FastPathRule(
        name="low_fund_utilization",
        patterns=[
            r"low (fund )?utili[sz]ation",
            r"under.?utili[sz]ed",
            r"least utili[sz]ed",
        ],
        sql_template=(
            "SELECT project_name, region, budget, utilized_amount, "
            "ROUND(utilized_amount / budget * 100, 1) AS utilization_pct "
            "FROM projects WHERE budget > 0 ORDER BY utilization_pct ASC LIMIT 20"
        ),
    ),
    FastPathRule(
        name="donor_most_projects",
        patterns=[
            r"donor.*funded.*most projects",
            r"which donor.*most projects",
            r"top donor by project count",
        ],
        sql_template=(
            "SELECT d.name, COUNT(p.id) AS project_count FROM donors d "
            "JOIN projects p ON p.donor_id = d.id "
            "GROUP BY d.id, d.name ORDER BY project_count DESC LIMIT 5"
        ),
    ),
]

_KNOWN_REGIONS = ["South", "West", "North", "East"]
_KNOWN_STATUSES = ["Active", "Planning", "Completed", "On Hold", "Cancelled", "Delayed"]
_FY_PATTERN = re.compile(r"\b(20\d{2})[-/]?(\d{2})?\b")


@dataclass
class PreprocessedQuestion:
    normalized: str
    entities: dict = field(default_factory=dict)
    fast_path_rule: FastPathRule | None = None


def normalize_question(question: str) -> str:
    return " ".join(question.strip().lower().split())[:500]


def extract_entities(normalized_question: str) -> dict:
    entities = {}

    regions = [r for r in _KNOWN_REGIONS if r.lower() in normalized_question]
    if regions:
        entities["regions"] = regions

    statuses = [s for s in _KNOWN_STATUSES if s.lower() in normalized_question]
    if statuses:
        entities["statuses"] = statuses

    fy_match = _FY_PATTERN.search(normalized_question)
    if fy_match:
        entities["financial_year_hint"] = fy_match.group(0)

    return entities


def match_fast_path(normalized_question: str) -> FastPathRule | None:
    for rule in FAST_PATH_RULES:
        for pattern in rule.patterns:
            if re.search(pattern, normalized_question, re.IGNORECASE):
                return rule
    return None


def preprocess(question: str) -> PreprocessedQuestion:
    normalized = normalize_question(question)
    return PreprocessedQuestion(
        normalized=normalized,
        entities=extract_entities(normalized),
        fast_path_rule=match_fast_path(normalized),
    )
