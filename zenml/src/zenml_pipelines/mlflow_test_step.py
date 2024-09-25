# zenml_pipelines/mlflow_test_step.py

from zenml.steps import step
from sklearn.linear_model import LinearRegression
import pandas as pd
import mlflow
import mlflow.sklearn

@step
def mlflow_test_step(X_train: pd.DataFrame, y_train: pd.Series):
    """
    Train a simple model and log it to MLflow.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Log the model using MLflow
    mlflow.sklearn.log_model(model, "linear_regression_model")
    
    return model

