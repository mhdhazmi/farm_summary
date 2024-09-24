# GOAL
I am developing a model that estimates the consumption of the farms based on available data. I have HASAR data as the input and the prediction is in visits data (total_electrical_load). Your goal is to improve the performance of the model we have currently 
You can also highlight issues that I have in the code but I would like you to focus on major issues only such as data leak from visits data and so on
# Code

## Cell 1 
<code>

def loading_geo_data():
    import geopandas as gpd
    import fiona
    import pandas as pd
    pd.options.display.max_columns = 100
    # Path to your .gdb file
    file_path = "./HSR_KSATD2.gdb/"

    # List all layers in the .gdb file
    layers = fiona.listlayers(file_path)
    for layer in layers:
        pass

    # Specify the layer name you're interested in
    layer_name = 'Farms'

    # Read the layer into a GeoDataFrame
    df_farms = gpd.read_file(file_path, layer=layer_name)
    layer_name = 'Property'
    df_property = gpd.read_file(file_path, layer=layer_name)
    layer_name = 'Wells'

    # Read the layer into a GeoDataFrame
    df_wells = gpd.read_file(file_path, layer=layer_name)
    return df_farms, df_property, df_wells


df_farms, df_property, df_wells = loading_geo_data()
</code>

## Cell 1 Output

## Cell 2 
<code>
# Updated code to handle well_is_active column more robustly

import pandas as pd
import geopandas as gpd

# Assuming df_wells is your GeoDataFrame
# If it's not, convert it first:
# df_wells = gpd.GeoDataFrame(df_wells, geometry='geometry')

# 1. Consistent and clear naming
df_wells = df_wells.rename(
    columns={
        "HSRCode": "well_id",
        "OB_HSRCode": "farm_id",
        "PossessionType": "well_possession_type",
        "IsActive": "well_is_active",
        "IrragationSource": "well_irrigation_source",
        "IrrigationType": "well_irrigation_type",
        "X": "well_longitude",
        "Y": "well_latitude",
        "Region": "well_region",
    }
)



# 3. More nuanced handling of missing and unexpected values
def clean_active_status(value):
    if pd.isna(value) or value == 0:  # Treat 0 as missing data
        return 1  # Assume active if not specified, you may want to change this based on domain knowledge
    elif value in [1, 2]:
        return value
    else:
        print(f"Unexpected value in well_is_active: {value}")
        return 1  # Default to active for unexpected values, adjust as needed

df_wells['well_is_active'] = df_wells['well_is_active'].apply(clean_active_status)

# 4. General function for handling missing values in other columns
def fill_missing(series):
    if pd.api.types.is_numeric_dtype(series):
        return series.fillna(series.median())
    elif pd.api.types.is_object_dtype(series):
        return series.fillna(series.mode()[0] if not series.mode().empty else 'Unknown')
    else:
        return series  # Return as-is for other types (including geometry)

# Apply fill_missing to all columns except the geometry and well_is_active columns
for col in df_wells.columns:
    if col not in [df_wells.geometry.name, 'well_is_active']:
        df_wells[col] = fill_missing(df_wells[col])

# 5. Preserve geographical information
geo_columns = ['well_longitude', 'well_latitude', 'well_region']

# 6. Add data validation
assert df_wells['well_id'].nunique() == len(df_wells), "Duplicate well IDs found"
assert df_wells['well_is_active'].isin([1, 2]).all(), "Invalid values in well_is_active after cleaning"

# 7. Use pandas categorical type for efficiency
categorical_columns = ['well_possession_type', 'well_is_active', 'well_irrigation_source', 'well_irrigation_type']
for col in categorical_columns:
    df_wells[col] = df_wells[col].astype('category')
    df_wells[col] = df_wells[col].replace(0,df_wells[col].mode()[0]).astype('category')

# 8. More flexible aggregation function
def aggregate_wells(group):
    agg_dict = {
        'well_id': 'count',
        'well_is_active': lambda x: (x == 1).sum(),
        'well_irrigation_source': lambda x: x.value_counts().to_dict(),
        'well_irrigation_type': lambda x: x.value_counts().to_dict(),
    }
    return pd.Series(group.agg(agg_dict))

# Apply the aggregation
df_wells_summary = df_wells.groupby("farm_id").apply(aggregate_wells).reset_index()

# Function to flatten dictionary columns
def flatten_dict_column(df, column_name):
    # Get all unique keys from all dictionaries in the column
    all_keys = set()
    for d in df[column_name]:
        all_keys.update(d.keys())
    
    # Create new columns for each key
    for key in all_keys:
        df[f'{column_name}_{key}'] = df[column_name].apply(lambda d: d.get(key, 0))
    
    # Drop the original dictionary column
    df = df.drop(columns=[column_name])
    return df

# Flatten the dictionary columns
df_wells_summary = flatten_dict_column(df_wells_summary, 'well_irrigation_source')
df_wells_summary = flatten_dict_column(df_wells_summary, 'well_irrigation_type')

