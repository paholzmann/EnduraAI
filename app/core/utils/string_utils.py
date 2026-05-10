import pandas as pd
import re
import logging
from app.core.logger import Logger

class StringUtils:
    def __init__(self):
        self.logger = Logger(name="String Utilities", level=logging.DEBUG).logger

    def lowercase(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        """
        
        """
        self.logger.debug(f"Lowercasing column {col} in pd.DataFrame")
        df[f"{col}_Processed"] = df[col].str.lower()
        return df
    
    def remove_years(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        """
        
        """
        self.logger.debug(f"Removing years from column {col} in pd.DataFrame")
        def remove_year(text: str) -> str:
            if pd.isna(text):
                return text
            text = re.sub(r"\b\d{4}\b", "", text).strip()
            return text
        
        df[col] = df[col].apply(remove_year)
        return df