import pandas as pd
import logging
from app.core.logger import Logger

class FileHandler:
    def __init__(self):
        self.logger = Logger(name="File Handler", level=logging.DEBUG).logger
    
    def read_json_as_df(self, json_filepath: str) -> pd.DataFrame:
        self.logger.debug(f"Reading json file {json_filepath} as pd.DataFrame")
        df = pd.read_json(json_filepath)
        return df
    
    def read_csv_as_df(self, csv_path: str) -> pd.DataFrame:
        self.logger.debug(f"Reading csv file {csv_path} as pd.DataFrame")
        df = pd.read_csv(csv_path)
        return df
    
    def save_df_as_csv(self, df: pd.DataFrame, filepath: str) -> None:
        self.logger.debug(f"Saving DataFrame in {filepath}")
        try:
            df.to_csv(filepath, index=False)
        except FileNotFoundError:
            self.logger.error(f"Invalid path: {filepath}")