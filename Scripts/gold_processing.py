from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws

def main():
    spark = SparkSession.builder \
        .appName("Gold_Layer_Processing") \
        .getOrCreate()

    bronze_path = "hdfs://hadoop-namenode:9000/data/bronze/uber_data"
    print("Reading data from Bronze layer...")
    df = spark.read.json(bronze_path)

    for c in df.columns:
        clean_col_name = c.replace(" ", "_")
        df = df.withColumnRenamed(c, clean_col_name)

    if "Date" in df.columns and "Time" in df.columns:
        df = df.withColumn("Date_Time", concat_ws(" ", df.Date, df.Time))
    
    print("Transforming data into Star Schema...")
    
    dim_customers = df.select("Customer_ID", "Customer_Rating").dropDuplicates(["Customer_ID"])
    dim_ride_details = df.select("Booking_ID", "Vehicle_Type", "Pickup_Location", "Drop_Location", "Payment_Method")
    
    fact_rides = df.select(
        "Booking_ID", "Customer_ID", "Date_Time", "Booking_Status", 
        "Booking_Value", "Ride_Distance", "Driver_Ratings"
    )

    gold_path_customers = "hdfs://hadoop-namenode:9000/data/gold/dim_customers"
    gold_path_ride_details = "hdfs://hadoop-namenode:9000/data/gold/dim_ride_details"
    gold_path_fact_rides = "hdfs://hadoop-namenode:9000/data/gold/fact_rides"

    print("Writing data to Gold layer in Parquet format using OVERWRITE...")
    
    dim_customers.write.mode("overwrite").parquet(gold_path_customers)
    dim_ride_details.write.mode("overwrite").parquet(gold_path_ride_details)
    fact_rides.write.mode("overwrite").parquet(gold_path_fact_rides)

    print("Completed Successfully!")
    spark.stop()

if __name__ == "__main__":
    main()
