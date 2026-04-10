# 🏃 Personal Running Performance System (Strava-Based)

## 📌 Overview

This project builds a **personal performance analytics and prediction system** using running data from Strava and wearable devices (e.g. Polar, Suunto).

The goal is to transform raw activity data into actionable insights and predictive models that answer questions like:

* How does pace evolve at the same heart rate over time?
* Can we predict future performance improvements?
* What training patterns lead to better results?

This project complements the **UTMB Race Analysis Project** by focusing on **individual-level optimization**, while UTMB focuses on **population-level insights**.

---

## 🎯 Objectives

### 1. Data Integration

* Collect and unify running data from:

  * Strava
  * Wearables (Polar, Suunto)

### 2. Data Processing

* Clean and standardize activity-level data
* Handle missing or inconsistent metrics (e.g. HR gaps)

### 3. Feature Engineering

* Create performance metrics (pace, HR efficiency, load)
* Build time-based features (weekly trends, fatigue)

### 4. Modeling

* Predict:

  * Pace at a given heart rate
  * Performance improvements over time
  * Race readiness

---

## 📂 Dataset

### Source

* Strava API
* Exported activity data (JSON / CSV)

### Structure (Typical Activity Fields)

| Field                | Description            |
| -------------------- | ---------------------- |
| distance             | Distance in meters     |
| moving_time          | Moving time in seconds |
| average_heartrate    | Avg HR                 |
| max_heartrate        | Max HR                 |
| total_elevation_gain | Elevation gain         |
| start_date           | Activity timestamp     |
| type                 | Activity type (Run)    |

---

## 🛠️ Data Processing

### Cleaning

* Convert units:

  * meters → km
  * seconds → minutes
* Remove invalid activities:

  * missing HR
  * unrealistic pace
* Normalize timestamps

### Feature Engineering

#### Core Features

* `distance_km`
* `pace_min_per_km`
* `avg_hr`
* `elevation_gain`

#### Derived Features

* `hr_efficiency = pace / avg_hr`
* `training_load = distance_km * avg_hr`
* `elevation_per_km`
* `rolling_weekly_km`
* `rolling_avg_hr`
* `fatigue_index`

---

## 📊 Exploratory Analysis

Key analyses include:

* Pace vs Heart Rate relationship
* Weekly mileage trends
* HR drift over long runs
* Performance progression over time

---

## 🤖 Modeling

### Targets

* `pace_min_per_km` at given HR
* performance trend (time series prediction)

### Model Ideas

* Baseline:

  * Linear Regression
* Intermediate:

  * Random Forest
* Advanced:

  * Gradient Boosting
  * Time Series Models (optional)

---

## 📁 Project Structure

```id="p82jda"
strava-performance/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_modeling.ipynb
│
├── src/
│   ├── data/
│   │   ├── strava_client.py
│   │   ├── loader.py
│   │
│   ├── features/
│   │   ├── performance_features.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │
│   ├── utils/
│   │   ├── logger.py
│
├── models/
├── reports/
├── requirements.txt
└── README.md
```

---

## 🔌 Data Collection

### Option 1: Strava API

* Use OAuth authentication
* Fetch activities via `/athlete/activities`

### Option 2: Export Data

* Export activities from Strava dashboard
* Load JSON/CSV files locally

---

## 🚀 Getting Started

### 1. Clone the repository

```bash id="z3m91x"
git clone https://github.com/yourusername/strava-performance.git
cd strava-performance
```

### 2. Create environment

```bash id="d7aklq"
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash id="c9ak2x"
pip install -r requirements.txt
```

### 4. Run notebooks

```bash id="f3m19k"
jupyter notebook
```

---

## 📈 Example Use Cases

* Track performance improvements over time
* Optimize training intensity
* Predict race readiness
* Analyze efficiency at different heart rates

---

## 🧠 Key Learnings

* Time-series analysis for sports data
* Feature engineering for physiological signals
* Combining domain knowledge (running) with ML
* Building personal analytics systems

---

## 🔮 Future Work

* Combine with UTMB dataset for hybrid modeling
* Build personalized race predictions
* Deploy as a web app (Streamlit / FastAPI)
* Integrate real-time wearable data

---

## 🔗 Integration with UTMB Project

This project is designed to integrate with:
👉 **UTMB Race Performance Analysis**

Combination enables:

* Personal vs global performance comparison
* Personalized race recommendations
* More accurate predictions

---

## 📬 Contact

Open to collaboration in:

* ML for sports performance
* Data-driven training systems

---

## ⭐ Motivation

This project represents:

* Real-world ML system building
* Personal data utilization
* Performance optimization through data

The ultimate goal is to build intelligent systems that improve human performance.
