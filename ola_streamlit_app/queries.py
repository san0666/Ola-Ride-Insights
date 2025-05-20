queries = {
    "1. Retrieve all successful bookings":
        "SELECT *, 'Successful Booking' AS booking_result FROM ola_rides WHERE booking_status = 'Success';",

    "2. Average ride distance for each vehicle type":
        "SELECT vehicle_type, ROUND(AVG(ride_distance), 1) AS avg_distance FROM ola_rides GROUP BY vehicle_type;",

    "3. Total number of cancelled rides by customers":
        "SELECT COUNT(*) AS total_cancellations FROM ola_rides WHERE canceled_rides_by_customer != 'No Info';",

    "4. Top 5 customers with highest ride bookings":
        "SELECT customer_id, COUNT(*) AS ride_count FROM ola_rides GROUP BY customer_id ORDER BY ride_count DESC LIMIT 5;",

    "5. Rides cancelled by drivers (personal/car issues)":
        "SELECT * FROM ola_rides WHERE canceled_rides_by_driver LIKE '%personal%' OR canceled_rides_by_driver LIKE '%car%';",

    "6. Max & Min driver ratings for Prime Sedan":
        "SELECT MAX(driver_ratings) AS max_rating, MIN(driver_ratings) AS min_rating FROM ola_rides WHERE vehicle_type = 'Prime Sedan';",

    "7. All rides paid using UPI":
        "SELECT *, 'UPI Payment' AS payment_info FROM ola_rides WHERE payment_method = 'UPI';",

    "8. Avg customer rating per vehicle type":
        "SELECT vehicle_type, ROUND(AVG(customer_rating), 2) AS avg_customer_rating FROM ola_rides GROUP BY vehicle_type;",

    "9. Total booking value of successful rides":
        "SELECT SUM(booking_value) AS total_value FROM ola_rides WHERE booking_status = 'Success';",

    "10. All incomplete rides with reasons":
        "SELECT * FROM ola_rides WHERE incomplete_rides != 'No Info';"
}
