import pandas as pd
from sklearn.model_selection import train_test_split

class DataSplitter():
    def __init__(self):
        pass

    def split_data(self, df: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
        X = df[feature_columns]
        return X

    def train_test_split(self, df: pd.DataFrame, features: list, targets: list):
        X = df[features]
        y = df[targets]
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return x_train, x_test, y_train, y_test
