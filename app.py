# streamlit_app.py

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.mention import mention

# Set the page layout to wide and apply a custom theme
st.set_page_config(
    page_title="Farm Data Input App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to enhance the visual appeal
st.markdown("""
    <style>
        .main {
            background-color: #215c26;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stHeader, .stSubheader {
            color: #2E8B57;
        }
        .stTextInput>div>div>input {
            background-color: #e6f2ff;
        }
        .stSelectbox>div>div>div>select {
            background-color: #e6f2ff;
        }
        .stNumberInput>div>div>input {
            background-color: #e6f2ff;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 Farm Data Input App")
st.write("Please fill in the following information about your farm to help us better understand your agricultural activities.")

# Progress indicator
progress = st.progress(0)

# Property Section
st.header("🏠 Property Information")
st.write("Provide details about your property.")

with st.form(key='property_form'):
    cols = st.columns(2)

    # Property Area
    with cols[0]:
        property_area = st.number_input(
            "Property Area (hectares)",
            min_value=0.0,
            step=0.1,
            help="Total area of your property.",
        )

    # Property Main Type Code
    with cols[1]:
        property_main_type_options = {
            1: "زراعي غير عضوي",
            2: "حيواني",
            3: "مختلط",
            4: "منشآت وخدمات مساندة",
            5: "زراعي عضوي",
        }
        property_main_type = st.selectbox(
            "Property Main Type",
            options=list(property_main_type_options.keys()),
            format_func=lambda x: property_main_type_options[x],
            help="Select the main type of your property.",
        )

    # Submit Property Form
    submitted_property = st.form_submit_button("Save Property Information")
    if submitted_property:
        st.success("Property information saved.")
        progress.progress(20)

add_vertical_space(2)

# Activity Section
st.header("🚜 Activity Information")
st.write("Provide details about your farming activities.")

with st.form(key='activity_form'):
    # Common Activity Inputs
    st.subheader("General Activity Details")
    cols = st.columns(3)

    # Total Farm Area
    with cols[0]:
        activity_total_area_hectares = st.number_input(
            "Total Farm Area (hectares)",
            min_value=0.0,
            step=0.1,
            help="Total cultivated area of your farm.",
        )

    # Number of Farming Activities
    with cols[1]:
        activity_count = st.number_input(
            "Number of Farming Activities",
            min_value=0,
            step=1,
            help="Number of different farming activities on your farm.",
        )

    # Number of Unique Crop Types
    with cols[2]:
        activity_unique_crop_types_count = st.number_input(
            "Number of Unique Crop Types",
            min_value=0,
            step=1,
            help="Number of unique crop types you are cultivating.",
        )

    add_vertical_space(1)

    cols = st.columns(3)

    # Productive Trees Count
    with cols[0]:
        activity_productive_trees_count = st.number_input(
            "Productive Trees Count",
            min_value=0,
            step=1,
            help="Number of productive trees on your farm.",
        )

    # Protected House Count
    with cols[1]:
        activity_protected_house_count = st.number_input(
            "Protected House Count",
            min_value=0,
            step=1,
            help="Number of protected houses (e.g., greenhouses).",
        )

    # Plantations Count
    with cols[2]:
        activity_plantations_count = st.number_input(
            "Plantations Count",
            min_value=0,
            step=1,
            help="Number of plantations on your farm.",
        )

    add_vertical_space(1)

    # Protected House Type Codes
    st.subheader("Protected House Type Codes")
    activity_protected_house_type_options = {
        1.0: "بلاستيك عادي",
        2.0: "بلاستيك مكيف",
        3.0: "زجاج زراعة بالتربة",
        4.0: "فايبر جلاس زراعة بالتربة",
        6.0: "زجاج زراعة مائية",
        7.0: "فايبر جلاس زراعة مائية",
    }
    activity_protected_house_type_codes = st.multiselect(
        "Select Protected House Type Codes",
        options=list(activity_protected_house_type_options.keys()),
        format_func=lambda x: f"{x} - {activity_protected_house_type_options[x]}",
        help="Select the types of protected houses present on your farm.",
    )

    # Plantations Type Codes
    st.subheader("Plantations Type Codes")
    activity_plantations_type_options = {
        1.0: "تباتات زينة",
        2.0: "أشجار",
        3.0: "خضروات",
    }
    activity_plantations_type_codes = st.multiselect(
        "Select Plantations Type Codes",
        options=list(activity_plantations_type_options.keys()),
        format_func=lambda x: f"{x} - {activity_plantations_type_options[x]}",
        help="Select the types of plantations on your farm.",
    )

    # Sprinklers Inputs
    st.subheader("Sprinkler System Details")
    cols = st.columns(2)

    # Sprinklers Count
    with cols[0]:
        sprinklers_count = st.number_input(
            "Sprinklers Count",
            min_value=0,
            step=1,
            help="Number of sprinklers on your farm.",
        )

    # Sprinklers Total kW
    with cols[1]:
        sprinklers_count_kw = st.number_input(
            "Sprinklers Total kW",
            min_value=0.0,
            step=0.1,
            help="Total kilowatt capacity of the sprinkler system.",
        )

    # Submit Activity Form
    submitted_activity = st.form_submit_button("Save Activity Information")
    if submitted_activity:
        st.success("Activity information saved.")
        progress.progress(50)

add_vertical_space(2)

# Per-Activity Details
if activity_count > 0:
    st.header("📝 Per-Activity Details")
    st.write("Provide specific details for each farming activity.")

    activities = []

    for i in range(int(activity_count)):
        with st.expander(f"Activity {i + 1} Details", expanded=False):
            cols = st.columns(3)

            # Activity Status Code
            with cols[0]:
                activity_status_options = {
                    1: "قائم",
                    3: "متوقف حالياً",
                }
                activity_status_code = st.selectbox(
                    f"Status Code (Activity {i + 1})",
                    options=list(activity_status_options.keys()),
                    format_func=lambda x: f"{x} - {activity_status_options[x]}",
                    key=f"activity_status_code_{i}",
                    help="Select the status code for this activity.",
                )

            # Activity Type Code
            with cols[1]:
                activity_type_options = {
                    1.0: "زراعة بالغمر",
                    2.0: "جهاز ري محوري",
                    5.0: "بيوت محمية",
                    6.0: "أشجار النخيل",
                    7.0: "أشجار دائمة",
                    10.0: "مشاتل",
                    11.0: "الزراعة المكشوفة",
                }
                activity_type_code = st.selectbox(
                    f"Type Code (Activity {i + 1})",
                    options=list(activity_type_options.keys()),
                    format_func=lambda x: f"{x} - {activity_type_options[x]}",
                    key=f"activity_type_code_{i}",
                    help="Select the type code for this activity.",
                )

            # Farming Season Code
            with cols[2]:
                activity_farming_season_options = {
                    1.0: "صيف",
                    2.0: "شتاء",
                    3.0: "طوال العام",
                    4.0: "لا يوجد",
                }
                activity_farming_season_code = st.selectbox(
                    f"Farming Season (Activity {i + 1})",
                    options=list(activity_farming_season_options.keys()),
                    format_func=lambda x: f"{x} - {activity_farming_season_options[x]}",
                    key=f"activity_farming_season_code_{i}",
                    help="Select the farming season for this activity.",
                )

            cols = st.columns(3)

            # Main Crop Type Code
            with cols[0]:
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
                farm_main_crop_type_code = st.selectbox(
                    f"Main Crop Type (Activity {i + 1})",
                    options=list(farm_main_crop_type_options.keys()),
                    format_func=lambda x: f"{x} - {farm_main_crop_type_options[x]}",
                    key=f"farm_main_crop_type_code_{i}",
                    help="Select the main crop type for this activity.",
                )

            # Irrigation Source Code
            with cols[1]:
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
                activity_irrigation_source_code = st.selectbox(
                    f"Irrigation Source (Activity {i + 1})",
                    options=list(activity_irrigation_source_options.keys()),
                    format_func=lambda x: f"{x} - {activity_irrigation_source_options[x]}",
                    key=f"activity_irrigation_source_code_{i}",
                    help="Select the irrigation source for this activity.",
                )

            # Irrigation Type Code
            with cols[2]:
                activity_irrigation_type_options = {
                    1.0: "ري محوري",
                    2.0: "ري بالغمر",
                    3.0: "ري بالتنقيط",
                    4.0: "مطرية",
                    6.0: "لا يوجد",
                    7.0: "ري مدفعي",
                }
                activity_irrigation_type_code = st.selectbox(
                    f"Irrigation Type (Activity {i + 1})",
                    options=list(activity_irrigation_type_options.keys()),
                    format_func=lambda x: f"{x} - {activity_irrigation_type_options[x]}",
                    key=f"activity_irrigation_type_code_{i}",
                    help="Select the irrigation type for this activity.",
                )

            # Activity Crop Type Code
            activity_crop_type_options = {
                1.0: "نوع محصول 1",
                2.0: "نوع محصول 2",
                3.0: "نوع محصول 3",
                # Add more crop types as needed
            }
            activity_crop_type_code = st.selectbox(
                f"Crop Type (Activity {i + 1})",
                options=list(activity_crop_type_options.keys()),
                format_func=lambda x: f"{x} - {activity_crop_type_options[x]}",
                key=f"activity_crop_type_code_{i}",
                help="Select the crop type for this activity.",
            )

            # Collect activity data
            activity = {
                "activity_status_code": activity_status_code,
                "activity_type_code": activity_type_code,
                "farm_main_crop_type_code": farm_main_crop_type_code,
                "activity_irrigation_source_code": activity_irrigation_source_code,
                "activity_irrigation_type_code": activity_irrigation_type_code,
                "activity_farming_season_code": activity_farming_season_code,
                "activity_crop_type_code": activity_crop_type_code,
            }
            activities.append(activity)

    # Update progress
    progress.progress(70)

add_vertical_space(2)

# Wells Section
st.header("💧 Wells Information")
st.write("Provide details about the wells on your farm.")

with st.form(key='wells_form'):
    # Number of Wells on the Farm
    well_count = st.number_input(
        "Number of Wells",
        min_value=0,
        step=1,
        help="Number of wells associated with your farm.",
    )

    if well_count > 0:
        st.write("Provide details for each well.")

        # Initialize dictionaries to hold counts of each code
        well_possession_type_counts = {}
        well_is_active_counts = {}
        well_irrigation_source_counts = {}
        well_irrigation_type_counts = {}

        for i in range(int(well_count)):
            with st.expander(f"Well {i + 1} Details", expanded=False):
                cols = st.columns(2)

                # Well Possession Type Code
                with cols[0]:
                    well_possession_type_options = {
                        1: "Owned",
                        2: "Leased",
                    }
                    well_possession_type = st.selectbox(
                        f"Possession Type (Well {i + 1})",
                        options=list(well_possession_type_options.keys()),
                        format_func=lambda x: f"{x} - {well_possession_type_options[x]}",
                        key=f"well_possession_type_{i}",
                        help="Select the possession type code.",
                    )
                    well_possession_type_counts[well_possession_type] = well_possession_type_counts.get(well_possession_type, 0) + 1

                # Well Active Status Code
                with cols[1]:
                    well_is_active_options = {
                        1: "قائم",
                        2: "متوقف حالياً",
                    }
                    well_is_active = st.selectbox(
                        f"Active Status (Well {i + 1})",
                        options=list(well_is_active_options.keys()),
                        format_func=lambda x: f"{x} - {well_is_active_options[x]}",
                        key=f"well_is_active_{i}",
                        help="Select the active status code.",
                    )
                    well_is_active_counts[well_is_active] = well_is_active_counts.get(well_is_active, 0) + 1

                cols = st.columns(2)

                # Well Irrigation Source Codes
                with cols[0]:
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
                    well_irrigation_source_codes = st.multiselect(
                        f"Irrigation Source (Well {i + 1})",
                        options=list(well_irrigation_source_options.keys()),
                        format_func=lambda x: f"{x} - {well_irrigation_source_options[x]}",
                        key=f"well_irrigation_source_{i}",
                        help="Select irrigation source codes.",
                    )
                    for code in well_irrigation_source_codes:
                        well_irrigation_source_counts[code] = well_irrigation_source_counts.get(code, 0) + 1

                # Well Irrigation Type Codes
                with cols[1]:
                    well_irrigation_type_options = {
                        1.0: "ري محوري",
                        2.0: "ري بالغمر",
                        3.0: "ري بالتنقيط",
                        4.0: "مطرية",
                        6.0: "لا يوجد",
                        7.0: "ري مدفعي",
                    }
                    well_irrigation_type_codes = st.multiselect(
                        f"Irrigation Type (Well {i + 1})",
                        options=list(well_irrigation_type_options.keys()),
                        format_func=lambda x: f"{x} - {well_irrigation_type_options[x]}",
                        key=f"well_irrigation_type_{i}",
                        help="Select irrigation type codes.",
                    )
                    for code in well_irrigation_type_codes:
                        well_irrigation_type_counts[code] = well_irrigation_type_counts.get(code, 0) + 1

    # Submit Wells Form
    submitted_wells = st.form_submit_button("Save Wells Information")
    if submitted_wells:
        st.success("Wells information saved.")
        progress.progress(90)

add_vertical_space(2)

# Additional Information Section
st.header("ℹ️ Additional Information")
st.write("The following features will be calculated from your inputs:")

st.markdown("- **Trees per Hectare**: Calculated as `activity_productive_trees_count / activity_total_area_hectares`.")
st.markdown("- **Irrigation Intensity**: Calculated if `activity_irrigation_type_2.0` is selected in any activity.")
st.markdown("- **Well Density**: Calculated as `well_count / activity_total_area_hectares`.")
st.markdown("- **Area per Activity**: Calculated as `activity_total_area_hectares / activity_count`.")
st.markdown("- **Sprinklers Total kW**: Calculated as `sprinklers_count * 25` if not provided.")

add_vertical_space(2)

# Final Submit Button
if st.button("Finalize and Submit All Data"):
    st.success("All data submitted successfully! Thank you.")
    progress.progress(100)

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
        "sprinklers_count": sprinklers_count,
        "sprinklers_count_kw": sprinklers_count_kw,
        "well_count": well_count,
        "activities": activities,  # List of activity details
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
        calculated_features["area_per_activity"] = (
            activity_total_area_hectares / activity_count if activity_count > 0 else 0
        )
    else:
        calculated_features["trees_per_hectare"] = 0
        calculated_features["well_density"] = 0
        calculated_features["area_per_activity"] = 0

    # Irrigation Intensity
    irrigation_intensity = 0
    for activity in activities:
        if activity["activity_irrigation_type_code"] == 2.0:
            irrigation_intensity = activity_total_area_hectares
            break
    calculated_features["irrigation_intensity"] = irrigation_intensity

    # Sprinklers Total kW (if not provided)
    if sprinklers_count_kw == 0 and sprinklers_count > 0:
        calculated_features["sprinklers_count_kw"] = sprinklers_count * 25
    else:
        calculated_features["sprinklers_count_kw"] = sprinklers_count_kw

    # Displaying the collected data
    st.write("### Collected Data:")
    st.json(collected_data)

    st.write("### Calculated Features:")
    st.json(calculated_features)

    # You can proceed to process the data as required
    # For example, encode categorical variables, calculate percentages, etc.
