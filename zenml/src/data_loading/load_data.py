import geopandas as gpd

def loading_geo_data(file_path="./data/raw/HSR_KSATD2.gdb/"):
    """
    Load geospatial data from a .gdb file.

    Parameters:
    - file_path: Path to the .gdb file.

    Returns:
    - df_farms: GeoDataFrame for Farms.
    - df_property: GeoDataFrame for Property.
    - df_wells: GeoDataFrame for Wells.
    """
    layer_names = ['Farms', 'Property', 'Wells']
    df_farms = gpd.read_file(file_path, layer=layer_names[0])
    df_property = gpd.read_file(file_path, layer=layer_names[1])
    df_wells = gpd.read_file(file_path, layer=layer_names[2])
    return df_farms, df_property, df_wells
