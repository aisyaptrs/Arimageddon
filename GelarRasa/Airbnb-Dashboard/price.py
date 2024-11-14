# Import library yang diperlukan
import streamlit as st
import pandas as pd
import pickle

# Muat model yang telah disimpan
with open(r"C:\Users\Aisya\Downloads\GelarRasa\Airbnb-Dashboard\airbnb_price_predictor_ensemble.sav", 'rb') as model_file:
    model = pickle.load(model_file)

# Judul aplikasi
st.title("Airbnb Price Prediction")

# Input dari pengguna
st.header("Input Features")
accommodates = st.number_input("Accommodates", min_value=1, max_value=10, step=1)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, step=1)
minimum_nights = st.number_input("Minimum Nights", min_value=1, max_value=30, step=1)
maximum_nights = st.number_input("Maximum Nights", min_value=1, max_value=100, step=1)
review_scores_rating = st.slider("Review Scores Rating", min_value=0, max_value=100, step=1)
review_scores_cleanliness = st.slider("Review Scores Cleanliness", min_value=0, max_value=10, step=1)
review_scores_location = st.slider("Review Scores Location", min_value=0, max_value=10, step=1)
host_total_listings_count = st.number_input("Host Total Listings Count", min_value=1, max_value=100, step=1)
host_response_rate = st.slider("Host Response Rate", min_value=0.0, max_value=1.0, step=0.01)

# Buat DataFrame dari input pengguna
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

# Tombol untuk prediksi
if st.button("Predict Price"):
    # Prediksi harga menggunakan model yang telah dilatih
    price_prediction = model.predict(input_data)
    st.write(f"Predicted Price: ${price_prediction[0]:,.2f}")
