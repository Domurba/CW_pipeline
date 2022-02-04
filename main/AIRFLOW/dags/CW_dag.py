from DATABASE.to_DB_and_files import run_pipeline_in_order

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from pathlib import Path
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("GIT_REPO_SHH_URL")


def is_git_init():
    if (Path(__file__).parents[1] / 'plugins' / 'Push_to_github' / '.git').is_dir():
        return 'skip_init'
    return 'git_init'

def is_git_remote():
    git = subprocess.run(
        'git remote show', capture_output=True, cwd=(Path(__file__).parents[1] / 'plugins' / 'Push_to_github' ), shell=True)
    if git.stdout.decode():
        return 'skip_remote'
    return 'git_remote_add'

with DAG(
    dag_id="CW_DAG",
    # At minute 0 past every 2nd hour from 0 through 23
    schedule_interval="0 0/2 * * *",
    start_date=days_ago(1),
    catchup=False,
) as dag:
    t1 = PythonOperator(
        task_id="run_ETL",
        provide_context=True,
        python_callable=run_pipeline_in_order,
        op_kwargs={"Username": "Kolhelma"},
    )
    t2 = BranchPythonOperator(
        task_id='Branch_git_init', 
        python_callable=is_git_init,
    )
    t3 = BashOperator(
        task_id='git_init',
        bash_command="cd /opt/airflow/plugins/Push_to_github && git init"
    )
    t4 = BashOperator(
        task_id='git_commit',
        bash_command="cd /opt/airflow/plugins/Push_to_github && git add . && git commit -m 'auto commit'; exit 0 ",
        trigger_rule='one_success'
    )
    t5=BranchPythonOperator(
        task_id='Branch_git_remote', 
        python_callable=is_git_remote
    )
    t6=BashOperator(
        task_id='git_remote_add',
        bash_command=f"cd /opt/airflow/plugins/Push_to_github && git remote add origin {URL}"
    )
    t7=BashOperator(
        task_id='git_push',
        bash_command="cd /opt/airflow/plugins/Push_to_github && git push --force origin master",
        trigger_rule='one_success'
    )
    dummy1 =  DummyOperator(task_id='skip_init')
    dummy2 =  DummyOperator(task_id='skip_remote')

    t1 >> t2 >> [t3, dummy1] >> t4 >> t5 >> [t6, dummy2] >> t7