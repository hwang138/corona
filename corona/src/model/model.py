import os
import sys

current_dir = os.path.abspath(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
SUPPORTED_MODELS = ["simple"]

class Model(object):
    def __init__(self, model_type="simple"):
        if model_type not in SUPPORTED_MODELS:
            raise ValueError(f"Supported models: {SUPPORTED_MODELS}")
        self.model_type = model_type
        self.model = self.initialize_model()

    def initialize_model(self):

        if self.model_type == "simple":
            from src import simple_model
            return simple_model

    def fit_model(self, X, y):
        self.training_data = {"X": X, "y": y}
        self.model.fit_model(X=X, y=y)

    def predict(self, X=None):
        if X is None:
            X = self.training_data["X"]

        self.prediction_data = {"X": X}

        self.model.predict(X=X)