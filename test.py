from utils.recommendation_engine import RecommendationEngine

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
