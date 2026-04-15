# EnduraAI---ML-System-for-Running-Performance

EnduraAI-ML-System-for-Running-Performance/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── predictions.py
│   │   │   ├── athletes.py
│   │   │   ├── races.py
│   │   │   └── training.py
│   │   ├── schemas/
│   │   │   ├── prediction.py
│   │   │   ├── athlete.py
│   │   │   ├── race.py
│   │   │   └── training.py
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── constants.py
│   │   └── security.py
│   │
│   ├── domain/
│   │   ├── utmb/
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── validators.py
│   │   ├── strava/
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── validators.py
│   │   ├── prediction/
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── scoring.py
│   │   └── recommendations/
│   │       ├── services.py
│   │       └── rules.py
│   │
│   ├── infrastructure/
│   │   ├── storage/
│   │   │   ├── local_files.py
│   │   │   ├── parquet_store.py
│   │   │   └── model_registry.py
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   ├── models.py
│   │   │   └── repositories.py
│   │   ├── clients/
│   │   │   ├── strava_client.py
│   │   │   └── utmb_client.py
│   │   └── monitoring/
│   │       └── metrics.py
│   │
│   ├── ml/
│   │   ├── data/
│   │   │   ├── loaders.py
│   │   │   ├── split.py
│   │   │   └── validation.py
│   │   ├── features/
│   │   │   ├── utmb_features.py
│   │   │   ├── strava_features.py
│   │   │   ├── fusion_features.py
│   │   │   └── preprocess.py
│   │   ├── training/
│   │   │   ├── train_baseline.py
│   │   │   ├── train_regression.py
│   │   │   ├── train_tree_models.py
│   │   │   └── evaluate.py
│   │   ├── inference/
│   │   │   ├── predictor.py
│   │   │   ├── postprocessing.py
│   │   │   └── model_loader.py
│   │   └── artifacts/
│   │       └── README.md
│   │
│   └── services/
│       ├── prediction_service.py
│       ├── athlete_service.py
│       ├── race_service.py
│       └── training_service.py
│
├── frontend/
│   ├── streamlit_app.py
│   └── components/
│
├── data/
│   ├── raw/
│   │   ├── utmb/
│   │   └── strava/
│   ├── interim/
│   │   ├── utmb/
│   │   └── strava/
│   ├── processed/
│   │   ├── utmb/
│   │   ├── strava/
│   │   └── fused/
│   └── external/
│
├── models/
│   ├── baselines/
│   ├── trained/
│   └── metadata/
│
├── notebooks/
│   ├── utmb/
│   ├── strava/
│   └── experiments/
│
├── scripts/
│   ├── ingest_utmb.py
│   ├── ingest_strava.py
│   ├── build_features.py
│   ├── train_model.py
│   └── run_api.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── docs/
│   ├── architecture/
│   ├── product/
│   ├── ml/
│   └── api/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
└── docker-compose.yml



