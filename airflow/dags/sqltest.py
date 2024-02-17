from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.decorators import task, dag
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
import time
from datetime import datetime, timedelta
import pyodbc
import os
from subprocess import Popen, PIPE



default_args = {
    "start_date": datetime(2022, 1, 1)
}


@dag(
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False, dagrun_timeout=timedelta(minutes=10), concurrency=2, max_active_runs=1)
def my_dag():

    @task(task_id='testsql')
    def test_sql():
        # server="Server"
        # username="User"
        # password="Password"
        # database="master"
        # ddw_connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;')
        DEFAULT_DRIVER = "pyodbc"
        DEFAULT_ODBC_DRIVER = "ODBC Driver 17 for SQL Server"
        database={
        "name": "estaff_cut",
        "mssql.driver": "pyodbc",
        "pyodbc.config": "ODBC Driver 17 for SQL Server",
        "hostname": "t-estaff-dl.dellin.local",
        "port": "1433",
        "user": "dellin\\ashilo",
        "password": "eXB4021205Bia$"}

        password="eXB4021205Bia$"
        userid='ashilo'
        kinit = '/usr/bin/kinit'
        kinit_args = [ kinit, userid ]
        kinit = Popen(kinit_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        kinit.stdin.write( bytes('{}/n'.format(password) ,"UTF8"))

        kinit.wait()

        driver_config = database.get("pyodbc.config")
        connection_lnk_pyodbc = f"DRIVER={driver_config};" \
                                                       f"SERVER={database['hostname']};" \
                                                       f"DATABASE={database['name']};" \
                                                       f"APP=CDC Connector;" \
                                                       f"Encrypt=yes;" \
                                                       f"TrustServerCertificate=yes;" \
                                                       f"Authentication=ActiveDirectoryIntegrated;" \
                                                       f"UID={database['user']}"


        ddw_connection = pyodbc.connect(connection_lnk_pyodbc, autocommit=True)

        query1 = "select 1"
        print(query1)
        print(ddw_connection)
        cursor = ddw_connection.cursor()
        queryresult  = cursor.execute(query1)
   ##database_names    = [db.ddw_databasename for db in databases_to_sync]
        print(queryresult)

    test_sql()


sqltestdag = my_dag()
