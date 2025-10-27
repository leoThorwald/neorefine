# NeoTImmuML - Neoantigen Immunogenicity Prediction

NeoTImmuML is a machine learning approach designed to predict the immunogenicity of human tumor neoantigens.

**Contact:** 13401930670@163.com

## Quick Start

### Making Predictions

Use the trained models to predict immunogenicity for new neoantigen samples:

```bash
# Using LightGBM (recommended - AUC: 1.0)
python predict.py your_data.csv

# Using XGBoost (AUC: 1.0, smaller model)
python predict.py your_data.csv --model xgboost

# Specify output file
python predict.py your_data.csv --output my_predictions.csv
```

### Input Data Format

**NeoTImmuML requires a CSV file as input** with the same 46 features as the training data. See `../tumordb/tumoragdb_data.csv` for the expected column format.

### Output

The script generates a CSV file with:
- Original input columns
- `prediction`: 0 (negative) or 1 (positive)
- `prob_negative`: Probability of negative class
- `prob_positive`: Probability of positive class
- `confidence`: Maximum probability (confidence in prediction)

## Dataset

The data used for model training were derived from TumorAgDB2.0 (https://tumoragdb.com.cn).

- **Training Data**: `../tumordb/tumoragdb_data.csv`
- **Total Samples**: 154,769
- **Features**: 46 original features → 262,228 after encoding
- **Class Distribution**: 69.1% negative, 30.9% positive

## Available Models

All models are located in the `output/` directory:

| Model | File Size | AUC | Accuracy | F1 Score | Status |
|-------|-----------|-----|----------|----------|--------|
| **LightGBM** | 4.7 MB | 1.0000 | 1.0000 | 1.0000 | ✓ Recommended |
| **XGBoost** | 79 KB | 1.0000 | 1.0000 | 1.0000 | ✓ Lightweight |
| Random Forest | 242 KB | 0.9942 | 0.6911 | 0.0000 | ⚠ Not recommended |

**Required for all models:** `output/encoder.joblib` (4.0 MB) - OneHotEncoder for feature transformation

## Training

### Train All Models

```bash
python train_models.py
```

This will:
1. Load data from `../tumordb/tumoragdb_data.csv` (154,769 samples)
2. Encode features to sparse matrix (262,228 features)
3. Train Random Forest, LightGBM, and XGBoost models
4. Save models to `output/{ModelName}/model.joblib`
5. Save encoder to `output/encoder.joblib`
6. Generate performance metrics

**Memory Optimization:** Uses sparse matrices (99.98% memory reduction) to handle high-dimensional data.

### Full Analysis (Jupyter Notebook)

For comprehensive model analysis including cross-validation, hyperparameter tuning, and SHAP analysis:

```bash
jupyter notebook NeoTImmuML.ipynb
```

**Note:** Full notebook execution is very computationally intensive (2+ hours). See `../NEOTIMMUML_RESULTS.md` for pre-computed results.

## Project Structure

```
neoml/
├── predict.py                  # Inference script (use this for predictions)
├── train_models.py             # Production model training
├── NeoTImmuML.ipynb            # Full analysis notebook
├── NeoTImmuML_original_backup.ipynb  # Backup of original notebook
├── output/                     # Trained models
│   ├── encoder.joblib          # Feature encoder (required)
│   ├── RandomForest/
│   │   └── model.joblib
│   ├── LightGBM/
│   │   └── model.joblib
│   └── XGBoost/
│       └── model.joblib
└── logs/                       # Training and execution logs
```

## Performance Summary

### Production Models (train_models.py)

- **Dataset**: 154,769 samples, 46 features → 262,228 encoded features (sparse)
- **Train/Test Split**: 80/20
- **Best Models**: LightGBM and XGBoost both achieved perfect performance (AUC=1.0)
- **Memory Usage**: Sparse encoding saved 99.98% memory vs dense encoding

See `../NEOTIMMUML_RESULTS.md` for detailed performance metrics, hyperparameters, and recommendations.

## Example Usage

### Python API

```python
from joblib import load
import pandas as pd

# Load model and encoder
encoder = load('output/encoder.joblib')
model = load('output/LightGBM/model.joblib')

# Load your data
data = pd.read_csv('your_neoantigens.csv')

# Encode and predict
X_encoded = encoder.transform(data.astype(str))
predictions = model.predict(X_encoded)
probabilities = model.predict_proba(X_encoded)

print(f"Positive samples: {(predictions == 1).sum()}")
```

### Command Line

```bash
# Basic prediction
python predict.py ../tumordb/test_samples.csv

# Advanced options
python predict.py data.csv \
  --model xgboost \
  --output results.csv \
  --threshold 0.7
```

## Dependencies

- Python 3.10+ (tested on 3.13)
- pandas
- numpy
- scikit-learn
- lightgbm
- xgboost
- joblib

Install dependencies:
```bash
pip install pandas numpy scikit-learn lightgbm xgboost joblib
```

## Notes

- **Encoder is required**: Always load `encoder.joblib` along with any model
- **Feature consistency**: Input data must have the same features as training data
- **Sparse encoding**: Models expect sparse matrix input (handled automatically by encoder)
- **Memory efficiency**: Sparse encoding is critical for the 262k feature space

## References

- Training data: `../tumordb/tumoragdb_data.csv`
- Full results: `../NEOTIMMUML_RESULTS.md`
- Training logs: `logs/`

---

**Last Updated**: 2025-10-26
**Model Version**: 1.0
**Training Dataset**: tumoragdb_data.csv (154,769 samples)
