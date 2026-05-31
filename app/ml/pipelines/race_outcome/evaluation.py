import pandas as pd
import numpy as np
import logging

from app.core.logger import Logger
from app.ml.pipelines.race_outcome.config import RaceOutcomeConfig

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.inspection import permutation_importance


class EvaluateRaceOutcome:
    def __init__(self):
        self.logger = Logger(name="Race Outcome Pipeline", level=logging.INFO, log_file="app/logs/ml/race_outcome/race_outcome_pipeline.log").logger
        self.config = RaceOutcomeConfig()

    def get_train_test_prediction(self, model: RandomForestRegressor, x_train: pd.DataFrame, x_test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        train_preds = model.predict(x_train)
        test_preds = model.predict(x_test)
        train_preds = pd.DataFrame(train_preds, columns=self.config.targets, index=x_train.index)
        test_preds = pd.DataFrame(test_preds, columns=self.config.targets, index=x_test.index)
        return train_preds, test_preds

    def get_metrics(self, train_preds, test_preds, y_train: pd.DataFrame, y_test: pd.DataFrame):
        target_columns = y_train.columns
        metrics = {}
        for target_column in target_columns:
            metrics[target_column] = {}
            metrics[target_column]["Train MAE"] = mean_absolute_error(y_train[target_column], train_preds[target_column])
            metrics[target_column]["Train RMSE"] = np.sqrt(mean_squared_error(y_train[target_column], train_preds[target_column]))
            metrics[target_column]["Train R2"] = r2_score(y_train[target_column], train_preds[target_column])

            metrics[target_column]["Test MAE"] = mean_absolute_error(y_test[target_column], test_preds[target_column])
            metrics[target_column]["Test RMSE"] = np.sqrt(mean_squared_error(y_test[target_column], test_preds[target_column]))
            metrics[target_column]["Test R2"] = r2_score(y_test[target_column], test_preds[target_column])
        return metrics
    
    def get_feature_importance(self, model: RandomForestRegressor, x_test: pd.DataFrame, y_test: pd.DataFrame) -> tuple:
        feature_importance = model.feature_importances_
        feature_importance = pd.DataFrame({"Feature": self.config.features, "Importance": feature_importance})
        if self.config.calculate_permutation_importance:
            _permutation_importance = permutation_importance(model, x_test, y_test, n_repeats=self.config.n_repeats, random_state=self.config.random_state, n_jobs=self.config.n_jobs)
            _permutation_importance = pd.DataFrame({"Feature": self.config.features, "Permutation Importance": _permutation_importance.importances_mean})
        else:
            _permutation_importance = None
        return feature_importance, _permutation_importance
    
    def calculate_residuals(self, test_preds_df: pd.DataFrame, x_test: pd.DataFrame, y_test: pd.DataFrame) -> pd.DataFrame:
        test_preds_df = test_preds_df.rename(columns={col: f"Predicted_{col}" for col in test_preds_df.columns})
        residuals_df = x_test.join(test_preds_df)
        residuals_df = residuals_df.join(y_test)
        predicted_columns = [f"Predicted_{col}" for col in self.config.targets]
        for predicted_column, target_column in zip(predicted_columns, self.config.targets):
            residuals_df[f"Residual_{target_column}"] = residuals_df[target_column] - residuals_df[predicted_column]
        return residuals_df
    
    def residuals_by_group(self, residuals_df: pd.DataFrame):
        residuals_df["Distance_Bin"] = pd.cut(
            residuals_df["Distance"],
            bins=[0, 25, 50, 100, 200, 500, 1000],
            labels=["0 - 25 km", "25 - 50 km", "50 - 100 km", "100 - 200 km", "200 km - 500 km", "500 - 1000 km"]
        )
        residuals_df["Elevation_Bin"] = pd.cut(
            residuals_df["Elevation_Gain"],
            bins=[0, 500, 1000, 2000, 4000, 6000, 10000, 20000, 50000],
            labels=["0 - 500 m+", "500 - 1000 m+", "1000 - 2000 m+", "2000 - 4000 m+", "4000 - 6000 m+", "6000 - 10000 m+", "10000 - 20000 m+", "20000 - 50000 m+"]
        )
        return residuals_df

    def evaluate_model_pipeline(self, model: RandomForestRegressor, x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame) -> tuple:
        self.logger.info("Evaluating Race Outcome Engine")
        train_preds, test_preds = self.get_train_test_prediction(model=model, x_train=x_train, x_test=x_test)
        metrics = self.get_metrics(train_preds=train_preds, test_preds=test_preds, y_test=y_test, y_train=y_train)
        feature_importance, _permutation_importance = self.get_feature_importance(model=model, x_test=x_test, y_test=y_test)
        residuals_df = self.calculate_residuals(test_preds_df=test_preds, x_test=x_test, y_test=y_test)
        residuals_df = self.residuals_by_group(residuals_df=residuals_df)
        return metrics, feature_importance, _permutation_importance, residuals_df