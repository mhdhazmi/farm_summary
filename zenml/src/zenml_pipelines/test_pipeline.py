# zenml_pipelines/test_pipeline.py

from zenml.pipelines import pipeline
from zenml_pipelines.mlflow_test_step import mlflow_test_step

@pipeline
def test_mlflow_pipeline(
    test_step=mlflow_test_step
):
    model = test_step(X_train, y_train)

