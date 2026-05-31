import pandas as pd
import numpy as np

from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, mean_absolute_error, mean_squared_error, r2_score

class RegressionModel:
    def __init__(self):
        pass

    def get_train_test_prediction(self, model, x_train: pd.DataFrame, x_test: pd.DataFrame):
        train_preds = model.predict(x_train)
        test_preds = model.predict(x_test)
        return train_preds, test_preds
    
    def get_basic_metrics(self, train_preds, test_preds, y_train: pd.DataFrame, y_test: pd.DataFrame):
        metrics = {
            "Train MAE": mean_absolute_error(y_train, train_preds),
            "Test MAE": mean_absolute_error(y_test, test_preds),
            "Train RMSE": np.sqrt(mean_squared_error(y_train, train_preds)),
            "Test RMSE": np.sqrt(mean_squared_error(y_test, test_preds)),
            "Train R2": r2_score(y_train, train_preds),
            "Test R2": r2_score(y_test, test_preds)
        }
        return metrics
    
    def create_predictions_df(self, test_preds, x_test, y_test, targets: list):
        test_preds_df = pd.DataFrame(test_preds, columns=[f"Test_Predicted_{col}" for col in targets], index=x_test.index)
        predicted_columns = [col for col in test_preds_df.columns]
        error_df = x_test.join(test_preds_df)
        error_df = error_df.join(y_test)
        return error_df, predicted_columns
    
    def calculate_residuals(self, error_df, predicted_columns: list, targets: list):
        residual_columns = []
        for target_col, predicted_col in zip(targets, predicted_columns):
            error_df[f"Residual_{target_col}"] = error_df[target_col] - error_df[predicted_col]
            residual_columns.append(f"Residual_{target_col}")
        return error_df, residual_columns
    
    def errors_by_group(self, error_df: pd.DataFrame):
        error_df["Distance_Bin"] = pd.cut(
            error_df["Distance"],
            bins=[0, 25, 50, 100, 200, 500, 1000],
            labels=["0 - 25 km", "25 - 50 km", "50 - 100 km", "100 - 200 km", "200 km - 500 km", "500 - 1000 km"]
        )
        error_df["Elevation_Bin"] = pd.cut(
            error_df["Elevation_Gain"],
            bins=[0, 500, 1000, 2000, 4000, 6000, 10000, 20000, 50000],
            labels=["0 - 500 m+", "500 - 1000 m+", "1000 - 2000 m+", "2000 - 4000 m+", "4000 - 6000 m+", "6000 - 10000 m+", "10000 - 20000 m+", "20000 - 50000 m+"]
        )
        
        return error_df