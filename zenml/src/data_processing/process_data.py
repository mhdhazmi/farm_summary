# src/data_processing/process_data.py

import pandas as pd
from src.utils.helpers import OutlierCapper

def process_wells_data(df_wells):
    # Rename columns
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
    df_wells = df_wells[['well_id', 'farm_id', 'well_possession_type', 'well_is_active', 'well_irrigation_source', 'well_irrigation_type']]
    df_wells['well_possession_type'] = df_wells['well_possession_type'].astype('category')
    df_wells['well_is_active'] = df_wells['well_is_active'].astype('category')
    df_wells['well_irrigation_source'] = df_wells['well_irrigation_source'].astype('category')
    df_wells['well_irrigation_type'] = df_wells['well_irrigation_type'].astype('category')

    categorical_columns = df_wells.drop(columns=['farm_id']).select_dtypes(include=['object', 'category']).columns.tolist()

    # Fill missing categorical data
    for col in categorical_columns:
        df_wells[col] = df_wells[col].fillna(df_wells[col].mode()[0])
        df_wells[col] = df_wells[col].replace(0, df_wells[col].mode()[0])

    # Count wells per farm
    well_count = df_wells.groupby("farm_id").agg(well_count=pd.NamedAgg(column="well_id", aggfunc="count")).reset_index()
    df_wells = df_wells.drop(columns=['well_id'])

    # One-hot encoding
    df_wells_summary = pd.get_dummies(df_wells, columns=['well_possession_type','well_is_active','well_irrigation_source', 'well_irrigation_type'], dtype=int)
    df_wells_summary = df_wells_summary.groupby("farm_id").sum().reset_index()
    df_wells_summary = pd.merge(df_wells_summary, well_count, on='farm_id')

    # Calculate percentages for irrigation sources and types
    for col in df_wells_summary.columns:
        if col.startswith('well_') and col != 'well_count':
            df_wells_summary[f'{col}_percentage'] = df_wells_summary[col] / df_wells_summary['well_count']

    df_wells_summary['sprinklers_count'] = df_wells_summary['well_count']
    df_wells_summary['sprinklers_count_kw'] = df_wells_summary['well_count'] * 25

    return df_wells_summary

def process_farms_data(df_farms):
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

    # Convert data types
    float_cols = ['total_area_hectares', 'productive_trees_count', 'protected_house_count', 'plantations_count']
    for col in float_cols:
        df_farms[col] = df_farms[col].astype(float)

    categorical_cols = ['activity_id', 'farm_id', 'activity_status', 'farm_type', 'main_crop_type',
                        'crop_type', 'irrigation_source', 'irrigation_type',
                        'farming_season', 'protected_house_type', 'plantations_type']

    for col in categorical_cols:
        if col in df_farms.columns:
            df_farms[col] = df_farms[col].astype('category')

    numeric_columns = df_farms.select_dtypes(include=['float', 'int']).columns.tolist()
    categorical_columns = df_farms.drop(columns=['farm_id', 'activity_id', 'crop_type']).select_dtypes(include=['object', 'category']).columns.tolist()

    # Fill missing categorical data
    for col in categorical_columns:
        if col in df_farms.columns:
            df_farms[col] = df_farms[col].fillna(df_farms[col].mode()[0])
            df_farms[col] = df_farms[col].replace(0, df_farms[col].mode()[0])

    # One-hot encoding
    df_farms = pd.get_dummies(df_farms, columns=categorical_columns, prefix_sep='_', dtype=int)

    # Aggregation
    agg_dict = {
        'activity_id': 'nunique',
        'crop_type': 'nunique',
    }
    agg_dict.update({col: 'sum' for col in numeric_columns})

    # Add dummy columns to aggregation dictionary
    dummy_columns = [col for col in df_farms.columns if '_' in col and col not in ['farm_id', 'activity_id', 'crop_type'] and col not in numeric_columns]
    agg_dict.update({col: 'sum' for col in dummy_columns})

    # Group by farm_id and aggregate
    df_farms_summary = df_farms.groupby('farm_id').agg(agg_dict).rename(columns={'activity_id': 'activity_count', 'crop_type': 'unique_crop_types_count'}).reset_index()

    # Drop unnecessary columns if any
    columns_to_drop = ["X", "Y", "SHAPE_Length", "SHAPE_Area"]  # Adjust as needed
    df_farms_summary = df_farms_summary.drop(columns=[col for col in columns_to_drop if col in df_farms_summary.columns], errors='ignore')

    return df_farms_summary

def process_property_data(df_property):
    df_property = (
        df_property[["OB_HSRCode", "SHAPE_Area", "MainType"]].rename(
            columns={
                "OB_HSRCode": "farm_id",
                "SHAPE_Area": "property_area",
                "MainType": "property_main_type",
            }
        )
    )
    return df_property

def integrate_data(df_property, df_farms_summary, df_wells_summary, df_visits_processed):
    # Start with df_property as the base
    df_integrated = df_property.copy()

    # Merge with df_farms_summary
    df_integrated = df_integrated.merge(df_farms_summary, on='farm_id', how='left')

    # Merge with df_wells_summary
    df_integrated = df_integrated.merge(df_wells_summary, on='farm_id', how='left')

    # Merge with df_visits_processed
    df_integrated = df_integrated.merge(df_visits_processed, on='farm_id', how='right')

    return df_integrated

