from datetime import datetime
import pandas as pd
import numpy as np
import requests
import urllib.parse
import csv
import sys
import coord

# Get the coordinate from address_cache, otherwise query the API
def fill_addr(transaction, blocks):
    # Iterate over each row in the DataFrame
    for index, row in transaction.iterrows():
        # Get the address from the 'block' and 'street_name' columns
        address = f"{row['block']} {row['street_name']}"

        # If address not in memo
        if blocks["address"].isin([address]).any() is False:
            print(f"{address} is not in, getting coordinates")
            x, y = coord.get_xy(address)
            x = float(x)
            y = float(y)

            if np.isnan(x) or np.isnan(y):
                print(f"Failed to get coordinates for {address}, exiting")
                sys.exit(1)

            # Stored the address into the memo
            new_addr_row = {"address": address, "x": x, "y": y}
            blocks.loc[blocks.index.max() + 1] = new_addr_row
        else:
            print(f"{address} is in")
        
if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage is parse_addr.py <resale_file.csv> <blocks.csv> <output.csv>")
        sys.exit(1)
    
    resale_csv = sys.argv[1]
    blocks_csv = sys.argv[2]
    output_csv = sys.argv[3]

    transactions = pd.read_csv(resale_csv)
    blocks = pd.read_csv(blocks_csv)
    fill_addr(transactions, blocks)

    # Write out to output csv
    blocks.to_csv(output_csv, index=False)


  