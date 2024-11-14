import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
# Load data from Parquet
listings = pd.read_parquet('GelarRasa/Airbnb-Dashboard/listings.parquet')
reviews = pd.read_parquet('GelarRasa/Airbnb-Dashboard/reviews.parquet')
hosts = pd.read_parquet('GelarRasa/Airbnb-Dashboard/hosts.parquet')
merged_data = pd.read_parquet(GelarRasa/Airbnb-Dashboard/all.parquet')

# Sidebar filter for city selection
st.title("📊 Exploratory Data Analysis (EDA)")
selected_city = st.selectbox("Which district would you like to explore?", ["All District"] + listings['district'].unique().tolist())

# Filter data based on the selected city
if selected_city != "All District":
    listings = listings[listings['district'] == selected_city]
    merged_data = merged_data[merged_data['district'] == selected_city]
    

# Tabbed layout for Overview, Pricing, and Review
tab1, tab2, tab3 = st.tabs(["Overview", "Pricing", "Reviews"])

# Konversi review_date menjadi datetime dengan dayfirst=True
merged_data['review_date'] = pd.to_datetime(merged_data['review_date'], dayfirst=True, errors='coerce')

# Define the current year and the previous year
previous_year_start = pd.to_datetime('2020-01-01')
previous_year_end = pd.to_datetime('2020-02-05')  # End of February 2020

# Find the earliest and latest dates in the dataset
earliest_date = merged_data['review_date'].min()
max_date = merged_data['review_date'].max()

# Filter data for the current year (cumulative data from the earliest date to the max date)
current_year_data = merged_data[merged_data['review_date'] >= earliest_date]
new_data = merged_data[merged_data['review_date'] >= previous_year_end]
# Filter data for the previous year (January to February 2020)
previous_year_data = merged_data[(merged_data['review_date'] >= earliest_date) & 
                                  (merged_data['review_date'] <= previous_year_end)]

# Calculate metrics for the current year (cumulative data)
total_listings = current_year_data['listing_id'].nunique()
total_hosts = current_year_data['host_id'].nunique() if 'host_id' in current_year_data.columns else "N/A"
median_review_score = current_year_data['review_scores_rating'].median() if 'review_scores_rating' in current_year_data.columns else "N/A"
median_price = current_year_data['price'].median() if 'price' in current_year_data.columns else "N/A"

# Calculate metrics for the previous year (January and February 2020)
previous_listings = previous_year_data['listing_id'].nunique()
previous_hosts = previous_year_data['host_id'].nunique() if 'host_id' in previous_year_data.columns else "N/A"
previous_review_score = previous_year_data['review_scores_rating'].median() if 'review_scores_rating' in previous_year_data.columns else "N/A"
previous_price = previous_year_data['price'].median() if 'price' in previous_year_data.columns else "N/A"

# Calculate the deltas (increases) for each metric
delta_listings = total_listings - previous_listings
delta_hosts = total_hosts - previous_hosts
delta_review_score = round(median_review_score - previous_review_score, 2) if previous_review_score != "N/A" else "N/A"
delta_price = round(median_price - previous_price, 2) if previous_price != "N/A" else "N/A"

# --- Overview Tab ---
with tab1:
    st.header("Overview")
    
    # Display metrics with deltas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Listings", f"{total_listings:,}", f"{delta_listings:,}", delta_color="normal")
    col2.metric("Active Hosts", f"{total_hosts:,}", f"{delta_hosts:,}", delta_color="normal")
    col3.metric("Median Review Score", f"{median_review_score}/100", f"{delta_review_score}", delta_color="normal")
    col4.metric("Median Nightly Price", f"${median_price}", f"${delta_price}", delta_color="normal")
    st.write("""Note: Metrics are for January 2021 and are compared to January 2020.""")
    # Extract year from 'review_date' column if it's not already done
    if 'review_date' in merged_data.columns:
        merged_data['year'] = pd.to_datetime(merged_data['review_date']).dt.year
        merged_data['month'] = pd.to_datetime(merged_data['review_date']).dt.month
        merged_data['year_month'] = pd.to_datetime(merged_data['review_date']).dt.to_period('M').astype(str)


    # Active Listings & Hosts over Time
    if 'month' in merged_data.columns:
        listings_by_year = merged_data.groupby('year_month').agg({'listing_id': 'nunique', 'host_id': 'nunique','review_id':'count'}).reset_index()
        listings_by_year.columns = ['Month', 'Listings', 'Hosts', 'Review']

        # Memfilter data untuk hanya menampilkan hingga Januari 2021
        listings_by_year = listings_by_year[listings_by_year['Month'] <= '2021-01']
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=listings_by_year['Month'], y=listings_by_year['Hosts'], mode='lines+markers', name='Hosts', line=dict(color='pink')))
        fig_line.add_trace(go.Scatter(x=listings_by_year['Month'], y=listings_by_year['Listings'], mode='lines+markers', name='Listings', line=dict(color='salmon')))
        fig_line.add_trace(go.Scatter(x=listings_by_year['Month'], y=listings_by_year['Review'], mode='lines+markers', name='Review', line=dict(color='red')))
        fig_line.update_layout(title="Review Count, Active Listings, and Hosts by Years on Platform", xaxis_title="Year", yaxis_title="Count")
        st.plotly_chart(fig_line, use_container_width=True)

    # Listings by Room Type
    if 'room_type' in merged_data.columns:
        room_type_counts = merged_data.groupby('room_type')['listing_id'].nunique().reset_index()
        room_type_counts.columns = ['Room Type', 'Count']

        fig_bar = px.bar(room_type_counts, x='Room Type', y='Count', title="Listings by Room Type", color='Room Type', color_discrete_sequence=px.colors.sequential.Reds)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Listings by Neighbourhood
    if 'neighbourhood' in merged_data.columns:
        neighbourhood_counts = merged_data.groupby('neighbourhood')['listing_id'].nunique().reset_index()
        neighbourhood_counts.columns = ['Neighbourhood', 'Count']
        neighbourhood_counts = neighbourhood_counts.sort_values(by='Count', ascending=False)

        fig_bar = px.bar(neighbourhood_counts, x='Neighbourhood', y='Count', title="Listings by Neighbourhood", color='Neighbourhood', color_discrete_sequence=px.colors.qualitative.Vivid_r)
        st.plotly_chart(fig_bar, use_container_width=True)

