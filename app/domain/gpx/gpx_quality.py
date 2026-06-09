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

    def get_gpx_quality(self, filepath: str):
        activity_df, gpx = self.gpx_utils.read_gpx_file(filepath=filepath)
        print(activity_df)
        print(gpx)

if __name__ == "__main__":
    GPXQuality().get_gpx_quality(filepath="data/raw/gpx/Mozart_100.gpx")