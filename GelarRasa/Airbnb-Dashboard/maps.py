import streamlit as st
import pandas as pd
import pydeck as pdk

# Load data
data = pd.read_csv(r"C:\Users\Aisya\Downloads\GelarRasa\Airbnb-Dashboard\listings.csv", sep=';')

# Filter data untuk distrik dan neighbourhood tertentu (opsional)
district_filter = st.selectbox("Pilih distrik", data['district'].unique())
filtered_data = data[data['district'] == district_filter]

# Menampilkan neighbourhood yang sesuai dengan distrik
neighbourhood_filter = st.multiselect("Pilih neighbourhood", filtered_data['neighbourhood'].unique())
if neighbourhood_filter:
    filtered_data = filtered_data[filtered_data['neighbourhood'].isin(neighbourhood_filter)]

# Membuat peta menggunakan pydeck
st.write(f"Menampilkan peta untuk distrik: {district_filter}")
view_state = pdk.ViewState(
    latitude=filtered_data['latitude'].mean(),
    longitude=filtered_data['longitude'].mean(),
    zoom=10,
    pitch=50
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_data,
    get_position='[longitude, latitude]',
    get_color='[200, 30, 0, 160]',
    get_radius=100,
    pickable=True
)

# Render peta di Streamlit
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{listing_name}\nPrice: ${price}"})
st.pydeck_chart(r)
