# streamlit_app.py

import streamlit as st

st.title("Farm Data Input App")

# Property Section
st.header("Property Information")

# Property Area
property_area = st.number_input(
    "What is the total area of your property (in hectares)?",
    min_value=0.0,
    step=0.1,
)

# Property Main Type Code
property_main_type_options = {
    1: "زراعي غير عضوي",
    2: "حيواني",
    3: "مختلط",
    4: "منشآت وخدمات مساندة",
    5: "زراعي عضوي",
}
property_main_type = st.selectbox(
    "Please select the main type of your property:",
    options=list(property_main_type_options.keys()),
    format_func=lambda x: property_main_type_options[x],
)

# Activity Section
st.header("Activity Information")

# Total Farm Area
activity_total_area_hectares = st.number_input(
    "What is the total cultivated area of your farm (in hectares)?",
    min_value=0.0,
    step=0.1,
)

# Number of Farming Activities
activity_count = st.number_input(
    "How many different farming activities are you conducting on your farm?",
    min_value=0,
    step=1,
)

# Number of Unique Crop Types
activity_unique_crop_types_count = st.number_input(
    "How many unique crop types are you cultivating?",
    min_value=0,
    step=1,
)

# Productive Trees Count
activity_productive_trees_count = st.number_input(
    "How many productive trees are present on your farm?",
    min_value=0,
    step=1,
)

# Protected House Count
activity_protected_house_count = st.number_input(
    "How many protected houses (e.g., greenhouses) are there on your farm?",
    min_value=0,
    step=1,
)

# Protected House Type Codes
activity_protected_house_type_options = {
    1.0: "بلاستيك عادي",
    2.0: "بلاستيك مكيف",
    3.0: "زجاج زراعة بالتربة",
    4.0: "فايبر جلاس زراعة بالتربة",
    6.0: "زجاج زراعة مائية",
    7.0: "فايبر جلاس زراعة مائية",
}
activity_protected_house_type_codes = st.multiselect(
    "Please select the protected house type codes:",
    options=list(activity_protected_house_type_options.keys()),
    format_func=lambda x: f"{x} - {activity_protected_house_type_options[x]}",
)

# Plantations Count
activity_plantations_count = st.number_input(
    "How many plantations are there on your farm?",
    min_value=0,
    step=1,
)

# Plantations Type Codes
activity_plantations_type_options = {
    1.0: "تباتات زينة",
    2.0: "أشجار",
    3.0: "خضروات",
}
activity_plantations_type_codes = st.multiselect(
    "Please select the plantations type codes:",
    options=list(activity_plantations_type_options.keys()),
    format_func=lambda x: f"{x} - {activity_plantations_type_options[x]}",
)

# Activity Status Codes
activity_status_options = {
    1: "قائم",
    3: "متوقف حالياً",
}
activity_status_codes = st.multiselect(
    "Please select the activity status codes applicable to your farm:",
    options=list(activity_status_options.keys()),
    format_func=lambda x: f"{x} - {activity_status_options[x]}",
)

# Activity Type Codes
activity_type_options = {
    1.0: "زراعة بالغمر",
    2.0: "جهاز ري محوري",
    5.0: "بيوت محمية",
    6.0: "أشجار النخيل",
    7.0: "أشجار دائمة",
    10.0: "مشاتل",
    11.0: "الزراعة المكشوفة",
}
activity_type_codes = st.multiselect(
    "Please select the activity type codes that describe your farm:",
    options=list(activity_type_options.keys()),
    format_func=lambda x: f"{x} - {activity_type_options[x]}",
)

# Main Crop Type Codes
farm_main_crop_type_options = {
    1.0: "أعلاف",
    2.0: "تمور",
    3.0: "فواكه",
    4.0: "خضروات",
    5.0: "ورقيات",
    6.0: "قمح",
    7.0: "قمح بلدي",
    8.0: "شعير",
    9.0: "ذرة",
    10.0: "زيتون",
    12.0: "مورينقا",
    13.0: "منتجات عضوية",
    14.0: "شتلات أو أشجار زينة",
    15.0: "لا يوجد",
}
farm_main_crop_type_codes = st.multiselect(
    "Please select the main crop type codes for your farm:",
    options=list(farm_main_crop_type_options.keys()),
    format_func=lambda x: f"{x} - {farm_main_crop_type_options[x]}",
)

