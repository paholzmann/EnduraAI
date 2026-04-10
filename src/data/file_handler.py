import pandas as pd
import os
import json

class FileHandler:
    def __init__(self):
        pass

    def read_json_as_df(self, json_filepath: str) -> pd.DataFrame:
        df = pd.read_json(json_filepath)
        return df