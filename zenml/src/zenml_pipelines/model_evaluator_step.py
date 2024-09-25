# zenml_pipelines/model_evaluator_step.py

from zenml.steps import step
from src.modeling.evaluate_models import evaluate_model
import pandas as pd
import numpy as np

@step
def model_evaluator(y_test: pd.Series, y_pred: pd.Series, model_name: str):
    """
    Evaluate model performance.
    """
    evaluate_model(y_test, y_pred, model_name)

