import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



class Plots:
    def __init__(self):
        pass

    def prediction_vs_actual(self, y_pred, y_true, title: str = "Test", x_label: str = "Predicted value", y_label: str = "Actual value") -> None:
        plt.figure(figsize=(8, 6))
        plt.scatter(y_true, y_pred, alpha=0.65)
        # min_val = min(y_true.min(), y_pred.min())
        # max_val = max(y_true.max(), y_pred.max())
        # plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")
        plt.grid(True, alpha=0.3)
        plt.show()
