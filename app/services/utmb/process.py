import pandas as pd
import ast
import re
import logging
from app.core.logger import Logger
from app.core.utils.file_utils import FileUtils

class ProcessUTMBData:
    def __init__(self):
        self.logger = Logger(name="Process UTMB Data", level=logging.DEBUG).logger
        self.file_utilities = FileUtils()
    
    def clean_raw_df(self, utmb_df: pd.DataFrame, columns_to_expand: list = []) -> pd.DataFrame:
        self.logger.debug(f"Cleaning raw DataFrame and expanding columns: {columns_to_expand}")
        utmb_df = utmb_df.T
        utmb_df = utmb_df.rename(columns={"City / Country": "Race_Country", "Elevation Gain": "Elevation_Gain", "N Results": "N_Results", "Race Category": "Race_Category", "Race Title": "Race_Title"})
        for col in columns_to_expand:
            expanded_df = utmb_df[col].apply(pd.Series)
            expanded_df.columns = [f"{col}_{str(subcol).strip().replace(' ', '_')}" for subcol in expanded_df.columns]
            utmb_df = pd.concat([utmb_df, expanded_df], axis=1)
            utmb_df = utmb_df.drop(columns=[col])
        return utmb_df
    
    def result_to_minutes(self, utmb_df: pd.DataFrame) -> pd.DataFrame:
        self.logger.debug("Converting results in hours to minutes")
        utmb_df = utmb_df.copy()
        utmb_df["Results"] = utmb_df["Results"].apply(lambda results: [x * 60 for x in results])
        return utmb_df

    def remove_str_from_numeric_col(self, utmb_df: pd.DataFrame, columns: list = ["Distance", "Elevation_Gain"]) -> pd.DataFrame:
        self.logger.debug(f"Removing strings from numeric columns: {columns}")
        def extract_number(val):
            if pd.isna(val):
                return None
            match = re.findall(r"\d+\.?\d*", str(val))
            return float(match[0]) if match else None
        for col in columns:
            utmb_df[col] = utmb_df[col].apply(extract_number)
        return utmb_df
    
    def drop_irrelevant_columns(self, utmb_df: pd.DataFrame, columns_to_drop: list = ["Country"]) -> pd.DataFrame:
        self.logger.debug(f"Dropping irrelevant columns from DataFrame: {columns_to_drop}")
        utmb_df = utmb_df.copy()
        utmb_df = utmb_df.drop(columns=columns_to_drop)
        return utmb_df
    
    def parse_race_results(self, utmb_df: pd.DataFrame) -> pd.DataFrame:
        self.logger.debug("Parsing race results from DataFrame")
        utmb_df = utmb_df.copy()
        def parse_results(value):
            if isinstance(value, list):
                return value
            if pd.isna(value):
                return []
            if isinstance(value, str):
                return ast.literal_eval(value)
            return value
        utmb_df["Results"] = utmb_df["Results"].apply(parse_results)
        return utmb_df

    def processing_pipeline(self, utmb_df: pd.DataFrame) -> None:
        self.logger.debug("Starting processing pipeline")
        utmb_df = self.clean_raw_df(utmb_df=utmb_df, columns_to_expand=["Age", "Sex"])
        utmb_df = self.result_to_minutes(utmb_df=utmb_df)
        utmb_df = self.remove_str_from_numeric_col(utmb_df=utmb_df)
        utmb_df = self.drop_irrelevant_columns(utmb_df=utmb_df)
        utmb_df = self.parse_race_results(utmb_df=utmb_df)
        utmb_df = self.file_utilities.save_df_as_csv(df=utmb_df, filepath="data/processed/utmb/utmb-race-data-processed.csv")


if __name__ == "__main__":
    utmb_df = FileUtils().read_json_as_df(json_filepath="data/raw/utmb/utmb-race-data-raw.json")
    ProcessUTMBData().processing_pipeline(utmb_df=utmb_df)