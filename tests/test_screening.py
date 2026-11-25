from app.screening import score_candidate


def test_score_is_probability():
    s = score_candidate({"years_experience": 5, "skills_match": 0.7, "assessment_score": 70, "employment_gap_years": 0})
    assert 0.0 <= s <= 1.0