# --- Pricing Tab ---
# Calculate metrics for the current year
mean_price = current_year_data['price'].mean()
ninety_percentile_price = current_year_data['price'].quantile(0.9)
median_superhost_price = current_year_data[current_year_data['host_is_superhost'] == 't']['price'].median()

# Calculate metrics for the previous year
previous_mean_price = previous_year_data['price'].mean()
previous_ninety_percentile_price = previous_year_data['price'].quantile(0.9)
previous_median_superhost_price = previous_year_data[previous_year_data['host_is_superhost'] == 't']['price'].median()

# Calculate the deltas (increases)
delta_mean_price = round(mean_price - previous_mean_price, 2)
delta_ninety_percentile_price = round(ninety_percentile_price - previous_ninety_percentile_price, 2)
delta_median_superhost_price = round(median_superhost_price - previous_median_superhost_price, 2)

with tab2:
    st.header("Pricing")
    
    # Display pricing metrics with deltas
    col1, col3, col4 = st.columns(3)
    col1.metric("Mean Price", f"${mean_price:.2f}", f"{delta_mean_price}", delta_color="normal")
    col3.metric("Ninetieth Percentile Price", f"${ninety_percentile_price:.2f}", f"{delta_ninety_percentile_price}", delta_color="normal")
    col4.metric("Median Superhost Price", f"${median_superhost_price:.2f}", f"{delta_median_superhost_price}", delta_color="normal")
    st.write("""Note: Metrics are for January 2021 and are compared to January 2020.""")
    # Active Listings & Hosts over Time
    if 'month' in merged_data.columns:
        price_by_year = merged_data.groupby('year_month').agg({'price': 'mean'}).reset_index()
        price_by_year.columns = ['Month','Price']

        # Memfilter data untuk hanya menampilkan hingga Januari 2021
        price_by_year = price_by_year[price_by_year['Month'] <= '2021-01']
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=price_by_year['Month'], y=price_by_year['Price'], mode='lines+markers', name='Price', line=dict(color='red')))
        fig_line.update_layout(title="Average Price by Years on Platform", xaxis_title="Year", yaxis_title="Average")
        st.plotly_chart(fig_line, use_container_width=True)

    # Listing Prices by Room Type
    if 'room_type' in merged_data.columns:
        room_type_prices = current_year_data.groupby('room_type')['price'].mean().reset_index()
        room_type_prices.columns = ['Room Type', 'Average Price']

        fig_room_type = px.bar(
            room_type_prices,
            x='Room Type',
            y='Average Price',
            title="Listing Prices by Room Type",
            color='Room Type',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        st.plotly_chart(fig_room_type, use_container_width=True)

    # Listing Prices by Neighborhood
    if 'neighbourhood' in merged_data.columns:
        neighbourhood_prices = current_year_data.groupby('neighbourhood')['price'].median().reset_index()
        neighbourhood_prices.columns = ['Neighborhood', 'Median Price']
        neighbourhood_prices = neighbourhood_prices.sort_values(by='Median Price', ascending=False)

        fig_neighborhood = px.bar(
            neighbourhood_prices,
            x='Neighborhood',
            y='Median Price',
            title="Listing Prices by Neighborhood",
            color='Neighborhood',
            color_discrete_sequence=px.colors.qualitative.Vivid_r
        )
        fig_neighborhood.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_neighborhood, use_container_width=True)

