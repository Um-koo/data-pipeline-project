"""
airkorea_etl_dag.py

목적:
Airflow에서 AirKorea 데이터 적재 스크립트를 실행하기 위한 DAG 파일이다.

역할:
- Airflow UI에 DAG를 등록한다.
- BashOperator를 통해 Python 적재 스크립트를 실행한다.
- CSV -> PostgreSQL 적재 작업을 수동 실행할 수 있게 한다.

현재 구조:
Airflow DAG
    -> BashOperator
        -> load_to_postgres.py 실행

참고:
현재는 학습 및 검증 목적의 단일 Task 구조이며,
향후에는 extract / transform / load를 각각 분리한 다중 Task DAG로 확장할 수 있다.
"""

# 날짜/시간 객체
from datetime import datetime

# Airflow DAG 객체
from airflow import DAG

# Bash 명령 실행용 Operator
from airflow.operators.bash import BashOperator


# DAG 정의
with DAG(
    # Airflow UI에 표시될 DAG 이름
    dag_id="airkorea_etl_pipeline",

    # DAG 시작 기준 날짜
    # 과거 실행 이력을 만들기 위한 기준점 역할을 한다.
    start_date=datetime(2026, 3, 16),

    # 현재는 자동 스케줄 없이 수동 실행만 사용
    schedule=None,

    # 과거 날짜 기준으로 누락 실행을 자동 보충하지 않도록 설정
    catchup=False,

    # Airflow UI에서 DAG 검색 및 분류에 사용할 태그
    tags=["airkorea", "etl", "postgres"],
) as dag:

    # 단일 Task 정의
    # BashOperator를 이용해 Python 적재 스크립트를 실행한다.
    run_load_to_postgres = BashOperator(
        # Airflow UI에서 표시될 Task 이름
        task_id="run_load_to_postgres",

        # Airflow Docker 컨테이너 내부에서 실행할 명령
        # scripts 폴더가 /opt/airflow/scripts 로 마운트되어 있어야 한다.
        bash_command="python /opt/airflow/scripts/load_to_postgres.py",
    )
