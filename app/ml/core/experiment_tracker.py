import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import pickle

class ExperimentTracker:
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        self.base_path = (
            Path("reports")
            / pipeline_name
            / self.run_id
        )

        self.plots_path = self.base_path / "plots"
        self.metrics_path = self.base_path / "metrics.json"
        self.config_path = self.base_path / "config.json"
        self.feature_importance_path = self.base_path / "feature_importance.csv"
        self.permutation_importance_path = self.base_path / "permutation_importance.csv"
        self.model_path = self.base_path / "model.pkl"

    def create_run_folders(self):
        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.plots_path.mkdir(
            exist_ok=True
        )

        return self.base_path
    
    def save_metrics(self, metrics: dict):
        with open(self.metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)

    def save_config(self, config: dict):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

    def save_feature_importance(self, feature_importance: pd.DataFrame) -> None:
        feature_importance.to_csv(self.feature_importance_path, index=False)
    
    def save_permutation_importance(self, permutation_importance: pd.DataFrame) -> None:
        permutation_importance.to_csv(self.permutation_importance_path, index=False)

    def save_model(self, model) -> None:
        with open(self.model_path, "wb") as f:
            pickle.dump(model, f)