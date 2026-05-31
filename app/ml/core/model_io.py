import pickle

class ModelIO:
    def __init__(self):
        pass

    def load_model(self, path: str):
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model