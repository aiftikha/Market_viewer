import streamlit as st
import datetime
import pandas as pd
from lightweight_charts.widgets import StreamlitChart

# Set page configuration to control layout
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
        <style>
            .appview-container .main .block-container{{
                padding-top: {padding_top}px;
                padding-bottom: {padding_bottom}px;
                }}

        </style>""".format(
        padding_top=50, padding_bottom=50
    ),
    unsafe_allow_html=True,
)

st.title("Market Data Viewer")

# Function to load market data from CSV
def load_market_data(nasdaq_csv, spx_csv):
    nasdaq_data = pd.read_csv(nasdaq_csv, parse_dates=[['Date', 'Timestamp']])
    nasdaq_data['datetime'] = pd.to_datetime(nasdaq_data['Date_Timestamp'], format='%Y%m%d %H:%M:%S')
    nasdaq_data.drop(columns=['Date_Timestamp'], inplace=True)

    
    spx_data = pd.read_csv(spx_csv, parse_dates=[['Date', 'Timestamp']])
    spx_data['datetime'] = pd.to_datetime(spx_data['Date_Timestamp'], format='%Y%m%d %H:%M:%S')
    spx_data.drop(columns=['Date_Timestamp'], inplace=True)
    
    return nasdaq_data, spx_data

# Function to load news data
def load_news_data(news_csv):
    news_data = pd.read_csv(news_csv)
    news_data['datetime'] = pd.to_datetime(news_data['Date'] + ' ' + news_data['Time'], format='%Y/%m/%d %H:%M')
    return news_data

# Function to filter news by the selected date
def get_news_for_day(news_data, selected_date):
    return news_data[news_data['datetime'].dt.date == selected_date]

# Function to filter news by the selected date
def get_news_for_week(news_data, start, end):
    return news_data[(news_data['datetime'].dt.date >= start) & (news_data['datetime'].dt.date <= end)]

# Function to format data for lightweight-charts (candlestick format)
def format_candle_data(data):
    return [
        {
            'time': row.datetime.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to Unix timestamp (seconds)
            'open': row.Open,
            'high': row.High,
            'low': row.Low,
            'close': row.Close
        }
        for row in data.itertuples(index=False)
    ]

# Streamlit UI Elements

# File uploaders
with st.sidebar:
    st.header("File Upload Section")
    nasdaq_file = st.file_uploader("Upload NASDAQ CSV", type=["csv"])
    spx_file = st.file_uploader("Upload SPX CSV", type=["csv"])
    news_file = st.file_uploader("Upload News CSV", type=["csv"])
    
    # Initialize today's date
    today = datetime.date.today()
    
    # Select view mode (Day or Week)
    view_mode = st.sidebar.radio("View Mode", ["Day", "Week"])

# Initialize session_state if not already set



# Ensure all files are uploaded
if nasdaq_file and spx_file and news_file:
    if 'start_of_week' not in st.session_state:
        st.session_state.start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday of the current week
    if 'end_of_week' not in st.session_state:
        st.session_state.end_of_week = st.session_state.start_of_week + datetime.timedelta(days=6)  # Sunday of the current week

    if 'date_selector' not in st.session_state:
        st.session_state.date_selector = today
    # Load data from the CSVs
    nasdaq_data, spx_data = load_market_data(nasdaq_file, spx_file)
    news_data = load_news_data(news_file)

    # Handle different view modes
    if view_mode == "Day":
        # Show date selector when in Day view
        st.session_state.date_selector = st.sidebar.date_input("Select Date", st.session_state.date_selector)  # Default to today's date

        # Navigation buttons for prev/next day
        prev_day, next_day = st.columns([1, 1])

        with prev_day:
            if st.button("Previous Day"):
                st.session_state.date_selector = st.session_state.date_selector - datetime.timedelta(days=1)

        with next_day:
            if st.button("Next Day"):
                st.session_state.date_selector = st.session_state.date_selector + datetime.timedelta(days=1)
        nasdaq_day_data = nasdaq_data[nasdaq_data['datetime'].dt.date == st.session_state.date_selector]
        spx_day_data = spx_data[spx_data['datetime'].dt.date == st.session_state.date_selector]
    else:  # For Week view
        # Show date selector to select any date within the week
        st.session_state.date_selector = st.sidebar.date_input("Select Date in Week", st.session_state.date_selector)

        # Calculate the start (Monday) and end (Sunday) of the week for the selected date
        st.session_state.start_of_week = st.session_state.date_selector - datetime.timedelta(days=st.session_state.date_selector.weekday())  # Monday of selected week
        st.session_state.end_of_week = st.session_state.start_of_week + datetime.timedelta(days=6)  # Sunday of selected week

        # Display the full week range

        
        # Navigation buttons for prev/next week
        prev_week, next_week = st.columns([1, 1])

        with prev_week:
            if st.button("Previous Week"):
                st.session_state.date_selector = st.session_state.date_selector - datetime.timedelta(weeks=1)
                st.session_state.start_of_week = st.session_state.start_of_week - datetime.timedelta(weeks=1)
                st.session_state.end_of_week = st.session_state.start_of_week + datetime.timedelta(days=6) 

        with next_week:
            if st.button("Next Week"):
                st.session_state.date_selector = st.session_state.date_selector + datetime.timedelta(weeks=1)
                st.session_state.start_of_week = st.session_state.start_of_week + datetime.timedelta(weeks=1)
                st.session_state.end_of_week = st.session_state.start_of_week + datetime.timedelta(days=6) 

        nasdaq_day_data = nasdaq_data[(nasdaq_data['datetime'].dt.date >= st.session_state.start_of_week) & (nasdaq_data['datetime'].dt.date <= st.session_state.end_of_week)]
        spx_day_data = spx_data[(spx_data['datetime'].dt.date >= st.session_state.start_of_week) & (spx_data['datetime'].dt.date <= st.session_state.end_of_week)]
        st.sidebar.write(f"Week: {st.session_state.start_of_week} to {st.session_state.end_of_week}")




    # Initialize charts


    # Create the main chart for NASDAQ
    chart_nasdaq = StreamlitChart(inner_width=0.5, inner_height=1, height=600)  # Adjust width as needed
    chart_nasdaq.set(pd.DataFrame(format_candle_data(nasdaq_day_data)))
    chart_nasdaq.watermark(text= 'NQ')
    chart_n2 = chart_nasdaq.create_subchart(height=1, sync=True)
    chart_n2.set(pd.DataFrame(format_candle_data(spx_day_data)))
    chart_n2.watermark(text= 'ES')
    chart_nasdaq.load()
    
    # News filter options
    st.subheader("Filter News")
    impact_col, curr_col = st.columns([3, 1])
    # Filter by Impact (allowing multiple selections)
    with impact_col:
        impact_filter = st.multiselect(
            "Select Impact", 
            ["All", "H", "M", "L","N"], 
            default=["All"]
        )
        
    # Filter by Currency (Example)
    with curr_col:
        currency_filter = st.selectbox("Select Currency", ["All"] + news_data['Currency'].unique().tolist())
    
    # Filter news data based on selected filters
    filtered_news = news_data
    if "All" not in impact_filter:
        filtered_news = filtered_news[filtered_news['Impact'].isin(impact_filter)]
    
    if currency_filter != "All":
        filtered_news = filtered_news[filtered_news['Currency'] == currency_filter]

   
    if view_mode == "Day":
        # Filter news by selected date
        news_for_day = get_news_for_day(filtered_news, st.session_state.date_selector)
        
        # Display news with Impact
        st.subheader("News for " + str(st.session_state.date_selector))
        for _, row in news_for_day.iterrows():
            st.write(f"{row['datetime'].strftime('%Y/%m/%d %H:%M:%S')} - {row['Impact']} - **{row['Description']}**")
    else:
        # Filter news by selected date
        news_for_week = get_news_for_week(filtered_news, st.session_state.start_of_week,st.session_state.end_of_week)
        
        # Display news with Impact
        st.subheader("News for " + str(st.session_state.start_of_week) + " to " + str(st.session_state.end_of_week))
        for _, row in news_for_week.iterrows():
            st.write(f"{row['datetime'].strftime('%Y/%m/%d %H:%M:%S')} - {row['Impact']} - **{row['Description']}**")

else:
    st.write("Please upload all CSV files.")
