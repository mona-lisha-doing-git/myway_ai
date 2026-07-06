from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from utils.recommendation_engine import RecommendationEngine


class RecommendationRequest(BaseModel):
    state: str | None = None
    city: str | None = None
    ownership: str | None = None
    course_name: str | None = None
    specialization: str | None = None
    exam: str | None = None
    category: str | None = None
    max_total_fees: float | None = Field(default=None, ge=0)
    min_package: float | None = Field(default=None, ge=0)
    admission_rank: int | None = Field(default=None, ge=1)
    limit: int = Field(default=10, ge=1, le=25)
    include_ai_explanation: bool = True

    def engine_filters(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "city": self.city,
            "ownership": self.ownership,
            "course_name": self.course_name,
            "specialization": self.specialization,
            "exam": self.exam,
            "category": self.category,
            "max_total_fees": self.max_total_fees,
            "min_package": self.min_package,
            "max_rank": self.admission_rank,
            "limit": self.limit,
        }

    def as_dict(self) -> dict[str, Any]:
        if hasattr(self, "model_dump"):
            return self.model_dump()
        return self.dict()


app = FastAPI(
    title="MyWay AI",
    description="AI-powered college decision intelligence APIs.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_engine() -> RecommendationEngine:
    return RecommendationEngine()


@app.get("/health")
def health() -> dict[str, str]:
    engine = get_engine()
    return {"status": "ok", "analytics_backend": engine.backend}


@app.get("/metadata")
def metadata() -> dict[str, Any]:
    return get_engine().metadata()


@app.post("/recommendations")
def recommendations(request: RecommendationRequest) -> dict[str, Any]:
    engine = get_engine()
    results = engine.recommend_as_records(**request.engine_filters())
    explanation = None
    if request.include_ai_explanation:
        explanation = generate_explanation(request, results)

    return {
        "preferences": request.as_dict(),
        "analytics_backend": engine.backend,
        "count": len(results),
        "recommendations": results,
        "explanation": explanation,
    }


def generate_explanation(
    request: RecommendationRequest,
    recommendations: list[dict[str, Any]],
) -> str:
    if not recommendations:
        return (
            "No colleges matched the current filters. Try increasing the budget, "
            "relaxing the rank filter, or broadening the state/course preference."
        )

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return _fallback_explanation(recommendations)

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        prompt = (
            "You are MyWay AI, a college decision intelligence assistant. "
            "Explain why these recommendations fit the student's preferences. "
            "Be concise, practical, and mention tradeoffs across fees, placements, "
            "rank, course fit, and institutional ranking.\n\n"
            f"Student preferences: {request.as_dict()}\n\n"
            f"Top recommendations: {recommendations[:5]}"
        )
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text or _fallback_explanation(recommendations)
    except Exception:
        return _fallback_explanation(recommendations)


def _fallback_explanation(recommendations: list[dict[str, Any]]) -> str:
    top = recommendations[0]
    return (
        f"{top['college_name']} is the strongest match because it balances "
        f"{top.get('specialization') or top.get('course_name')} availability, "
        f"NIRF rank {top.get('nirf_rank')}, average package "
        f"{top.get('average_package_lpa')} LPA, and total fees "
        f"{top.get('total_fees')}. Review the remaining options for better "
        "budget, location, or admission-rank comfort."
    )
