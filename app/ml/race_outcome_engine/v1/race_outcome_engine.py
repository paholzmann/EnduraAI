import pandas as pd
import logging

from app.core.utils.file_utils import FileUtils
from app.ml.utils.preprocessing import Preprocessing
from app.ml.utils.data_splitter import DataSplitter


class RaceOutcomeEngine:
    def __init__(self):
        self.file_utils = FileUtils()
        self.preprocessing = Preprocessing()
        self.data_splitter = DataSplitter()

        
        self.utmb_df = self.file_utils.read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-features.csv")

        self.train_df = self.preprocessing.fill_missing(df=self.utmb_df, value=0)

        self.features = ["Distance", "Elevation_Gain", "Elevation_per_km", "Race_Effort"]
        self.targets = ["Winning_Time", "Median_Time", "Slowest_Time"]
        self.output_columns = ["Race_Title"]

    def train_pipeline(self):
        x_train, x_test, y_train, y_test = self.data_splitter.train_test_split(df=self.utmb_df, features=self.features, targets=self.targets)

engine = RaceOutcomeEngine()
engine.train_pipeline()