# Calculate percentages for irrigation sources and types
well_count = df_wells_summary['well_id']
for col in df_wells_summary.columns:
    if col.startswith('well_irrigation_source_') or col.startswith('well_irrigation_type_'):
        df_wells_summary[f'{col}_percentage'] = df_wells_summary[col] / well_count

# Calculate percentage of active wells
df_wells_summary['active_wells_percentage'] = df_wells_summary['well_is_active'] / df_wells_summary['well_id']

# Remove geographical columns if they exist
columns_to_drop = ['well_longitude', 'well_latitude', 'well_region']
df_wells_summary = df_wells_summary.drop(columns=[col for col in columns_to_drop if col in df_wells_summary.columns])

# 9. Add documentation
"""
This script processes well data, performing the following steps:
1. Renames columns for clarity
2. Examines and cleans the well_is_active column
3. Handles missing values in other columns
4. Validates data integrity
5. Optimizes data types
6. Aggregates data at the farm level, including:
   - Count of wells
   - Count and percentage of active wells
   - Flattened counts and percentages for irrigation sources and types
7. Removes geographical information

Input: GeoDataFrame with individual well data
Output: DataFrame with farm-level well summaries
"""


# Most common irrigation source and type
most_common_source = df_wells_summary[[col for col in df_wells_summary.columns if col.startswith('well_irrigation_source_') and not col.endswith('_percentage')]].sum().idxmax()
most_common_type = df_wells_summary[[col for col in df_wells_summary.columns if col.startswith('well_irrigation_type_') and not col.endswith('_percentage')]].sum().idxmax()


df_wells_summary['sprinklers_count'] = df_wells_summary['well_id']
df_wells_summary['sprinklers_count_kw'] = df_wells_summary['well_id'] * 25


df_wells_summary.head()
</code>

## Cell 2 Output
	farm_id	well_id	well_is_active	well_irrigation_source_1	well_irrigation_source_2	well_irrigation_source_4	well_irrigation_source_5	well_irrigation_source_6	well_irrigation_source_10	well_irrigation_source_12	well_irrigation_type_1.0	well_irrigation_type_2.0	well_irrigation_type_3.0	well_irrigation_type_4.0	well_irrigation_type_6.0	well_irrigation_type_7.0	well_irrigation_source_1_percentage	well_irrigation_source_2_percentage	well_irrigation_source_4_percentage	well_irrigation_source_5_percentage	well_irrigation_source_6_percentage	well_irrigation_source_10_percentage	well_irrigation_source_12_percentage	well_irrigation_type_1.0_percentage	well_irrigation_type_2.0_percentage	well_irrigation_type_3.0_percentage	well_irrigation_type_4.0_percentage	well_irrigation_type_6.0_percentage	well_irrigation_type_7.0_percentage	active_wells_percentage	sprinklers_count	sprinklers_count_kw
0	01_00_000002	5	5	4	1	0	0	0	0	0	4	1	0	0	0	0	0.8	0.2	0.0	0.0	0.0	0.0	0.0	0.8	0.2	0.0	0.0	0.0	0.0	1.0	5	125
1	01_00_000003	5	5	5	0	0	0	0	0	0	5	0	0	0	0	0	1.0	0.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0	0.0	0.0	0.0	0.0	1.0	5	125
2	01_00_000006	1	1	0	1	0	0	0	0	0	1	0	0	0	0	0	0.0	1.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0	0.0	0.0	0.0	0.0	1.0	1	25
3	01_00_000008	2	2	1	1	0	0	0	0	0	1	0	1	0	0	0	0.5	0.5	0.0	0.0	0.0	0.0	0.0	0.5	0.0	0.5	0.0	0.0	0.0	1.0	2	50


## Cell 3 
<code>
import pandas as pd
import geopandas as gpd
import numpy as np



# Rename columns
rename_dict = {
    'HSRCode': 'activity_id',
    'OB_HSRCode': 'farm_id',
    'ActivityStatus': 'activity_status',
    'FarmType': 'farm_type',
    'MainCropsType': 'main_crop_type',
    'CropsType': 'crop_type',
    'IrragationSource': 'irrigation_source',
    'IrragationType': 'irrigation_type',
    'FarmingSeason': 'farming_season',
    'TotalArea': 'total_area_hectares',
    'ProductiveTreesNo': 'productive_trees_count',
    'ProtectedHouseNo': 'protected_house_count',
    'ProtectedHouseType': 'protected_house_type',
    'PlantationsNo': 'plantations_count',
    'PlantationsType': 'plantations_type'
}
df_farms = df_farms.rename(columns={k: v for k, v in rename_dict.items() if k in df_farms.columns})

def safe_float(x):
    if pd.isna(x) or x == '':
        return np.nan
    try:
        return float(x)
    except ValueError:
        return np.nan

# Handle numeric columns
numeric_columns = ['total_area_hectares', 'productive_trees_count', 'protected_house_count', 'plantations_count', 'SHAPE_Length', 'SHAPE_Area']
numeric_columns = [col for col in numeric_columns if col in df_farms.columns]
for col in numeric_columns:
    df_farms[col] = df_farms[col].apply(safe_float)

