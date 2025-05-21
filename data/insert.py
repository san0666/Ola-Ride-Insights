import mysql.connector
import pandas as pd

# Load your CSV file
df = pd.read_csv("data/OLA_Cleaned_Final.csv")  # Ensure this file is in the same folder as the script

# Connect to Railway MySQL
conn = mysql.connector.connect(
    host="turntable.proxy.rlwy.net",
    port=32361,
    user="root",
    password="maUUVmXJlzlupYdWnDLyKIqFXQmjDsDV",
    database="railway"
)

cursor = conn.cursor()

# Insert data into ola_rides
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ola_rides (
            date, time, booking_id, booking_status, customer_id, vehicle_type,
            pickup_location, drop_location, v_tat, c_tat,
            canceled_rides_by_customer, canceled_rides_by_driver, incomplete_rides,
            booking_value, payment_method, ride_distance, driver_ratings,
            customer_rating, vehicle_images
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("All rows inserted into 'ola_rides' successfully!")
