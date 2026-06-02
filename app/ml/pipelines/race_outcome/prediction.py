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
        prediction = self.model.predict(input)[0]
        output = {
            "Winning_Time": round(prediction[0]),
            "Median_Time": round(prediction[1]),
            "Slowest_Time": round(prediction[2])
        }
        return output


# model_path = "reports/race_outcome/2026-05-31_20-02-35/model.pkl"
# distance = 16.9
# elevation_gain = 790
# elevation_per_km = 790 / 16.9
# race_effort = 16.9 + (790 / 100)
# effort_per_km = race_effort / distance
# n_results = 200
# df = pd.DataFrame({"Distance": [distance], "Elevation_Gain": [elevation_gain], "Elevation_per_km": [elevation_per_km], "Race_Effort": [race_effort], "Effort_per_km": [effort_per_km], "N_Results": [n_results]})
# output = RaceOutcomePredictor(model_path).get_prediction(input_df=df)
# print(output)