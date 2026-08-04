# Student Success Prediction in Higher Education

Machine-learning analysis of student dropout, continued enrolment and graduation in higher education. The project combines supervised classification, grade regression and unsupervised student profiling in a single reproducible notebook.

Developed by **Rodrigo Alejandro Sicilia Maroto** as the final project for the Machine Learning course (2025/2026), Universidad Pontificia Comillas - ICAI.

## Project highlights

- **Multiclass classification:** six linear and non-linear models compared with stratified cross-validation. Logistic Regression achieved a weighted F1-score of **0.7617** and test accuracy of **0.7718**.
- **Second-semester grade regression:** leakage-prone second-semester predictors were excluded. Lasso achieved **R² = 0.7430**, **RMSE = 2.6379** and **MAE = 1.5521**.
- **Unsupervised learning:** PCA, K-Means and Ward hierarchical clustering identified three stable student profiles. K-Means achieved a silhouette score of **0.3223**, with a mean subsampling ARI of **0.9922**.
- **Interpretability and robustness:** permutation importance, impurity-based importance, residual analysis, learning curves and bootstrap confidence intervals.
- **Early-warning analysis:** using only information available before the first semester reduced weighted F1 from **0.7617** to **0.6270**, showing the value of early university performance data.

## Main results

### Classification

The strongest classes were `graduado` and `abandono`; `matriculado` was substantially harder because it is both the smallest class and an intermediate state that overlaps with the other two outcomes.

![Confusion matrix for the best classifier](assets/classification_confusion_matrix.png)

Academic performance variables from the first and second semesters dominated the permutation-importance ranking, followed by administrative variables such as tuition status.

![Classification permutation importance](assets/classification_permutation_importance.png)

### Regression

The most informative predictors of second-semester mean grade were the number of first-semester subjects passed and the first-semester mean grade. A reduced set of 21 numerical and binary predictors lost only 0.007 R² compared with the full encoded feature set.

![Regression feature importance](assets/regression_feature_importance.png)

### Student profiles

Both K-Means and Ward clustering recovered a similar three-group structure: a low-performance group with a high concentration of dropouts, a large standard-student group and a smaller high-workload group with many credited subjects.

![PCA projection comparing K-Means and Ward clusters](assets/pca_cluster_comparison.png)

## Repository structure

```text
student-success-ml/
├── README.md
├── LICENSE
├── requirements.txt
├── .python-version
├── .gitignore
├── .github/workflows/
│   └── validate-notebook.yml
├── notebooks/
│   └── student_success_analysis.ipynb
├── data/
│   ├── README.md
│   └── rendimiento_estudiantes.csv
└── assets/
    ├── classification_confusion_matrix.png
    ├── classification_permutation_importance.png
    ├── regression_feature_importance.png
    ├── clustering_model_selection.png
    └── pca_cluster_comparison.png
```

## Reproducibility

The repository has been validated with **Python 3.13.5** and the exact package versions in `requirements.txt`. A complete run takes approximately six to ten minutes on a modern laptop, depending on the processor.

### Windows PowerShell

```powershell
git clone <repository-url>
cd student-success-ml
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

### macOS or Linux

```bash
git clone <repository-url>
cd student-success-ml
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

Open `notebooks/student_success_analysis.ipynb` and run **Kernel -> Restart Kernel and Run All Cells**. The notebook searches for the dataset both from the repository root and from the `notebooks/` directory.

Every push and pull request is also checked automatically by the GitHub Actions workflow in `.github/workflows/validate-notebook.yml`.

A headless execution can also be performed with:

```bash
jupyter nbconvert --to notebook --execute notebooks/student_success_analysis.ipynb \
  --output student_success_analysis_executed.ipynb \
  --ExecutePreprocessor.timeout=1800
```

## Methodology

1. **Exploratory data analysis:** class balance, distributions, consistency checks, correlations and interaction profiles.
2. **Preprocessing:** rare-category grouping, one-hot encoding, stratified train/test splitting and training-only standardisation.
3. **Classification:** Logistic Regression, LDA, KNN, Random Forest, Gradient Boosting and RBF SVM.
4. **Regression:** Linear Regression, Ridge, Lasso, Elastic Net, Random Forest and KNN.
5. **Unsupervised learning:** StandardScaler, PCA, K-Means, Ward clustering and stability analysis.
6. **Validation:** five-fold cross-validation, held-out test evaluation, learning curves and bootstrap confidence intervals.

## Dataset

The project uses a Spanish-labelled derivative of the UCI **Predict Students' Dropout and Academic Success** dataset: 4,424 anonymised records, 36 predictors and one three-class target. See [`data/README.md`](data/README.md) for attribution and licensing details.

## Limitations and responsible use

- The `matriculado` class is an intermediate state and is inherently harder to distinguish from eventual graduation or dropout.
- The second-semester mean grade is structurally bimodal: many observations are zero, while passing averages lie mostly between 10 and 20.
- Administrative and socioeconomic variables can reflect underlying structural factors; associations must not be interpreted as causal effects.
- Any real institutional deployment would require fairness analysis, calibration, monitoring and human oversight. The models in this repository are an academic study, not a production decision system.

## License

The source code and notebook are released under the [MIT License](LICENSE). The dataset is governed separately by the CC BY 4.0 terms described in [`data/README.md`](data/README.md).
