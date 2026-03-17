"""
AirKorea Data Pipeline DAG

이 DAG는 AirKorea OpenAPI 데이터를 ETL 처리하여
PostgreSQL 데이터베이스에 적재하는 파이프라인이다.

파이프라인 흐름

AirKorea API
→ CSV 저장
→ PostgreSQL 적재

현재 DAG에서는 기존에 작성한 Python 스크립트
scripts/load_to_postgres.py 를 실행하여
CSV 데이터를 PostgreSQL로 적재한다.

작성 목적
Data Engineering Portfolio - Data Pipeline 구현
"""

# 날짜 및 시간 관련 객체
from datetime import datetime

# Airflow DAG 객체
from airflow import DAG

# Bash 명령을 실행하기 위한 Operator
from airflow.operators.bash import BashOperator


# DAG 정의 시작
with DAG(

    # Airflow UI에서 표시될 DAG 이름
    dag_id="airkorea_etl_pipeline",

    # DAG 시작 기준 날짜
    start_date=datetime(2026, 3, 16),

    # 자동 스케줄 설정
    # None → 수동 실행
    schedule=None,

    # 과거 실행(catchup) 방지
    catchup=False,

    # Airflow UI에서 DAG 분류용 태그
    tags=["airkorea", "etl", "postgres"],

) as dag:

    """
    Task 정의

    이 Task는 기존 Python 스크립트를 실행한다.
    """

    run_load_script = BashOperator(

        # Task 이름 (UI에 표시됨)
        task_id="run_load_to_postgres",

        # 실행할 명령어
        # Airflow Docker 컨테이너 내부에서 Python 실행
        bash_command="python /opt/airflow/scripts/load_to_postgres.py"

    )