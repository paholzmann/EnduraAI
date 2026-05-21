import pandas as pd
import numpy as np
import logging

from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, mean_absolute_error, mean_squared_error, r2_score

from app.core.utils.file_utils import FileUtils
from app.ml.utils.preprocessing import Preprocessing
from app.ml.utils.data_splitter import DataSplitter
from app.ml.utils.plots import Plots
from app.ml.utils.regression_model import RegressionModel


class RaceOutcomeEngine:
    def __init__(self):
        self.file_utils = FileUtils()
        self.preprocessing = Preprocessing()
        self.data_splitter = DataSplitter()
        self.plotter = Plots()
        self.regression_model = RegressionModel()

        
        self.utmb_df = self.file_utils.read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-features.csv")

        self.features = ["Distance", "Elevation_Gain", "Elevation_per_km", "Race_Effort"]
        self.targets = ["Winning_Time", "Median_Time", "Slowest_Time"]

        check_missing_columns = self.features + self.targets + ["Race_Title_Cleaned"]
        self.train_df = self.preprocessing.drop_missing(df=self.utmb_df, columns=check_missing_columns)

        self.predicted_columns = []

    def train_pipeline(self):

        X = self.train_df[self.features]
        y = self.train_df[self.targets]
        group_splitter = GroupShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
        train_index, test_index = next(group_splitter.split(X, y, self.train_df["Race_Title_Cleaned"].astype(str)))
        x_train, x_test, y_train, y_test = X.iloc[train_index], X.iloc[test_index], y.iloc[train_index], y.iloc[test_index]

        random_forest_regressor = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
        random_forest_regressor.fit(x_train, y_train)
        return random_forest_regressor, x_train, x_test, y_train, y_test
    
    def evaluate_model(self, model: RandomForestRegressor, x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame):
        train_preds, test_preds = self.regression_model.get_train_test_prediction(model=model, x_train=x_train, x_test=x_test)
        metrics= self.regression_model.get_basic_metrics(train_preds=train_preds, test_preds=test_preds, y_test=y_test, y_train=y_train)
        error_df, self.predicted_columns = self.regression_model.create_predictions_df(test_preds=test_preds, x_test=x_test, y_test=y_test, targets=self.targets)
        print(error_df)
        error_df = self.regression_model.calculate_residuals(error_df=error_df, predicted_columns=self.predicted_columns, targets=self.targets)
        print(error_df)
        return metrics, error_df, train_preds, test_preds
        
    def visualization(self, df: pd.DataFrame) -> None:
        for predicted_col, target_col in zip(self.predicted_columns, self.targets):
            self.plotter.prediction_vs_actual(y_pred=df[predicted_col], y_true=df[target_col])

# Next steps:
# Error analysis
# Visualization for everything (predictions, error analysis, etc.)
# Feature importance
# New Features (features that give the model new information (distance, elevation but not race effort because it is the same information as distance and elevation))

engine = RaceOutcomeEngine()
model, x_train, x_test, y_train, y_test = engine.train_pipeline()
_, error_df, _, _ = engine.evaluate_model(model, x_train, x_test, y_train, y_test)
engine.visualization(df=error_df)


"""

Error Analysis ist einer der Punkte, der Anfänger von Leuten trennt, die wirklich ML-Systeme bauen. Du brauchst nicht nur wissen: *"Mein Modell hat R²=0.89"*, sondern:

> **Wo macht mein Modell Fehler und warum?**

Gerade für EndurAI ist das extrem wertvoll.

# Ziel

Nicht:

> Modell schlecht → mehr Bäume

Sondern:

> Modell schlecht bei langen technischen Rennen → Feature fehlt

---

# Schritt 1: Ergebnisse-Tabelle bauen

Immer nach dem Predict:

```python
results = X_test.copy()

results["actual"] = y_test
results["pred"] = y_pred

results["error"] = (
    results["actual"] - results["pred"]
)

results["abs_error"] = abs(
    results["error"]
)
```

Beispiel:

| Distance | Elevation | actual | pred | error | abs_error |
| -------: | --------: | -----: | ---: | ----: | --------: |
|       20 |       500 |    120 |  118 |     2 |         2 |
|      100 |      6000 |   1300 |  900 |   400 |       400 |

Sofort sichtbar:

Rennen 2 wurde komplett falsch vorhergesagt.

---

# Schritt 2: Größte Fehler ansehen

```python
results.sort_values(
    "abs_error",
    ascending=False
).head(20)
```

Fragen:

```text
Welche Rennen werden zerstört?
```

Suche Muster:

* nur sehr lange Rennen?
* nur sehr viele Höhenmeter?
* nur bestimmte Kategorien?
* nur Extremwerte?

---

# Schritt 3: Prediction vs Realität plotten

```python
import matplotlib.pyplot as plt

plt.scatter(
    y_test,
    y_pred
)

plt.xlabel("Actual")
plt.ylabel("Prediction")

plt.show()
```

Ideal:

```text
•
  •
    •
      •
        •
```

Diagonale.

Schlecht:

```text
• • • • •
```

---

Noch besser:

```python
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()]
)
```

Dann siehst du die ideale Linie.

---

# Schritt 4: Fehlerverteilung ansehen

```python
plt.hist(
    results["error"],
    bins=50
)

plt.show()
```

Interpretation:

Mitte bei 0:

gut.

Links:

Modell überschätzt.

Rechts:

Modell unterschätzt.

---

Beispiel:

```text
Fehler stark positiv
```

heißt:

```text
actual > prediction
```

Modell sagt zu kleine Werte.

---

# Schritt 5: Fehler gegen Features plotten

Das ist Gold.

Distance:

```python
plt.scatter(
    results["Distance"],
    results["abs_error"]
)
```

Frage:

Werden Fehler größer?

Beispiel:

```text
20km → Fehler klein

100km → Fehler riesig
```

Aha:

Lange Rennen schwierig.

---

Höhenmeter:

```python
plt.scatter(
    results["Elevation_Gain"],
    results["abs_error"]
)
```

---

Race Category:

```python
results.groupby(
    "Race_Category"
)["abs_error"].mean()
```

Beispiel:

| Kategorie | Fehler |
| --------- | -----: |
| 20K       |     35 |
| 50K       |     50 |
| 100K      |    150 |
| 100M      |    310 |

Sofort sichtbar:

Ultra-Rennen problematisch.

---

# Schritt 6: Warum fragen

Jetzt beginnt ML-Denken:

100M schlecht?

Warum?

Vielleicht:

Feature fehlt:

```text
Elevation/km
Race_effort
Technicality
Temperature
```

oder:

```text
Zu wenig Trainingsdaten
```

oder:

```text
Ausreißer
```

---

# Schritt 7: Feature bauen → erneut testen

Du erkennst:

```text
Distance + Elevation reicht nicht
```

Neue Idee:

```python
Race_Effort=
distance+elevation/100
```

Trainieren.

Vergleichen:

Vorher:

```text
MAE=91
```

Nachher:

```text
MAE=70
```

Perfekt.

---

Für EndurAI würde ich jedes Modell mit dieser festen Checkliste bauen:

```text
[ ] MAE
[ ] RMSE
[ ] R²
[ ] Prediction vs Actual Plot
[ ] Error Histogram
[ ] Top 20 größte Fehler
[ ] Fehler nach Kategorie
[ ] Fehler vs Distance
[ ] Fehler vs Elevation
[ ] Hypothese
[ ] Neues Feature
```

Das ist schon fast ein professioneller ML-Workflow.


"""