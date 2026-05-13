import gpxpy
import gpxpy.gpx
import pandas as pd
import logging
from app.core.logger import Logger

class RouteIntelligence:
    def __init__(self):
        self.logger = Logger(name="Route Intelligence", level=logging.DEBUG).logger


    def get_basic_information(self, filepath: str):
        gpx_file = open(filepath, "r")
        gpx = gpxpy.parse(gpx_file)
        print(gpx.length_2d()) # Horizontale Strecke ohne Höhenmeter
        print(gpx.length_3d()) # Horizontale Strecke inklusive Höhenmeter
        print(gpx.get_uphill_downhill()) # Höhenmeter hoch und runter
        print(gpx.get_time_bounds()) # Start und Endzeit der Aktivität
        print(gpx.get_moving_data()) # Zeit in Bewegung in Sekunden, Zeit im Stillstand in Sekunden, Distanz während Bewegung in Metern, Distanz während Stillstand, Maximale Geschwindigkeit in Meter pro Sekunde

    def read_gpx_file(self, filepath: str) -> pd.DataFrame:
        gpx_file = open(filepath, "r")
        gpx = gpxpy.parse(gpx_file)
        gpx_points = [point for track in gpx.tracks for segment in track.segments for point in segment.points]
        data = {
            "Longitude": [point.longitude for point in gpx_points],
            "Latitude": [point.latitude for point in gpx_points],
            "Elevation": [point.elevation for point in gpx_points],
            "Time": [point.time for point in gpx_points]
        }
        df = pd.DataFrame(data)
        return df, gpx
    
    def activity_summary(self, filepath: str) -> dict:
        activity_df, gpx = self.read_gpx_file(filepath=filepath)
        min_elevation = activity_df["Elevation"].min()
        max_elevation = activity_df["Elevation"].max()
        total_elevation_gain = gpx.get_uphill_downhill()
        moving_data = gpx.get_moving_data()
        total_distance = gpx.length_2d()
        time_bounds = gpx.get_time_bounds()
        summary = {
            "min_elevation": float(min_elevation),
            "max_elevation": float(max_elevation),
            "Uphill elevation gain": total_elevation_gain.uphill,
            "Downhill elevation gain": total_elevation_gain.downhill,
            "Total moving time": moving_data.moving_time,
            "Total stopped time": moving_data.stopped_time,
            "Total moving distance": moving_data.moving_distance,
            "Total stopped distance": moving_data.stopped_distance,
            "Max speed": moving_data.max_speed,
            "Total distance": total_distance,
            "Activity start time": time_bounds.start_time,
            "Activity end time": time_bounds.end_time
        }
        return summary

ri = RouteIntelligence()
# ri.read_gpx_file(filepath="data/raw/gpx/mozart100_2026.gpx")
# ri.get_basic_information(filepath="data/raw/gpx/10k_400m.gpx")
# df = ri.read_gpx_file(filepath="data/raw/gpx/10k_400m.gpx")
print(ri.activity_summary(filepath="data/raw/gpx/10k_400m.gpx"))