# Handle categorical columns
categorical_columns = ['activity_status', 'farm_type', 'main_crop_type', 'irrigation_source', 'irrigation_type', 'farming_season', 'protected_house_type', 'plantations_type']
categorical_columns = [col for col in categorical_columns if col in df_farms.columns]
for col in categorical_columns:
    df_farms[col] = df_farms[col].fillna(df_farms[col].mode()[0]).astype('category')
    df_farms[col] = df_farms[col].replace(0, df_farms[col].mode()[0]).astype('category')
    df_farms[col] = df_farms[col].astype('category')

# Create dummy variables for categorical columns
df_farms = pd.get_dummies(df_farms, columns=categorical_columns, prefix_sep='_', dtype=int)

# Prepare aggregation dictionary
agg_dict = {
    'activity_id': 'nunique',
    'crop_type': 'nunique',
    'X': 'first',
    'Y': 'first'
}
agg_dict.update({col: 'sum' for col in numeric_columns})

# Add dummy columns to aggregation dictionary
dummy_columns = [col for col in df_farms.columns if '_' in col and col not in ['farm_id', 'activity_id', 'crop_type']]
agg_dict.update({col: 'sum' for col in dummy_columns})

# Group by farm_id and aggregate
df_farms_summary = df_farms.groupby('farm_id').agg(agg_dict)

# Rename columns for clarity
df_farms_summary = df_farms_summary.rename(columns={
    'activity_id': 'activity_count',
    'crop_type': 'unique_crop_types_count'
})



df_farms_summary = df_farms_summary.drop(columns=["X", "Y", "SHAPE_Length", "SHAPE_Area",])
df_farms_summary
</code>

## Cell 3 Output
	activity_count	unique_crop_types_count	total_area_hectares	productive_trees_count	protected_house_count	plantations_count	activity_status_1	activity_status_3	activity_status_4	activity_status_6	farm_type_1.0	farm_type_2.0	farm_type_5.0	farm_type_6.0	farm_type_7.0	farm_type_10.0	farm_type_11.0	main_crop_type_1.0	main_crop_type_2.0	main_crop_type_3.0	main_crop_type_4.0	main_crop_type_5.0	main_crop_type_6.0	main_crop_type_7.0	main_crop_type_8.0	main_crop_type_9.0	main_crop_type_10.0	main_crop_type_12.0	main_crop_type_13.0	main_crop_type_14.0	main_crop_type_15.0	irrigation_source_1.0	irrigation_source_2.0	irrigation_source_4.0	irrigation_source_5.0	irrigation_source_6.0	irrigation_source_7.0	irrigation_source_10.0	irrigation_source_12.0	irrigation_type_1.0	irrigation_type_2.0	irrigation_type_3.0	irrigation_type_4.0	irrigation_type_6.0	irrigation_type_7.0	farming_season_1.0	farming_season_2.0	farming_season_3.0	farming_season_4.0	protected_house_type_1.0	protected_house_type_2.0	protected_house_type_3.0	protected_house_type_4.0	protected_house_type_6.0	protected_house_type_7.0	plantations_type_1.0	plantations_type_2.0	plantations_type_3.0
farm_id																																																										
01_00_000002	6	2	55.035575	594.0	0.0	0.0	4	1	1	0	0	5	0	1	0	0	0	4	1	0	0	0	0	0	0	0	0	0	0	0	1	0	5	0	0	0	0	0	1	4	0	1	0	1	0	4	0	0	2	6	0	0	0	0	0	0	0	6
01_00_000003	5	1	67.494602	0.0	0.0	0.0	5	0	0	0	0	5	0	0	0	0	0	5	0	0	0	0	0	0	0	0	0	0	0	0	0	0	5	0	0	0	0	0	0	5	0	0	0	0	0	5	0	0	0	5	0	0	0	0	0	0	0	5
01_00_000006	1	1	30.682688	0.0	0.0	0.0	1	0	0	0	0	1	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	1	0	0	0	0	0	0	0	1	0	1	0	0	0	0	0	0	0	1

## Cell 4 
<code>
df_property = (
    df_property[["OB_HSRCode", "SHAPE_Area", "MainType"]].rename(
        columns={
            "OB_HSRCode": "farm_id",
            "SHAPE_Area": "property_area",
            "MainType": "property_main_type",
        }
    )
)
df_property
</code>
## Cell 4 Output
	farm_id	property_area	property_main_type
0	05_00_000030	3.565259e+06	3.0
1	05_00_000090	3.681615e+06	3.0
2	05_00_000051	2.555279e+06	3.0

## Cell 5 
<code>
import pandas as pd
import numpy as np

# Load the data
df_visits = pd.read_csv("./processed_data/visits_final.csv")
print(f"\nNumber of rows before processing: {len(df_visits)}")


# Function to safely convert to float
def safe_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


# Function to safely convert to int
def safe_int(x):
    try:
        return int(float(x))
    except (ValueError, TypeError):
        return np.nan


