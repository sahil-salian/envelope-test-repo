"""Application screening model (logistic regression on synthetic data)."""
from functools import lru_cache
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parent.parent / "data" / "candidates.csv"
FEATURES = ["years_experience", "skills_match", "assessment_score", "employment_gap_years"]
PROTECTED = ["gender", "age_band"]  # recorded for fairness testing only; not model inputs


def load():
    return pd.read_csv(DATA)


@lru_cache(maxsize=1)
def train(seed: int = 7):
    df = load()
    X_train, X_test, y_train, y_test, g_train, g_test = train_test_split(
        df[FEATURES], df["hired"], df[PROTECTED], test_size=0.3, random_state=seed, stratify=df["hired"]
    )
    model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    return model, (X_train, y_train, g_train), (X_test, y_test, g_test)


def score_candidate(candidate: dict) -> float:
    model, _, _ = train()
    row = pd.DataFrame([{f: candidate[f] for f in FEATURES}])
    return float(model.predict_proba(row)[0, 1])
