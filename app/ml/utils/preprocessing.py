import pandas as pd
import numpy as np

class Preprocessing:
    def __init__(self):
        pass

    def fill_missing(self, df: pd.DataFrame, value: float | str) -> pd.DataFrame:
        return df.fillna(value)