# Clean and process the data
def process_visits_data(df):
    # Select only the specified columns
    columns_to_keep = [
        "farm_id",
        "mechanical_head_1_hp",
        "mechanical_head_2_hp",
        "mechanical_head_3_hp",
        "mechanical_head_4_hp",
        "mechanical_head_5_hp",
        "mechanical_head_6_hp",
        "mechanical_head_7_hp",
        "mechanical_head_8_hp",
        "mechanical_head_9_hp",
        "mechanical_head_10_hp",
        "mechanical_head_11_hp",
        "mechanical_head_12_hp",
        "mechanical_head_13_hp",
        "mechanical_head_14_hp",
        "mechanical_head_15_hp",
        "total_mechanical_head_hp",
        #"total_mechanical_head_kw",
        "electrical_head_1_hp",
        "electrical_head_2_hp",
        "electrical_head_3_hp",
        "electrical_head_4_hp",
        "electrical_head_5_hp",
        "electrical_head_6_hp",
        "total_electrical_head_hp",
        #"total_electrical_head_kw",
        "water_level_sensor_1_hp",
        "water_level_sensor_2_hp",
        "water_level_sensor_3_hp",
        "water_level_sensor_4_hp",
        "water_level_sensor_5_hp",
        "water_level_sensor_6_hp",
        "water_level_sensor_7_hp",
        "water_level_sensor_8_hp",
        "water_level_sensor_9_hp",
        "water_level_sensor_10_hp",
        "water_level_sensor_11_hp",
        "water_level_sensor_12_hp",
        "water_level_sensor_13_hp",
        "water_level_sensor_14_hp",
        "water_level_sensor_15_hp",
        "water_level_sensor_16_hp",
        "water_level_sensor_17_hp",
        "water_level_sensor_18_hp",
        "water_level_sensor_19_hp",
        "water_level_sensor_20_hp",
        "water_level_sensor_21_hp",
        "total_water_level_sensor_hp",
        #"total_water_level_sensor_kw",
        "pump_1_hp",
        "pump_2_hp",
        "pump_3_hp",
        "pump_4_hp",
        "total_pump_hp",
        #"total_pump_kw",
        "total_electrical_load_kw",
        #"total_electrical_load_kva",
        "mechanical_heads_counts",
        "electrical_heads_counts",
        "water_level_counts",
        "pump_counts",
    ]
    df = df[columns_to_keep]

    # Rename water_level_sensor columns to submersible_pump
    rename_dict = {
        col: col.replace("water_level_sensor", "submersible_pump")
        for col in df.columns
        if "water_level_sensor" in col
    }
    df = df.rename(columns=rename_dict)

    # Convert all numeric columns to float
    numeric_columns = df.columns.drop("farm_id")
    for col in numeric_columns:
        df[col] = df[col].apply(safe_float)
    
    df = df.rename(columns={"water_level_counts": "submersible_pump_counts"})

    # Convert count columns to integers
    count_columns = [
        "mechanical_heads_counts",
        "electrical_heads_counts",
        "submersible_pump_counts",
        "pump_counts",
    ]
    for col in count_columns:
        df[col] = df[col].apply(safe_int)

    # Drop rows where all equipment counts are 0 or NaN
    df = df[
        ~(
            (df["mechanical_heads_counts"].fillna(0) == 0)
            & (df["electrical_heads_counts"].fillna(0) == 0)
            & (df["submersible_pump_counts"].fillna(0) == 0)
            & (df["pump_counts"].fillna(0) == 0)
        )
    ]

    return df


# Process the data
df_visits_processed = process_visits_data(df_visits).fillna(0)

# Print the number of rows before and after filtering
print(f"\nNumber of rows before filtering: {len(df_visits)}")
print(f"Number of rows after filtering: {len(df_visits_processed)}")

df_visits_processed
</code>
## Cell 5 Output
	farm_id	mechanical_head_1_hp	mechanical_head_2_hp	mechanical_head_3_hp	mechanical_head_4_hp	mechanical_head_5_hp	mechanical_head_6_hp	mechanical_head_7_hp	mechanical_head_8_hp	mechanical_head_9_hp	mechanical_head_10_hp	mechanical_head_11_hp	mechanical_head_12_hp	mechanical_head_13_hp	mechanical_head_14_hp	mechanical_head_15_hp	total_mechanical_head_hp	electrical_head_1_hp	electrical_head_2_hp	electrical_head_3_hp	electrical_head_4_hp	electrical_head_5_hp	electrical_head_6_hp	total_electrical_head_hp	submersible_pump_1_hp	submersible_pump_2_hp	submersible_pump_3_hp	submersible_pump_4_hp	submersible_pump_5_hp	submersible_pump_6_hp	submersible_pump_7_hp	submersible_pump_8_hp	submersible_pump_9_hp	submersible_pump_10_hp	submersible_pump_11_hp	submersible_pump_12_hp	submersible_pump_13_hp	submersible_pump_14_hp	submersible_pump_15_hp	submersible_pump_16_hp	submersible_pump_17_hp	submersible_pump_18_hp	submersible_pump_19_hp	submersible_pump_20_hp	submersible_pump_21_hp	total_submersible_pump_hp	pump_1_hp	pump_2_hp	pump_3_hp	pump_4_hp	total_pump_hp	total_electrical_load_kw	mechanical_heads_counts	electrical_heads_counts	submersible_pump_counts	pump_counts
