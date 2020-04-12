import os
import sys

import numpy as np

# sys.path.append parent directory
current_dir = os.path.abspath(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# supported model types
SUPPORTED_MODEL_TYPE_LIST = ["simple"]

# some local testing X and y values
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3


class Model(object):
    def __init__(self, model_type="simple"):
        if model_type not in SUPPORTED_MODEL_TYPE_LIST:
            raise ValueError(f"Supported models: {SUPPORTED_MODEL_TYPE_LIST}")
        self.model_type = model_type
        self.model = self.initialize_model()

    def initialize_model(self):
        """
        Initialize model based on self.model_type
        
        Returns
        -------
        the {model_type}.py script
        """

        if self.model_type == "simple":
            from src import simple_model

            return simple_model

    def fit(self, X, y, verbose=False):
        """
        Fit the model.
        
        Parameters
        ----------
        X: np.ndarray
            design matrix
        y: np.ndarray
            response vector
            
        Returns
        -------
        - self.training_data: dict with X and y keys
        - self.model.fitted_model
        """
        self.training_data = {"X": X, "y": y}
        self.model.fit(self, X, y)
        self.score(verbose=verbose)

    def score(self, X=None, y=None, verbose=False):
        """ Compute R^2 of the fitted_model """
        if (X is None) & (y is None):
            X = self.training_data["X"]
            y = self.training_data["y"]

        if verbose:
            print(f"Fit R^2: {self.score()}")

        return self.model.fitted_model.score(X, y)

    def predict(self, X=None):
        """
        
        Parameters
        ----------
        X: np.ndarray (default: self.training_data["X"])
            design matrix

        Returns
        -------
        np.ndarray of preditions
        """
        if X is None:
            X = self.training_data["X"]

        self.prediction_data = {"X": X}

        return self.model.fitted_model.predict(X)
