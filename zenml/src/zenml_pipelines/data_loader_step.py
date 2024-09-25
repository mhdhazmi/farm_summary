# zenml_pipelines/data_loader_step.py

from zenml.steps import step
from zenml.src.data_loading.load_data import loading_geo_data

@step
def data_loader() -> tuple:
    """
    Load geospatial data.
    Returns:
        df_farms, df_property, df_wells
    """
    df_farms, df_property, df_wells = loading_geo_data()
    return df_farms, df_property, df_wells

