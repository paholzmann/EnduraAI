from haversine import haversine, Unit
import pandas as pd
import logging
from app.core.logger import Logger
from app.core.utils.gpx_utils import GpxUtils

class GPXGradientFeatures:
    def __init__(self):
        self.logger = Logger(name="GPX Gradient Features", level=logging.INFO).logger
        self.gpx_utils = GpxUtils()

    def add_distance_delta(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Prev_Longitude"] = df["Longitude"].shift(1)
        df["Prev_Latitude"] = df["Latitude"].shift(1)
        df["Distance_Delta"] = df.apply(lambda row: haversine(
            (row["Prev_Latitude"], row["Prev_Longitude"]),
            (row["Latitude"], row["Longitude"]),
            unit=Unit.METERS)
            if pd.notna(row["Prev_Latitude"])
            else 0,
            axis=1
        )
        return df
    
    def add_elevation_delta(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Prev_Elevation"] = df["Elevation"].shift(1)
        df["Elevation_Delta"] = df.apply(lambda row: (row["Elevation"] - row["Prev_Elevation"]), axis=1)
        return df
    
    def calculate_gradient(self, df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
        df["Distance_Window"] = df["Distance_Delta"].rolling(window).sum()
        df["Elevation_Window"] = df["Elevation_Delta"].rolling(window).sum()
        df["Gradient"] = (df["Elevation_Window"] / df["Distance_Window"].replace(0, pd.NA)) * 100
        df.loc[df["Distance_Window"] < 10, "Gradient"] = pd.NA
        df.loc[df["Gradient"].abs() > 60, "Gradient"] = pd.NA
        return df
    
    def calculate_max_gradient(self, df: pd.DataFrame) -> pd.DataFrame:
        return float(df["Gradient"].max())
    
    def calculate_avg_gradient(self, df: pd.DataFrame) -> float:
        return float(df["Gradient"].median())

    def build_gradient_features(self, filepath: str) -> dict:
        activity_df, gpx = self.gpx_utils.read_gpx_file(filepath=filepath)
        activity_df = self.add_distance_delta(activity_df)
        activity_df = self.add_elevation_delta(activity_df)
        activity_df = self.calculate_gradient(activity_df)
        average_gradient = self.calculate_avg_gradient(activity_df)
        max_gradient = self.calculate_max_gradient(activity_df)

        output = {
            "DataFrame": activity_df,
            "Average_Gradient": average_gradient,
            "Max_Gradient": max_gradient
        }

if __name__ == "__main__":
    GPXGradientFeatures().build_gradient_features(filepath="data/raw/gpx/Mozart_100.gpx")