# Key Review Metrics
median_review_count = current_year_data['review_id'].count() if 'review_id' in current_year_data.columns else "N/A"
mean_reviews_score = current_year_data['review_scores_rating'].mean() if 'review_scores_rating' in current_year_data.columns else "N/A"
mean_superhost_score = current_year_data[current_year_data['host_is_superhost'] == 't']['review_scores_rating'].mean() if 'host_is_superhost' in current_year_data.columns else "N/A"
# Calculate metrics for the previous year
previous_median_review_count = previous_year_data['review_id'].count()
previous_mean_reviews_score = previous_year_data['review_scores_rating'].mean()
previous_mean_superhost_score = previous_year_data[previous_year_data['host_is_superhost'] == 't']['review_scores_rating'].mean()


# Calculate the deltas (increases)
delta_median_review_count = round(median_review_count - previous_median_review_count, 2)
delta_mean_reviews_score = round(mean_reviews_score - previous_mean_reviews_score, 2)
delta_mean_superhost_score = round(mean_superhost_score - previous_mean_superhost_score, 2)

# --- Review Tab ---
with tab3:
    st.header("Review")
    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Median Review Count", f"{median_review_count:,}",f"{delta_median_review_count}", delta_color="normal")
    col2.metric("Mean Reviews Score", f"{mean_reviews_score:.2f}/100",f"{delta_mean_reviews_score}", delta_color="normal")
    col3.metric("Mean Superhost Reviews Score", f"{mean_superhost_score:.2f}/100", f"{delta_mean_superhost_score}", delta_color="normal")
    st.write("""Note: Metrics are for January 2021 and are compared to January 2020.""")

    # 1. Distribusi Skor Ulasan per Kategori
    review_categories = ['accuracy', 'cleanliness', 'checkin', 'communication', 'location', 'value']

    # Menghitung rata-rata skor untuk setiap kategori dan menyimpannya dalam DataFrame
    category_means_df = pd.DataFrame({
        'Review Type': [cat.capitalize() for cat in review_categories],
        'Average Score': [merged_data[f'review_scores_{cat}'].mean() for cat in review_categories]
    })

    # Menampilkan bar chart
    fig1 = px.bar(category_means_df, x='Review Type', y='Average Score', title="Average Score per Review Type", color_discrete_sequence=px.colors.qualitative.Vivid_r)
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Perbandingan Skor Superhost vs Non-Superhost
    superhost_scores = [merged_data[merged_data['host_is_superhost'] == 't'][f'review_scores_{cat}'].mean() for cat in review_categories]
    non_superhost_scores = [merged_data[merged_data['host_is_superhost'] == 'f'][f'review_scores_{cat}'].mean() for cat in review_categories]

    comparison_df = pd.DataFrame({
        'Review Type': review_categories,
        'Superhost': superhost_scores,
        'Non-Superhost': non_superhost_scores
    })

    comparison_melted = comparison_df.melt(id_vars='Review Type', var_name='Host Type', value_name='Score')

    fig2 = px.line(comparison_melted, x='Review Type', y='Score', color='Host Type', markers=True,
               title="Comparison of Superhost vs Non-Superhost Scores per Review Type", color_discrete_sequence=['#E63946', '#F1A7A7'])

    # Menambahkan data label di setiap titik
    fig2.update_traces(text=comparison_melted['Score'].round(2), textposition="top center")

    # Tampilkan chart
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Distribusi Skor Berdasarkan Kelompok Harga
    merged_data['price_group'] = pd.qcut(merged_data['price'], q=5, labels=[f'Group {i}' for i in range(1, 6)])

    # Menghitung rata-rata skor setiap kategori berdasarkan kelompok harga dan menggabungkannya ke dalam satu DataFrame
    price_group_scores = merged_data.groupby('price_group')[[f'review_scores_{cat}' for cat in review_categories]].mean().reset_index()

    price_group_scores.columns = ['price_group'] + [cat.capitalize() for cat in review_categories]
    # Mengubah kolom menjadi long format agar bisa di-plot dengan plotly express
    price_group_scores_melted = price_group_scores.melt(id_vars='price_group', var_name='Review Type', value_name='Score')

    # Membuat plot garis
    fig3 = px.line(price_group_scores_melted, x='price_group', y='Score', color='Review Type',
                   title="Review Scores by Price Group", color_discrete_sequence=px.colors.sequential.Reds)
    # Mengubah nama sumbu dan memberi keterangan pada setiap grup
    fig3.update_layout(
        xaxis_title="Price Group",
        yaxis_title="Average Review Score",
        xaxis=dict(
            tickvals=[f'Group {i}' for i in range(1, 6)],
            ticktext=['Lowest Price', 'Low Price', 'Middle Price', 'High Price', 'Highest Price']
        )
    )
    # Menampilkan plot
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Perbandingan Waktu Respon Host
    st.write("Correlation between Host and Score")
    grouped_data = merged_data.groupby('host_id').agg({
        'host_response_rate': 'mean',
        'host_acceptance_rate': 'mean', 
        'review_scores_rating': 'mean',
        'host_is_superhost': 'first'  # Mengambil nilai pertama atau mayoritas dalam group
    }).reset_index()
    # Daftar variabel yang bisa dipilih untuk sumbu x
    x_options = ['host_response_rate', 'host_acceptance_rate']  # Sesuaikan dengan nama kolom di dataset Anda
    y_variable = 'review_scores_rating'  # Variabel tetap untuk sumbu y

    # Dropdown untuk memilih variabel x
    x_variable = st.selectbox("Pilih Variabel X:", x_options)

    # Membuat plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=grouped_data, x=x_variable, y=y_variable, hue='host_is_superhost', ax=ax)
    ax.axhline(y=1, color='green', linestyle='--')  # Garis horizontal di y=50
    ax.axvline(x=1, color='red', linestyle='--')    # Garis vertikal di x=50

    # Pengaturan label
    ax.set_xlabel(x_variable)
    ax.set_ylabel("Review Scores Rating")
    ax.set_title(f"Scatter Plot: {x_variable} vs Review Scores Rating")

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
