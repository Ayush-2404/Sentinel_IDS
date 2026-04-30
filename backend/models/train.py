"""
One-time training script for UNSW-NB15 dataset.
Run from backend/ directory with venv activated:
    python -m models.train
"""

import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ── Paths ────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(__file__)
TRAIN_PATH = os.path.join(BASE_DIR, "UNSW_NB15_training-set.csv")
TEST_PATH  = os.path.join(BASE_DIR, "UNSW_NB15_testing-set.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
META_PATH  = os.path.join(BASE_DIR, "model_meta.pkl")

# ── UNSW-NB15 has 49 columns. We use these 10 for demo ──────
# These are the most impactful and easy to extract at runtime
FEATURES = [
    "proto",        # protocol (tcp/udp/etc) — categorical
    "service",      # service (http/ftp/etc)  — categorical
    "state",        # connection state        — categorical
    "dur",          # connection duration
    "sbytes",       # source bytes
    "dbytes",       # destination bytes
    "sttl",         # source time to live
    "dttl",         # destination time to live
    "sloss",        # source packets lost
    "dloss",        # destination packets lost
]
LABEL_COL = "label"   # 0 = normal, 1 = attack (already binary in UNSW-NB15)

def load_and_prepare(path: str, encoders: dict = None, fit: bool = True):
    print(f"[Train] Loading {os.path.basename(path)}...")
    df = pd.read_csv(path)

    # Keep only our selected features + label
    df = df[FEATURES + [LABEL_COL]].copy()

    # Drop rows with nulls
    df.dropna(inplace=True)

    # Encode categorical columns
    cat_cols = ["proto", "service", "state"]
    if fit:
        encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    else:
        for col in cat_cols:
            le = encoders[col]
            # Handle unseen labels gracefully
            df[col] = df[col].astype(str).apply(
                lambda x: le.transform([x])[0] if x in le.classes_ else -1
            )

    X = df[FEATURES]
    y = df[LABEL_COL]
    return X, y, encoders


def main():
    # Load training data
    X_train, y_train, encoders = load_and_prepare(TRAIN_PATH, fit=True)

    # Load test data using same encoders
    X_test, y_test, _ = load_and_prepare(TEST_PATH, encoders=encoders, fit=False)

    print(f"[Train] Training set: {len(X_train)} samples")
    print(f"[Train] Test set:     {len(X_test)} samples")
    print(f"[Train] Attack ratio in training: {y_train.mean():.1%}")

    # Train
    print("[Train] Training Random Forest (this takes ~1-2 mins)...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1,       # use all CPU cores
        class_weight="balanced"  # handles class imbalance
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("\n[Train] === Results ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Attack"]))

    # Save model + encoders together
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(META_PATH, "wb") as f:
        pickle.dump({"encoders": encoders, "features": FEATURES}, f)

    print(f"[Train] Saved model  → {MODEL_PATH}")
    print(f"[Train] Saved meta   → {META_PATH}")


if __name__ == "__main__":
    main()