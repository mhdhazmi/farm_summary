import pandas as pd

def get_dummies(df, columns, dtype):
    return pd.get_dummies(df, columns=columns, dtype=dtype, dummy_na=False, drop_first=False)

def count_non_zero_non_nan(df):
    return df.map(lambda x: x != 0).sum()

def processing_farms(df_farms):
    df_farms_count = (
    df_farms.rename(
        columns={
            "HSRCode": "activity_id",
            "OB_HSRCode": "farm_id",
            "ActivityStatus": "farm_activity_status",
            "FarmType": "farm_type",
            "MainCropsType": "farm_main_crops_type",
            "CropsType": "farm_crops_type",
            "IrragationSource": "farm_irrigation_source",
            "IrragationType": "farm_irrigation_type",
            "FarmingSeason": "farm_farming_season",
            "TotalArea": "farm_activity_area_hectares",
            "ProductiveTreesNo": "farm_trees_count",
            "ProtectedHouseNo": "farm_house_count",
            "ProtectedHouseType": "farm_house_type",
            "PlantationsNo": "farm_plantations_count",
            "X": "farm_x",
            "Y": "farm_y",
            "SHAPE_Length": "farm_activity_length_m",
            "SHAPE_Area": "farm_activity_area_sq_m",
            "geometry": "farm_geometry",
            "PlantationsType": "farm_plantations_type",
        }
    )
    .drop_duplicates()
    .fillna(0)
    .assign(farm_activity_status = lambda x: x['farm_activity_status'].replace(0, x['farm_activity_status'].mode()[0]))
    .assign(farm_type = lambda x: x['farm_type'].astype(int).replace(0, x['farm_type'].mode()[0]))
    .assign(farm_main_crops_type = lambda x: x['farm_main_crops_type'].astype(int).replace(0, x['farm_main_crops_type'].mode()[0]))
    .assign(farm_irrigation_source = lambda x: x['farm_irrigation_source'].astype(int).replace(0, x['farm_irrigation_source'].mode()[0]))
    .assign(farm_irrigation_type = lambda x: x['farm_irrigation_type'].astype(int).replace(0, x['farm_irrigation_type'].mode()[0]))
    .assign(farm_farming_season = lambda x: x['farm_farming_season'].astype(int).replace(0, x['farm_farming_season'].mode()[0]))
    .assign(farm_house_type = lambda x: x['farm_house_type'].astype(int).replace(0, x['farm_house_type'].mode()[0]))
    .assign(farm_plantations_type = lambda x: x['farm_plantations_type'].astype(int).replace(0, x['farm_plantations_type'].mode()[0]))
    .pipe(
        get_dummies,
        columns=[
            "farm_main_crops_type",
            "farm_activity_status",
            "farm_type",
            "farm_irrigation_source",
            "farm_irrigation_type",
            "farm_farming_season",
            "farm_house_type",
            "farm_plantations_type"
        ],
        dtype=int,
    )
    .groupby("farm_id")
    .apply(count_non_zero_non_nan)
    .drop(
        columns=[
            "farm_id",
            "farm_x",
            "farm_y",
            "activity_id",
            "farm_crops_type",
            "farm_activity_area_hectares",
            "farm_trees_count",
            "farm_house_count",
            "farm_plantations_count",
            # "farm_plantations_type",
            "farm_activity_length_m",
            "farm_activity_area_sq_m"
            
        ]
    )
    .reset_index()
    )

    df_farms_sum = (
        df_farms.rename(
            columns={
                "HSRCode": "activity_id",
                "OB_HSRCode": "farm_id",
                "ActivityStatus": "farm_activity_status",
                "FarmType": "farm_type",
                "MainCropsType": "farm_main_crops_type",
                "CropsType": "farm_crops_type",
                "IrragationSource": "farm_irrigation_source",
                "IrragationType": "farm_irrigation_type",
                "FarmingSeason": "farm_farming_season",
                "TotalArea": "farm_activity_area_hectares",
                "ProductiveTreesNo": "farm_trees_count",
                "ProtectedHouseNo": "farm_house_count",
                "ProtectedHouseType": "farm_house_type",
                "PlantationsNo": "farm_plantations_count",
                "X": "farm_x",
                "Y": "farm_y",
                "SHAPE_Length": "farm_activity_length_m",
                "SHAPE_Area": "farm_activity_area_sq_m",
                "geometry": "farm_geometry",
                "PlantationsType": "farm_plantations_type",
            }
        )
        .drop_duplicates()
        .fillna(0)
        .groupby("farm_id")
        .agg({
            "farm_crops_type": "nunique",
            "farm_activity_status": "nunique",
            "farm_type": "nunique",
            "farm_irrigation_source": "nunique",
            "farm_irrigation_type": "nunique",
            "farm_activity_area_hectares": "sum",
            "farm_trees_count": "sum",
            "farm_house_count": "sum",
            "farm_plantations_count": "sum",
            # "farm_plantations_type": "nunique",
            "farm_activity_length_m": "sum",
            "farm_activity_area_sq_m": "sum",
        })
        .reset_index()
    )

    df_farms_count = df_farms_count.drop(columns=['farm_house_type_0'])
    df_farms = df_farms_sum.merge(df_farms_count, on="farm_id", how="inner")
    df_farms = df_farms.rename(columns={"farm_crops_type":"main_crop_type"})
    return df_farms