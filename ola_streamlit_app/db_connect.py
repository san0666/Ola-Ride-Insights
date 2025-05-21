import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="turntable.proxy.rlwy.net",
        port=32361,
        user="root",
        password="maUUVmXJlzlupYdWnDLyKIqFXQmjDsDV",
        database="railway"
    )

