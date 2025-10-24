# NeoTImmuML - Execution Guide

## Setup Complete ✓

The notebook has been configured to use `tumoragdb_data.csv` as the training dataset. All dependencies have been installed and the OpenMP library issue for LightGBM has been resolved.

## Dataset Information

- **File**: `../tumordb/tumoragdb_data.csv`
- **Size**: 49 MB
- **Samples**: 154,769 rows
- **Features**: 46 columns (after excluding id and antigenName)
- **Target**: `immunogenicity` (binary classification)
  - Positive samples: 47,808 (30.89%)
  - Negative samples: 106,961 (69.11%)
- **Note**: Dataset is imbalanced and contains missing values that will be handled during preprocessing

## How to Execute the Notebook

### Option 1: Jupyter Notebook

```bash
cd /Users/vanetten/git_repos/neorefine/NeoTImmuML
jupyter notebook NeoTImmuML.ipynb
```

Then run all cells from the menu: Cell → Run All

### Option 2: JupyterLab

```bash
cd /Users/vanetten/git_repos/neorefine/NeoTImmuML
jupyter lab NeoTImmuML.ipynb
```

### Option 3: VS Code

Open the notebook in VS Code with the Jupyter extension installed.

### Option 4: Command Line Execution

```bash
cd /Users/vanetten/git_repos/neorefine/NeoTImmuML
jupyter nbconvert --to notebook --execute NeoTImmuML.ipynb --output NeoTImmuML_executed.ipynb
```

## What the Notebook Will Do

1. **Data Loading & Preprocessing** - Load tumoragdb_data.csv and encode categorical features
2. **5-Fold Cross-Validation** - Evaluate 8 models:
   - LightGBM
   - XGBoost
   - Random Forest
   - Naive Bayes (Gaussian)
   - Logistic Regression CV
   - SVC
   - K-Nearest Neighbors
   - MLP (Neural Network)
3. **Hyperparameter Tuning** - Grid search for:
   - LightGBM
   - XGBoost
   - Random Forest
4. **Ensemble Models** - Create weighted voting ensembles
5. **SHAP Analysis** - Generate feature importance and interpretability plots
6. **Visualizations** - ROC curves, radar charts, and performance comparisons

## Expected Outputs

The notebook will create the following directories and files:

- `./output/SHAP_LightGBM/` - SHAP plots for LightGBM
- `./output/SHAP_XGBoost/` - SHAP plots for XGBoost
- Model files:
  - `RandomForest_model.joblib`
  - `LightGBM_model.joblib`
  - `XGBoost_model.joblib`

## Important Notes

- The dataset is large (154K samples), so training may take significant time
- Hyperparameter tuning cells (Grid Search) are computationally expensive
- You may want to reduce the parameter grids for faster testing
- The independent dataset validation cell is commented out - uncomment and update the path when you have an independent test set

## Performance Expectations

Based on the original notebook outputs, you can expect:

- **Best Models**: LightGBM and XGBoost (AUC ~0.87)
- **Training Time**:
  - 5-fold CV with 8 models: ~10-20 minutes
  - Hyperparameter tuning: ~1-3 hours per model (depending on grid size)
- **Ensemble Model**: Weighted voting typically achieves AUC ~0.870

## Troubleshooting

If you encounter issues:

1. **LightGBM Import Error**: The libomp library has been installed and symlinked. If issues persist, run:
   ```bash
   export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:$DYLD_LIBRARY_PATH
   ```

2. **Memory Issues**: Consider reducing the dataset size or using a subset for initial testing

3. **Long Training Times**: Reduce `n_estimators` in model definitions or skip hyperparameter tuning cells

## Environment

- Python: 3.13.7
- Virtual Environment: `.venv`
- Key packages installed:
  - pandas 2.3.3
  - numpy 2.3.4
  - scikit-learn 1.7.2
  - lightgbm 4.6.0
  - xgboost 3.1.1
  - shap 0.49.1
  - matplotlib 3.10.7
  - seaborn 0.13.2

## Quick Start Commands

```bash
# Navigate to project directory
cd /Users/vanetten/git_repos/neorefine/NeoTImmuML

# Activate virtual environment (if needed)
source ../.venv/bin/activate

# Launch Jupyter
jupyter notebook NeoTImmuML.ipynb
```
