# End-to-End-Uber-Data-Pipeline-From-On-Premise-Spark-to-Snowflake-Cloud

## Project Description
This is the final project for the Data Engineering program. It demonstrates a complete, automated ETL pipeline. I have successfully integrated core big data technologies on-premise with a cloud data warehouse, following industry best practices like the Medallion Architecture.

![Data Engineering](media/header.png)

## Core Tech Stack (Requirement #6 & #7)
*   **Orchestration:** Apache Airflow
*   **Processing:** Apache Spark (PySpark) with YARN (Cluster Manager)
*   **Data Lake:** HDFS (Hadoop Distributed File System)
*   **Data Warehouse:** Snowflake
*   **Containerization:** Docker

## Architecture Diagram
This technical map illustrates the data flow from the Landing Zone to the Cloud DWH:
![Architecture Diagram](diagrams/first.png)

## Data Modeling (DWH Schema)
The data is modeled into a Star Schema within Snowflake:
![DWH Schema Diagram](diagrams/star_schema.png)

### Facts & Dimensions:
*   **FACT_RIDES:** Stores metrics and metrics links.
*   **DIM_CUSTOMERS:** Customer-specific details.
*   **DIM_RIDE_DETAILS:** Categorical ride details (Vehicle Type, Payment, Location).

## Airflow Execution
The entire pipeline is automated and monitored by Airflow. Below is a confirmation of a successful DAG run:
![Airflow DAG Run](media/airflow.png)


## Final Output Validation
Here are live queries executed within Snowflake showing that the final data is clean and accurate (Handling Nulls, no duplication).

![Snowflake](snowflake/snowflake.png)


