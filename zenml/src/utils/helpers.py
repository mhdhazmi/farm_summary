# src/utils/helpers.py

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierCapper(BaseEstimator, TransformerMixin):
    def __init__(self, variables=None, factor=1.5):
        """
        Cap the outliers in specified variables using the IQR method.

        Parameters:
        - variables: list of column names to apply capping.
        - factor: multiplier for the IQR to define the cap.
        """
        self.variables = variables
        self.factor = factor

    def fit(self, X, y=None):
        self.cap_dict_ = {}
        for var in self.variables:
            Q1 = X[var].quantile(0.25)
            Q3 = X[var].quantile(0.75)
            IQR = Q3 - Q1
            lower_cap = Q1 - self.factor * IQR
            upper_cap = Q3 + self.factor * IQR
            self.cap_dict_[var] = (lower_cap, upper_cap)
        return self

    def transform(self, X):
        X_capped = X.copy()
        for var in self.variables:
            lower_cap, upper_cap = self.cap_dict_[var]
            X_capped[var] = np.where(
                X_capped[var] < lower_cap, lower_cap,
                np.where(X_capped[var] > upper_cap, upper_cap, X_capped[var])
            )
        return X_capped

