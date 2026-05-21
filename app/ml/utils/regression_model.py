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
        print(targets)
        print(predicted_columns)
        for target_col, predicted_col in zip(targets, predicted_columns):
            error_df[f"Residual_{target_col}"] = error_df[target_col] - error_df[predicted_col]
        return error_df