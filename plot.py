from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import csv
import sys

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage is plot.py <resale_file.csv>")
        sys.exit(1)
    
    df = pd.read_csv(sys.argv[1])

    town = ''
    flat_type = '3 ROOM'
    months_ago = 24

    # Convert months to panda's time format 
    df['month'] = pd.to_datetime(df['month'])
    period_ago = pd.Timestamp.today() - pd.DateOffset(months=months_ago)
    
    query = df
    # Perform query is there is a town
    if town:
        query = query[query['town'] == town]
    query = query[query['flat_type'] == flat_type]
    query = query[query['flat_model'] != 'Premium Apartment']
    query = query[query['flat_model'] != 'Premium Apartment Loft']
    query = query[query['month'] >= period_ago]

    print(query)

    flat_counts = query['remaining_lease_int'].value_counts().sort_index(ascending=False)
    print(flat_counts)
    
    plt.figure(figsize=(12, 8))
    sb = sns.boxplot(x='remaining_lease_int', y='price_per_sqft', data=query)
    sb.invert_xaxis()

    town_title = 'ALL TOWNS'
    if town: 
        town_title = town

    title = "Price Per Square Foot vs Remaining Lease for {} Flats in {}, with transactions from {} months ago".format(flat_type, town_title, months_ago)
    plt.title(title)
    plt.xlabel('Remaining Lease (Years)')
    plt.ylabel('Price Per Square Foot (SGD)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    plt.show()


  