import pandas as pd

def get_dummies(df, columns, dtype):
    return pd.get_dummies(df, columns=columns, dtype=dtype, dummy_na=False, drop_first=False)

def count_non_zero_non_nan(df):
    return df.map(lambda x: x != 0).sum()
def wells_processing(df_wells):
    df_wells = (
        df_wells
        .drop_duplicates()
        .fillna(0)
        .rename(
                columns={
                    "HSRCode": "activity_id", 
                    "OB_HSRCode": "farm_id",
                    "activity_id": "well_activity_count",
                    "PossessionType": "well_possession_type",
                    "IsActive": "well_is_active",
                    "IrragationSource": "well_irrigation_source",
                    "IrrigationType": "well_irrigation_type",
                    "X": "well_x",
                    "Y": "well_y",
                    "Region": "well_region",
                    "geometry": "well_count",
                }
            )
        .assign(well_is_active = lambda x: x['well_is_active'].astype(int).replace(0,x['well_is_active'].mode()[0]))
        .assign(well_irrigation_source = lambda x: x['well_irrigation_source'].astype(int).replace(0,x['well_irrigation_source'].mode()[0]))
        .assign(well_irrigation_type = lambda x: x['well_irrigation_type'].astype(int).replace(0,x['well_irrigation_type'].mode()[0]))
        .pipe(get_dummies, columns=["well_possession_type", "well_is_active", "well_irrigation_source", "well_irrigation_type"], dtype=int)
        .groupby("farm_id")
        .apply(count_non_zero_non_nan)
        # # # .apply(lambda df: df.notna().astype(int).sum() - df.eq(0).sum())
        .drop(columns=["farm_id", "well_x", "well_y", "well_region"])
        .reset_index()
        
    )
    df_wells = df_wells.drop(index=0)
    df_wells = df_wells.drop(columns=['well_possession_type_2'])
    return df_wells