import pandas as pd
import logging

from app.core.logger import Logger
from app.core.utils.file_utils import FileUtils
from app.ml.core.experiment_tracker import ExperimentTracker
from app.ml.pipelines.race_outcome.config import RaceOutcomeConfig
from app.ml.pipelines.race_outcome.train import TrainRaceOutcome
from app.ml.pipelines.race_outcome.preprocessing import Preprocessing
from app.ml.pipelines.race_outcome.evaluation import EvaluateRaceOutcome
from app.ml.pipelines.race_outcome.plots import PlotRaceOutcome

class RaceOutcomePipeline:
    def __init__(self):
        self.logger = Logger(name="Race Outcome Pipeline", level=logging.INFO, log_file="app/logs/ml/race_outcome/race_outcome_pipeline.log").logger
        self.file_utils = FileUtils()
        self.experiment_tracker = ExperimentTracker(pipeline_name="race_outcome")
        self.config = RaceOutcomeConfig()
        self.config_data = self.config.save_config_data()
        self.train_race_outcome = TrainRaceOutcome()
        self.preprocessing = Preprocessing()
        self.evaluation = EvaluateRaceOutcome()
        self.plot = PlotRaceOutcome(experiment_tracker=self.experiment_tracker)

        self.df = self.file_utils.read_csv_as_df(csv_path=self.config.data_path)

    def run_pipeline(self):
        self.experiment_tracker.create_run_folders()
        self.logger.info("Starting Race Outcome Pipeline")
        check_missing_columns = self.config.features + self.config.targets + [self.config.group_column]
        df = self.preprocessing.drop_missing(df=self.df, columns=check_missing_columns)
        random_forest_regressor, x_train, x_test, y_train, y_test = self.train_race_outcome.train_model(df=df)
        metrics, feature_importance, _permutation_importance, residuals_df = self.evaluation.evaluate_model_pipeline(random_forest_regressor, x_train, x_test, y_train, y_test)
        self.experiment_tracker.save_metrics(metrics=metrics)
        self.experiment_tracker.save_config(config=self.config_data)
        self.experiment_tracker.save_feature_importance(feature_importance=feature_importance)
        if self.config.calculate_permutation_importance:
            self.experiment_tracker.save_permutation_importance(permutation_importance=_permutation_importance)
        self.experiment_tracker.save_model(model=random_forest_regressor)
        self.plot.plot_all(df=residuals_df, feature_importance=feature_importance)

if __name__ == "__main__":
    RaceOutcomePipeline().run_pipeline()