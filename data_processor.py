import pandas as pd
import glob
import os

def process_data():
    # 1. Update the path to look inside the 'data' folder
    # If your files are in the same folder as the script, use './'
    # If they are in a subfolder, use './data/'
    data_path = './data/' 
    search_pattern = os.path.join(data_path, "daily_sales_data_*.csv")
    all_files = glob.glob(search_pattern)

    # DEBUG: Show what files were found
    print(f"Looking for files in: {os.path.abspath(data_path)}")
    print(f"Files found: {all_files}")

    if not all_files:
        print("ERROR: No CSV files found! Please ensure your CSVs are in the 'data' folder.")
        return

    df_list = []
    for filename in all_files:
        df_list.append(pd.read_csv(filename))

    # 2. Combine into one DataFrame
    df = pd.concat(df_list, ignore_index=True)

    # 3. Filter for Pink Morsels only
    df = df[df['product'].str.lower() == 'pink morsel']

    # 4. Clean price (remove $) and calculate sales
    # Using a safer replacement method
    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['sales'] = df['price'] * df['quantity']

    # 5. Keep only required columns and sort
    df = df[['sales', 'date', 'region']]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by="date")

    # 6. Export
    df.to_csv('formatted_data.csv', index=False)
    print("Success: formatted_data.csv has been created.")

if __name__ == '__main__':
    process_data()