import gpxpy
import gpxpy.gpx
import logging
import pandas as pd
from app.core.logger import Logger

class GpxUtils:
    def __init__(self):
        self.logger = Logger(name="GPX Utilities", level=logging.DEBUG).logger

    def read_gpx_file(self, filepath: str) -> pd.DataFrame:
        gpx_file = open(filepath, "r")
        gpx = gpxpy.parse(gpx_file)
        gpx_points = [
            point for track in gpx.tracks for segment in track.segments for point in segment.points]
        data = {
            "Longitude": [point.longitude for point in gpx_points],
            "Latitude": [point.latitude for point in gpx_points],
            "Elevation": [point.elevation for point in gpx_points],
            "Time": [point.time for point in gpx_points]
        }
        df = pd.DataFrame(data)
        return df, gpx