import pandas as pd
from sqlalchemy import create_engine

# --- Step 1: Load the cleaned CSV ---
csv_file = 'data/OLA_Cleaned_Final.csv'
df = pd.read_csv(csv_file)

# --- Step 2: Setup MySQL connection parameters ---
username = 'root'   # replace with your MySQL username
password = 'san2003'   # replace with your MySQL password
host = 'localhost'                 # replace with your MySQL host, e.g., 'localhost' or IP
port = '3306'                     # replace with your MySQL port, usually 3306
database = 'ola_db'               # your MySQL database name

# --- Step 3: Create SQLAlchemy engine for MySQL ---
engine_str = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(engine_str)

# --- Step 4: Load DataFrame into MySQL table ---
table_name = 'ola_rides'

try:
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"Data loaded successfully into MySQL table '{table_name}' in database '{database}'")
except Exception as e:
    print("Error loading data:", e)
