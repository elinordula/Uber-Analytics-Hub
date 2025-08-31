import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta


st.set_page_config(page_title="Uber Analytics Hub", layout="wide", initial_sidebar_state="expanded")


st.markdown(
    """
    <div style="
        text-align: center; 
        background: linear-gradient(135deg, #000 0%, #333 100%);
        padding: 40px 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        color: white;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    ">
        <h1 style="
            font-size: 48px; 
            font-weight: 900; 
            letter-spacing: 4px;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
            margin: 0;
        ">
            Uber Analytics Hub
        </h1>
        <p style="
            font-size: 18px; 
            font-weight: 400;
            margin-top: 5px;
            color: #ccc;
        ">
            Comprehensive Insights for NCR Ride Bookings
        </p>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)


try:
    df = pd.read_csv("ncr_ride_bookings.csv")
except FileNotFoundError:
    st.error("Error: The file 'ncr_ride_bookings.csv' was not found. Please make sure it is in the same directory as the app.py file.")
    st.stop()


try:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.time
except KeyError:
    st.error("Error: The DataFrame does not contain the expected 'Date' and 'Time' columns. Please check your CSV file.")
    st.stop()


df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()
df["Weekday"] = df["Date"].dt.day_name()
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
df["Is_Weekend"] = df["Weekday"].isin(["Saturday", "Sunday"])
df["DateOnly"] = df["Date"].dt.date


df["Ride Distance"] = df["Ride Distance"].fillna(0)
df["Booking Value"] = df["Booking Value"].fillna(0)
df["Driver Ratings"] = df["Driver Ratings"].fillna(df["Driver Ratings"].mean())
df["Customer Rating"] = df["Customer Rating"].fillna(df["Customer Rating"].mean())


df["Vehicle Type"] = df["Vehicle Type"].str.lower()
df["Vehicle Type"] = df["Vehicle Type"].str.replace('go sedan', 'go sedan')
df["Vehicle Type"] = df["Vehicle Type"].str.replace('go mini', 'go mini')
df["Vehicle Type"] = df["Vehicle Type"].str.replace('e-bike', 'ebike')
df["Vehicle Type"] = df["Vehicle Type"].str.replace('premier sedan', 'premier sedan')
df["Vehicle Type"] = df["Vehicle Type"].str.replace('uber xl', 'uber xl')


cols = [
    "Date", "Month", "Weekday", "Hour", "Is_Weekend",
    "Booking ID", "Booking Status", "Vehicle Type",
    "Ride Distance", "Booking Value",
    "Driver Ratings", "Customer Rating", "Payment Method",
    "Reason for cancelling by Customer", "Driver Cancellation Reason",
    "Customer ID", "DateOnly"
]
df_clean = df[cols].copy()


min_date = df_clean["Date"].min().date()
max_date = df_clean["Date"].max().date()


months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


st.markdown(
    """
    <style>
    /* Hide Streamlit elements */
    .stApp > header {visibility: hidden;}
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Overall page styling */
    .stApp {
        background-color: white;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }

    /* Hide the scrollbar for the entire app */
    .main {
        overflow: hidden !important;
    }
    .block-container {
        padding: 1.5rem !important;
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* Sidebar styling - Enhanced */
    .css-1d391kg, .css-1lcbmhc, .css-1cypcdb {
        background: linear-gradient(180deg, #000 0%, #333 100%) !important;
        border-right: none !important;
        padding: 0 !important;
        height: 100vh !important;
        min-height: 100vh !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
    }
    
    /* Uber header - Enhanced */
    .uber-header {
        background: linear-gradient(135deg, #000 0%, #333 100%);
        padding: 40px 20px;
        text-align: center;
        border-bottom: 3px solid #444;
        margin: 0;
        position: relative;
        overflow: hidden;
    }
    
    .uber-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.03) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .uber-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
        position: relative;
        z-index: 1;
    }
    
    .uber-logo-inner {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #000 0%, #333 100%);
        border-radius: 50%;
    }
    
    .uber-text {
        color: white;
        font-size: 36px;
        font-weight: 900;
        margin: 0;
        letter-spacing: 4px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Navigation buttons - Enhanced */
    .stButton > button {
        width: 100% !important;
        margin: 0 !important;
        border-radius: 0 !important;
        border: none !important;
        padding: 25px 30px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.05) 50%, transparent 100%) !important;
        color: #ccc !important;
        text-align: left !important;
        border-bottom: 1px solid #444 !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0.1) 100%) !important;
        color: white !important;
        border-left: 4px solid #fff !important;
        transform: translateX(4px) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:focus, .stButton > button:active {
        background: linear-gradient(90deg, #fff 0%, #f0f0f0 100%) !important;
        color: #000 !important;
        border-left: 6px solid #fff !important;
        box-shadow: inset 0 0 20px rgba(255,255,255,0.2) !important;
        transform: translateX(6px) !important;
    }
    
    /* KPI cards */
    .kpi-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e6e6e6;
        margin-bottom: 15px;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-title {
        font-size: 12px;
        color: #666;
        margin-bottom: 8px;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #333;
    }
    
    /* Section headers */
    .section-header {
        color: #333;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 16px;
        margin-bottom: 15px;
        text-align: center;
        font-weight: 600;
    }
    
    /* Chart heights */
    .stPlotlyChart {
        height: 300px !important;
    }
    
    /* Remove extra spacing and hide scrollbars for containers */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    .stMarkdown, .stSubheader {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Multi-column chart layout */
    .chart-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    .chart-col {
        flex: 1;
        margin: 0 5px;
    }
    
    /* Professional table styling */
    .professional-table {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .professional-table th {
        background-color: #f8f9fa;
        padding: 12px;
        text-align: left;
        font-weight: 600;
        color: #333;
        border-bottom: 2px solid #e6e6e6;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 1px;
    }
    
    .professional-table td {
        padding: 12px;
        border-bottom: 1px solid #f0f0f0;
        color: #666;
    }
    
    .professional-table tr:hover {
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "OVERALL"


with st.sidebar:
    st.markdown(
        """
        <div class="uber-header">
            <div class="uber-logo">
                <div class="uber-logo-inner"></div>
            </div>
            <div class="uber-text">UBER</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    menu_options = ["OVERALL", "VEHICLE TYPE", "REVENUE", "CANCELLATION", "RATINGS"]
    
    for option in menu_options:
        if st.button(option, key=f"nav_{option}"):
            st.session_state.selected_page = option

selected = st.session_state.selected_page


if selected == "OVERALL":
    # Date filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date, key="overall_start")
    with col2:
        end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date, key="overall_end")
    
    filtered_df = df_clean[(df_clean["Date"].dt.date >= start_date) & (df_clean["Date"].dt.date <= end_date)]
    

    col3, col4, col5 = st.columns(3)
    with col3:
        vehicle_type = st.selectbox("Vehicle Type", ["All"] + list(df_clean["Vehicle Type"].unique()))
    with col4:
        booking_status = st.selectbox("Booking Status", ["All"] + list(df_clean["Booking Status"].unique()))
    with col5:
        payment_method = st.selectbox("Payment Method", ["All"] + list(df_clean["Payment Method"].unique()))
    

    if vehicle_type != "All":
        filtered_df = filtered_df[filtered_df["Vehicle Type"] == vehicle_type]
    if booking_status != "All":
        filtered_df = filtered_df[filtered_df["Booking Status"] == booking_status]
    if payment_method != "All":
        filtered_df = filtered_df[filtered_df["Payment Method"] == payment_method]


    total_bookings = filtered_df["Booking ID"].nunique()
    total_revenue = filtered_df["Booking Value"].sum()
    avg_ride_distance = filtered_df["Ride Distance"].mean()
    avg_booking_value = filtered_df["Booking Value"].mean()
    avg_hourly_bookings = filtered_df["Booking ID"].nunique() / (len(filtered_df["Hour"].unique()) or 1)
    weekend_bookings = filtered_df[filtered_df["Is_Weekend"]]["Booking ID"].nunique()
    weekend_percentage = (weekend_bookings / total_bookings * 100) if total_bookings > 0 else 0


    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    with kpi_col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Bookings</div>
                <div class="kpi-value">{total_bookings/1000:.1f}K</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">₹{total_revenue/1000:.0f}K</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Distance</div>
                <div class="kpi-value">{avg_ride_distance:.1f} km</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Value</div>
                <div class="kpi-value">₹{avg_booking_value:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col5:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Weekend %</div>
                <div class="kpi-value">{weekend_percentage:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Time-based Analysis</div>", unsafe_allow_html=True)
    

    chart_col1, chart_col2 = st.columns(2, gap="medium")
    
    with chart_col1:
        hourly_bookings = filtered_df.groupby("Hour")["Booking ID"].nunique()
        fig_hour = go.Figure([go.Bar(x=hourly_bookings.index, y=hourly_bookings.values, marker_color='#000')])
        fig_hour.update_layout(
            title={'text': 'Bookings by Hour', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_hour, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        weekday_bookings = filtered_df.groupby("Weekday")["Booking ID"].nunique().reindex(weekdays_order)
        fig_weekday = go.Figure([go.Bar(x=weekday_bookings.index, y=weekday_bookings.values, marker_color='#000')])
        fig_weekday.update_layout(
            title={'text': 'Bookings by Weekday', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_weekday, use_container_width=True, config={'displayModeBar': False})


    daily_trend = filtered_df.groupby("DateOnly")["Booking ID"].nunique().rolling(window=7).mean()
    fig_daily = go.Figure([go.Scatter(x=daily_trend.index, y=daily_trend.values, line=dict(color='#000'), fill='tozeroy')])
    fig_daily.update_layout(
        title={'text': 'Daily Trend (7-day Moving Average)', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
        height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
    st.plotly_chart(fig_daily, use_container_width=True, config={'displayModeBar': False})

elif selected == "VEHICLE TYPE":
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min_date, key="vehicle_start")
    with col2:
        end_date = st.date_input("End Date", max_date, key="vehicle_end")
    
    filtered_df = df_clean[(df_clean["Date"].dt.date >= start_date) & (df_clean["Date"].dt.date <= end_date)]
    success_df = filtered_df[filtered_df["Booking Status"] == "Completed"]
    
    grouped = filtered_df.groupby("Vehicle Type").agg(
        total_booking_value=("Booking Value", "sum"),
        total_distance_travelled=("Ride Distance", "sum"),
        avg_booking_value=("Booking Value", "mean"),
        avg_distance_travelled=("Ride Distance", "mean")
    ).reset_index()
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Booking Value</div>
                <div class="kpi-value" style="font-size: 22px;">₹{grouped['total_booking_value'].sum():,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Distance Travelled</div>
                <div class="kpi-value" style="font-size: 22px;">{grouped['total_distance_travelled'].sum():,.0f} km</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Booking Value</div>
                <div class="kpi-value" style="font-size: 22px;">₹{grouped['avg_booking_value'].mean():,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Distance</div>
                <div class="kpi-value" style="font-size: 22px;">{grouped['avg_distance_travelled'].mean():,.2f} km</div>
            </div>
            """, unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2, gap="medium")
    
    with chart_col1:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=grouped['Vehicle Type'], y=grouped['total_booking_value'], name='Booking Value', marker_color='#000'))
        fig_bar.add_trace(go.Bar(x=grouped['Vehicle Type'], y=grouped['total_distance_travelled'], name='Distance', marker_color='#666'))
        fig_bar.update_layout(
            title={'text': 'Booking Value & Distance by Vehicle', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            barmode='group', height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        fig_pie = px.pie(grouped, values='total_booking_value', names='Vehicle Type', title='Revenue Share by Vehicle', hole=0.5,
                         color_discrete_sequence=['#000', '#333', '#666', '#999', '#ccc', '#e0e0e0'])
        fig_pie.update_layout(
            title={'text': 'Revenue Share by Vehicle', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white',
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1)
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    
    fig_bubble = px.scatter(grouped, x="total_booking_value", y="total_distance_travelled", size="avg_distance_travelled", color="Vehicle Type",
                            hover_name="Vehicle Type", size_max=60, title="Revenue vs. Distance (Bubble size indicates Avg. Distance)",
                            color_discrete_sequence=['#000', '#333', '#666', '#999', '#ccc', '#e0e0e0'])
    fig_bubble.update_layout(
        title={'text': 'Revenue vs. Distance (Bubble size indicates Avg. Distance)', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
        height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bubble, use_container_width=True, config={'displayModeBar': False})

elif selected == "REVENUE":
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date(2024, 1, 1), min_value=min_date, max_value=max_date, key="revenue_start")
    with col2:
        end_date = st.date_input("End Date", date(2024, 12, 30), min_value=min_date, max_value=max_date, key="revenue_end")
    
    filtered_df = df_clean[(df_clean["Date"].dt.date >= start_date) & (df_clean["Date"].dt.date <= end_date)]
    
    total_revenue = filtered_df["Booking Value"].sum()
    avg_booking_value = filtered_df["Booking Value"].mean()
    total_bookings = filtered_df["Booking ID"].nunique()
    revenue_per_ride = total_revenue / total_bookings if total_bookings > 0 else 0
    prev_period = filtered_df[filtered_df["Date"].dt.date < start_date]
    prev_revenue = prev_period["Booking Value"].sum()
    revenue_growth = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Booking Value</div>
                <div class="kpi-value">₹{avg_booking_value:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Revenue per Ride</div>
                <div class="kpi-value">₹{revenue_per_ride:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Revenue Growth %</div>
                <div class="kpi-value">{revenue_growth:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Revenue Over Time</div>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2, gap="medium")
    with chart_col1:
        daily_revenue = filtered_df.groupby("DateOnly")["Booking Value"].sum()
        fig_daily = go.Figure([go.Scatter(x=daily_revenue.index, y=daily_revenue.values, line=dict(color='#000'), fill='tozeroy')])
        fig_daily.update_layout(
            title={'text': 'Daily Revenue Trend', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_daily, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        monthly_revenue = filtered_df.groupby("Month")["Booking Value"].sum().reindex(months_order)
        fig_monthly = go.Figure([go.Bar(x=monthly_revenue.index, y=monthly_revenue.values, marker_color='#000')])
        fig_monthly.update_layout(
            title={'text': 'Monthly Revenue Trend', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-header'>Revenue by Category</div>", unsafe_allow_html=True)
    
    chart_col3, chart_col4 = st.columns(2, gap="medium")
    with chart_col3:
        revenue_by_vehicle = filtered_df.groupby("Vehicle Type")["Booking Value"].sum()
        fig_vehicle = go.Figure([go.Bar(x=revenue_by_vehicle.index, y=revenue_by_vehicle.values, marker_color='#000')])
        fig_vehicle.update_layout(
            title={'text': 'Revenue by Vehicle Type', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_vehicle, use_container_width=True, config={'displayModeBar': False})

    with chart_col4:
        revenue_by_payment = filtered_df.groupby("Payment Method")["Booking Value"].sum()
        fig_payment = go.Figure([go.Bar(x=revenue_by_payment.index, y=revenue_by_payment.values, marker_color='#000')])
        fig_payment.update_layout(
            title={'text': 'Revenue by Payment Method', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_payment, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-header'>Revenue Distribution</div>", unsafe_allow_html=True)
    
    chart_col5, chart_col6 = st.columns(2, gap="medium")
    with chart_col5:
        fig_hist = px.histogram(filtered_df, x="Booking Value", nbins=20, title="Histogram of Booking Values", color_discrete_sequence=['#000'])
        fig_hist.update_layout(
            title={'text': 'Histogram of Booking Values', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})

    with chart_col6:
        top_customers = filtered_df.groupby("Customer ID")["Booking Value"].sum().sort_values(ascending=False).head(10).reset_index()
        table_html = """
        <div style="height: 300px; overflow-y: auto;">
            <h3 class="section-header" style="margin-top: 0;">Top 10 Customers</h3>
            <table class="professional-table">
                <thead>
                    <tr>
                        <th>Customer ID</th>
                        <th>Total Revenue</th>
                    </tr>
                </thead>
                <tbody>
        """
        for _, row in top_customers.iterrows():
            table_html += f'<tr><td>{row["Customer ID"]}</td><td>₹{row["Booking Value"]:,.2f}</td></tr>'
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)

elif selected == "CANCELLATION":
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date(2024, 1, 1), min_value=min_date, max_value=max_date, key="cancel_start")
    with col2:
        end_date = st.date_input("End Date", date(2024, 12, 30), min_value=min_date, max_value=max_date, key="cancel_end")
    
    filtered_df = df_clean[(df_clean["Date"].dt.date >= start_date) & (df_clean["Date"].dt.date <= end_date)]
    
    total_bookings = len(filtered_df)
    completed_bookings = len(filtered_df[filtered_df["Booking Status"] == "Completed"])
    cancelled_bookings = total_bookings - completed_bookings
    cancellation_rate = (cancelled_bookings / total_bookings * 100) if total_bookings > 0 else 0
    cust_cancellations = len(filtered_df[filtered_df["Booking Status"] == "Cancelled by Customer"])
    driver_cancellations = len(filtered_df[filtered_df["Booking Status"] == "Cancelled by Driver"])
    revenue_lost = filtered_df[filtered_df["Booking Status"].str.contains("Cancelled")]["Booking Value"].sum()

    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    with kpi_col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Bookings</div>
                <div class="kpi-value">{total_bookings/1000:.1f}K</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Completed</div>
                <div class="kpi-value">{completed_bookings/1000:.1f}K</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Cancelled</div>
                <div class="kpi-value">{cancelled_bookings/1000:.1f}K</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Cancel Rate</div>
                <div class="kpi-value">{cancellation_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col5:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Revenue Lost</div>
                <div class="kpi-value">₹{revenue_lost/1000:.0f}K</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Cancellation Breakdown</div>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2, gap="medium")
    
    cust_cancel_df = filtered_df[filtered_df["Booking Status"] == "Cancelled by Customer"]
    driver_cancel_df = filtered_df[filtered_df["Booking Status"] == "Cancelled by Driver"]
    
    with chart_col1:
        if len(cust_cancel_df) > 0:
            cust_reasons = cust_cancel_df["Reason for cancelling by Customer"].value_counts()
            fig_cust = px.pie(names=cust_reasons.index, values=cust_reasons.values, title="Customer Cancellation Reasons", 
                             color_discrete_sequence=['#000', '#333', '#666', '#999', '#ccc'])
            fig_cust.update_layout(
                title={'text': 'Customer Cancellation Reasons', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
                height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white'
            )
            st.plotly_chart(fig_cust, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        if len(driver_cancel_df) > 0:
            driver_reasons = driver_cancel_df["Driver Cancellation Reason"].value_counts()
            fig_driver = px.pie(names=driver_reasons.index, values=driver_reasons.values, title="Driver Cancellation Reasons",
                               color_discrete_sequence=['#000', '#333', '#666', '#999', '#ccc'])
            fig_driver.update_layout(
                title={'text': 'Driver Cancellation Reasons', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
                height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white'
            )
            st.plotly_chart(fig_driver, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='section-header'>Cancellation Trends</div>", unsafe_allow_html=True)
    
    chart_col3, chart_col4 = st.columns(2, gap="medium")
    
    with chart_col3:
        cancel_over_time = filtered_df[filtered_df["Booking Status"].str.contains("Cancelled")].groupby("DateOnly").size()
        fig_time = go.Figure([go.Scatter(x=cancel_over_time.index, y=cancel_over_time.values, line=dict(color='#000'), fill='tozeroy')])
        fig_time.update_layout(
            title={'text': 'Cancellations Over Time', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_time, use_container_width=True, config={'displayModeBar': False})

    with chart_col4:
        cancel_by_hour = filtered_df[filtered_df["Booking Status"].str.contains("Cancelled")].groupby("Hour").size()
        fig_hour = go.Figure([go.Bar(x=cancel_by_hour.index, y=cancel_by_hour.values, marker_color='#000')])
        fig_hour.update_layout(
            title={'text': 'Cancellations by Hour', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig_hour, use_container_width=True, config={'displayModeBar': False})

    cancel_by_vehicle_impact = filtered_df[filtered_df["Booking Status"].str.contains("Cancelled")].groupby("Vehicle Type")["Booking Value"].sum()
    fig_vehicle_impact = go.Figure([go.Bar(x=cancel_by_vehicle_impact.index, y=cancel_by_vehicle_impact.values, marker_color='#000')])
    fig_vehicle_impact.update_layout(
        title={'text': 'Revenue Loss by Vehicle Type', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
        height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white', showlegend=False
    )
    st.plotly_chart(fig_vehicle_impact, use_container_width=True, config={'displayModeBar': False})

elif selected == "RATINGS":
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min_date, key="ratings_start")
    with col2:
        end_date = st.date_input("End Date", max_date, key="ratings_end")
    
    filtered_df = df_clean[(df_clean["Date"].dt.date >= start_date) & (df_clean["Date"].dt.date <= end_date)]

    overall_cust_rating = filtered_df["Customer Rating"].mean().round(2)
    overall_driver_rating = filtered_df["Driver Ratings"].mean().round(2)
    rating_difference = (overall_cust_rating - overall_driver_rating).round(2)
    
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Overall Customer Rating</div>
                <div class="kpi-value" style="font-size: 22px;">⭐ {overall_cust_rating}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Overall Driver Rating</div>
                <div class="kpi-value" style="font-size: 22px;">⭐ {overall_driver_rating}</div>
            </div>
            """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Rating Difference</div>
                <div class="kpi-value" style="font-size: 22px;">{rating_difference}</div>
            </div>
            """, unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2, gap="medium")
    with chart_col1:

        fig_dist = px.histogram(filtered_df, x=["Customer Rating", "Driver Ratings"], barmode="overlay",
                                color_discrete_sequence=['#000', '#666'])
        fig_dist.update_layout(
            title={'text': 'Distribution of Ratings', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dist, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        daily_ratings = filtered_df.groupby("DateOnly").agg(
            avg_cust_rating=("Customer Rating", "mean"),
            avg_driver_rating=("Driver Ratings", "mean")
        ).reset_index()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=daily_ratings['DateOnly'], y=daily_ratings['avg_cust_rating'], mode='lines', name='Customer Rating', line=dict(color='#000')))
        fig_trend.add_trace(go.Scatter(x=daily_ratings['DateOnly'], y=daily_ratings['avg_driver_rating'], mode='lines', name='Driver Rating', line=dict(color='#666')))
        fig_trend.update_layout(
            title={'text': 'Average Daily Rating Trend', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})

    chart_col3, chart_col4 = st.columns(2, gap="medium")
    with chart_col3:
        avg_ratings_by_vehicle = filtered_df.groupby("Vehicle Type")["Customer Rating"].mean().sort_values(ascending=False)
        top_bottom_vehicles = pd.concat([avg_ratings_by_vehicle.head(5), avg_ratings_by_vehicle.tail(5)]).reset_index()
        top_bottom_vehicles['Performance'] = top_bottom_vehicles['Customer Rating'].apply(lambda x: 'Top 5' if x >= avg_ratings_by_vehicle.head(5).min() else 'Bottom 5')
        
        fig_top_bottom = px.bar(top_bottom_vehicles, x='Vehicle Type', y='Customer Rating', color='Performance',
                                title='Top/Bottom 5 Vehicle Types by Customer Rating',
                                color_discrete_map={'Top 5': '#000', 'Bottom 5': '#ccc'})
        fig_top_bottom.update_layout(
            title={'text': 'Top/Bottom 5 Vehicle Types by Customer Rating', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_top_bottom, use_container_width=True, config={'displayModeBar': False})
    
    with chart_col4:
        ratings_vs_value = filtered_df.groupby("Booking ID").agg(
            booking_value=("Booking Value", "mean"),
            customer_rating=("Customer Rating", "mean")
        ).reset_index()
        fig_scatter = px.scatter(ratings_vs_value, x="booking_value", y="customer_rating", title="Customer Rating vs. Booking Value",
                                 color_discrete_sequence=['#000'])
        fig_scatter.update_layout(
            title={'text': 'Customer Rating vs. Booking Value', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 14, 'color': '#000'}},
            height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white', plot_bgcolor='white'
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})