# Market_viewer
It's a streamlit tool to view historical market data at the 1 minute resolution. Allows you to load/render upto 1 week at a time and lets you navigate through.

# Getting Started
1. Launch the streamlit app
2. Download data files from "Tickstory"
3. Download news file "https://robots4forex.com/historical-forex-economic-calendar-2007-present-csv-format/"
2. Upload files for your data assets into the app
3. Select date/date range

# Background
Popular charting tools such as "tradingview.com" only let you view up to 1 month on the 1-minute resolution. I needed a tool to let me see histoical data, say from 5 years ago, at the 1 minute resolution. 
It is built on the python wrapper for tradingviews's "Lightweight Charts" library.

# Intended Functionality
I built this tool specifically to let me view Nasdaq and S&P500 data side by side, on a synchronized chart. It also displays economic news that occured on selected date range, along with timestamps.
It can however view any two assets side-by-side. It is intended to run on your local machine, as I have no interest in web data hosting.

# Limitations
1. It looks for 3 files before rendering, one file for asset 1, one for asset 2, one for news.
2. If you need to view just 1 asset, upload an empty file, or just the same file again.
3. Same applies for news file upload. If you don't have news data, try an empty file
4. Hardcoded watermark on the chart, this was what I needed when I built it but seems redundant now.
5. All timezones are in America/NewYork.
6. There is no option to resample into a different resolution.

# Future Improvements
1. Integrate with snowlfake or polygon.io.
2. Dyanamic subcharts instead of two charts hardcoded.
3. Dynamic asset name watermark.
4. Selecting news filter should not re-render the charts.
5. Option to not upload a news file.

# Screenshot
![Alt text](/screenshot/screenshot.png?raw=true)