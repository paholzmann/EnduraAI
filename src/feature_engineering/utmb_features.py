import pandas as pd

class UTMBFeatures:
    def __init__(self):
        pass

    def calculate_race_effort(self, utmb_df: pd.DataFrame) -> pd.DataFrame:
        """
        1km = 1km effort
        100m+ = 1km effort
        1km with 100m+ = 2km effort
        Example:
            100km with 6000m+ = 160km effort
        """
        utmb_df = utmb_df.copy()
        utmb_df["Race_Effort"] = utmb_df["Distance"] + (utmb_df["Elevation_Gain"] / 100)
        return utmb_df
    