3	01_00_000008	300.0	300.0	300.0	300.0	300.0	300.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	1800.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	1492.80	6	0	0	0
7	01_00_000012	300.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	300.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	150.0	0.0	0.0	0.0	150.0	360.70	1	0	0	1

## Cell 6
<code>
import pandas as pd
import numpy as np

# Assuming all dataframes are already loaded and preprocessed
# df_property, df_farms_summary, df_visits_processed, df_wells_summary

# Start with df_property as the base
df_integrated = df_property.copy()

# Merge with df_farms_summary
df_integrated = df_integrated.merge(df_farms_summary, on='farm_id', how='left')

# Merge with df_wells_summary
df_integrated = df_integrated.merge(df_wells_summary, on='farm_id', how='left')


# Merge with df_visits_processed
df_integrated = df_integrated.merge(df_visits_processed, on='farm_id', how='left')


# Handle missing values
numeric_columns = df_integrated.select_dtypes(include=[np.number]).columns
df_integrated[numeric_columns] = df_integrated[numeric_columns].fillna(0)


df_integrated.columns.tolist()
</code>

## Cell 6 Output
['farm_id',
 'property_area',
 'property_main_type',
 'activity_count',
 'unique_crop_types_count',
 'total_area_hectares',
 'productive_trees_count',
 'protected_house_count',
 'plantations_count',
 'activity_status_1',
 'activity_status_3',
 'activity_status_4',
 'activity_status_6',
 'farm_type_1.0',
 'farm_type_2.0',
 'farm_type_5.0',
 'farm_type_6.0',
 'farm_type_7.0',
 'farm_type_10.0',
 'farm_type_11.0',
 'main_crop_type_1.0',
 'main_crop_type_2.0',
 'main_crop_type_3.0',
 'main_crop_type_4.0',
 'main_crop_type_5.0',
 'main_crop_type_6.0',
 'main_crop_type_7.0',
 'main_crop_type_8.0',
 'main_crop_type_9.0',
 'main_crop_type_10.0',
 'main_crop_type_12.0',
 'main_crop_type_13.0',
 'main_crop_type_14.0',
 'main_crop_type_15.0',
 'irrigation_source_1.0',
 'irrigation_source_2.0',
 'irrigation_source_4.0',
 'irrigation_source_5.0',
 'irrigation_source_6.0',
 'irrigation_source_7.0',
 'irrigation_source_10.0',
 'irrigation_source_12.0',
 'irrigation_type_1.0',
 'irrigation_type_2.0',
 'irrigation_type_3.0',
 'irrigation_type_4.0',
 'irrigation_type_6.0',
 'irrigation_type_7.0',
 'farming_season_1.0',
 'farming_season_2.0',
 'farming_season_3.0',
 'farming_season_4.0',
 'protected_house_type_1.0',
 'protected_house_type_2.0',
 'protected_house_type_3.0',
 'protected_house_type_4.0',
 'protected_house_type_6.0',
 'protected_house_type_7.0',
 'plantations_type_1.0',
 'plantations_type_2.0',
 'plantations_type_3.0',
 'well_id',
 'well_is_active',
 'well_irrigation_source_1',
 'well_irrigation_source_2',
 'well_irrigation_source_4',
 'well_irrigation_source_5',
 'well_irrigation_source_6',
 'well_irrigation_source_10',
 'well_irrigation_source_12',
 'well_irrigation_type_1.0',
 'well_irrigation_type_2.0',
 'well_irrigation_type_3.0',
 'well_irrigation_type_4.0',
 'well_irrigation_type_6.0',
 'well_irrigation_type_7.0',
 'well_irrigation_source_1_percentage',
 'well_irrigation_source_2_percentage',
 'well_irrigation_source_4_percentage',
 'well_irrigation_source_5_percentage',
 'well_irrigation_source_6_percentage',
 'well_irrigation_source_10_percentage',
 'well_irrigation_source_12_percentage',
 'well_irrigation_type_1.0_percentage',
 'well_irrigation_type_2.0_percentage',
 'well_irrigation_type_3.0_percentage',
 'well_irrigation_type_4.0_percentage',
 'well_irrigation_type_6.0_percentage',
 'well_irrigation_type_7.0_percentage',
 'active_wells_percentage',
 'sprinklers_count',
 'sprinklers_count_kw',
 'mechanical_head_1_hp',
 'mechanical_head_2_hp',
 'mechanical_head_3_hp',
 'mechanical_head_4_hp',
 'mechanical_head_5_hp',
 'mechanical_head_6_hp',
 'mechanical_head_7_hp',
 'mechanical_head_8_hp',
 'mechanical_head_9_hp',
 'mechanical_head_10_hp',
 'mechanical_head_11_hp',
 'mechanical_head_12_hp',
 'mechanical_head_13_hp',
 'mechanical_head_14_hp',
 'mechanical_head_15_hp',
 'total_mechanical_head_hp',
 'electrical_head_1_hp',
 'electrical_head_2_hp',
 'electrical_head_3_hp',
 'electrical_head_4_hp',
 'electrical_head_5_hp',
 'electrical_head_6_hp',
 'total_electrical_head_hp',
 'submersible_pump_1_hp',
 'submersible_pump_2_hp',
 'submersible_pump_3_hp',
 'submersible_pump_4_hp',
 'submersible_pump_5_hp',
 'submersible_pump_6_hp',
 'submersible_pump_7_hp',
 'submersible_pump_8_hp',
 'submersible_pump_9_hp',
 'submersible_pump_10_hp',
 'submersible_pump_11_hp',
 'submersible_pump_12_hp',
 'submersible_pump_13_hp',
 'submersible_pump_14_hp',
 'submersible_pump_15_hp',
 'submersible_pump_16_hp',
 'submersible_pump_17_hp',
 'submersible_pump_18_hp',
 'submersible_pump_19_hp',
 'submersible_pump_20_hp',
 'submersible_pump_21_hp',
 'total_submersible_pump_hp',
 'pump_1_hp',
 'pump_2_hp',
 'pump_3_hp',
 'pump_4_hp',
 'total_pump_hp',
 'total_electrical_load_kw',
 'mechanical_heads_counts',
 'electrical_heads_counts',
 'submersible_pump_counts',
 'pump_counts']

