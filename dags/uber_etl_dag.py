from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mahmoud',
    'start_date': datetime(2026, 5, 7),
    'retries': 1,
}

dag = DAG(
    'uber_etl_pipeline',
    default_args=default_args,
    description='Automated Uber ETL Pipeline',
    schedule_interval='*/5 * * * *', 
    catchup=False,
    max_active_runs=1
)

YARN_OPTS = (
    "--master local[*] "
    "--deploy-mode client "
    "--driver-memory 1G "
    "--executor-memory 1G "
    "--conf spark.yarn.stagingDir=hdfs://hadoop-namenode:9000/tmp/spark-staging "
    "--conf spark.yarn.jars=hdfs://hadoop-namenode:9000/spark-jars/* "
    "--conf spark.yarn.dist.archives=hdfs://hadoop-namenode:9000/spark-libs/pyspark.zip#pyspark,hdfs://hadoop-namenode:9000/spark-libs/py4j-0.10.9.7-src.zip#py4j "
    "--conf spark.executorEnv.PYTHONPATH=pyspark:py4j "
    "--conf spark.hadoop.yarn.resourcemanager.hostname=resourcemanager "
)

# 0. الـ Batcher
task_simulation = BashOperator(
    task_id='run_data_batcher',
    bash_command='python3 /opt/airflow/scripts/data_simulator.py',
    dag=dag,
)

# 1. Bronze
task_bronze = BashOperator(
    task_id='ingest_bronze_to_hdfs',
    bash_command=f'docker exec -i spark-jupyter spark-submit {YARN_OPTS} /opt/airflow/scripts/bronze_ingestion.py',
    dag=dag,
)

# 2. Gold
task_gold = BashOperator(
    task_id='process_gold_layer',
    bash_command=f'docker exec -i spark-jupyter spark-submit {YARN_OPTS} /opt/airflow/scripts/gold_processing.py',
    dag=dag,
)

# 3. Snowflake
task_snowflake = BashOperator(
    task_id='load_to_snowflake',
    bash_command=f'''docker exec -i spark-jupyter spark-submit {YARN_OPTS} \
        --jars /opt/spark/jars/snowflake-jdbc-3.16.1.jar,/opt/spark/jars/spark-snowflake_2.12-2.12.0-spark_3.3.jar \
        /opt/airflow/scripts/load_to_snowflake.py''',
    dag=dag,
)

# 4. Clean Up
task_cleanup = BashOperator(
    task_id='cleanup_landing_zone',
    bash_command='rm -f /opt/airflow/data/landing_zone/*.csv',
    dag=dag,
)

task_simulation >> task_bronze >> task_gold >> task_snowflake >> task_cleanup
