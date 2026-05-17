import numpy as np
import pandas as pd

class Scaler:
    def __init__(self):
        pass

    def min_max_scaler(self, series: pd.Series) -> pd.Series:
        return (series - series.min()) / (series.max() - series.min())
    
    def z_score(self, series: pd.Series) -> pd.Series:
        return (series - series.mean()) / series.std(ddof=0)