## Cell 7
<code>
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.feature_selection import SelectFromModel
from sklearn.impute import KNNImputer

def evaluate_model(y_true, y_pred, step_name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\nEvaluation metrics for {step_name}:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.2f}")

# Load the data
df = df_integrated.copy()

# Separate HASAR features from visits data
hasar_columns = [
    'farm_id', 'property_area', 'property_main_type', 'activity_count', 
    'unique_crop_types_count', 'total_area_hectares', 'productive_trees_count', 
    'protected_house_count', 'plantations_count'
] + [col for col in df.columns if col.startswith(('activity_status_', 'farm_type_', 
    'main_crop_type_', 'irrigation_source_', 'irrigation_type_', 'farming_season_', 
    'protected_house_type_', 'plantations_type_', 'well_'))]

visits_columns = ['total_electrical_load_kw']

df_hasar = df[hasar_columns]
df_visits = df[['farm_id', 'total_electrical_load_kw']]

# Handle missing values in HASAR data
# imputer = KNNImputer(n_neighbors=5)
# df_hasar_imputed = pd.DataFrame(imputer.fit_transform(df_hasar), columns=df_hasar.columns)
df_hasar_imputed = df_hasar.copy()
# Normalize numerical features
scaler = StandardScaler()
numerical_features = df_hasar_imputed.select_dtypes(include=[np.number]).columns
df_hasar_imputed[numerical_features] = scaler.fit_transform(df_hasar_imputed[numerical_features])

# Feature selection
features = [col for col in df_hasar_imputed.columns if col not in ['farm_id']]
selector = SelectFromModel(RandomForestRegressor(n_estimators=100, random_state=42), threshold='median')
selector = selector.fit(df_hasar_imputed[features], df_visits['total_electrical_load_kw'])
selected_features = df_hasar_imputed[features].columns[selector.get_support()]

# Prepare data for modeling
X = df_hasar_imputed[selected_features]
y = df_visits['total_electrical_load_kw']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models and parameter grids
models = {
    'RandomForest': RandomForestRegressor(random_state=42),
    'GradientBoosting': GradientBoostingRegressor(random_state=42),
    'SVR': SVR()
}

param_grids = {
    'RandomForest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    },
    'GradientBoosting': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 4, 5],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    },
    'SVR': {
        'C': [0.1, 1, 10],
        'epsilon': [0.1, 0.2, 0.3],
        'kernel': ['rbf', 'linear']
    }
}

# Perform RandomizedSearchCV for each model
best_model = None
best_score = float('-inf')

for name, model in models.items():
    print(f"\nTuning {name}...")
    random_search = RandomizedSearchCV(model, param_distributions=param_grids[name],
                                       n_iter=20, cv=5, scoring='neg_mean_squared_error',
                                       random_state=42, n_jobs=-1)
    random_search.fit(X_train, y_train)
    
    # Evaluate the best model from the random search
    y_pred = random_search.best_estimator_.predict(X_test)
    evaluate_model(y_test, y_pred, f"{name} (after tuning)")
    
    # Update the best model if this one performed better
    score = r2_score(y_test, y_pred)
    if score > best_score:
        best_score = score
        best_model = random_search.best_estimator_

# Use the best model to make final predictions
df_hasar_imputed['estimated_total_electrical_load_kw'] = best_model.predict(df_hasar_imputed[selected_features])

# Merge predictions with actual values
results = pd.merge(df_hasar_imputed[['farm_id', 'estimated_total_electrical_load_kw']], 
                   df_visits, on='farm_id', how='left')

# Print results
print("\nSummary statistics of actual vs estimated total electrical load:")
print(results[['total_electrical_load_kw', 'estimated_total_electrical_load_kw']].describe())

# Calculate final evaluation metrics
final_predictions = results.dropna()
evaluate_model(final_predictions['total_electrical_load_kw'], 
               final_predictions['estimated_total_electrical_load_kw'], 
               "Final Model")

