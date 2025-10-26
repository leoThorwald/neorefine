#!/usr/bin/env python3
"""
Train and save NeoTImmuML models
"""
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from joblib import dump
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
from scipy import sparse
import os

warnings.filterwarnings("ignore")

def main():
    print("="*70)
    print("NEOTIMMUML - TRAINING MODELS")
    print("="*70)

    # Load data
    print("\n[1/5] Loading data...")
    file_path = "../tumordb/tumoragdb_data.csv"
    data = pd.read_csv(file_path)
    X = data.iloc[:, 2:]
    y = data['immunogenicity']
    print(f"✓ Loaded {len(data):,} samples")

    # Encode categorical features using sparse matrices to save memory
    print("\n[2/5] Encoding features (sparse)...")
    # Use OneHotEncoder which creates sparse matrices directly, avoiding dense intermediate
    encoder = OneHotEncoder(sparse_output=True, handle_unknown='ignore')
    X_sparse = encoder.fit_transform(X.astype(str))
    print(f"✓ Encoded to {X_sparse.shape[1]:,} features (sparse format)")
    print(f"✓ Memory efficiency: {X_sparse.nnz / (X_sparse.shape[0] * X_sparse.shape[1]) * 100:.2f}% non-zero")
    X = X_sparse

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✓ Split: {X_train.shape[0]:,} train / {X_test.shape[0]:,} test")

    # Set random seed
    random_seed = 42

    print("\n[3/5] Training models...")

    # Model 1: Random Forest (now works with sparse matrices)
    print("  [1/3] Random Forest (100 trees)...", end=" ", flush=True)
    model_1 = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=4,
        random_state=random_seed,
        n_jobs=1  # Use 1 job to minimize memory usage
    )
    model_1.fit(X_train, y_train)
    print("✓")

    # Model 2: LightGBM
    print("  [2/3] LightGBM (100 trees)...", end=" ", flush=True)
    model_2 = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=7,
        num_leaves=31,
        min_child_samples=50,
        subsample=0.6,
        colsample_bytree=0.8,
        reg_lambda=0.01,
        random_state=random_seed,
        verbose=-1
    )
    model_2.fit(X_train, y_train)
    print("✓")

    # Model 3: XGBoost
    print("  [3/3] XGBoost (100 trees)...", end=" ", flush=True)
    model_3 = XGBClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        min_child_weight=3,
        subsample=0.6,
        colsample_bytree=1.0,
        gamma=0.1,
        reg_alpha=0.01,
        reg_lambda=0,
        random_state=random_seed,
        eval_metric='logloss',
        verbosity=0
    )
    model_3.fit(X_train, y_train)
    print("✓")

    # Create output directories
    print("\n[4/5] Creating output directories...")
    os.makedirs("output/RandomForest", exist_ok=True)
    os.makedirs("output/LightGBM", exist_ok=True)
    os.makedirs("output/XGBoost", exist_ok=True)
    print(f"  ✓ output/RandomForest/")
    print(f"  ✓ output/LightGBM/")
    print(f"  ✓ output/XGBoost/")

    # Save models and encoder
    print("\n[5/5] Saving models and encoder...")
    dump(model_1, 'output/RandomForest/model.joblib')
    print(f"  ✓ output/RandomForest/model.joblib")

    dump(model_2, 'output/LightGBM/model.joblib')
    print(f"  ✓ output/LightGBM/model.joblib")

    dump(model_3, 'output/XGBoost/model.joblib')
    print(f"  ✓ output/XGBoost/model.joblib")

    # Save encoder for production inference
    dump(encoder, 'output/encoder.joblib')
    print(f"  ✓ output/encoder.joblib (required for inference)")

    # Quick evaluation
    print("\n[6/6] Evaluating models on test set...")
    print("-"*70)

    for name, model in [("Random Forest", model_1), ("LightGBM", model_2), ("XGBoost", model_3)]:
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)
        f1 = f1_score(y_test, y_pred)

        print(f"{name:20s}: Acc={acc:.4f} | AUC={auc:.4f} | F1={f1:.4f}")

    print("\n" + "="*70)
    print("✓ ALL COMPLETE!")
    print(f"✓ Models saved in: {os.path.join(os.getcwd(), 'output')}")
    print(f"✓ Directory structure:")
    print(f"    output/")
    print(f"    ├── encoder.joblib (OneHotEncoder for inference)")
    print(f"    ├── RandomForest/")
    print(f"    │   └── model.joblib")
    print(f"    ├── LightGBM/")
    print(f"    │   └── model.joblib")
    print(f"    └── XGBoost/")
    print(f"        └── model.joblib")
    print("="*70)

if __name__ == "__main__":
    main()
