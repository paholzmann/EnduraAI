import pandas as pd
import logging

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from app.core.logger import Logger
from app.core.utils.file_utils import FileUtils
from app.ml.utils.preprocessing import Preprocessing
from app.domain.performance_metrics import Performance_Metrics

class RaceMatchingEngine:
    def __init__(self):
        self.logger = Logger(name="Race Matching Engine", level=logging.DEBUG).logger
        self.performance_metrics = Performance_Metrics()
        self.file_utils = FileUtils()
        self.preprocessing = Preprocessing()
        self.scaler = StandardScaler()

        self.train_df = None

        self.utmb_df = self.file_utils.read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-features.csv")
        self.feature_columns = ["Distance", "Elevation_Gain", "Elevation_per_km"]
        self.output_columns = ["Race_Title", "Distance", "Elevation_Gain", "Elevation_per_km"]

    def _data_split(self, df: pd.DataFrame) -> pd.DataFrame:
        X = df[self.feature_columns]
        return X
    
    def _percentage_diff(self, input_value: float, output_value: float) -> float:
        if input_value == 0:
            return None
        return abs((output_value - input_value) / input_value) * 100
    
    def _scale_data(self, X) -> pd.DataFrame:
        X_scaled = self.scaler.fit_transform(X)
        return pd.DataFrame(X_scaled, columns=self.feature_columns)
    
    def _build_model(self, top_n: int = 5, metric: str = "euclidean"):
        knn = NearestNeighbors(n_neighbors=top_n, metric=metric)
        return knn
    
    def train_pipeline(self):
        self.train_df = self.preprocessing.fill_missing(df=self.utmb_df, value=0)
        X = self._data_split(df=self.train_df)
        X_scaled = self._scale_data(X=X)
        knn = self._build_model()
        knn = knn.fit(X=X_scaled)
        return knn
    
    def explainability(self, race_input, race_output):
        distance_diff_pct = self._percentage_diff(input_value=race_input["Distance"], output_value=race_output["Distance"])
        elevation_diff_pct = self._percentage_diff(input_value=race_input["Elevation_Gain"], output_value=race_output["Elevation_Gain"])
        elevation_per_km_diff_pct = self._percentage_diff(input_value=race_input["Elevation_per_km"], output_value=race_output["Elevation_per_km"])
        return {"Distance_diff_pct": distance_diff_pct, "Elevation_diff_pct": elevation_diff_pct, "Elevation_per_km_diff_pct": elevation_per_km_diff_pct}

    def recommend_similar_races(self, query: pd.DataFrame, knn: NearestNeighbors, n_recommendations: int = 5) -> dict:
        """
        """
        query = query.copy()
        query["Elevation_per_km"] = query.apply(lambda row: self.performance_metrics.calculate_vertical_rate(distance=row["Distance"], elevation=row["Elevation_Gain"]), axis=1)
        query_scaled = self.scaler.transform(query)
        query_scaled = pd.DataFrame(query_scaled, columns=self.feature_columns)
        
        distances, indices = knn.kneighbors(X=query_scaled, n_neighbors=n_recommendations)
        results = []
        input_queries = query.to_dict(orient="records")
        for input_query, indice in zip(input_queries, indices):
            results_dict = {}
            results_dict["Results"] = {}
            results_dict["Results"]["Inputs"] = input_query
            outputs = self.train_df[self.output_columns].iloc[indice].copy()
            outputs = outputs.to_dict(orient="records")
            for output in outputs:
                output["Explainability"] = self.explainability(race_input=input_query, race_output=output)
            results_dict["Results"]["Outputs"] = outputs
            results.append(results_dict)
        return results



# engine = RaceMatchingEngine()
# knn = engine.train_pipeline()
# query = pd.DataFrame({"Distance": [1000], "Elevation_Gain": [40000]})
# results = engine.recommend_similar_races(query=query, knn=knn)
# print(results)