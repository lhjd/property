from datetime import datetime
import pandas as pd
import csv
import sys
import re

def str_to_years(date_str):
    # Split the string by space and strip whitespaces
    parts = [part.strip() for part in date_str.split()]
    
    # Extract the numeric values using regular expressions
    years = int(''.join(re.findall('\d+', parts[0])))
    months = 0
    if len(parts) >= 3:
        months = int(''.join(re.findall('\d+', parts[2])))
    
    # Convert months to fractional years (assuming 1 month = 1/12 year)
    years += months / 12.0
    
    return years

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage is parse_transactions.py <resale_file.csv> <output.csv>")
        sys.exit(1)
    
    resale_csv = sys.argv[1]
    output_csv = sys.argv[2]

    df = pd.read_csv(resale_csv)
    
    # # Add floor area in sqft
    df['floor_area_sqft'] = df['floor_area_sqm'] * 10.7639

    # Add price per square foot
    df['price_per_sqft'] = df['resale_price'] / df['floor_area_sqft']
    
    # Calculate remaining lease
    df['remaining_lease'] = df['remaining_lease'].apply(str_to_years)

    # Round down remaining lease
    df['remaining_lease_int'] = df['remaining_lease'].astype(int)

    # Write out to output csv
    df.to_csv(output_csv, index=False)


  