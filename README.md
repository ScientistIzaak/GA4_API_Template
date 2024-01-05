# Google Analytics 4 Data Extraction Script

This Python script allows you to fetch data from Google Analytics 4 using the Google Analytics Data API. It is designed to be a template that can be easily customized for your specific requirements.

## Prerequisites

Before using this script, make sure you have the following:

  - **Google Analytics 4 Property ID:** Replace YOUR_PROPERTY_ID in the script with the actual Property ID for your Google Analytics 4 property.

  - **Service Account Credentials:** You need a service account and its corresponding JSON key file. Replace 'path/to/your/credentials.json' with the path to your JSON key file.

  - **Python Libraries:** Ensure you have the required Python libraries installed. You can install them using:

    ```bash
    pip install pandas google-auth google-analytics-data
    ```

## Usage

1. **Set Request Parameters:** Update the dimension_arr and measure_arr arrays in the script with the dimensions and measures you want to retrieve.

2. **Set Date Range:** Adjust the start_date_str and end_date_str variables to specify the date range for the data extraction.

3. **Run the Script:** Execute the script in your Python environment.

    ```bash
    python your_script_name.py
    ```
    
4. **Review Output:** The script will fetch data from Google Analytics 4 for the specified date range, dimensions, and measures. The results will be saved in separate CSV files for each year.

## Notes

  - The script includes a delay of 1 second between API requests to avoid rate limits.
  - Any errors encountered during the API requests will be printed to the console.









