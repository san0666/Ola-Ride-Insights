import mysql.connector

# Connect to Railway MySQL
conn = mysql.connector.connect(
    host="turntable.proxy.rlwy.net",
    port=32361,
    user="root",
    password="maUUVmXJlzlupYdWnDLyKIqFXQmjDsDV",
    database="railway"
)

cursor = conn.cursor()

# Create ola_rides table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ola_rides (
  date  DATETIME,
  time DATETIME,
  booking_id VARCHAR(50) PRIMARY KEY,
  booking_status VARCHAR(50),
  customer_id VARCHAR(50),
  vehicle_type VARCHAR(50),
  pickup_location VARCHAR(100),
  drop_location VARCHAR(100),
  v_tat FLOAT,
  c_tat FLOAT,
  canceled_rides_by_customer TEXT,
  canceled_rides_by_driver TEXT,
  incomplete_rides VARCHAR(10),
  booking_value FLOAT,
  payment_method VARCHAR(50),
  ride_distance FLOAT,
  driver_ratings FLOAT,
  customer_rating FLOAT,
  vehicle_images TEXT
);
""")

conn.commit()
cursor.close()
conn.close()

print("Table created in Railway!")