| Datei                                          | Was genau rein muss                                                                 |
| ---------------------------------------------- | ----------------------------------------------------------------------------------- |
| `app/api/main.py`                              | FastAPI-App erstellen, Router registrieren, App-Metadaten, Startup-Basis            |
| `app/api/routes/health.py`                     | einfacher `/health` Endpoint, damit du prüfen kannst, ob API läuft                  |
| `app/api/routes/predictions.py`                | Endpoints für Vorhersagen, z. B. `/predict/time`, Request an Service weitergeben    |
| `app/api/routes/races.py`                      | Endpoints für Race-Daten oder Race-Suche, z. B. verfügbare Rennen/Facts             |
| `app/api/routes/athletes.py`                   | Endpoints für Athlete-Input, Profilwerte oder Strava-basierte Daten                 |
| `app/api/routes/training.py`                   | Endpoints für Trainingsempfehlungen oder Readiness-Logik                            |
| `app/api/schemas/prediction.py`                | Pydantic-Request/Response-Modelle für Vorhersagen                                   |
| `app/api/schemas/race.py`                      | Pydantic-Modelle für Race-Input und Race-Output                                     |
| `app/api/schemas/athlete.py`                   | Pydantic-Modelle für Athlete-Input wie Gewicht, Wochen-km, HR etc.                  |
| `app/api/schemas/training.py`                  | Pydantic-Modelle für Trainings-Inputs/Outputs                                       |
| `app/api/dependencies.py`                      | gemeinsame Dependency-Funktionen, z. B. Predictor laden, Config injizieren          |
| `app/core/config.py`                           | zentrale Settings, Pfade, Modellpfade, ENV-Variablen                                |
| `app/core/logging.py`                          | Logger-Konfiguration für API, Training und Pipelines                                |
| `app/core/constants.py`                        | feste Konstanten wie Dateinamen, Default-Spalten, Zielvariablen                     |
| `app/core/security.py`                         | später API-Key/Auth; in V1 kann das minimal oder leer sein                          |
| `app/domain/utmb/models.py`                    | fachliche Objekte oder Dataclasses für UTMB-Races                                   |
| `app/domain/utmb/services.py`                  | fachliche UTMB-Logik, z. B. Race-Effort, Kategorien, Validierungslogik              |
| `app/domain/utmb/validators.py`                | Prüfungen für UTMB-Daten, z. B. Pflichtspalten, gültige Werte                       |
| `app/domain/strava/models.py`                  | fachliche Strava-Objekte, z. B. Activity, AthleteSummary                            |
| `app/domain/strava/services.py`                | fachliche Logik für Strava-Metriken, z. B. rolling km, pace trends                  |
| `app/domain/strava/validators.py`              | Prüfungen für Strava-Daten                                                          |
| `app/domain/prediction/models.py`              | Objekte für Prediction-Kontext, Input-Strukturen, Ergebnisobjekte                   |
| `app/domain/prediction/services.py`            | Logik, wie Inputs aus Race + Athlete zu einem Modellinput werden                    |
| `app/domain/prediction/scoring.py`             | Score-Logik, z. B. readiness, suitability, confidence                               |
| `app/domain/recommendations/services.py`       | Regeln oder Logik für Race-/Trainingsempfehlungen                                   |
| `app/domain/recommendations/rules.py`          | konkrete regelbasierte Heuristiken                                                  |
| `app/infrastructure/storage/local_files.py`    | Lesen/Schreiben lokaler CSV/Parquet/JSON-Dateien                                    |
| `app/infrastructure/storage/parquet_store.py`  | spezialisierte Parquet-Operationen                                                  |
| `app/infrastructure/storage/model_registry.py` | Laden/Speichern von Modellen und Metadaten                                          |
| `app/infrastructure/database/base.py`          | später DB-Setup; in V1 oft noch nicht nötig                                         |
| `app/infrastructure/database/models.py`        | spätere ORM-Modelle; anfangs leer oder weglassen                                    |
| `app/infrastructure/database/repositories.py`  | später DB-Zugriff; anfangs meist nicht nötig                                        |
| `app/infrastructure/clients/strava_client.py`  | Strava-API-Anbindung oder Mock-Client                                               |
| `app/infrastructure/clients/utmb_client.py`    | falls du externe UTMB-Daten nachladen willst; sonst optional                        |
| `app/infrastructure/monitoring/metrics.py`     | einfache Laufzeit-/Fehler-Metriken oder Platzhalter                                 |
| `app/ml/data/loaders.py`                       | Laden der Trainingsdaten aus raw/interim/processed                                  |
| `app/ml/data/split.py`                         | Train/Validation/Test-Split-Logik                                                   |
| `app/ml/data/validation.py`                    | ML-seitige Datenchecks, Nulls, Datentypen, Zielvariable vorhanden                   |
| `app/ml/features/utmb_features.py`             | alle UTMB-spezifischen Features, z. B. Race_Effort, Pace-Metriken                   |
| `app/ml/features/strava_features.py`           | Strava-spezifische Features, z. B. rolling_7d_km, avg_hr_efficiency                 |
| `app/ml/features/fusion_features.py`           | Features aus der Kombination von Race + Athlete                                     |
| `app/ml/features/preprocess.py`                | allgemeine Vorverarbeitung wie Encoding, Spaltenselektion, Scaling                  |
| `app/ml/training/train_baseline.py`            | Dummy/Baseline-Modell trainieren                                                    |
| `app/ml/training/train_regression.py`          | lineare oder reguläre Regressionsmodelle trainieren                                 |
| `app/ml/training/train_tree_models.py`         | Random Forest / Gradient Boosting / XGBoost-artige Modelle                          |
| `app/ml/training/evaluate.py`                  | RMSE, MAE, R², Fehleranalyse, Feature Importance                                    |
| `app/ml/inference/predictor.py`                | zentrale Klasse für `.predict()` mit geladenem Modell                               |
| `app/ml/inference/postprocessing.py`           | Prediction-Output hübsch machen, runden, Erklärwerte ergänzen                       |
| `app/ml/inference/model_loader.py`             | Modell + Preprocessor + Metadaten laden                                             |
| `app/services/prediction_service.py`           | API-nahe Businesslogik: Request rein, Featurebau, Predictor aufrufen, Response raus |
| `app/services/athlete_service.py`              | Athlete-bezogene Logik, z. B. Profil vorbereiten                                    |
| `app/services/race_service.py`                 | Race-bezogene Logik für Filtern, Lookup, Normalisierung                             |
| `app/services/training_service.py`             | Trainings-/Readiness-Service                                                        |
| `frontend/streamlit_app.py`                    | Haupt-UI, Inputs sammeln, API aufrufen oder lokal Predictor nutzen                  |
| `frontend/components/`                         | wiederverwendbare UI-Bausteine, z. B. Race-Form, Athlete-Card, Metrics              |
| `scripts/ingest_utmb.py`                       | UTMB-Rohdaten einlesen und in raw/interim speichern                                 |
| `scripts/ingest_strava.py`                     | Strava-Daten einlesen oder von API abholen                                          |
| `scripts/build_features.py`                    | Feature-Pipeline von raw/interim nach processed/fused                               |
| `scripts/train_model.py`                       | Trainingsskript für End-to-End-Trainingslauf                                        |
| `scripts/run_api.py`                           | lokales Startskript für FastAPI                                                     |
| `tests/unit/`                                  | kleine Tests für Featurefunktionen, Utilities, Validatoren                          |
| `tests/integration/`                           | Tests, ob Loader + Features + Modell zusammen funktionieren                         |
| `tests/api/`                                   | Tests für FastAPI-Endpunkte                                                         |
| `docs/architecture/`                           | Architekturdiagramme, Struktur, Datenfluss                                          |
| `docs/product/`                                | Produktidee, Zielgruppe, Use Cases                                                  |
| `docs/ml/`                                     | Features, Modelle, Evaluation, Datenannahmen                                        |
| `docs/api/`                                    | Endpoint-Dokumentation, Request-/Response-Beispiele                                 |
| `data/raw/utmb/`                               | originale unveränderte UTMB-Daten                                                   |
| `data/raw/strava/`                             | originale unveränderte Strava-Daten                                                 |
| `data/interim/utmb/`                           | erste bereinigte Zwischenschritte                                                   |
| `data/interim/strava/`                         | erste bereinigte Strava-Zwischenschritte                                            |
| `data/processed/utmb/`                         | fertige ML-taugliche UTMB-Tabellen                                                  |
| `data/processed/strava/`                       | fertige ML-taugliche Strava-Tabellen                                                |
| `data/processed/fused/`                        | zusammengeführte Modell-Inputs                                                      |
| `models/baselines/`                            | einfache Baseline-Modelle                                                           |
| `models/trained/`                              | finale trainierte Modelle                                                           |
| `models/metadata/`                             | Metriken, Featurelisten, Trainingsparameter, Modellinfos                            |
| `notebooks/utmb/`                              | EDA und Analyse nur für UTMB                                                        |
| `notebooks/strava/`                            | EDA und Analyse nur für Strava                                                      |
| `notebooks/experiments/`                       | spontane Modell- und Feature-Experimente                                            |
| `.env`                                         | echte lokale Secrets                                                                |
| `.env.example`                                 | Vorlage ohne Secrets                                                                |
| `README.md`                                    | Setup, Projektziel, Struktur, Quickstart                                            |
| `requirements.txt`                             | Dependencies                                                                        |
| `pyproject.toml`                               | Projekt-Metadaten, Tooling, Formatierung, Packaging                                 |
| `docker-compose.yml`                           | später Container-Setup für API/Frontend/DB                                          |




| Bereich                            | Stunden |
| ---------------------------------- | ------: |
| Projektstruktur sauber umbauen     |     4–8 |
| UTMB Loader + Cleaning             |    6–12 |
| Strava Loader + erste Features     |    6–12 |
| Fusion Features                    |     4–8 |
| Baseline + Regression + Evaluation |    8–16 |
| Inference Layer                    |     4–8 |
| FastAPI                            |    6–12 |
| Streamlit Frontend                 |    6–12 |
| Tests + Doku + Cleanup             |    8–20 |
