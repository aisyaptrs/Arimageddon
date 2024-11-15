import streamlit as st
import pandas as pd
import pickle
import shap
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Styling
st.set_page_config(page_title="Airbnb Price Prediction", page_icon="🏠", layout="wide")
st.markdown(
    """
    <style>
    .main-title {font-size: 36px; color: #000000; font-weight: bold;}
    .sub-title {font-size: 24px; color: #117A65;}
    .highlight {color: #E74C3C; font-weight: bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to display SHAP plots in HTML format
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

# Load the saved model
with open('GelarRasa/Airbnb-Dashboard/airbnb_price_predictor_xgb.sav', 'rb') as model_file:
    model = pickle.load(model_file)

# App title
st.markdown('<p class="main-title">Airbnb Price Prediction🏡</p>', unsafe_allow_html=True)

# Sidebar for input
st.sidebar.header("🔧 Input Features")
accommodates = st.sidebar.number_input("Accommodates", min_value=0, max_value=10, step=1)
bedrooms = st.sidebar.number_input("Bedrooms", min_value=0, max_value=10, step=1)
minimum_nights = st.sidebar.number_input("Minimum Nights", min_value=0, max_value=30, step=1)
maximum_nights = st.sidebar.number_input("Maximum Nights", min_value=0, max_value=100, step=1)
review_scores_rating = st.sidebar.slider("Review Scores Rating", min_value=0, max_value=100, step=1)
review_scores_cleanliness = st.sidebar.slider("Review Scores Cleanliness", min_value=0, max_value=10, step=1)
review_scores_location = st.sidebar.slider("Review Scores Location", min_value=0, max_value=10, step=1)
host_total_listings_count = st.sidebar.number_input("Host Total Listings Count", min_value=0, max_value=100, step=1)
host_response_rate = st.sidebar.slider("Host Response Rate", min_value=0.0, max_value=1.0, step=0.01)

# Create three tabs
tab1, tab2, tab3 = st.tabs(["🏡 Prediction", "📊 Methodology", "🔍 SHAP Analysis"])

# Initialize input_data as an empty DataFrame
input_data = pd.DataFrame()

with tab1:
    st.markdown('<p class="sub-title">Price Prediction 💵</p>', unsafe_allow_html=True)

    # Validation check for inputs
    if st.button("Predict Price 🚀"):
        if minimum_nights > maximum_nights:
            st.error("⚠️ Minimum Nights cannot be greater than Maximum Nights. Please adjust the values.")
        elif (accommodates == 0 or bedrooms == 0 or minimum_nights == 0 or maximum_nights == 0 or 
              review_scores_rating == 0 or review_scores_cleanliness == 0 or review_scores_location == 0 or
              host_total_listings_count == 0 or host_response_rate == 0):
            st.warning("⚠️ Please ensure all features have a value greater than 0.")
        else:
            # Create a DataFrame from user inputs
            input_data = pd.DataFrame({
                'accommodates': [accommodates],
                'bedrooms': [bedrooms],
                'minimum_nights': [minimum_nights],
                'maximum_nights': [maximum_nights],
                'review_scores_rating': [review_scores_rating],
                'review_scores_cleanliness': [review_scores_cleanliness],
                'review_scores_location': [review_scores_location],
                'host_total_listings_count': [host_total_listings_count],
                'host_response_rate': [host_response_rate]
            })

            # Make a prediction
            price_prediction = model.predict(input_data)
            
            # Display prediction result directly below the button
            st.write("### Predicted Price")
            st.write(f"💲 **${price_prediction[0]:,.2f}**")

with tab2:
    st.markdown('<p class="sub-title">Methodology 📈</p>', unsafe_allow_html=True)
    with st.expander("Learn More About the Model"):
        st.write("""
        ### Model: XGBoost Regressor
        XGBoost is a powerful and popular decision-tree-based algorithm for prediction. 
        It uses a boosting method that builds models iteratively to minimize errors and improve prediction accuracy.
        
        - **Mean Squared Error (MSE):** 2656.96 — Lower MSE indicates a better model.
        - **R-squared Score (R²):** 0.8467 — A score closer to 1 indicates a highly accurate model.
        """)

with tab3:
    st.markdown('<p class="sub-title">SHAP Value Analysis 🔍</p>', unsafe_allow_html=True)
    st.write("""
    SHAP (SHapley Additive exPlanations) is a technique to explain predictions. 
    It shows the contribution of each feature to the final prediction.
    """)
    # Ensure input_data is not empty before proceeding with SHAP analysis
    if not input_data.empty:
        # SHAP analysis
        explainer = shap.Explainer(model)
        shap_values = explainer(input_data)

        # Display SHAP force plot for the first prediction
        st.subheader("SHAP Force Plot for Prediction")
        expected_value = explainer.expected_value[0] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value
        st_shap(shap.force_plot(expected_value, shap_values.values[0], input_data))

        # Display SHAP summary plot for the input_data
        st.subheader("SHAP Summary Plot")
        fig_summary, ax_summary = plt.subplots()
        shap.summary_plot(shap_values, input_data, plot_type="bar", show=False)
        st.pyplot(fig_summary)
    else:
        st.warning("⚠️ Please enter valid input features and run the prediction first.")
