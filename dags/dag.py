import pandas as pd
import csv
from airflow.decorators import dag,task
from datetime import datetime
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.models.baseoperator import chain
from astro import sql as aql
from astro.files import File
from astro.constants import FileType
from astro.sql.table  import Table,Metadata

from include.dbt.cosmos_config import DBT_CONFIG, DBT_PROJECT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig

@dag(
    start_date=datetime(2024,1,1),
    schedule=None,
    catchup=False,
    tags = ['retail']
)
def retail():
    
    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id = 'upload_csv_to_gcs',
        src = '/usr/local/airflow/include/dataset/Online_Retail.csv',
        dst = 'raw/online_retail.csv',
        bucket = 'zizheng_online_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )
    
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id = 'create_dataset',
        dataset_id = 'retail',
        gcp_conn_id='gcp',
    )
    

    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://zizheng_online_retail/raw/online_retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )
    
    @task.external_python(python = '/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath = 'sources'):
        from include.soda.check_function import check
        
        return check(scan_name, checks_subpath)
    
    # create_reporting_table = create_reporting_table(conn_id='gcp')
    
    transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        )
    )
    
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    
    report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        )
    )
    
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='report'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    
    chain(
        upload_csv_to_gcs,
        create_dataset,
        gcs_to_raw,
        check_load(),
        # create_reporting_table,
        transform,
        check_transform(),
        report,
        check_report(),
    )
    
retail()
