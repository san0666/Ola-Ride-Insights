# eda_cleaning.py

import pandas as pd

# 1. Load the Excel file
df = pd.read_excel("data/OLA_DataSet.xlsx")

# 2. Display basic info
print("Initial Shape:", df.shape)
print("Column Names:", df.columns.tolist())

# 3. Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 4. Drop column with the MOST null values
null_counts = df.isnull().sum()
most_null_column = null_counts.idxmax()
print(f"Dropping column with most nulls: {most_null_column} ({null_counts[most_null_column]} nulls)")
df.drop(columns=[most_null_column], inplace=True)

# 5. Drop rows with all nulls (if any)
df.dropna(how='all', inplace=True)

datetime_columns = []
# 6. Fill or convert all other columns
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            converted = pd.to_datetime(df[col], errors='raise', dayfirst=True)
            df[col] = converted
            datetime_columns.append(col)
            print(f" Converted '{col}' to datetime.")
        except:
            df[col] = df[col].astype(str).str.strip().str.lower().fillna('unknown')
    elif df[col].dtype in ['float64', 'int64']:
        df[col] = df[col].fillna(df[col].median())
    else:
        df[col] = df[col].fillna('unknown')

# Now generate new features only for valid datetime columns
for col in datetime_columns:
    df[f'{col}_month'] = df[col].dt.month
    df[f'{col}_weekday'] = df[col].dt.day_name()

# 8. Final check
print("Final Shape:", df.shape)
print("Remaining Missing:\n", df.isnull().sum())

# 9. Save cleaned dataset to CSV
df.to_csv("data/OLA_Cleaned.csv", index=False)
print("Cleaned dataset saved as data/OLA_Cleaned.csv")
