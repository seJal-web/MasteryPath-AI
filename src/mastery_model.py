import numpy as np
from sklearn.linear_model import LogisticRegression


def train_mastery_model():
    X = np.array([
        [30, 1, 5], [40, 2, 4], [50, 2, 4], [55, 3, 3],
        [60, 2, 3], [65, 2, 2], [70, 1, 2], [75, 2, 1],
        [80, 1, 1], [85, 1, 0], [90, 1, 0], [95, 1, 0]
    ])

    y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

    model = LogisticRegression()
    model.fit(X, y)
    return model


def predict_mastery(score, attempts, weak_topics):
    model = train_mastery_model()

    features = np.array([[score, attempts, weak_topics]])
    probability = model.predict_proba(features)[0][1]

    mastery_percentage = round(probability * 100, 2)

    if mastery_percentage >= 80:
        level = "Mastered"
    elif mastery_percentage >= 60:
        level = "Good"
    elif mastery_percentage >= 40:
        level = "Needs Practice"
    else:
        level = "Weak"

    return mastery_percentage, level
