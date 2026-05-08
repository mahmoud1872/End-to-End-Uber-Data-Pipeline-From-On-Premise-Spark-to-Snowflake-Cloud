from pyspark.sql import SparkSession

def main():
    sf_options = {
        "sfURL": "BGCLVOD-MR85270.snowflakecomputing.com",
        "sfUser": "mElshennawy",
        "sfPassword": "Mahmoud94795704",
        "sfDatabase": "UBER_ETL_DB",
        "sfSchema": "GOLD_LAYER",
        "sfWarehouse": "COMPUTE_WH"
    }

    spark = SparkSession.builder \
        .appName("Load_to_Snowflake") \
        .getOrCreate()

    gold_tables = ["dim_customers", "dim_ride_details", "fact_rides"]

    for table in gold_tables:
        print(f"Reading {table} from HDFS...")
        hdfs_path = f"hdfs://hadoop-namenode:9000/data/gold/{table}"
        df = spark.read.parquet(hdfs_path)

        df = df.fillna(0)
        df = df.fillna("")

        print(f"Loading {table} to Snowflake...")
        df.write \
            .format("net.snowflake.spark.snowflake") \
            .options(**sf_options) \
            .option("dbtable", table.upper()) \
            .mode("overwrite") \
            .save()

    print("SUCCESS!")
    spark.stop()

if __name__ == "__main__":
    main()
