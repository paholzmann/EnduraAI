import pandas as pd
from app.core.utils.file_utils import FileUtils
from app.ml.data.process import ProcessUTMBData

class UTMBProcessService:
    def __init__(self):
        self.utmb_processor = ProcessUTMBData()
        self.file_utilities = FileUtils()

    def run_utmb_processing_service(self, utmb_df: pd.DataFrame) -> None:
        utmb_df = self.utmb_processor.clean_raw_df(utmb_df=utmb_df, columns_to_expand=["Age", "Sex"])
        utmb_df = self.utmb_processor.result_to_minutes(utmb_df=utmb_df)
        utmb_df = self.utmb_processor.remove_str_from_numeric_col(utmb_df=utmb_df)
        utmb_df = self.utmb_processor.drop_irrelevant_columns(utmb_df=utmb_df)
        utmb_df = self.utmb_processor.parse_race_results(utmb_df=utmb_df)
        utmb_df = self.utmb_processor.grouping_races(df=utmb_df)
        utmb_df = self.file_utilities.save_df_as_csv(df=utmb_df, filepath="data/processed/utmb/utmb-race-data-processed.csv")


if __name__ == "__main__":
    utmb_df = FileUtils().read_json_as_df(json_filepath="data/raw/utmb/utmb-race-data-raw.json")
    utmb_df = UTMBProcessService().run_utmb_processing_service(utmb_df=utmb_df)