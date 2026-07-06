import os

from utils.recommendation_engine import RecommendationEngine

if not os.getenv("BIGQUERY_DATASET"):
    raise SystemExit(
        "Set BIGQUERY_DATASET and GOOGLE_CLOUD_PROJECT or BIGQUERY_PROJECT_ID "
        "before running the BigQuery recommendation smoke test."
    )

engine = RecommendationEngine()

recommendations = engine.recommend(
    state="Maharashtra",
    ownership="Government",
    course_name="B.Tech",
    specialization="Computer Science",
    max_total_fees=10000000,
    min_package=10,
    max_rank=5000,
    limit=5,
)

assert not recommendations.empty
assert "recommendation_score" in recommendations.columns

print(recommendations)
