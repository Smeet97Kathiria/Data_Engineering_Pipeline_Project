from datetime import timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['NHATT416@GMAIL.COM'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': airflow.utils.dates.days_ago(0),
    #'retries': 1,
    #'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

EMR_CLUSTER_ID = '{emr_cluster_id_here}'

# TODO think of solution (and function) to dynamically calculate amount of resources
# (e.g. num-executors, executor-memory, executor-cores, etc.) to allocate to
# the given job 
SPARK_STEPS = [
    {
        'Name': 'wcd_data_processing_engine',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                '/usr/bin/spark-submit',
                '--class', 'Driver.MainApp',
                '--master', 'yarn',
                '--deploy-mode', 'cluster',
                '--num-executors', '2',
                '--executor-memory', '3g',
                '--driver-memory', '1g',
                '--executors-cores', '2',
                's3://demo-wcd/wcd_final_project_2.11-0.1.jar', # artifact
                '-p', 'wcd-demo',
                '-t', 'Csv' # should have a function to dynamically set this parameter based on file extension
                '-o', 'parquet',
                # TODO: change this to parse s3 location with incoming event that triggers Lambda function 
                '-s', 's3://demo-wcd/banking.csv',
                '-d', 's3://demo-wcd/data',
                '-c', 'job',
                '-m', 'append',
                '--input_options', 'header=true'
                ]
        }
    }
]

with DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
    )
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beggining of the DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
        params={'my_param': 'Parameter I passed in'},
    )

    t1 >> [t2, t3]