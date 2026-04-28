import pandas as pd
import logging
from app.core.logger import Logger
from app.core.utils.file_utils import FileUtils
from app.domain.features.utmb_features import UTMBFeatures
from app.services.utmb.process import ProcessUTMBData

class UTMBFeatureService:
    def __init__(self):
        self.logger = Logger(name="UTMB Feature Service", level=logging.DEBUG).logger
        self.utmb_features = UTMBFeatures()
        self.file_utilities = FileUtils()

    def run_utmb_feature_service(self, utmb_df: pd.DataFrame) -> None:
        self.logger.debug("Running UTMB Feature Service")
        utmb_df = utmb_df.copy()
        utmb_df = self.utmb_features.calculate_race_effort(utmb_df=utmb_df)
        utmb_df = self.utmb_features.calculate_race_result_features(utmb_df=utmb_df)
        utmb_df = self.utmb_features.calculate_normalized_features(utmb_df=utmb_df)
        utmb_df = self.utmb_features.calculate_competition_features(utmb_df=utmb_df)
        utmb_df = self.utmb_features.calculate_difficulty_features(utmb_df=utmb_df)
        self.file_utilities.save_df_as_csv(df=utmb_df, filepath="data/processed/utmb/utmb-race-data-features.csv")

utmb_df = FileUtils().read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-processed.csv")
utmb_df = ProcessUTMBData().parse_race_results(utmb_df=utmb_df)
UTMBFeatureService().run_utmb_feature_service(utmb_df=utmb_df)