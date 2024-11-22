#Please read this documentation for the datacbricks implementation:

#https://docs.databricks.com/en/jobs/how-to/use-airflow-with-jobs.html

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.utils.dates import days_ago

default_args = {
  'owner': 'alejandro'
}

with DAG('databricks_dag',
  start_date = days_ago(2),
  schedule_interval = '0 0 * * 0', #Runs once a week on Sunday at midnight Ref.: https://airflow.apache.org/docs/apache-airflow/1.10.1/scheduler.html
  default_args = default_args
  ) as dag:

  opr_run_now = DatabricksRunNowOperator(
    task_id = 'run_now',
    databricks_conn_id = 'databricks_default',
    job_id = 'Undefined' #Not yet defined
  )

  opr_run_now