# Save the results
results.to_csv('hasar_only_farm_consumption_estimates.csv', index=False)

# Print feature importances
if hasattr(best_model, 'feature_importances_'):
    importances = pd.DataFrame({'feature': selected_features, 
                                'importance': best_model.feature_importances_})
    importances = importances.sort_values('importance', ascending=False)
    print("\nTop 10 most important features:")
    print(importances.head(10))
</code>

## Cell 7 Output

Tuning RandomForest...

Evaluation metrics for RandomForest (after tuning):
MAE: 145.29
RMSE: 214.99
R2 Score: 0.28

Tuning GradientBoosting...

Evaluation metrics for GradientBoosting (after tuning):
MAE: 146.50
RMSE: 216.21
R2 Score: 0.27

Tuning SVR...
/Users/moealhazmi/opt/anaconda3/envs/farms_claude/lib/python3.11/site-packages/sklearn/model_selection/_search.py:320: UserWarning: The total space of parameters 18 is smaller than n_iter=20. Running 18 iterations. For exhaustive searches, use GridSearchCV.
  warnings.warn(

Evaluation metrics for SVR (after tuning):
MAE: 154.11
RMSE: 234.28
R2 Score: 0.14

Summary statistics of actual vs estimated total electrical load:
       total_electrical_load_kw  estimated_total_electrical_load_kw
count              18317.000000                        18317.000000
mean                 206.034694                          207.298903
std                  256.928693                          142.733892
min                    0.000000                            0.000000
25%                    0.000000                          106.417725
50%                  174.200000                          197.303257
75%                  342.050000                          270.866803
max                 4291.500000                         2217.173099

Evaluation metrics for Final Model:
MAE: 132.39
RMSE: 191.66
R2 Score: 0.44

Top 10 most important features:
                     feature  importance
4        total_area_hectares    0.287364
37  well_irrigation_type_1.0    0.128180
22       irrigation_type_1.0    0.088054
0              property_area    0.076746
5     productive_trees_count    0.042348
33            well_is_active    0.040581
29        farming_season_4.0    0.033813
3    unique_crop_types_count    0.030779
7          activity_status_1    0.027544
27        farming_season_2.0    0.022243

## Cell 8
<code>
pd.DataFrame({"predicted": best_model.predict(X_test), "true": y_test}).sample(10)
</code>
## Cell 8 Output
	predicted	true
10820	0.000000	0.00
5198	337.551629	342.05
11398	213.240099	286.10
700	193.796258	248.80
15394	278.597432	628.15
14508	199.143286	0.00
15348	105.635780	0.00
15108	139.966355	0.00
15800	310.220247	0.00
11668	91.339812	0.00

## Cell 9
<code>
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, QuantileTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import joblib
import shap

class NonNegativeRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, base_estimator):
        self.base_estimator = base_estimator

    def fit(self, X, y):
        self.base_estimator.fit(X, y)
        return self

    def predict(self, X):
        predictions = self.base_estimator.predict(X)
        return np.maximum(predictions, 0)

def load_and_preprocess_data(file_path):
    df = df_integrated.copy()
    
    # Top 10 important features based on SHAP values
    important_features = [
        'irrigation_source_2.0', 'total_area_hectares', 'unique_crop_types_count',
        'irrigation_type_2.0', 'property_area', 'productive_trees_count',
        'main_crop_type_6.0', 'activity_count', 'main_crop_type_15.0',
        'irrigation_type_4.0'
    ]
    
    # Add 'farm_id' for joining purposes
    columns_to_keep = ['farm_id'] + important_features
    
    df_hasar = df[columns_to_keep]
    df_target = df[['farm_id', 'total_electrical_load_kw']]
    
    return df_hasar, df_target

def engineer_features(df):
    # Since we're using only the top 10 features, we might not need to engineer new features
    # However, if any of these were engineered features, we would keep that logic here
    return df

def create_preprocessor(X):
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', QuantileTransformer(output_distribution='normal'))
            ]), numeric_features),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ]), categorical_features)
        ])
    return preprocessor

def create_ensemble_model():
    gb_model = NonNegativeRegressor(GradientBoostingRegressor(random_state=42))
    rf_model = NonNegativeRegressor(RandomForestRegressor(random_state=42))

    ensemble = VotingRegressor([
        ('gb', gb_model),
        ('rf', rf_model)
    ])
    return ensemble

def evaluate_model(y_true, y_pred, step_name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\nEvaluation metrics for {step_name}:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.2f}")

def perform_cross_validation(model, X, y, cv=5):
    kfold = KFold(n_splits=cv, shuffle=True, random_state=42)
    
    r2_scores = cross_val_score(model, X, y, cv=kfold, scoring='r2')
    rmse_scores = np.sqrt(-cross_val_score(model, X, y, cv=kfold, scoring='neg_mean_squared_error'))
    mae_scores = -cross_val_score(model, X, y, cv=kfold, scoring='neg_mean_absolute_error')
    
    print(f"\nCross-Validation Results (mean ± std):")
    print(f"R2 Score: {r2_scores.mean():.3f} ± {r2_scores.std():.3f}")
    print(f"RMSE: {rmse_scores.mean():.3f} ± {rmse_scores.std():.3f}")
    print(f"MAE: {mae_scores.mean():.3f} ± {mae_scores.std():.3f}")

