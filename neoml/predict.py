#!/usr/bin/env python3
"""
NeoTImmuML Inference Script
===========================
Uses trained models to predict neoantigen immunogenicity.

Requirements:
- output/encoder.joblib (feature encoder)
- output/LightGBM/model.joblib (or XGBoost/RandomForest)
- Input data with same 46 features as training data

Usage:
    python predict.py <input_csv> [--model lightgbm|xgboost|randomforest]
"""

import pandas as pd
import numpy as np
from joblib import load
import argparse
import sys
from pathlib import Path


def load_model_and_encoder(model_type='lightgbm'):
    """
    Load the feature encoder and trained model.

    Args:
        model_type: One of 'lightgbm', 'xgboost', or 'randomforest'

    Returns:
        encoder, model
    """
    base_path = Path(__file__).parent / 'output'

    # Load encoder (required for all models)
    encoder_path = base_path / 'encoder.joblib'
    if not encoder_path.exists():
        raise FileNotFoundError(f"Encoder not found: {encoder_path}")

    encoder = load(encoder_path)
    print(f"✓ Loaded encoder from {encoder_path}")

    # Load model
    model_map = {
        'lightgbm': 'LightGBM',
        'xgboost': 'XGBoost',
        'randomforest': 'RandomForest'
    }

    if model_type not in model_map:
        raise ValueError(f"Invalid model type: {model_type}")

    model_path = base_path / model_map[model_type] / 'model.joblib'
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    model = load(model_path)
    print(f"✓ Loaded {model_type.upper()} model from {model_path}")

    return encoder, model


def predict_immunogenicity(data, encoder, model):
    """
    Predict immunogenicity for neoantigen samples.

    Args:
        data: DataFrame with neoantigen features (same columns as training)
        encoder: Fitted OneHotEncoder
        model: Trained classification model

    Returns:
        DataFrame with predictions and probabilities
    """
    # Encode features to sparse matrix (262k features)
    print(f"\nEncoding {len(data):,} samples...")
    X_encoded = encoder.transform(data.astype(str))
    print(f"✓ Encoded to {X_encoded.shape[1]:,} features (sparse format)")
    print(f"  Memory efficiency: {X_encoded.nnz / (X_encoded.shape[0] * X_encoded.shape[1]) * 100:.2f}% non-zero")

    # Make predictions
    print("\nMaking predictions...")
    predictions = model.predict(X_encoded)
    probabilities = model.predict_proba(X_encoded)

    # Create results DataFrame
    results = pd.DataFrame({
        'prediction': predictions,
        'prob_negative': probabilities[:, 0],
        'prob_positive': probabilities[:, 1],
        'confidence': np.max(probabilities, axis=1)
    })

    # Add original data
    results = pd.concat([data.reset_index(drop=True), results], axis=1)

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Predict neoantigen immunogenicity using trained models'
    )
    parser.add_argument(
        'input_file',
        help='Path to CSV file with neoantigen features'
    )
    parser.add_argument(
        '--model',
        choices=['lightgbm', 'xgboost', 'randomforest'],
        default='lightgbm',
        help='Model to use for predictions (default: lightgbm)'
    )
    parser.add_argument(
        '--output',
        help='Output CSV file for predictions (default: predictions.csv)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.5,
        help='Probability threshold for positive class (default: 0.5)'
    )

    args = parser.parse_args()

    # Load data
    print(f"\n{'='*60}")
    print(f"NeoTImmuML Inference")
    print(f"{'='*60}")
    print(f"\nLoading data from: {args.input_file}")

    try:
        data = pd.read_csv(args.input_file)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    print(f"✓ Loaded {len(data):,} samples with {len(data.columns)} columns")

    # Load model and encoder
    try:
        encoder, model = load_model_and_encoder(args.model)
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    # Make predictions
    try:
        results = predict_immunogenicity(data, encoder, model)
    except Exception as e:
        print(f"Error during prediction: {e}")
        sys.exit(1)

    # Summary statistics
    print(f"\n{'='*60}")
    print("Prediction Summary")
    print(f"{'='*60}")

    num_positive = (results['prediction'] == 1).sum()
    num_negative = (results['prediction'] == 0).sum()

    print(f"\nTotal samples:      {len(results):,}")
    print(f"Predicted positive: {num_positive:,} ({num_positive/len(results)*100:.1f}%)")
    print(f"Predicted negative: {num_negative:,} ({num_negative/len(results)*100:.1f}%)")
    print(f"\nAverage confidence: {results['confidence'].mean():.3f}")
    print(f"Min confidence:     {results['confidence'].min():.3f}")
    print(f"Max confidence:     {results['confidence'].max():.3f}")

    # High confidence predictions
    high_conf_positive = ((results['prediction'] == 1) & (results['confidence'] >= 0.9)).sum()
    high_conf_negative = ((results['prediction'] == 0) & (results['confidence'] >= 0.9)).sum()

    print(f"\nHigh confidence (≥0.9):")
    print(f"  Positive: {high_conf_positive:,} ({high_conf_positive/len(results)*100:.1f}%)")
    print(f"  Negative: {high_conf_negative:,} ({high_conf_negative/len(results)*100:.1f}%)")

    # Save results
    output_file = args.output or 'predictions.csv'
    results.to_csv(output_file, index=False)
    print(f"\n✓ Saved predictions to: {output_file}")

    # Display sample predictions
    print(f"\n{'='*60}")
    print("Sample Predictions (first 10 rows)")
    print(f"{'='*60}")

    display_cols = ['prediction', 'prob_positive', 'confidence']
    if len(results.columns) > 10:
        # If too many columns, just show key prediction columns
        print(results[display_cols].head(10).to_string(index=True))
    else:
        print(results.head(10).to_string(index=True))

    print(f"\n{'='*60}")
    print("Done!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
