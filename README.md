# Uber Analytics Hub

A comprehensive and interactive analytics dashboard built with **Streamlit** to provide deep insights into ride-booking data from the NCR (National Capital Region). This application helps stakeholders visualize key metrics, identify trends, and make data-driven decisions related to business performance, customer behavior, and operational efficiency.

-----

## Key Features

  * **Overall Performance Dashboard:** Get a high-level view of total bookings, revenue, average ride distance, and more.
  * **Vehicle Type Analysis:** Analyze performance metrics like total revenue and distance traveled broken down by vehicle type.
  * **Revenue Insights:** Dive into revenue trends over time, by vehicle type, and by payment method.
  * **Cancellation Analysis:** Understand cancellation rates and identify the primary reasons behind customer and driver cancellations.
  * **Ratings and Feedback:** Monitor and analyze driver and customer ratings to assess service quality.
  * **Interactive Filters:** Use date ranges and categorical filters to customize your analysis.

-----

## Installation and Setup

This project requires a Python environment and a few key libraries. Follow these steps to get the app running on your local machine.

### Prerequisites

  * Python 3.8+
  * `ncr_ride_bookings.csv` (Please replace with your actual data source link)

### Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd uber-analytics-hub
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

      * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
      * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required libraries:**

    ```bash
    pip install streamlit pandas plotly
    ```

5.  **Place the data file:**
    Ensure your data file, `ncr_ride_bookings.csv`, is in the same directory as the `app.py` script. The application is configured to look for this file locally.

6.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

The application will automatically open in your default web browser.

-----

## Project Structure

```
uber-analytics-hub/
├── app.py              # Main Streamlit application script
├── ncr_ride_bookings.csv  # Dataset used for the analysis
└── README.md           # This file
```

-----

## Data and Methodology

The dashboard uses a dataset named `ncr_ride_bookings.csv`. The data is pre-processed within the `app.py` script to handle missing values, format dates and times, and convert data types for accurate analysis.

**Data Cleaning Steps:**

  * Missing values in "Ride Distance" and "Booking Value" are filled with 0.
  * Missing "Driver Ratings" and "Customer Rating" are filled with the mean of their respective columns.
  * Date and time columns are converted to proper datetime objects.
  * The "Vehicle Type" column is standardized to lowercase for consistent analysis.

-----

## Future Enhancements

  * Add a user authentication system to restrict access to the dashboard.
  * Integrate real-time data streaming to provide live analytics.
  * Include geospatial analysis to visualize booking heatmaps and popular routes.
  * Add predictive models to forecast future booking trends and demand.

-----

## Acknowledgements

  * **Streamlit**: For the powerful and easy-to-use framework for building data apps.
  * **Pandas**: The essential library for data manipulation and analysis.
  * **Plotly**: For creating professional and interactive data visualizations.

-----

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
