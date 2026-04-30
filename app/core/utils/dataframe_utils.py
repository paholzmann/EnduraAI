import pandas as pd
import logging
from app.core.logger import Logger

class DataFrameUtils():
    def __init__(self):
        self.logger = Logger(name="DataFrame Utilities", level=logging.DEBUG).logger

    def df_to_dict(self, df: pd.DataFrame) -> dict:
        """
        
        """
        return df.to_dict(orient="records")
    
    def columns_to_keep(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        """
        
        """
        return df[cols]