# Irrigation Source Codes
activity_irrigation_source_options = {
    1.0: "بئر عادي",
    2.0: "بئر ارتوازي",
    4.0: "بئر مشترك",
    5.0: "مياه معالجة",
    6.0: "شبكة ري عامة",
    7.0: "صهريج ماء",
    10.0: "أمطار",
    12.0: "لا يوجد",
}
activity_irrigation_source_codes = st.multiselect(
    "Please select the irrigation source codes used on your farm:",
    options=list(activity_irrigation_source_options.keys()),
    format_func=lambda x: f"{x} - {activity_irrigation_source_options[x]}",
)

# Irrigation Type Codes
activity_irrigation_type_options = {
    1.0: "ري محوري",
    2.0: "ري بالغمر",
    3.0: "ري بالتنقيط",
    4.0: "مطرية",
    6.0: "لا يوجد",
    7.0: "ري مدفعي",
}
activity_irrigation_type_codes = st.multiselect(
    "Please select the irrigation type codes used on your farm:",
    options=list(activity_irrigation_type_options.keys()),
    format_func=lambda x: f"{x} - {activity_irrigation_type_options[x]}",
)

# Farming Season Codes
activity_farming_season_options = {
    1.0: "صيف",
    2.0: "شتاء",
    3.0: "طوال العام",
    4.0: "لا يوجد",
}
activity_farming_season_codes = st.multiselect(
    "Please select the farming season codes applicable to your farm:",
    options=list(activity_farming_season_options.keys()),
    format_func=lambda x: f"{x} - {activity_farming_season_options[x]}",
)

# Sprinklers Count
sprinklers_count = st.number_input(
    "How many sprinklers are there on your farm?",
    min_value=0,
    step=1,
)

# Sprinklers Total kW
sprinklers_count_kw = st.number_input(
    "What is the total kilowatt (kW) capacity of the sprinklers on your farm?",
    min_value=0.0,
    step=0.1,
)

# Wells Section
st.header("Wells Information")

# Number of Wells on the Farm
well_count = st.number_input(
    "How many wells are associated with your farm?",
    min_value=0,
    step=1,
)

well_possession_type_options = {
    1: "Owned",
    2: "Leased",
}
well_is_active_options = {
    1: "قائم",
    2: "متوقف حالياً",
}
well_irrigation_source_options = {
    1.0: "بئر عادي",
    2.0: "بئر ارتوازي",
    4.0: "بئر مشترك",
    5.0: "مياه معالجة",
    6.0: "شبكة ري عامة",
    7.0: "صهريج ماء",
    10.0: "أمطار",
    12.0: "لا يوجد",
}
well_irrigation_type_options = {
    1.0: "ري محوري",
    2.0: "ري بالغمر",
    3.0: "ري بالتنقيط",
    4.0: "مطرية",
    6.0: "لا يوجد",
    7.0: "ري مدفعي",
}

if well_count > 0:
    st.subheader("Well Details")

    # Initialize dictionaries to hold counts of each code
    well_possession_type_counts = {}
    well_is_active_counts = {}
    well_irrigation_source_counts = {}
    well_irrigation_type_counts = {}

    # For each well, collect the details
    for i in range(int(well_count)):
        st.markdown(f"**Well {i + 1} Details**")

        # Well Possession Type Code
        well_possession_type = st.selectbox(
            f"Well {i + 1}: Please select the possession type code:",
            options=list(well_possession_type_options.keys()),
            format_func=lambda x: f"{x} - {well_possession_type_options[x]}",
            key=f"well_possession_type_{i}",
        )
        # Update counts
        well_possession_type_counts[well_possession_type] = well_possession_type_counts.get(well_possession_type, 0) + 1

        # Well Active Status Code
        well_is_active = st.selectbox(
            f"Well {i + 1}: Please select the active status code:",
            options=list(well_is_active_options.keys()),
            format_func=lambda x: f"{x} - {well_is_active_options[x]}",
            key=f"well_is_active_{i}",
        )
        # Update counts
        well_is_active_counts[well_is_active] = well_is_active_counts.get(well_is_active, 0) + 1

        # Well Irrigation Source Codes
        well_irrigation_source_codes = st.multiselect(
            f"Well {i + 1}: Please select the irrigation source codes:",
            options=list(well_irrigation_source_options.keys()),
            format_func=lambda x: f"{x} - {well_irrigation_source_options[x]}",
            key=f"well_irrigation_source_{i}",
        )
        # Update counts
        for code in well_irrigation_source_codes:
            well_irrigation_source_counts[code] = well_irrigation_source_counts.get(code, 0) + 1

        # Well Irrigation Type Codes
        well_irrigation_type_codes = st.multiselect(
            f"Well {i + 1}: Please select the irrigation type codes:",
            options=list(well_irrigation_type_options.keys()),
            format_func=lambda x: f"{x} - {well_irrigation_type_options[x]}",
            key=f"well_irrigation_type_{i}",
        )
        # Update counts
        for code in well_irrigation_type_codes:
            well_irrigation_type_counts[code] = well_irrigation_type_counts.get(code, 0) + 1

