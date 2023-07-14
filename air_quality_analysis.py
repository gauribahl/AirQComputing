import requests
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg

def fetch_openaq_data(country_code, limit):
    """
    Fetches air quality data from OpenAQ API based on user preferences.
    Returns a DataFrame containing the retrieved data.
    """
    url = 'https://api.openaq.org/v1/measurements'
    params = {
        'country': country_code,
        'limit': limit,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'results' in data:
        df = pd.DataFrame(data['results'])
        return df
    else:
        print('Error: No results found in the API response.')
        return pd.DataFrame()  # Return an empty DataFrame

def clean_data(df):
    """
    Cleans the air quality data by handling missing values, outliers, and inconsistencies.
    Returns the cleaned DataFrame.
    """
    # Drop rows with missing values
    df.dropna(subset=['value'], inplace=True)

    # Remove outliers (you can modify this based on your specific requirements)
    df = df[(df['value'] >= 0) & (df['value'] <= 1000)]

    # Handle inconsistencies, if any
    # ...

    return df

def analyze_data(df):
    """
    Performs correlation analysis and identifies trends or patterns in the data.
    """
    if df.empty:
        print("No data available for correlation analysis.")
        return None

    # Select numeric columns for correlation calculation
    numeric_cols = df.select_dtypes(include='number')

    if numeric_cols.empty:
        print("No numeric columns available for correlation analysis.")
        return None

    # Calculate correlations
    correlations = numeric_cols.corr()

    # Identify trends or patterns
    # ...

    return correlations


# Create the GUI layout
layout = [
    [sg.Text('Country Code:'), sg.Input(key='-COUNTRY_CODE-')],
    [sg.Text('Limit:'), sg.Input(key='-LIMIT-')],
    [sg.Button('Fetch Data')]
]

# Create the window
window = sg.Window('Air Quality Data Analysis', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Fetch Data':
        country_code = values['-COUNTRY_CODE-']
        limit = int(values['-LIMIT-'])

        # Fetch the data from OpenAQ API
        air_quality_data = fetch_openaq_data(country_code, limit)

        # Clean the data
        cleaned_data = clean_data(air_quality_data)

        # Analyze the data
        correlation_results = analyze_data(cleaned_data)

        # Print the correlation matrix
        print(correlation_results)

     
        # Convert 'location' column to categorical variable
        cleaned_data['location'] = pd.Categorical(cleaned_data['location'])

        # Create a color map based on the number of unique categories in 'location' column
        cmap = plt.get_cmap('Set3', len(cleaned_data['location'].cat.categories))

        # Create the scatter plot with assigned colors
        plt.figure(figsize=(10, 6))
        plt.scatter(cleaned_data['parameter'], cleaned_data['value'], c=cleaned_data['location'].cat.codes, cmap=cmap)
        plt.xlabel('Parameter')
        plt.ylabel('Value')
        plt.title('Air Quality Scatter Plot for US')
        plt.colorbar(label='Location')
        plt.show()
        
window.close()
