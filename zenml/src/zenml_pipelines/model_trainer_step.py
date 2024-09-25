# zenml_pipelines/model_trainer_step.py

from zenml.steps import step
from src.modeling.train_models import train_and_log_model, train_and_log_stacking
from src.utils.helpers import OutlierCapper
import pandas as pd
import numpy as np

@step
def model_trainer(df_integrated: pd.DataFrame) -> tuple:
    """
    Train models and log them using MLflow.
    Returns:
        best_estimators for stacking
    """
    # Your existing training code here, adapted to ZenML steps
    # For brevity, this is a placeholder
    pass

