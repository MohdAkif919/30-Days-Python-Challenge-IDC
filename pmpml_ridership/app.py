# ---------------------------------------------------
# PMPML RIDERSHIP DASHBOARD
# ---------------------------------------------------
# Built with: Streamlit, Pandas, Matplotlib
# ---------------------------------------------------

import pandas as pd
import streamlit as st
import eda
import plots
from streamlit_lottie import st_lottie
from utils import format_inr, format_dataframe_inr
import json

# ---------------------------------------------------
# Load custom CSS
# ---------------------------------------------------
with open('pmpml_ridership/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------
# Streamlit Config
# ---------------------------------------------------
st.set_page_config(
    page_title="PMPML Ridership Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Lottie Loader Function
# ---------------------------------------------------
def load_lottiefile(filepath: str):
    """Load a local Lottie JSON animation"""
    with open(filepath, "r") as f:
        return json.load(f)

# Load bus animation
lottie_bus = load_lottiefile("pmpml_ridership/bus.json")

# ---------------------------------------------------
# Header with Bus Animation + Title
# ---------------------------------------------------
col1, col2 = st.columns([1, 1.85])
with col1:
    if lottie_bus:
        st_lottie(lottie_bus, speed=2, width=300, height=300, key="bus")
with col2:
    st.markdown(
        """
        <div style='padding-top: 90px'>
            <h1>🚌 PMPML Ridership Dashboard</h1>
            <h5>Analyzing Passenger Usage Patterns to Enhance Pune PMPML Bus Service</h5>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# Documentation
# ---------------------------------------------------

if 'doc_shown' not in st.session_state:
    st.session_state.doc_shown = False

def show_documentation():
    st.markdown("""
    ### ❓ **Problem Statement**
    Pune is one of India's fastest-growing cities, with thousands of commuters depending daily on PMPML
    bus services to travel between residential areas, commercial hubs, and industrial zones.
    Understanding how people use different bus routes, boarding stations, and time slots helps
    the transport authority optimize resources, reduce overcrowding, and improve passenger convenience.
    Public transportation agencies like PMPML collect large amounts of ridership data every day. Analyzing this data helps uncover:
                
    - Which routes and time slots are the busiest
    - How weekday vs weekend trends differ
    - Which boarding stations handle the most passengers
    - How fare collection varies over time

    This dashboard aims to provide actionable insights using a **dummy dataset (5,00,000+ records)** that mimics real-life scenarios.

    ### 🗂️ About this Project
    - This is a **practice project** built as part of the **[30 Days of Python Challenge](https://indiandataclub.notion.site/30DaysOfPython-1f9a16c0422f8074bf29eee315a6802a)** organized by [Indian Data Club](https://indiandataclub.com/).
    - Built with **Streamlit**, **Pandas**, **Matplotlib**, and **custom CSS animations** to enhance interactivity and presentation.
    - Includes filters for year, route, and boarding station to explore different usage patterns.

    ### 📁 **Access the Code & Dataset**
    - GitHub Repository: [View the full code and dummy data](https://github.com/MohdAkif919/30-Days-Python-Challenge-IDC)

    ### 🙋‍♂️ **About Me**
    - **Mohd Akif**, a Data Analyst passionate about transforming numbers into insights.
    - 🔗 [LinkedIn](https://www.linkedin.com/in/mohdakif919/) | [Portfolio](https://codebasics.io/portfolio/Mohd-Akif) | [GitHub](https://github.com/MohdAkif919)
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# File Upload
# ---------------------------------------------------
uploaded_file = st.file_uploader("📂 Upload PMPML CSV file", type=["csv"])
if not uploaded_file:
    st.info("📌 Upload your CSV file to get started!")
    st.markdown("---")

    # Reset session state if file is cleared
    if st.session_state.get("doc_shown", False) is True:
        st.session_state.doc_shown = False

    if not st.session_state.doc_shown:
        show_documentation()
        st.session_state.doc_shown = True

# ---------------------------------------------------
# Main Dashboard
# ---------------------------------------------------
if uploaded_file:
    # Load and clean data
    df = eda.load_and_clean_data(uploaded_file)
    st.success("✅ Data Loaded and Cleaned!")

    # ---------------------------------------------------
    # Filters
    # ---------------------------------------------------
    years = sorted(df['Year'].unique())
    year_options = ["All Years"] + [str(y) for y in years]
    selected_years = st.multiselect("📅 **Select Year(s)**", options=year_options, default="All Years")

    routes = sorted(df['Route'].unique())
    route_options = ["All Routes"] + [str(r) for r in routes]
    selected_routes = st.multiselect("🚌 **Select Route(s)**", options=route_options, default="All Routes")

    stations = sorted(df['Boarding Station'].unique())
    station_options = ["All Stations"] + [str(s) for s in stations]
    selected_stations = st.multiselect("🚏 **Select Boarding Station(s)**", options=station_options, default="All Stations")

    df_filtered = df.copy()

    # Apply filters
    if "All Years" not in selected_years and selected_years:
        selected_years_int = [int(y) for y in selected_years]
        df_filtered = df_filtered[df_filtered['Year'].isin(selected_years_int)]

    if "All Routes" not in selected_routes and selected_routes:
        df_filtered = df_filtered[df_filtered['Route'].isin(selected_routes)]

    if "All Stations" not in selected_stations and selected_stations:
        df_filtered = df_filtered[df_filtered['Boarding Station'].isin(selected_stations)]

    # Filter info
    info_parts = []
    info_parts.append("📅 **All Years**" if "All Years" in selected_years or not selected_years else f"📅 {', '.join(selected_years)}")
    info_parts.append("🚌 **All Routes**" if "All Routes" in selected_routes or not selected_routes else f"🚌 {', '.join(selected_routes)}")
    info_parts.append("🚏 **All Stations**" if "All Stations" in selected_stations or not selected_stations else f"🚏 {', '.join(selected_stations)}")
    st.info(f"📌 Showing data for: {' | '.join(info_parts)}")

    # ---------------------------------------------------
    # Metrics
    # ---------------------------------------------------
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👥 Total Passengers", f"{format_inr(eda.total_passengers(df_filtered))}")
    col2.metric("📅 Avg Daily Passengers", f"{format_inr(int(eda.daily_ridership(df_filtered).mean()))}")
    col3.metric("🚌 Total Routes", f"{format_inr(df_filtered['Route'].nunique())}")
    col4.metric("🚏 Total Stations", f"{format_inr(df_filtered['Boarding Station'].nunique())}")
    col5.metric("💰 Total Fare Collected", f"₹ {format_inr(eda.total_fare(df_filtered))}")

    # ---------------------------------------------------
    # Tabs
    # ---------------------------------------------------
    overview, routes_tab, stations_tab, trends_tab, fare_tab, doc_tab = st.tabs(
        ["📊 Overview", "🚌 Routes", "🚏 Stations", "⏰ Trends", "💰 Fare", "📄 Documentation"]
    )

    with overview:
        st.subheader("📂 Data Preview")
        st.dataframe(df_filtered.head(100))
        col1, col2 = st.columns([1, 1])
        with col1:
            st.pyplot(plots.plot_weekday_vs_weekend(eda.weekday_vs_weekend(df_filtered)), use_container_width=True)
        with col2:
            st.pyplot(plots.plot_passengers_by_timeslot(eda.peak_time_slots(df_filtered)), use_container_width=True)
        st.info(eda.generate_overview_insight(df_filtered))

    with routes_tab:
        with st.expander("📊 Route vs Peak Time Slot", expanded=True):
            st.dataframe(format_dataframe_inr(eda.route_peak_timeslot(df_filtered)))
        with st.expander("📊 Route: Weekday vs Weekend Usage", expanded=True):
            st.dataframe(format_dataframe_inr(eda.route_weekday_weekend(df_filtered)))
        st.pyplot(plots.plot_passengers_by_route(eda.top_routes(df_filtered)))
        st.info(eda.generate_routes_insight(df_filtered))

    with stations_tab:
        with st.expander("🚏 Top 10 Boarding Stations", expanded=True):
            busiest = eda.busiest_stations(df_filtered).reset_index().rename(columns={"index": "Boarding Station"})
            st.dataframe(format_dataframe_inr(busiest.head(10)))
        with st.expander("📊 Station vs Routes Table", expanded=True):
            st.dataframe(format_dataframe_inr(eda.station_vs_routes(df_filtered)))
        st.info(eda.generate_stations_insight(df_filtered))

    with trends_tab:
        st.subheader("⏰ Monthly Trends")
        if not selected_years or "All Years" in selected_years:
            last_3_years = sorted(df['Year'].unique())[-3:]
            df_trend = df_filtered[df_filtered['Year'].isin(last_3_years)]
            st.info(f"Showing monthly trends for: {', '.join(map(str, last_3_years))}")
        else:
            selected_years_int = [int(y) for y in selected_years]
            df_trend = df_filtered[df_filtered['Year'].isin(selected_years_int)]
        col1, col2 = st.columns([1, 1])
        with col1:
            st.pyplot(plots.plot_monthly_trend(eda.monthly_passenger_trend(df_trend), 'Passenger Count', "Monthly Passenger Trend"), use_container_width=True)
        with col2:
            st.pyplot(plots.plot_monthly_trend(eda.monthly_fare_trend(df_trend), 'Fare Collected', "Monthly Fare Collection Trend"), use_container_width=True)
        col3, col4 = st.columns([1, 1])
        with col3:
            st.pyplot(plots.plot_yearly_ridership(eda.yearly_ridership(df_filtered)), use_container_width=True)
        with col4:
            df_wday = eda.weekday_pattern(df_filtered)
            st.pyplot(plots.plot_weekday_pattern(df_wday), use_container_width=True)
        st.info(eda.generate_trends_insight(
            eda.monthly_passenger_trend(df_trend),
            eda.monthly_fare_trend(df_trend),
            eda.yearly_ridership(df_filtered),
            df_wday
        ))

    with fare_tab:
        with st.expander("💰 Yearly Fare Collection", expanded=True):
            st.dataframe(format_dataframe_inr(eda.yearly_fare(df_filtered)))
        col1, col2 = st.columns([1, 1])
        with col1:
            st.pyplot(plots.plot_fare_by_route(eda.fare_by_route(df_filtered)), use_container_width=True)
        with col2:
            st.pyplot(plots.plot_fare_by_station(eda.fare_by_station(df_filtered)), use_container_width=True)
        st.info(eda.generate_fare_insight(df_filtered))

    with doc_tab:
        show_documentation()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("---")
footer = """
<div class="footer">
        <strong>PMPML Ridership Dashboard</strong><br>
        This is a <em>practice project</em> tested on a dummy dataset (5,00,000+ records) mimicking real-life scenarios.<br>
        Developed by <strong>Mohd Akif (Data Analyst)</strong> | © 2025 All Rights Reserved
        <br><br>
        <a href='https://www.linkedin.com/in/mohdakif919/' target='_blank'>
        <img src='https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/linkedin.svg' alt='LinkedIn' />
        </a>
        <a href='https://codebasics.io/portfolio/Mohd-Akif' target='_blank'>
        <img src='https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/codeberg.svg' alt='Portfolio' />
        </a>
        <a href='https://github.com/MohdAkif919' target='_blank'>
        <img src='https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg' alt='GitHub' />
        </a>
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)
