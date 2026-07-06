from __future__ import annotations

from typing import Any

from google.adk.agents.llm_agent import Agent

from utils.recommendation_engine import RecommendationEngine


def recommend_colleges(
    state: str | None = None,
    city: str | None = None,
    ownership: str | None = None,
    course_name: str | None = None,
    specialization: str | None = None,
    exam: str | None = None,
    category: str | None = None,
    max_total_fees: float | None = None,
    min_package: float | None = None,
    admission_rank: int | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Return ranked college recommendations from the structured dataset."""
    engine = RecommendationEngine()
    recommendations = engine.recommend_as_records(
        state=state,
        city=city,
        ownership=ownership,
        course_name=course_name,
        specialization=specialization,
        exam=exam,
        category=category,
        max_total_fees=max_total_fees,
        min_package=min_package,
        max_rank=admission_rank,
        limit=limit,
    )
    return {
        "analytics_backend": engine.backend,
        "count": len(recommendations),
        "recommendations": recommendations,
    }


recommendation_agent = Agent(
    model="gemini-2.5-flash",
    name="college_recommendation_agent",
    description="Ranks colleges using structured education datasets and student preferences.",
    instruction="""
        You are the MyWay AI college recommendation agent.

        Use the recommend_colleges tool whenever a student provides preferences
        such as budget, course, state, admission rank, ownership, cutoff category,
        or placement expectation. Explain results with practical tradeoffs:
        affordability, admission likelihood, institutional ranking, placements,
        location, and scholarship availability.

        If required preferences are missing, ask a focused follow-up question.
        Do not invent colleges or statistics that are not returned by the tool.
    """,
    tools=[recommend_colleges],
)
