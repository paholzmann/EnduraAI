import gpxpy
import gpxpy.gpx
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
    
    def calculate_gradient(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Gradient"] = (df["Elevation_Delta"] / df["Distance_Delta"].replace(0, pd.NA)) * 100
        return df
    
    def calculate_max_gradient(self, df: pd.DataFrame) -> pd.DataFrame:
        return float(df["Gradient"].max())
    
    def calculate_avg_gradient(self, df: pd.DataFrame) -> float:
        average_gradient = df["Gradient"].median()
        return average_gradient

    def build_gradient_features(self, filepath: str) -> dict:
        activity_df, gpx = self.gpx_utils.read_gpx_file(filepath=filepath)
        activity_df = self.add_distance_delta(activity_df)
        activity_df = self.add_elevation_delta(activity_df)
        activity_df = self.calculate_gradient(activity_df)
        average_gradient = self.calculate_avg_gradient(activity_df)
        print(average_gradient)
        print(activity_df)


if __name__ == "__main__":
    GPXGradientFeatures().build_gradient_features(filepath="data/raw/gpx/Mozart_100.gpx")