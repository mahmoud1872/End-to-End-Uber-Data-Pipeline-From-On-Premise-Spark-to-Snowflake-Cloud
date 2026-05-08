from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("Bronze_Layer_Ingestion") \
        .getOrCreate()

    local_csv_path = "/opt/airflow/data/landing_zone/*.csv"

    print("Reading raw CSV batches...")
    df = spark.read.csv(local_csv_path, header=True, inferSchema=True)

    if df.isEmpty():
        print("No new data found in landing zone.")
    else:
        hdfs_bronze_path = "hdfs://hadoop-namenode:9000/data/bronze/uber_data"
        print(f"Appending data to HDFS at {hdfs_bronze_path} in JSON format...")
        df.write.mode("append").json(hdfs_bronze_path)
        print("Completed Successfully!")
    
    spark.stop()

if __name__ == "__main__":
    main()