# Additional Information Section
st.header("Additional Information")

st.markdown("The following features will be calculated from your inputs:")

st.markdown("- **Trees per Hectare**: Calculated as `activity_productive_trees_count / activity_total_area_hectares`")
st.markdown("- **Irrigation Intensity**: Calculated if `activity_irrigation_type_2.0` is selected")
st.markdown("- **Well Density**: Calculated as `well_count / activity_total_area_hectares`")
st.markdown("- **Area per Activity**: Calculated as `activity_total_area_hectares / activity_count`")
st.markdown("- **Sprinklers Total kW**: Calculated as `sprinklers_count * 25` if not provided")

# Submit Button
if st.button("Submit"):
    st.success("Data submitted successfully!")

    # Collecting all data into a dictionary
    collected_data = {
        "property_area": property_area,
        "property_main_type": property_main_type,
        "activity_total_area_hectares": activity_total_area_hectares,
        "activity_count": activity_count,
        "activity_unique_crop_types_count": activity_unique_crop_types_count,
        "activity_productive_trees_count": activity_productive_trees_count,
        "activity_protected_house_count": activity_protected_house_count,
        "activity_protected_house_type_codes": activity_protected_house_type_codes,
        "activity_plantations_count": activity_plantations_count,
        "activity_plantations_type_codes": activity_plantations_type_codes,
        "activity_status_codes": activity_status_codes,
        "activity_type_codes": activity_type_codes,
        "farm_main_crop_type_codes": farm_main_crop_type_codes,
        "activity_irrigation_source_codes": activity_irrigation_source_codes,
        "activity_irrigation_type_codes": activity_irrigation_type_codes,
        "activity_farming_season_codes": activity_farming_season_codes,
        "sprinklers_count": sprinklers_count,
        "sprinklers_count_kw": sprinklers_count_kw,
        "well_count": well_count,
    }

    if well_count > 0:
        collected_data["well_possession_type_counts"] = well_possession_type_counts
        collected_data["well_is_active_counts"] = well_is_active_counts
        collected_data["well_irrigation_source_counts"] = well_irrigation_source_counts
        collected_data["well_irrigation_type_counts"] = well_irrigation_type_counts

    # Calculated Features
    calculated_features = {}

    # Trees per Hectare
    if activity_total_area_hectares > 0:
        calculated_features["trees_per_hectare"] = (
            activity_productive_trees_count / activity_total_area_hectares
        )
        calculated_features["well_density"] = well_count / activity_total_area_hectares
        calculated_features["area_per_activity"] = activity_total_area_hectares / activity_count if activity_count > 0 else 0
    else:
        calculated_features["trees_per_hectare"] = 0
        calculated_features["well_density"] = 0
        calculated_features["area_per_activity"] = 0

    # Irrigation Intensity
    if 2.0 in activity_irrigation_type_codes:
        calculated_features["irrigation_intensity"] = activity_total_area_hectares
    else:
        calculated_features["irrigation_intensity"] = 0

    # Sprinklers Total kW (if not provided)
    if sprinklers_count_kw == 0 and sprinklers_count > 0:
        calculated_features["sprinklers_count_kw"] = sprinklers_count * 25
    else:
        calculated_features["sprinklers_count_kw"] = sprinklers_count_kw

    # Displaying the collected data
    st.write("Collected Data:")
    st.json(collected_data)

    st.write("Calculated Features:")
    st.json(calculated_features)

    # Here, you can proceed to process the data as required
    # For example, encode categorical variables, calculate percentages, etc.
