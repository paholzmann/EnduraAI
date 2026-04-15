# 🏔️ UTMB Race Performance Analysis & Prediction


# Targets



## 📌 Overview

This project analyzes large-scale ultra trail running race data from UTMB events (833,000+ race records) to understand performance patterns and build predictive models.

The goal is to answer questions like:

* What makes a race difficult?
* How do distance and elevation impact finishing times?
* Can we predict finishing times or race outcomes?

This project is part of a larger **Performance Optimization System for Runners**, combining public race data with personal training data.

---

## 🎯 Objectives

### 1. Data Understanding

* Clean and structure raw UTMB race data
* Extract meaningful numerical features from raw strings

### 2. Exploratory Data Analysis (EDA)

* Analyze relationships between:

  * Distance
  * Elevation gain
  * Finishing times
  * Participant distributions

### 3. Feature Engineering

* Create a **Race Difficulty Score**
* Extract demographic insights (age, gender distribution)
* Compute race-level statistics

### 4. Predictive Modeling

* Predict:

  * Finishing times (regression)
  * Race difficulty (scoring)
* Compare baseline vs advanced models

---

## 📂 Dataset

### Source

UTMB race dataset (JSON format)

### Size

* ~833,000 race entries

### Structure

| Field          | Description             |
| -------------- | ----------------------- |
| Age            | Age group distribution  |
| City / Country | Race location           |
| Country        | Participants by country |
| Date           | Race date               |
| Distance       | Race distance (string)  |
| Elevation Gain | Elevation gain (string) |
| N Results      | Number of participants  |
| Race Category  | e.g. 50K / 100K / 100M  |
| Race Title     | Race name               |
| Results        | Finishing times (hours) |
| Sex            | Gender distribution     |

---

## 🛠️ Data Processing

### Cleaning

* Convert strings to numeric:

  * `"99.1 KM"` → `99.1`
  * `"5990 M+"` → `5990`
* Handle missing / zero values in results
* Normalize categorical fields

### Feature Engineering

#### Core Features

* `distance_km`
* `elevation_m`
* `participants`

#### Derived Features

* `difficulty_score = distance_km * elevation_m`
* `avg_finish_time`
* `median_finish_time`
* `finish_rate`
* `female_ratio`
* `age_distribution_stats`

---

## 📊 Exploratory Analysis

Key analyses include:

* Distribution of finishing times
* Elevation vs finishing time
* Distance vs race completion rate
* Category comparisons (50K vs 100K vs 100M)

---

## 🤖 Modeling

### Targets

* `avg_finish_time` (Regression)
* `difficulty_score` (Regression / Ranking)

### Models

* Baseline:

  * Linear Regression
* Intermediate:

  * Random Forest
* Advanced:

  * Gradient Boosting (XGBoost / LightGBM)

### Evaluation Metrics

* MAE
* RMSE
* R² Score

---

## 📁 Project Structure

```
utmb-performance/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   ├── cleaning.py
│   │
│   ├── features/
│   │   ├── feature_engineering.py
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

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/utmb-performance.git
cd utmb-performance
```

### 2. Create environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run notebooks

```bash
jupyter notebook
```

---

## 📈 Example Use Cases

* Estimate race difficulty before participating
* Compare races based on objective metrics
* Analyze trends in ultra running performance
* Build data-driven training strategies

---

## 🧠 Key Learnings

* Large-scale data cleaning (JSON → structured data)
* Feature engineering for real-world problems
* Regression modeling on noisy sports data
* Translating domain knowledge (running) into ML features

---

## 🔮 Future Work

* Integrate personal training data (Strava, Polar)
* Build personalized performance predictions
* Add API for real-time predictions
* Develop recommendation system for race selection

---

## 📬 Contact

If you’re interested in ML + endurance sports, feel free to connect.

---

## ⭐ Motivation

This project combines:

* Machine Learning Engineering
* Endurance Sports
* Real-world data systems

with the goal of building intelligent systems for performance optimization.