def compute_shap_values(model, X):
    explainer = shap.TreeExplainer(model.estimators_[0].base_estimator)
    shap_values = explainer.shap_values(X)
    
    feature_names = X.columns
    shap_sum = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame(list(zip(feature_names, shap_sum)), columns=['feature', 'importance'])
    importance_df = importance_df.sort_values('importance', ascending=False)
    
    print("\nFeature importance based on SHAP values:")
    print(importance_df)
    
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig('shap_summary_plot.png')
    plt.close()

def save_pipeline(pipeline, feature_names, file_path):
    pipeline_data = {
        'pipeline': pipeline,
        'feature_names': feature_names
    }
    joblib.dump(pipeline_data, file_path)

def main():
    # Load and preprocess data
    df_hasar, df_target = load_and_preprocess_data('df_integrated.csv')
    df_hasar = engineer_features(df_hasar)

    # Prepare data for modeling
    X = df_hasar.drop('farm_id', axis=1)
    y = df_target['total_electrical_load_kw']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create preprocessor and model
    preprocessor = create_preprocessor(X)
    ensemble = create_ensemble_model()

    # Create a pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', ensemble)
    ])

    # Define parameter grid for RandomizedSearchCV
    param_grid = {
        'model__gb__base_estimator__n_estimators': [100, 200, 300],
        'model__gb__base_estimator__max_depth': [3, 4, 5],
        'model__gb__base_estimator__learning_rate': [0.01, 0.1, 0.2],
        'model__rf__base_estimator__n_estimators': [100, 200, 300],
        'model__rf__base_estimator__max_depth': [10, 20, 30, None],
        'model__rf__base_estimator__min_samples_split': [2, 5, 10],
    }

    # Perform RandomizedSearchCV
    random_search = RandomizedSearchCV(pipeline, param_distributions=param_grid,
                                       n_iter=20, cv=5, scoring='neg_mean_squared_error',
                                       random_state=42, n_jobs=-1)
    random_search.fit(X_train, y_train)

    # Get the best model
    best_pipeline = random_search.best_estimator_

    # Perform cross-validation
    print("\nPerforming cross-validation on the best model:")
    perform_cross_validation(best_pipeline, X, y)

    # Make predictions on the test set
    y_pred_test = best_pipeline.predict(X_test)

    # Evaluate the model on the test set
    print("\nEvaluating the model on the test set:")
    evaluate_model(y_test, y_pred_test, "Best Ensemble Model (Test Set)")

    # Make predictions on the entire dataset
    y_pred_all = best_pipeline.predict(X)

    # Merge predictions with actual values
    results = pd.DataFrame({
        'farm_id': df_hasar['farm_id'],
        'actual_load': df_target['total_electrical_load_kw'],
        'estimated_load': y_pred_all
    })

    # Print summary statistics
    print("\nSummary statistics of actual vs estimated total electrical load:")
    print(results[['actual_load', 'estimated_load']].describe())

    # Calculate final evaluation metrics
    print("\nFinal evaluation metrics on the entire dataset:")
    evaluate_model(results['actual_load'], results['estimated_load'], "Final Ensemble Model (Full Dataset)")

    # Compute SHAP values
    compute_shap_values(best_pipeline.named_steps['model'], X)

    # Save the results
    results.to_csv('ensemble_hasar_farm_consumption_estimates.csv', index=False)

    # Save the pipeline and feature names
    save_pipeline(best_pipeline, X.columns.tolist(), 'hasar_farm_pipeline.joblib')

if __name__ == "__main__":
    main()
</code>

## Cell 9 Output
Performing cross-validation on the best model:

Cross-Validation Results (mean ± std):
R2 Score: 0.223 ± 0.020
RMSE: 226.016 ± 13.366
MAE: 156.837 ± 2.183

Evaluating the model on the test set:

Evaluation metrics for Best Ensemble Model (Test Set):
MAE: 156.10
RMSE: 223.18
R2 Score: 0.22

Summary statistics of actual vs estimated total electrical load:
        actual_load  estimated_load
count  18313.000000    18313.000000
mean     206.036230      207.676565
std      256.939899      121.599872
min        0.000000       10.762010
25%        0.000000      126.602952
50%      174.200000      196.254522
75%      342.050000      266.495831
max     4291.500000     2066.679092

Final evaluation metrics on the entire dataset:

Evaluation metrics for Final Ensemble Model (Full Dataset):
MAE: 131.48
RMSE: 188.42
R2 Score: 0.46

Feature importance based on SHAP values:
                   feature  importance
1      total_area_hectares  300.278207
8      main_crop_type_15.0  104.128328
2  unique_crop_types_count   34.218157
5   productive_trees_count   29.933737
4            property_area   27.060146
0    irrigation_source_2.0    8.878495
7           activity_count    2.983722
6       main_crop_type_6.0    1.215203
3      irrigation_type_2.0    1.205966
9      irrigation_type_4.0    0.000000

