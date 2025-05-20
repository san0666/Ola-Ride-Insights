import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_connect import get_connection
from queries import queries

# Set Streamlit page config
st.set_page_config(page_title="OLA Ride Insights", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Home", "SQL Queries", "Power BI Dashboard"])

# ---------- HOME PAGE ----------
if page == "Home":
    st.markdown("""
        <style>
        .title {
            text-align: center;
            color: #555;
            font-size: 60px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 22px;
            margin-bottom: 30px;
        }
        .features {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        ul {
            font-size: 18px;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 7])
    with col1:
        st.image("images.png", width=100)
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
    with col1:
        st.metric("Rides Analyzed", "1,20,000+")
    with col2:
        st.metric("Cities Covered", "350+")
    with col3:
        st.metric("Avg. Rating", "4.6 ⭐")

    st.markdown("###  Use the **Sidebar** to Explore SQL Queries and Visualizations")
    st.image("ola.jpg", use_container_width=True)
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; font-size: 18px; color: gray; padding-top: 20px;'>
            🚀 Ready to dive into data? <br>
            Head to the <b>SQL Query Explorer</b> from the sidebar <span style='font-size:18px;'>👉</span> to begin your analysis.<br><br>
            <i>Built using Streamlit | Powered by OLA Ride Data</i><br>
            <small>© 2025 OLA Analytics Project</small>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    if selected_query.startswith("1."):
        if not df.empty and 'vehicle_type' in df.columns:
            counts = df['vehicle_type'].value_counts()
            st.bar_chart(counts)

    elif selected_query.startswith("2."):
        if not df.empty:
            st.bar_chart(df.set_index('vehicle_type')['avg_distance'])

    elif selected_query.startswith("3."):
        if not df.empty:
            total_cancelled = df.iloc[0, 0]
            st.metric("Total Cancelled Rides by Customers", total_cancelled)

    elif selected_query.startswith("4."):
        if not df.empty and 'customer_id' in df.columns:
            st.bar_chart(df.set_index('customer_id')['ride_count'])

    elif selected_query.startswith("5."):
        if not df.empty and 'canceled_rides_by_driver' in df.columns:
            reason_counts = df['canceled_rides_by_driver'].value_counts().reset_index()
            reason_counts.columns = ['Reason', 'Count']
            st.bar_chart(reason_counts.set_index('Reason'))
        else:
            st.info("No cancellation reasons by drivers found.")

    elif selected_query.startswith("6."):
        if not df.empty and 'max_rating' in df.columns and 'min_rating' in df.columns:
            col1, col2 = st.columns(2)
            col1.metric("Max Driver Rating", df['max_rating'].iloc[0])
            col2.metric("Min Driver Rating", df['min_rating'].iloc[0])

    elif selected_query.startswith("7."):
        st.metric("Total Rides Paid via UPI", len(df))

    elif selected_query.startswith("8."):
        if not df.empty and 'avg_customer_rating' in df.columns:
            st.bar_chart(df.set_index('vehicle_type')['avg_customer_rating'])

    elif selected_query.startswith("9."):
        if not df.empty:
            total_value = df.iloc[0, 0]
            st.metric("Total Booking Value (₹)", round(float(total_value), 2))

    elif selected_query.startswith("10."):
        if not df.empty and 'incomplete_rides' in df.columns:
            reason_counts = df['incomplete_rides'].value_counts().reset_index()
            reason_counts.columns = ['Reason', 'Count']
            st.bar_chart(reason_counts.set_index('Reason'))
        else:
            st.info("No incomplete ride reasons found.")

    else:
        st.info("No specific visualization defined for this query.")

    cursor.close()
    conn.close()

# ---------- POWER BI DASHBOARD PAGE ----------
elif page == "Power BI Dashboard":
    col1, col2 = st.columns([1, 15])  # Adjust the ratio as needed

# Display logo in the first column
    with col1:
      st.image("New_Power_BI_Logo.svg.png", width=50)

# Display title in the second column
    with col2:
      st.markdown("<h1 style='padding-top: 5px;'>Power BI Dashboard Preview</h1>", unsafe_allow_html=True)

    st.markdown("Here’s a preview of the Power BI Dashboard Built for OLA Ride Insights. Each visual represents Trends, Cancellations, and Performance metrics.")

    option = st.selectbox(
    "Select a Visualization to View:",
    ("Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings")
    )

    if option == "Overall":
       st.image("overall.png", use_container_width=True)

    elif option == "Vehicle Type":
       st.image("vehicle type.png", use_container_width=True)

    elif option == "Revenue":
       st.image("Revenue.png", use_container_width=True)

    elif option == "Cancellation":
       st.image("Cancellation.png", use_container_width=True)

    elif option == "Ratings":
       st.image("Ratings.png", use_container_width=True)
    st.markdown("###")
    st.markdown("---")
    # Optional download button for your .pbix file
    with open("ola_ride_dashboard.pbix", "rb") as file:
        st.download_button("📥 Download Full Power BI Report (.pbix)", file, file_name="OLA_Dashboard.pbix")
    st.markdown("""
        <div style='text-align: center; padding: 30px 0 10px 0; color: gray;'>
            <hr style='border: 0.5px solid #ccc;'>
            <h4 style='color: #444;'>✨ Insightful Rides, Smarter Decisions ✨</h4>
            <p>Analyzing OLA rides is more than just numbers—it's a journey that shapes smarter transport solutions.</p>
            <p style='font-size: 16px;'>Built with using Power BI & Streamlit</p>
            <small>© 2025 OLA Analytics Project | All Rights Reserved</small>
        </div>
    """, unsafe_allow_html=True)