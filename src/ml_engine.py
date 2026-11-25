import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

FEATURE_COLS = [
    "Cart_Value",
    "Items_In_Cart",
    "Discount_Pct",
    "Is_Festival_Season",
    "Past_Orders",
    "Time_On_Site_Mins"
]

def train_and_evaluate_models(sessions_df: pd.DataFrame, save_model: bool = True):
    """
    Trains a Random Forest Classifier (100 trees) and a Logistic Regression baseline
    on 80% of the data, evaluates on the unseen 20%, and saves the trained model.
    """
    X = sessions_df[FEATURE_COLS]
    y = sessions_df["Bundle_Accepted"]

    # 80% Training Data, 20% Unseen Testing Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 1. Baseline Model: Logistic Regression (for comparison in presentation)
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)

    # 2. Primary AI Model: Random Forest Classifier
    rf_model = RandomForestClassifier(
        n_estimators=100,   # 100 independent decision trees
        max_depth=8,        # Prevents overfitting / memorization
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)

    # Save trained model to disk
    if save_model:
        os.makedirs("models", exist_ok=True)
        joblib.dump(rf_model, "models/random_forest_bundle.pkl")

    # Benchmark Comparison Table
    metrics_df = pd.DataFrame({
        "Model": ["Logistic Regression (Baseline)", "Random Forest (Proposed AI)"],
        "Accuracy": [accuracy_score(y_test, lr_preds), accuracy_score(y_test, rf_preds)],
        "Precision": [precision_score(y_test, lr_preds), precision_score(y_test, rf_preds)],
        "Recall": [recall_score(y_test, lr_preds), recall_score(y_test, rf_preds)],
        "F1-Score": [f1_score(y_test, lr_preds), f1_score(y_test, rf_preds)]
    }).round(4)

    # Explainable AI: Feature Importance
    importance_df = pd.DataFrame({
        "Feature": FEATURE_COLS,
        "Importance": rf_model.feature_importances_
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

    cm = confusion_matrix(y_test, rf_preds)

    return rf_model, metrics_df, importance_df, cm