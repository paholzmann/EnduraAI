import logging
import pandas as pd
from app.core.logger import Logger
from app.core.utils.gpx_utils import GpxUtils

class GPXAltitudeFeatures:
    def __init__(self):
        self.logger = Logger(name="GPX Altitude Features", level=logging.INFO).logger
        self.gpx_utils = GpxUtils()

    def calculate_basic_elevation_summary(self, df: pd.DataFrame) -> dict:
        """
        min_elevation
        max_elevation
        start_elevation
        end_elevation
        elevation_range
        """
        
        min_elevation = df["Elevation"].min()
        max_elevation = df["Elevation"].max()
        elevation_range = max_elevation - min_elevation
        start_elevation = df.loc[0, "Elevation"]
        end_elevation = df.loc[len(df) - 1, "Elevation"]

        basic_elevation_summary = {
            "Min_Elevation": float(min_elevation),
            "Max_Elevation": float(max_elevation),
            "Elevation_Range": float(elevation_range),
            "Start_Elevation": float(start_elevation),
            "End_Elevation": float(end_elevation)
        }
        return basic_elevation_summary

    def calculate_gpx_altitude_features(self, filepath: str) -> dict:
        gpx_df, _ = self.gpx_utils.read_gpx_file(filepath=filepath)
        basic_elevation_summary = self.calculate_basic_elevation_summary(df=gpx_df)
        print(basic_elevation_summary)
        gpx_altitude_features = {
            "Basic_Elevation_Summary": basic_elevation_summary
        }

if __name__ == "__main__":
    GPXAltitudeFeatures().calculate_gpx_altitude_features(filepath="data/raw/gpx/Mozart_100.gpx")