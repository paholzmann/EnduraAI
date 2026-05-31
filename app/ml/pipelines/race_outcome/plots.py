import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from app.ml.pipelines.race_outcome.config import RaceOutcomeConfig
from app.ml.core.experiment_tracker import ExperimentTracker


class PlotRaceOutcome:
    def __init__(self, experiment_tracker: ExperimentTracker):
        self.config = RaceOutcomeConfig()
        self.experiment_tracker = experiment_tracker

        sns.set_theme(
            style="whitegrid",
            context="talk",
            palette="deep"
        )

        plt.rcParams.update({
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titleweight": "bold",
            "axes.labelweight": "bold",
            "legend.frameon": False
        })

    def prediction_vs_actual(self, df: pd.DataFrame) -> None:
        predicted_columns = [col for col in df.columns if "Predicted" in col]
        for target_column, predicted_column in zip(self.config.targets, predicted_columns):
            plt.figure(figsize=(8, 5))
            plt.scatter(df[target_column], df[predicted_column], alpha=0.65)
            min_val = min(df[target_column].min(), df[predicted_column].min())
            max_val = max(df[target_column].max(), df[predicted_column].max())
            plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")
            plt.title(f"Predicted vs. Actual value for {target_column}")
            plt.xlabel("Predicted value")
            plt.ylabel("Actual value")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            save_path = self.experiment_tracker.plots_path / f"prediction_vs_actual_{target_column}.png"
            plt.savefig(save_path, bbox_inches="tight")

    def plot_residuals_distribution(self, df: pd.DataFrame) -> None:
        residual_columns = [col for col in df.columns if "Residual" in col]
        for residual_column in residual_columns:
            plt.figure(figsize=(8, 5))
            plt.hist(df[residual_column], bins=35, alpha=0.8)
            plt.axvline(0, linestyle="--")
            plt.title(f"Residuals distribution for {residual_column}")
            plt.xlabel("Residual")
            plt.ylabel("Count")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            save_path = self.experiment_tracker.plots_path / f"residuals_distribution_{residual_column}.png"
            plt.savefig(save_path, bbox_inches="tight")

    def plot_residual_vs_prediction(self, df: pd.DataFrame) -> None:
        residual_columns = [col for col in df.columns if "Residual" in col]
        predicted_columns = [col for col in df.columns if "Predicted" in col]
        for residual_column, predicted_column in zip(residual_columns, predicted_columns):
            plt.figure(figsize=(8, 5))
            plt.scatter(df[predicted_column], df[residual_column], alpha=0.65)
            plt.axhline(0, linestyle="--")
            plt.title("Residual vs. Prediction")
            plt.xlabel("Prediction")
            plt.ylabel("Residual")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            save_path = self.experiment_tracker.plots_path / f"residual_vs_prediction_{residual_column}.png"
            plt.savefig(save_path, bbox_inches="tight")

    def plot_residual_vs_feature(self, df: pd.DataFrame) -> None:
        residual_columns = [col for col in df.columns if "Residual" in col]
        for residual_column in residual_columns:
            for feature_column in self.config.features:
                plt.figure(figsize=(8, 5))
                plt.scatter(df[feature_column], df[residual_column], alpha=0.65)
                plt.axhline(0, linestyle="--")
                plt.title("Residual vs. Feature")
                plt.xlabel("Feature")
                plt.ylabel("Residual")
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                save_path = self.experiment_tracker.plots_path / f"residual_vs_{feature_column}.png"
                plt.savefig(save_path, bbox_inches="tight")

    def plot_feature_importances(self, feature_importance: pd.DataFrame) -> None:
        plt.figure(figsize=(8, 5))
        plt.bar(feature_importance["Feature"], feature_importance["Importance"])
        plt.title("Feature vs. Feature importance")
        plt.xlabel("Feature")
        plt.ylabel("Importance")
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        save_path = self.experiment_tracker.plots_path / f"feature_importance.png"
        plt.savefig(save_path, bbox_inches="tight")

    def plot_mean_residual_by_group(self, df: pd.DataFrame) -> None:
        residual_columns = [col for col in df.columns if "Residual" in col]
        bin_columns = [col for col in df.columns if "Bin" in col]
        for residual_column in residual_columns:
            for bin_column in bin_columns:
                results = df.groupby(bin_column)[residual_column].mean()
                results = results.reset_index()
                plt.figure(figsize=(8, 5))
                plt.bar(results[bin_column], results[residual_column])
                plt.title("Residuals by group")
                plt.xlabel("Group")
                plt.ylabel("Residual")
                plt.xticks(rotation=45)
                plt.tight_layout()
                save_path = self.experiment_tracker.plots_path / f"{residual_column}_by_{bin_column}.png"
                plt.savefig(save_path, bbox_inches="tight")

    def plot_all(self, df: pd.DataFrame, feature_importance: list) -> None:
        self.prediction_vs_actual(df=df)
        self.plot_residuals_distribution(df=df)
        self.plot_residual_vs_prediction(df=df)
        self.plot_feature_importances(feature_importance=feature_importance)
        self.plot_mean_residual_by_group(df=df)