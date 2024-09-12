import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.base import BaseEstimator, RegressorMixin


st.set_page_config( page_title="مشروع تقدير الأحمال في المزارع", page_icon="MOE_logo.png")
st.image("MOE_logo.png", width=150)
    
# Define NonNegativeRegressor class
class NonNegativeRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, base_estimator):
        self.base_estimator = base_estimator

    def fit(self, X, y):
        self.base_estimator.fit(X, y)
        return self

    def predict(self, X):
        predictions = self.base_estimator.predict(X)
        return np.maximum(predictions, 0)

# Import functions from HASAR Farm Consumption Inference Script
def inference(pipeline_data, new_data):
    pipeline = pipeline_data['pipeline']
    feature_names = pipeline_data['feature_names']

    # Ensure new_data has all the required features
    for feature in feature_names:
        if feature not in new_data.columns:
            new_data[feature] = 0  # or any appropriate default value

    # Select only the features used during training
    new_data = new_data[feature_names]

    # Make predictions
    predictions = pipeline.predict(new_data)

    return predictions

# Load the saved pipeline
@st.cache_resource
def cached_load_pipeline(file_path):
    return joblib.load(file_path)

pipeline_data = cached_load_pipeline('hasar_farm_pipeline.joblib')

st.title('تقدير أحمال المزارع: حل مصغر')

st.write("""
This app estimates the electrical consumption of a farm based on various features.
Please input the farm's characteristics below.
""")

# Create input fields for each feature, rearranged
st.subheader("بيانات الأنشطة")
total_area = st.number_input('مساحة الأنشطة (هكتار)', min_value=0.0, value=10.0, step=0.00001)
property_area = st.number_input('مساحة المزرعة', min_value=0.0, value=1000.0)
activity_count = st.number_input('عدد الأنشطة', min_value=0, value=2)

st.subheader("بيانات المحصول")
unique_crop_types = st.number_input('عدد المحاصيل المختلفة', min_value=0, value=2)
main_crop_type_6 = st.number_input('عدد الأنشطة التي تنتج قمح', min_value=0, max_value=1, value=0, step=1)
main_crop_type_15 = st.number_input('عدد الأنشطة التي تنتج محاصيل متنوعة', min_value=0, max_value=1, value=0, step=1)

st.subheader("بيانات الأشجار")
productive_trees = st.number_input('عدد الأشجار والنخيل', min_value=0, value=100)

st.subheader("بيانات الري")
irrigation_source_2 = st.number_input('عدد الأنشطة التي تتغذى من بئر ارتوازي', min_value=0, value=0, step=1)
irrigation_type_2 = st.number_input('عدد الأنشطة التي تعتمد على الري بالغمر', min_value=0, value=0, step=1)
irrigation_type_4 = st.number_input('عدد الأنشطة التي تعتمد على الري بمياه الأمطار', min_value=0, value=0, step=1)


if st.button('حساب الحمل المتوقع للمزرعة'):
    # Create a DataFrame with the input data
    new_data = pd.DataFrame({
        'total_area_hectares': [total_area],
        'property_area': [property_area],
        'unique_crop_types_count': [unique_crop_types],
        'main_crop_type_6.0': [main_crop_type_6],
        'main_crop_type_15.0': [main_crop_type_15],
        'productive_trees_count': [productive_trees],
        'irrigation_source_2.0': [irrigation_source_2],
        'irrigation_type_2.0': [irrigation_type_2],
        'irrigation_type_4.0': [irrigation_type_4],
        'activity_count': [activity_count]
    })

    # Make prediction using the imported inference function
    prediction = inference(pipeline_data, new_data)[0]

    # Display the result
    # st.success(f'Estimated Electrical Consumption: {prediction:.2f} kW')
    st.metric(
            label="الاستهلاك المتوقع للمزرعة",
            value=f"{prediction:.2f} كيلوواط",
            delta_color="inverse"
        )

    


