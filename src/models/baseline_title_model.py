import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot  as plt
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def run_baseline() -> LogisticRegression:
    df = pd.read_csv("ryukahr_videos.csv")

    FEATURE_COLUMNS = [
        "publish_hour",
        "publish_weekday",
        "duration_seconds",
    ]

    X = df[["title"] + FEATURE_COLUMNS]
    y = df["successful"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("title", TfidfVectorizer(max_features=3000, stop_words="english"), "title"),
            ("num", StandardScaler(), FEATURE_COLUMNS)
        ]
    )

    model = LogisticRegression(max_iter=1000, class_weight="balanced")

    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", model),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
    plt.title("Baseline Title Model Confusion Matrix")
    plt.show()

    return model

if __name__ == "__main__":
    run_baseline()