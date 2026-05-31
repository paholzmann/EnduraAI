import pandas as pd
import logging

from app.core.logger import Logger
from app.ml.pipelines.race_outcome.config import RaceOutcomeConfig

from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestRegressor

class TrainRaceOutcome:
    def __init__(self):
        self.logger = Logger(name="Race Outcome Pipeline", level=logging.INFO, log_file="app/logs/ml/race_outcome/race_outcome_pipeline.log").logger
        self.config = RaceOutcomeConfig()
    
    def train_model(self, df: pd.DataFrame) -> tuple[RandomForestRegressor, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        self.logger.info("Training Race Outcome Engine")
        X = df[self.config.features]
        y = df[self.config.targets]
        group_splitter = GroupShuffleSplit(n_splits=self.config.n_splits, test_size=self.config.test_size, random_state=self.config.random_state)
        train_index, test_index = next(group_splitter.split(X, y, df[self.config.group_column].astype(str)))
        x_train, x_test, y_train, y_test = X.iloc[train_index], X.iloc[test_index], y.iloc[train_index], y.iloc[test_index]

        random_forest_regressor = RandomForestRegressor(n_estimators=self.config.n_estimators, random_state=self.config.random_state, n_jobs=self.config.n_jobs)
        random_forest_regressor.fit(x_train, y_train)
        return random_forest_regressor, x_train, x_test, y_train, y_test