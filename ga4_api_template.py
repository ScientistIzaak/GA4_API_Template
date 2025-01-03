# Imports
import pandas as pd
import time
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, Dimension, Metric, DateRange
from google.auth import exceptions as auth_exceptions
from google.oauth2 import service_account

# Set Request Parameters
dimension_arr = [
    # Replace with the desired dimensions, e.g., ['dimension1', 'dimension2']
]

measure_arr = [
    # Replace with the desired measures, e.g., ['measure1', 'measure2']
]

# Set start date, end date, and day duration
start_date_str = 'YYYY-MM-DD'  # Replace with the desired start date
end_date_str = 'YYYY-MM-DD'    # Replace with the desired end date

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

duration = (end_date - start_date).days


def run_report(property_id="YOUR_PROPERTY_ID", start_date=None, num_days=duration):
    """
    Fetches GA4 data for a specified property and date range.

    :param property_id: Google Analytics 4 property ID.
    :param start_date: Start date in YYYY-MM-DD format.
    :param num_days: Number of days to fetch data for.
    :return: DataFrame containing GA4 data.
    """
    # Load credentials from the 'credentials.json' file and specify the required scope
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/your/credentials.json',  # Replace with the path to your credentials file
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    
    # Create a BetaAnalyticsDataClient using the loaded credentials
    client = BetaAnalyticsDataClient(credentials=credentials)
    
    # Initialize an empty list to store data frames
    dfs = []

    # Loop through the specified range of dates
    for i in range(num_days):
        current_date = pd.to_datetime(start_date) + pd.DateOffset(days=i)
        current_date_str = current_date.strftime('%Y-%m-%d')

        # Specify the parameters for the API request using a RunReportRequest
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dimension) for dimension in dimension_arr],
            metrics=[Metric(name=measure) for measure in measure_arr],
            date_ranges=[DateRange(start_date=current_date_str, end_date=current_date_str)],
        )

        try:
            # Send the API request and get the response
            response = client.run_report(request)

            # Collect data from the API response
            data = []
            for row in response.rows:
                row_data = {}
                for i, dimension in enumerate(dimension_arr):
                    row_data[dimension] = row.dimension_values[i].value
                for i, measure in enumerate(measure_arr):
                    row_data[measure] = row.metric_values[i].value
                data.append(row_data)

            # Convert the list of dictionaries into a DataFrame
            df = pd.DataFrame(data)
            dfs.append(df)

            # Pause for 1 seconds before making the next API request
            time.sleep(1)

        except Exception as e:
            # Handle exceptions, e.g., print an error message
            print(f"Error: {e}")

    # Concatenate all data frames in the list vertically
    result_df = pd.concat(dfs, ignore_index=True)

    return result_df

# run for n days starting from start_date
final_df = run_report(start_date=start_date)

# Transform Date column to Datetime format
final_df['Date'] = pd.to_datetime(final_df['Date'])

# Group by year and create separate DataFrames
yearly_dfs = {year: group for year, group in final_df.groupby(final_df['Date'].dt.year)}

# Specify the base file path for the CSV files
base_csv_file_path = "ga_ga4_data_{}.csv"

# Loop through the years and save each DataFrame to a separate CSV file
for year, df in yearly_dfs.items():
    # Specify the file path for the CSV file
    csv_file_path = base_csv_file_path.format(year)
    
    # Save the DataFrame to the CSV file
    df.to_csv(csv_file_path, index=False)
    
    print(f"DataFrame for {year} saved to {csv_file_path}")
