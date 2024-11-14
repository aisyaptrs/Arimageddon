import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load the data (gunakan os.path untuk mengelola path file lebih fleksibel)
listings = pd.read_parquet(r'C:\Users\Aisya\Downloads\GelarRasa\Airbnb-Dashboard\listings.parquet')
reviews = pd.read_parquet(r'C:\Users\Aisya\Downloads\GelarRasa\Airbnb-Dashboard\reviews.parquet')
hosts = pd.read_parquet(r'C:\Users\Aisya\Downloads\GelarRasa\Airbnb-Dashboard\hosts.parquet')

st.sidebar.title("Airbnb Dashboard Analysis")
st.sidebar.success("Select Page Above")

st.title("✨ Airbnb Dashboard Analysis ✨")
st.write("""### *Analysis, Visualization, and Prediction*""")

st.subheader("📃 Pages at a Glance")
st.markdown('''
            The dashboard provides a deep analysis and predictive insights into the Airbnb dataset. It offers users an interactive platform to explore data trends, understand spatial distribution, and forecast pricing. By combining statistical analysis, spatial visualization, and machine learning, this dashboard is designed to assist hosts, guests, and market analysts in making informed decisions based on Airbnb data.                  

            There are 3 dashboard pages that can be accessed on the sidebar on the left, namely:
            - 📊 Exploration: Exploratory Data Analysis (EDA)
            - 🗺️ Map: Spatial Overview of Listing
            - 📈 Price Prediction: Price Prediction
            ''')

# Dataset Overview
st.subheader("📂 Dataset Overview")
st.write("This dataset includes Airbnb listings, reviews, and host data.")

# Key metrics
total_areas = listings['district'].nunique()  # Unique cities
total_listings = listings['listing_id'].nunique()  # Unique listings
total_neighborhoods = listings['neighbourhood'].nunique()
total_reviews = reviews['review_id'].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Districts", total_areas)
col2.metric("Neighborhoods", total_neighborhoods)
col3.metric("Listings", total_listings)
col4.metric("Total Reviews", total_reviews)

# Listings by City
st.write("### 🌆 Listings by District")
city_counts = listings['district'].value_counts().reset_index()
city_counts.columns = ['district', 'Number of Listings']

# Plotly bar chart for listings by city
fig = px.bar(
    city_counts.head(10),  # Menampilkan 10 distrik teratas
    x='district',
    y='Number of Listings',
    title="Airbnb Listings by District in New York",
    color='Number of Listings',
    color_continuous_scale=["#ffc0cb", "#ffb3b3", "#ff8080", "#ff4d4d", "#ff0000"]
)
st.plotly_chart(fig, use_container_width=True)
