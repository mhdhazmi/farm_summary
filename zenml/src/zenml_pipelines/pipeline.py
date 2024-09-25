# src/zenml_pipelines/pipeline.py
from zenml.pipelines import pipeline
from zenml_pipelines.data_loader_step import data_loader
from zenml_pipelines.data_processor_step import data_processor
from zenml_pipelines.model_trainer_step import model_trainer
from zenml_pipelines.model_evaluator_step import model_evaluator

@pipeline
def farms_load_estimation_pipeline(
    loader=data_loader,
    processor=data_processor,
    trainer=model_trainer,
    evaluator=model_evaluator
):
    df_farms, df_property, df_wells = loader()
    df_integrated = processor(df_farms, df_property, df_wells, df_visits)  # Ensure df_visits is provided
    best_estimators = trainer(df_integrated)
    # Add evaluation steps as needed
    evaluator(y_test, y_pred, model_name="Best_Model")
