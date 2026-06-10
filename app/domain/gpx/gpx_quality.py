import gpxpy
import gpxpy.gpx
import pandas as pd
import logging
from app.core.logger import Logger
from app.core.utils.gpx_utils import GpxUtils

class GPXQuality:
    def __init__(self):
        self.logger = Logger(name="GPX Quality", level=logging.INFO).logger
        self.gpx_utils = GpxUtils()

    def get_gpx_quality(self, filepath: str) -> dict:
        """
        number_of_points missing_elevation_points missing_time_points duration_available elevation_available time_available gps_sampling_rate_seconds duplicate_points
        """
        activity_df, gpx = self.gpx_utils.read_gpx_file(filepath=filepath)
        number_of_points = len(activity_df)
        missing_elevation_points = activity_df["Elevation"].isna().sum()
        missing_time_points = activity_df["Time"].isna().sum()
        duration_available = activity_df["Time"].notna().any()
        elevation_available = activity_df["Elevation"].notna().any()
        time_diffs = (activity_df["Time"].sort_values().diff().dt.total_seconds())
        gps_sampling_rate_seconds = time_diffs.median()
        duplicated_points = activity_df.duplicated(subset=["Longitude", "Latitude", "Elevation", "Time"]).sum()
        output = {
            "Number_of_points": number_of_points,
            "Missing_elevation_points": missing_elevation_points,
            "Missing_time_points": missing_time_points,
            "Duration_available": duration_available,
            "Elevation_available": elevation_available,
            "GPS_sampling_rate_seconds": gps_sampling_rate_seconds,
            "Duplicated_points": duplicated_points
        }
        return output