import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load data dari file Parquet
data = pd.read_parquet(GelarRasa/Airbnb-Dashboard/listings.parquet")

# Filter data untuk distrik dan neighbourhood tertentu (opsional)
st.title("🌎 Explore Airbnb Listings")
st.markdown(
    'Use the filters below to narrow your search by district and neighborhood! '
    'By default, all listings in New York that match your search criteria will be displayed.'
)

# Filter untuk distrik
district_filter = st.selectbox("**Select District**", list(data['district'].unique()), index=0)

# Filter data berdasarkan distrik yang dipilih
if district_filter == "":
    filtered_data = data[data['city'] == "New York"]
else:
    filtered_data = data[(data['district'] == district_filter) & (data['city'] == "New York")]

# Menampilkan jumlah total listing setelah memilih district
total_listings_district = len(filtered_data)
st.markdown(f"##### Total Listings in {district_filter}: {total_listings_district} 🏠")

# Filter untuk neighbourhood (hanya tampil jika distrik sudah dipilih)
filtered_data = filtered_data.dropna(subset=['listings_name', 'price', 'latitude', 'longitude'])
neighbourhood_filter = st.multiselect("**Select neighbourhood** (1 or more)", filtered_data['neighbourhood'].unique())

# Filter data berdasarkan neighbourhood yang dipilih
if neighbourhood_filter:
    filtered_data = filtered_data[filtered_data['neighbourhood'].isin(neighbourhood_filter)]

# Menampilkan jumlah total listing setelah memilih neighborhood
total_listings_neighborhood = len(filtered_data)
st.markdown(f"##### Total Listings in Selected neighbourhood(s): {total_listings_neighborhood} 🏠")

# Buat peta dengan folium
if not filtered_data.empty:
    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=11)

    # Tambahkan marker dengan informasi tambahan pada setiap listing
    for idx, row in filtered_data.iterrows():
        popup_content = f"""
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            td {{
                padding: 4px;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
                text-align: left;
                padding: 4px;
            }}
        </style>
        <table>
            <tr><th colspan="2">{row['listings_name']}</th></tr>
            <tr><td><strong>Price</strong></td><td>${row['price']}</td></tr>
            <tr><td><strong>Property Type</strong></td><td>{row['property_type']}</td></tr>
            <tr><td><strong>Room Type</strong></td><td>{row['room_type']}</td></tr>
            <tr><td><strong>Accommodates</strong></td><td>{row['accommodates']}</td></tr>
            <tr><td><strong>Bedrooms</strong></td><td>{row['bedrooms']}</td></tr>
            <tr><td><strong>Minimum Nights</strong></td><td>{row['minimum_nights']}</td></tr>
            <tr><td><strong>Maximum Nights</strong></td><td>{row['maximum_nights']}</td></tr>
            <tr><td><strong>Instant Bookable</strong></td><td>{"Yes" if row['instant_bookable'] else "No"}</td></tr>
        </table>
        """

        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=popup_content,
            tooltip=row['listings_name'],
            icon=folium.Icon(icon="home", prefix="fa", color="blue")  # ikon rumah dengan warna biru
        ).add_to(m)

    # Tampilkan peta di Streamlit
    st.write(f"### Showing map for district: **{district_filter}**")
    st_folium(m, width=700, height=500)

else:
    st.markdown("### No listings found for the selected district and neighborhood(s). Try adjusting the filters!")
