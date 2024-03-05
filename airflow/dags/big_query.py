Здравствуйте! Как я могу вам помочь сегодня?

напиши Apache airflow DAG для загрузки данных из Microsoft SQL на S3 хранилище в виде parquet

from airflow.operators.mssql_to_gcs import MsSqlToGoogleCloudStorageOperator
from airflow.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryOperator

# Загрузка данных из Microsoft SQL на S3 в виде parquet
mssql_to_gcs_parquet = MsSqlToGoogleCloudStorageOperator(
    task_id='mssql_to_gcs_parquet',
    sql='SELECT * FROM my_table',
    gcp_conn_id='google_cloud_default',
    mssql_conn_id='mssql_default',
    bucket='my-bucket',
    filename='my-file.parquet',
    schema_filename='my-schema.json',
    export_format='parquet'
)

# Перемещение данных из S3 в BigQuery
gcs_to_bq_parquet = GCSToBigQueryOperator(
    task_id='gcs_to_bq_parquet',
    bucket='my-bucket',
    source_objects=['my-file.parquet'],
    destination_dataset_table='my_dataset.my_table',
    schema_fields=[
        {'name': 'id', 'type': 'INTEGER'},
        {'name': 'name', 'type': 'STRING'},
        {'name': 'created_at', 'type': 'TIMESTAMP'}
    ],
    write_disposition='WRITE_TRUNCATE',
    source_format='PARQUET'
)

# Создание внешней таблицы в BigQuery
create_ext_table = BigQueryCreateExternalTableOperator(
    task_id='create_ext_table',
    table_resource={
        'tableReference': {
            'projectId': 'my-project',
            'datasetId': 'my_dataset',
            'tableId': 'my_ext_table'
        },
        'externalDataConfiguration': {
            'sourceUris': ['gs://my-bucket/my-file.parquet'],
            'schema': {
                'fields': [
                    {'name': 'id', 'type': 'INTEGER'},
                    {'name': 'name', 'type': 'STRING'},
                    {'name': 'created_at', 'type': 'TIMESTAMP'}
                ]
            }
        }
    }
)

# Запуск запроса BigQuery
bq_query = BigQueryOperator(
    task_id='bq_query',
    sql='SELECT * FROM my_dataset.my_table',
    use_legacy_sql=False
)

# Перемещение данных из BigQuery в S3
bq_to_gcs = BigQueryToGoogleCloudStorageOperator(
    task_id='bq_to_gcs',
    source_project_dataset_table='my-project.my_dataset.my_table',
    destination_bucket='my-bucket',
    destination_object_name='my-file.csv',
    export_format='CSV'
)

# Bash задача для дополнительных действий
bash_task = BashOperator(
    task_id='bash_task',
    bash_command='echo "Hello, world!"'
)

# Python задача для дополнительных действий
python_task = PythonOperator(
    task_id='python_task',
    python_callable=lambda: print('Hello, world!')
)
