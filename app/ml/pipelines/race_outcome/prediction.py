import pandas as pd
import joblib

from app.ml.pipelines.race_outcome.config import RaceOutcomeConfig
from app.ml.core.model_io import ModelIO

class RaceOutcomePredictor:
    def __init__(self, model_path: str):
        self.config = RaceOutcomeConfig()
        self.model_io = ModelIO()
        self.model_path = model_path
        self.model = self.model_io.load_model(path=self.model_path)

    def get_prediction(self, input_df: pd.DataFrame):
        prediction = self.model.predict(input_df)[0]
        output = {
            "Winning_Time": round(prediction[0]),
            "Median_Time": round(prediction[1]),
            "Slowest_Time": round(prediction[2])
        }
        return output