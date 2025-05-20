import pandas as pd
import numpy as np
import re

# Load CSV
file_path = 'data/OLA_Cleaned.csv'
df = pd.read_csv(file_path)

print("Initial shape:", df.shape)

# Step 1: Show missing values
print("\n Missing Values:")
print(df.isnull().sum())

# Step 2: Drop duplicates if any
duplicates = df.duplicated().sum()
print(f"\n Duplicate rows: {duplicates}")
if duplicates > 0:
    df.drop_duplicates(inplace=True)

# Step 3: Rename columns to be SQL-friendly
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace(r'[^\w_]', '', regex=True)
)
print("\n Cleaned Column Names:")
print(df.columns.tolist())

# Step 4: Parse date/time columns safely
date_time_cols = [col for col in df.columns if 'date' in col or 'time' in col]
for col in date_time_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Step 5: Handle missing values without creating new columns
problem_cols = ['canceled_rides_by_customer', 'canceled_rides_by_driver', 'incomplete_rides']
for col in problem_cols:
    if col in df.columns:
        # Fill missing with a string placeholder
        df[col] = df[col].fillna('No Info')

# Step 6: Fill missing values in payment_method similarly
if 'payment_method' in df.columns:
    df['payment_method'] = df['payment_method'].fillna('Unknown')

 
# *** Add this to check missing values after filling ***
print("\n Missing Values after filling:")
print(df.isnull().sum())
# Step 7: Check for special characters in text columns
print("\n Checking for special characters in text columns:")
for col in df.select_dtypes(include='object').columns:
    if df[col].str.contains(r'[,\n\r\"\']').any():
        print(f" Potential special characters in column: {col}")

# Step 8: Show final data types
print("\n Final Data Types:")
print(df.dtypes)

# Step 9: Export cleaned dataframe to CSV
final_path = 'data/OLA_Cleaned_Final.csv'
df.to_csv(final_path, index=False, encoding='utf-8')
print(f"\n Cleaned file saved as: {final_path}")
