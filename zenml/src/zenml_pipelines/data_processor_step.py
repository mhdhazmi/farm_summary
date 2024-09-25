# zenml_pipelines/data_processor_step.py

from zenml.steps import step
from src.data_processing.process_data import process_farms_data, process_property_data, process_wells_data, integrate_data
import pandas as pd

@step
def data_processor(df_farms: pd.DataFrame, df_property: pd.DataFrame, df_wells: pd.DataFrame, df_visits: pd.DataFrame) -> pd.DataFrame:
    """
    Process and integrate data.
    Returns:
        df_integrated
    """
    df_farms_summary = process_farms_data(df_farms)
    df_wells_summary = process_wells_data(df_wells)
    df_property_processed = process_property_data(df_property)
    df_integrated = integrate_data(df_property_processed, df_farms_summary, df_wells_summary, df_visits)
    return df_integrated

