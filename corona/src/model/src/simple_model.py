from sklearn.linear_model import LinearRegression


def fit(model_class, X, y):
    """
    Fit a linear regression model

    Parameters
    ----------
    model_class: obj
    X: np.ndarray
        design matrix
    y: np.ndarray
        response vector
    Returns
    -------
    model_class.model.fitted_model
    """
    model_class.model.fitted_model = LinearRegression().fit(X=X, y=y)


def predict(model_class, X):
    """
    Make prediction

    Parameters
    ----------
    model_class: obj
    X: np.ndarray
        design matrix

    Returns
    -------
    np.ndarray of predicion values
    """
    return model_class.model.fitted_model.predict(X=X)
