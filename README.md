<div align="center">

# Medicine Price Finder

Predict medicine prices and discover cheaper alternatives using machine learning.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=flat-square\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat-square\&logo=scikit-learn\&logoColor=white)](https://scikit-learn.org/)
[![Git LFS](https://img.shields.io/badge/Git_LFS-Model-8033A4?style=flat-square\&logo=gitlfs\&logoColor=white)](https://git-lfs.com/)

<br>

<a href="YOUR_DEPLOYED_URL">
  <strong>Live Demo</strong>
</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="https://github.com/Oblivionium/medicine-finder">
  <strong>Source Code</strong>
</a>

</div>

---

## Overview

Medicine Price Finder is a machine learning application that predicts the price of a medicine from its characteristics and helps users find cheaper alternatives.

Instead of entering model features manually, users can simply search for a medicine, select the exact product, and get a predicted price. The application can then find cheaper medicines with the same composition.

The project combines a **Random Forest regression model**, a **FastAPI backend**, and a lightweight **HTML/CSS/JavaScript frontend**.

## Preview

<!-- Replace this image with a screenshot of the finished website -->

<div align="center">

<img src="docs/screenshots/home.png" alt="Medicine Price Finder" width="850">

</div>

## Features

* Medicine search with exact, prefix, substring, and fuzzy matching
* Search results for different strengths and dosage forms
* Machine-learning based price prediction
* Cheaper alternative finder based on medicine composition
* Dark mode by default
* Light mode with persistent theme preference
* Responsive frontend
* REST API powered by FastAPI
* Interactive API documentation through Swagger
* Model versioned with Git LFS

## How it works

```text
                     Medicine name
                           │
                           ▼
                  ┌─────────────────┐
                  │  Medicine Search │
                  └────────┬────────┘
                           │
                           ▼
                  Select exact product
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Price Prediction          Composition Search
              │                         │
              ▼                         ▼
       Predicted Price          Cheaper Alternatives
```

### Medicine search

The search system doesn't rely on unrestricted fuzzy matching.

It prioritizes:

1. Exact matches
2. Prefix matches
3. Substring matches
4. Fuzzy matching as a fallback

This prevents unrelated medicines with vaguely similar names from dominating the results.

For example:

```text
Tagrisso
    ├── Tagrisso 40mg Tablet
    └── Tagrisso 80mg Tablet
```

Searching for a specific strength also prioritizes the corresponding product.

### Price prediction

The selected medicine is looked up in the dataset and the following features are passed to the trained model:

* Dosage form
* Pack size
* Pack unit
* Primary ingredient
* Primary strength
* Therapeutic class
* Number of active ingredients

The user does not need to enter these features manually.

### Alternative finder

Alternatives are identified using the medicine's cleaned composition.

The application:

* finds medicines with matching composition
* removes the selected product
* keeps only cheaper products
* sorts them by price
* returns the most relevant alternatives

## Model

The final model is a `RandomForestRegressor`.

```text
RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
```

### Evaluation

Evaluation was performed on a held-out test set.

| Metric |   Score |
| ------ | ------: |
| MAE    | ₹116.32 |
| R²     |  0.3599 |
| MdAPE  |  17.04% |

The dataset is heavily right-skewed, with a relatively small number of very expensive medicines.

Because of this, MAE is considered alongside R² and MdAPE rather than being treated as the only measure of performance.

The model performs substantially better on the lower-priced majority of medicines than on the long tail of expensive products.

## Price distribution

The distribution of prices is strongly right-skewed:

```text
Price range       Medicines       MAE
────────────────────────────────────────
₹0–100              31,747       ₹16.88
₹100–500            16,995       ₹45.62
₹500–2,000           1,323      ₹473.34
₹2,000–10,000          560    ₹1,796.27
₹10,000+               169   ₹17,545.05
```

This imbalance is one of the main limitations of the current model.

## Tech stack

### Machine Learning

* Python
* pandas
* NumPy
* scikit-learn
* joblib

### Backend

* FastAPI
* Uvicorn
* RapidFuzz

### Frontend

* HTML
* CSS
* JavaScript
* Quicksand

### Tooling

* Git
* Git LFS
* Jupyter
* GitHub

## Project structure

```text
medicine-finder/
│
├── backend/
│   └── main.py
│
├── data/
│   └── medicine_data.csv
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── models/
│   └── medicine_price_model.joblib
│
├── notebooks/
│   ├── eda.ipynb
│   └── eda.py
│
├── src/
│   ├── alternatives.py
│   ├── cleaning.py
│   ├── data.py
│   ├── features.py
│   ├── predict.py
│   └── search.py
│
├── .gitattributes
├── .gitignore
├── .python-version
├── README.md
└── requirements.txt
```

## Running locally

### 1. Clone the repository

```bash
git clone https://github.com/Oblivionium/medicine-finder.git
cd medicine-finder
```

### 2. Set up Git LFS

The trained model is stored using Git LFS.

```bash
git lfs install
git lfs pull
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Linux / WSL**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the server

From the project root:

```bash
uvicorn backend.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## API

### Health

```http
GET /health
```

Returns:

```json
{
    "status": "ok"
}
```

### Search

```http
GET /api/search?query=Tagrisso
```

Searches for matching medicines.

### Predict price

```http
GET /api/predict/{medicine_name}
```

Returns the model's predicted price for the selected medicine.

### Find alternatives

```http
GET /api/alternatives/{medicine_name}
```

Returns cheaper medicines with the same cleaned composition.

## Development

Model development and exploratory analysis were initially performed in `notebooks/eda.ipynb`.

Once the modelling workflow was finalized, the application-specific code was separated into `src/` so that the deployed application does not depend on the notebook.

The frontend is served directly by FastAPI, keeping the deployment simple and avoiding a separate frontend framework or server.

## Limitations

The predictions should be treated as estimates rather than actual market prices.

The model does not account for:

* Pharmacy-specific pricing
* Location
* Discounts
* Availability
* Real-time market changes
* Brand preferences
* Taxes or other purchase-specific factors

The dataset is also strongly skewed toward lower-priced medicines, which limits prediction accuracy for the relatively small number of high-priced products.

## Deployment

The application is designed to run as a single web service:

```text
Browser
   │
   ▼
FastAPI
   ├── Frontend
   ├── Medicine Search
   ├── Price Prediction
   └── Alternative Finder
          │
          ├── Medicine Dataset
          └── Random Forest Model
```

Deployment configuration will depend on the hosting provider.

## License

This project was developed for educational and demonstration purposes.

---

<div align="center">

Built with Python, FastAPI and scikit-learn.

<a href="https://github.com/Oblivionium/medicine-finder">GitHub</a>

</div>
