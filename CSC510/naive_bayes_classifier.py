import argparse
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import accuracy_score, classification_report


# Sample categorical dataset.
# Target: whether a person will play tennis under given weather conditions.
DATA = [
    {"outlook": "sunny",    "temperature": "hot",  "humidity": "high",   "windy": "false", "play": "no"},
    {"outlook": "sunny",    "temperature": "hot",  "humidity": "high",   "windy": "true",  "play": "no"},
    {"outlook": "overcast", "temperature": "hot",  "humidity": "high",   "windy": "false", "play": "yes"},
    {"outlook": "rainy",    "temperature": "mild", "humidity": "high",   "windy": "false", "play": "yes"},
    {"outlook": "rainy",    "temperature": "cool", "humidity": "normal", "windy": "false", "play": "yes"},
    {"outlook": "rainy",    "temperature": "cool", "humidity": "normal", "windy": "true",  "play": "no"},
    {"outlook": "overcast", "temperature": "cool", "humidity": "normal", "windy": "true",  "play": "yes"},
    {"outlook": "sunny",    "temperature": "mild", "humidity": "high",   "windy": "false", "play": "no"},
    {"outlook": "sunny",    "temperature": "cool", "humidity": "normal", "windy": "false", "play": "yes"},
    {"outlook": "rainy",    "temperature": "mild", "humidity": "normal", "windy": "false", "play": "yes"},
    {"outlook": "sunny",    "temperature": "mild", "humidity": "normal", "windy": "true",  "play": "yes"},
    {"outlook": "overcast", "temperature": "mild", "humidity": "high",   "windy": "true",  "play": "yes"},
    {"outlook": "overcast", "temperature": "hot",  "humidity": "normal", "windy": "false", "play": "yes"},
    {"outlook": "rainy",    "temperature": "mild", "humidity": "high",   "windy": "true",  "play": "no"},
]

FEATURES = ["outlook", "temperature", "humidity", "windy"]
TARGET = "play"


def build_dataframe() -> pd.DataFrame:
    return pd.DataFrame(DATA)


def print_frequency_tables(df: pd.DataFrame) -> None:
    print("\n=== DATASET ===")
    print(df.to_string(index=False))

    print("\n=== FREQUENCY TABLES ===")
    for feature in FEATURES:
        table = pd.crosstab(df[feature], df[TARGET], margins=True)
        print(f"\nFrequency table for '{feature}':")
        print(table)


def print_likelihood_tables(df: pd.DataFrame, alpha: float = 1.0) -> None:
    print("\n=== LIKELIHOOD TABLES WITH LAPLACE SMOOTHING ===")
    classes = sorted(df[TARGET].unique())

    for feature in FEATURES:
        feature_values = sorted(df[feature].unique())
        print(f"\nLikelihoods for feature '{feature}' (alpha={alpha}):")
        rows = []
        for value in feature_values:
            row = {"value": value}
            for cls in classes:
                numerator = len(df[(df[feature] == value) & (df[TARGET] == cls)]) + alpha
                denominator = len(df[df[TARGET] == cls]) + alpha * len(feature_values)
                row[f"P({TARGET}={cls})"] = round(numerator / denominator, 4)
            rows.append(row)
        print(pd.DataFrame(rows).to_string(index=False))


def posterior_for_input(df: pd.DataFrame, sample: Dict[str, str], alpha: float = 1.0) -> Dict[str, float]:
    classes = sorted(df[TARGET].unique())
    total_rows = len(df)
    posteriors = {}

    for cls in classes:
        prior = len(df[df[TARGET] == cls]) / total_rows
        likelihood_product = 1.0

        for feature in FEATURES:
            feature_values = sorted(df[feature].unique())
            numerator = len(df[(df[feature] == sample[feature]) & (df[TARGET] == cls)]) + alpha
            denominator = len(df[df[TARGET] == cls]) + alpha * len(feature_values)
            likelihood_product *= numerator / denominator

        posteriors[cls] = prior * likelihood_product

    total = sum(posteriors.values())
    normalized = {cls: prob / total for cls, prob in posteriors.items()}
    return normalized


def train_sklearn_model(df: pd.DataFrame) -> tuple[CategoricalNB, OrdinalEncoder, List[str]]:
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )

    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    X_train_enc = encoder.fit_transform(X_train)
    X_test_enc = encoder.transform(X_test)

    # CategoricalNB expects non-negative integers.
    # This dataset's test set should use known categories, but we guard anyway.
    if (X_train_enc < 0).any() or (X_test_enc < 0).any():
        raise ValueError("Unknown category found after encoding. Use categories seen during training.")

    eval_model = CategoricalNB(alpha=1.0)
    eval_model.fit(X_train_enc, y_train)

    y_pred = eval_model.predict(X_test_enc)
    print("\n=== SCIKIT-LEARN MODEL CHECK ===")
    print(f"Accuracy on held-out test split: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Refit on the full dataset so the final prediction uses all available observations.
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    X_full_enc = encoder.fit_transform(X)
    model = CategoricalNB(alpha=1.0)
    model.fit(X_full_enc, y)

    return model, encoder, list(model.classes_)


def predict_sample(model: CategoricalNB, encoder: OrdinalEncoder, sample: Dict[str, str], class_labels: List[str]) -> None:
    sample_df = pd.DataFrame([sample])
    encoded = encoder.transform(sample_df)

    if (encoded < 0).any():
        raise ValueError(
            "Prediction contains a category not seen in training. "
            "Please use one of the values shown in the dataset."
        )

    probabilities = model.predict_proba(encoded)[0]
    predicted = model.predict(encoded)[0]

    print("\n=== SCIKIT-LEARN PREDICTION ===")
    print("Input sample:")
    print(sample)
    print("Predicted class:", predicted)
    print("Predicted probabilities:")
    for label, prob in zip(class_labels, probabilities):
        print(f"  P({TARGET}={label} | input) = {prob:.4f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Naive Bayes classifier demo using scikit-learn CategoricalNB."
    )
    parser.add_argument("--outlook", default="sunny", choices=["sunny", "overcast", "rainy"])
    parser.add_argument("--temperature", default="cool", choices=["hot", "mild", "cool"])
    parser.add_argument("--humidity", default="high", choices=["high", "normal"])
    parser.add_argument("--windy", default="true", choices=["true", "false"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = build_dataframe()

    sample = {
        "outlook": args.outlook,
        "temperature": args.temperature,
        "humidity": args.humidity,
        "windy": args.windy,
    }

    print_frequency_tables(df)
    print_likelihood_tables(df, alpha=1.0)

    manual_posteriors = posterior_for_input(df, sample, alpha=1.0)
    print("\n=== MANUAL POSTERIOR CALCULATION (NORMALIZED) ===")
    for cls, prob in manual_posteriors.items():
        print(f"P({TARGET}={cls} | input) = {prob:.4f}")

    model, encoder, class_labels = train_sklearn_model(df)
    predict_sample(model, encoder, sample, class_labels)


if __name__ == "__main__":
    main()
