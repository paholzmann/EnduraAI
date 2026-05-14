import gpxpy
import gpxpy.gpx
import pandas as pd
import logging
from app.core.logger import Logger
from app.core.utils.gpx_utils import GpxUtils
from app.domain.performance_metrics import Performance_Metrics

class Activity:
    def __init__(self):
        self.logger = Logger(name="Route Intelligence", level=logging.DEBUG).logger
        self.gpx_utilities = GpxUtils()
        self.performance_metrics = Performance_Metrics()

    def activity_summary(self, filepath: str) -> dict:
        activity_df, gpx = self.gpx_utilities.read_gpx_file(filepath=filepath)
        min_elevation = activity_df["Elevation"].min()
        max_elevation = activity_df["Elevation"].max()
        total_elevation_gain = gpx.get_uphill_downhill()
        positive_elevation = total_elevation_gain.uphill
        negative_elevation = total_elevation_gain.downhill
        moving_data = gpx.get_moving_data()
        total_distance = gpx.length_2d() / 1000
        time_bounds = gpx.get_time_bounds()
        moving_minutes = moving_data.moving_time / 60
        stopped_minutes = moving_data.stopped_time / 60
        total_minutes = moving_minutes + stopped_minutes
        total_hours = total_minutes / 60

        race_effort = self.performance_metrics.calculate_race_effort(distance=total_distance, elevation=total_elevation_gain.uphill)
        pace = self.performance_metrics.calculate_pace(distance=total_distance, total_minutes=total_minutes)
        sat = self.performance_metrics.calculate_estimated_pace_on_flat_equivalent(total_time=total_minutes, race_effort=race_effort)
        vertical_rate = self.performance_metrics.calculate_vertical_rate(distance=total_distance, elevation=positive_elevation)
        vertical_per_hour = self.performance_metrics.calculate_vertical_per_hour(total_hours=total_hours, elevation_gain=positive_elevation)
        category_label = self.performance_metrics.generate_category_label(distance=total_distance, elevation=positive_elevation)
        summary = {
            "Min elevation": float(min_elevation),
            "Max elevation": float(max_elevation),
            "Uphill elevation gain": positive_elevation,
            "Downhill elevation gain": negative_elevation,

            "Total moving time": moving_minutes,
            "Total stopped time": stopped_minutes,
            "Total time": total_minutes,
            "Activity start time": time_bounds.start_time,
            "Activity end time": time_bounds.end_time,

            "Total moving distance": moving_data.moving_distance / 1000,
            "Total stopped distance": moving_data.stopped_distance / 1000,
            "Total distance": total_distance,

            "Race effort": race_effort,
            "Pace": pace,
            "SAT": sat,
            "Vertical rate": vertical_rate,
            "Vertical per hour": vertical_per_hour,
            "Category label": category_label,

            "Max speed": moving_data.max_speed
        }
        return summary