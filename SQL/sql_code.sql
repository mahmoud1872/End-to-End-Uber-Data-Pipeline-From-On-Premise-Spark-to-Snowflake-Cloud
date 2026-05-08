-----------------------------------------------------------  1  --------------------------------------------------------------------------

CREATE OR REPLACE DATABASE UBER_ETL_DB;
CREATE OR REPLACE SCHEMA UBER_ETL_DB.GOLD_LAYER;

USE DATABASE UBER_ETL_DB;
USE SCHEMA GOLD_LAYER;

CREATE OR REPLACE TABLE DIM_CUSTOMERS (
    CUSTOMER_ID     STRING,
    CUSTOMER_RATING FLOAT
);

CREATE OR REPLACE TABLE DIM_RIDE_DETAILS (
    BOOKING_ID      STRING,
    VEHICLE_TYPE    STRING,
    PICKUP_LOCATION STRING,
    DROP_LOCATION   STRING,
    PAYMENT_METHOD  STRING
);

CREATE OR REPLACE TABLE FACT_RIDES (
    BOOKING_ID     STRING,
    CUSTOMER_ID    STRING,
    DATE_TIME      TIMESTAMP,
    BOOKING_STATUS STRING,
    BOOKING_VALUE  FLOAT,
    RIDE_DISTANCE  FLOAT,
    DRIVER_RATINGS FLOAT
);

SHOW TABLES;



-----------------------------------------------------------  2  --------------------------------------------------------------------------

SELECT * FROM FACT_RIDES LIMIT 10;

SELECT COUNT(*) AS TOTAL_RIDES FROM FACT_RIDES;

SELECT 
    BOOKING_STATUS, 
    COUNT(*) AS STATUS_COUNT,
    ROUND(AVG(BOOKING_VALUE), 2) AS AVG_VALUE
FROM FACT_RIDES 
GROUP BY 1
ORDER BY STATUS_COUNT DESC;



-----------------------------------------------------------  3  --------------------------------------------------------------------------

TRUNCATE TABLE FACT_RIDES;
TRUNCATE TABLE DIM_CUSTOMERS;
TRUNCATE TABLE DIM_RIDE_DETAILS;
