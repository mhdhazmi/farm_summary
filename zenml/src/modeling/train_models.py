# src/modeling/train_models.py

import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from src.utils.helpers import OutlierCapper
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

def train_and_log_model(model_name, pipeline, param_grid, X_train, y_train, X_test, y_test, cv, n_iter=10):
    with mlflow.start_run(run_name=model_name):
        mlflow.log_param("model_name", model_name)
        input_example = X_train.iloc[:1]

        # Perform RandomizedSearchCV
        search = RandomizedSearchCV(
            pipeline,
            param_distributions=param_grid,
            n_iter=n_iter,
            cv=cv,
            scoring='neg_mean_squared_error',
            random_state=42,
            n_jobs=-1
        )
        search.fit(X_train, y_train)

        # Log best parameters
        mlflow.log_params(search.best_params_)

        # Make predictions
        y_pred_log = search.predict(X_test)
        y_pred = np.expm1(y_pred_log)
        y_test_actual = np.expm1(y_test)

        # Calculate metrics
        mae = mean_absolute_error(y_test_actual, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred))
        r2 = r2_score(y_test_actual, y_pred)

        # Log metrics
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2_Score", r2)

        # Infer model signature
        signature = infer_signature(input_example, y_pred[:1])

        # Log the model with signature and input_example
        mlflow.sklearn.log_model(
            search.best_estimator_,
            artifact_path=model_name,
            signature=signature,
            input_example=input_example
        )

        print(f"Logged {model_name} with MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.4f}")

        return search.best_estimator_

def train_and_log_stacking(model_name, stacking_regressor, X_train, y_train, X_test, y_test, cv):
    with mlflow.start_run(run_name=model_name):
        mlflow.log_param("model_name", model_name)
        input_example = X_train.iloc[:1]

        # Fit the stacking regressor
        stacking_regressor.fit(X_train, y_train)

        # Make predictions
        y_pred_log = stacking_regressor.predict(X_test)
        y_pred = np.expm1(y_pred_log)
        y_test_actual = np.expm1(y_test)

        # Calculate metrics
        mae = mean_absolute_error(y_test_actual, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred))
        r2 = r2_score(y_test_actual, y_pred)

        # Log metrics
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2_Score", r2)

        # Infer model signature
        signature = infer_signature(input_example, y_pred[:1])

        # Log the model with signature and input_example
        mlflow.sklearn.log_model(
            stacking_regressor,
            artifact_path=model_name,
            signature=signature,
            input_example=input_example
        )

        print(f"Logged {model_name} with MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.4f}")

        return stacking_regressor

