import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from db_connect import get_connection
from queries import queries

# Get full path to file or return None if not found
def get_file_path(*path_parts):
    full_path = os.path.join(os.path.dirname(__file__), *path_parts)
    return full_path if os.path.exists(full_path) else None

# Set page configuration
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

# Sidebar
page = st.sidebar.selectbox("Navigate", ["Home", "SQL Queries", "Power BI Dashboard"])

# ---------- HOME PAGE ----------
if page == "Home":
    st.markdown("""
        <style>
        .title { text-align: center; font-size: 60px; font-weight: bold; margin-bottom: 10px; }
        .subtitle { text-align: center; font-size: 22px; margin-bottom: 30px; }
        .features { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
        ul { font-size: 18px; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 7])
    with col1:
        img_path = get_file_path("images.png")
        if img_path: st.image(img_path, width=100)
    with col2:
        st.markdown("<h1 style='color:black; font-size: 60px;'>OLA Ride Insights Dashboard</h1>", unsafe_allow_html=True)

    st.markdown("<div class='subtitle'>Uncover Smart Insights from Every Ride, Rating & Route</div>", unsafe_allow_html=True)
    st.image("http://blog.olacabs.com/wp-content/uploads/2018/01/Ola-Fleet2.gif", use_container_width=True)

    st.markdown("""
        <div class='features'>
            <h4>🔍 What You Can Do:</h4>
            <ul>
                <li>Analyze booking patterns, cancellations, and payments</li>
                <li>Compare ratings by vehicle type or driver</li>
                <li>Run real-time SQL queries to filter the data</li>
                <li>Visualize trends using interactive charts</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rides Analyzed", "1,20,000+")
    col2.metric("Cities Covered", "350+")
    col3.metric("Avg. Rating", "4.6 ⭐")

    st.markdown("### Use the **Sidebar** to Explore SQL Queries and Visualizations")

    ola_img_path = get_file_path("ola.jpg")
    if ola_img_path: st.image(ola_img_path, use_container_width=True)

    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; font-size: 18px; color: gray; padding-top: 20px;'>
            🚀 Ready to dive into data? <br>
            Head to the <b>SQL Query Explorer</b> from the sidebar 👉 to begin your analysis.<br><br>
            <i>Built using Streamlit | Powered by OLA Ride Data</i><br>
            <small>© 2025 OLA Analytics Project</small>
        </div>
    """, unsafe_allow_html=True)

# ---------- SQL QUERIES PAGE ----------
elif page == "SQL Queries":
    st.title("📊 SQL Query Explorer")

    selected_query = st.selectbox("Choose a question to explore:", list(queries.keys()))
    sql = queries[selected_query]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data)

    st.subheader("🔎 Query Results")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Visualization")

    if selected_query.startswith("1.") and 'vehicle_type' in df.columns:
        st.bar_chart(df['vehicle_type'].value_counts())

    elif selected_query.startswith("2.") and 'vehicle_type' in df.columns and 'avg_distance' in df.columns:
        st.bar_chart(df.set_index('vehicle_type')['avg_distance'])

    elif selected_query.startswith("3."):
        st.metric("Total Cancelled Rides by Customers", df.iloc[0, 0])

    elif selected_query.startswith("4.") and 'customer_id' in df.columns:
        st.bar_chart(df.set_index('customer_id')['ride_count'])

    elif selected_query.startswith("5.") and 'canceled_rides_by_driver' in df.columns:
        reason_counts = df['canceled_rides_by_driver'].value_counts().reset_index()
        reason_counts.columns = ['Reason', 'Count']
        st.bar_chart(reason_counts.set_index('Reason'))

    elif selected_query.startswith("6.") and 'max_rating' in df.columns:
        st.columns(2)[0].metric("Max Driver Rating", df['max_rating'].iloc[0])
        st.columns(2)[1].metric("Min Driver Rating", df['min_rating'].iloc[0])

    elif selected_query.startswith("7."):
        st.metric("Total Rides Paid via UPI", len(df))

    elif selected_query.startswith("8.") and 'avg_customer_rating' in df.columns:
        st.bar_chart(df.set_index('vehicle_type')['avg_customer_rating'])

    elif selected_query.startswith("9."):
        st.metric("Total Booking Value (₹)", round(float(df.iloc[0, 0]), 2))

    elif selected_query.startswith("10.") and 'incomplete_rides' in df.columns:
        reason_counts = df['incomplete_rides'].value_counts().reset_index()
        reason_counts.columns = ['Reason', 'Count']
        st.bar_chart(reason_counts.set_index('Reason'))

    else:
        st.info("No specific visualization defined for this query.")

    cursor.close()
    conn.close()

# ---------- POWER BI DASHBOARD PAGE ----------
elif page == "Power BI Dashboard":
    col1, col2 = st.columns([1, 15])
    logo_path = get_file_path("New_Power_BI_Logo.svg.png")
    if logo_path: col1.image(logo_path, width=50)

    col2.markdown("<h1 style='padding-top: 5px;'>Power BI Dashboard Preview</h1>", unsafe_allow_html=True)
    st.markdown("Here’s a preview of the Power BI Dashboard Built for OLA Ride Insights.")

    option = st.selectbox("Select a Visualization to View:", ("Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"))

    img_map = {
        "Overall": "overall.png",
        "Vehicle Type": "vehicle type.png",
        "Revenue": "Revenue.png",
        "Cancellation": "Cancellation.png",
        "Ratings": "Ratings.png"
    }

    selected_img = get_file_path(img_map[option])
    if selected_img:
        st.image(selected_img, use_container_width=True)
    else:
        st.warning("Image not found!")

    st.markdown("###")
    st.markdown("---")

    pbix_path = get_file_path("ola_ride_dashboard.pbix")
    if pbix_path:
        with open(pbix_path, "rb") as file:
            st.download_button("📥 Download Full Power BI Report (.pbix)", file, file_name="OLA_Dashboard.pbix")
    else:
        st.warning("Power BI file not found for download.")

    st.markdown("""
        <div style='text-align: center; padding: 30px 0 10px 0; color: gray;'>
            <hr style='border: 0.5px solid #ccc;'>
            <h4 style='color: #444;'>✨ Insightful Rides, Smarter Decisions ✨</h4>
            <p>Analyzing OLA rides is more than just numbers—it's a journey that shapes smarter transport solutions.</p>
            <p style='font-size: 16px;'>Built with Power BI & Streamlit</p>
            <small>© 2025 OLA Analytics Project | All Rights Reserved</small>
        </div>
    """, unsafe_allow_html=True)
