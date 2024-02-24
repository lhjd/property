import pandas as pd
import numpy as np
import requests
import urllib.parse
import time
import json
import csv

# Function to get x and y from OneMap API
def get_xy(address):
    # URL encode the address
    address_encoded = urllib.parse.quote(address)

    # Define the URL for the OneMap API
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={address_encoded}&returnGeom=Y&getAddrDetails=Y"
    
    # Send a GET request to the OneMap API
    response = requests.get(url)

    # Handle the case where the usage limit has been reached
    if response.status_code == 429:
        print("Usage limit reached. Sleeping for one hour...")
        for i in range(3600, 0, -1):
            time.sleep(1)
            print(f"Resuming in {i} seconds...", end='\r')
    elif response.status_code != 200:
        print(f"Error getting coordinates for address {address}: {response.status_code}")
        return np.nan, np.nan
    
    # Parse the JSON response
    data = response.json()

    if len(data['results']) == 0:
        print(f"No data found for {address}")
        return np.nan, np.nan

    # Get the latitude and longitude
    x = data['results'][0]['X']
    y = data['results'][0]['Y']

    return x, y