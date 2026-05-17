import numpy as np


class Similarity:
    def __init__(self):
        pass

    def euclidean_distance(self, a: list, b: list) -> float:
        a, b = np.array(a), np.array(b)
        return np.sqrt(np.sum((a - b) ** 2))

    def manhatten_distance(self, a: list, b: list) -> float:
        a, b = np.array(a), np.array(b)
        return np.sum(np.abs(a - b))
    
    def cosine_similarity(self, a: list, b: list) -> float:
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))